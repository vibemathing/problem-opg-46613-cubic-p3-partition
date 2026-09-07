# ROOT-R07: two genuine global equivalents of the P3-factor root

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-root` under the existing admitted Attempt/Route/Graph.
These are equivalences of universally quantified statements, not a proof that any of them holds. The divisible-two-factor strengthening is not used. No novelty or external-theorem attribution is asserted by this self-contained proof; comparison with the exact Kelmans literature remains a source-faithfulness task.

## 1. The three statements

All graphs below are finite, simple, cubic and 3-vertex-connected. P3 means a selected two-edge path on three distinct vertices, not necessarily an induced path.

(R) Every such graph of order divisible by three has a P3-factor.

(D4) For every such graph H of order 4 modulo 6 and every vertex v of H, the graph H-v has a P3-factor.

(E) For every such graph G of order divisible by three and every edge e of G, the graph G-e has a P3-factor.

A cubic graph has even order, so the order domain in (R) and (E) is exactly the positive multiples of six. The candidate theorem is

    (R) if and only if (D4) if and only if (E).

The proof explicitly establishes R=>D4=>E=>R, including the graph-domain checks and the finite witness transformations for the contrapositive directions.

## 2. The vertex three-sum preserves the host domain

Take disjoint simple 3-connected cubic graphs A,B, remove one vertex from each, and pair their three distinct former neighbors by three edges. The sum is simple and cubic. It remains 3-connected.

If two further deleted vertices lie on one side, every surviving component on that side has a surviving attachment neighbor: otherwise restoring its removed cap vertex would not reconnect the graph with only those two further vertices deleted. The opposite uncapped side is connected and joins all these components. If one further vertex is deleted on each side, both uncapped sides remain connected because at most two vertices have been deleted in each original graph, counting its cap. At least one of the three disjoint attachment edges survives. These cases, and the same arguments with fewer deletions, prove the claim.

A repeated three-sum therefore stays within the host domain. This elementary argument is the only connectivity-preservation fact needed below.

## 3. A three-copy forcing construction

Let H have order 4 modulo 6 and choose a vertex v. Put A=H-v and label its three distinct terminals by 1,2,3. Each terminal has one external port, and |A| is divisible by three.

Start from K3,3, retaining one of its parts as three single hubs z_1,z_2,z_3. Replace each of the other three vertices by a copy of A, attaching terminal j of every copy to z_j. Call the result Y(A). It has

    |V(Y(A))| = 3|A|+3 = 3|V(H)|,

a multiple of six. It is simple, cubic and 3-connected by Section 2.

**Forcing lemma.** Every P3-factor of Y(A) restricts to a completely internal P3-factor in at least one copy of A.

To prove this, use the three-port local meanings 0,A,B: an unused external edge, an internal singleton terminal attached to an outside center, and an internal two-vertex segment centered at a terminal and completed by an outside leaf. Distinct terminals each have just one outside edge, so these possibilities exhaust restrictions of crossing P3 components.

For a copy of order divisible by three, one selected boundary edge is impossible by vertex counting. If two boundary edges are selected, one has type A and the other type B: the number of internal vertices in these pieces is 1+2, whereas two singleton pieces or two pair pieces have the wrong residue. Thus every copy not tiled entirely internally uses at least two boundary edges.

Suppose none is tiled internally. The three copies then use at least six boundary edges in total. Each single hub has selected degree at most two, so there are at most six. Equality holds: every copy uses exactly two edges, one entering and one leaving, and each hub has selected degree two. A degree-two vertex in a P3-factor is a center, so every selected hub edge is directed from the hub into its copy. No copy can have its required outgoing boundary edge. This contradiction proves the forcing lemma.

Assuming (R), Y(A) has a factor. The forcing lemma gives a factor of A=H-v, proving (D4). Equivalently, any counterexample (H,v) to (D4) produces a root counterexample Y(H-v) of order 3|H|. Only this implication about Y is asserted; the existence of an internal factor in A by itself is not claimed to construct a factor of Y without additional interface data.

## 4. From one-vertex deletion to arbitrary edge avoidance

Assume (D4). Let G have order n divisible by six and fix e=u p_0. Write the other neighbors of u as p_1,p_2.

Take K3,3 with parts {z,t_1,t_2} and {r_0,r_1,r_2}. Form H by removing u from G, removing z from this K3,3, and joining p_i to r_i for i=0,1,2. Section 2 makes H a simple 3-connected cubic graph, of order

    n-1+5 = n+4,

which is 4 modulo 6. Delete r_0. By (D4), H-r_0 has a P3-factor F.

Put A=G-u. In H-r_0 the only external edges of A are p_1 r_1 and p_2 r_2; the edge at p_0 is absent. Its order is n-1, hence 2 modulo 3. Restrict F to A. Every component meeting that boundary leaves an A singleton or a B pair as in Section 3, and there are at most two selected boundary edges. The residue equation has exactly these possibilities:

- one B pair and no A singleton;
- two A singletons and no B pair.

Zero selected boundary edges has the wrong residue; the other one- or two-edge combinations also have the wrong residue. The two boundary edges form a matching, so there is no hidden case with one internal vertex incident with two crossing edges.

In the one-pair case, restore u and use it as the outside endpoint completing that pair. In the two-singleton case, restore u as their center and join it to p_1 and p_2. Retain every internal P3 of A. In either case all vertices of G are covered and the edge u p_0 is unused. Thus G-e has a P3-factor, proving (E).

The construction also proves its contrapositive with exact size control. If (G,e) has no edge-avoiding factor, this H of order n+4 satisfies that H-r_0 has no factor. Combining with Section 3 yields a root counterexample of order 3n+12.

Finally (E)=>R is immediate: a cubic graph has an edge, and a factor avoiding that edge is still a factor of the graph. This completes all three implications.

## 5. What the equivalence does and does not say

(E) is stronger than the pointwise statement that a particular G has some P3-factor. The proof of edge avoidance uses the universal root statement on other graphs, through the order-4 deletion statement and the three-copy construction. It does not infer that a single supplied factor, or a finite successful test of one G, already proves avoidance of every edge in that G.

Similarly, (D4) is a different order-domain statement about deleting a specified vertex. Its equivalence is global and comes from explicit host-preserving reductions. Neither (D4) nor (E) is being silently used as a proved induction hypothesis for smaller graphs whose orders fall outside a verified range.

For finite-range use, root coverage through order N gives (D4) only when 3|H|<=N by this proof. The same argument gives edge avoidance for a graph of order n only when 3n+12<=N. These are sufficient range translations of this construction, not sharp bounds.

If a smallest root counterexample of order nu and a smallest order-4 deletion counterexample of order mu both exist, the constructions give

    nu <= 3 mu,    mu <= nu+4.

The inequalities are conditional statements about hypothetical minima, not claims that either kind of counterexample exists.

## 6. Research consequence

Unlike divisible complementary two-factors, these two reformulations have genuine root-level equivalence proofs. They provide alternative falsifiable targets: a specified vertex deletion in the 4-modulo-6 domain, or a specified forbidden edge in the 0-modulo-6 domain. An actual counterexample in either domain has an explicit route back to a root-domain counterexample, with all size and connectivity checks included.

The proof does not extend edge avoidance from one edge to an arbitrary matching of four edges. In particular, the H expansion used in the companion positive family was applied only to four edges already known to be unused by an explicit factor. That conditional witness-preservation statement is not an unconditional compression rule for a hypothetical minimal root counterexample.

The next task is to compare the exact quantifiers and constructions here with the relevant Kelmans statements, and to exploit the equivalents without treating them as already proved. Both canonical obligations remain open. No protected graph record, verifier receipt, EvidenceLink, Result or Solution is created by this candidate.
