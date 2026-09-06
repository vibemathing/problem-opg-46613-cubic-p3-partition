---
id: GOV-STANDARDS-AGENTS
type: context
status: current
owner: engineering
created: 2026-08-13
last_reviewed: 2026-08-13
review_cycle: P90D
---

# Standards Guide

本目录保存跨任务长期生效的项目标准。任务证据留在 `governance/tasks/`，架构取舍留在 `governance/decisions/adr/`，可阻止交付的检查留在 `governance/architecture-gates/rules/`。

## 目录结构

```text
standards/
├── AGENTS.md                       # 标准目录职责、文件地图和维护边界
├── VIBE-MATHING-SPEC-v0.1.md       # 历史规范，保留可追溯性
├── VIBE-MATHING-SPEC-v0.2.md       # 当前研究闭环、输入与输出规范
├── Ponytail工程阶梯标准.md          # 新增所有权面的存在性判断
├── 未来最优解原则.md                # 从长期正确终态倒推迁移切片
├── 工程质量标准.md                  # 通用工程质量要求
├── 架构设计原则.md                  # 单一真相、信任分层、能力有界与依赖方向
├── 劣质代码定义.md                  # 不可接受的工程模式
└── 非功能性需求标准.md              # 性能、可靠性、安全等默认检查面
```

## 依赖与边界

- `VIBE-MATHING-SPEC-v0.2.md` 是当前研究闭环规范真相源；v0.1 只保留历史，ADR-0000/0001 解释决策，GATE-0002/0003 和研究空间校验器执行门禁。
- 标准只定义长期规则，不保存任务状态、运行输出或临时研究结论。
- 新增或修改标准后必须重建治理索引，并运行 governance strict/health 与相关项目测试。
