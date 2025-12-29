from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class RegressionMetrics:
    mse: float
    rmse: float
    r2: float


def regression_metrics(y_true: list[float], y_pred: list[float]) -> RegressionMetrics:
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    if not y_true:
        raise ValueError("y_true is empty")

    n = len(y_true)
    mean_true = sum(y_true) / n

    sse = 0.0
    sst = 0.0
    for actual, predicted in zip(y_true, y_pred):
        error = actual - predicted
        sse += error * error
        centered = actual - mean_true
        sst += centered * centered

    mse = sse / n
    rmse = math.sqrt(mse)
    r2 = 1.0 - (sse / sst) if sst > 0.0 else float("nan")
    return RegressionMetrics(mse=mse, rmse=rmse, r2=r2)
