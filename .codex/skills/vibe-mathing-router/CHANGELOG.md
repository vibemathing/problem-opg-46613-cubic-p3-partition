# Changelog

## 0.4.0

- 接入数学知识 source/operator registry；命中既有定理、包或数据库时先生成 ReusePlan/Candidate，再路由到唯一 owner。

## 0.3.0

- 增加单问题单 worker 的 persistent_research 路由；无限循环由 checkpoint 驱动，不启动并行工厂或无界命令。

## 0.2.0

- CandidateObservation 或缺少 active ProblemContract 时强制路由到 discovery。
- 来源状态、形式 build 和 surveyed/source_locked 工具不再触发越级研究或验证路线。

## 0.1.0 - 2026-08-13

- 建立按当前瓶颈单路由的 Vibe Mathing 项目入口。
