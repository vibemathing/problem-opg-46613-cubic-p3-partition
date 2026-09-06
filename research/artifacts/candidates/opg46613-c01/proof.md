# C01: divisible-cycle implication and a 30-vertex obstruction to the stronger route

Status: `candidate_only`. Primary owner: `math-proof`.
Candidate: `candidate:opg46613-c01-obstruction-proof`.
Target: `obligation:opg46613-divisible-two-factor`.
Root retained open: `obligation:opg46613-root`.

## 1. Frozen statements and scope

The ProblemContract asks whether every finite simple 3-connected cubic graph G on 3k vertices, k a positive integer, has a spanning subgraph with k components isomorphic to P3. A P3 has three distinct vertices and exactly the two selected path edges; it need not be induced in G. The permitted axioms here are finite graph basics and finite combinatorics.

The stronger assertion S asks for a perfect matching M such that every cycle of the spanning 2-factor G-M has length divisible by 3. This candidate gives (i) a constructive proof of S(G) implying the root conclusion for G, and (ii) a specific graph H in the root domain for which S(H) fails but a P3-factor exists. It is not a negative answer to the ProblemContract. No minimum order or novelty claim is made.

Internal claim dependencies: C01.1 uses only cycle indexing; C01.2 uses the explicit Petersen presentation; C01.3 uses C01.2 and the vertex-sum argument; C01.4 uses C01.2 and cut-degree counting; C01.5 uses the explicit edge list only. These are proof components, not newly admitted Obligation IDs.

## 2. C01.1: the constructive implication

In a cubic graph, deleting a perfect matching leaves degree two at every vertex. A finite simple degree-two graph is a disjoint union of cycles, all of length at least three. Conversely the complement of a spanning 2-factor in a cubic graph is a perfect matching.

Suppose a spanning 2-factor F has cycles C_i of length 3m_i. Choose a cyclic ordering v(i,0),...,v(i,3m_i-1) of each C_i. For every 0 <= j < m_i retain exactly

    v(i,3j)--v(i,3j+1)--v(i,3j+2).

The triples partition each cycle's vertex set and different cycles have disjoint vertices. Every selected consecutive pair is an edge. Retain no other edges. Therefore the resulting spanning subgraph has exactly sum_i m_i = |V(G)|/3 components, each P3. For m_i=1, omit the third edge of the triangle. Ambient chords and matching edges are not selected and create no additional component edges. Cubicity and connectivity are unnecessary for this implication once F is given.

Handshake counting gives 3|V(G)|=2|E(G)|, so a cubic graph's order is even. Within the stated domain, divisibility by three is equivalent to divisibility by six; odd k instances are empty, not additional cases needing a construction.

## 3. C01.2: Petersen facts with elementary certificates

Let P have vertices a_i,b_i, i in Z/5Z, and edges

    a_i a_(i+1), a_i b_i, b_i b_(i+2).

These give a finite simple cubic graph of order 10. The list

    (a1,a2,a3,a4,b4,b2,b0,b3,b1)

is a Hamiltonian cycle in P-a0. Rotations i -> i+c and the map a_i -> b_(2i), b_i -> a_(2i) are automorphisms: outer steps 1 become inner steps 2, inner steps 2 become outer steps -1, and spokes become spokes. They act transitively on vertices. Hence P-v contains a spanning 9-cycle for every v. Deleting any second vertex leaves a spanning path, so deletion of at most two vertices preserves connectivity. Thus P is 3-connected.

We now classify every perfect matching N of P. Let s be its number of spokes. The 5-s remaining outer vertices must be paired by outer edges; hence s is odd and s is 1, 3, or 5. If s=3, the same two indices remain on both rings. They would have to differ by +/-1 for their outer edge and by +/-2 for their inner edge, impossible modulo 5. If s=5, N is the set of all spokes and P-N consists of the two 5-cycles.

If s=1, rotate so that a0b0 is the sole spoke. The two remaining ring graphs are 4-vertex paths, each with a unique perfect matching. Thus

    N = {a0b0, a1a2, a3a4, b2b4, b1b3}.

The complementary cycles are

    (a0,a1,b1,b4,a4),  (a2,a3,b3,b0,b2).

Rotating gives exactly five such matchings. Together with the all-spoke matching these are all six perfect matchings. Every 2-factor of P therefore has spectrum (5,5). Each edge incident to a0 lies in exactly two perfect matchings: a0b0 in the all-spoke and singleton-0 matchings; a0a1 in singleton-2 and singleton-4; a0a4 in singleton-1 and singleton-3.

## 4. C01.3: the graph H and its domain membership

Make three disjoint copies B_i of P-a0, i=0,1,2, with terminals a1^i,a4^i,b0^i. Add three mutually nonadjacent vertices z0,z1,z2. Add edges a1^i z0, a4^i z1, b0^i z2 for every i. This is the specialization Y(P,a0) of Kelmans's Y construction [K, Section 2, Figure 2]; the construction is attributed, not claimed new.

H has 3*9+3=30 vertices and 3*12+9=45 edges. Terminals acquire their missing third edge, other brick vertices retain degree three, and each z_j has one neighbor in each brick. All endpoints are distinct as prescribed, so H is simple and cubic.

For completeness, the connectivity preservation used here has the following proof. If A,B are simple cubic 3-connected graphs, delete vertices a,b and match their three distinct neighbors bijectively with new edges. Let S be a set of at most two remaining vertices. If S is wholly in A-a, B-b is connected. Every component of A-a-S contains a surviving neighbor of a: otherwise that component could not connect to a in A-S, contradicting 3-connectivity of A. Each such neighbor has its joining edge into the intact B-b. The case wholly in B-b is symmetric. If one vertex is deleted on each side, both remaining sides are connected (two deleted vertices in each original graph), and at most two of the three joining edges are lost. At least one survives and joins the sides. This exhausts S, proving 3-connectivity of the sum.

K3,3 is 3-connected: after deleting at most two vertices each part remains nonempty and all cross edges between surviving vertices remain. Replacing each vertex of one part successively by P-a0 is precisely the above vertex-sum operation and produces H. Therefore H is 3-connected. Its order is divisible by three, as required.

## 5. C01.4: every 2-factor of H has spectrum (5,5,5,15)

Let F be any spanning 2-factor of H. For a brick B_i let c_i be the number of F-edges leaving B_i. The degree sum within the brick is

    2*9 = 2|E(F[B_i])| + c_i.

Thus c_i is even. Its boundary has only three edges, so c_i is 0 or 2. Each of the three hubs has F-degree two; all its incident edges go to bricks. Consequently c_0+c_1+c_2=6, forcing c_i=2 for every i.

Restore a0 inside brick i and join it to the two terminals whose boundary edges lie in F. The selected internal edges together with these two restored edges are a spanning 2-factor of P: the two affected terminals regain degree two, the third terminal already has degree two internally, and all other vertices have degree two. By C01.2 this factor has two 5-cycles. Deleting a0 from the cycle containing it leaves a path on four vertices, while the other 5-cycle remains wholly within B_i.

Hence F contains three disjoint internal 5-cycles, one in each brick. To identify the remaining component, contract each four-vertex path to its replaced vertex of K3,3. Together with the three hubs and the six selected boundary edges the quotient is a spanning 2-factor of K3,3. Every cycle in a simple bipartite graph has length at least four, so a 2-factor on six vertices can only be a 6-cycle. Restoring the three four-vertex paths replaces three singleton vertices by twelve vertices and changes this length to 6+9=15. This proves the asserted complete spectrum.

Existence is not vacuous. Each of the six perfect matchings of K3,3 prescribes one unused boundary edge at every brick. By C01.2 each prescribed edge at a0 extends to exactly two Petersen perfect matchings; use their restrictions inside the brick. These choices are unconstrained between bricks and yield every perfect matching of H exactly once. Thus H has 6*2^3=48 perfect matchings. Each complement has the spectrum just proved. Since 5 is not divisible by three, none satisfies S.

## 6. C01.5: an explicit P3-factor of H

For machine-readable labeling use a_i=i and b_i=i+5 in P; in brick r, original label j in {1,...,9} maps to 9r+j-1. Set (z0,z1,z2)=(27,28,29). The internal edges in each brick, before adding 9r to both ends, are

    (0,1),(0,5),(1,2),(1,6),(2,3),(2,7),
    (3,8),(4,6),(4,7),(5,7),(5,8),(6,8).

Add (9r,27),(9r+3,28),(9r+4,29). The following ordered triples are paths, with middle entry the center:

    (0,1,2), (4,7,5), (3,8,6), (10,9,27), (12,11,16),
    (14,17,15), (13,29,22), (20,21,28), (18,23,25), (19,24,26).

Each of 0,...,29 appears once, and consecutive entries are adjacent according to the edge prescription. Retaining only those twenty edges is the required P3-factor. This is a concrete reason that the stronger-route obstruction does not contradict the root conclusion.

## 7. Checks, limitations, and next obligation

`witness.json` records the full edge list, this P3-factor, a sample perfect matching and its complementary cycles, and generator-side exact screening output. `screen30.py` constructs this one graph from the given Petersen definition, checks all 466 deletion sets of sizes 0,1,2, exhaustively enumerates perfect matchings, and finds a P3-factor by exact cover recursion. The observed count was 48, all spectra (5,5,5,15), with all deletion tests passing. This finite screening is not a verifier receipt and is unnecessary for the universal quantifier over matchings in C01.4, which is handled by the preceding case proof.

Reproduction from the repository root: `python3 research/artifacts/candidates/opg46613-c01/screen30.py`. The saved run used CPython 3.13.5, one process/thread, a 20-second deadline and CPU limit, 256 MiB address-space limit, and a 16 KiB output limit. No external package or network is used. The script prints JSON only; the repository CI does not execute it as mathematical verification.

The source comparison is `research/artifacts/source-notes/opg46613-c01-statements.md`. No exhaustive search over all graphs below 30 vertices was performed, and minimum obstruction order remains unknown here. No formal proof assistant, external mathematical review, EvidenceLink, or Result admission has been produced. The frozen root and target remain open in repository truth pending the required checks of the mathematics.

The failed-route proposal concerns only the universal assertion S. Do not continue trying to prove S unchanged. The next bounded tasks are to generalize the cut obstruction, eliminate triangle-expansion false leads constructively, and study a weaker path-factor transfer across the three-port bricks. These are follow-on candidates under the same admitted target, not self-created admissions.

[K] A. Kelmans, *Packing 3-vertex Paths In Cubic 3-connected Graphs*, arXiv:0910.2766v2 (25 July 2011), Section 2 and Theorem 3.1. https://arxiv.org/abs/0910.2766v2
