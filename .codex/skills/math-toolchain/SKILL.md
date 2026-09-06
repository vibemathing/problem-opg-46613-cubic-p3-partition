---
name: math-toolchain
description: "网页版数学工具链规划入口。用于选择符号、数值、数据库或形式化路线并生成有界执行计划；不执行工具、不签发回执、不接纳数学结果。"
---

# Math Toolchain（Web constrained）

## When to Use

- 候选研究需要判断使用 SymPy、SageMath、OEIS、LMFDB、Lean/Mathlib 或其他已登记工具；
- 需要在 symbolic、numeric、database、formalization 路线之间选择；
- 需要为后续受信执行器生成带版本、预算、超时和预期证据能力的计划。

## Required Inputs

- 冻结的 ProblemContract、当前 Obligation 和已有 EvidenceLink；
- `governance/control-plane/math-tool-maturity.v1.json`；
- `governance/control-plane/math-knowledge-source.v1.json`；
- `governance/control-plane/math-knowledge-operators.v1.json`；
- 当前 Harness snapshot 与 Web output contract。

## Web Channel Contract

本 Skill 状态固定为 `constrained`：

1. 只能选择已登记、许可闭合且 maturity 足够的工具或来源；
2. 只能输出 `ToolPlan`、`ReusePlan` 或 Candidate 中的建议步骤；
3. 必须写明 exact version、输入摘要、预算、timeout、失败语义和 `evidence_ceiling`；
4. 不得声称命令已经执行，不得生成 stdout/stderr、kernel receipt、semantic review receipt 或 EvidenceLink；
5. 不得安装软件、访问计算节点、调用 GPU、修改 workflow 或写入受保护真相路径；
6. 数据库命中、符号化简和有限数值检查都不能自动成为一般性证明。

## Routing

- 来源与既有结果发现：`math-discovery`；
- 推导与候选路线：`math-derivation`；
- 计算设计：`math-computation`；
- 自然语言证明义务：`math-proof`；
- Lean 草稿与形式化计划：`math-formalization`；
- 方法选择：`solve`。

## Minimal Output

```json
{
  "tool_or_source_id": "<registered id>",
  "purpose": "<one bounded obligation>",
  "exact_version": "<required version or query profile>",
  "inputs": [],
  "budget": {"timeout_seconds": 0, "max_output_bytes": 0},
  "expected_artifact": "candidate_only",
  "evidence_ceiling": "<registry ceiling>",
  "execution_status": "not_executed"
}
```

## Boundaries

`ToolPlan` 不是执行回执；计划可行、CI 通过、PR 合并或模型自评都不是 Evidence、Result 或 Solution。实际执行必须由网页渠道之外的受信、受预算 Harness 完成并独立回读。
