# Web Mathematical Toolchain Model

The Web channel must distinguish planning from execution.

- Repository reads, source comparison, derivation, proof drafting, and ToolPlan creation produce Candidates.
- Commands, CAS, SMT, numerical programs, and proof assistants count as executed only when an authorized runtime emits a reproducible receipt.
- Every execution is bounded by timeout, resources, output size, versions, deterministic inputs/seeds where applicable, and termination behavior.
- Numerical/FP32/GPU output is screening or numeric support within its declared scope; it is not a universal proof.
- Symbolic simplification proves only the encoded expression under the tool's assumptions.
- Kernel success proves only the encoded formal theorem under reported axioms/environment; statement faithfulness and escape/axiom audit are separate evidence.
- `surveyed`, `source_locked`, and `installed` are maturity states, not evidence capability.

When execution is unavailable, emit a bounded ToolPlan or verifier request. Never fabricate stdout, exit status, versions, digests, CI state, or verifier receipts.
