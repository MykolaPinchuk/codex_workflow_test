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
    generate: Callable[[int, int, float], tuple[list[list[float]], list[float]]]


def _uniform_features(rng: random.Random, n_features: int) -> list[float]:
    return [rng.uniform(-1.0, 1.0) for _ in range(n_features)]


def _gaussian_noise(rng: random.Random, noise_std: float) -> float:
    if noise_std <= 0.0:
        return 0.0
    return rng.gauss(0.0, noise_std)


def _dgp001_linear(n: int, seed: int, noise_std: float) -> tuple[list[list[float]], list[float]]:
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


def _dgp002_interaction(n: int, seed: int, noise_std: float) -> tuple[list[list[float]], list[float]]:
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


def _dgp003_piecewise(n: int, seed: int, noise_std: float) -> tuple[list[list[float]], list[float]]:
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


def _dgp004_xor_like(n: int, seed: int, noise_std: float) -> tuple[list[list[float]], list[float]]:
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


def _dgp005_sine_quadratic(n: int, seed: int, noise_std: float) -> tuple[list[list[float]], list[float]]:
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
]


def list_dgps() -> list[DGP]:
    return list(_DGPS)


def get_dgp(name: str) -> DGP:
    for dgp in _DGPS:
        if dgp.name == name:
            return dgp
    known = ", ".join(dgp.name for dgp in _DGPS)
    raise KeyError(f"Unknown DGP '{name}'. Known: {known}")
