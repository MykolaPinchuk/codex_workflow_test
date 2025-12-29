from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import statistics
from typing import Any

from .dgps import list_dgps
from .runner import RunConfig, XGBConfig, run_experiment


def _parse_csv_list(value: str) -> list[str]:
    items = [item.strip() for item in value.split(",")]
    return [item for item in items if item]


def _parse_int_list(value: str) -> list[int]:
    return [int(item) for item in _parse_csv_list(value)]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m dgp_xgb.sweep",
        description="Run a small sweep across DGPs and training sizes; writes a compact summary table.",
    )

    parser.add_argument(
        "--dgps",
        type=str,
        default="all",
        help="Comma-separated DGP names or 'all'.",
    )
    parser.add_argument(
        "--n-train-list",
        type=str,
        default="200,500,1000,2000,5000",
        help="Comma-separated training sizes.",
    )
    parser.add_argument("--n-test", type=int, default=2000)
    parser.add_argument("--seeds", type=str, default="0,1,2")
    parser.add_argument("--noise-std", type=float, default=0.1)
    parser.add_argument(
        "--backend",
        type=str,
        default="baseline_mean",
        choices=["baseline_mean", "xgboost"],
        help="Model backend.",
    )
    parser.add_argument("--out-root", type=Path, default=Path("sweeps"))
    parser.add_argument("--sweep-id", type=str, required=True, help="Directory name under out-root.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned runs and exit.")
    parser.add_argument(
        "--report",
        action="store_true",
        help="Write `report.md` (aggregated across seeds) next to `summary.csv`.",
    )

    parser.add_argument("--xgb-max-depth", type=int, default=2)
    parser.add_argument("--xgb-eta", type=float, default=0.1)
    parser.add_argument("--xgb-subsample", type=float, default=0.8)
    parser.add_argument("--xgb-colsample-bytree", type=float, default=0.8)
    parser.add_argument("--xgb-rounds", type=int, default=50)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    available_dgps = [dgp.name for dgp in list_dgps()]
    if args.dgps == "all":
        dgps = available_dgps
    else:
        dgps = _parse_csv_list(args.dgps)
        unknown = [name for name in dgps if name not in available_dgps]
        if unknown:
            parser.error(f"Unknown DGP(s): {', '.join(unknown)}")

    n_train_list = _parse_int_list(args.n_train_list)
    seeds = _parse_int_list(args.seeds)

    planned = [(dgp, n_train, seed) for dgp in dgps for n_train in n_train_list for seed in seeds]
    if args.dry_run:
        for dgp, n_train, seed in planned:
            print(f"{dgp}\tn_train={n_train}\tseed={seed}")
        return 0

    sweep_dir = args.out_root / args.sweep_id
    sweep_dir.mkdir(parents=True, exist_ok=False)

    xgb_config = XGBConfig(
        max_depth=args.xgb_max_depth,
        eta=args.xgb_eta,
        subsample=args.xgb_subsample,
        colsample_bytree=args.xgb_colsample_bytree,
        num_boost_round=args.xgb_rounds,
    )

    summary_path = sweep_dir / "summary.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "run_id",
                "dgp",
                "n_train",
                "n_test",
                "seed",
                "noise_std",
                "backend",
                "train_mse",
                "train_rmse",
                "train_r2",
                "test_mse",
                "test_rmse",
                "test_r2",
                "run_dir",
            ],
        )
        writer.writeheader()

        for dgp, n_train, seed in planned:
            run_id = f"{dgp}__n{n_train}__seed{seed}"
            config = RunConfig(
                dgp=dgp,
                n_train=n_train,
                n_test=args.n_test,
                seed=seed,
                noise_std=args.noise_std,
                backend=args.backend,
                xgb=xgb_config,
            )
            artifacts = run_experiment(config=config, out_root=sweep_dir, run_id=run_id)

            metrics_payload = json.loads(artifacts.metrics_path.read_text(encoding="utf-8"))
            train = metrics_payload["train"]
            test = metrics_payload["test"]

            writer.writerow(
                {
                    "run_id": run_id,
                    "dgp": dgp,
                    "n_train": n_train,
                    "n_test": args.n_test,
                    "seed": seed,
                    "noise_std": args.noise_std,
                    "backend": args.backend,
                    "train_mse": train["mse"],
                    "train_rmse": train["rmse"],
                    "train_r2": train["r2"],
                    "test_mse": test["mse"],
                    "test_rmse": test["rmse"],
                    "test_r2": test["r2"],
                    "run_dir": str(artifacts.run_dir),
                }
            )

    _write_metadata(
        sweep_dir / "sweep.json",
        {
            "sweep_id": args.sweep_id,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "dgps": dgps,
            "n_train_list": n_train_list,
            "n_test": args.n_test,
            "seeds": seeds,
            "noise_std": args.noise_std,
            "backend": args.backend,
            "xgb": {
                "max_depth": xgb_config.max_depth,
                "eta": xgb_config.eta,
                "subsample": xgb_config.subsample,
                "colsample_bytree": xgb_config.colsample_bytree,
                "num_boost_round": xgb_config.num_boost_round,
            },
        },
    )

    if args.report:
        _write_report(sweep_dir=sweep_dir, summary_path=summary_path)

    print(str(sweep_dir))
    return 0


def _write_metadata(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


@dataclass(frozen=True)
class _AggRow:
    dgp: str
    n_train: int
    n: int
    test_r2_mean: float
    test_r2_std: float
    test_rmse_mean: float
    test_rmse_std: float


def _write_report(*, sweep_dir: Path, summary_path: Path) -> None:
    rows = _read_summary(summary_path)
    aggregated = _aggregate_rows(rows)

    report_path = sweep_dir / "report.md"
    lines: list[str] = [
        f"# Sweep `{sweep_dir.name}`",
        "",
        "- Aggregation: mean/std across seeds per `(dgp, n_train)`.",
        "- Source: `summary.csv`.",
        "",
    ]

    for dgp in sorted({row.dgp for row in aggregated}):
        lines.extend(
            [
                f"## `{dgp}`",
                "",
                "| n_train | n | test_r2_mean | test_r2_std | test_rmse_mean | test_rmse_std |",
                "|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for row in sorted((r for r in aggregated if r.dgp == dgp), key=lambda r: r.n_train):
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(row.n_train),
                        str(row.n),
                        _fmt(row.test_r2_mean),
                        _fmt(row.test_r2_std),
                        _fmt(row.test_rmse_mean),
                        _fmt(row.test_rmse_std),
                    ]
                )
                + " |"
            )
        lines.append("")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _fmt(value: float) -> str:
    if value != value:
        return "nan"
    return f"{value:.6g}"


def _read_summary(summary_path: Path) -> list[dict[str, str]]:
    with summary_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [dict(row) for row in reader]


def _aggregate_rows(rows: list[dict[str, str]]) -> list[_AggRow]:
    groups: dict[tuple[str, int], list[dict[str, str]]] = {}
    for row in rows:
        dgp = row["dgp"]
        n_train = int(row["n_train"])
        groups.setdefault((dgp, n_train), []).append(row)

    aggregated: list[_AggRow] = []
    for (dgp, n_train), group in groups.items():
        test_r2_values = [float(item["test_r2"]) for item in group]
        test_rmse_values = [float(item["test_rmse"]) for item in group]
        aggregated.append(
            _AggRow(
                dgp=dgp,
                n_train=n_train,
                n=len(group),
                test_r2_mean=statistics.fmean(test_r2_values),
                test_r2_std=_std(test_r2_values),
                test_rmse_mean=statistics.fmean(test_rmse_values),
                test_rmse_std=_std(test_rmse_values),
            )
        )
    return aggregated


def _std(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return statistics.stdev(values)


if __name__ == "__main__":
    raise SystemExit(main())
