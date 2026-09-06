# ROOT-R07: a girth-six triangle simulator and a triangle-free root reduction

Verdict: `candidate_only`. Primary owner: `math-proof`.
Problem: `problem:opg-46613-cubic-p3-partition`.
Attempt: `attempt:web-20260906-opg46613-a01`.
Route: `route:two-factor-divisible-cycles-v1`.
Graph: `graph:opg46613-initial-v1`.
Target: `obligation:opg46613-root`.
This is a self-contained proof candidate. No computation, novelty, external theorem attribution, verifier receipt or root admission is asserted.

## 1. Statements and the exact scope

There is an explicit 45-vertex three-terminal cell T with these properties:

- each terminal has internal degree two; all other vertices have degree three;
- the internal graph has girth six;
- adding one new vertex adjacent to the three terminals gives a simple 3-connected cubic graph;
- its ordered P3 boundary signatures are exactly those of a triangle.

Consequently, replacing any triangle in a root-domain graph by T, keeping its three external attachments, preserves P3-factor existence in both directions and adds 42 vertices. Replacing every triangle yields a triangle-free root-domain graph. If the original order is n, the new order is at most 15n.

Thus the universally quantified root statement is equivalent to its restriction to triangle-free graphs. This does not prove either statement. It also does not prove that a smallest-order counterexample is triangle-free: the operation enlarges, rather than shrinks, a counterexample. No reduction of all square- or pentagon-containing graphs to girth six is asserted.

## 2. Boundary convention

For a three-terminal cell whose terminals each receive one outside edge, use:

- 0: that outside edge is not selected;
- A: its terminal is an internal singleton, receiving an edge from an outside P3 center;
- B: its terminal is the center of an internal two-vertex pair, completed by an outside endpoint.

A realization partitions every cell vertex into internal P3s, A singletons and B pairs. Each terminal has at most one outside edge, so it cannot be the center of a P3 with two outside neighbors. Every restriction of a global P3-factor has the stated form. A P3 is a selected two-edge path; no induced-path requirement is imposed.

For a cell of order divisible by three, if a,b count A,B, then

    a+2b = 0 modulo 3,       a+b <= 3.

The only possible ordered signatures are 000, AAA, BBB, and six permutations of 0AB. A triangle realizes all of these except BBB: 000 is its internal P3, AAA its three singletons, and 0AB consists of one singleton and the pair on the other two vertices centered at the B terminal. BBB would require six vertices.

## 3. An explicit eighteen-vertex auxiliary graph

Let H have vertices 0,...,17. Its edges are the Hamiltonian cycle

    (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17)

and the matching

    0-5, 1-8, 2-13, 3-10, 4-15, 6-11, 7-14, 9-16, 12-17.

This is a complete specification of 27 distinct edges; H is simple and cubic. Every matching edge joins an even label to an odd label, so H is bipartite.

### 3.1 Girth and connectivity

There is no four-cycle. A square using one matching edge would require that edge to have cyclic distance three, and none does. A square using two matching edges would require the endpoints of one to be adjacent on the Hamiltonian cycle to the endpoints of the other, in one of the two pairings. Inspection of the nine displayed matching pairs excludes this. A square cannot use three matching edges, because matching edges cannot meet. Bipartiteness excludes triangles and pentagons. The cycle 0-1-2-3-4-5-0 has length six, so the girth is exactly six.

Here is a small connectivity certificate. Label the matching edges, in the displayed order, A,B,C,D,E,F,G,I,J. Two of these chords interlace when their endpoints alternate on the Hamiltonian cycle. The following eight interlacements form a spanning tree of the nine-chord interlacement graph:

    AB, AC, AD, AE, BF, BG, CI, CJ.

For example B=(1,8) interlaces F=(6,11), and C=(2,13) interlaces J=(12,17). Every listed relation is checked directly from the endpoints.

Hamiltonicity rules out a bridge. A two-edge cut would use exactly two Hamiltonian edges and no chord, separating the vertices into two nonempty cyclic intervals. Every vertex has a matching partner, so each interval would contain a chord. Chords lying wholly in different intervals cannot interlace, contradicting the displayed connected interlacement graph. Hence H is 3-edge-connected.

A simple cubic 3-edge-connected graph is 3-vertex-connected. A cut vertex would have to supply at least three boundary edges to each of two components. A two-vertex cut consisting of adjacent vertices would supply only four edges to at least two components. For a nonadjacent two-vertex cut, exactly two components would remain, each with three boundary edges, and each must meet both deleted vertices because there is no cut vertex. One component has two edges to one deleted vertex and one to the other; adjoining the former vertex to that component gives a two-edge cut. Each possibility is a contradiction. This proves the required host property.

### 3.2 All three incident-edge pairs at 0 occur on supplied Hamiltonian cycles

The neighbors of 0 are r_0=1, r_1=5, r_2=17. Besides the defining cycle, use

    (0,1,8,7,14,15,4,3,2,13,12,17,16,9,10,11,6,5),

and

    (0,17,12,13,14,7,8,1,2,3,4,15,16,9,10,11,6,5).

Each sequence contains all eighteen labels once and closes back to 0. Every consecutive pair is one of the displayed graph edges. The three cycles use, at 0, the pairs {1,17}, {1,5}, {17,5}, respectively.

Put A=H-0. For each i, A has a Hamiltonian path ending at r_i, obtained by deleting 0 from a cycle using 0-r_i. For each distinct j,k, the graph A-{r_j,r_k} has a spanning path on fifteen vertices: use the Hamiltonian cycle whose two edges at 0 lead to r_j,r_k and remove the three consecutive vertices r_j,0,r_k. Splitting this path into triples gives a P3-factor of A-{r_j,r_k}.

All of these paths are supplied by the three sequences; no general Hamiltonian assertion is imported.

## 4. A twenty-one-vertex source-polarity cell J

Take A=H-0 and four new vertices w,p_0,p_1,p_2. Add w-p_i and p_i-r_i for i=0,1,2. The terminals of J are p_0,p_1,p_2. It has 21 vertices, its three terminals have degree two, and all other vertices have degree three.

Its exact signature set is

    000, BBB, and all six permutations of 0AB,

with AAA absent.

For 000, choose distinct i,j,k. Use the P3 (p_i,w,p_j), and tile the remaining eighteen vertices by triples along the path obtained by putting p_k before a Hamiltonian path of A starting at r_k.

For A at p_i, B at p_j and 0 at p_k, use singleton p_i and the pair (p_j,w), centered at p_j. The same eighteen-vertex path through p_k and A supplies the remaining P3s.

For BBB, choose one i and let j,k be the other indices. Use the three pairs

    (p_i,w), (p_j,r_j), (p_k,r_k),

centered at their p terminals. Tile A-{r_j,r_k} by the fifteen-vertex path from Section 3.2. These pairs and paths cover all 21 vertices without overlap.

AAA is impossible because w is adjacent only to the three terminal singletons. Removing those singleton vertices from the internal cover isolates w. The congruence in Section 2 proves that no other signature can occur. The positive certificates cover every ordered choice, so no terminal-symmetry assumption is needed.

### 4.1 Internal girth and a 3-connected cap

Every cycle of J not contained in A passes through w and two different p vertices. It has length dist_A(r_i,r_j)+4. The same A path together with r_i-0-r_j is a cycle of H, so dist_A(r_i,r_j)>=4. Such a new cycle therefore has length at least eight. A has no cycle shorter than six and contains the six-cycle 6-7-8-9-10-11-6. Hence J has girth exactly six. Its distinct terminals have distance exactly two through w.

Add a cap v adjacent to all p_i. The result is the vertex three-sum of K3,3 and H, removing one vertex of K3,3 and vertex 0 of H. It is simple, cubic and 3-connected. To recall the finite proof of three-sum connectivity: after two additional deletions in one uncapped side, each surviving component has a surviving attachment neighbor, or restoring its cap would fail to reconnect the original graph with only those two vertices deleted. The opposite uncapped side is connected. With one deletion on each side, both sides are connected and at least one of the three disjoint joining edges survives. These arguments include fewer deletions. Distinct ports and disjoint vertex sets give simplicity and cubicity.

The cap may contain short cycles; the girth assertion concerns J itself. No cap-girth property is used for its substitution.

## 5. The forty-five-vertex triangle simulator T

Take two disjoint copies J_1,J_2 of J, with terminals p_i^1,p_i^2. Add three vertices q_0,q_1,q_2 and edges

    q_i-p_i^1, q_i-p_i^2  for i=0,1,2.

The terminals of T are q_0,q_1,q_2. Its order is 2*21+3=45. Its exact ordered signature set is

    000, AAA, and all six permutations of 0AB.

For 000, realize BBB in J_1, selecting its three outside edges toward the q vertices, and 000 in J_2. Each q vertex is an endpoint, and every B pair of J_1 is completed by its corresponding q vertex.

For AAA, leave the three q vertices as boundary singletons and tile J_1,J_2 using their 000 realizations.

For A at q_i, B at q_j and 0 at q_k, use the 0AB realization in J_1 with A at p_j^1 and B at p_k^1. Leave all boundaries of J_2 unused and tile it internally. Select the edge q_j-p_j^1, directed from q_j, and the edge p_k^1-q_k, directed toward q_k. The q_i vertex is the required singleton. The singleton p_j^1 together with q_j gives the required B pair centered at q_j. The B pair at p_k^1 is completed by q_k. Thus these are actual local P3 pieces with the required outer signature.

BBB is impossible. If all three q terminals are outer B centers, each must use exactly one internal edge toward one of the two J cells. Every selected attachment to a J cell would then enter that cell at an A terminal. Its signature would contain only 0 and A. For a zero-order-modulo-three cell such a nonempty signature would have to be AAA, but J excludes AAA. Neither J can receive any such selected edge, although the three q centers require three in total. This contradiction excludes BBB. Together with the residue classification, the list is exact.

The interface is identical to that of a triangle; it is not merely a set of sufficient states.

### 5.1 Girth, distances and a 3-connected cap

Any cycle inside one J cell has length at least six. A cycle using both cells must traverse at least two q vertices and has a path between different terminals inside each cell. Each such internal path has length at least two, and there are at least four q-to-cell edges. Its length is at least eight. There are no q-to-q edges and a q vertex has degree two internally, so these cases exhaust cycles of T. A six-cycle within J survives; the girth is exactly six. The distance between different terminals q_i,q_j is at least four, with equality through p_i^1,w_1,p_j^1.

Add a cap z adjacent to q_0,q_1,q_2. Start with K3,3 on parts {z,u_1,u_2} and {q_0,q_1,q_2}; replace u_1,u_2 by the two J cells. This is two successive vertex three-sums with the capped J graph. Section 4.1 proves that the resulting 46-vertex cap graph is simple, cubic and 3-connected.

## 6. Exact factor replacement in an arbitrary outside graph

Suppose a triangle is an induced three-terminal cell with exactly one external edge at each of its vertices. Restrict any P3-factor of the ambient graph to the triangle. Section 2 gives one of its eight possible signatures. Realize the same ordered signature in T and keep all selected edges outside the cell unchanged. Every A singleton and B pair is completed by the same external edge and role, and internal P3s tile the rest. This constructs a factor after replacement.

Conversely, restrict a factor of the replaced graph to T. Its signature is one of exactly the same eight states. Replace that internal realization by the corresponding triangle realization and keep the outside unchanged. This gives a factor of the original graph. In both directions, selected edges connect degree-two centers to degree-one endpoints, so no longer path or cycle is introduced. Extra unselected edges do not affect the argument.

This equivalence does not rely on a common cycle, a perfect matching, or the existence of a divisible-cycle two-factor. It applies to each particular outside factor, not merely to a chosen explicit witness.

## 7. Root-domain preservation and elimination of triangles

Let G be in the root domain. Its order is a multiple of six and at least six. Every nonempty proper edge cut has at least three edges: a cut of at most two cannot isolate one or two vertices in a simple cubic graph, and deleting its at most two endpoints on a larger side would contradict three-vertex-connectivity.

Contract one triangle to a single vertex, deleting only its internal loops. The result Q is loopless and cubic, of order |G|-2>=4, and each cut lifts to a cut of G with the same boundary. Thus Q is 3-edge-connected. It has no parallel edges: two vertices joined by at least two edges would form a two-edge cut or smaller. The cubic argument in Section 3 makes Q 3-vertex-connected. In particular, the three outside neighbors of the contracted triangle are distinct.

Replace that contracted vertex by T, using its 46-vertex cap graph in a three-sum. The result is simple, cubic and 3-connected. Its order is |G|+42, still divisible by six. Section 6 preserves factor existence in both directions.

Distinct triangles of G are vertex-disjoint. Sharing only one vertex would force degree at least four. Sharing an edge either gives an entire K4 component, outside the eligible order, or a diamond whose two other vertices form a vertex cut separating the shared edge from the rest. Both alternatives contradict the hypotheses here.

The replacement creates no triangle. T is triangle-free, and a cycle crossing its three external attachments uses at least two attachment edges, an internal path between different terminals of length at least four, and an outside path of positive length. Such a cycle cannot have length less than seven. Other old triangles remain disjoint and unchanged. Repeat on each original triangle, one at a time; the host-domain argument remains valid at every step.

If there were t triangles, the final order is n+42t. Disjointness gives t<=n/3 and hence n+42t<=15n. The final graph is triangle-free and has a P3-factor exactly when the original graph does.

Therefore a root counterexample, if one exists, gives a triangle-free root counterexample with explicit size bound 15n. A proof of the root restricted to triangle-free graphs would imply the unrestricted root by compression of the obtained factor. The other implication is restriction of the universal domain. This completes the claimed global equivalence.

## 8. Qualifications and the remaining root obligation

The construction does not imply that every minimal counterexample has no triangles, because its direction on orders is expansive. It also creates nontrivial three-edge cuts around replacement cells and does not preserve high cyclic edge connectivity.

No new square or pentagon is introduced. Any square or pentagon disjoint from the replaced triangle cells remains possible. Thus the final graph is not asserted to have girth six unless the original graph had no short cycle avoiding all its triangles. The internal simulator-girth statement must not be confused with a girth-six reduction for every root-domain graph.

This provides an exact, host-preserving alternative to unproved triangle contractions in a minimal-counterexample argument. The next research questions concern the remaining triangle-free configurations, neutral charged-flow plateaux, and exact source comparison with known Lambda-factor reductions. All claims remain candidate proof material; both canonical obligations remain open and no protected record is edited.
