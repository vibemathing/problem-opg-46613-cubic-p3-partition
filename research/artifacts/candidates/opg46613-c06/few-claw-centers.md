# C06: P3-factors with few vertices outside triangles

Verdict: `candidate_only`. Primary owner: `math-proof`.
Admitted target: `obligation:opg46613-divisible-two-factor`, repair analysis.
The original root remains open; this is a restricted-class candidate, not a
revival of the already obstructed divisible-complementary-cycle assertion.

## Candidate statements

Let G be finite, simple, cubic and 3-vertex-connected, and suppose 3 divides |V(G)|.
Let U(G) be the set of vertices lying in no triangle, and put u=|U(G)|.

1. If u is at most nine, G has a P3-factor.
2. If G is planar and u is at most twenty-one, G has a P3-factor.

In a simple cubic graph, v lies in a triangle precisely when two of its three
neighbors are adjacent. Thus U(G) is also exactly the set of centers of induced
claws. The statements count centers, not vertex-disjoint claws or chosen copies
of a claw. P3 components are selected two-edge paths, not induced paths.

The proof consists of the elementary reductions below, the C05 cycle-gluing
construction specialized to triangle cells, the published nine-point theorem,
and the planar 23-point theorem. The external theorems' exact public statements
were checked, but their full proofs have not been audited in this candidate.
The source note specifies dependencies and reuse limits. No novelty is claimed.

## Lemma A: collapse the triangles without losing the frame hypotheses

The handshake identity gives |V(G)| a positive multiple of six. In particular
G is not K4. Every nontrivial edge cut has at least three edges: a cut of at most
two edges cannot have a side of size one or two in a simple cubic graph; deleting
its at most two endpoints on one side would leave vertices on both sides and
contradict 3-vertex-connectivity.

Distinct triangles of G are vertex-disjoint. Sharing exactly one vertex would
require at least four edges there. If two triangles share edge ab and have third
vertices c and d, then a,b have no neighbors outside {a,b,c,d}. If c,d are adjacent,
this is an entire K4 component. If they are not adjacent, deleting c,d disconnects
a,b from the vertices outside those four. Both alternatives are impossible here.

Contract every triangle into one cell and leave every vertex of U(G) as a
singleton cell. Delete only the three internal triangle edges on contraction.
The resulting quotient Q is connected, loopless and cubic; a triangle has exactly
three external edges. Every nontrivial cut of Q is the corresponding cut of a
union of cells in G, so its size is at least three, counting multiplicities.

If two quotient vertices are joined by at least two edges and there are other
quotient vertices, their two-cell union has at most two outgoing edges, contrary
to that cut bound. A one-cell quotient is impossible here. Thus either Q is
simple with at least four vertices, or Q has exactly two cells joined by three
parallel edges. In the latter case, both cells must be triangles: two singleton
cells would violate simplicity of G, while one singleton and one triangle would
be K4. Hence the exceptional original graph is the triangular prism. Its two
triangles can each be tiled by one selected P3, proving the conclusion immediately.

In the other case Q is also 3-vertex-connected. Here is the needed cubic argument,
so contraction is not assumed to preserve vertex connectivity automatically.
A cut vertex x would leave at least two components, each requiring at least three
edges to x by the edge-cut bound, impossible when d(x)=3. If two vertices x,y form
a cut, every component after deleting them again has boundary at least three.
If xy is an edge there are at most four remaining incident edges, impossible.
If xy is absent, there are exactly two components A,B, with three boundary edges
each. Connectivity of Q implies x and y each have neighbors on both sides.
Relabel so that A has one edge to x and two to y. Then A together with y has just
two edges to its complement: one from A to x and one from y to B. This contradicts
the edge-cut bound. Thus no deletion of at most two vertices disconnects Q.

If G is planar, Q is planar: contract two edges of each connected triangle in a
planar drawing and remove its remaining loop. The simple quotient from above
is unchanged. We are now within the exact hypotheses of the cyclability sources.

## Lemma B: common-cycle gluing works for triangle cells

Mark in Q the singleton cells corresponding to U(G). Their number is u, and
|V(G)|=3t+u, where t is the number of triangle cells. Therefore 3 divides u.
If u=0, tile all triangle cells internally and finish without a cycle theorem.
Otherwise suppose a simple cycle C of Q contains all marked vertices.

Each triangle has terminals a,b,c. It supports UUU by selecting any two-edge path
inside it. For any distinct a,b, it supports A at a, B at b and unused boundary
at c: leave a as a singleton, and select the internal pair bc centered at b.
All six choices exist, without an automorphism or any external assumption.

Apply the same F3 recurrence as C05 along the cyclic order of C: subtract one at
a marked vertex and zero at a triangle cell; begin with boundary value zero.
The value returns to zero since u is divisible by three. Value one directs a
selected frame edge forward, value two backward, and zero leaves it unselected.
Marked vertices have one incoming edge or two outgoing edges. Triangle cells
have either no selected boundary or one incoming and one outgoing boundary.
All other cells have no selected boundary. Use the two local patterns just given.

Orient internal selected edges from their centers to endpoints. Every vertex
of the resulting selected spanning subgraph has either two outgoing edges and
no incoming edge, or one incoming edge and no outgoing edge. Every selected edge
joins a center to an endpoint. Consequently every component has one center and
its two endpoints and is exactly P3. No unselected edges are required to disappear.
This proves the gluing lemma for every permitted port bijection and supplied C.

The construction also works with any mixture of triangle and C05 Petersen bricks,
since both supply these seven patterns. This is only a sufficient cycle interface;
a triangle does not supply every nine-vertex-brick interface. In particular it
cannot realize three B pairs on its three vertices, so the unrestricted C04
marked-forest equivalence is NOT transferred to triangles by this argument.

## Lemma C: handle the small quotients explicitly

The nine-point source is applied to nine distinct frame vertices, so small Q
must not be disposed of by a vacuous reading of that theorem. Every simple
3-connected cubic graph of order four, six or eight has a Hamiltonian cycle:

A perfect matching exists by the finite matching/cut argument in C04's
`lower-order-factor-cover.md`. Its complementary 2-factor has cycle partitions
(4) at order four; (6) or (3,3) at order six; and (8), (3,5), or (4,4) at order
eight. The single-cycle cases already give the claim.

For (3,3), the matching has all three edges between the triangles; use any two
of them and a spanning path through each triangle. For (3,5), all three triangle
vertices have matching partners on the five-cycle. Among those three partners,
two are adjacent on that five-cycle, since an independent set in C5 has size at
most two. Delete that adjacent edge on C5 and the edge joining the corresponding
two terminals on C3; the two resulting spanning paths and their two matching
edges form a Hamiltonian cycle. For (4,4), an even number of matching edges cross
the two cycles, and the edge-cut bound forces all four to cross. The matching
bijection identifies their vertex sets. Each four-cycle supplies four adjacent
pairs out of the six possible pairs, so some pair is adjacent on both cycles.
Delete those two cycle edges and join the spanning paths by the matching edges
at their endpoints. This again gives a Hamiltonian cycle. The argument exhausts
all small-quotient cases and uses no graph-catalog completeness assumption.

## Complete the two restricted-class proofs

For u at most nine and |V(Q)| at least ten, enlarge the u marked vertices to a
set of nine distinct vertices of Q. The nine-point theorem gives a common cycle,
hence a cycle through the marked subset. At smaller quotient orders, Lemma C
supplies a Hamiltonian cycle. Lemma B then gives a P3-factor of G.

For planar G, apply the planar theorem of Aldred, Bau, Holton and McKay: every
set of at most twenty-three vertices of a 3-connected cubic planar graph lies
on a cycle. Its statement is explicitly for "at most" that number, so it applies
directly to the marked set in Q, including small quotients. Since u is a multiple
of three, the eligible values covered by u <= 23 are precisely 0,3,...,21.
Again Lemma B gives the factor. The zero and prism cases were handled separately.

Thus a counterexample to the original question, if one exists, must have at
least twelve induced-claw centers. A planar counterexample must have at least
twenty-four. These are necessary conditions from this candidate argument; no
existence or sharpness of a P3 obstruction at those bounds is asserted.

## Boundary checks and exact finite audit

`triangle_audit.py` checks the actual selected P3 components and independently
reconstructs all triangles of each expanded test graph before contracting them.
It verifies quotient simplicity, cubicity and connectivity after every deletion
of up to two quotient vertices. All 12014 tested cases succeed: 11990 have a
simple cubic 3-connected quotient, and 24 give the explicit prism exception.
Thirteen selected expanded graphs also pass every deletion of up to two of their
own vertices. The tests cover all seven local signatures and 80 specified
21-retained samples on a planar 12-prism frame. They are not an exhaustive
census of cubic or planar graphs and do not test universal source cyclability.
Actual Python version, counts, output digest and execution limits are preserved.

Reproduce with `python3 -S triangle_audit.py`, one process, CPU limit 40 seconds,
wall limit 43 seconds, memory 256 MiB and output file limit 1 MiB. The program's
internal audit deadline is 35 seconds. All calculations are generator-side.
Both admitted obligations remain open pending the required proof, axiom and
statement-faithfulness verification. No canonical failure record is changed.
