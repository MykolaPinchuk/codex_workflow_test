# REPO_MAP

Keep this file short. Update it only when something important changes.

## Critical entrypoints (read these first for work)
- `AGENTS.md` — operating rules and triggers for agents.
- `onboarding.md` — onboarding procedure when triggered.
- `HANDOFF.md` — current objective, next steps, and state.
- `REPO_MAP.md` — index of important files and hot paths.
- `README.md` — repo overview and agent start points.
- `agent_logs/current.md` — live execution log for this cycle.
- `docs/adr/0001-agentic-workflow-protocol.md` — foundational workflow decision.
- `docs/adr/0002-dgp-and-experiment-protocol.md` — DGP naming, runner, and artifact conventions.
- `dgp_xgb/cli.py` — CLI entrypoint (`python -m dgp_xgb ...`).
- `dgp_xgb/dgps.py` — DGP registry and generators.
- `dgp_xgb/runner.py` — experiment runner + artifact writing.
- `dgp_xgb/sweep.py` — simple sweep runner (learning curves across n_train).
- `requirements.txt` — base deps (intentionally minimal).
- `requirements-xgb.txt` — optional deps for XGBoost backend.
- `scripts/bootstrap.sh` — create a venv and install deps.
- `docs/dgp/ADDING_DGP.md` — checklist for adding a new DGP.

## Where results live
- `agent_logs/` — per-cycle logs and index.
- `docs/adr/` — decision records.
- `runs/` — local experiment outputs (gitignored).
- `sweeps/` — local sweep outputs (gitignored).

## Hot paths (last 1–2 cycles)
- `HANDOFF.md` — current cycle state and plans.
- `REPO_MAP.md` — repo index entries.
- `agent_logs/current.md` — active logging.
- `dgp_xgb/` — DGP definitions and runner implementation.

## New important files since last cycle
- `dgp_xgb/` — DGPs and experiment runner.
- `.gitignore` — ignores `runs/` and common Python artifacts.
- `requirements.txt` — intended runtime dependency list.

## Notes
- If you create a new "important" dir or entrypoint, add it above so future agents find it quickly.
