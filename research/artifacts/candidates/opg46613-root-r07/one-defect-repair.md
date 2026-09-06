# ROOT-R07: one-defect repair and the source-port omission

Verdict: `candidate_only`. Primary owner: `math-proof`.
Problem: `problem:opg-46613-cubic-p3-partition`.
Attempt: `attempt:web-20260906-opg46613-a01`.
Route: `route:two-factor-divisible-cycles-v1`.
Graph: `graph:opg46613-initial-v1`.
Target: `obligation:opg46613-root`.
This is a partial root-oriented proof, not a revival of the divisible-two-factor strengthening. The canonical graph and its legacy dependency are not edited.

## 1. Setting

A selected directed edge points from its P3 center toward an endpoint. More generally, assign values in F3 to the edges of a cubic graph, relative to arbitrary reference orientations, and require divergence 2 at every vertex. The permitted nonzero incidence types are a source with two outgoing edges, a leaf with one incoming edge, and a defect vertex with two incoming edges and one outgoing edge. The number of selected edges is 2n/3+b, where b is the number of defect vertices. In particular, b=0 gives exactly a P3-factor: all selected edges join sources to leaves.

We reuse the elementary identities of ROOT-R06, not any unproved global descent assertion. Suppose the selected support is a spanning forest with exactly one defect. Its exceptional component has six vertices and arcs

    a -> a', a -> b, c -> c', c -> b, b -> d.

Every other component is a P3 with its two selected edges directed from its source. The exceptional tree is denoted T. All six vertices displayed are distinct. A source still has one unselected incident edge in the ambient cubic graph; those edges must not be silently removed from an exact repair problem.

## 2. A sufficient auxiliary matching test

Let L be the set of selected leaves. For every ordinary P3 component (l,x,r), introduce a typed virtual matching edge lr, remembering its source x. Let M be the set of these virtual edges. Add every actual ambient edge whose endpoints both lie in L as a real edge. These actual edges are unselected. Keep virtual and real edges distinct if they have the same endpoints.

The resulting auxiliary multigraph has precisely three vertices unmatched by M: a', c', d. If the original graph has order 3k, then |L|=2k-1 and |M|=k-2.

**Repair lemma.** If M is not a maximum matching of this auxiliary graph, the original charged forest admits one simple-cycle update reducing its weight by one, and hence yielding a P3-factor.

Proof. The symmetric difference of M with a larger matching is a union of alternating paths and even cycles. Since the second matching is larger, one component is an augmenting path for M. Its endpoints are two distinct members of {a',c',d}. Its internal vertices cannot include the third exposed vertex: each internal vertex on an alternating augmenting path is incident with a matching edge of M.

Replace each virtual edge lr on the augmenting path by its actual selected path l-x-r. Distinct matching edges represent different ordinary sources. A simple auxiliary path has distinct leaves, so this lift is a simple ambient path; its interior is disjoint from T. Close it by the unique path in T between its endpoints. This gives a simple ambient cycle.

If the augmenting path contains t virtual edges, its lift contains t selected edges in each orientation and t+1 unselected edges. The path in T between a' and c' contributes two selected edges in each orientation. A path between d and either other exposed vertex contributes two in one orientation and one in the other. Thus, for the complete cycle, the numbers p,q,k of selected forward, selected reverse, and unselected edges are, up to exchanging p,q,

    (p,q,k) = (t+2,t+2,t+1) or (t+2,t+1,t+1).

Adding a unit F3 circulation around a simple cycle changes its weight by k-q; adding the opposite circulation changes it by k-p. In either displayed case one update has change -1. It preserves every divergence. Its weight is now 2n/3, so the defect-count identity makes every selected component a P3. This proves the lemma.

The conclusion is sufficient, not an equivalence. In particular, maximum cardinality of M certifies only failure of this restricted test.

## 3. Explicit eighteen-vertex control

Let the vertex set be 0,...,17, and use these 27 unordered edges:

    0-1 0-2 0-10 1-6 1-9 2-3 2-5 3-4 3-17
    4-12 4-15 5-8 5-13 6-7 6-8 7-11 7-16 8-10
    9-10 9-11 11-13 12-13 12-14 14-16 14-17 15-16 15-17.

Select the following 13 arcs:

    0->1, 0->2, 3->2, 3->4, 2->5,
    6->7, 6->8, 9->10, 9->11,
    12->13, 12->14, 15->16, 15->17.

The first five arcs give T, with (a,a',b,c,c',d)=(0,1,2,3,4,5). The remaining arcs give four ordinary P3 components. Each vertex has divergence 2 in F3; there is exactly one defect, at 2.

The leaf set and its virtual matching are

    L={1,4,5,7,8,10,11,13,14,16,17},
    M={7-8,10-11,13-14,16-17}.

The real auxiliary edges are

    5-8,5-13,7-11,7-16,8-10,11-13,14-16,14-17.

Both 1 and 4 are isolated in the auxiliary graph. At most floor((11-2)/2)=4 matching edges are possible, and M already has four. Therefore M is maximum and has no augmenting path. This is a complete matching-number argument, not a negative solver assertion.

Nevertheless take the simple cycle in cyclic order

    (0,1,6,7,16,15,17,3,2).

It has p=4 selected edges in the displayed direction, q=2 selected edges in the reverse direction, and k=3 unselected edges. Subtract its unit circulation. The weight changes by k-p=-1. Directly, the result is the factor

    (0,2,5), (4,3,17), (1,6,8),
    (10,9,11), (13,12,14), (7,16,15).

The middle entry in each triple is its center. Each consecutive pair is one of the 27 listed edges and all eighteen vertices occur exactly once. Thus the graph is a positive root instance, not a root counterexample.

The missing information in the restricted auxiliary graph is concrete: the improving cycle uses unselected edges 1-6 and 3-17 incident with old sources. These edges disappear when the auxiliary construction retains only the selected leaves. Failure of its matching test cannot imply that the original one-defect forest is irreparable.

## 4. A short, noncomputational three-connectivity certificate

The graph in Section 3 has the Hamiltonian cycle

    H=(0,10,9,1,6,8,5,13,11,7,16,14,12,4,15,17,3,2).

Every consecutive pair, including 2-0, is listed above. The nine edges outside H form a perfect matching. In terms of positions 0,...,17 on H, call these chords

    A=(0,3), B=(1,5), C=(2,8), D=(4,9), E=(6,17),
    F=(7,12), G=(10,14), I=(11,15), J=(13,16).

Two chords interlace when their endpoints alternate around H. The following eight interlacements give a spanning tree of the nine-chord interlacement graph:

    AB, AC, BD, CE, CF, FG, FI, GJ.

Every one is verified by the displayed endpoint positions. For example C and E interlace as 2<6<8<17, and G and J as 10<13<14<16.

A Hamiltonian graph has no bridge. If a cut of size two existed here, the Hamiltonian cycle would contribute exactly its two crossing edges, leaving no crossing chord. The vertices on either side would form one nonempty cyclic interval, with every matching chord contained wholly in one interval. Each interval would contain a chord, because every vertex has a matching partner and no chord crosses. Chords in different intervals cannot interlace. This would disconnect the interlacement graph, contradicting the displayed spanning tree. Thus the graph is 3-edge-connected.

For completeness, a simple cubic 3-edge-connected graph is 3-vertex-connected. A cut vertex would leave at least two components, each with at least three incident boundary edges, impossible at a degree-three vertex. If deleting two adjacent vertices disconnects the graph, only four edges leave that pair, again fewer than the six required by two component boundaries. If the two deleted vertices u,v are nonadjacent, exactly two components remain, each with boundary three. Each component meets both u and v, since there is no cut vertex. One component C has two edges to one of them, say u, and one to v. Then delta(C union {u}) has size 3+3-4=2, contrary to edge connectivity. This handles all vertex cuts of size at most two.

Finally the graph is triangle-free. Its non-Hamiltonian edges are a matching, so a triangle would contain two consecutive Hamiltonian edges and one chord. That chord would join positions at cyclic distance two. None of the nine displayed chords does. This does not assert girth at least five: chord A and the intervening three cycle edges give a four-cycle.

These arguments establish the host hypotheses at candidate proof level without depending on an executed census, library connectivity call, or external graph catalogue.

## 5. Boundary of the result

The auxiliary matching test is a sound inexpensive sufficient repair criterion. Its failure is not a certificate that a charged forest, or its host graph, has no P3-factor. A stronger repair model must retain source third-edge incidences or permit the full simple-cycle updates of ROOT-R06.

The eighteen-vertex example only separates a restricted repair test from actual repair. It does not resolve whether every one-defect forest in a 3-connected cubic graph admits a decreasing simple cycle, whether neutral cycles always suffice before a decrease, or whether every root graph has a zero-defect charged flow. Those remain distinct open research questions.

No exhaustive-order claim, executable result, verifier receipt, EvidenceLink, Result, or Solution admission is asserted in this proof file. The exact definitions, 27-edge input, thirteen initial arcs, nine-cycle update, six output triples, and chord interlacement certificate are the complete finite objects to replay. Both canonical obligations remain open.
