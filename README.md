# codex_workflow_test

This repository is a testbed for an agentic workflow in the Codex VS Code extension.

## For agents
Start here (in this order):
- `AGENTS.md` (operating rules + triggers)
- `onboarding.md` (how onboarding works here)
- `HANDOFF.md` (current state / next steps)
- `REPO_MAP.md` (index of important files)
- `agent_logs/current.md` (live execution log; history indexed in `agent_logs/INDEX.md`)
- `docs/adr/` (decisions that should persist across agent generations)

## Repo conventions (high level)
- Keep raw data, secrets, and large generated artifacts out of git (update `.gitignore` as needed).
- Prefer writing results as markdown reports and small tables that are easy to review.
