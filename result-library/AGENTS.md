# Result Library Agent Guide

本目录是已结构化研究成果的真相源。`records/results.jsonl` 保存 `outcome × evidence` 二维状态；`indexes/solutions.json` 只是完整解的派生索引。

## 目录结构

```text
result-library/
├── AGENTS.md
├── README.md
├── schema/result.schema.json
├── records/results.jsonl
└── indexes/solutions.json
```

## Result 验收数学推理纪律

<!-- MATHEMATICAL_REASONING_DISCIPLINE_V1 -->

Result gate 必须按 `governance/standards/MATHEMATICAL_REASONING_DISCIPLINE.md` 复核定义/量词冻结、完整依赖链、显式 witness、反例攻击、不变量、单调量与终止、极值/对称/概率方法前提、尺度/边界以及证据能力。有限样本不得冒充归纳；逆否必须保持 `P → Q` 与 `¬Q → ¬P`；kernel check 必须与 statement-faithfulness、axiom/escape audit 分离。任一必要义务未闭合时拒绝 `established/refuted`。

## 职责与依赖

- 上游：每个结果必须引用一个 canonical `Problem` 和一个 `Attempt`。
- 下游：完整解查询只消费 `indexes/solutions.json`，但详情必须回到 `records/results.jsonl`。
- 数值证据、符号证据、局部结果和失败路径不能使用 `established` 或 `refuted` 闭合原问题。
- `proof` 的完整解验证接受独立人工审查，或同时具备 proof assistant 内核检查与公理/逃逸审计；反例接受独立反例检查、人工审查，或内核检查与公理/逃逸审计；两者都要求陈述忠实性证据。
- `prior_art_review` 记录归因和新颖性，不替代数学正确性的直接验证。
- 证据账本只追加；失效记录只能引用更早的 `evidence_id`，当前结论由未失效证据派生。
- Result 与 Attempt 必须引用同一个 Problem；独立证据的 verifier 必须不同于 Attempt.generator，并绑定可复查摘要。
- 不手工制造不在 `results.jsonl` 中的解库条目。
- 同一 Problem 的 proof 与 counterexample 不得同时满足完整解准入；冲突必须阻止写入与 ResearchBundle 导出。
- 新增、删除或移动文件时同步维护本文件与 README。

## 验证

```bash
python3 scripts/validate_research_spaces.py
```
