# HANDOFF

## Current slice
Iterate on parameterized DGPs (starting with `dgp008_parametric_ripple`) to map complexity vs learnability under low-capacity XGBoost.
Keep runs reproducible (configs/reports) while keeping bulky artifacts out of git.

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
- Added `dgp006_thresholded_sum` to extend complexity with a threshold-gated linear term.
- Added `dgp007_multi_sine_interaction` to add multi-frequency + interaction complexity.
- Added parametric DGP support (`--dgp-params`) and `dgp008_parametric_ripple`.
- Documented parameterized DGP decision: `docs/adr/0003-parameterized-dgp-family.md`.
- Ran dgp008 learning curves:
  - XGBoost, `complexity=2.0`: `sweeps/loop07_dgp008_curve_xgb_agent03/report.md` (R2 ~0.49–0.55).
  - XGBoost, `complexity=1.0`: `sweeps/loop08_dgp008_curve_xgb_agent03/report.md` (R2 ~0.82–0.85).
  - XGBoost, `complexity=2.5`: `sweeps/loop11_dgp008_curve_xgb_agent03/report.md` (R2 ~0.39–0.43).
  - baseline_mean, `complexity=2.0`: `sweeps/loop09_dgp008_curve_baseline_agent03/report.md` (R2 ~0.00).
  - baseline_mean, `complexity=1.0`: `sweeps/loop10_dgp008_curve_baseline_agent03/report.md` (R2 ~-0.004 to -0.001).
- Key checkpoints:
  - `8fad083` — env bootstrap + optional XGBoost
  - `f0bdfe5` — opt-in `report.md` for sweeps
  - `054261d` — `--report-only` + metadata embedded in report
  - `3dbb797` — first fast loop results recorded
  - `a553b83` — agent02 added `dgp006_thresholded_sum`
  - `8b5acc0` — agent02 added `dgp007_multi_sine_interaction`
  - `14d2850` — agent02 ran dgp007 sweeps + docs
  - `b3bd286` — agent03 added parametric DGP support + dgp008
  - `d71dcb4` — agent03 updated dgp008 curve notes + ADR summary

### Next (ordered)
1) Decide on the target complexity range for `dgp008_parametric_ripple` (e.g., 2.0 vs 2.5 vs 3.0) and run a small curve to pick a default.
2) Consider adding a second parameter (e.g., interaction scale) if single-parameter scaling is too coarse.
3) If runtime creeps up, trim grids first (seeds, n_train_list, n_test, rounds) before changing code.

### Open questions
- Do we want to standardize a default `complexity` for `dgp008_parametric_ripple` (or treat it as always user-specified)?

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
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop02_fast_baseline_agent02 --dgps all --n-train-list 2000 --n-test 1000 --seeds 0 --noise-std 0.1 --backend baseline_mean --report`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop02_fast_xgb_agent02d --dgps all --n-train-list 2000 --n-test 1000 --seeds 0 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop03_dgp007_xgb_agent02 --dgps dgp007_multi_sine_interaction --n-train-list 2000 --n-test 1000 --seeds 0 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop04_dgp007_curve_xgb_agent02 --dgps dgp007_multi_sine_interaction --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop05_dgp007_curve_baseline_agent02 --dgps dgp007_multi_sine_interaction --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0 --noise-std 0.1 --backend baseline_mean --report`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop06_dgp007_curve_xgb_agent02 --dgps dgp007_multi_sine_interaction --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0,1,2 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop07_dgp008_curve_xgb_agent03 --dgps dgp008_parametric_ripple --dgp-params complexity=2.0 --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0,1 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop08_dgp008_curve_xgb_agent03 --dgps dgp008_parametric_ripple --dgp-params complexity=1.0 --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0,1 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop09_dgp008_curve_baseline_agent03 --dgps dgp008_parametric_ripple --dgp-params complexity=2.0 --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0,1 --noise-std 0.1 --backend baseline_mean --report`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop10_dgp008_curve_baseline_agent03 --dgps dgp008_parametric_ripple --dgp-params complexity=1.0 --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0,1 --noise-std 0.1 --backend baseline_mean --report`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop11_dgp008_curve_xgb_agent03 --dgps dgp008_parametric_ripple --dgp-params complexity=2.5 --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0,1 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
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

## Second loop (fast, agent02)
- Baseline: `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop02_fast_baseline_agent02 --dgps all --n-train-list 2000 --n-test 1000 --seeds 0 --noise-std 0.1 --backend baseline_mean --report`
- XGBoost: `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop02_fast_xgb_agent02d --dgps all --n-train-list 2000 --n-test 1000 --seeds 0 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
- Result summary (test R² at n_train=2000, seed=0):
  - `dgp006_thresholded_sum`: 0.1038
  - `dgp007_multi_sine_interaction`: 0.8829
  - Full reports: `sweeps/loop02_fast_baseline_agent02/report.md`, `sweeps/loop02_fast_xgb_agent02d/report.md`

## Learning curve (dgp007, agent02)
- XGBoost curve: `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop04_dgp007_curve_xgb_agent02 --dgps dgp007_multi_sine_interaction --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
- Baseline curve: `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop05_dgp007_curve_baseline_agent02 --dgps dgp007_multi_sine_interaction --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0 --noise-std 0.1 --backend baseline_mean --report`
- Multi-seed XGBoost curve: `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop06_dgp007_curve_xgb_agent02 --dgps dgp007_multi_sine_interaction --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0,1,2 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
- Result summary (test R² mean across seeds):
  - `dgp007_multi_sine_interaction`: ~0.88 across 200–2000; curve is flat vs n_train
  - Full reports: `sweeps/loop04_dgp007_curve_xgb_agent02/report.md`, `sweeps/loop05_dgp007_curve_baseline_agent02/report.md`, `sweeps/loop06_dgp007_curve_xgb_agent02/report.md`

## Known issues / current breakage
- A larger sweep attempt was interrupted; `sweeps/loop01_xgb_agent01/` may be partially populated (gitignored).

## Git notes (handoff)
- `.gitignore` updates made:
  - Ignore local artifacts under `runs/` and `sweeps/`.
- Branch state:
  - Local branch `dev` is ahead of `origin/dev` by multiple commits; do not push unless the human requests it.
- Latest checkpoint:
  - `d71dcb4` — agent03 updated dgp008 curve notes + ADR summary
- If anything is intentionally uncommitted, list it here with a reason:
  - Local `sweeps/` artifacts from agent02 and agent03 runs (gitignored).
