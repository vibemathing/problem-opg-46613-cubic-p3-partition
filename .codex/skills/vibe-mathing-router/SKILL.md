---
name: vibe-mathing-router
description: "数学研究任务路由器。用户提出找问题、查文献、推公式、做计算、写证明或形式化验证，但当前瓶颈尚未明确时使用；每次只选择一个主 skill。"
---

# Vibe Mathing Router

识别当前数学研究瓶颈，只把任务交给一个 owner；不把整条研究链同时启动。

## When to Use This Skill

- 用户提出开放式数学问题，但尚未说明需要检索、推导、计算还是证明。
- 输入混合了论文、公式、猜想和代码，需要先决定当前最短验证路径。
- 用户问“下一步该做什么”或“该用哪个数学 skill”。

## Not For / Boundaries

- 已明确要求符号计算、证明或 Lean 验证时，直接使用对应 owner。
- 不生成数学结论，不替代领域知识或机械验证。
- CandidateObservation、论坛 answered、目录 resolved 或形式题面 build 都不能触发 computation/proof/formalization；未形成 active ProblemContract 时只能路由到 `math-discovery`。
- 调研到的工具只有达到对应运行时准入状态后才能路由；`surveyed/source_locked` 不等于 installed 或 verifier-admitted。
- 不因输出文件类型选择路线；按当前阻塞选择。
- 用户要求持续推进时仍只选一个 owner skill 和一个 worker；“无限持久攻坚”表示 checkpoint 驱动的 bounded steps，不表示并行工厂、无界命令或自动重复发送 Goal。

## Quick Reference

```text
CandidateObservation/缺少 ProblemContract -> math-discovery
缺少问题边界/前人工作 -> math-discovery
公式对象、假设或近似不清 -> math-derivation
需要精确计算、数值实验、反例搜索 -> math-computation
需要定理证明、补步骤、攻击证明 -> math-proof
需要 Lean/内核级验证 -> math-formalization
```

路由输出必须包含：当前阶段、主 skill、选择理由、必需输入、停止条件、唯一下一步。

## Reuse-first 数学知识路由

路由前读取 `governance/control-plane/math-knowledge-source.v1.json` 和 `math-knowledge-operators.v1.json`。若当前缺口可能由既有定理、形式包、序列、数学对象数据库、公式参考或算法实现覆盖，先路由到 `resolve_formal_package` / `search_*` / `compare_statement`，再决定 derivation、computation、proof 或 formalization。registry 命中、package build 或搜索成功都只产生 Candidate/ReusePlan，不闭合义务。

## Examples

### Example 1：候选库开放问题
- 输入：“研究候选库里这个 resolved 问题。”
- 动作：选择 `math-discovery`，先核验来源状态、原题、许可和 ProblemContract；不把 resolved 当 Result。
- 验收：没有创建 Attempt，只给出准入缺口与唯一下一步。

### Example 2：明确恒等式
- 输入：“检查这个积分恒等式。”
- 动作：选择 `math-computation`。
- 验收：产出可重跑计算和适用条件，不标记为一般性证明。

### Example 3：形式化请求
- 输入：“把这个证明写成 Lean。”
- 动作：选择 `math-formalization` 并先运行工具预检。
- 验收：Lean 缺失时状态为 blocked/calibration，不伪造 kernel-check。

## References

- `references/source-map.md`：项目 owner 映射来源。
- `references/pressure-tests.md`：路由误触发压力场景。

## Maintenance

- Sources：本项目 owner mapping 与供应链审计结果。
- Last updated：2026-09-05。
- Verification：`python3 scripts/validate_project.py`。
