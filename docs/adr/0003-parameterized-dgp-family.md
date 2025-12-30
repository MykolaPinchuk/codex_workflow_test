# ADR 0003 — Parameterized DGP families

## Context
The repo is accumulating sequentially numbered DGPs to represent increasing complexity.
As complexity grows, some variations are best expressed as a parameterized family (e.g., scaling frequency or interaction strength) rather than adding multiple near-duplicate DGPs.

## Decision
- Keep the numbered DGP registry as the primary mechanism for tracking complexity (`dgpNNN_<slug>`).
- Allow DGPs to define optional `default_params` and accept `params` to support small family variations.
- Expose a CLI/sweep flag `--dgp-params key=value[,key=value...]` to override defaults for parametric DGPs.
- Record `dgp_params` in run configs and sweep metadata for reproducibility.
- Set the default `complexity` for `dgp008_parametric_ripple` to 2.2 to target a moderate difficulty band.
- Add `interaction_scale` to decouple interaction/gate strength from frequency scaling (default 0.9).

## Consequences
- We can introduce a single numbered DGP that represents a family (e.g., `dgp008_parametric_ripple`) without proliferating similar DGPs.
- Sweeps can keep a stable DGP list while adjusting complexity via `--dgp-params`.
- Param handling adds a small amount of plumbing to the CLI and runner but keeps the DGP registry central.

## Empirical summary
- `dgp008_parametric_ripple` shows a clear complexity effect under low-capacity XGBoost.
  - `complexity=1.0`: test R2 ~0.82–0.85 across n_train 200–2000 (`sweeps/loop08_dgp008_curve_xgb_agent03/report.md`).
  - `complexity=2.0`: test R2 ~0.49–0.55 across n_train 200–2000 (`sweeps/loop07_dgp008_curve_xgb_agent03/report.md`).
  - `complexity=2.2`: test R2 ~0.42–0.46 across n_train 200–2000 (`sweeps/loop13_dgp008_curve_xgb_agent04/report.md`).
  - `complexity=2.2, interaction_scale=0.8`: test R2 ~0.47–0.55 across n_train 200–2000 (`sweeps/loop14_dgp008_curve_xgb_agent04/report.md`).
  - `complexity=2.2, interaction_scale=0.9`: test R2 ~0.44–0.52 across n_train 200–2000 (`sweeps/loop15_dgp008_curve_xgb_agent04/report.md`).
  - `complexity=2.5`: test R2 ~0.39–0.43 across n_train 200–2000 (`sweeps/loop11_dgp008_curve_xgb_agent03/report.md`).
  - baseline_mean at `complexity=2.0`: test R2 ~0.00 (`sweeps/loop09_dgp008_curve_baseline_agent03/report.md`).
  - baseline_mean at `complexity=1.0`: test R2 ~-0.004 to -0.001 (`sweeps/loop10_dgp008_curve_baseline_agent03/report.md`).

## Alternatives considered
- Use parameterized DGPs only (drop numbered registry). Rejected: complexity ordering and historical continuity are useful.
- Add a separate config file per DGP variant. Rejected: adds extra file management overhead for small variations.
