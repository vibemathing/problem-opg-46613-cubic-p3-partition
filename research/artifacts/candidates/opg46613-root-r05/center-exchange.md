# ROOT-R05: feasible centers can be isolated under single exchanges

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-root`, in the existing admitted Attempt/Route/Graph.
The results below concern the geometry of actual P3-factor center sets, not the
already obstructed divisible-two-factor assertion. No root closure is claimed.

## 1. Exact objects and the exchange hypothesis

For a finite simple graph G of order 3k, let B(G) consist of the k-element
subsets which occur as the centers of a spanning P3-factor. Paths are selected
two-edge subgraphs and need not be induced. A one-center exchange replaces c
in C by v outside C, with all other center memberships unchanged.

ROOT-R04 showed that certain bad proposed center sets cannot be repaired in
one exchange. That does not, by itself, decide basis exchange among the good
sets in B(G). This candidate gives an infinite family of original-domain graphs
with a good set C isolated under every one-center exchange and with other good
sets explicitly present. Thus B(G) need not be the bases of a matroid on V(G).
The failed axiom is stated precisely in Section 5, not inferred from terminology.

## 2. Private endpoints and a general obstruction

Suppose G is cubic and C is a vertex subset with the following properties:
G[C] is a perfect matching, and every vertex of D=V(G)-C has exactly one
neighbor in C. Each center c has two distinct neighbors L_c in D, and these
pairs partition D. Counting their incidences gives |D|=2|C|. Hence C is a
feasible center set with the unique factor whose paths are L_c joined through c.
Uniqueness follows because c has exactly two neighbors outside C and must use
both. No matching theorem is needed for this assertion.

Equivalently, every vertex of G has exactly one neighbor in C. This familiar
condition is efficient open domination; the source note distinguishes it from
the much weaker requirement of being a feasible P3 center set. We do not assume
that every root-domain graph admits such a set.

If, for every c, the two vertices of L_c are nonadjacent and have no common
neighbor in G[D], then no one-center exchange from C can be feasible. Indeed,
let C'=(C-{c}) union {v}. If v is one of the two private endpoints, the other
endpoint is outside C' and has no neighbor in C': its only old center c is
removed, and v is not adjacent to it. If v is not one of them, both endpoints
stay outside C'. They would both need v as their new center-neighbor, contrary
to the absence of a common neighbor in G[D]. Thus every such C' even fails the
necessary domination condition for a P3 center set.

## 3. An explicit family at every order 6m, m>=2

For each integer m>=2, take vertices

    z_0,...,z_(4m-1), c_0,...,c_(2m-1).

The z vertices form the cycle in this cyclic order. Add edges

    c_i z_i and c_i z_(i+2m)       (0<=i<2m),
    c_i c_(i+m)                   (0<=i<m).

Indices on z are interpreted modulo 4m, and indices on c modulo 2m. Call the
result G_m. Its 6m vertices are distinct. Every z has its two cycle neighbors
and one c neighbor; every c has two z neighbors and one c neighbor. The listed
edges have no loops or repetitions, so G_m is simple and cubic.

### 3.1 Full three-vertex-connectivity proof

Delete a set of at most two vertices. With at most one deleted z vertex, the
remaining z cycle or path is connected. Every remaining c has a surviving z
neighbor, so all remaining vertices belong to that connected component.

It remains to delete exactly two z vertices, with no center deleted. If they
are adjacent, the surviving z vertices form a single path, and no c loses both
of its antipodal neighbors. Otherwise they leave two nonempty open arcs. Rotate
indices and, if necessary, reverse cyclic order to put the holes at z_0,z_d
with 2<=d<=2m. Every z_i on the shorter open arc, 1<=i<d, has antipode z_(i+2m)
on the other open arc, not at a hole. The two are joined by their surviving
center c_i. Thus the two arcs are connected in the remaining graph. All centers
with a surviving z neighbor attach to this common component.

A center loses both z neighbors only when the holes are antipodal, d=2m. There
is then exactly one such center, c_0 in the rotated labeling. Its matching
partner c_m has neighbors z_m,z_(3m), both surviving, so c_0 also attaches. The
rotation merely relabels these pairs and does not change the matching rule.
This exhausts all deletions of at most two vertices. Therefore G_m is
3-vertex-connected and belongs to the root domain.

### 3.2 No triangle or square

The z cycle has length at least eight and the graph on centers is a matching.
There is no vertex of D adjacent to two centers. A short cycle containing just
one center would need a path of length one or two in G[D] between its antipodal
endpoints, whose distance there is 2m>=4. A short cycle containing two centers
with no center-center edge needs four spoke edges and at least two D edges,
so has length at least six. With a center-center edge, a square would need an
edge in D between the endpoint pairs of matched centers. Their closest cyclic
distance is m>=2, so no such edge exists. A triangle is likewise impossible.
Three or more centers cannot occur on a cycle of length at most four, since
center-center edges form a matching and each endpoint has only one center
neighbor. Thus the girth is at least five. This bound is enough for the claims;
the finite audit records actual girths of the tested members.

## 4. A unique factor at C, but many factors with other centers

Put C={c_i:0<=i<2m}. The private endpoints of c_i are z_i,z_(i+2m), antipodal
on the 4m-cycle. They are neither adjacent nor share a neighbor on that cycle.
Section 2 proves that every one-center exchange from C fails domination.
Nevertheless the original factor is completely explicit:

    (z_i,c_i,z_(i+2m)),           0<=i<2m.

Replace its paths for i=0,1 by

    (c_0,z_0,z_1), (z_(2m),z_(2m+1),c_1).

They use the same six vertices and only listed edges; all other paths remain.
The resulting factor has center set C*=(C-{c_0,c_1}) union {z_0,z_(2m+1)}.
The minimum positive exchange distance from C to B(G_m) is exactly two.

More generally, for each j=0,...,m-1 let i=2j. The six vertices belonging to
centers c_i,c_(i+1) have a cycle

    z_i,c_i,z_(i+2m),z_(i+1+2m),c_(i+1),z_(i+1),z_i.

Its three tilings by two consecutive P3s have center pairs

    {c_i,c_(i+1)}, {z_i,z_(i+1+2m)}, {z_(i+2m),z_(i+1)}.

These six-vertex blocks partition G_m. Independently selecting one tiling in
each block yields at least 3^m different feasible center sets and P3-factors.
Edges between blocks are simply not selected. This count is a lower bound;
other factors are not excluded.

## 5. Precise failed exchange premise

The basis-exchange axiom for a family B requires: for any X,Y in B and any
x in X-Y there is y in Y-X such that (X-{x}) union {y} is again in B.
Take X=C, Y=C* and x=c_0. Both possible y values, z_0 and z_(2m+1), give an
infeasible center set by Section 2. Thus the actual family B(G_m) violates this
axiom. Its graph with adjacency defined by one-center exchange is disconnected:
C is an isolated vertex and C* is another vertex.

This is not a counterexample to the root: G_m has the displayed factors.
It rules out applying matroid basis-exchange or connectivity of one-exchange
feasible-center walks without a new hypothesis. It does not rule out algorithms
which temporarily leave B(G), exchange several centers, use an enlarged ground
set, or optimize a different potential. The initial C is already feasible, so
this example alone is not a local-search failure for finding the first factor.

## 6. Every change from a private-endpoint set is localized

Return to the general setting of Section 2. Write tau(c) for the matching partner
of c in G[C]. Let C' be any feasible center set, not necessarily satisfying the
private-endpoint condition, and put

    R=C-C', A=C'-C, r=|R|=|A|, S=R union tau(R).

For v in D, let owner(v) be its unique neighbor in C. Then

    owner(A) is a subset of S.                         (L1)

To prove this, consider an old center c not in R with a private endpoint promoted
to A. In C' it loses that endpoint from its available noncenter neighbors. Since
it originally had only two such neighbors, it can still have two only if tau(c)
has become a noncenter, namely tau(c) in R. Thus c belongs to S. If owner(v) is
already in R there is nothing to prove. This proves (L1). It also shows that a
remaining center whose partner was removed can lose at most one private endpoint.

For c outside S, both c and tau(c) remain centers, and neither private endpoint
can lie in A by (L1). Hence in every C'-factor the c path is forced to be its
original private-endpoint path. Delete all these unchanged paths. Both the old
and new factors restrict to P3-factors of the induced graph

    H=G[S union (union over c in S of L_c)].

The private pairs are disjoint, so |V(H)|=3|S|<=6r. This proves localization of
all factor changes, not just their center memberships. It is valid for every
C'-factor and does not assume an alternating-walk implementation.

## 7. Forest uniqueness gives a girth obstruction

A finite forest has at most one P3-factor as a selected edge set. For a tree
edge e and one side W of its deletion, a P3-factor omitting e partitions W into
triples, hence 3 divides |W|. A factor using e has exactly one crossing P3,
which contains one or two vertices in W; all its other P3s are inside one side.
Thus 3 does not divide |W|. Consequently in any factor

    e is selected if and only if |W| is not divisible by three.

All edge memberships are fixed, proving uniqueness. The argument applies in
each tree component and includes the empty forest. It does not assert that a
forest with arbitrary order or shape has such a factor.

When r>0 in Section 6, the old and new factors on H have different center sets,
so they are different factors. H therefore cannot be a forest. If G has girth g,
it follows that

    g <= |V(H)| = 3|S| <= 6r,
    r >= ceiling(g/6).                                (L2)

A sharper version replaces r by the number of matching edges of G[C] touched
by R, since S is the union of their endpoint pairs. This is a necessary lower
bound, not a sufficient criterion for an exchange. No existence theorem for
arbitrarily high-girth graphs with this special partition is assumed or claimed.

## 8. Actual finite observations and reproducible scope

A local generator-side run tested G_m for m=2,...,10 (orders 12 through 60 in
steps of six): cubicity, the two explicit factors, all deletions of at most two
vertices, and all 8m^2 one-center exchanges. Each exchange has a noncenter with
no neighbor in the new center set. For m<=6 all 3^m block-product factors were
constructed and checked, including distinctness of their center sets.

For G_2 and G_3, every center subset of size n/3 was tested by a bipartite
matching with two copies of each center. A separate centered-P3 exact-cover
recursion returned the same feasible sets and counted their factors. The counts
are 41 center sets / 65 factors at n=12 and 243 center sets / 297 factors at n=18.
The distances from the distinguished C have histograms

    n=12: 0:1, 2:16, 3:16, 4:8;
    n=18: 0:1, 2:12, 3:64, 4:90, 5:60, 6:16.

The localization and forced-triple conditions were checked for every feasible
center set of these two explicit graphs. These are not graph-order censuses.

For reproduction, label z_i by i and c_i by 4m+i. Enumerate deletion sets and
center subsets in lexicographic order. In the doubled-center test, clone c into
2c,2c+1, join each clone to every neighbor outside C, and run ordinary augmenting
matching paths until both clones of every center are matched or no augmenting
path exists. In the exact-cover test list each pair a<b of neighbors of c as a
row (a,c,b). Recursively take the least uncovered vertex and sum over rows
containing it and otherwise contained in the uncovered set. Retain the center
mask with each branch; count different centers even on the same triangle.
The empty uncovered set has count one and empty center mask. Equality of the
resulting center masks with the matching test gives the reported comparison.

The companion finite JSON includes the explicit order-12 edge list and both
factors, every per-m test count, execution limits and hashes of local-only code
and output. The observed interpreter was Python 3.13.5; one process used CPU
35 seconds, outer wall 40 seconds, memory 512 MiB, and output limit 2048 KiB,
with a 30-second internal deadline. Exit status was zero. No remote execution,
blocked code re-upload, registered verifier receipt or root admission is claimed.
The full theorem relies on the finite proofs above, not extrapolation from m<=10.

## 9. Next root work

Multi-center algorithms must respect the localized residual factor problem,
rather than assuming a matroid on the original vertex center sets. The next
useful direction is a complete small matched-pair exchange classification or a
constructive extension theorem that tolerates intermediate Hall defects. The
old strengthening stays excluded; canonical records and the obsolete DAG edge
remain untouched pending trusted coordinator action. Root remains open.
