# ADR 0001 — Agentic workflow protocol

## Context
This repo is used to pilot an agentic workflow using the Codex VS Code extension.
Work is performed by multiple "generations" of agents, so continuity depends on durable repo artifacts.

## Decision
We standardize on:
- `AGENTS.md` as the operating contract and trigger definitions.
- `onboarding.md` + `HANDOFF.md` + `REPO_MAP.md` as the minimal onboarding set.
- `agent_logs/current.md` for frequent in-progress logging, rotated at handoff.
- A `wrap-up` procedure that updates docs, rotates logs, and creates a safe **handoff** git commit.

## Consequences
- Agents must keep `HANDOFF.md` accurate to avoid chat-history dependence.
- Repo evolution is handled via `REPO_MAP.md` updates at handoff *when needed*.
- Git commits are created at handoff with strict safety constraints (no push/amend/rebase, no secrets, no large datasets).

## Alternatives considered
- Relying on chat history alone (rejected: fragile across compaction and agent changes).
- Enforcing tests/lint at handoff (rejected for this repo type: experimentation-heavy; record breakage instead).
