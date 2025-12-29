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
- Added optional sweep reports: `python3 -m dgp_xgb.sweep --report` and `--report-only` in `dgp_xgb/sweep.py`.
- Added reproducible local environment bootstrap: `scripts/bootstrap.sh`.
- Added dependency split: `requirements.txt` (minimal) and `requirements-xgb.txt` (optional XGBoost).
- Ignored run artifacts: `.gitignore` (includes `runs/` and `sweeps/`).
- Documented protocol decision: `docs/adr/0002-dgp-and-experiment-protocol.md`.
- Added DGP contribution checklist: `docs/dgp/ADDING_DGP.md`.

### Next (ordered)
1) Start adding new DGPs (`dgp006_...`, `dgp007_...`) and keep them deterministic + regression-only.
2) Run occasional small sweeps with `--report` and capture the key takeaway in `HANDOFF.md` / `agent_logs/current.md` (artifacts stay gitignored). A good default is the “fast loop” below.
3) If results comparison becomes painful, agree on a “default” sweep command (not mandatory) and document it in `HANDOFF.md`.

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
  - `python3 -m dgp_xgb.sweep --sweep-id smoke_report_agent01 --dgps dgp001_linear --n-train-list 50,100 --n-test 40 --seeds 0,1 --backend baseline_mean --report`
  - `python3 -m dgp_xgb.sweep --sweep-id smoke_report_agent01 --report-only`
- Outcome:
  - Succeeded; created local artifacts under `runs/smoke_agent01/`, `runs/smoke_xgb_agent01/`, and `sweeps/smoke_sweep_agent01/` (gitignored).

## First loop (fast)
- Baseline (≈0.1s): `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop01_fast_baseline_agent01 --dgps all --n-train-list 2000 --n-test 1000 --seeds 0 --noise-std 0.1 --backend baseline_mean --report`
- XGBoost (≈13s): `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop01_fast_xgb_agent01 --dgps all --n-train-list 2000 --n-test 1000 --seeds 0 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
- Result summary (test R² at n_train=2000, seed=0):
  - `dgp001_linear`: 0.9387
  - `dgp002_interaction`: 0.4439
  - `dgp003_piecewise`: 0.0647
  - `dgp004_xor_like`: 0.2404
  - `dgp005_sine_quadratic`: 0.8881
  - Full reports: `sweeps/loop01_fast_baseline_agent01/report.md`, `sweeps/loop01_fast_xgb_agent01/report.md`

## Known issues / current breakage
- None known.

## Git notes (handoff)
- `.gitignore` updates made:
  - Ignore local artifacts under `runs/` and `sweeps/`.
- If anything is intentionally uncommitted, list it here with a reason:
  - None.
