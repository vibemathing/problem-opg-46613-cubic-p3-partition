# Six retained vertices and the five-internal-edge sufficient condition

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-divisible-two-factor`.
This refines the open parameter left by the marked-forest repair. No root closure, executable verification or novelty claim is asserted.

## 1. Setting and conclusions

Let Q be a finite simple cubic graph with edge connectivity at least three. Let U be a set of retained vertices and replace every vertex outside U by the fixed Petersen nine-vertex brick, using any bijections at the three ports. Write X(Q,V(Q) minus U) for the expanded graph.

Two candidate conclusions are proved below:

1. If |U| is divisible by three and Q[U] has at most five edges, then the expanded graph has a P3-factor.
2. If |U|=6, then the expanded graph has a P3-factor, with no restriction on Q[U].

Together with the already proved zero- and three-retained-vertex cases, every instance with at most six retained vertices and eligible order is covered by these constructive candidates. Nine retained vertices is the next uncovered parameter, not six.

Every simple 3-vertex-connected cubic frame satisfies the edge-connectivity hypothesis used here. Indeed a cut of size at most two cannot have a side with one or two vertices, since such a side in a simple cubic graph has at least three or four outgoing edges, respectively. Each side would thus have at least three vertices. Deleting the at most two cut endpoints on one side would disconnect nonempty sets on the two sides, contradicting 3-vertex-connectivity.

We use the pair-selection and partition lemmas fully proved in `independent-retained.md`, and the exact marked-forest transfer theorem fully proved in `p3-interface.md`.

## 2. Subdivide the edges between retained vertices

Put q=|E(Q[U])| and assume q<=5. Subdivide every edge of Q[U] exactly once, introducing a set W of q new vertices. Call the resulting graph Q'. The vertices of U now form an independent set in Q'. Their degrees remain three; each vertex of W has degree two; all other original vertices have degree three.

Let S'=V(Q') minus U. Its induced connected components consist of the original components of Q[V(Q) minus U] and the isolated subdivision vertices in W. For each u in U, form an indexed subset e_u of these component indices, recording which components contain its neighbors. The pair-tree partition criterion will be applied to this indexed family.

We need the following exact observation about cuts of Q'. Subdivision preserves connectedness and cannot create a bridge from a bridgeless graph. Moreover, every cut of size two in Q' separates a single subdivision vertex from all the other vertices. To prove the latter statement, delete two edges of Q'. If their original edges in Q are distinct, deleting those two original edges leaves Q connected by its edge-connectivity assumption. Every subdivision vertex on either affected edge still has a surviving connection to an original endpoint, so Q' also remains connected. If the two deleted edges belong to the same original edge, they must be the two halves of one subdivided edge. They isolate precisely its new vertex; the rest remains connected because deleting one original edge of Q leaves Q connected.

## 3. Check every partition

Take a partition of the S' components into r>=2 nonempty groups. For each group, collect all its S' vertices and all vertices of U whose entire Q' neighborhood lies in that group; call the resulting vertex sets A_1,...,A_r. Let Z be the remaining vertices of U, exactly the indices e_u crossing the partition.

As in the independent-set argument, no edges run between distinct A_i, and every edge incident with a vertex in Z runs to one of the A_i. Therefore

```
sum_i |delta_(Q')(A_i)| = 3|Z|.
```

Each A_i is a nonempty proper vertex set. By the cut observation, its boundary has at least three edges unless A_i is a single subdivision vertex or the complement of such a vertex. The complement case cannot occur for these particular A_i: if a subdivision vertex w lies outside A_i, its two original retained endpoints have a neighbor outside the associated S' group and consequently are not included in A_i either. Thus the complement of A_i cannot be just {w}.

At most q of the A_i can be singleton subdivision vertices. Writing s for the number that are, we obtain

```
3|Z| >= 3r-s >= 3r-q >= 3r-5.
```

Since |Z| is an integer, |Z|>=r-1. This holds for every partition, so the partition criterion provides a spanning pair-tree of the S' components using distinct indices in U. Lift that tree exactly as in `independent-retained.md`: expand each component to an internal spanning tree, subdivide selected pair-tree edges by their corresponding retained vertices, and attach all other retained vertices as leaves. The result is a spanning tree T' of Q' with degree at most two on U.

When there is only one S' component, the same construction is immediate: take its spanning tree and attach all retained vertices as leaves. If U is empty, the desired P3 conclusion already follows from the UUU brick tilings.

## 4. Return to the original frame

Every added subdivision vertex w has T'-degree one or two. Delete the degree-one subdivision vertices as leaves, and suppress each degree-two subdivision vertex, replacing its two-edge path by the corresponding original edge of Q. These operations preserve connectedness and acyclicity on the original vertices. They do not increase the degree of any retained vertex. There are no edges between subdivision vertices, so the operations do not create an unaccounted chain of added vertices.

Thus Q has a spanning tree T with degree at most two at every vertex of U. If |U| is divisible by three, its single component satisfies the exact marked-forest criterion, proving conclusion 1. The threshold five is a sufficient condition obtained from this counting argument; optimality of that threshold is not asserted.

## 5. Deleting any three-vertex path leaves the frame connected

Let A be three vertices that contain a P3 in Q. There are at least two edges within A, so cubicity gives

```
|delta_Q(A)| = 9-2|E(Q[A])| <= 5.
```

If Q-A had two or more components, each component would have at least three boundary edges in Q. All such edges go to A, so their total would be at least six, a contradiction. Hence Q-A is connected whenever it is nonempty. If the three vertices form a triangle, the boundary is three and the same argument applies.

This is a connectivity lemma only. It does not claim that Q-A remains cubic or 3-connected, and it does not assert a general P3-factor theorem for Q-A.

## 6. All six-retained-vertex cases

Now let |U|=6.

If Q[U] contains no P3, every vertex has internal degree at most one; otherwise a vertex and two of its neighbors would form a non-induced P3. Thus Q[U] is a matching together with isolated vertices and has at most three edges. Conclusion 1 applies.

Otherwise choose a P3 with vertex set A contained in U. Use its two edges as one forest component. By Section 5, Q-A is connected. In Q-A choose a minimal tree joining the three vertices of U minus A, deleting every unmarked leaf and unnecessary edge. Its leaves are among those three retained vertices. None of those retained vertices can have tree-degree at least three: three branches at such a vertex would require at least three other terminal leaves, but only two other retained vertices exist.

Consequently this tree has degree at most two on its three retained vertices. Together with the chosen P3 on A and the remaining isolated unmarked vertices, it forms a spanning forest of Q. Each nontrivial component contains exactly three retained vertices, and every retained vertex has degree at most two. Isolated unmarked vertices contain zero retained vertices. The exact marked-forest transfer theorem gives a P3-factor of the expanded graph.

The argument does not divide an arbitrary six-terminal support tree into two trees. It constructs the two components only in the case where an actual P3 among retained vertices is available and its deletion has been shown not to disconnect the frame. This avoids the auxiliary triple-splitting failure already recorded in `p3-interface.md`.

## 7. Resulting parameter restriction and remaining gap

For a counterexample to the P3 assertion within this specified Petersen-replacement family, the retained set must now have at least nine vertices, must contain at least six internal frame edges, and must evade the earlier path-contained and independent-retained positive criteria. These are candidate-derived restrictions, not an exhaustive classification and not a root Result.

When U is the entire vertex set of Q, the expanded graph is Q itself and the general marked-forest criterion contains the original problem. The present proof does not establish that general case. In particular, repeatedly deleting retained P3 paths is not justified by Section 5: after one deletion the residual graph need not have edge connectivity three, so the same cut bound cannot be reused without a new argument.

All proofs in this artifact are finite combinatorial deductions with explicit dependencies on the companion candidates. The two admitted obligations remain open in repository truth pending their prescribed verification and any trusted coordinator action.
