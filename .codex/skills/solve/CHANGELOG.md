# Changelog

## 0.3.0 - 2026-09-05

### Added

- 新增 6 个形式证明工程相关 source：声明/候选/结果分离、证据能力接纳、失败路线记忆、陈述身份审计、
  精确强度审计和占位符可达性审计。
- 新增 3 个 derived Method：有界义务循环、机器—语义双审计、路线优先产物审计。
- 增加大型形式证明仓库压力场景，覆盖测试夹具占位符、静态扫描、fresh replay 缺失和证据跳级。

### Changed

- 强化证明状态子目标分解：使用稳定 obligation ID、依赖 DAG、状态与自底向上闭合规则。
- 强化来源权威与血缘审计：区分 original、adapted、imported、model-generated 等贡献角色。
- 强化元认知监控：只把义务关闭、未知减少、反例排除或证据能力增加视为实质进展。
- Reference Library 更新为 56 个 pack、417 source、60 derived、477 total。

### Reason

- FLT/Prove2Me 案例证明：长期难题需要冻结问题、分离候选与结果、按能力逐门验收、保存失败路线；
  source/build/kernel/semantic 不能被错误压成允许自动跳级的线性证据阶梯。

### Affected

- `SKILL.md`、`README.md`、`AGENTS.md`、选择/输出/质量/压力 references，以及三类 operator pack、
  catalog、inventory 和 taxonomy 发布快照。

### Validation

- `validate-skill.sh --strict` 对项目、WSL、Windows 三份 Skill 分别执行。
- 源库和三份 Skill 内 Reference Library 校验。
- 三份受管文件 SHA-256 manifest 一致性比对。

### Risk

- 证据能力接纳会让只有静态源码或自报状态的任务更早返回 `inconclusive`/缺口状态；这是有意的
  fail-closed 行为。新增条目仍是 `experimental`/reference-only，不代表真实 Agent 效果已验证。

### Rollback

- 恢复 `0.2.0` 的入口文档和 468 条目快照，再将该版本同步到两个 Codex 目录；不得用删除整个 Skill
  目录的方式回滚。

### Source

- Pi session `[redacted-session-identifier]`、`vibe-mathing-cn-internal` 的案例报告、
  ProblemContract/Result/checkpoint/failed-route 契约、数学证明 Skill，以及现有官方 reference frameworks。

## 0.2.0 - 2026-09-04

### Changed

- 将 `SKILL.md` 收敛为可执行的选择循环：先做安全门，再按功能类和前置条件按需加载 pack。
- 明确“非算子任务”边界、缺失输入的最多三个澄清问题、证据标签和无界循环禁止规则。
- 将四个示例改为带 Input、Steps、Expected 的可复现案例，并使用真实稳定 operator ID。
- 新增 `selection-protocol.md`、`output-contract.md` 和 `quality-checklist.md`，补齐选择、证据和发布门禁。

### Reason

- 原入口虽然结构校验通过，但示例偏叙述、选择标准不够机械、缺少必填输入处理和质量清单，低上下文
  Harness 容易整库加载或把参考条目误当成已执行结论。

### Affected

- `SKILL.md`、`README.md`、`AGENTS.md`、`references/index.md`、三个新增 reference、压力场景和版本元数据。

### Validation

- `validate-skill.sh --strict`。
- 源库与 Skill 副本 `validate_harness.py --operator-library`。
- 项目 architecture、contract、test gates；治理 strict/health。

### Risk

- 更明确的选择上限和安全升级可能让信息不足的任务更早返回 `inconclusive` 或 `escalate`；这是有意的
  fail-closed 行为，不代表领域结论失败。

### Rollback

- 将 `VERSION` 恢复为 `0.1.0`，恢复本次修改的入口与 references 文档；算子 JSON 快照不需要回滚。

### Source

- `auto-skill` quality checklist、Skill Spec、Superpowers pressure-testing contract、Ponytail existence
  gate，以及项目 `operators/`、PSOA PRD 和用户对短名称/可执行 Skill 的要求。

## 0.1.0 - 2026-09-04

### Added

- 建立短名称为 `solve` 的可移植 Skill 包。
- 将 `operators/` 的 catalog、source inventory、taxonomy、Core Schema 和 56 个 pack 复制到
  `references/`，使安装后的 Skill 自包含。
- 增加按需加载、宽松调用结果、边界规则和四个使用示例。

### Source and ownership

- 内容真相源仍是仓库根目录 `operators/`；Skill 内 JSON 是发布快照，不是第二份可编辑内容库。
- Skill 不拥有运行时 selector、工具权限、执行结果、业务状态或密钥。

### Validation

- 原始发布包曾通过 owner strict validator；Web 快照改用仓库内 `python3 scripts/validate_web_problem_harness.py --project-root .`、
  `uv run --locked --script scripts/validate_harness.py --operator-library operators/catalog.json` 和
  `uv run --locked --script scripts/validate_harness.py --operator-library skills/solve/references/catalog.json`；
  两个库均保持 `411/411`、`57/57`、`468`。
