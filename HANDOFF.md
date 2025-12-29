# HANDOFF

## Current slice
Build the DGP + experiment runner scaffold so future agents can add new DGPs and run a low-capacity XGBoost baseline consistently.
Keep outputs reproducible and avoid committing large run artifacts.

## Invariants (do not break)
- Follow `AGENTS.md` triggers and procedures.
- Use Pacific time for timestamps.
- Keep logs current in `agent_logs/current.md`.
- Do not commit `runs/` or `sweeps/` outputs unless explicitly requested.
- Regression-only: do not introduce classification objectives/metrics.

## State of work

### Done (with evidence)
- Added initial DGP registry + experiment runner: `dgp_xgb/`.
- Added sweep runner for learning-curve summaries: `dgp_xgb/sweep.py`.
- Added runtime dependency list: `requirements.txt`.
- Ignored run artifacts: `.gitignore` (includes `runs/` and `sweeps/`).
- Documented protocol decision: `docs/adr/0002-dgp-and-experiment-protocol.md`.
- Added DGP contribution checklist: `docs/dgp/ADDING_DGP.md`.

### Next (ordered)
1) Run a smoke check locally (`--backend baseline_mean`) and, if available, with `--backend xgboost`.
2) Define the next DGPs to add (or parameters for increasing complexity) and success criteria (metrics vs sample size).
3) Decide a standard sweep grid (n_train list, seeds) and whether to produce a consolidated markdown report per sweep.

### Open questions
- Should complexity be represented as separate numbered DGPs only, or via a parameterized DGP family (e.g., `dgp010_family --complexity k`)?

## Repro / smoke check
- Commands run:
  - `python3 -m dgp_xgb --list-dgps`
  - `python3 -m dgp_xgb --dgp dgp003_piecewise --backend baseline_mean --n-train 200 --n-test 100 --run-id smoke_agent01`
  - `python3 -m dgp_xgb.sweep --sweep-id smoke_sweep_agent01 --dgps dgp001_linear --n-train-list 50 --n-test 30 --seeds 0 --backend baseline_mean`
  - `./scripts/bootstrap.sh`
  - `./scripts/bootstrap.sh --xgb`
  - `.venv/bin/python -m dgp_xgb --dgp dgp002_interaction --backend xgboost --n-train 500 --n-test 200 --run-id smoke_xgb_agent01 --xgb-max-depth 2 --xgb-rounds 25`
- Outcome:
  - Succeeded; created local artifacts under `runs/smoke_agent01/`, `runs/smoke_xgb_agent01/`, and `sweeps/smoke_sweep_agent01/` (gitignored).

## Known issues / current breakage
- None known.

## Git notes (handoff)
- `.gitignore` updates made:
  - Ignore local artifacts under `runs/` and `sweeps/`.
- If anything is intentionally uncommitted, list it here with a reason:
  - None.
