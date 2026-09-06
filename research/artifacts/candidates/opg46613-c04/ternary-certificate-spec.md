# Bounded ternary certificates for the remaining quotients

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-divisible-two-factor`.
This specifies a complete finite certificate system and proves its coverage. No negative table, exhaustive outer search or execution receipt is claimed to exist.

## 1. Fixed input and current range

Use a loopless quotient multigraph K on labels 0,...,n-1. Labels 0,...,8 are retained vertices and all other labels are hubs. Edges have stable integer indices; parallel edges are distinct indexed incidences. Orient each edge from its smaller endpoint to its larger endpoint.

The remaining range after the preceding proofs is

```
e = number of retained-to-retained edges in {6,7,8},
r_boundary = 27-2e,
1 <= p = n-9 <= floor(r_boundary/3).
```

Each retained vertex has degree three, each hub has degree at least three, no hub-to-hub edge is present, the retained induced graph is simple, and every nontrivial cut has size at least three. Consequently n<=14 and m=|E(K)|=27-e<=21.

Input validation can check the cut condition without assuming a flow or graph library: enumerate every proper subset containing label 0. This checks each unordered cut once, with at most 2^(14-1)-1=8191 cuts. Repeated endpoints are permitted only for retained-to-hub edges and are counted with multiplicity.

A reproducible encoding should record n and the sorted list of endpoint pairs, retaining duplicate pairs in consecutive slots. The slot indices then distinguish parallel edges. This is an exact labeled encoding, not a claim of graph-isomorphism canonicalization.

## 2. A bijective coordinate system for all divergence solutions

Prescribe b_v=-1 in F3 for retained vertices and b_v=0 for hubs. The total prescribed divergence is -9=0 in F3.

Choose a deterministic spanning tree T, for example by breadth-first traversal from label 0 with adjacency incidences scanned in edge-index order. List the non-tree edge indices in increasing order. Put

```
d = m-n+1 = 19-e-p <= 12.
```

Give the d non-tree edges arbitrary values a_0,...,a_(d-1) in F3 in their fixed orientations. At each vertex subtract their outgoing signed contributions from b_v, obtaining a residual demand q_v. The residual demands sum to zero.

Root T at 0. For a tree edge oriented from child w toward its parent, assign the value

```
sum_(v in subtree(w)) q_v in F3.
```

Negate it when converting to the input's fixed edge orientation. Telescoping proves the divergence equation at every non-root vertex; the zero total proves it at the root. Thus every non-tree assignment produces one full divergence solution.

The tree values are unique: subtract two solutions with the same non-tree values, remove leaves of T one at a time, and the zero divergence forces the incident tree-edge difference to be zero at every removal. Therefore the construction is a bijection between F3^d and all solutions of the prescribed divergence equations. It omits no flow and counts none twice.

## 3. Positive certificate

A positive certificate consists of one value x_j in {0,1,2} for each indexed edge j. Check:

1. Signed incidence sums equal b_v at every vertex.
2. At each retained vertex at least one of its three incident values is zero.

The second condition is exactly retained support degree at most two. The quotient-lifting theorem then supplies the local P3 construction, and the normalization theorem gives a bounded simple 3-connected cubic representative when needed.

The raw edge-value payload has at most twenty-one ternary symbols. The graph identity, chosen orientation and actual content digest must accompany it; no digest is supplied by guessing or by this specification.

## 4. Negative certificate as a complete rejection table

Index the coordinate assignments by integers j=0,...,3^d-1, with

```
a_i(j) = floor(j/3^i) mod 3.
```

This fixes the little-endian ternary coordinate order. A negative certificate is a byte string of exactly 3^d bytes. Its byte at position j is the ASCII digit for one retained label u in {0,...,8}.

For each j, reconstruct the complete divergence solution by Section 2. Check that all three indexed edge values incident with the indicated retained vertex u are nonzero. This certifies that this solution violates the retained support-degree condition. Reject an invalid digit, a wrong byte count, a wrong graph binding or a single false indicated violation.

If every table entry passes, every divergence solution has been rejected for an explicit local reason. By the coordinate bijection, no feasible quotient assignment exists. Conversely, if no feasible quotient assignment exists, each solution has at least one such retained vertex; choosing the least one yields a valid table. Thus this is a complete certificate format, not merely a heuristic obstruction list.

The table has at most

```
3^12 = 531441
```

bytes, below a one-MiB candidate-file limit even after keeping the small graph input separately. Verification can stream the table and reconstruct each flow with O(n+m) working storage. It does not need to trust a solver's internal search or keep every reconstructed flow in memory.

An interrupted or truncated table cannot be mistaken for a complete negative result because the exact length is checked against the input rank d. A timeout, missing table or failed reconstruction is a tool limitation, not a mathematical counterexample.

## 5. What a negative quotient would imply

For e=6,7,8, cycle normalization produces simple 3-connected cubic frames on twenty-four,twenty-two,twenty vertices. Replacing their unmarked vertices by the fixed Petersen bricks gives graphs on 144,126,108 vertices, respectively. The exact quotient theorem makes a valid negative rejection table a candidate nonexistence certificate for the corresponding P3-factor, conditional on full verification of the encoding, local signatures, normalization and table replay.

No such table has been produced or reported in this artifact. This is a specified verification path for an actual future finite witness, not a statement that the root assertion has a counterexample.

## 6. Outer coverage remains separate

Positive certificates for selected quotients do not prove all nine-retained cases. A complete outer enumeration must generate every retained simple graph of maximum degree three with e=6,7,8 and every partition of its remaining indexed degree slots into hubs of degree at least three, then apply only justified equivalences and filters. Symmetry reduction needs a separate coverage proof.

The endpoint-allocation and retained-P3-packing conditions can supply short positive witnesses before the full ternary test. Failure of either shortcut must continue to the full test rather than emit a negative table. This separation of input coverage, sufficient shortcuts and exact rejection certificates is mandatory for any later mathematical interpretation.

Both admitted obligations remain open in repository truth, and the entire specification remains candidate-only.
