# Mixed triangle/Petersen cells: an exact forest test and counterexample compression

Verdict: `candidate_only`. Primary owner: `math-proof`.
Problem: `problem:opg-46613-cubic-p3-partition`.
Attempt: `attempt:web-20260906-opg46613-a01`.
Admitted target: `obligation:opg46613-divisible-two-factor`.
This is consequence/repair analysis of that route. The root remains open. The unchanged divisible-two-factor assertion is not being retried.

## 1. Objects and local certificates

Let Q be a finite simple cubic graph. Partition its vertices into U, T and P. Retain U as single vertices, replace each vertex of T by a triangle, and replace each vertex of P by the Petersen graph with one vertex removed. At either replacement, attach the three incident frame edges bijectively to the three distinct terminals. Denote the expanded graph by X. Its order is |U|+3|T|+9|P|, so its order is divisible by three exactly when |U| is.

A P3 is a selected two-edge path on three distinct vertices; it need not be induced. At a cell terminal use state 0 for an unused external edge, A for an internal singleton which receives an edge from an outside center, and B for an internal edge centered at the terminal which receives an outside endpoint. Restricting a P3-factor to a cell produces precisely internal P3s, A singletons and B pairs: a cell terminal has only one external edge, hence cannot be a center with two external neighbors. If a,b count the A,B ports and the cell has order divisible by three, then a+2b is divisible by three.

For a triangle the exact signatures are 000, AAA, and the six permutations of 0AB. The 000 signature uses the triangle as a selected P3; AAA uses its three singleton vertices; with A at i and B at j the B pair is (j,k), where k is the remaining terminal. BBB would require three disjoint internal pairs and is impossible on three vertices.

For the nine-vertex Petersen cell, label the vertices 0,...,8 and use internal edges

```
01 05 12 16 23 27 38 46 47 57 58 68
```

with terminals 0,3,4. Its signatures are the preceding eight plus BBB. Complete certificates are:

- 000: P3s (0,1,2), (4,7,5), (3,8,6).
- AAA: singleton terminals 0,3,4; P3s (1,2,7), (5,8,6).
- BBB: pairs (0,5), (3,8), (4,7), centered at the first entry; P3 (2,1,6).
- A at 0, B at 3, 0 at 4: singleton 0, pair (3,8); P3s (1,6,4), (2,7,5).

Every row partitions the nine vertices and every required edge is displayed. For the other five 0AB placements use the following explicit symmetry. Adjoin the removed vertex and identify the ten Petersen vertices with the two-subsets

```
a0 a1 a2 a3 a4 b0 b1 b2 b3 b4
12 34 15 24 35 45 25 23 13 14
```

where 0,...,8 are a1,...,a4,b0,...,b4. Adjacency is disjointness. Permuting 3,4,5 while fixing 1,2 induces all terminal permutations and preserves adjacency. The congruence and a+b<=3 leave only (a,b)=(0,0),(1,1),(3,0),(0,3), so this list is exhaustive.

These certificates reuse the exact P9 interface of C04. The new restriction is that triangle cells do not admit BBB.

## 2. Exact mixed-cell forest theorem

X has a P3-factor if and only if Q has a spanning forest F with these three properties:

(F1) Each tree of F contains a number of vertices of U divisible by three.

(F2) Every vertex in U has F-degree at most two.

(F3) If a vertex t in T has F-degree three, the three branches of its tree after deleting t do not all contain 1 modulo 3 vertices of U.

Isolated vertices outside U are allowed. A component is not required to contain exactly three vertices of U. Branch counts in (F3) refer to the entire branches in F, not only their immediate neighbors.

### Necessity: flow and cycle elimination

Orient selected P3 edges from center to endpoint. Give a frame edge value +1 in that direction, -1 in the reverse direction and 0 when unused, over the field F3. The divergence is -1 at each vertex of U and zero at each cell. Support degree at U is at most two. A P cell allows support patterns of degree zero, degree two with one edge entering and one leaving, and degree three with all edges entering or all leaving. A T cell allows the same patterns except three leaving edges.

Eliminate a cycle in the nonzero support by adding a nonzero multiple of its unit circulation chosen to cancel an edge. Divergence is unchanged and no new support edge is introduced. At least one edge disappears. It remains to check the triangle restriction, which cannot be omitted from this argument. A triangle cell of support degree at most two cannot acquire support degree three. If a triangle cell on the cycle initially has support degree three, all its incident values, read outward, are -1. The circulation changes its two cycle incidences by +lambda and -lambda. Since lambda is 1 or -1 in F3, one of these two incidences becomes zero and the other becomes +1. Its new support degree is two. Thus no forbidden three-outgoing pattern is created.

After at most |E(Q)| cancellations the support is a spanning forest, after adding isolated vertices. Summing divergences over a tree proves (F1), and (F2) is preserved. If t has three branches W_i, the value on the edge from t into W_i is |U intersect W_i| modulo 3: sum the divergences inside W_i and cancel its internal edges. Three branch counts equal to 1 would force three outgoing edges at t, which is forbidden. Hence (F3).

### Sufficiency: subtree counts and actual P3 gluing

Root each tree of F. Assign the edge from a child w to its parent the value -|U intersect W| modulo 3, where W is its rooted subtree; reverse the sign on the reverse incidence. Set every edge outside F to zero. Subtree sums give divergence -1 on U and zero elsewhere. The root equation follows from (F1). Zero-valued tree edges may be discarded.

At a vertex in U, divergence -1 and support degree at most two allow exactly one entering edge or two leaving edges. At a cell the zero-divergence patterns are exactly those listed above. The only possible forbidden triangle pattern is three outgoing edges. Its three branch counts would all equal 1, excluded by (F3). Thus every cell has a local certificate.

Realize these certificates and join the chosen external edges. A B pair is completed by the endpoint on the other side; an A singleton receives the edge from the outside center. Each retained vertex is either an endpoint with one entering edge or a center with two leaving edges. All selected edges join a degree-two center to a degree-one endpoint. A connected component cannot have two centers, since an endpoint has degree one. Consequently each component is exactly P3, and the local partitions ensure that every vertex is covered. This proves the equivalence.

## 3. An exact falsifier for forgetting the triangle restriction

Take Q=K4 with vertices z,u1,u2,u3. Put U={u1,u2,u3}, T={z}, P empty. The star F with center z satisfies (F1) and (F2), but all three branch counts are 1. Its unique divergence solution directs all three edges away from z. It cannot be realized in the triangle cell, as BBB is absent.

This is a counterexample to the assertion that every forest certificate for the P9 interface also works for triangle cells. It is not a counterexample to existence of a P3-factor: the expanded graph is the triangular prism. If t1,t2,t3 are the triangle-cell vertices and ui-ti are the external edges, then

```
(u1,u2,t2), (t1,t3,u3)
```

are two disjoint P3s covering all six vertices. The example distinguishes failure of a particular certificate from failure of the graph-level statement, within a finite simple 3-connected cubic example of eligible order.

## 4. Monotonicity under replacing triangle cells by P9 cells

Every triangle signature has a P9 realization with the same ordered port states. Therefore replacing any collection of triangle cells by P9 cells preserves existence of a P3-factor, without imposing a cycle or forest on the given factor. Restrict the factor to each chosen triangle, retain its boundary signature, substitute the corresponding P9 certificate, and leave the rest unchanged. The certificates cover the new vertices and complete the same crossing paths.

Equivalently, in the forest theorem the replacement simply removes some conditions (F3). This is monotonicity, not an assertion that the two graph-level existence predicates are different on some 3-connected eligible frame. The K4 example proves strictness at the certificate level only.

In particular, for a fixed frame and retained set, a counterexample using P9 cells would imply a counterexample using triangles in their place. The latter has six fewer vertices per changed cell. This implication concerns P3-factors, not the existence of divisible-cycle 2-factors.

## 5. A smallest root counterexample cannot contain an induced P9 cell

The following elementary connectivity facts supply the domain audit.

First, a simple cubic 3-vertex-connected graph is 3-edge-connected. A cut of at most two edges cannot have a side of one or two vertices, since those sides have boundaries at least three or four. Deleting the at most two cut endpoints on a larger side would disconnect surviving vertices on both sides, contradicting 3-vertex-connectivity.

Second, a loopless cubic multigraph with at least four vertices and edge connectivity at least three has no parallel edges: a pair of vertices joined by at least two edges has boundary at most two. Once simple, it is 3-vertex-connected. A cut vertex would leave two components with total boundary at least six but only three incident edges. For a two-vertex cut {u,v}, adjacency of u,v would leave only four boundary edges, also impossible. If u,v are nonadjacent, there are exactly two components, each with three boundary edges and adjacent to both u and v (there is no cut vertex). One component C has two edges to one of u,v, say u. The boundary of C union {u} then has size 3+3-2*2=2, a contradiction.

Third, replacing one vertex of a 3-edge-connected cubic graph by a triangle preserves 3-edge-connectivity. A cut not splitting the triangle contracts to a cut of the original graph. A cut of at most two edges splitting it would use exactly its two crossing triangle edges and no other crossing edge. The outside graph is connected because deleting the original vertex leaves a connected graph. It must lie wholly on one side, while every triangle vertex has an attachment to it. Thus a split triangle necessarily contributes an attachment edge as well, a contradiction. The replacement is simple and cubic, so the second fact gives 3-vertex-connectivity.

Now let G be an eligible root-domain graph containing an induced P9 cell R with exactly the three designated external edges. Its order is at least twelve, since it is divisible by six and contains nine vertices. Contract R to one vertex z and delete the resulting internal loops. The resulting graph Q is loopless and cubic, has |V(G)|-8>=4 vertices, and has edge connectivity at least three: every cut of Q is the image of a cut of G with the same boundary. The second fact makes Q simple and 3-vertex-connected. Replace z by a triangle to get G'. The third fact shows that G' lies in the root domain; it has |V(G)|-6 vertices.

Every P3-factor of G' lifts to G by Section 4. Consequently, if G has no P3-factor, G' has none either. A smallest-order root counterexample therefore cannot contain such an induced P9 cell. This is a conditional exclusion of a minimal-counterexample configuration, not a claim that a root counterexample exists or that the root has been decided.

## 6. Scope and verification requests

All new implications above have finite local certificates and explicit combinatorial proofs. They remain proof candidates; no verifier receipt, EvidenceLink or Result is generated here. The three-port labeling and the non-induced meaning of P3 are essential. The algebraic cycle-cancellation step explicitly preserves the triangle restriction.

Dependencies and provenance: C04 `p3-interface.md` for the fixed P9 labeling and local certificates; C01/C02 for the distinct already-obstructed divisible-two-factor route. No novelty claim is made. The mixed-cell criterion does not solve general forest existence: when every vertex is retained it contains the root problem itself.

Next obligation: audit the triangle restriction, the three connectivity facts and the P9-to-triangle compression against the fixed root statement, then seek additional replaceable three-port configurations or a constructive forest existence theorem for the remaining frames. Do not discard (F3), treat the prism certificate failure as a root counterexample, or restart the unchanged divisible-two-factor assertion.
