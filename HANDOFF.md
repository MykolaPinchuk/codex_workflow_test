# HANDOFF

## Current slice
Pick the next DGP calibration target or add a new DGP; `dgp008_parametric_ripple` defaults are now confirmed at `complexity=2.2, interaction_scale=0.8`.

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
- Ignored run artifacts and secrets: `.gitignore` (includes `runs/`, `sweeps/`, `.env`, key files).
- Documented protocol decision: `docs/adr/0002-dgp-and-experiment-protocol.md`.
- Added DGP contribution checklist: `docs/dgp/ADDING_DGP.md`.
- Added `dgp006_thresholded_sum` to extend complexity with a threshold-gated linear term.
- Added `dgp007_multi_sine_interaction` to add multi-frequency + interaction complexity.
- Added parametric DGP support (`--dgp-params`) and `dgp008_parametric_ripple`.
- Documented parameterized DGP decision: `docs/adr/0003-parameterized-dgp-family.md`.
- Added `interaction_scale` to `dgp008_parametric_ripple` to decouple interaction/gate strength from frequency scaling.
- Added `dgp009_radial_gate` with radial sine ridge + gated interaction + quadratic term.
- Parameterized `dgp009_radial_gate` with `complexity` and `interaction_scale` defaults.
- Ran dgp009 learning curve (3 seeds): `sweeps/loop18_dgp009_curve_xgb_agent06/report.md`.
- Ran dgp009 grid sweeps for `complexity=0.8` and `complexity=1.2`: `sweeps/loop19_dgp009_c0p8_xgb_agent06/report.md`, `sweeps/loop20_dgp009_c1p2_xgb_agent06/report.md`.
- Ran tighter dgp009 grid sweeps for `complexity=0.9, 1.0, 1.1`: `sweeps/loop21_dgp009_c0p9_xgb_agent06/report.md`, `sweeps/loop22_dgp009_c1p0_xgb_agent06/report.md`, `sweeps/loop23_dgp009_c1p1_xgb_agent06/report.md`.
- Recommended dgp009 default `complexity=0.9` based on grid (R2 ~0.51 across n_train 200–2000); updated defaults accordingly.
- Ran dgp008 learning curves:
  - XGBoost, `complexity=2.0`: `sweeps/loop07_dgp008_curve_xgb_agent03/report.md` (R2 ~0.49–0.55).
  - XGBoost, `complexity=1.0`: `sweeps/loop08_dgp008_curve_xgb_agent03/report.md` (R2 ~0.82–0.85).
  - XGBoost, `complexity=2.5`: `sweeps/loop11_dgp008_curve_xgb_agent03/report.md` (R2 ~0.39–0.43).
  - XGBoost, `complexity=2.2` (3 seeds): `sweeps/loop13_dgp008_curve_xgb_agent04/report.md` (R2 ~0.42–0.46).
  - XGBoost, `complexity=2.2, interaction_scale=0.8` (3 seeds): `sweeps/loop16_dgp008_curve_xgb_agent04/report.md` (R2 ~0.47–0.52).
  - XGBoost, default params (3 seeds): `sweeps/loop17_dgp008_default08_curve_xgb_agent05/report.md` (R2 ~0.47–0.52).
  - XGBoost, `complexity=2.2, interaction_scale=0.9`: `sweeps/loop15_dgp008_curve_xgb_agent04/report.md` (R2 ~0.44–0.52).
  - baseline_mean, `complexity=2.0`: `sweeps/loop09_dgp008_curve_baseline_agent03/report.md` (R2 ~0.00).
  - baseline_mean, `complexity=1.0`: `sweeps/loop10_dgp008_curve_baseline_agent03/report.md` (R2 ~-0.004 to -0.001).
- Set default params for `dgp008_parametric_ripple` to `complexity=2.2, interaction_scale=0.8` and documented them in the ADR/README.
- Confirmed default params with a 3-seed XGBoost sweep: `sweeps/loop17_dgp008_default08_curve_xgb_agent05/report.md`.
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
  - `9ed292a` — agent04 set dgp008 default complexity=2.2
  - `142928f` — agent04 confirmed complexity=2.2 with 3 seeds
  - `0fc169c` — agent04 added interaction_scale param
  - `8488cac` — agent04 set default interaction_scale=0.9
  - `f93758d` — agent04 ran 3-seed sweep for interaction_scale=0.8
  - `1d603e8` — agent05 set default interaction_scale=0.8
  - `2983a86` — agent05 confirmed default-params curve sweep

### Next (ordered)
1) Select the next DGP candidate or complexity band to calibrate.
2) If runtime creeps up, trim grids first (seeds, n_train_list, n_test, rounds) before changing code.

### Open questions
- None.

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
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop12_dgp008_curve_xgb_agent04 --dgps dgp008_parametric_ripple --dgp-params complexity=2.2 --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0,1 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop13_dgp008_curve_xgb_agent04 --dgps dgp008_parametric_ripple --dgp-params complexity=2.2 --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0,1,2 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop14_dgp008_curve_xgb_agent04 --dgps dgp008_parametric_ripple --dgp-params complexity=2.2,interaction_scale=0.8 --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0,1 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop15_dgp008_curve_xgb_agent04 --dgps dgp008_parametric_ripple --dgp-params complexity=2.2,interaction_scale=0.9 --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0,1 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop16_dgp008_curve_xgb_agent04 --dgps dgp008_parametric_ripple --dgp-params complexity=2.2,interaction_scale=0.8 --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0,1,2 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
  - `python3 -m dgp_xgb --dgp dgp008_parametric_ripple --backend baseline_mean --n-train 100 --n-test 50 --run-id smoke_dgp008_default08_agent05`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id smoke_dgp008_default08_xgb_agent05 --dgps dgp008_parametric_ripple --n-train-list 200,500 --n-test 200 --seeds 0 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
  - `.venv/bin/python -m dgp_xgb.sweep --sweep-id loop17_dgp008_default08_curve_xgb_agent05 --dgps dgp008_parametric_ripple --n-train-list 200,500,1000,2000 --n-test 1000 --seeds 0,1,2 --noise-std 0.1 --backend xgboost --xgb-max-depth 2 --xgb-rounds 25 --report`
- Outcome:
  - Succeeded; created local artifacts under `runs/smoke_agent01/`, `runs/smoke_xgb_agent01/`, `runs/smoke_dgp008_default08_agent05/`, `sweeps/smoke_sweep_agent01/`, `sweeps/smoke_dgp008_default08_xgb_agent05/`, and `sweeps/loop17_dgp008_default08_curve_xgb_agent05/` (gitignored).

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
  - Ignore secret-like files (`.env`, `*.pem`, `*.key`, `id_rsa`, `id_ed25519`).
- Branch state:
  - Local branch `dev` is ahead of `origin/dev` by multiple commits; do not push unless the human requests it.
- Handoff commit:
  - `9789dfc` — log rotation + state refresh (agent05)
- Latest checkpoint:
  - `2983a86` — agent05 confirmed default-params curve sweep
- If anything is intentionally uncommitted, list it here with a reason:
  - Local `sweeps/` artifacts from agent02 and agent03 runs (gitignored).
  - Local `sweeps/` artifacts from agent04 runs (`loop12`–`loop16`, gitignored).
  - Local `runs/` + `sweeps/` artifacts from agent05 smoke/default sweeps (`smoke_dgp008_default08_agent05`, `smoke_dgp008_default08_xgb_agent05`, `loop17_dgp008_default08_curve_xgb_agent05`, gitignored).
