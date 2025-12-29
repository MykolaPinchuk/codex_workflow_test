# onboarding.md

This file describes how onboarding should work for agents in this repo.

## What the user will do
- Start a new Codex chat.
- Attach `AGENTS.md`.
- Type a single word: `Onboard`.

## What you (the agent) must do on `Onboard`
Follow the **Onboard procedure** in `AGENTS.md` (it is equivalent to the `$onboard` skill):
- Read the small set of index/state files first.
- Propose a bounded list (<= 10) of additional files you need next, and open only those.
- Produce the required onboarding output (summary, options, files read, unknowns).
- Append a short entry to `agent_logs/current.md`.

## Design intent
This repo may evolve quickly. Do not assume that a static file list is sufficient.
Instead, treat:
- `HANDOFF.md` as the authoritative current state,
- `REPO_MAP.md` as the authoritative index of important files and entrypoints.
