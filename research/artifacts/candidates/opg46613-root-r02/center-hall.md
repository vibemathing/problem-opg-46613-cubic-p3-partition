# ROOT-R02: center-capacity certificates for P3 factors and cut signatures

Verdict: `candidate_only`. Primary owner: `math-proof`.
Problem: `problem:opg-46613-cubic-p3-partition`.
Target: `obligation:opg46613-root`.
Attempt and legacy graph/route bindings are unchanged. This is a partial root
candidate. It does not use or revive the divisible-two-factor strengthening.

## 1. Frozen semantics

Graphs are finite and simple. A P3 is a selected two-edge path on three distinct
vertices; its endpoints may be adjacent in the ambient graph. A P3-factor is a
spanning union of such paths. Its center set has size n/3. For disjoint sets
S,D, write N_D(S) for the vertices in D adjacent to at least one vertex in S.
An eventual root proof must find a suitable center set; the present criteria do
not assert that every admissible cubic graph has one.

## 2. Exact center theorem (claim root-r02-center-hall)

Let n=3k and let C be a specified k-element subset of V(G). Put D=V(G)\C.
There is a P3-factor with center set exactly C if and only if

    |N_D(S)| >= 2|S|       for every S subset C.                    (H)

In particular, a factor exists if and only if at least one k-element C satisfies
(H). This is an equivalence to the root's selected-path semantics, not a stronger
perfect-matching/2-factor assertion.

Necessity: the two endpoints assigned to each center in S are distinct vertices
of N_D(S), and endpoints assigned to different centers are disjoint.

Sufficiency, including the matching fact used: replace each c in C by two clones,
each adjacent to N_D({c}). Every set X of clones has a support S in C, and
|X| <= 2|S| <= |N_D(S)| = |N(X)|. Take a maximum matching in this finite bipartite
graph. If a clone is unmatched, start alternating paths at all unmatched clones.
If any reachable right vertex is unmatched, toggling such a path enlarges the
matching, impossible. Otherwise write L0,R0 for reachable left and right sets.
All neighbors of L0 are in R0, every right vertex in R0 is matched back into L0,
and each matched vertex of L0 has its mate in R0. Since L0 also contains an
unmatched left vertex, |L0|>|R0|=|N(L0)|, contradiction. Thus every clone is
matched. There are 2k clones and 2k vertices in D, so every vertex in D is used.
Forget the clone labels; the two matching edges of each original center form
one P3. This covers V(G), proving sufficiency.

This is the capacity-two specialization of Hall's theorem; the preceding proof
is included so that no uninspected external theorem is a hidden dependency.

## 3. Exact boundary feasibility via residual capacities

Use ROOT-R01 port states U (unused), A (endpoint supplied by an external center),
and B (center supplied with an external endpoint). A port is an incidence, so
several ports may attach to the same vertex. For a fixed signature let a_v,b_v
count A and B incidences at v, and a,b be their totals.

A local realization exists if and only if there is C subset V(B), the local
center set, satisfying all the following finite conditions:

1. At a center v in C, a_v=0 and 0<=b_v<=2. At an endpoint v outside C,
   b_v=0 and a_v is either 0 or 1. Mixed A/B roles and repeated A at a vertex
   are excluded. U imposes no vertex-role restriction.
2. Set D0={v outside C : a_v=0}, and k_v=2-b_v for v in C. Then

       sum_{v in C} k_v = |D0|,
       |N_{D0}(S)| >= sum_{v in S} k_v   for every S subset C.       (BH)

Only INTERNAL adjacency is used in N_{D0}. Vertices outside C with a_v=1 are
already externally supplied and must not be counted as available endpoints.

Proof: necessity counts the internally assigned endpoints. For sufficiency,
replace each center by k_v clones, apply the alternating-path argument in
Section 2, and add the prescribed selected port incidences. Internal selected
edges always join a center and an endpoint. The complete selected degrees are
two at centers and one at endpoints, exactly the ROOT-R01 local realization.
A center with two B ports has k_v=0, so the repeated-port singleton-center case
is included rather than lost. Capacity-zero centers cause no problem: a partial
clone set has support only on positive-capacity centers, to which (BH) applies.

The balance identity is equivalently

       3|C| = |V(B)| - a + b.                                     (B)

Thus the residue table narrows the possible size of C; it does not replace (BH).
Given a finite fragment, (B), forced roles, and the capacity Hall tests enumerate
its ACTUAL signature set. Together with ROOT-R01's dual-port rule this supplies
an exact cut-interface algorithm, also for vertex 3-sums. It does not assume
all residue-allowed words are realizable.

For exact counts, form the square 0/1 bipartite adjacency matrix M_C whose rows
are the k_v clones and columns are D0, for each role-compatible C satisfying
balance. If per denotes the permanent, then

    w_B(signature) = sum_C per(M_C) / product_{v in C} k_v! .       (P)

Each local selected-edge realization has exactly product k_v! lifts to a clone
matching, obtained by permuting clones at each center. Its center roles are
unique, so the sum over C has no other overcount. The empty matrix permanent
and 0! both equal one. Consequently (P), composed with ROOT-R01's compatibility
matrix, is an exact integer counting formula, not just a decision encoding.

## 4. What cubicity implies, and the smallest Hall-defect frontiers

For a cubic graph, (H) implies max degree(G[C])<=1 by taking S={c}, and it implies
that C dominates D by taking S=C and using |D|=2|C|. Neither implication can be
reversed: Section 5 supplies an explicit counterexample even with cyclic edge
connectivity four.

For a candidate C and S subset C define

    col_D(S) = sum_{d in N_D(S)} (|N(d) intersect S|-1).

A direct edge count gives the exact defect identity

    2|S|-|N_D(S)|
      = 2|E(G[S])| + |E(S,C\S)| + col_D(S) - |S|.                 (D)

Indeed, the number of edges from S to D is
3|S|-2|E(G[S])|-|E(S,C\S)|, while subtracting col_D(S) counts each
neighbor once. Identity (D) separates lost center-to-center incidences from
endpoint collisions. Connectivity alone does not eliminate either term.

Assume every c in C has at least two neighbors in D. Let S be inclusion-minimal
with defect d=2|S|-|N_D(S)|>0. Then:

- |S|>=2 and d is either 1 or 2.
- If p_c is the number of neighbors in D that have c as their unique neighbor
  within S, then d+p_c<=2 for every c in S.
- In the bipartite graph with vertex classes S and N_D(S), all vertices lie in
  a single connected component.

For the second assertion, minimality applied to S\{c} gives
2|S|-d-p_c=|N_D(S\{c})|>=2(|S|-1). This also proves d<=2. The singleton
case is excluded by the degree assumption. If the incidence graph were
disconnected, the defect would be a sum of component defects, one positive;
its proper center support would contradict minimality.

A sharper conditional frontier: suppose C has no internal edges. If |S|=2 is a
Hall obstruction, both centers have three neighbors in D and their union has
at most three vertices. Hence their neighborhoods coincide and the incidence
subgraph is K2,3. In a simple cubic 3-connected G of order divisible by three,
these three common neighbors have no internal edge between them: such an edge
would leave at most one edge out of the five-vertex set, contradicting
3-edge-connectivity. Consequently the five-vertex K2,3 is a cyclic side of a
matching three-edge cut. The other side is not a singleton unless n=6; at n=6
its singleton has no neighbor in C, contradicting domination. For a connected cubic cut side on t>=3 vertices with three boundary edges,
its internal edge count (3t-3)/2 is at least t, so it contains a cycle. Thus in
a cyclically 4-edge-connected graph with C dominating, this obstruction is excluded.

If C has no internal edges and G has no 4-cycle, Hall obstructions cannot have
|S|=2 or 3. For three centers the pairwise overlaps of their three-element
neighborhoods are at most one; inclusion-exclusion yields |N_D(S)|>=9-3=6.
This is only a bound on a bad specified center set, not a lower bound on the
order of a root counterexample and not a claim that independent centers always
exist. A P3-factor is allowed to have adjacent centers in the ambient graph.

## 5. Explicit failure of the domination shortcut in the root domain

Let G be the 12-vertex Mobius ladder, vertices 0,...,11, with cycle edges
(i,i+1 mod 12), and chords (i,i+6), 0<=i<6. Choose

       C={0,1,4,8},             D={2,3,5,6,7,9,10,11}.

The only edge of G[C] is 01. The four external neighborhoods are

| Center | Neighbors in D |
|---|---|
| 0 | 6,11 |
| 1 | 2,7 |
| 4 | 3,5,10 |
| 8 | 2,7,9 |

Their union is D, so C dominates every noncenter. But S={1,8} has only
N_D(S)={2,7,9}, while it needs four distinct endpoints. There is no factor
whose centers are this C. A different C works: four explicit paths are

       (1,0,6), (2,3,4), (5,11,10), (7,8,9).

Thus G is NOT a root counterexample. It only invalidates the auxiliary claim
that domination, the correct cardinality, and max degree(G[C])<=1 suffice.

Here is a hand-checkable connectivity certificate. Every nonempty proper set
has a positive even number of crossing cycle edges. A cut of size at most three
would have exactly two such edges, so its side is a contiguous interval of the
12-cycle. An interval of length l has min(l,12-l) crossing chords. Its cut size
is therefore 2+min(l,12-l), which is three only for a singleton or its complement;
no cut of size one or two occurs. The graph is cubic and has no vertex cut of
size one or two: a cut vertex would give some component with at most one edge
to it. For a two-vertex cut {u,v}, every component must have at least three edges
to {u,v}. Thus u,v cannot be adjacent, and there are exactly two components,
each with three attachment edges. Both deleted vertices meet both components
(no cut vertex); one component has two attachments at u and one at v. Adding
u to that component leaves a two-edge cut, contradiction.

Every three-edge cut is trivial, so no such cut separates two cycles. The set
{0,1,6,7} induces a 4-cycle and has four edges to its complement; the complement
contains the cycle (2,3,4,5,11,10,9,8,2). Thus cyclic edge connectivity is exactly
four. Requiring cyclic 4-connectivity does not repair the domination shortcut.

## 6. Source relation, falsifiers, and continuation

Hall, On Representatives of Subsets (1935), is prior art for Section 2; the
capacity and port formulations are explicit specializations. Kelmans,
arXiv:0910.2766v2, supplies global conjecture equivalences and vertex-3-sum prior
art, not a theorem that these particular Hall inequalities always have a solution.
The companion source note gives exact locators and limitations.

The fixed graph, center set, deficient subset and positive paths in Section 5
can be checked directly; no census claim or unavailable code is needed. A fresh
local generator check found 24 bad eligible center sets in this single labeled
M12, but that count is not needed for any proof here. The earlier Issue's counts
2896/2280/616 over 57 graphs and partial order-18 generation have NOT been
reproduced in this transaction, and are not promoted to current results.

A finite negative certificate for a specified n=3k graph can also use (H): for
EVERY k-element C, supply a subset S of C and its exact external neighborhood
with |N_D(S)|<2|S|. A checker must verify complete coverage of all k-element C,
not just tested center sets, plus the graph's domain assumptions. A single
failed C is not such a certificate. This avoids relying on a solver's bare UNSAT
status; no graph-level negative certificate is asserted here.

Next root obligations: select a center set satisfying ALL Hall inequalities;
use minimal Hall-defect supports to design valid exchanges; compute missing
boundary signatures with (BH); independently replay source-faithful direct
P3-cover censuses. No claim that a minimal root counterexample is triangle-free
or cyclically 4-connected follows from this document. The protected legacy
obligation dependency also still requires coordinator repair before admission.
