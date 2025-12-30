from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from .backends import BackendResult, predict_baseline_mean, predict_xgboost
from .dgps import get_dgp, resolve_dgp_params
from .metrics import regression_metrics


@dataclass(frozen=True)
class XGBConfig:
    max_depth: int = 2
    eta: float = 0.1
    subsample: float = 0.8
    colsample_bytree: float = 0.8
    num_boost_round: int = 50


@dataclass(frozen=True)
class RunConfig:
    dgp: str
    dgp_params: dict[str, float]
    n_train: int
    n_test: int
    seed: int
    noise_std: float
    backend: str
    xgb: XGBConfig


@dataclass(frozen=True)
class RunArtifacts:
    run_dir: Path
    config_path: Path
    metrics_path: Path
    summary_path: Path


def _default_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_experiment(config: RunConfig, out_root: Path, *, run_id: str | None = None) -> RunArtifacts:
    run_id_value = run_id or _default_run_id()
    run_dir = out_root / run_id_value
    run_dir.mkdir(parents=True, exist_ok=False)

    dgp = get_dgp(config.dgp)
    dgp_params = resolve_dgp_params(dgp, config.dgp_params)
    x_train, y_train = dgp.generate(config.n_train, config.seed, config.noise_std, dgp_params)
    x_test, y_test = dgp.generate(config.n_test, config.seed + 1, config.noise_std, dgp_params)

    backend_result: BackendResult
    if config.backend == "baseline_mean":
        backend_result = predict_baseline_mean(y_train=y_train, n_test=len(y_test))
    elif config.backend == "xgboost":
        backend_result = predict_xgboost(
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            seed=config.seed,
            max_depth=config.xgb.max_depth,
            eta=config.xgb.eta,
            subsample=config.xgb.subsample,
            colsample_bytree=config.xgb.colsample_bytree,
            num_boost_round=config.xgb.num_boost_round,
        )
    else:
        raise ValueError(f"Unknown backend '{config.backend}'")

    train_metrics = regression_metrics(y_true=y_train, y_pred=backend_result.y_pred_train)
    test_metrics = regression_metrics(y_true=y_test, y_pred=backend_result.y_pred_test)

    config_path = run_dir / "config.json"
    metrics_path = run_dir / "metrics.json"
    summary_path = run_dir / "summary.md"

    _write_json(
        config_path,
        {
            "run_id": run_id_value,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "config": asdict(config),
        },
    )
    _write_json(
        metrics_path,
        {
            "dgp": dgp.name,
            "backend": backend_result.backend,
            "backend_info": backend_result.backend_info,
            "train": asdict(train_metrics),
            "test": asdict(test_metrics),
        },
    )
    summary_path.write_text(
        "\n".join(
            [
                f"# Run {run_id_value}",
                "",
                f"- DGP: `{dgp.name}` — {dgp.description}",
                f"- DGP params: {json.dumps(dgp_params, sort_keys=True)}",
                f"- Backend: `{backend_result.backend}`",
                f"- Train: n={config.n_train}, noise_std={config.noise_std}",
                f"- Test: n={config.n_test}, noise_std={config.noise_std}",
                "",
                "## Metrics (test)",
                f"- mse: {test_metrics.mse:.6g}",
                f"- rmse: {test_metrics.rmse:.6g}",
                f"- r2: {test_metrics.r2:.6g}",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    return RunArtifacts(
        run_dir=run_dir,
        config_path=config_path,
        metrics_path=metrics_path,
        summary_path=summary_path,
    )
