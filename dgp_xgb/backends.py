from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import platform
import sys


@dataclass(frozen=True)
class BackendResult:
    backend: str
    backend_info: dict[str, Any]
    y_pred_train: list[float]
    y_pred_test: list[float]


def predict_baseline_mean(y_train: list[float], n_test: int) -> BackendResult:
    mean_value = sum(y_train) / len(y_train)
    y_pred_train = [mean_value for _ in range(len(y_train))]
    y_pred_test = [mean_value for _ in range(n_test)]
    return BackendResult(
        backend="baseline_mean",
        backend_info={
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        y_pred_train=y_pred_train,
        y_pred_test=y_pred_test,
    )


def predict_xgboost(
    x_train: list[list[float]],
    y_train: list[float],
    x_test: list[list[float]],
    seed: int,
    *,
    max_depth: int,
    eta: float,
    subsample: float,
    colsample_bytree: float,
    num_boost_round: int,
) -> BackendResult:
    try:
        import xgboost as xgb  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "xgboost is required for backend='xgboost'. Install with: "
            "`python3 -m pip install -r requirements-xgb.txt`"
        ) from exc

    train_matrix = xgb.DMatrix(x_train, label=y_train)
    test_matrix = xgb.DMatrix(x_test)

    params = {
        "objective": "reg:squarederror",
        "max_depth": int(max_depth),
        "eta": float(eta),
        "subsample": float(subsample),
        "colsample_bytree": float(colsample_bytree),
        "seed": int(seed),
        "verbosity": 0,
    }

    booster = xgb.train(params=params, dtrain=train_matrix, num_boost_round=int(num_boost_round))
    y_pred_train = booster.predict(train_matrix).tolist()
    y_pred_test = booster.predict(test_matrix).tolist()

    return BackendResult(
        backend="xgboost",
        backend_info={
            "xgboost_version": getattr(xgb, "__version__", "unknown"),
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "params": params,
            "num_boost_round": int(num_boost_round),
        },
        y_pred_train=y_pred_train,
        y_pred_test=y_pred_test,
    )
