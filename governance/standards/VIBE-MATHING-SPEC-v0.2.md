---
id: STD-VIBE-MATHING-SPEC-V0.2
type: standard
status: current
owner: engineering
created: 2026-08-14
last_reviewed: 2026-08-14
review_cycle: P90D
version: 0.2
source: ADR-0000,ADR-0001
related_gates: [GATE-0002, GATE-0003]
supersedes: STD-VIBE-MATHING-SPEC-V0.1
---

# VIBE-MATHING-SPEC v0.2

本规范定义 `vibe-mathing-cn` 的最小可信研究闭环。它是项目级规范，不声称是 ISO、IEEE、AMS 或数学共同体统一标准。

## 目标

建立以下逻辑接口：

```text
ProblemContract -> ResearchBundle
```

非可信 Agent 只探索候选；受信验证链裁决候选；只有完整、保真、可独立复核且证据当前有效的证明或反例进入解库派生视图。

## 规范词

- `MUST` / 必须：不满足即违反规范。
- `MUST NOT` / 禁止：出现即违反规范。
- `SHOULD` / 应当：默认遵守；偏离时必须记录理由和风险。

## 对象与视图

- `Problem` / `ProblemContract`：同一个 canonical 输入对象，回答“研究什么、在什么边界内研究”。
- `Attempt`：一次 ResearchRun 的机器对象，回答“做过什么”。
- `Result`：一项原子数学主张及其证据账本，回答“真正知道了什么”。
- `Solution View`：从合格 Result 派生的只读解库索引。
- `ResearchBundle`：按一个 Problem 聚合 Problem / Attempt / Result / evidence / Solution View 的只读响应，不是第四张真相表。
- `Verification Artifact`：可复查的计算、审查、证明证书、内核输出或忠实性审计产物。

## 三条基本法则

### R1 — 候选隔离

系统事实链必须是：

```text
Problem -> Attempt -> Result
```

- Agent 只能创建 Attempt 和候选 Result，禁止自行宣布问题已解决。
- Result 必须引用产生它的 Attempt，Attempt 必须引用同一个 Problem。
- Solution View 和 ResearchBundle 必须从事实表派生，禁止成为独立写入源。

### R2 — 验证准入

Result 必须分开记录 `outcome × evidence`。证据是能力集合，不是线性等级。

Solution View 只允许：

```text
proof + established
counterexample + refuted
```

两者都必须具备当前有效的独立直接验证和 `statement_faithfulness=accept`。依赖 `kernel_check` 的直接验证还必须有 `axiom_escape_audit`。Agent 自报、数值支持、符号支持、局部结果和失败路径均不能闭合原问题。

### R3 — 证据守恒

每项可晋升结论必须形成：

```text
Problem -> Attempt -> Result -> Verification Artifacts
```

- 证据和失效记录只追加，不覆盖历史。
- 当前结论、Solution View 和 ResearchBundle 必须由当前有效证据重算。
- 来源、引用、验证产物或陈述忠实性断链时，Result 必须退出 Solution View。

## ProblemContract v1

canonical Problem 必须使用 `schema_version=1.0.0`，并冻结：

- 稳定 `problem_id`、版本化 `statement`、`domain`、`quantifiers`；
- `definitions`、`assumptions`、`allowed_axioms`；
- `sources` 与 MSC 分类；
- `acceptance.policy=solution-admission-v1`；调用者不能声明更弱策略；
- `constraints.allowed_methods`、`allowed_adapters`、`max_attempts` 和运行预算；`allowed_adapters=[]` 表示只允许非自动研究；
- `lifecycle=draft|active|withdrawn`。

ProblemContract 禁止保存 `open|solved|refuted` 解题状态。解题 disposition 只能从 Result 与有效证据派生；否则 Problem 与 Result 会形成双真相。

ProblemContract lifecycle 只允许 `draft → active → withdrawn` 或 `draft → withdrawn`。只有 `active` 可以创建新 Attempt；withdrawn 必须保留既有 Attempt/Result 历史，但拒绝新研究。Attempt 方法、adapter、次数和 runtime 必须服从契约约束。

## ResearchBundle v1

ResearchBundle 必须在一致快照上按稳定 ID 排序并包含：

```text
problem
attempts[]
results[]
evidence[]
disposition
solution_view[]
unresolved_obligations[]
```

disposition 的唯一合法值和语义是：

- `solved`：存在通过准入的 `proof + established`；
- `refuted`：存在通过准入的 `counterexample + refuted`；
- `open`：不存在任何通过准入的闭合结果。

同一 Problem 同时存在通过准入的 proof 与 counterexample 时，系统必须以非零错误 fail-closed；`conflict` 不是第四种正常 disposition，系统不得任选一侧或降级为 `open`。

## 操作层要求

1. 记录模型、工具、输入摘要、日期、计算资源和人类干预。
2. 同时探索证明、反例、边界条件、变体和既有工作。
3. 保存版本化修补与 proof-obligation ledger，修补后重验依赖。
4. 最终闭合必须来自独立工具或领域专家。
5. 形式化验证必须固定工具链、扫描逃逸、审计公理并独立检查 statement faithfulness。
6. 发现错误时追加失效记录，不覆盖原证据。

## 当前机器实现

- 输入契约：`problem-library/schema/canonical-problem.schema.json`。
- 事实契约：`research/schema/attempt.schema.json`、`result-library/schema/result.schema.json`。
- 输出契约：`research/schema/research-bundle.schema.json`。
- 准入与冲突裁决：`scripts/validate_research_spaces.py`。
- 派生输出：`scripts/vibe_mathing/bundle.py`、`scripts/vibe_mathing_cli.py export-bundle`。
- 正负例：`scripts/test_problem_contract.py`、`scripts/test_research_bundle.py`、`scripts/test_research_spaces.py`。

## 成熟度边界

当前实现已具备单机、单 Agent 的契约、存储、证据、恢复、SymPy/Lean fixture 和派生输出能力。纯合成测试证明系统语义，不构成任何真实数学问题的新结论。真实问题处理、自然语言到形式陈述的代表案例校准和外部 reviewer 实际签发仍是独立阶段。

## 一句话

> Agent 产生可能，验证建立事实，ResearchBundle 只汇总当前事实。
