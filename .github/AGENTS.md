# GitHub Automation Boundary

- Web GPT candidate branches must not modify `.github/**`.
- Workflows run untrusted candidate diffs with `contents: read` only and without secrets.
- The required candidate gate must validate the immutable Harness snapshot, full diff, packet schema, candidate-path add/modify/delete boundary, file modes, size budgets and privacy rules.
- After repository admission, AI may review/revise, rerun the existing candidate workflow and merge after required checks; no project-added human approval is required.
- Issue, PR, AI review, merge and CI success are transport/runtime states, not EvidenceLink, Result or Solution admission.
- Workflow changes require a separate trusted Harness-maintainer change on a protected branch; never accept them from `web/attempt-*`.
