# ADR 0003 — Parameterized DGP families

## Context
The repo is accumulating sequentially numbered DGPs to represent increasing complexity.
As complexity grows, some variations are best expressed as a parameterized family (e.g., scaling frequency or interaction strength) rather than adding multiple near-duplicate DGPs.

## Decision
- Keep the numbered DGP registry as the primary mechanism for tracking complexity (`dgpNNN_<slug>`).
- Allow DGPs to define optional `default_params` and accept `params` to support small family variations.
- Expose a CLI/sweep flag `--dgp-params key=value[,key=value...]` to override defaults for parametric DGPs.
- Record `dgp_params` in run configs and sweep metadata for reproducibility.

## Consequences
- We can introduce a single numbered DGP that represents a family (e.g., `dgp008_parametric_ripple`) without proliferating similar DGPs.
- Sweeps can keep a stable DGP list while adjusting complexity via `--dgp-params`.
- Param handling adds a small amount of plumbing to the CLI and runner but keeps the DGP registry central.

## Alternatives considered
- Use parameterized DGPs only (drop numbered registry). Rejected: complexity ordering and historical continuity are useful.
- Add a separate config file per DGP variant. Rejected: adds extra file management overhead for small variations.
