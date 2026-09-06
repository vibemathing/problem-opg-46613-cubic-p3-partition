# ROOT-R07: one-defect strict-cycle minima with cyclic connectivity five

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-root` in the existing admitted Attempt/Route/Graph.
This is a stronger parameter-domain obstruction to strict-cycle descent. It is not a counterexample to the P3-factor conjecture. All graphs in the family have explicit P3-factors. Only the base graph is claimed Hamiltonian here.

## 1. Candidate theorem

For every integer q>=0 there is an explicitly defined finite simple cubic graph G_q on 42+6q vertices such that:

1. G_q is 3-vertex-connected, has girth six and has cyclic edge connectivity exactly five.
2. G_q has an explicit P3-factor.
3. There is a charged spanning forest of divergence 2 over F3 with exactly one defect, and neither nonzero circulation update on any simple cycle decreases its weight.

Consequently even cyclic edge connectivity five and the absence of cycles shorter than six do not validate the strict single-cycle descent rule. The homogeneous-layer lemma of `cycle-local-minimum-family.md` supplies the all-cycles proof. No numerical enumeration of cycles is asserted or required.

## 2. The thirteen-vertex block B

Use a leaf cycle on local vertices 0,...,8. Add four sources S_i, i=1,...,4, joining S_i to i and i+4. Its five ports are 0,S_1,S_2,S_3,S_4. All ports have internal degree two and all other vertices internal degree three. The block has seventeen edges.

Suppress the five ports. The resulting graph M is the eight-cycle on 1,...,8 with opposite chords i-(i+4), i=1,...,4. Thus B is obtained by subdividing all four chords and the edge 8-1 once. The unsubdivided edges form the path 1-2-...-8.

M is simple and 3-connected. Its opposite chords have a connected interlacement graph on its Hamiltonian cycle, so it has no two-edge cut; a two-edge cut would split the cycle into intervals with no crossing chord and disconnect that interlacement graph. Hamiltonicity rules out a bridge. A simple cubic 3-edge-connected graph is 3-vertex-connected, by the elementary vertex-cut argument used in the companion files.

M is triangle-free. It has only trivial three-edge cuts: a nontrivial cut would have an odd smaller side of order three, and the cubic cut count would require a triangle on that side. These are complete small-graph arguments, not catalogue assertions.

We need three exact block properties.

### 2.1 Two-edge cuts

B is 2-connected. Every two-edge cut in B separates exactly one port from the rest. Indeed if two deleted edges descend to distinct edges of M, M minus those two edges is connected and each subdividing vertex retains a connection to an endpoint. If both deleted edges descend to the same edge, they are the two halves of one subdivided edge and isolate just its port. The remaining graph is connected because deleting that one edge of M leaves it connected.

### 2.2 Port survival

After deleting at most two vertices in B, every remaining component contains a remaining port. This can also be seen directly from the leaf cycle and source ears. With two leaf deletions, every remaining leaf interval contains port 0 or a leaf attached to an undeleted source port. With one leaf and one source deletion, the remaining leaf path is connected and attaches all other surviving sources. With two source deletions the leaf cycle remains connected and contains port 0. An isolated remaining source is itself a port. These cases cover all deletions of size at most two.

### 2.3 A cyclic subset has completed boundary at least five

For C contained in V(B), let p(C) count its ports and put d(C)=|delta_B(C)|+p(C), its boundary when all ports receive one outside edge. If B[C] contains a cycle, then d(C)>=5.

For a proof, let A be the original M vertices in C. Comparing each subdivided edge with its original edge gives

    d(C) >= |delta_M(A)|+p(C).

There is an additional contribution of two whenever a port lies outside C and both endpoints of its original edge lie in A. Every cycle of B contains a port, because the unsubdivided edges form a path. Hence p(C)>=1 for the case at issue.

If A is nonempty and proper and is neither a singleton nor a seven-vertex set, its M boundary is at least four, and the inequality proves the assertion. A singleton A cannot support a cycle. If A has seven vertices, its M boundary is three. A boundary at most four would then require p(C)=1. Of the five subdivided edges, at least three have both endpoints in A, because each original M vertex meets at most two of those five edges. At least two of their ports would lie outside C, contributing four additional edges and contradicting d(C)<=4. If A contains all eight original vertices, each of the five subdivided edges contributes at least one completed boundary edge, so d(C)>=5. If A is empty there is no cycle. This proves the claim.

Internally B has girth six. Every square of M uses two opposite chords and both are subdivided; its other cycles are not shortened, and every five-cycle uses a subdivided chord. A six-cycle is supplied by S_1-1-2-S_2-6-5-S_1.

## 3. The forty-two-vertex base graph

Use core vertices a=0,b=1,c=2 and three disjoint copies U,V,W of B:

- U has leaves 3,...,11 and sources 12,13,14,15, paired with (4,8),(5,9),(6,10),(7,11).
- V has leaves 16,...,24 and sources 25,26,27,28, paired with (17,21),(18,22),(19,23),(20,24).
- W has leaves 29,...,37 and sources 38,39,40,41, paired with (30,34),(31,35),(32,36),(33,37).

Include the three leaf cycles and all listed source-leaf pairs. Add the twelve edges

    0-1, 2-1, 0-3, 2-16, 1-29,
    0-25, 2-13, 12-38, 14-40, 15-27, 26-39, 28-41.

There are 3*17+12=63 edges. Every vertex has degree three and the graph is simple.

Select

    0->3, 0->1, 2->16, 2->1, 1->29,

and the two outgoing edges at every block source. The selected support has 29 edges and one defect at 1. Its sources are 0,2 and the twelve block sources. The remaining leaves form the three nine-cycles, with exposed leaves 3,16,29 in different cycles. The unselected source edges are the last seven extra edges. Thus every hypothesis of the homogeneous-layer lemma holds, and no strictly decreasing simple-cycle update exists for this flow.

## 4. Frame and three-connectivity

Contract U,V,W. The six-vertex frame K contains K3,3 with parts {a,c,W} and {b,U,V}. It also has a second copy of U-W, a second copy of V-W, and the edge U-V. The core vertices have degree three and the hubs degree five. All incidences are attached to distinct ports.

The expanded graph is 3-vertex-connected. If two deletions lie in one block, the port-survival property joins every remaining component to the connected outside frame. If the deletions lie in different blocks, the block interiors remain connected and at most two frame edges are lost; K remains connected. If one deletion is a core vertex and one lies in a block, the frame minus that core vertex contains a bridgeless K2,3, so loss of at most one further incidence does not disconnect it. If both deletions are core vertices, the remaining frame is connected. Simplicity and cubicity were checked directly above.

For later use, the only frame cuts of size at most four isolate one core vertex or two adjacent core vertices. This follows by inspecting subsets of at most three vertices: a core star has boundary three, a hub star boundary five; a two-core adjacent set has boundary four, whereas any two-set involving a hub has boundary at least six. A three-set of core vertices, or of hubs, has boundary five; a mixed three-set has boundary at least seven. Complements give the other sets. Also, K minus one hub contains a bridgeless K2,3, and K minus two hubs is connected. The multiplicity between any pair of hubs is at most two.

## 5. Cyclic edge connectivity of the base graph

Suppose a cut has at most four edges and cycles on both sides. A split block contributes at least two internal cut edges, so at most two blocks can be split.

If no block is split, the frame cut description makes one side a single core vertex or an adjacent core pair. That side is acyclic, a contradiction.

Suppose exactly one block is split. If the outside is unsplit, the cyclic side lying inside the block would have completed boundary at most four, contrary to Section 2.3. If the outside is split, it contributes at least two edges because K minus that hub is bridgeless. The block therefore contributes exactly two, the outside exactly two, and no attachment crosses. Section 2.1 says that the block cut separates one port from its bulk. Contract the bulk back to its frame hub. The separated port's attachment becomes the one additional edge of a frame three-cut. Such a cut isolates a core vertex. In the expanded graph that side has only the core vertex and the separated port, joined by an edge, and is acyclic.

Suppose two blocks are split. They contribute exactly four edges and no other edge crosses. The outside frame is connected, so all outside vertices lie on one side. In each split block the portion on the opposite side is a single port or the bulk left after removing one port. A bulk contains four ports, all of whose attachments would have to go to the other split block. There are at most two frame edges between those hubs, so this is impossible. The separated side thus consists of two single ports and is acyclic.

Every case contradicts the assumed cyclic cut. Hence cyclic edge connectivity is at least five. The five edges leaving U separate its internal six-cycle from cycles in V and W, giving equality.

The base graph has girth six. Internal cycles were treated in Section 2. A projected two-edge cycle uses parallel hub edges and has two source-to-source block paths, each of length at least three. A projected triangle has three hubs and likewise has long internal paths. A projected four-cycle has at least one block and at least two internal edges in addition to its four frame edges. Longer projected cycles cannot produce a cycle shorter than six. The internal six-cycle remains present.

## 6. Explicit positive witness

The following is a Hamiltonian cycle of the base graph:

    0,1,
    29,37,41,33,32,40,36,35,34,38,30,31,39,
    26,18,17,25,21,22,23,27,19,20,28,24,16,
    2,
    13,5,4,12,8,9,10,14,6,7,15,11,3.

The final edge is 3-0. The list contains every vertex once and each consecutive pair is in Section 3. Partition this list, starting at 0, into consecutive triples to define a specific P3-factor F_0.

In W, this factor uses only the leaf-cycle edges between local positions 1-2 and 5-6. In particular, none of the four edges at local positions

    2-3, 4-5, 6-7, 8-0

belongs to F_0. In global labels these four unused edges are 31-32,33-34,35-36,37-29.

## 7. The six-vertex H expansion

The following operation is useful beyond this particular base. In a simple cubic graph choose four pairwise disjoint edges e_i=l_i r_i, i=0,...,3. Subdivide e_i by a new vertex A_i. Add new vertices X,Y and edges

    X-A_0, X-A_2, X-Y, Y-A_1, Y-A_3.

The six new vertices induce a tree H. The graph remains simple and cubic, and its order increases by six.

If the four old edges are unselected leaf-cycle edges of a homogeneous charged forest, select X->A_0,X->A_2,Y->A_1,Y->A_3 and leave all new remaining edges unselected. The leaf cycle gains four leaves, the source matching gains X-Y, and two ordinary P3 components are added. The single defect and the homogeneous-layer hypotheses persist.

If the four old edges are also unused in a supplied P3-factor F, that factor is preserved exactly: keep every old selected edge and add (A_0,X,A_2),(A_1,Y,A_3). This observation is the positive-witness invariant used below; no Hamiltonian lifting for the enlarged graphs is claimed.

## 8. Connectivity and the exact cut identity for H expansion

For any cut of the expanded graph, let P be its old vertices and T its new vertices on one side. Let beta count subdividing vertices A_i placed opposite both old endpoints of e_i, and let tau count crossing edges of the new tree H. Comparing each subdivided edge with its old edge gives the exact identity

    |delta_new(P union T)| = |delta_old(P)|+2 beta+tau.

If P is nonempty and proper and the old graph is 3-edge-connected, the new boundary is at least three. If one side has no old vertices, it induces a forest inside H; its boundary is 3|T|-2e_H(T)>=3 for nonempty T. Thus the new graph is 3-edge-connected, and being simple and cubic it is 3-vertex-connected.

Assume now that the old graph has cyclic edge connectivity at least five. A nonempty proper old cut of size at most four has a forest on one side. A forest on p vertices and c components in a cubic graph has boundary p+2c. Consequently that side is a single vertex with boundary three, or two adjacent vertices with boundary four.

For the adjacent pair, a new cut of size at most four would require beta=tau=0. The tree H is therefore wholly on one side. If it lies with the adjacent pair, beta=0 would require all four disjoint selected edges to have endpoints in that two-vertex set, impossible. Otherwise the pair remains acyclic.

For the single old vertex v, the identity requires beta=0 and tau<=1. If tau=0, placing H with v would require four disjoint edges incident with v, impossible; the other choice leaves a singleton. If tau=1, the new portion on v's side is one component of H minus one edge. Beta=0 and the disjointness of the old edges allow at most one A_i in this portion. The only such component is a single leaf A_i of H. The separated side then consists of v,A_i and is acyclic. A side with no old vertices is also acyclic because H is a tree.

Thus H expansion on four disjoint edges preserves cyclic edge connectivity at least five. This proof does not assume that ordinary 3-connectivity alone implies that stronger property.

## 9. Girth under the stated pairing restriction

Suppose the old graph has girth at least six, and no endpoint of e_0 is adjacent to an endpoint of e_2, and no endpoint of e_1 is adjacent to an endpoint of e_3. These restrictions concern the sibling pairs at X and Y.

A cycle using no new H edge is a subdivided old cycle and is not shortened. A cycle using one H path between two A_i has an internal path of length two for siblings or three for nonsiblings. Its outside path has two attachment edges and an old path between endpoints of distinct selected edges. That old path has length at least two for siblings by the restriction, and at least one for nonsiblings by disjointness. In either case the cycle has length at least six. A cycle using two disjoint H paths has four internal H edges and two outside paths of length at least three each, so is longer still. There are only four leaves in H, so these exhaust its possible nontrivial intersections with a simple cycle. Girth at least six is preserved.

## 10. Infinite iteration with exact witnesses

In the base graph choose the four unused W edges

    e_0=31-32, e_1=33-34, e_2=35-36, e_3=37-29.

They are disjoint. Pair e_0 with e_2 at X and e_1 with e_3 at Y. Their sibling endpoint sets have no adjacency: the only edges between charged leaves are the nine-cycle edges, and the displayed pairs are separated on that cycle.

Perform H expansion. At the next step choose l_i-A_i, where the fixed old endpoints are l_0=31,l_1=33,l_2=35,l_3=37 and A_i denotes the newest subdivision on that arm. Repeat the same sibling pairing, using fresh vertex names at every step. These four edges remain disjoint and unused by the recursively supplied factor. The sibling endpoint sets remain nonadjacent, since each insertion only lengthens the leaf cycle in those four fixed edge positions. The induced graph on charged leaves is still just that cycle.

After q expansions the order is 42+6q. The selected charged forest has 29+4q edges, equal to 2(42+6q)/3+1. The three leaf cycles have lengths 9,9,9+4q; their exposed exceptional leaves are unchanged. There is one defect and no strictly decreasing simple-cycle update by the homogeneous-layer lemma.

The old P3-factor F_0 and the two new P3s from each expansion give a complete explicit factor. Three-connectivity, girth at least six and cyclic edge connectivity at least five persist by Sections 8-9. The six-cycle in U and the five-edge cut around U are untouched, giving girth exactly six and cyclic edge connectivity exactly five.

## 11. Scope and next question

The family meets both of the cyclic-connectivity thresholds contemplated in the root research, yet remains an obstruction only to an unconditional strict-cycle repair step. It supplies neither a root counterexample nor a claim that neutral moves fail. The positive factors are explicit, and the all-cycles nondecrease assertion is structural rather than an unreported computation.

The next issue is the neutral plateau or the larger exchange core of these flows. The local defect-transport table and the connected difference-core theorem remain applicable. No proof of global termination, mathematical verifier receipt, EvidenceLink or Result is asserted in this file.
