# Project Skills

这里记录中央项目 active skills；问题仓库 builder 会按 Web profile 生成不同的固定 Skill 集合。每个目录只有一个稳定 owner；上游方法先进入受控 source snapshot，经过 owner mapping、依赖适配和压力测试后才能分发。

| Skill | 单一职责 |
|---|---|
| `vibe-mathing-router` | 根据当前瓶颈选择一个主流程 |
| `math-discovery` | 研究问题、检索、来源和证据图 |
| `math-derivation` | 公式推导与假设/近似边界 |
| `math-computation` | 符号、数值与反例计算 |
| `math-proof` | 自然语言证明与证明义务审计 |
| `math-formalization` | proof assistant 形式化与 kernel 验证 |
| `nvidia-private-compute` | 数学客户端白名单内的固定私密 GPU canary |

问题库中的 CandidateObservation 只归 `math-discovery`，且始终 `research_eligible=false`。工具调研按 `surveyed → source_locked → installed → smoke_checked → evidence_capable → verifier_admitted` 逐层准入；只有项目 runtime probe 支持的能力才能进入 owner 路由。

对已准入开放问题，skills 在 `persistent_research` 下按“一题一个 worker、一个有界 step、一个 checkpoint”工作。skills 负责数学路线，Harness 负责 session/scope/配额；路线失败追加 failed-route 后换路，checkpoint 进展摘要和 Goal 文案都不能升级为 Result。

数学定理、形式包、序列、对象数据库、公式与算法复用统一读取 `governance/control-plane/math-knowledge-source.v1.json` 和 `math-knowledge-operators.v1.json`。所有命中先形成 `KnowledgeHit`/`ReusePlan`/Candidate，不直接创建 EvidenceLink、Result 或 Solution。

Web 问题仓库固有集合为 8 个：router/discovery/derivation/proof/solve 为 active，computation/formalization/math-toolchain 为 constrained。`solve` 固定 0.3.0 并按需加载 477 条算子中的少量相关项；`math-toolchain` 固定 0.2.0，只生成 ToolPlan。`nvidia-private-compute`、`auto-goal`、`auto-tmux` 不进入问题仓库或通用 Suite。
