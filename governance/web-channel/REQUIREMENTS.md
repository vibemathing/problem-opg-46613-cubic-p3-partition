# Web GPT + GitHub Candidate Channel Requirements

The channel reads a self-contained single-problem repository and acts only as a candidate generator and GitHub transport writer.

Required capabilities, when confirmed by fresh GitHub receipts, are repository read, Issue write, candidate branch/file/commit write, Pull Request create/review/merge, and read/rerun of the existing candidate workflow. Repository administration, secrets, workflow writes, direct default-branch writes, force push, Evidence signing, and Result admission are excluded.

Machine boundaries:

- candidate writes are limited to paths declared by `WEB_CHANNEL_PROFILE.json`;
- every branch binds one pre-admitted Attempt, Route, graph, and Obligation;
- PR gates validate the immutable Harness snapshot, packet schema, complete diff, path/mode/size budgets, and privacy;
- GitHub operations and model self-review are not independent mathematical verification;
- actual capabilities remain pending until the acting principal and repository rules have fresh object receipts;
- platform-mandatory confirmation is allowed, but the project adds no routine human handoff inside the admitted candidate loop.

The repository must never depend on local compute-node orchestration, private credentials, another repository's moving branch, or unstated tools. If command execution is unavailable, the channel emits a Candidate, ToolPlan, or verifier request rather than fabricated execution output.
