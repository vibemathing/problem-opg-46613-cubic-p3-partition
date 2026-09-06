# ROOT-R07: one-defect strict-cycle minima at every order 24+6q

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-root`, under the existing admitted Attempt/Route/Graph.
This is a counterexample family to a repair rule, not to the root. Every host graph below has an explicit P3-factor and a Hamiltonian cycle. No executable result or mathematical admission is asserted.

## 1. Exact candidate theorem

For every integer q>=0 there is a finite simple triangle-free 3-connected cubic graph G_q on 24+6q vertices, together with a charged spanning forest x_q, such that:

- divergence is 2 at every vertex over F3;
- exactly one vertex is a defect, and the weight is 2|V(G_q)|/3+1;
- neither of the two nonzero updates around any simple cycle strictly decreases the weight;
- one specified neutral six-cycle update followed by one specified decreasing seven-cycle update produces a P3-factor.

Thus even with one defect, 3-connectivity and triangle-freeness do not justify a strictly decreasing simple-cycle rule. The conclusion concerns all simple cycles of each displayed graph, not merely cycles inspected by a search.

The proof below gives a structural certificate for the universal cycle assertion, a twenty-four-vertex base graph, a six-vertex extension, and unchanged two-step repair cycles for the entire family.

## 2. A homogeneous-layer obstruction lemma

Consider a one-defect charged forest. Let S be its sources, L its leaves and b its unique defect. Write its exceptional component as

    a->a', a->b, c->c', c->b, b->d.

Assume the following additional structure in the ambient cubic graph:

(H1) Every unselected edge joins two sources or two leaves.
(H2) The graph on L is the disjoint union of three odd cycles, containing a', c', d in three different cycles.
(H3) Each ordinary P3 has both leaves in the same one of these three cycles.

The unselected source-to-source edges form a perfect matching of S. The virtual matching M on L, obtained by replacing every ordinary selected P3 by a typed matching edge between its leaves, is maximum in the auxiliary graph consisting of M and all actual leaf-to-leaf edges. Indeed each of the three components has odd order and exactly one of a',c',d unmatched by M. Each matching has at most (|L|-3)/2 edges, and M attains that bound. No auxiliary augmenting path joins two exposed leaves.

**Layer lemma.** Under (H1)-(H3), neither nonzero circulation update on any simple ambient cycle decreases the weight.

Here is a complete incidence proof, including cycles which revisit a forest component. Fix an orientation of a simple cycle. Let s be the number of source vertices on it, t the number of its unselected source-to-source edges, and z the number of its leaves at which both incident cycle edges are unselected. Let k be its number of unselected edges and Q its number of selected edges traversed backwards. A source contributes to Q precisely when the traversal arrives through a selected edge. Each of the t source-to-source edges accounts for exactly one arrival through an unselected edge. The only possible additional backward selected edge is d->b. Consequently

    Q=s-t+epsilon,

where epsilon=1 precisely when the cycle traverses d->b, and epsilon=0 otherwise.

Let h be the number of cycle edges between b and sources, and j the number between b and leaves. Counting selected incidences at sources gives 2s-2t incidences. Subtract h and add j to obtain the number of leaves incident with one selected cycle edge. Counting the unselected leaf incidences now gives

    k=s+z+(j-h)/2.

There are just three cases:

1. b is absent: h=j=epsilon=0, so k-Q=t+z>=0.
2. The cycle uses a-b and b-c: h=2,j=epsilon=0, so k-Q=t+z-1.
3. The cycle uses b-d and one of a-b,c-b: h=j=1, so k-Q=t+z-epsilon.

A negative value in either of the last two cases would force t=z=0. Then no source-to-source edge is used; every visited ordinary source uses both selected edges; and every visited leaf uses one selected and one unselected edge. The cycle meets the exceptional tree in exactly one path, between two of a',c',d. For example, if b-d is absent, d cannot lie elsewhere on the cycle, since its selected edge would be absent and z=0. If b-c is absent, neither c nor c' can appear elsewhere: c would need its two selected edges and c' would need its selected edge. The other cases are identical.

Outside that exceptional path, compress each ordinary selected P3 to its virtual edge. The resulting auxiliary path is an M-augmenting path between two different exposed leaves, contrary to the maximum-matching argument above. Therefore k-Q cannot be negative. Adding the unit circulation has weight change k-Q. Reversing the orientation proves the same for the other nonzero update. This proves the layer lemma without enumerating simple cycles.

## 3. The twenty-four-vertex graph

Use core vertices 0,1,2. For each base t in {3,10,17}, add a seven-vertex block on t,...,t+6 with edges

    (t+i)-(t+(i+1 mod 5)) for i=0,...,4,
    (t+5)-(t+1), (t+5)-(t+3),
    (t+6)-(t+2), (t+6)-(t+4).

The block has three ports t,t+5,t+6. Add the nine remaining edges

    0-1, 2-1, 0-3, 2-10, 1-17,
    0-15, 2-8, 9-22, 16-23.

All edges are unordered in the host. They give exactly 36 edges on 24 distinct vertices and every degree is three.

Select these seventeen directed edges:

    0->3, 0->1, 2->10, 2->1, 1->17,
    (t+5)->(t+1), (t+5)->(t+3),
    (t+6)->(t+2), (t+6)->(t+4) for t=3,10,17.

The unique defect is 1. The exceptional tree has (a,a',b,c,c',d)=(0,3,1,2,10,17); the remaining six components are ordinary P3s. The unselected source matching is

    {0-15,2-8,9-22,16-23}.

The leaves form the three displayed five-cycles. Each ordinary source has both leaves in its own block. Conditions (H1)-(H3) hold, so the layer lemma certifies that every simple cycle has nonnegative update cost in both directions.

### 3.1 Host connectivity, with no catalogue dependency

Cap a seven-vertex block by a new vertex adjacent to its three ports. On local labels 0,...,7, where 7 is the cap, this graph has Hamiltonian cycle

    (0,1,2,6,7,5,3,4)

and its remaining matching joins opposite positions on that cycle. It is the explicit eight-cycle with four opposite chords. Its chord interlacement graph is complete, so it has no two-edge cut: a cut of size two would split the Hamiltonian cycle into two intervals with no crossing chord, disconnecting the chord interlacement graph. It has no bridge by Hamiltonicity. Hence it is 3-edge-connected, and the elementary cubic argument in the companion proof gives 3-vertex-connectivity. The cap graph is simple and triangle-free by its displayed edges.

Before expansion the six-vertex frame is K3,3, with parts {0,2,V3} and {1,V1,V2}. Replace Vi by the seven-vertex block with base 3,10,17, respectively. The port attachments are exactly the nine extra edges above. This is three successive vertex 3-sums with the displayed eight-vertex cap graph.

For completeness, a vertex 3-sum of two simple 3-connected cubic graphs remains simple, cubic and 3-connected. Delete the chosen vertex in each graph and pair their three distinct neighbors across the sum. If at most two further deleted vertices lie on one side, each component on that side has a surviving attachment neighbor: restoring the removed vertex would otherwise leave that component disconnected in a graph with at most two vertices deleted. The opposite side is connected. If one further vertex is deleted on each side, both sides are connected, and at least one of the three disjoint attachment edges survives. These facts cover every deletion of at most two vertices. The attachments join distinct vertices in disjoint graphs, proving simplicity and cubicity as well.

The sum also remains triangle-free in this construction. Each side is triangle-free, and the three attachment edges form a matching, so a triangle cannot cross the cut.

### 3.2 An explicit Hamiltonian cycle and positive root witness

The base graph has the Hamiltonian cycle

    (0,1,2,8,4,3,7,6,5,9,22,18,17,21,20,19,23,16,12,13,14,10,11,15).

The final edge is 15-0. Each edge is listed in the construction. Consecutive triples give, for example,

    (0,1,2), (8,4,3), (7,6,5), (9,22,18),
    (17,21,20), (19,23,16), (12,13,14), (10,11,15).

Thus the host has a P3-factor, although the initial one-defect flow is a strict-cycle local minimum.

## 4. An exact neutral-then-decreasing escape

First add the unit circulation around

    N=(4,8,6,7,9,5).

Initially N has two selected forward edges, two selected reverse edges and two unselected edges. Its weight change is zero. The two affected ordinary P3s become

    6->8, 6->7, 5->9, 5->4.

All other selected arcs are unchanged. The exceptional six-vertex tree and its one defect persist.

Next add the unit circulation around

    D=(3,0,1,2,8,6,7).

In the updated flow this cycle has two unselected edges and three selected reverse edges, so its weight change is -1. The resulting factor is

    (0,1,17), (10,2,8), (6,7,3), (9,5,4),
    (11,15,13), (12,16,14), (18,22,20), (19,23,21).

Every vertex appears exactly once and every consecutive pair belongs to the host. This also audits the signs of both updates. The first update changes which vertices are sources: old sources 8,9 become leaves and old leaves 6,5 become sources. It makes previously excluded source-port routes available to the second update. Neutral updates are therefore substantive here, not merely rotations of an already feasible factor.

## 5. A six-vertex extension preserving the obstruction

Suppose a constructed graph has a selected Hamiltonian cycle H, an unselected source-to-source edge u-v of H, and an unselected leaf-to-leaf edge l-r of H. The four endpoints are distinct because sources and leaves are disjoint.

Delete u-v and l-r. Add six new vertices X,Y,A,B,C,D and the seven internal edges

    X-A, X-C, Y-B, Y-D, A-B, B-C, C-D.

Add four attachments

    u-X, v-Y, l-A, r-D.

Select X->A,X->C,Y->B,Y->D. Leave all new remaining edges unselected. This adds two ordinary P3 components, six vertices and nine host edges. The source matching replaces u-v by u-X and v-Y. The leaf cycle replaces l-r by l-A-B-C-D-r, increasing its length by four. Its parity and its unique exposed exceptional leaf are unchanged; both new virtual matching edges A-C and B-D remain inside that same leaf cycle. Thus (H1)-(H3), the one defect and the layer lemma all persist.

### 5.1 Three-connectivity of the extension

The six-vertex internal graph is K3,3 with two disjoint edges removed. It is 2-connected, as witnessed by the spanning cycle

    (X,A,B,Y,D,C).

Its four attachment ports are X,Y,A,D. After deleting at most two internal vertices, every remaining component contains a remaining port. A port-free component would be a subset of {B,C}. Isolating B or C alone requires deleting its three neighbors; isolating {B,C} requires deleting A,Y,D,X. Neither is possible with two deletions.

If two deleted vertices lie in the old graph, every component of the old graph after additionally removing u-v,l-r has a surviving attachment endpoint. Otherwise restoring those two edges could not reconnect it in the old graph with only those two vertices deleted. The intact new internal graph connects all these attachments.

If two deleted vertices lie in the new graph, the old graph minus u-v,l-r is connected by its 3-edge-connectivity. Every remaining new component has a port by the preceding paragraph and joins that connected old graph.

If one vertex is deleted on each side, the new internal graph remains connected. The old graph minus one vertex is 2-connected and in particular bridgeless. If at most one of u-v,l-r remains as an effective removed edge, the old remainder is connected. If both remain, every component created by their deletion has at least two of their surviving attachment endpoints: a boundary of just one would make that edge a bridge before the two edges were removed. At most one attachment is lost through deletion of the new vertex, so every old component still joins the connected new remainder. This covers the mixed case as well. The conclusions for fewer deletions follow by the same arguments. Simplicity and cubicity are immediate from the four distinct attachment endpoints.

The extension preserves triangle-freeness. Its internal graph is bipartite, the old graph has no triangle, and its four cut edges form a matching. A triangle crossing that cut is impossible.

### 5.2 Hamiltonian lifting

Removing the two chosen edges from H gives two disjoint spanning paths on the old vertices. The new internal graph supports both cross-pairings of its four ports by disjoint spanning paths:

    X-A and Y-B-C-D,
    X-C-D and Y-B-A.

Exactly one of these two cross-pairings joins the two old paths into a single cycle instead of closing them separately. Choose that pairing and all four attachment edges. This gives a Hamiltonian cycle of the enlarged graph. In particular it contains u-X and l-A, available for the next extension.

## 6. The complete infinite family and its fixed repair

Start with the base graph in Section 3, choose u=0,v=15,l=10,r=11, and use the displayed Hamiltonian cycle. At each subsequent step choose the newly created unselected edges 0-X and 10-A in place of the preceding selected pair of edges for extension. Give each step six fresh vertex labels. Both chosen edges belong to the lifted Hamiltonian cycle, and neither belongs to either fixed cycle N,D of Section 4.

After q steps the order is 24+6q. The graph is finite, simple, cubic, triangle-free and 3-connected. The initial charged support has one defect, while its three leaf cycles have lengths 5,5+4q,5. The layer lemma still rules out a strictly decreasing update around every simple cycle.

The cycles N and D are unchanged as graph edges and as local flow patterns. Apply the same neutral update N and then the same decreasing update D. The original twenty-four vertices acquire the eight P3s listed in Section 4. At every extension, the additional vertices retain their two selected P3s (A,X,C) and (B,Y,D). Thus a P3-factor is explicitly supplied for every member, separately from its Hamiltonian construction.

No assertion about all cubic graphs of these orders is involved: this is one explicitly defined family at each order.

## 7. A quantitative secondary-potential observation

In the homogeneous setting, an alternating cycle of virtual M edges and real leaf-cycle edges, contained in one leaf-cycle block, lifts to a neutral simple cycle on ordinary P3 components. Let R be its old source set and A its new source set after one of the two updates. Then |R|=|A|=r. No new source in A is adjacent to an unchanged source: before the update, all unselected edges were source-source or leaf-leaf, and each old leaf on this cycle had its unique selected source in R. Consequently

    e(S_new)-e(S_old) = -r + e(R) + e(A) <= 0.

Here e(R)<=r/2 because the old source edges are a matching, and e(A)<=r/2 because the new source edges are also a matching. If an old source in R has its source-matching partner outside R, the inequality is strict.

Such a neutral cycle with a strict secondary decrease exists in every 3-edge-connected homogeneous configuration satisfying (H2)-(H3). Take one leaf-cycle block together with all its ordinary sources. It has one selected edge to the exceptional tree. Its other boundary edges are source-matching edges, so 3-edge-connectivity forces an ordinary source whose partner lies outside the block. Delete the block's unique exposed leaf from its odd cycle and take the real perfect matching of the resulting even path. This real matching and the virtual matching M cover the same leaf vertices and are disjoint as typed edge sets. Their union decomposes into alternating cycles and every virtual edge occurs in one. The alternating cycle containing the selected external source's virtual edge has all its old sources inside the block and that source's partner outside, proving the strict decrease.

This proves a local escape for the lexicographic potential (weight,number of source-source edges) in this particular homogeneous class. It does not prove that this potential decreases in every nonoptimal charged forest, or that repeated lexicographic descent always reaches a factor. That general implication remains a separate root-level obligation.

## 8. Scope and next research obligation

The strict-cycle rule is invalidated within the exact root domain, including triangle-free hosts and a single initial defect. All hosts are positive P3 instances. The next question is the structure of neutral plateaux outside the homogeneous class, not another search for a divisible complementary 2-factor. In particular, a source-aware single-pass failure cannot be used as a root counterexample certificate.

The proof includes every input graph, update, boundary attachment and connectivity argument required for mathematical replay. Numerical enumeration is not needed for the all-cycles conclusion. It remains a natural-language candidate requiring the repository's prescribed verification and faithful linkage to the frozen root. No protected record is changed and no EvidenceLink or Result is created.
