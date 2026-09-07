# Lean Proof Fixture

<!-- MATHEMATICAL_REASONING_DISCIPLINE_V1 -->

This fixture inherits `governance/standards/MATHEMATICAL_REASONING_DISCIPLINE.md`: the formal statement must match frozen definitions and quantifiers, induction/contraposition must be logically valid, and kernel success still requires axiom/escape and statement-faithfulness audits.

本目录用固定 Lean/Mathlib 构建一个无逃逸的最小定理，并输出 `#print axioms` 供证据层审计。

```text
lean-proof/
├── AGENTS.md
├── README.md
├── lean-toolchain
├── lakefile.toml
├── lake-manifest.json
├── VibeMathingFixture.lean
└── AxiomAudit.lean
```

- `lean-toolchain` 固定 Lean 版本；`lakefile.toml` 固定直接依赖，`lake-manifest.json` 锁定全部传递依赖。
- `VibeMathingFixture.lean` 是唯一形式化陈述真相源。
- `AxiomAudit.lean` 只导入已构建模块并执行 `#print axioms`，避免为公理审计重复解释顶层 Mathlib 源文件。
- `.lake/` 是可重建缓存，不属于 fixture 事实。
