# Analytic certificate for the eighteen-vertex matching spectrum

Verdict: `candidate_only`. Primary owner: `math-proof`.
Target: `obligation:opg46613-divisible-two-factor`.
This strengthens the auditability of C02; it does not change the ProblemContract or claim a new graph. The root remains open in repository truth. The proof below uses finite counting, not reported executable output.

## 1. The graph and its explicit P3-factor

Let P have vertices a_i,b_i for i in Z/5Z and edges a_i a_(i+1), a_i b_i, b_i b_(i+2). Let L have vertices 0,...,9, cycle edges i(i+1) modulo 10, and diameters i(i+5) for i=0,...,4. Form H by deleting a_0 and 0 and joining the three resulting terminal pairs a_1--1, a_4--9, b_0--5.

In the C02 numeric labeling, the first brick has vertices 0,...,8 and edges

```
01 05 12 16 23 27 38 46 47 57 58 68
```

The second brick has the path 9-10-11-12-13-14-15-16-17 and chords (9,14),(10,15),(11,16),(12,17). Joining edges are (0,9),(3,17),(4,13).

Six P3 paths are

```
(0,1,2), (4,7,5), (3,8,6),
(9,10,11), (12,13,14), (15,16,17).
```

Every consecutive pair is a displayed edge, and the six triples partition the eighteen vertices. Therefore this graph cannot be a counterexample to the original P3-factor assertion.

Both completed graphs P and L are simple cubic and 3-connected. For P one may use the C01 explicit Hamiltonian cycle after deleting a vertex, together with its vertex-transitive two-subset representation. For L, deleting one cycle vertex leaves a spanning path. For two deleted vertices, rotation and reversal reduce to deleted vertices 0,d with 1<=d<=5. When d=1 the remaining cycle vertices form a path. When 2<=d<=5, the surviving diameter 1--6 joins the two remaining cycle paths. Thus every deletion of at most two vertices leaves L connected. The vertex 3-sum deletion lemma proved in C01 applies, so H is simple, cubic, 3-connected and of order eighteen. H is triangle-free: neither brick contains a triangle, and a triangle cannot cross this cut, whose endpoints are distinct on each side.

## 2. The six perfect matchings of P

Let r be the number of spokes a_i b_i in a perfect matching. The other 5-r outer vertices must be paired by outer edges, so r is odd: r is 1,3, or 5.

If r=3, the two remaining indices must be adjacent modulo 5 for their outer vertices to match, but differ by 2 modulo 5 for their inner vertices to match. This is impossible. For r=5 the matching consists of all spokes. For r=1, choosing the spoke a_i b_i leaves one four-vertex path in each of the outer and inner five-cycles; both paths have unique perfect matchings. Hence there are exactly five one-spoke matchings and one all-spoke matching.

The all-spoke complement consists of two five-cycles. For the one-spoke matching with spoke a_0 b_0, the other edges are a_1 a_2, a_3 a_4, b_2 b_4, b_1 b_3, and the complementary cycles are

```
(a_0,a_1,b_1,b_4,a_4), (a_2,a_3,b_3,b_0,b_2).
```

Rotating indices covers all five one-spoke cases. Thus every 2-factor of P has spectrum (5,5).

Exactly two of these six matchings use each specified edge incident with a_0. The all-spoke matching and the one-spoke matching indexed by 0 use a_0 b_0. The one-spoke matchings indexed by 2 and 4 use a_0 a_1; those indexed by 1 and 3 use a_0 a_4. This explicit list avoids any additional edge-transitivity assumption.

## 3. The thirteen perfect matchings of L

Choose the set I of diameter indices used by a perfect matching, a subset of Z/5Z. If I is empty, the two alternating perfect matchings of the ten-cycle are the only possibilities.

Suppose I is nonempty. After removing the vertices covered by the selected diameters, every remaining matching edge must be a cycle edge. The uncovered vertices lie on disjoint cycle paths. A path has a perfect matching precisely when its number of vertices is even, and then that matching is unique. Equivalently, all cyclic distances between successive covered vertices must be odd.

The selected index pattern repeats after five steps around the ten-cycle. Thus the condition is precisely that the positive cyclic gaps between successive indices of I in Z/5Z are all odd. These gaps sum to 5. Their number r=|I| must therefore be odd. The possible gap patterns are:

- r=1: the single gap 5, giving five choices of the selected diameter;
- r=3: gaps 1,1,3, giving the five cyclic triples of consecutive indices;
- r=5: all gaps 1, giving one matching.

Together with the two r=0 matchings this gives exactly 2+5+5+1=13 perfect matchings.

For r=1, take diameter 0--5. The remaining matching edges are 1--2,3--4,6--7,8--9. Its complementary cycles are

```
(0,1,6,5,4,9), (2,3,8,7).
```

The five rotated matchings therefore all have spectrum (4,6).

For one r=0 matching, namely (0,1),(2,3),(4,5),(6,7),(8,9), the complement is the Hamiltonian cycle

```
(0,5,6,1,2,7,8,3,4,9).
```

Rotation gives the other r=0 case. For r=3, take diameters 0--5,1--6,2--7 and the cycle edges 3--4,8--9. The complement is the Hamiltonian cycle

```
(0,1,2,3,8,7,6,5,4,9).
```

Rotation covers all five r=3 cases. The r=5 matching leaves the original ten-cycle. Consequently eight of the thirteen complements are Hamiltonian and five have type (4,6).

Among the five type-(4,6) complements, the deleted vertex 0 lies on a four-cycle exactly twice and on a six-cycle exactly three times. Indeed rotation acts transitively on the ten vertices and permutes these five factors. There are 5*4=20 incidences of a vertex with one of their four-cycles, so every vertex has 20/10=2 such incidences.

## 4. Bijection of matchings across the three-edge cut

A 2-factor crosses every vertex cut in an even number of edges, because summing its degree two over one side gives an even integer. The joining cut of H has size three, so its intersection with a 2-factor has size zero or two.

It cannot be zero. The L-minus-0 brick is bipartite on nine vertices. Any internal 2-factor would partition these nine vertices into even cycles, which is impossible. Therefore every 2-factor crosses the cut twice, and the complementary perfect matching crosses it exactly once.

Restoring the deleted vertex in each brick, with its matched incident edge at the port selected by that single matching cut edge, yields a perfect matching of P and a perfect matching of L. Conversely, any such pair with corresponding matched ports restricts to a unique perfect matching of H. For each of the thirteen L matchings, its edge at 0 determines the port, and Section 2 supplies exactly two compatible P matchings. Hence H has exactly twenty-six perfect matchings. This is a bijection, not merely a lower bound.

Let ell be the length of the complementary L cycle through its vertex 0. The complementary P cycle through a_0 has length five. Deleting these two vertices and joining the resulting paths gives a cycle with (5-1)+(ell-1)=ell+3 vertices. The other P five-cycle remains internal, and any other L cycle remains internal. The exact spectrum table is therefore

| Complementary L cycle through 0 | Number of L matchings | Spectrum in H | Number of H matchings |
|---|---:|---|---:|
| ell=10 | 8 | (5,13) | 16 |
| ell=6 | 3 | (4,5,9) | 6 |
| ell=4 | 2 | (5,6,7) | 4 |

All twenty-six matchings are accounted for, and every complementary 2-factor contains an internal five-cycle. Thus no perfect matching of this explicit graph has all complementary cycle lengths divisible by three.

## 5. Scope

The graph and spectrum agree with C02; this artifact replaces the numerical spectrum count with an analytic derivation. The displayed P3-factor separates the failed strengthening from the original ProblemContract. This proof does not by itself establish minimum obstruction order; lower-order completeness and replay are separate C04 obligations. No canonical ledger, EvidenceLink or Result is modified.

Repository sources: C01 `proof.md` for the vertex 3-sum deletion lemma; C02 `proof.md` and `witness.json` for the existing graph and comparison. All counting and complementary cycles needed for the spectrum are supplied explicitly above.
