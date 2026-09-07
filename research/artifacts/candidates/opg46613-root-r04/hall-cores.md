# ROOT-R04: minimal Hall cores and a two-center repair barrier

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-root` in the retained admitted graph and attempt.
This partial proof refines ROOT-R02. No root counterexample or universal
center-selection theorem is claimed.

## 1. Fixed-center notation

Let G be finite simple cubic, of order 3k. Fix C of size k and put D=V(G)-C.
Assume G[C] has maximum degree at most one, a necessary but insufficient condition
for C to be the centers of a P3-factor. Write N(S)=N_G(S) intersect D.
ROOT-R02 proves that C works exactly when |N(S)|>=2|S| for every S subset C.
The companion source note records an exact general-graph characterization in
Bose--Maheshwari--Miraftab--Otachi, Theorem 7 (2026), expressed from the D side.

If C fails, let S be inclusion-minimal among its nonempty Hall-deficient subsets.
Put t=|S|, q=|N(S)|, d=2t-q>0. The incidence graph J retains only edges between
S and N(S); edges within D and all vertices outside these two sets are discarded.
Let r count vertices of S having a neighbor in C. Because G[C] has maximum
degree one, each such vertex has exactly two neighbors in D and every other
vertex of S has three.

## 2. The defect/cycle-rank identity (claim root-r04-rank)

The graph J is connected, d is either 1 or 2, and

    mu(J) = |E(J)|-|V(J)|+1 = d+1-r.

In particular r<=d+1. These conclusions do not require G itself to have large
girth or high connectivity.

Proof. Every center has at least two external neighbors, so t>=2. For c in S,
let p_c be the number of neighbors of c which have no other neighbor in S.
Minimality applied to S-{c} gives

    q-p_c >= 2(t-1), hence p_c <= 2-d.

Thus 1<=d<=2. If J had more than one connected component, its center parts
would all be proper subsets of S. Applying Hall to each and adding the disjoint
neighbor counts would give q>=2t, a contradiction. Finally |E(J)|=3t-r and
|V(J)|=t+q, which yields the displayed identity. A connected graph has
nonnegative cycle rank, proving r<=d+1.

Interpretation: an eligible proposed center set cannot have a minimal bad support
with arbitrarily many center-center incidences. A defect-one support has at most
two, and a defect-two support at most three. This is a restriction on a fixed C,
not an assertion that G has no such support for some suitable C.

## 3. Defect two without four-cycles (root-r04-tetrahedron)

If G has no four-cycle and d=2, then t=4, r=0, and J is exactly the graph
obtained by subdividing every edge of K4 once. The four original K4 vertices
are S. Conversely that incidence graph gives a minimal Hall defect of two.

Proof. Since d=2, the bound p_c<=0 shows that every vertex of N(S) has at least
two neighbors in S. Thus

    3t-r = |E(J)| >= 2q = 4t-4, so t+r<=4.

If t=2, the two centers need at least two neighbors each but q=2; they form a
four-cycle. If t=3, then r<=1. No pair of centers can have two common neighbors,
so inclusion-exclusion gives

    q >= (3t-r)-binom(t,2) = 6-r >= 5,

contrary to q=4. Therefore t=4 and r=0. Equality in the edge count makes each
of the six neighbor vertices have degree two in J. Suppress those six vertices.
This produces a loopless cubic multigraph on four center vertices. Parallel
edges would give a four-cycle in J, so it is simple and hence K4.

Conversely, the six subdividing vertices are the neighbors of all four centers,
so the defect is 8-6=2. One, two, or three centers have respectively 3,5,6
neighbors, hence each proper subset satisfies Hall. This also confirms that
all four centers have no neighbors elsewhere in C.

Corollary. In a cubic graph of girth at least seven, every minimal Hall defect
of an eligible center set has d=1: the defect-two graph contains a six-cycle.
This does not say that such graphs automatically have a P3-factor.

## 4. Defect one when the center set contains no edge (root-r04-bicycle)

Now assume G[C] has no edge and d=1. Delete all degree-one neighbor vertices
from J, leaving J0. Then J0 is connected, all its degrees are two or three,
and exactly two of its vertices have degree three. After suppressing its
degree-two vertices, its topology is one of:

- two vertices with three parallel edges (a theta);
- two vertices joined by one edge, each also carrying one loop (two disjoint
  cycles joined by a path, or loose handcuffs).

These describe suppressed incidence cores, not loops or parallel edges in G.

Proof. Each center originally has degree three and loses at most p_c<=1 leaf.
No remaining neighbor vertex changes degree. Thus every degree is two or three,
and removing pendant leaves preserves connectivity and cycle rank. Section 2
has r=0, so mu(J0)=2. Consequently sum_v(deg(v)-2)=2, giving exactly two
branch vertices. Suppression leaves a connected multigraph on these two
vertices, both of degree three. If h edges join them and l1,l2 are the loop
counts, then h+2l1=h+2l2=3. Connectivity requires h>0, so either h=3,l1=l2=0,
or h=1,l1=l2=1. This proves the classification directly.

This topology is familiar from bicircular matroids; it does not prove that the
feasible center sets of G are matroid bases. Changing C changes its incidence
graph, and the one-exchange assertion in Section 5 explicitly fails.

A finite small-support consequence is also available. Suppose G has no
four-cycle and t=4. Let h be the number of degree-three vertices on the neighbor
side of J0, so h is 0,1,or2. Counting edges before and after leaf deletion shows
that there are t+h-2 deleted leaves and

    |E(J0)| = 2t-h+2 = 10-h.

A handcuff core has two cycles of even length at least six plus a nonempty
joining path, requiring at least thirteen edges, so it is impossible here.
For a theta, let its three branch-to-branch path lengths be l1,l2,l3. They
have the same parity; each pair sum is at least six.

- h=0: both branch vertices are centers, all lengths are even, and their sum
  is ten. The only possibility is (2,4,4), up to order.
- h=1: branch vertices lie on opposite sides, all lengths are odd, and their
  sum is nine. The only possibility is (3,3,3).
- h=2: their sum is eight, whereas adding the three cycle bounds requires
  their sum to be at least nine. This is impossible.

Thus a four-center minimal defect in this edgeless-center/no-four-cycle setting
has exactly three incidence types: the defect-two subdivided K4, or one of the
two displayed defect-one thetas with its forced private leaves. No enumeration
of host cubic graphs is needed for this necessary classification.

## 5. Why a defect-two support cannot be fixed by one exchange (root-r04-no-one-swap)

Suppose G[C] has no edge and S is minimal with defect two. No center set

    C' = (C-{c}) union {v}, with c in C and v in D,

can be the centers of a P3-factor. The new C' is not required to remain edgeless.

Proof. If c is outside S, making c an endpoint supplies no new neighbor to S,
since G[C] has no edge. Moving v to the center side can only remove a neighbor
from S. Its original positive Hall deficit therefore remains.

If c is in S, the new endpoint c has no neighbor in C-{c}. For C' even to
dominate c, v must belong to N_G(c), hence to N(S). Minimal defect two gives
p_c=0, so N(S-{c})=N(S). The external neighborhood of S-{c} relative to C'
is now exactly N(S)-{v}: c supplies no neighbor because C had no edge. Its size
is 2t-3, less than 2(t-1). Again Hall fails. This exhausts all exchanges.

The lemma forbids repairing the whole fixed center set in a single exchange.
It does not forbid partial improvement followed by another exchange, nor imply
that the host graph has no other good center set.

## 6. Explicit eighteen-vertex control and a two-exchange factor

Use vertices 0,...,17. Subdivide the six edges 01,02,03,12,13,23 of K4 by
vertices 4,5,6,7,8,9, respectively. Separately use the three paths

    10-12-15-11, 10-13-16-11, 10-14-17-11.

Join i to i+8 for i=4,...,9. These are exactly the 27 edges in the companion
JSON. Let C={0,1,2,3,10,11}. This is an edgeless dominating size-six set.
Its subset S={0,1,2,3} has exactly the neighbors {4,5,6,7,8,9}; Section 3
certifies its minimal defect two. Section 5 excludes all 6*12 possible
single exchanges, by proof rather than relying on a solver's negative result.

The graph nevertheless has the factor

    (4,0,5), (7,1,8), (2,9,3),
    (6,14,17), (12,10,13), (15,11,16).

Its centers are {0,1,9,14,10,11}; this replaces precisely 2,3 by 9,14 in C.
Every edge in these six triples appears in the displayed construction and all
18 vertices occur once. The minimum exchange distance from C to a factor's
center set is therefore exactly two.

Here are self-contained host-property checks. The two pieces of the graph are
a subdivided K4 and a three-path theta, each 2-connected. Their six joining
edges form a matching, with every non-branch vertex of each piece a port.
Deleting one vertex from each piece leaves both connected, and at least four
joining edges survive. Deleting two vertices from one piece leaves every
remaining component attached to the untouched other piece: a component without
a surviving port would consist only of its branch vertices, which are mutually
nonadjacent, and isolating any branch would require deleting its three distinct
port neighbors. That is impossible with two deletions. The same reasoning
handles fewer deletions. Hence the graph is simple cubic and 3-connected.

Every cycle confined to either piece has length at least six. A cycle crossing
the joining matching uses at least two of its edges. With exactly two crossings,
its path between K4-side ports has length at least two (there are no adjacent
ports there), and its other path has length at least one, so its total length
is at least five. Four or more crossings require at least eight edges. The
cycle 1-4-12-15-7-1 has length five. Thus the girth is exactly five.

## 7. Finite observations and reproducibility boundaries

A local Python 3.13.5 generator checked cubicity, the displayed factor, all 172
deletions of at most two vertices, and all 131071 unordered nontrivial vertex
bipartitions of this one graph. The companion JSON records these finite
observations, the neighbor sets of all 15 proper subsets of S, and the complete
cut-size histogram. It is not a census of eighteen-vertex cubic graphs and not
a registered verifier receipt.

For replay, number bits by vertices, fix bit 0 equal to one, and run through
all odd masks m with 1<=m<2^18-1. For each, compute

    b(m) = sum over edges {u,v} of (bit_u(m) XOR bit_v(m)).

There were exactly 18 cuts of size three and 27 of size four. The known cuts
isolating one vertex give 18 distinct size-three bipartitions; those isolating
the endpoints of an edge give 27 distinct size-four bipartitions. Thus the
observed histogram, if replayed correctly, excludes any other cut of these
sizes. A five-cycle side such as {3,6,9,14,17} and its complement each contain
a cycle and have five crossing edges. The resulting observed cyclic edge
connectivity is five. This last finite histogram conclusion remains a replay
obligation; the structural claims and the one-exchange barrier above require
only the fully supplied hand proofs of 3-connectivity and girth five.

The private local checker used a 35-second CPU limit, 512-MiB address-space
limit and a 45-second outer timeout. No remote execution or previously blocked
code upload is asserted. The prepared checker is not included in this proof-only
packet; the formulas and explicit input permit a new permitted implementation.

## 8. Open root work

The center Hall characterization is exact but still existential in C. These
results restrict minimal obstructions for a proposed C; they do not supply a
choice of C or a guaranteed sequence of improving exchanges. Next examine
multi-center alternating exchanges and the relation between these incidence
cores and actual cut signatures. The old divisible-two-factor route remains
excluded, the canonical DAG is unchanged, and root remains open.
