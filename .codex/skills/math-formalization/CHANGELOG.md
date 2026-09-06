# Changelog

## 0.5.0

- 增加 exact-version 形式包 resolver、跨 proof assistant 隔离和 quarantine 工具链 fail-closed 规则。

## 0.4.0

- 形式化 step 必须可中断、可恢复并绑定 checkpoint；超时或编译失败只关闭当前路线，不改变数学结论。

## 0.3.0

- CandidateObservation 与 formal-conjectures benchmark 条目不再自动触发形式化或 Result。
- formal-conjectures 绑定 vendor 固定 commit/immutable snapshot，并强制独立 statement-faithfulness 审计。

## 0.2.0 - 2026-08-26

- 增加输入/工具链绑定的 verifier receipt、claim strength、未闭合义务和结构化失败分类。
- 增加空洞陈述、调用者自报 PASS、陈旧 receipt、timeout 与静默 claim 升级压力测试。
- 接入固定 commit 的 Lean 官方 Skills、MathEvidence、ITPEval 与 atp-checkers 证据谱系，同时保留项目更严格的最终门禁。

## 0.1.0 - 2026-08-13

- 建立 Lean 工具预检、无 sorry 门禁、kernel-check 与 faithfulness 分离契约。
