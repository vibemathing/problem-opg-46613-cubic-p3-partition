# Changelog

## 0.4.0

- 增加 Mathlib/Reservoir/AFP/MathComp、OEIS/LMFDB/DLMF/SageMath 的受控知识检索与陈述关系分类。

## 0.3.0

- 持久研究新路线前读取 failed-route 历史；发现阶段只更新下一义务，不越级创建 Attempt/Result。

## 0.2.0

- 接入 admitted/candidate 联邦问题查询，但默认保持 admitted。
- CandidateObservation 保持 `research_eligible=false`，来源状态不得映射为数学 Result。
- 新增来源 registry、raw locator、许可边界和 identity review queue 规则。

## 0.1.0 - 2026-08-13

- 合并研究问题、文献发现、来源账本、证据图和数学查新边界。
