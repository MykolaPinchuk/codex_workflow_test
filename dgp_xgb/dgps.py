from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import math
import random


@dataclass(frozen=True)
class DGP:
    name: str
    description: str
    n_features: int
    generate: Callable[[int, int, float, dict[str, float]], tuple[list[list[float]], list[float]]]
    default_params: dict[str, float] | None = None


def _uniform_features(rng: random.Random, n_features: int) -> list[float]:
    return [rng.uniform(-1.0, 1.0) for _ in range(n_features)]


def _gaussian_noise(rng: random.Random, noise_std: float) -> float:
    if noise_std <= 0.0:
        return 0.0
    return rng.gauss(0.0, noise_std)


def _dgp001_linear(
    n: int, seed: int, noise_std: float, params: dict[str, float]
) -> tuple[list[list[float]], list[float]]:
    rng = random.Random(seed)
    n_features = 5
    features: list[list[float]] = []
    targets: list[float] = []
    for _ in range(n):
        row = _uniform_features(rng, n_features)
        y_value = 2.0 * row[0] - 1.0 * row[1] + _gaussian_noise(rng, noise_std)
        features.append(row)
        targets.append(y_value)
    return features, targets


def _dgp002_interaction(
    n: int, seed: int, noise_std: float, params: dict[str, float]
) -> tuple[list[list[float]], list[float]]:
    rng = random.Random(seed)
    n_features = 5
    features: list[list[float]] = []
    targets: list[float] = []
    for _ in range(n):
        row = _uniform_features(rng, n_features)
        y_value = (row[0] * row[1]) + 0.5 * row[2] + _gaussian_noise(rng, noise_std)
        features.append(row)
        targets.append(y_value)
    return features, targets


def _dgp003_piecewise(
    n: int, seed: int, noise_std: float, params: dict[str, float]
) -> tuple[list[list[float]], list[float]]:
    rng = random.Random(seed)
    n_features = 6
    features: list[list[float]] = []
    targets: list[float] = []
    for _ in range(n):
        row = _uniform_features(rng, n_features)
        slope = 1.0 if row[0] > 0.0 else -1.0
        y_value = slope * row[1] + 0.2 * row[2] + _gaussian_noise(rng, noise_std)
        features.append(row)
        targets.append(y_value)
    return features, targets


def _dgp004_xor_like(
    n: int, seed: int, noise_std: float, params: dict[str, float]
) -> tuple[list[list[float]], list[float]]:
    rng = random.Random(seed)
    n_features = 4
    features: list[list[float]] = []
    targets: list[float] = []
    for _ in range(n):
        row = _uniform_features(rng, n_features)
        a_positive = row[0] > 0.0
        b_positive = row[1] > 0.0
        xor_value = 1.0 if (a_positive ^ b_positive) else 0.0
        y_value = xor_value + _gaussian_noise(rng, noise_std)
        features.append(row)
        targets.append(y_value)
    return features, targets


def _dgp005_sine_quadratic(
    n: int, seed: int, noise_std: float, params: dict[str, float]
) -> tuple[list[list[float]], list[float]]:
    rng = random.Random(seed)
    n_features = 6
    features: list[list[float]] = []
    targets: list[float] = []
    for _ in range(n):
        row = _uniform_features(rng, n_features)
        y_value = math.sin(3.0 * row[0]) + (row[1] ** 2) + _gaussian_noise(rng, noise_std)
        features.append(row)
        targets.append(y_value)
    return features, targets


def _dgp006_thresholded_sum(
    n: int, seed: int, noise_std: float, params: dict[str, float]
) -> tuple[list[list[float]], list[float]]:
    rng = random.Random(seed)
    n_features = 6
    features: list[list[float]] = []
    targets: list[float] = []
    for _ in range(n):
        row = _uniform_features(rng, n_features)
        threshold = row[0] + 0.5 * row[1]
        gate = 1.0 if threshold > 0.0 else -1.0
        y_value = gate * row[2] + 0.3 * row[3] + _gaussian_noise(rng, noise_std)
        features.append(row)
        targets.append(y_value)
    return features, targets


def _dgp007_multi_sine_interaction(
    n: int, seed: int, noise_std: float, params: dict[str, float]
) -> tuple[list[list[float]], list[float]]:
    rng = random.Random(seed)
    n_features = 7
    features: list[list[float]] = []
    targets: list[float] = []
    for _ in range(n):
        row = _uniform_features(rng, n_features)
        y_value = (
            math.sin(2.0 * row[0])
            + 0.5 * math.sin(4.0 * row[1])
            + 0.4 * row[2] * row[3]
            + 0.2 * abs(row[4])
            + _gaussian_noise(rng, noise_std)
        )
        features.append(row)
        targets.append(y_value)
    return features, targets


def _dgp008_parametric_ripple(
    n: int, seed: int, noise_std: float, params: dict[str, float]
) -> tuple[list[list[float]], list[float]]:
    rng = random.Random(seed)
    n_features = 7
    complexity = max(0.5, params.get("complexity", 2.2))
    interaction_scale = max(0.0, params.get("interaction_scale", 1.0))
    freq_primary = 2.0 * complexity
    freq_secondary = 3.5 * complexity
    interaction = 0.3 * complexity * interaction_scale
    gate_scale = 0.4 * complexity * interaction_scale

    features: list[list[float]] = []
    targets: list[float] = []
    for _ in range(n):
        row = _uniform_features(rng, n_features)
        gate = 1.0 if row[4] + 0.25 * row[5] > 0.0 else -1.0
        y_value = (
            math.sin(freq_primary * row[0])
            + 0.6 * math.sin(freq_secondary * row[1])
            + interaction * row[2] * row[3]
            + gate_scale * gate * row[6]
            + _gaussian_noise(rng, noise_std)
        )
        features.append(row)
        targets.append(y_value)
    return features, targets


_DGPS: list[DGP] = [
    DGP(
        name="dgp001_linear",
        description="Linear signal + distractors.",
        n_features=5,
        generate=_dgp001_linear,
    ),
    DGP(
        name="dgp002_interaction",
        description="One multiplicative interaction + linear term.",
        n_features=5,
        generate=_dgp002_interaction,
    ),
    DGP(
        name="dgp003_piecewise",
        description="Piecewise sign flip (requires splits).",
        n_features=6,
        generate=_dgp003_piecewise,
    ),
    DGP(
        name="dgp004_xor_like",
        description="XOR-like boundary; regression target in {0,1}.",
        n_features=4,
        generate=_dgp004_xor_like,
    ),
    DGP(
        name="dgp005_sine_quadratic",
        description="Sinusoid + quadratic; smooth nonlinearity.",
        n_features=6,
        generate=_dgp005_sine_quadratic,
    ),
    DGP(
        name="dgp006_thresholded_sum",
        description="Thresholded sum gates a linear term; piecewise interaction.",
        n_features=6,
        generate=_dgp006_thresholded_sum,
    ),
    DGP(
        name="dgp007_multi_sine_interaction",
        description="Multi-frequency sines + interaction + absolute value term.",
        n_features=7,
        generate=_dgp007_multi_sine_interaction,
    ),
    DGP(
        name="dgp008_parametric_ripple",
        description="Parametric family; tune `complexity` and `interaction_scale` via --dgp-params.",
        n_features=7,
        generate=_dgp008_parametric_ripple,
        default_params={"complexity": 2.2, "interaction_scale": 1.0},
    ),
]


def list_dgps() -> list[DGP]:
    return list(_DGPS)


def get_dgp(name: str) -> DGP:
    for dgp in _DGPS:
        if dgp.name == name:
            return dgp
    known = ", ".join(dgp.name for dgp in _DGPS)
    raise KeyError(f"Unknown DGP '{name}'. Known: {known}")


def resolve_dgp_params(dgp: DGP, params: dict[str, float] | None) -> dict[str, float]:
    resolved = dict(dgp.default_params or {})
    if params:
        resolved.update(params)
    return resolved
