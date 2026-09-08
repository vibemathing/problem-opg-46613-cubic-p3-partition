# ROOT-TF-222-R01: complete three-edge types, a cost-four obstruction, and exchange limits

Status: NONTERMINAL_CHECKPOINT. Verdict: candidate_only.
Primary owner: math-proof. Generator trust domain: web-candidate-generation.
Repository: vibemathing/problem-opg-46613-cubic-p3-partition.
Base: ed428d8a771ae581bf5175f24e8f8276e6232244.
This package is neither a root counterexample nor a trusted verification receipt.

## 1. Frozen target and dependencies

R_tf asks whether every finite simple triangle-free 3-vertex-connected cubic
graph of positive order divisible by 6 has a spanning P3-factor. A P3 is a
selected two-edge path on three distinct vertices; inducedness is not required
by the contract (and follows automatically here). The complete root is related
to R_tf by the existing simulator candidate, not proved by that reduction.

Document-local DAG, not newly admitted record IDs:
B = existing root <=> R_tf bridge, already candidate-audited, not admitted;
N = supplied perfect matching M and F=G-M normal form;
L = the exact role/gap equations and lifting below;
K = fixed-S gap-forest criterion, reused from ROOT-TF-CORE-R01;
X = for every eligible G and a supplied M, some S subset M satisfies L/K;
R_tf follows from matching existence + X + L; R follows using B.
X is still OPEN. A supplied M avoids using an unrecorded matching-existence
proof inside this package. Classical matching existence is a separate dependency.

The old n<=18/cost-two package is preserved through PR27. No old source was
recreated, no 18/45-vertex object audit was repeated, and no divisible-cycle
2-factor strengthening is assumed.

## 2. Complete local equations, for three or any number of cycles

Fix S subset M. Its endpoints are active. On each F cycle list active vertices
v_0,...,v_(h-1) in cyclic order. For h=1 the one gap returns to that same vertex.
Let d_i be the number of F edges in the gap v_i to v_(i+1), and r_i=(d_i-1) mod 3.
Use binary physical-incidence variables x_(i,-), x_(i,+). Require

    b_i = x_(i,-) + x_(i,+) in {0,1},
    x_(i,+) + x_(i+1,-) = r_i,
    b_u + b_v = 1 for every selected matching edge uv in S.

Here b=0 is an A singleton, b=1 a B-centered pair; minus/plus specifies which
F neighbor the B center uses. The matching equation is also required for
INTERNAL matching chords whose endpoints lie on the same cycle. Neither those
chords nor their two physical incidences may be erased. A gap with no internal
vertex has r=0; a gap with exactly one internal vertex has r=1, so its vertex
cannot be consumed twice. A gap with r=2 has at least two internal vertices.
A cycle with no active vertex must have length divisible by three.

These equations are necessary and sufficient, not just congruences. Necessity:
each P3 contains at most one M edge, since M is a matching. Restrict a factor to
F. An M-using P3 leaves one A singleton and one B pair; other P3s are consecutive
cycle triples. Exactly the indicated first/last gap vertices are consumed, so
the remaining gap order is a nonnegative multiple of three. This gives L.

Sufficiency: choose every indicated B pair, join it along its selected M edge
to the corresponding A singleton, and tile the remaining interior of each gap
by successive triples. Untouched divisible cycles are tiled in any of their
three phases. One unit per M edge means exactly one B end and one A end; it also
prevents any active vertex from extending to both sides. The gap equations
prevent overlap at internal vertices. Thus all vertices occur once and every
chosen component is actually a P3. Restricting this factor recovers the original
roles and incidences. This is a two-way correspondence on the UNCHANGED graph,
not a contraction that silently loses cubicity, triangle-freeness or modulus.

In particular, if h active vertices on a cycle have b B roles, then

    h+b == L (mod 3).

This necessary scalar equality does not replace the physical-incidence equations.

## 3. Exact constrained quotient and fixed-S augmentation

Retain the F cycles as quotient vertices, cyclic orders as annotations, cross M
edges as ordinary edges, and internal M chords as loops with two labeled ends.
For a chosen S, the derived gap multigraph has V(K_S)=S: a demand-one gap is an
edge between its two owners (loops and parallel edges retained); demand-two gaps
force one unit at each owner. Then K is exactly the previously supplied theorem:
no owner has two forced marks, each component is a singly marked tree or an
unmarked unicycle, and every untouched F cycle is divisible. Its elementary
rooted-tree/cycle orientation construction gives the allocation in Section 2.
The old exact count 2^u*3^z is reused, not claimed as a new result.

A different implementation in allocation.py instead makes one demand slot for
each required unit. Each selected M edge has capacity one, and a gap's slots
can use only its two incident owners. A demand-two gap needs two distinct
owners; if its two ends have the same owner it cannot be fulfilled. For
feasibility, two identical demand-slot neighborhoods are harmless; factor
COUNTING instead retains physical incidences and avoids artificial slot-label
multiplicities. The implementation counts by physical assignments, not by an
unadjusted permanent of the cloned graph.

Let s=|S|, D=sum r_i, nu be its maximum slot matching size, and u the number of
untouched cycles with nonzero residue. Define

    kappa(S)=s+D-2*nu+3*u.

Every term is nonnegative after grouping (s-nu)+(D-nu)+3u. Hence kappa=0 iff
the exact system is feasible. For a current slot matching A, the working
potential is s+D-2*|A|+3*u, which is not yet the optimized value kappa(S).
With S fixed, an alternating augmenting path increases |A| by one and strictly
reduces the working potential by two. At most min(s,D) augmentations occur.
At termination A is maximum, so the working potential equals kappa(S).
A BFS from unmatched slots then gives a Hall-deficient set if demand is not
saturated; unmatched supply or an untouched bad cycle are separate failures.
This is a finite fixed-S algorithm, not a proof that its terminal kappa is zero.

Changing S changes the gaps, their demands, and their owner graph. The fixed-S
monovariant therefore gives no general S-exchange descent. Section 7 supplies
a concrete no-strict-single-toggle state, despite an available positive factor.

## 4. Complete selected-three-edge classification for spectrum 222

Assume F has exactly three cycles, each length 2 modulo 3, and a factor uses
exactly three matching edges. Let h_i,b_i be active and B counts on each cycle.
All cycles are touched, sum h_i=6 and sum b_i=3. For h=1,2,3 the residue rule
forces b=1,0,2 respectively. For h=4, b is 1 or 4, and the global B budget rules
out 4 in the (1,1,4) distribution. The only positive partitions of six into
three parts are (1,1,4), (1,2,3), (2,2,2). The last forces sum b_i=0 and fails.
Thus, up to permuting cycles, the ONLY possibilities are

|Active counts h|B counts b|Local role types|
|---|---|---|
|(1,1,4)|(1,1,1)|B; B; three A and one B|
|(1,2,3)|(1,0,2)|B; AA; one A and two B|

Every connected component of the selected quotient must have total original
cycle order divisible by three: no selected factor edge leaves its vertex set.
For 222, a proper one- or two-cycle component has nonzero residue. Consequently
the selected quotient is connected. Three edges on three vertices form a
unicycle, including multigraph possibilities. The complete list is:

1. a quotient tree plus an INTERNAL chord/loop at its middle: (1,1,4);
2. a quotient tree plus an internal chord/loop at a leaf: (1,2,3);
3. a doubled cross edge plus a third edge attaching the remaining vertex: (1,2,3);
4. a simple quotient triangle: (2,2,2), impossible.

The first three shapes are sufficient ONLY when the exact local equations and
A/B matching pairing also hold. This yields a complete finite test for exactly
three selected edges, with no presumed loop erasure. A plain quotient cycle or
parity/T-join selection is not a substitute for these mod-three role conditions.
For four or more edges the unrestricted system in Sections 2-3 remains exact;
there is no imposed bound on h or the number of cycles in that theorem.

## 5. New 42-vertex positive host: minimum specified-M usage is four

objects.json contains the full sorted edge table and specified M. Equivalently,
F consists of consecutive cycles 0..13, 14..27, 28..41. In each offset a=0,14,28
add internal matching chords

    (a+2,a+9), (a+4,a+8), (a+5,a+12), (a+7,a+11), (a+10,a+13).

Let b be the next offset cyclically; add (a,b+3) and (a+1,b+6).
There are 42 vertices, 63 distinct loopless edges and 21 matching edges. Every
vertex has two F edges and one M edge. A triangle could contain at most one M
edge, so would require an internal chord at cyclic distance two; none exists.
Cross edges join different F cycles and cannot close such a triangle.

### Three-vertex-connectivity certificate

Deleting at most one vertex in each of two different F cycles leaves each of
the three cycle paths connected. Each adjacent quotient pair has two disjoint
joining edges. Two deleted vertices can destroy at most two joining edges;
at worst one quotient link disappears, leaving a connected three-vertex path.

If both deletions occur in a single F cycle, the other two intact cycles and
their joining edges form a connected outside. The damaged cycle splits into
at most two intervals. A component with a surviving port in {0,1,3,6} attaches
to that outside. Any component with no surviving port must be one of the
32 nonempty intervals wholly inside the port-free runs {2}, {4,5}, {7,...,13}.
For each such interval, allocation-results.json supplies an internal matching
chord from the interval to a vertex outside it and outside its two deleted
boundary vertices. This joins it to the other surviving interval. The second
consumer checks exactly all 32 possible intervals and their escape chords.
Thus all deletion cases are covered. It also directly checks all 904 deletion
sets of size at most two from the full edge list.

### Excluding cost at most three

Cost zero leaves nondivisible cycles. With only one selected cross edge, one
of the three cycles remains separated with nonzero order. At cost two the
quotient must be a tree, with AA at its middle. Each middle cycle would need
one port from U={0,1} and one from V={3,6}; their forward distances (3,6,2,5)
are never 1 modulo three. Since cycle length is 2 modulo three, reversing the
direction preserves whether that distance is 1. The two-A condition fails.

For cost three, Section 4 exhausts the quotient shapes. A simple triangle is
already impossible. A loop at a leaf leaves a middle AA pair with the same
U/V obstruction. In the doubled-edge shape, the two-active cycle must be AA.
Its U pair has distance one and its V pair distance three; only the U pair can
work. The three-active cycle then uses its V pair {3,6} and one U port. Both
choices yield total gap demand FIVE rather than the necessary B count TWO.

It remains a tree plus a loop at the middle. Its two external ports u in U,
v in V are A; one of the two chord ends is B. All 4*5=20 choices of (u,v,chord)
are recorded with positions and gap residues. Seventeen choices have total
demand four, not one. The other three choices are

    (u,v,chord)=(1,3,(4,8)), (1,3,(7,11)), (1,6,(7,11)).

In each, the UNIQUE demand-one gap is bounded by u and v, both forced A.
The internal chord cannot supply that gap. Thus every shape fails. This is an
explicit finite local-role proof of the restricted nonexistence, not root UNSAT.

A different unordered-triple exact-cover search additionally emits a complete
1,069-node failure DAG for cost<=3. certificate_check.py regenerates every
center-neighbor triple through each stored pivot and checks EVERY allowed child,
including its residual budget. Residual order drops by three, so this validates
all branches without trusting the producer's search. Resource limits cause an
error, never an UNSAT leaf. The archived DAG is negative-42.json.

### Positive factor and exact minimum

The following fourteen P3s, with middle entries their centers, cover all vertices:

    (0,17,16) (1,20,21) (15,34,35) (22,18,19)
    (2,3,4) (5,6,7) (8,9,10) (11,12,13)
    (23,24,25) (26,27,14)
    (36,37,38) (39,40,41) (28,29,30) (31,32,33).

Their M edges are (0,17),(1,20),(15,34),(18,22), exactly four. The two direct
implementations agree on 96 cost-four factors. All 1,562 subsets of M of size
at most three fail, and all 5,985 size-four subsets were tested. This graph is
therefore POSITIVE for root. No global no-P3 or all-M failure is claimed.

Minimum-order qualification: 42 is NOT claimed minimum over all eligible graphs.
It is minimum within the stated family of three equal even-length cycles
L=6m+2>=8, the same four ports, fixed cross wiring and arbitrary triangle-free
internal matchings. The only smaller length is L=8; its unused vertices
{2,4,5,7} force chords (2,5),(4,7), giving the previous positive cost-three
24-vertex control. This limited minimum does not exclude other smaller hosts.

## 6. New finite checks, distinct implementations and mutations

allocation.py uses physical gap assignments and augmenting slot matchings.
direct_cover.py instead generates paths from unordered vertex triples and
branches on residual vertices, without importing the allocation code.
certificate_check.py imports neither program; it uses a matrix, partition
merging, center-neighbor rows and a proof-DAG consumer. None imports an older
candidate constructor or verifier. All remain in the SAME generator trust domain.

The control G24 is reconstructed from the already archived bits=000 definition,
not relabeled as a new obstruction. Its entire 4,096-subset vector agrees with
the direct enumeration of all 585 factors; exactly 246 S are feasible. All 24
cost-three factors have active-count type (1,1,4). These are counts for ONE
specified graph, not an isomorphism-reduced order census.

local_states.py compares direct cycle exact cover with the role equations for
ALL positions and ALL A/B words with 1..4 active vertices at lengths 5,8,11,14:
28,068 states in total. Larger active counts use the general theorem, not an
unperformed local census. Seventeen semantic mutations are rejected: malformed
host/matching/cycle, duplicate supply, gap distance/residue/wrap incidence,
center/leaf reversal, repeated extension, invalid P3s, negative-DAG missing child,
wrong budget/pivot, and a cost-four factor mislabeled as cost three.

Five final bounded Python stages exit zero. execution.json records actual
interpreter, start times, wall observations, limits, exit codes and all hashes.
Each has CPU<=25s, wall<=35s, address-space<=512 MiB, output-file<=1 MiB, one
worker/thread. The first search-wrapper run failed because its inner file-size
limit attempted to exceed the parent's hard limit; initial-search-failure.json
preserves the diagnostic and source fingerprint. The limit alone was corrected
and all five stages rerun. This failure was never a mathematical counterexample.

The deterministic discovery stopped after 47 local internal-matchings, of which
45 hosts passed three-connectivity; the first 44 had cost-three factors. This
is a bounded specified-family search, not a complete family or order census.
The selected witness's restricted tests, in contrast, exhaust their stated range.

## 7. Strict single-toggle repair fails on the old POSITIVE G24

With M in sorted order, choose S={M_0,M_3}={(0,11),(3,16)} (mask 9).
All three F cycles are touched. The gap demands are (2,1,1,1), total D=5,
while s=2 and nu=2. All five demand slots have just two owner neighbors:
a full Hall witness. Thus kappa(S)=3.

For toggling matching edge indices 0..11, the recomputed conflicts are

    4,3,3,4,3,3,6,6,3,3,6,3.

None strictly decreases kappa. Nevertheless adding M_2=(2,5) and then
M_4=(4,7) gives masks 9 -> 13 -> 29 with conflicts 3 -> 3 -> 0 and factor

    (0,11,12) (5,2,1) (3,16,17) (4,7,6)
    (13,14,15) (8,9,10) (18,19,20) (21,22,23).

This excludes the precise route 'every positive-conflict S admits a strictly
improving single toggle', not neutral exchanges, multi-edge repair or root.
The feasible set is at Hamming distance two; all 4,096 masks were checked.
No global minimality of this obstruction is claimed.

## 8. Arbitrary cycle count and the first open gap

Sections 2-3 already apply to any number of F cycles and any |S|, including
internal chords. A selected-quotient component must have total cycle order
zero modulo three, and then the physical gap/Hall constraints still have to be
met. Ordinary quotient connectivity, scalar residue, or a parity T-join alone
does not enforce them.

The first OPEN lemma is still X: prove some S always meets the exact allocation
constraints in an eligible host. A possible next atomic question is whether
positive global minima of kappa can be excluded by a multi-edge exchange that
keeps internal chords and all changing gap demands. The single-toggle route is
now excluded; cost<=3 is insufficient even for three 222 cycles. Merely raising
a matching-edge budget or finishing a finite enumeration does not prove X.

For any supplied M, ranging over ALL S includes every P3-factor. Consequently
if a factor is displayed, the graph is positive for every choice of M after
using its actual intersection as S. A restricted no-cost<=3 certificate says
nothing about global nonexistence; testing more M cannot turn this positive
graph into a root counterexample.

Verification/admission gaps: neither the universal exchange/X lemma nor a
trusted receipt for the present partial claims exists here. No Lean elaboration
or axiom report is supplied. A scoped verifier/formalization request asks for
separate finite replay and the general proof/statement-faithfulness audit.
Even admission of these partial lemmas would leave root open. Both canonical
obligations, historical raw-output gaps and pending C08 Lean remain open.
