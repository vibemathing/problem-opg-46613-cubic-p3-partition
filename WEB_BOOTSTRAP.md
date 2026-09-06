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
- Harness suite: `harness-source:web-research-full` `1.1.0`
- Suite manifest SHA-256: `7dfdb41a68bfda314d663ba03b4b2a713ea194168ade5287e58c6434be5cc4fb`
- Harness snapshot SHA-256: `121c0304e89d3ebd56e34a594ff575ceb41ad335de1ec2bb572971a668829111`
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

## AI-native writable route

After repository admission, perform the routine candidate transport end to end without project-added human handoffs:

1. Open or use one Issue labeled `web-research-question` for the bounded question.
2. Create branch `web/attempt-<attempt-suffix>`.
3. Add, revise, or delete files only under `research/artifacts/web-inbox/**`, `research/artifacts/candidates/**`, or `research/artifacts/source-notes/**`.
4. Commit real changes and open a PR using the web candidate template.
5. Monitor required checks and, when needed, rerun the existing candidate workflow.
6. Review and revise the candidate PR; this AI review is not independent mathematical review.
7. After transport checks pass, merge the candidate PR and write the next checkpoint.

Do not create repositories, direct-push the default branch, modify workflow/truth paths, force-push, cancel/dispatch Actions, or sign Evidence/Result. Follow only platform-mandatory confirmation UI; no extra human approval is required for routine candidate operations. Issue, PR, review, merge, Actions status, command exit 0, or model self-review never closes a mathematical obligation.
