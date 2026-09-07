# ROOT-R07: strict-cycle barriers of girth five and cyclic edge connectivity four

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-root`, with the existing admitted Attempt/Route/Graph.
This strengthens the counterexample to strict-cycle descent, not the counterexample status of the root. Every graph constructed below has an explicit Hamiltonian cycle and hence a P3-factor. No executed census, verifier receipt or admission is asserted.

## 1. Candidate theorem

For every q>=0 there is an explicitly constructible simple cubic graph G_q of order 36+12q with all of the following properties:

- G_q is 3-vertex-connected and has girth five;
- every three-edge cut isolates a single vertex, and G_q has a cyclic four-edge cut;
- G_q has a supplied Hamiltonian cycle;
- G_q has a charged spanning forest of divergence 2 over F3 with exactly one defect, but neither nonzero update on any simple cycle strictly decreases its weight.

Thus eliminating triangles, squares and nontrivial three-edge cuts does not make the strict-cycle descent assertion valid. The assertion invalidated here is a statement about a specified charged flow. The hosts themselves are positive root instances.

We use the fully proved homogeneous-layer lemma in `cycle-local-minimum-family.md`: if the unselected edges are source-source or leaf-leaf, the leaves form three odd cycles with one exceptional exposed leaf in each, and every ordinary P3 has both leaves in its own cycle, then no simple-cycle update has negative cost. Its all-cycles incidence proof is not a computational enumeration.

## 2. The thirty-six-vertex base graph

Use core vertices a=0,b=1,c=2. A block B_r consists of an odd leaf cycle on local vertices 0,...,2r, and sources S_1,...,S_r, where S_i is adjacent to leaves i and i+r. Its ports are leaf 0 and the r sources. Use two blocks B_3 and one block B_4, with the following global labels:

- U: leaves 3,...,9 and sources 10,11,12, paired respectively with (4,7),(5,8),(6,9);
- V: leaves 13,...,19 and sources 20,21,22, paired respectively with (14,17),(15,18),(16,19);
- W: leaves 23,...,31 and sources 32,33,34,35, paired respectively with (24,28),(25,29),(26,30),(27,31).

Include all consecutive cyclic leaf edges in each block and the displayed source-leaf edges. Add the eleven edges

    0-1, 2-1, 0-3, 2-13, 1-23,
    0-20, 2-10, 11-32, 12-34, 21-33, 22-35.

This is a complete edge specification: 13 internal edges in each B_3, 17 in B_4, and eleven additional edges, totaling 54. All 36 vertices have degree three and no edge is repeated.

Select the five core arcs

    0->3, 0->1, 2->13, 2->1, 1->23,

and direct the two displayed edges at every block source toward its leaves. There are 25 selected edges. Vertex 1 is the unique defect; 0,2 and the ten block sources are sources. The unselected source edges are exactly the last six extra edges displayed above. The three leaf cycles have lengths 7,7,9 and contain the exceptional leaves 3,13,23 separately. The homogeneous-layer lemma therefore certifies nonnegative cost for both updates on every simple cycle.

## 3. Three-connectivity and girth of the base graph

Each block is 2-connected: start from its leaf cycle and add each source as a two-edge ear between distinct leaves. Moreover, after deleting at most two block vertices, every remaining component contains a remaining port. If two leaf vertices are deleted, every nonempty remaining leaf interval either contains port 0 or a leaf incident with an undeleted source port; any isolated source is itself a port. If one leaf and one source are deleted, the remaining leaf path is connected and contains a port, and every other remaining vertex attaches to it or is a source port. If two sources are deleted, the leaf cycle remains connected and contains port 0. These cases also cover fewer deletions.

Contract the three blocks. The underlying simple frame is K3,3 with parts {a,c,W} and {b,U,V}; the edges U-W and V-W each have multiplicity two. Adding those parallel incidences does not destroy the vertex- or edge-connectivity of K3,3. Each incidence is attached to a different port in the expanded blocks.

A deletion of two vertices in one block leaves all its components attached to the connected outside frame. A deletion of one vertex in each of two blocks leaves each affected block connected and removes at most two frame edges; the frame remains connected. A deletion of one block vertex and one core vertex leaves connected block interiors and removes at most one edge from the frame minus that core vertex; the latter contains the bridgeless K2,3. Deleting two core vertices leaves the remaining frame connected. This proves 3-vertex-connectivity of the expanded graph. The arguments for fewer deletions are included in the same cases.

Internally a B_3 source joins leaves at distance three around its seven-cycle, and a B_4 source joins leaves at distance four around its nine-cycle. No internal triangle or square is possible: a cycle using one source has length at least five, and a cycle using two sources has at least six edges because their leaf pairs are disjoint. There is an internal five-cycle in B_3.

A cycle meeting more than one block or the core has length at least six. Its projection to the bipartite frame either uses at least four frame edges, or uses two parallel edges. Distinct ports in a block have internal distance at least two, and distinct source ports have distance at least three. A projected four-cycle has at least one block and therefore at least two additional internal edges. The two-parallel-edge case has two source-to-source internal block paths and has length at least eight. A projected walk that revisits a frame vertex cannot produce a shorter cycle than these lower bounds. Thus the base graph has girth exactly five.

## 4. Every base-graph three-edge cut is trivial

We first record a small girth fact with its proof. In a simple 3-connected cubic graph, a nontrivial three-edge cut has distinct endpoints on each side: otherwise at most two vertices on that side separate nonempty surviving vertex sets. Its internal graph on a side of order s therefore has three vertices of degree two and all others of degree three. The side order is odd by degree counting.

In girth at least five, such a nontrivial side cannot have order three, five or seven. Order three would require a triangle. At orders five or seven there is an internal degree-three vertex. Its neighbors and their other neighbors are all distinct, by the absence of triangles and squares. There are at least seven vertices in that radius-two neighborhood, so order five is impossible. At order seven equality forces every neighbor of every internal degree-three vertex to have degree two. But the four degree-three vertices at order seven would require twelve incidences into the three degree-two vertices, which have only six incidences. This is impossible. Thus a nontrivial side has order at least nine.

Suppose a three-edge cut of the base graph splits two blocks. Each split block contributes at least two internal crossing edges, since its interior is 2-connected. This already exceeds three. Hence at most one block is split.

If no block is split, the cut descends to the frame. K3,3 has only vertex-star cuts of size three: subsets of sizes two and three have boundary at least four and five, respectively, unless the complement is a single vertex. The extra parallel edges cannot decrease a boundary. The degree-three frame stars belong only to the core vertices, so the expanded cut is trivial.

If exactly one block is split and the outside is also split, the outside frame contains a K2,3 and contributes at least two crossing edges. Together with the two internal block edges this is again impossible. Thus the smaller separated side lies entirely inside one block and, if nontrivial, has odd order at least nine.

A B_3 has ten vertices and boundary four. Removing one vertex to leave a nine-vertex subset gives boundary at least 4+3-2=5. This excludes a nontrivial three-cut side in B_3.

A B_4 has thirteen vertices and boundary five. Its full vertex set has boundary five. A subset of eleven vertices, obtained by deleting two vertices D, has boundary

    5+3|D|-2e(D)-2p(D) >= 5,

where p(D) counts deleted ports. For a nine-vertex subset, |D|=4 and the boundary is 17-2(e(D)+p(D)). A four-vertex induced graph of girth at least five is a forest, so e(D)<=3. If p(D)<=3 the boundary is at least five. If all four deleted vertices are ports, e(D)=0 because the ports are independent. Thus this case also cannot give boundary three.

All possibilities are exhausted. Every three-edge cut is trivial. The four edges leaving U separate its internal leaf cycle from cycles in V and W, so the base graph has cyclic edge connectivity exactly four.

## 5. A Hamiltonian certificate

The following cyclic sequence contains all 36 vertices exactly once:

    0,1,23,31,35,27,26,34,30,29,28,32,24,25,33,
    21,15,16,22,19,18,17,20,14,13,2,
    10,4,5,11,8,7,6,12,9,3.

Its final edge is 3-0. Every edge follows directly from Section 2. Consecutive triples give an explicit P3-factor, for example

    (0,1,23), (31,35,27), (26,34,30), (29,28,32),
    (24,25,33), (21,15,16), (22,19,18), (17,20,14),
    (13,2,10), (4,5,11), (8,7,6), (12,9,3).

Thus the strict-cycle minimum is not a no-factor certificate.

## 6. A twelve-vertex extension

Choose an unselected source edge u-v and an unselected leaf edge l-r, both on the supplied Hamiltonian cycle, with no edge between {u,v} and {l,r}. Delete the two chosen edges. Add leaves A_0,...,A_7 and sources Z,X,W,Y, with internal edges

    A_i-A_(i+1) for i=0,...,6,
    Z-A_0, Z-A_4, X-A_1, X-A_5,
    W-A_2, W-A_6, Y-A_3, Y-A_7,
    Z-W.

Add attachments u-X, v-Y, l-A_0, r-A_7. Select the eight source-to-leaf arcs at Z,X,W,Y and leave the new remaining edges unselected.

The source matching replaces u-v by u-X,v-Y,Z-W. The leaf cycle replaces l-r by the eight-leaf path, increasing its length by eight. Its exposed exceptional leaf is unchanged. All four new ordinary P3s have both leaves in that same cycle. Therefore the homogeneous-layer hypotheses and the single defect persist. The order increases by twelve and the edge count by eighteen.

The internal graph I has ports X,Y,A_0,A_7 and sixteen edges. It is obtained from the eight-cycle A_0,...,A_7 with opposite chords by deleting A_7-A_0, subdividing its four opposite chords by Z,X,W,Y, and adding Z-W. The original eight-vertex graph is 3-connected: its opposite chords have connected interlacement, which rules out two-edge cuts, and the elementary cubic argument gives vertex connectivity. Deleting one edge preserves 2-connectivity, subdividing edges preserves it, and adding Z-W cannot destroy it. Hence I is 2-connected.

After at most two deletions in I, every remaining component has a remaining port. To see this, suppose a port-free component contains an A_i. Temporarily restore A_7-A_0; both endpoints are ports, so the restored edge cannot reconnect this port-free component. In the underlying eight-vertex graph, deletion of an A_i is a vertex deletion and deletion of a subdivision source removes one chord. Any combination of at most two such deletions leaves that graph connected: the mixed one-vertex/one-edge case follows because deletion of one vertex leaves a bridgeless graph. All surviving original vertices would therefore lie in the same component. That component contains a surviving original port, or, if both original ports were deleted, it contains the surviving port X or Y through its neighbors. This is a contradiction. A component with no A_i is a subset of {Z,W}; isolating either one requires three deletions and isolating both requires four. This proves the port assertion.

## 7. Three-connectivity and girth after extension

If two deleted vertices are old, every component of the old remainder after additionally removing u-v,l-r has a surviving attachment endpoint. Otherwise restoring those edges could not reconnect the old graph with only two vertices deleted. The intact I joins all these components.

If two deleted vertices are new, the old graph minus the two selected edges is connected by 3-edge-connectivity, and every remaining new component attaches by the port assertion.

If one vertex is deleted on each side, I minus one vertex is connected. The old graph minus one vertex is 2-connected and bridgeless. Removing at most one effective edge leaves it connected; if both removed edges remain effective, every resulting old component has at least two distinct attachment endpoints. The new deletion removes at most one of them. Hence all components still join. These arguments prove 3-connectivity. Simplicity and cubicity follow from the distinct attachment endpoints.

I has no triangle or square. Without Z-W it is a subdivision of a subgraph of the eight-cycle with opposite chords; every square of that graph uses two chords and is lengthened by their subdivisions, and its other cycles are not shortened. Adding Z-W can create no cycle shorter than five, since the neighbor sets {A_0,A_4} and {A_2,A_6} have no common or adjacent vertices on the leaf path. A cycle crossing the four attachments has at least five edges: a four-cycle would require an old edge between {u,v} and {l,r} in addition to an adjacent port pair, and that was excluded. The old five-cycle in U is left unchanged by the iterative choices below. Girth remains five.

## 8. The extension preserves the absence of nontrivial three-edge cuts

We need the following precise four-port property of I. For every nonempty subset C of its vertices, let p(C) count its ports. Then

    |delta_I(C)|+p(C) >= 4

unless C is a single vertex. The full set also has boundary four.

Here is a proof rather than an assumed gadget property. Put A=C intersect {A_0,...,A_7}, and compare the displayed boundary with the cut of A in the original eight-cycle with opposite chords. Subdividing a chord never lowers its contribution. A subdivision vertex X or Y in C adds at least one extra boundary contribution from its external port. If X or Y is outside C while both its chord endpoints lie in A, that chord contributes two extra edges. Replacing A_7-A_0 by the two external port incidences adds two when both endpoints lie in A and zero otherwise. The added edge Z-W is another nonnegative contribution.

Every nontrivial three-edge cut of the original eight-vertex graph is a vertex star: it is triangle-free and a nontrivial side would have odd order three or five and would require a triangle on the smaller side. Thus, when A is nonempty and proper, a boundary at most three would force A to be a singleton or its complement and all extra contributions to vanish. For a singleton A, X,Y must lie outside C and Z,W must be on the same side. They cannot both lie inside because their chord endpoint pairs are disjoint, so one subdivision would then contribute two extra edges. Hence C is just that singleton. For a seven-vertex A, X,Y again lie outside, but at least one of their two disjoint endpoint pairs lies entirely inside A and contributes two extra edges, a contradiction.

If A is empty, C is a subset of {X,Y,Z,W}, whose only internal edge is Z-W. Any subset of at least two of these vertices has the claimed boundary at least four. If A contains all eight original vertices, the ports A_0,A_7 contribute two and the two subdivided X,Y chords contribute at least one each. This proves the four-port property in all cases.

Now consider a three-edge cut of the extended graph. If I is wholly on one side, the old cut obtained by restoring u-v,l-r has size at most three and hence is a vertex star. The new cut is trivial if the outside side is that singleton. If its old complement is the singleton, at least three attachment edges and at least two remaining old edges cross, giving boundary at least five, impossible.

If I and the old vertices are both split, I contributes at least two crossing edges. The old graph minus u-v,l-r is connected and contributes at least one. Boundary three forces exactly two plus one and no crossing attachment. Restoring the two old edges must make both cross, or it would produce an old cut of size at most two. The resulting old three-edge cut would isolate one vertex. But two disjoint removed edges cannot both be incident with that vertex. This is impossible.

The only other possibility is a side wholly inside I. The four-port property makes a three-edge cut of this form a singleton. Thus all three-edge cuts remain trivial. The four attachments isolate cycles of I from cycles of the old graph, providing a cyclic four-edge cut.

## 9. Hamiltonian lifting and iteration

I has the following two pairs of disjoint spanning paths between its ports:

    X-A_1-A_0,
    Y-A_3-A_2-W-Z-A_4-A_5-A_6-A_7;

and

    X-A_5-A_4-Z-W-A_6-A_7,
    Y-A_3-A_2-A_1-A_0.

Each displayed pair covers all twelve new vertices exactly once. The first pairs X with A_0 and Y with A_7; the second uses the other cross-pairing. Removing u-v and l-r from the old Hamiltonian cycle leaves two paths. Exactly one of these two new pairings joins them into a single cycle. Choose it and all four attachments. This is a finite explicit Hamiltonian lifting rule.

In the base graph choose u=2,v=10,l=23,r=31. Both chosen edges occur in the supplied Hamiltonian cycle, and the two endpoint sets have no joining edge. At each next step choose the newly created edges 2-X and 23-A_0. They occur in the lifted Hamiltonian cycle. The new X is adjacent only to A_1,A_5 and 2, while 2 has no adjacency to 23 or the new A_0. Thus the required endpoint separation persists.

The iteration has order 36+12q, leaves U and V unchanged, and lengthens the W leaf cycle from nine to 9+8q. Its initial charged support still has one defect and meets the homogeneous-layer lemma. Every host has the constructed Hamiltonian cycle, whose consecutive triples give a P3-factor. Every three-edge cut is trivial and a cyclic four-edge cut is supplied, so cyclic edge connectivity is exactly four.

## 10. Scope

The family rules out strict simple-cycle descent even after imposing girth five and the absence of nontrivial three-edge cuts. It does not supply a root counterexample, a no-factor certificate, or a theorem about every cubic graph of any listed order. The twelve-vertex extension preserves an explicit positive witness, while the all-cycles obstruction comes from the exact layer identities. Neutral updates and larger exchange cores remain the relevant open repair mechanisms. All conclusions are proof candidates pending the repository's prescribed verification and statement-faithfulness checks.
