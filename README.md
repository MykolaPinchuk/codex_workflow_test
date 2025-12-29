# codex_workflow_test

This repository is a testbed for an agentic workflow in the Codex VS Code extension.

This repo will build increasingly more complex synthetic data-generating processes (DGPs) to test how a low-capacity XGBoost model learns them (regression-only).

## For agents
Start here (in this order):
- `AGENTS.md` (operating rules + triggers)
- `onboarding.md` (how onboarding works here)
- `HANDOFF.md` (current state / next steps)
- `REPO_MAP.md` (index of important files)
- `agent_logs/current.md` (live execution log; history indexed in `agent_logs/INDEX.md`)
- `docs/adr/` (decisions that should persist across agent generations)
- `docs/dgp/ADDING_DGP.md` (how to add a new DGP)
- `dgp_xgb/` (DGPs + experiment runner code)

## Repo conventions (high level)
- Keep raw data, secrets, and large generated artifacts out of git (update `.gitignore` as needed).
- Prefer writing results as markdown reports and small tables that are easy to review.

## Quickstart (local)
- Create venv (recommended): `./scripts/bootstrap.sh`
- List DGPs: `python3 -m dgp_xgb --list-dgps`
- Run (no deps needed): `python3 -m dgp_xgb --dgp dgp001_linear --backend baseline_mean`
- Enable XGBoost backend: `./scripts/bootstrap.sh --xgb`
- Run with XGBoost: `python3 -m dgp_xgb --dgp dgp002_interaction --backend xgboost`
- Override XGBoost capacity: `python3 -m dgp_xgb --backend xgboost --xgb-max-depth 2 --xgb-rounds 25`
- Run a small sweep: `python3 -m dgp_xgb.sweep --sweep-id demo --dgps dgp001_linear,dgp002_interaction --backend baseline_mean`
- Add a markdown report: `python3 -m dgp_xgb.sweep --sweep-id demo --dgps dgp001_linear --backend baseline_mean --report`
- Rebuild report without rerunning: `python3 -m dgp_xgb.sweep --sweep-id demo --report-only`
