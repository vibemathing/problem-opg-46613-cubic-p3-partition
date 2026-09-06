# Web Mathematical Knowledge Reuse Requirements

Mathematical knowledge lookup is reuse-first and evidence-bounded.

- Every source has an ID, class, maturity, operational status, license/use policy, version resolver, and evidence ceiling.
- Every operator has one owner Skill, declared inputs/outputs, external effect, timeout/failure behavior where executable, and evidence ceiling.
- Search hits, theorem names, package availability, formula matches, and model recollection remain Candidates until exact statements, assumptions, versions, attribution, and reuse gaps are checked.
- `surveyed` and `source_locked` do not mean installed; `installed` does not mean verifier-admitted.
- Formal reuse requires an exact package/library version and a statement comparison against the frozen Obligation.
- A reused theorem can close only the matching dependency; remaining glue obligations must be proved and verified separately.
- Public artifacts include only sources and content whose license/use boundary permits redistribution.

The registries in `governance/control-plane/math-knowledge-source.v1.json` and `math-knowledge-operators.v1.json` are the machine truth. Skills route work but cannot raise a source/operator above its registered maturity or evidence ceiling.
