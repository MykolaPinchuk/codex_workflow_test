# AGENTS

These are the operating rules for Codex agents working in this repo.

## General context
- This repo is being developed by coding agents under human supervision.
- Development is iterative: agents onboard, explore, propose next steps, implement, test, and hand off.
- Agents are numbered sequentially (agent01, agent02, etc). Each agent should mentions its number in logs, handoff doc, and commit messages.

## Triggers
- User message **exactly**: `Onboard`
  - Perform the onboarding procedure described below (equivalent to running the `$onboard` skill).
- User message contains: `wrap up` or `handoff` (any case)
  - Perform the wrap-up + handoff procedure described below (equivalent to running the `$wrap-up` skill).

## Onboard procedure (trigger: `Onboard`)
**Goal:** quickly understand current repo state without indiscriminate scanning.

1) Read (in order, if present):
   - `onboarding.md`
   - `HANDOFF.md`
   - `REPO_MAP.md`
   - `README.md` (focus on "For agents" + quickstart sections)

2) Bounded discovery:
   - Propose up to **10** additional files you need for the *current* slice.
   - Open only those files after listing them with a 1-line reason each.
   - Do **not** scan the repo broadly during onboarding.

3) Output contract:
   - 5-bullet summary of current state
   - 3 next-slice options (each 1–2 bullets)
   - list of files read
   - unknowns / risks (<= 5 bullets)

4) Logging:
   - Append a short entry to `agent_logs/current.md` capturing your understanding and intended next steps.

## Logging (during work)
Maintain a lightweight log in `agent_logs/current.md`.
Write an entry:
- after onboarding
- after each meaningful milestone (decision, change, run result)
- after any failure worth remembering

The **Result** section may be longer when needed (e.g., metrics, findings), but keep it factual and link to artifact paths.

## Wrap-up + handoff procedure (trigger: `wrap up` / `handoff`)
**Goal:** produce a clean handoff and a safe git checkpoint commit on the current branch.

### A) Documentation + state
1) Update `HANDOFF.md` using its required structure.
2) Update `REPO_MAP.md` **only if needed**:
   - new important file/dir/entrypoint created
   - important file moved/renamed
   - canonical commands/entrypoints changed
   - focus area ("hot paths") changed
3) Ensure `README.md` "For agents" links are still correct.
4) Rotate logs:
   - Move `agent_logs/current.md` to `agent_logs/YYYY-MM-DD_agentNN.md` (choose next NN).
   - Append one line to `agent_logs/INDEX.md`.
   - Create a fresh `agent_logs/current.md`.

### B) Git safety + commit (handoff commit)
You may commit to the current branch (e.g., `dev`) for checkpoints and handoff.

You must NOT run:
- `git push`
- `git commit --amend`
- `git rebase`
- `git reset --hard`
- `git clean -fdx`
- modify git remotes

Before committing, always show:
- `git status`
- `git diff --stat`

Never commit secrets or credentials. Never add `.env` or key files (`*.pem`, `*.key`, `id_rsa`, etc.).
If unsure, stop and report.

Never commit large datasets or large artifacts unless explicitly instructed.
Prefer to keep datasets and heavy artifacts ignored via `.gitignore`.

Commit messages:
- `checkpoint: <short description>` during work (only if user asked for a checkpoint)
- `handoff: <short description>` at wrap-up

At handoff, ensure either:
- everything is committed and `git status` is clean, OR
- uncommitted files are listed with a reason

### C) Optional smoke check
A small, local smoke check is encouraged if feasible (e.g., import/module run or the most local command touched).
If not run, state so in `HANDOFF.md` with a reason.

## Decisions
If a non-trivial decision is made (trade-offs, protocol changes, new conventions), create/update an ADR under `docs/adr/` and link it from `HANDOFF.md`.

## Miscellaneous
- Use Pacific time for timestamps.
- Keep generated artifacts out of git (e.g., `runs/`, `sweeps/`); update `.gitignore` if new artifact roots are introduced.
- Do not go outside the repo unless explicitly instructed.
