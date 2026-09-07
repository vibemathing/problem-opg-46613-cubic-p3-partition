# C08 PR18 review repair, version r01

Verdict: `candidate_only`. This is a versioned source-repair draft, not a compiled theorem or verifier receipt. No new graph theorem is proposed. The frozen C08 files and packet remain unchanged.

## Changes and exact semantic boundary

`lean/MathlibTargets.lean` replaces only the H graph constructor and adds an adjacency-contract lemma. SimpleGraph.fromRel uses the relation `forwardEdge q u.val v.val`; the documented adjacency is exactly `u != v` together with the disjunction of the forward and reversed relations. Thus the intended simple-graph relation is unchanged. No compatibility assumption about Std.Symm or Std.Irrefl constructors is needed at this call site. FiniteTarget, FamilyTarget, RootProblem and both bridge targets remain unproved Prop definitions. The new H_adj proof is a draft until compiled.

`lean/Local.lean` preserves all edge lists, bit ordering, local validity, InternalAdj, ClosedFive, boundary cases and the six closed-cycle certificates. It preserves the public internal_degree_faithful statement but replaces its full 4096-by-9 decidable proof attempt with nine symbolic row lemmas. Each row splits only its two or three incident bits, after a mod-two bound; the generated proof script has 60 row leaves rather than enumerating every state/vertex pair. This is a source-structure count, not a measured speed or memory result. The remaining valid_boundary decidable proofs are unchanged and may still require further work.

The unlimited heartbeat setting is replaced by maxHeartbeats 2000000; maxRecDepth stays finite at 200000. This is a fail-closed internal cap, not evidence that the file fits it. The external planned run budget is separately recorded. No successful performance comparison is asserted.

## Provenance and source review

The user's isolated review reports Lean 4.33.0 / Mathlib prefix db584cd6, a compiling fromRel edit, and Local's high-resource success. Its full revision, edited source and logs were not supplied. This version was newly written from the frozen remote originals, whose SHA-256 values were recomputed and matched. It is not the user's exact draft. The current runtime probe found no lean, lake or elan, so neither new module has been compiled here.

The official generated Mathlib documentation was read on 2026-09-07:
https://leanprover-community.github.io/mathlib4_docs/Mathlib/Combinatorics/SimpleGraph/Basic.html#SimpleGraph.fromRel
The displayed fromRel equation and fromRel_adj agree with the intended adjacency. This moving documentation is an API/source lead, not the user's immutable Mathlib pin and not a compilation receipt. No other repository was operated on.

## Reproduction and review

The two files retain the original namespaces; compile the replacement version separately, not by importing both original and replacement declarations into one module. Local uses only the original Lean imports. For the semantic file, use a Mathlib project fixed to the full intended revision; no guessed lake-manifest or new dependency lock is supplied. Run the exact planned commands and limits in repair-status.json, retaining sanitized output, versions, source/output hashes and an axiom audit. Compilation and statement-faithfulness are separate gates.

source-diff.patch exposes the complete changes relative to the frozen C08 originals. The new source has no placeholder proof, custom axiom or unsafe evaluation token in the static scan; this lexical observation is not a kernel axiom audit. The global proof obligations and root remain open.

## Transport recovery retained

PR20 already delivered the two previously missing C08 detailed outputs, bounded C06/C08 replay observations, the external review intake and a missing-originals inventory. That inventory is not cleared by this repair. Earlier unarchived local audit sources, historical logs and the proposed R07 135-row certificate remain unavailable. No new mathematical derivation is used to disguise those transport gaps.
