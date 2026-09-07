# math-toolchain Web Snapshot

- 本目录是计算容器 `math-toolchain` 0.2.0 的 Web 约束适配，不是节点运行时副本。
- 只允许修改 ToolPlan/Candidate 语义；不得添加命令执行、安装器、远端连接、凭据、GPU 或证据签发能力。
- `VERSION` 保留上游功能版本；Web 适配差异记录在 `CHANGELOG.md` 和容器 Skill source lock。
- 相对引用必须指向问题仓库内现有文件；禁止依赖 `$CODEX_HOME`、中央仓库或计算节点路径。


## Mandatory mathematical reasoning discipline

<!-- MATHEMATICAL_REASONING_DISCIPLINE_V1 -->

This scoped instruction file inherits `governance/standards/MATHEMATICAL_REASONING_DISCIPLINE.md`. Its local rules may only tighten that standard; they cannot omit, replace, or weaken definition/quantifier freeze, traceable dependencies, valid induction and contraposition, explicit witnesses, counterexample pressure tests, invariants, termination, extremal/symmetry/probability/scale checks, or honest evidence ceilings.
