# 算子选择协议

本文件把“从 477 条目中选什么”压成一个有限、可复核的流程。它是检索与编排建议，不是新的运行时
selector，也不授予宿主任何权限。

## 输入最小集

开始前尽量得到四项：

| 输入 | 要回答的问题 |
|---|---|
| `goal` | 最终要改变或判断什么？ |
| `state` | 当前已有事实、产物、失败现象和未知量是什么？ |
| `constraints` | 时间、资源、风险、权限、格式或不可改变的条件是什么？ |
| `success` | 什么证据足以接受、拒绝或暂停？ |

缺少其中一项时，安全做法是最多问三个澄清问题；若可以安全推断，必须把假设写出来，不要悄悄补全。

## 选择顺序

1. **先做安全门**：判断是否涉及现实副作用、敏感数据或医疗/法律/化学安全；高风险先 `escalate`，
   不从算子文本获得执行授权。
2. **再定功能类**：用 taxonomy 的 `functional_class` 判断当前主要需要表征、分解、变换、搜索、构造、
   验证/证伪、诊断/修正还是控制/元认知。
3. **再看来源域**：只有当来源域能改变适用性或证据标准时，才选择 mathematics、programming、physics、
   chemistry 等具体 pack；来源域是出处，不是能力等级。
4. **读取 catalog**：根据 `references/catalog.json` 找到 pack 路径，再读取 taxonomy 或 pack 元数据；
   不先打开全部 JSON。
5. **筛候选**：按 `core_question`、`applicability.when`、`not_when`、前置条件和所需证据筛出 1 个主算子，
   最多 2 个辅助算子；候选过多时先用 `task-framing` 或 `problem-space-model`。
6. **检查语义类型**：`MentalModelSpec` 只能作为观察视角使用；需要改变状态或产生证据时，选择
   `OperatorSpec` 或 `MethodSpec`，不能把视角当成动作。
7. **检查前置条件**：不满足就补采样、重表征、降低范围或返回 `not_applicable`，不要强行执行。
8. **执行一个小步**：每次只改变一个明确假设或子目标，记录输入、操作、观察和剩余不确定性。
9. **检查证据能力**：多门验收先声明 required capability set，逐项核对身份、范围和新鲜度；不存在
   “源码扫描自动升级为 build/kernel/semantic 通过”。
10. **判断结果**：证据足够则停止或进入下一子目标；证据不足则 `revise`、`switch` 或 `escalate`，
   不以重复相同推理代替新信息。

## 功能类起点

| 当前问题 | 优先功能类 | 可先查的稳定 ID |
|---|---|---|
| 问题说不清、目标含糊 | `representation` | `psoa.problem-solving-methodology.task-framing`、`psoa.mathematics.definition-first` |
| 大问题无从下手 | `decomposition` | `psoa.problem-solving-methodology.means-ends-analysis`、`psoa.computer-science.problem-decomposition` |
| 想换一种等价视角 | `transformation` | `psoa.problem-solving-methodology.representational-change`、`psoa.computer-science.reduction` |
| 要找候选或搜索路径 | `search` | `psoa.problem-solving-methodology.heuristic-search`、`psoa.computer-science.backtracking` |
| 要做出可检查的候选 | `construction` | `psoa.problem-solving-methodology.constructive-witness`、`psoa.engineering.engineering-prototype` |
| 要判断是否成立 | `verification-falsification` | `psoa.mathematics.counterexample`、`psoa.mathematics.proof-audit` |
| 要验收形式证明/规格 | `verification-falsification` | `psoa.formal-logic-automated-reasoning.machine-semantic-dual-audit`、`psoa.problem-solving-methodology.evidence-capability-admission` |
| 已失败但不知道原因 | `diagnosis-revision` | `psoa.programming.hypothesis-driven-debugging`、`psoa.programming.minimal-reproduction` |
| 需要停止、回退或分配预算 | `control-metacognition` | `psoa.problem-solving-methodology.metacognitive-monitoring`、`psoa.programming.resource-bounded-loop` |

上表中的 ID 是稳定引用；若某个 pack 在未来改名，必须以 catalog 和实际条目为准，不凭短名称猜路径。

## 停止与切换

- `succeeded`：成功条件已由宿主 Verifier 或可复核证据支持。
- `failed`：前置条件满足，但动作明确未达到目标；保留失败证据。
- `inconclusive`：信息、实验或证明不足，不能推出真假。
- `not_applicable`：问题形态与算子不匹配，或安全边界不允许。
- `switch`：重复状态、无新增信息、假设无法区分或当前表示阻塞搜索。
- `escalate`：需要权限、专业判断、不可逆操作或高风险批准。

形式证明还要区分声明、候选和接纳结果；若只有静态源码锁定而没有 fresh replay、kernel 或语义审查，
应返回当前证据支持的有限状态与缺口，不能把“没有发现问题”改写成“证明完成”。

默认禁止无界重试；每次继续都要说明新增信息和下一步停止条件。
