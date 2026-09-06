# Web Mathematical Skills Guide

This directory contains the fixed Skills available to the single-problem Web GPT + GitHub workflow. It does not import user-level Skills or activate upstream repositories.

Use `vibe-mathing-router` to choose exactly one primary owner Skill for the current obligation:

```text
math-discovery -> identify objects, exact statements, sources, and prior art
math-derivation -> derive intermediate claims from frozen definitions
math-computation -> design bounded checks and falsifiers; evidence ceiling applies
math-proof -> construct and adversarially audit proof/counterexample candidates
math-formalization -> encode frozen obligations and request kernel verification
solve -> broad candidate generation only
math-toolchain -> ToolPlan generation only
```

`math-computation` and `math-formalization` are constrained by runtime availability and receipts. `solve` never emits an admitted Result; `math-toolchain` never claims that its plan was executed. `nvidia-private-compute`, `auto-goal`, `auto-tmux`, compute-node orchestration, and session control are excluded from Web problem repositories.

Search registered mathematical knowledge sources before inventing new machinery. Respect exact versions, source maturity, operational status, external effects, and evidence ceilings. A Skill is a method contract, not a verifier identity or evidence level.
