# GitHub Automation Boundary

## Mandatory reasoning boundary

<!-- MATHEMATICAL_REASONING_DISCIPLINE_V1 -->

Automation inherits `governance/standards/MATHEMATICAL_REASONING_DISCIPLINE.md`. CI may check structure, frozen artifacts and receipts, but it cannot replace definition/quantifier review, valid induction or contraposition, explicit witnesses, counterexample pressure tests, invariant/termination arguments, scale/boundary analysis, statement-faithfulness, or independent mathematical evidence.

- Web GPT candidate branches must not modify `.github/**`.
- Workflows run untrusted candidate diffs with `contents: read` only and without secrets.
- The required candidate gate must validate the immutable Harness snapshot, full diff, packet schema, candidate-path add/modify/delete boundary, file modes, size budgets and privacy rules.
- After repository admission, AI may review/revise, rerun the existing candidate workflow and merge after required checks; no project-added human approval is required.
- Issue, PR, AI review, merge and CI success are transport/runtime states, not EvidenceLink, Result or Solution admission.
- Workflow changes require a separate `maintenance/harness-*` PR by the allowlisted `vibemathing` maintainer; the diff gate requires an exact regenerated Harness snapshot delta and forbids Problem/record/candidate/Evidence/Result/Solution changes. Never accept maintenance files from `web/attempt-*`.
