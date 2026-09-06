# math-toolchain Web Snapshot

- 本目录是计算容器 `math-toolchain` 0.2.0 的 Web 约束适配，不是节点运行时副本。
- 只允许修改 ToolPlan/Candidate 语义；不得添加命令执行、安装器、远端连接、凭据、GPU 或证据签发能力。
- `VERSION` 保留上游功能版本；Web 适配差异记录在 `CHANGELOG.md` 和容器 Skill source lock。
- 相对引用必须指向问题仓库内现有文件；禁止依赖 `$CODEX_HOME`、中央仓库或计算节点路径。
