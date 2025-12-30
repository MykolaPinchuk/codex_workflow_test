# Adding a new DGP

This repo grows by adding synthetic data-generating processes (DGPs) of increasing complexity.

## Checklist
1) Pick the next available number: `dgpNNN_<slug>` (e.g., `dgp006_thresholded_sum`).
2) Implement a generator in `dgp_xgb/dgps.py` with signature:
   - `generate(n: int, seed: int, noise_std: float, params: dict[str, float]) -> (X, y)`
3) Ensure determinism:
   - use only a local `random.Random(seed)` instance,
   - do not read files or global state.
4) Return Python lists:
   - `X`: `list[list[float]]` with fixed width,
   - `y`: `list[float]` (regression-only; even if binary, represent as floats).
5) Add it to the `_DGPS` registry with a short description.
   - If you want a parameterized DGP family, add `default_params` and document the supported keys.
6) Update `HANDOFF.md` with what you added and what should be done next.

## Quick local check
- List DGPs: `python3 -m dgp_xgb --list-dgps`
- Run baseline: `python3 -m dgp_xgb --dgp <new_name> --backend baseline_mean`
- Run with params: `python3 -m dgp_xgb --dgp <new_name> --dgp-params key=value`
