# A nine-vertex triangle cell preserving P3 feasibility and cycle divisibility

Verdict: `candidate_only`. Primary owner: `math-proof`.
Attempt: `attempt:web-20260906-opg46613-a01`.
Target: `obligation:opg46613-divisible-two-factor`.
This is a finite replacement lemma, not root closure or a verification receipt.

## 1. The fixed cell D

For i in Z/3Z take a triangle on a_i,b_i,c_i, and add the three edges b_i c_(i+1). The terminals are a_0,a_1,a_2. D has nine vertices, twelve internal edges, degree two at its terminals and degree three elsewhere. Each terminal receives exactly one external edge when inserted in a cubic graph.

Use the 0,A,B boundary meanings of the companion mixed-cell candidate: unused edge, singleton endpoint attached to an outside center, and internal pair centered at the terminal, respectively.

## 2. D has exactly the triangle's eight P3 signatures

The vertex-count congruence a+2b=0 modulo 3 restricts the possible signatures to 000, AAA, BBB and the six permutations of 0AB. The following give all signatures except BBB:

- 000: use the three internal P3s (a_i,b_i,c_i), one for each i.
- AAA: singleton a_0,a_1,a_2 and P3s (b_0,c_1,b_1), (c_2,b_2,c_0).
- A at a_0, B at a_1, 0 at a_2: singleton a_0, the pair (a_1,c_1) centered at a_1, and P3s (b_0,c_0,b_2), (a_2,c_2,b_1).

The rotation i -> i+1 and the reflection a_i -> a_(-i), b_i -> c_(-i), c_i -> b_(-i) preserve every edge of D and induce all permutations of its three terminals. Thus the last certificate realizes all six ordered 0AB states.

For BBB, each a_i must be paired to b_i or c_i, since those are its only internal neighbors. After deleting the three pairs, exactly one vertex remains in each small triangle. Each remaining vertex has at most one neighbor among the other two: it has only one edge leaving its own small triangle. The three remaining vertices therefore cannot form the one remaining P3. BBB is impossible.

Consequently D and a single triangle have exactly the same ordered P3 signatures. Replacing one by the other in any ambient graph with these three external edges preserves P3-factor existence in both directions: keep the restriction outside the cell and replace the local realization with one having the identical port states. This argument permits non-induced P3s and does not require the particular outside factor to follow a cycle.

## 3. Exact perfect-matching lifting multiplicity

Consider replacing a triangle in a cubic graph by D, keeping the ordered external attachments. In a perfect matching the number of selected external edges is odd, hence either one or three, for both cells. For each fixed outside matching, including its external-edge choices, there are exactly two extensions inside D and exactly one inside the original triangle.

To prove the count, look at the complementary 2-factor. At each of D's three small triangles it uses either zero or two of that small triangle's three external edges. With zero it uses the entire internal triangle. With two its internal edges are uniquely the spanning three-vertex path between the two corresponding ports. There is no alternative local component: the third vertex must have internal degree two.

If all three outer edges belong to the matching, none belongs to the factor. On the triangle of small-triangle indices, the used inter-triangle edges have degree zero or two at each index. The choices are precisely the empty set and the full three-cycle. These produce internal factor spectra (3,3,3) and (9), respectively.

If just one outer edge belongs to the matching, assume it is the edge at a_2. The factor uses the outer edges at a_0 and a_1. The inter-triangle support has degree one at indices 0 and 1, and degree zero or two at index 2. Its choices are precisely the direct edge 0-1 and the path 0-2-1. The direct choice gives a six-vertex path from a_0 to a_1 and a disjoint triangle at index 2. The indirect choice gives a nine-vertex path from a_0 to a_1. The local spanning paths are unique, proving exactly two extensions.

Compression sends both extensions to the unique matching of the original triangle with the same external-edge choices. It is therefore a two-to-one map on perfect matchings of the complete graphs. For h vertex-disjoint substituted triangles it is 2^h-to-one, since the internal choices are independent once the original matching and all boundary choices are fixed. This is an exact combinatorial count, not a numerical experiment.

## 4. Cycle-length residues and the stronger route

If the original triangle is a whole component of the complementary factor, its length three becomes either (3,3,3) or (9).

Otherwise it lies on a complementary cycle of length L crossing the cell boundary twice. The two lifted choices replace its three internal vertices by either six vertices with a separate internal triangle, or nine vertices. The new factor therefore has, in place of that cycle, either (L+3,3) or (L+6). All other cycle lengths are unchanged.

Every changed cycle retains its old residue modulo three, and all newly separated cycles have length divisible by three. Hence the replacement preserves existence of a divisible-cycle 2-factor in both directions. In fact every original perfect matching has two lifts with this property simultaneously, and every new perfect matching compresses as described.

This establishes a stronger local equivalence than the P9-to-triangle monotonicity in the companion candidate: the present D-to-triangle replacement preserves both P3-factor existence and divisible-factor existence. Do not transfer that two-factor assertion to the Petersen cell, whose obstructing internal cycles have a different behavior.

## 5. Domain preservation and a second minimal-counterexample exclusion

The cell D is obtained by replacing all three vertices of a triangle by triangles. Thus insertion of D in place of a triangle can be realized as three successive triangle expansions at distinct vertices. The companion candidate proves that triangle expansion preserves simplicity, cubicity and 3-connectivity. The operation adds six vertices and preserves the eligible congruence.

Conversely, suppose an eligible 3-connected cubic graph contains an induced D with exactly its three designated external edges. Contract D to one vertex. Its order decreases by eight; it remains a loopless cubic multigraph with at least four vertices and edge connectivity at least three, since every cut lifts to a cut of the original graph. The companion connectivity argument makes this contracted graph simple and 3-connected. Expand the contracted vertex to a triangle. The result is an eligible 3-connected cubic graph six vertices smaller.

By Section 2, the smaller graph has a P3-factor exactly when the original graph does. Thus a smallest-order root counterexample cannot contain this induced D configuration. The same configuration cannot occur in a smallest-order counterexample to the divisible-cycle strengthening, by Section 4. Neither statement claims the existence of a root counterexample.

Any sequence of these compressions terminates, since each removes six vertices. No uniqueness or confluence of the resulting reduced graph is asserted. Together with the companion P9 compression, this gives two sound local reductions for a hypothetical root counterexample; it does not claim that every cubic graph contains a reducible cell.

## 6. Audit scope

The proof uses only the displayed finite cell, explicit local P3 partitions, all three terminal permutations, the two possible factor patterns on the three-index triangle, and the companion connectivity lemmas. No search output, external verifier identity or admitted mathematical status is asserted. Required next checks are the local-signature exhaustiveness, two-to-one matching map, both directions of cycle-divisibility preservation, and statement-faithfulness of the minimal-counterexample corollaries.
