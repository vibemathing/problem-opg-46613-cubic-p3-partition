# Web Research Bootstrap

- Repository: `vibemathing/problem-opg-46613-cubic-p3-partition`
- Repository binding: `verified`
- Repository database ID: `1358762601`
- Repository node ID: `R_kgDOUP0SaQ`
- Default branch: `main`
- Visibility: `public`
- Canonical Problem: `problem:opg-46613-cubic-p3-partition`
- ProblemContract SHA-256: `f22ec1937d8b771614cb85435b6d4e0712afb9a3939780e04b74e4649617c26a`
- Problem lifecycle: `active`
- Problem admission: `canonical_admitted`
- Harness suite: `harness-source:web-research-full` `1.2.4`
- Suite manifest SHA-256: `fedd664f1ac16c5232eb05076b73f2bab566ed672840e7f2af851c77253813b3`
- Harness snapshot SHA-256: `c361ab971cb9dc51270888c605adb9dc84d98e8f33316d9fc23d7064a8d24718`
- Channel: `chatgpt-web-github-issue-pr-writer`

## Required read order

1. `AGENTS.md`
2. `WEB_CHANNEL_PROFILE.json`
3. `HARNESS_SNAPSHOT.json`
4. `WEB_CONTEXT_BUNDLE.md`
5. `WEB_ACTIVE_SKILLS.json`
6. `problem-library/records/canonical-problems.jsonl`
7. `research/records/failed-routes.jsonl`
8. the current route and obligation packet named by the Issue
9. exactly the owner Skill files selected by `WEB_ACTIVE_SKILLS.json`
10. `WEB_OUTPUT_CONTRACT.json`

Return a `web-bootstrap-ack.schema.json` object before mathematical work. Hashes shown here are manifest-declared values; do not claim to have recomputed them in chat.

## Fresh-state gate precedence

At the start of every turn, refresh the default branch plus live Issue/branch/PR/check state. Current repository records outrank launch-prompt SHAs, and launch-prompt SHAs outrank old chat replies. A controlled merge may legitimately advance main or the Harness snapshot; use the fresh revision as the packet base after validating the new snapshot. Never repeat an old `BLOCK_PRE_ADMISSION` unless a fresh read proves that the exact Attempt/Route/Graph/Obligation is currently absent or mismatched.

Channel audit maturity is not repository admission. `capability_status` and connector identity fields describe how completely the exact Plugin/App identity has been audited; they do not block a repository whose current identity, canonical ProblemContract, admitted route objects, and transport controls pass. The admitted namespace remains candidate-only and grants no Evidence/Result authority.

Branch protection and automated required checks are transport controls, not demands for manual approval. Reuse the one Issue identified by `(problem_id, attempt_id, route_id, obligation_id)` and label `web-research-question`; search before create, including a second fresh search immediately before creation, so retries and concurrent turns stay idempotent.

One Web response ending is a runtime boundary, not a permission failure and not mathematical completion. Before the boundary, save the best bounded checkpoint when possible. The next turn must resume by rereading current main and live GitHub state rather than replaying a stale bootstrap decision.

## AI-native writable route

After repository admission, perform the routine candidate transport end to end without project-added human handoffs:

1. Reuse the unique Issue labeled `web-research-question` for the exact Problem/Attempt/Route/Obligation tuple; create one only after two fresh searches find none.
2. Create branch `web/attempt-<attempt-suffix>`.
3. Add, revise, or delete files only under `research/artifacts/web-inbox/**`, `research/artifacts/candidates/**`, or `research/artifacts/source-notes/**`.
4. Commit real changes and open a PR using the web candidate template.
5. Monitor required checks and, when needed, rerun the existing candidate workflow.
6. Review and revise the candidate PR; this AI review is not independent mathematical review.
7. After transport checks pass, merge the candidate PR and write the next checkpoint.

Do not create repositories, direct-push the default branch, modify workflow/truth paths, force-push, cancel/dispatch Actions, or sign Evidence/Result. Follow only platform-mandatory confirmation UI; no extra human approval is required for routine candidate operations. Issue, PR, review, merge, Actions status, command exit 0, or model self-review never closes a mathematical obligation.
