# ADR 0002 — DGP + experiment protocol

## Context
This repo will accumulate many synthetic data-generating processes (DGPs) of increasing complexity to study how a low-capacity XGBoost model learns them.
Dozens of agents will contribute over time, so we need stable conventions for:
- how DGPs are added and named,
- how experiments are run,
- where results land,
- what is (and is not) committed to git.

## Decision
### DGP library
- DGPs live in `dgp_xgb/dgps.py` and are registered in a small in-code registry.
- DGP names are monotonically numbered: `dgpNNN_<slug>` (e.g., `dgp001_linear`), where the number indicates intended complexity ordering.
- Each DGP must be deterministic given `(n, seed, noise_std)` and return `(X, y)` as Python lists (to keep dependencies optional).
- This project is regression-only: `y` is always `float` and models are evaluated with regression metrics.

### Experiment runner
- Canonical CLI: `python3 -m dgp_xgb ...` (implemented via `dgp_xgb/__main__.py` + `dgp_xgb/cli.py`).
- Optional sweep CLI: `python3 -m dgp_xgb.sweep ...` for quick learning-curve style summaries.
- Default backend is `baseline_mean` so the pipeline can run without extra dependencies.
- `backend=xgboost` is supported when `xgboost` is installed (via `requirements-xgb.txt`, capped to `<3` to avoid very large optional GPU dependencies).
- Hyperparameters may change between runs; they must be passed explicitly (CLI flags) and are recorded in `config.json`/`sweep.json` for reproducibility.
- Outputs go to `runs/<run_id>/` with:
  - `config.json` (full run config + timestamp),
  - `metrics.json` (train/test metrics + backend info),
  - `summary.md` (human-readable snapshot).

### Git hygiene
- `runs/` is ignored via `.gitignore` to avoid committing large or noisy artifacts.
- `sweeps/` is ignored via `.gitignore` for the same reason.

## Consequences
- Adding a DGP is a code change (not a data drop): agents extend the registry and keep the ordering intact.
- Runs are reproducible via `config.json` and deterministic DGP generation, but run directories are ephemeral unless explicitly requested to commit.

## Alternatives considered
- Storing DGP specs as separate files (YAML/JSON). Rejected for now: adds parsing and schema overhead; can be revisited when DGP count grows.
- Requiring `numpy`/`pandas` as baseline deps. Rejected for now: keep the runner usable in minimal Python environments.
