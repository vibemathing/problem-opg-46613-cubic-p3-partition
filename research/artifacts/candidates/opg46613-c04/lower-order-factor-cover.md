# A self-contained lower-order cover by four bad two-factor types

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-divisible-two-factor`.
This supplies a second finite-cover route for the lower-order question. It does not report execution of the accompanying enumeration, and does not promote the proposed minimum order to an admitted result.

## 1. Perfect-matching criterion, including a finite proof

For a finite graph H and S contained in V(H), write o(H-S) for the number of connected components of H-S having an odd number of vertices. The perfect-matching criterion is:

```
H has a perfect matching if and only if o(H-S) <= |S| for every S.
```

The statement is the classical Tutte criterion. A complete proof needed for this candidate is given here; no unquoted external implication is used.

Necessity follows because every odd component of H-S must have a matching edge to a distinct vertex of S.

For sufficiency, assume the inequalities and suppose H has no perfect matching. The inequality for S empty implies that |V(H)| is even. Add edges, without adding vertices, until an edge-maximal graph J without a perfect matching is reached. This is possible because there are finitely many missing edges. The inequalities persist when an edge is added: for any fixed S an added edge either leaves the components unchanged or merges two components; merging cannot increase their number of odd components.

We first show the following saturation property of J. If uv and vw are edges, uw is not an edge, and u,v,w are distinct, then v is adjacent to every other vertex. Suppose instead that vx is a missing edge. The four vertices u,v,w,x are distinct. By maximality, J+uw has a perfect matching M containing uw and J+vx has a perfect matching N containing vx. In the symmetric difference of M and N, these two exceptional edges lie on alternating even cycles.

If they lie on different cycles, flip M along the cycle containing uw. All N edges on that cycle belong to J, since vx is on a different cycle. This gives a perfect matching of J, a contradiction.

If they lie on the same alternating cycle, traverse it starting with the M edge u,w. Index its vertices 0,...,2t-1, with u at 0 and w at 1. Its N edges join odd indices to the following even indices, cyclically. If vx is traversed from v to x, v has an odd index. Use the existing edge uv instead. Deleting u and v from the cycle leaves two paths of even vertex order, each matched by consecutive path edges. Both exceptional edges have been removed, so these path edges and uv lie in J. If vx is traversed from x to v, v has an even index. Use wv instead; deleting w and v again leaves two even-order paths and removes both exceptional edges. In either case this matches all cycle vertices using only J edges. Use M outside this cycle to obtain a perfect matching of J, again a contradiction. This proves the saturation property.

Let S be the vertices of J adjacent to every other vertex. Every component of J-S is a clique. Otherwise, a shortest path between two nonadjacent vertices in one such component contains three consecutive vertices u,v,w with uv,vw edges and uw absent. The saturation property would put v in S, a contradiction.

If the number of odd clique components of J-S were at most |S|, match one vertex from each odd clique to a different vertex of S. Match the remaining vertices inside each clique. The number of unused vertices of S is even, because |V(J)| is even and the parities of the clique orders have already been accounted for. They can be matched inside the clique S. Thus J would have a perfect matching. Consequently o(J-S)>|S|, contradicting the inequalities that persist in J. Sufficiency follows.

The empty graph has the empty perfect matching and causes no exception to this proof.

## 2. Apply the criterion to the cubic domain

Let G be a finite simple cubic graph with edge connectivity at least three. For any S and any odd component C of G-S, degree counting gives

```
3|V(C)| = 2|E(C)| + |delta_G(C)|.
```

Thus its boundary has odd size. When S is nonempty, edge connectivity gives |delta_G(C)|>=3. When S is empty, the cubic graph has even order and is connected, so there are no odd components. Summing the boundaries of the odd components gives

```
3 o(G-S) <= 3|S|.
```

The criterion therefore produces a perfect matching M. Its complement is a spanning subgraph of degree two at every vertex, hence a disjoint union of simple cycles of length at least three.

A simple 3-vertex-connected cubic graph has edge connectivity at least three. To see this directly, an edge cut of size at most two cannot have a side of one vertex or two vertices: their boundaries have size three and at least four, respectively. Both sides would have at least three vertices. Deleting the at most two cut endpoints on one side then separates nonempty surviving vertex sets, contrary to 3-vertex-connectivity.

This supplies the perfect-matching existence input within finite graph reasoning, rather than assuming completeness of a graph generator or a Hamiltonian search.

## 3. Six vertices need no enumeration

The handshaking identity 3|V(G)|=2|E(G)| implies that the cubic order is even. Divisibility by three thus makes it a multiple of six. At order six, a simple 2-factor can only have cycle-length partition (6) or (3,3). Both are divisible-cycle factors. Hence no six-vertex graph in the specified domain is an obstruction to the strengthening.

The existence of a perfect matching, not merely an attempt to search for one, is essential to this argument and was proved in Section 2.

## 4. Exactly four bad two-factor types at order twelve

The partitions of twelve into integer parts at least three are

```
(12), (3,9), (4,8), (5,7), (6,6),
(3,3,6), (3,4,5), (4,4,4), (3,3,3,3).
```

Only four fail the requirement that every part be divisible by three:

```
(4,8), (5,7), (3,4,5), (4,4,4).
```

Fix, on labels 0,...,11, one disjoint cycle union F_t for each of these four ordered lists, putting its cycles on consecutive intervals. For each t enumerate every perfect matching M of the twelve labels that shares no edge with F_t. Form G=F_t union M. This graph is automatically finite, simple and cubic. Retain it for testing precisely when deletion of every set of at most two vertices leaves it connected.

Every possible twelve-vertex counterexample to the strengthening occurs, up to relabeling, in this finite family. Indeed Section 2 gives some perfect matching M_0 of such a graph. Its complementary factor F_0 must be bad, since a good factor would already settle that instance positively. Its cycle-length partition is one of the four listed types. Relabel the cycles and their cyclic vertices so that F_0 becomes the fixed F_t. Under the same relabeling M_0 is a matching included in the enumeration. No assumption that a graph has a particular distinguished matching is made.

Conversely, every retained union really is in the target finite domain. Thus checking a good complementary-factor witness for each retained union is sufficient. Repeated isomorphism classes are harmless and must not be silently pruned without a separate coverage proof.

## 5. Deterministic enumeration and its upper bound

Generate a matching recursively by taking the least unmatched label u and pairing it, in increasing order, with each other unmatched label v for which uv is not an edge of F_t. Recurse on the remaining labels. At each complete matching emit the union graph.

Every allowed matching is emitted exactly once: its partner of the least unmatched vertex uniquely selects the recursive branch at each stage. A complete graph on twelve labels has

```
11*9*7*5*3*1 = 10395
```

perfect matchings. The four types therefore generate at most 4*10395=41580 complete matching/cycle-union combinations, before edge exclusions and the connectivity filter. These are combinations with a specified complementary factor, not isomorphism-class counts.

For each retained union, a second complete matching recursion over its actual adjacency lists searches for a matching whose complementary cycles all have lengths divisible by three. Store the successful matching and the cycle lengths, or emit the exact union if no such matching exists. The recursive search is complete for the same least-unmatched-vertex reason. A negative result is a finite graph candidate requiring its own replay, not a source or tool error.

This cover is substantially smaller than the earlier 498960 BG construction traces at order twelve and has no BG theorem dependency. The two reductions can be used as different coverage audits. The number 41580 is a proved upper bound; it is not a reported run count, successful execution, or certificate that every retained graph passed.

## 6. Exact conclusion currently licensed by this artifact

The six-vertex case is settled by the supplied proof at candidate level. The twelve-vertex question is reduced to the stated complete, bounded family. The existing eighteen-vertex construction provides an upper bound on the minimum obstruction order. A global minimum of eighteen additionally requires that every retained twelve-vertex union in this new cover, or every case in the earlier complete BG cover, be positively checked with reproducible certificates and the required statement-faithfulness validation.

Both admitted obligations remain open in repository truth. This file neither edits canonical records nor reports a runtime or mathematical admission receipt.
