# NONTERMINAL_CHECKPOINT: positive global minima and physical exchange

Verdict: candidate_only. Primary owner: math-proof.
Problem: problem:opg-46613-cubic-p3-partition.
Source main: 29e101f446712c4d786251dd2e7943de80bb6fa8.
Attempt: attempt:web-20260906-opg46613-a01.
Legacy transport route: route:two-factor-divisible-cycles-v1 (not a premise).
Target: obligation:opg46613-root. Both canonical obligations remain open.

## Candidate mathematical progress

Retain the PR28 physical A/B and left/right gap equations with internal M
chords. For selected S, let L_S have S as owner vertices and one edge-slot per
unit of gap demand, including loops and parallel units. Every connected
component with v vertices and e edges has maximum slot-owner matching size
min(v,e): orient a tree away from a root, or orient a spanning unicycle and its
attached trees to saturate every owner. Hence

    kappa(S)=sum_C |v_C-e_C|+3u=t+b+3u,

where t counts tree components and b sums positive excess e-v. This rank idea
is prior candidate material, not claimed novel. Minimal deficient Hall slot
sets are connected bicycles: e=v+1, minimum degree two, and after suppressing
degree-two paths the possibilities are theta, tight or loose handcuffs.
Pure tree surplus must also be tracked; it need not have a deficient demand set.

A new activation lemma has a complete case proof: if C is an untouched
nonzero-residue F-cycle, EVERY M edge e incident with C satisfies
kappa(S union {e})<kappa(S). If both ends are in untouched cycles, compare the
one new owner's loop demand directly against the disappearing 3u penalty.
If the other end splits a touched gap, replace r parallel a-b units by p a-z
and q z-b units, where r=(p+q+1) mod3, plus ell=0 or 1 loops at z. The maximum
increase in sum |v-e| is at most two, including a=b and all split cases, while
u decreases by one. The split bounds (ell=0,ell=1) are:
00/r1: (2,1); 01/r2: (2,1); 02 or11/r0: (1,2);
12/r1: (1,2); 22/r2: (1,2), with reversed pairs included.
Thus every GLOBAL minimizer has u=0. This does not revive general strict
single-toggle descent after all bad cycles have already been touched.

When u=0 and total order is divisible by three, D-s=b-t is divisible by three.
Therefore positive kappa cannot equal one. For three residue-222 F-cycles,
two cross edges forming a quotient tree give either kappa=0 or kappa=3.
A hypothetical positive GLOBAL minimum must consequently be 2 or 3:
- Value 2 has one tree component, one bicyclic component and otherwise
  unicyclic components.
- If the global minimum is 3, the two-edge quotient tree can be chosen as a
  minimum-cardinality minimizer. Its unit graph has two owners, a loop at each,
  and three parallel middle-gap units. This is an available representative,
  not a claim about every possible cardinality-minimal representative.
Neither remaining positive value has been excluded.

For a simultaneous exchange S'=(S minus R) union A, retain only matching pairs
with unchanged full physical gap keys and surviving owners. If l old matching
pairs are lost and a new alternating augmentations are made, then

    kappa(S') <= kappa(S)+Delta s+Delta D+3Delta u+2l-2a.

Equality holds if the new slot matching is maximum. Strict improvement follows
from 2(a-l)>Delta s+Delta D+3Delta u. This endpoint accounting imposes no
monotonicity on intermediate single-edge steps. G24's known neutral route and
G42's known four-edge factor supply two positive controls, not root failures.
Conditional surgeries transfer one cycle from a bicycle to a tree, reduce
excess three to one tree and one bicycle, or merge three surplus trees. Their
physical split hypotheses are explicit; universal availability remains open.

## Bounded verification package and transport boundary

The new local package has separate producer and consumer cores: component
orientation/alternating matching versus successor-walk reconstruction, matrix
max flow, and owner-mask assignment DP. It includes deterministic new positive
hosts, explicit surgery traces, minimal Hall certificates, conditional surgery
cases and semantic mutations. Old 4096/1562/5985 censuses are not repeated.
Actual execution metadata and all fixed file identities are in the local
execution/manifest/receipt files. They are not trusted verifier attestations.

Prepared physical files in this namespace: surgery.py, search_hosts.py,
audit.py, local_switches.py, check.py, run_bounded.py, report.md,
source-note.md, verifier-request.json, restore.py, manifest.json,
and the exact bounded replay-data segments. Blob/tree writes were attempted.
Their attachment, byte identities and a single legal attempt packet must be
freshly reconciled before claiming a final commit/PR/check/merge transaction.
Do not infer completed delivery from an unattached Git tree or blob. No
successful new PR or merge is claimed by this checkpoint.

The separate historical branch web/attempt-opg46613-root-tf-exchange-r02 at
351b3183f251e0849bdee471e4bd180dbf52fb60 adds only its orphan packet, whose PR27
binding is wrong and whose listed candidate source/output files are missing.
It is preserved, not used as execution evidence, and is not a valid replacement
for the new namespace's packet. Do not recreate its missing historical outputs.

## First open lemma and next action

X2: from a hypothetical global-minimum tree+bicycle allocation, prove existence
of a physical multi-edge exchange satisfying the strict gain inequality.
X3: do the same from the standard five-unit/two-owner value-three allocation.
The abstract Hall core is insufficient without controlling which unselected
matching edges connect actual cyclic positions and how all affected gaps change.

For arbitrary cycle count, rank, activation and simultaneous accounting already
apply; the 222 upper bound three does not automatically extend. A residue-group
or ear-exchange invariant controlling both surplus trees and excess components
is still required. Trusted replay, statement-faithfulness, formalization and
closure remain pending. No root result, no signed Evidence and no Solution
admission is asserted. Research state remains nonterminal.
