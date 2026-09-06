# Lean/Mathlib 最小验证样例

该 fixture 证明三件事：固定工具链可构建、定理无 `sorry/admit/unsafe`、`#print axioms` 输出可审计。它不证明任何开放数学问题，也不替代陈述忠实性审查。

项目 adapter 优先从 `PATH` 查找 `lake`，并兼容 elan 官方默认安装目录 `~/.elan/bin`；所有 Lean 命令均通过 `lake env lean` 运行，以服从 fixture 的固定 toolchain。两处都不存在时 fail-closed。

```bash
lake update
lake exe cache get
lake --quiet build
lake env lean AxiomAudit.lean
```
