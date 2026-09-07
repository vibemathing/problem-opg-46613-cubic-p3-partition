# ROOT-TF-CORE-R01: exact gap-forest selection and a phase obstruction

Status: NONTERMINAL_CHECKPOINT. Verdict: candidate_only.
Primary owner: math-proof. Same web-candidate-generation trust domain.
Problem: problem:opg-46613-cubic-p3-partition.
Source/base: d1df88796cc753123f53796f8de5c9e89066e0cc.
Neither the root nor the legacy divisible-two-factor obligation is closed.

## 1. Frozen goal and shortest candidate dependency DAG

R: every finite simple 3-vertex-connected cubic graph of order 3k, k>0,
has a spanning subgraph with k components isomorphic to the two-edge path P3.
P3 is not required to be induced by the contract. In a triangle-free graph,
its endpoints cannot be adjacent, so every such P3 is automatically induced.
Cubicity gives even order; the eligible orders are precisely positive multiples
of six. No connectivity or modulus condition is dropped.

Local DAG labels below are document-local claims, not newly admitted IDs:

- B: the existing 45-vertex replacement proves candidate equivalence R <=> R_tf.
  Its fixed-object audit is already merged; trusted admission is still pending.
- L: the exact normal-form and gap-forest theorem in Sections 3-5.
- X: for every R_tf-domain G and every supplied perfect matching M, some
  S subset M satisfies all the gap-forest conditions. THIS IS OPEN.
- P: existence of a perfect matching when passing from the root domain to X
  must retain its standard bridgeless-cubic theorem dependency; L itself is
  conditional on an explicit supplied M and does not need that theorem.
- R_tf follows from P + X + L; R follows from R_tf + B.

This DAG is a research decomposition, not an admission or a rewrite of the
canonical graph. In particular its historical strengthening dependency is not
used. An alternative exact formulation of X is the all-retained specialization
of C07: a spanning forest of maximum degree two with every component order
positive and divisible by three. Such components are paths, and splitting each
path into consecutive triples gives a P3-factor. Conversely a P3-factor is
already such a forest. This equivalence does not prove forest existence.

R06's charged-flow space has divergence -1 in F3, n/3 centers, and
w=2n/3+b. Its existence does not imply b=0. R07 already gives triangle-free
one-defect strict-cycle minima; strict single-cycle descent is not retried.
Neutral movement or a multi-cycle exchange requires an additional global
argument. No such argument is silently supplied by the new fixed-M criterion.

## 2. Direct root-domain witness, not a new replacement cell

The complete sorted edge table and factor are in input.json. Let F consist of
cycles on 0..6, 7..24, and 25..35, in consecutive order, of lengths 7,18,11.
Add the following perfect matching M:

```
1-5 3-6 8-17 9-18 11-20 12-21 14-23 15-24
26-32 27-33 29-34 30-35
0-7 2-10 4-13 16-25 19-28 22-31
```

The first twelve edges are chords within individual F cycles. The last six
join distinct cycles; the simple skeleton of the cycle quotient is a path.
There are three parallel cross links on each of its two links. Keeping this
multiplicity and keeping the internal matching chords are distinct issues.

New code checks exactly 36 vertices and 54 different nonloop edges, all degrees
three, no triangle, and connectivity after all 667 deletions of at most two
vertices. This is one graph, not a graph-order census or a minimum-order claim.

A positive factor, with the middle entry the center, is

```
(1,0,6) (3,4,5) (2,10,9) (8,7,24)
(16,17,18) (13,14,15) (21,22,23) (12,11,20)
(19,28,27) (26,25,35) (29,30,31) (32,33,34).
```

Its selected M edges are 2-10, 11-20 and 19-28. Every path edge and the full
vertex partition are explicitly checked. The full host therefore is NOT a
root counterexample.

## 3. Exact fixed-matching cycle normal form

Let G be any finite simple cubic graph with a specified perfect matching M.
Its complementary spanning graph F is a disjoint union of simple cycles.
Fix a subset S of M that is to be used by a P3-factor, exactly.
Call every endpoint of an edge of S active. Each P3 contains at most one edge
of M, because its two edges meet at its center and M is a matching.

A P3 using e in S leaves, on the F cycles, a singleton at one endpoint of e
and a two-vertex consecutive pair centered at the other endpoint. Denote these
roles A and B, respectively. A P3 using no M edge is a consecutive triple on
one F cycle. Thus local pieces are A singletons, center-first B pairs, and
consecutive triples. Every selected M edge has one A end and one B end, even
when its ends are on the SAME F cycle. Internal matching chords are not erased.

Conversely such a full partition of every F cycle, respecting the A/B role
relation along every e in S, becomes a P3-factor by adjoining those e. Each B
pair acquires its A endpoint; internal triples remain untouched. Distinctness
and complete coverage follow from the local partitions and disjoint matching
ends. This proves both directions, for each specified S, without changing G.

## 4. Gap demands remove the orientation search

On a cycle with active vertices, list them in cyclic order. A gap runs from
one active vertex u to the next active vertex v, contains no other active
vertex, and has d>=1 cycle edges. When there is just one active vertex, the
gap goes around the whole cycle back to that same vertex and d is its length.
Set r=(d-1) mod 3 in {0,1,2}. Its d-1 internal vertices are inactive.

The B pair at u can consume the first internal gap vertex; the B pair at v
can consume the last. Let their indicators be alpha,beta in {0,1}. No other
piece crosses an active endpoint. The remaining gap is a path tiled by
triples, so d-1-alpha-beta is a nonnegative multiple of three. Since the sum
of indicators is at most two, this is equivalent to alpha+beta=r. For d=1,
r=0 and neither extension is allowed. For d=2, r=1 and exactly one extension
is allowed, so the one internal vertex cannot be used twice. For r=2 there
are at least two internal vertices and the two consumed vertices are distinct.

An edge e in S must supply exactly ONE extension: choose which of its two
endpoints is B and which adjacent gap receives its B pair. Its other endpoint
is A. This one-choice rule also forbids a port from extending in both directions.
Hence the remaining problem is an exact allocation: each selected matching
edge supplies one unit; each gap demands r units from its two adjacent active
endpoint incidences. A cycle without active vertices must have length divisible
by three, and then has exactly three internal P3 tilings.

An equivalent small bipartite demand-matching formulation has selected matching
edges as supply-one vertices and gaps as demand-r vertices. Incidences remember
which physical endpoint and which side of it is used; parallel incidences may
not be discarded. This is a polynomial finite test for a FIXED S, not a
polynomial root algorithm: selecting S is still open in the universal proof.

## 5. Exact gap-forest theorem

Construct a multigraph K_S whose vertices are the edges of S.
For a gap of demand one, add a labeled edge between the owners in S of its
bounding active endpoints. Loops and parallel edges are retained.
For a gap of demand two, put one forced mark on each bounding owner, counting
multiplicity; there is no K_S edge for this gap. Demand-zero gaps do nothing.
Let f(e) be the number of forced marks at vertex e of K_S.

THEOREM (candidate proof). G has a P3-factor using exactly S from M iff:

(i) every untouched F cycle has length divisible by three;
(ii) no K_S vertex has more than one forced mark;
(iii) every connected component of K_S is either a tree with exactly one forced
mark in total, or a unicyclic multigraph with no forced mark.
An isolated marked vertex is an allowed tree. A loop counts as one cycle and
a pair of parallel edges as a two-edge cycle.

Proof of necessity. Each demand-two gap consumes its owners' units immediately,
so f(e)<=1. A demand-one edge must be assigned to one of its two endpoint
incidences, using an owner's remaining unit. In a connected component with
v vertices, a edges and f forced marks, every owner must use one unit, giving
a=v-f. Connectedness gives a>=v-1. Nonnegative f therefore gives exactly the
two alternatives f=1,a=v-1 or f=0,a=v. These are a tree and a unicyclic
multigraph, respectively. Untouched cycles require (i).

Proof of sufficiency. In a tree component root at its uniquely marked vertex.
Assign each edge to its endpoint farther from the root. Each unmarked vertex
receives exactly its parent edge; the root already spends its unit on its
forced gap. In an unmarked unicyclic component choose one of the two directions
around its unique cycle and assign cycle edges to their arrival vertices.
Assign off-cycle tree edges away from the cycle. This uses each unit exactly
once. For a loop, the two directions mean its two distinct physical gap-end
incidences. Restore each incidence as a B pair in the indicated cycle gap.
Demand-two gaps already receive their two distinct end pieces. Every gap then
has a nonnegative multiple of three vertices left, tiled consecutively; (i)
handles untouched cycles. Section 3 gives the required global factor.

This construction is also an exact count: the number of factors with precisely
S is 2^u*3^z, where u is the number of unmarked unicyclic K_S components and z
is the number of untouched F cycles. Tree allocations are unique. Cycle
orientations give genuinely different B choices; untouched cycle phases give
three different selected path tilings. The restriction of a factor recovers
all these choices uniquely, proving no overcount. If any condition fails the
count is zero. This proof, not the finite test, supports the general formula.

The theorem applies to any supplied perfect matching, is weaker than requiring
all complementary cycles divisible by three, and does not claim a set S always
exists. It retains actual positions, gap lengths and internal matching edges.
No host reduction or induction on a noncubic graph is involved.

## 6. A synchronized-attachment obstruction

LEMMA. Suppose an induced chordless cycle C has length 3m and its only possible
outside incidences are at marked positions all congruent modulo three around C,
with at most one outside edge per marked vertex. No P3-factor of the ambient
graph can use any of these outside edges.

Proof. Let h>0 be the number of actually used outside incidences and list their
positions cyclically. Every gap distance is a positive multiple of three,
including the single-active-vertex case. Each gap therefore demands two
extensions, by Section 4. The h active vertices can supply at most h extensions
(each is A or B with at most one internal pair), whereas the h gaps require
2h. This contradiction proves the lemma. The empty-active case is not excluded.
The chordless and single-outside-edge hypotheses are essential.

Delete all twelve internal M chords from the fixed G to obtain G0. Its middle
18-cycle has external attachment positions 0,3,6,9,12,15, so the lemma forces
all six links to the other cycles unused in any hypothetical factor of G0.
The remaining sides have orders 7 and 11, neither divisible by three, and
cannot be covered internally. Thus G0 has no P3-factor. G0 has 42 edges and
is NOT cubic, so this is not a root counterexample.

It follows that erasing internal matching chords while retaining the cycle
quotient and total mod-three data is not a valid sufficient proof route.
Moreover every factor of G uses at least one M edge across each of its two
specified three-edge cuts. With at most two M edges in total it would use no
internal chord and would be a factor of G0. Thus at least three M edges are
needed. The explicit factor in Section 2 attains three. This proves the exact
minimum three without interpreting a search failure as a proof.

## 7. Three-edge-cut recursion: exact modulus audit

In a simple cubic 3-vertex-connected graph, every nontrivial three-edge cut
separating sides of more than one vertex is a matching. If two cut edges share
an endpoint v in one side, moving v across the cut leaves a cut of size at
most two; three shared edges disconnect that side without v. The boundary
lower bound of three excludes both. Each side is connected, since otherwise
its different components would require at least six crossing edges.

If one side has a vertices, 3a=2|E(side)|+3 gives a odd. Capping that side adds
one vertex. For total n=0 mod6, the two capped orders sum to n+2=2 mod6 and
are both even. Their residue pairs are precisely (0,2), (2,0), or (4,4), never
(0,0). Thus the unchanged zero-mod-six root induction cannot be applied to
both caps. The cap is simple and cubic; its cuts inherit the old cut lower
bound (take a side not containing the cap), and the elementary cubic cut-case
argument gives three-vertex-connectivity. Triangle-freeness additionally
requires pairwise nonadjacent ports; it is not silently inferred from the
uncapped side being triangle-free.

For the new witness all four caps actually are triangle-free and three-
vertex-connected, but their orders are 8/30 and 12/26. New deletion checks
cover 37/466 and 79/352 sets, respectively. The modulus obstruction persists
even in these favorable triangle-free cases. No one-way cap lifting is claimed
as a two-way root reduction; exact matching of boundary states would be an
additional obligation. Removing a short cycle or an ear likewise changes
boundary degrees and often the modulus. No unproved repair of these changes
is treated as a root-domain induction step.

A valid elementary positive subcase is worth separating: a connected graph
with a supplied complementary two-factor of at most two cycles, and total
order divisible by three, has a factor. One cycle is tiled directly. For two
cycles, either both lengths are divisible by three or their residues are 1,2.
In the latter case connectedness supplies a matching edge between them; use
an A singleton on the first cycle and a B pair on the second. The remaining
cycle paths have divisible-by-three orders. This proof gives a witness but
supplies no bound of two on the number of cycles in a general root graph.

## 8. New bounded executions and falsifiers

checker.py validates G, both cuts, all four caps, the positive factor and exact
minimum claim. Its centered-neighbor exact-cover branching emits complete
failure DAGs: 45 states for G0 nonexistence and 200 states for cost<=2 in G.
Each DAG stores a pivot for every failed residual mask/budget. The separate
consumer recomputes ALL possible triples through that pivot and checks that
every child is present. Vertex count drops by three, so it is a finite proof
object. Resource exhaustion is an error, never a negative certificate.

verify_certificates.py generates paths from unordered triples rather than
center-neighbor rows, checks connectivity by partition merging, validates both
DAGs and computes the complete factor-count polynomial by a separate residual
vertex recurrence. Neither program imports the other or any old verifier.
normal_form.py enumerates 7,177 matching-subset/orientation patterns at costs
0..3 and checks local gap tilings. gap_forest.py instead checks all 262,144
subsets of the fixed 18-edge M with the new multigraph theorem.

All four final runs exited zero with empty stderr. They agree on minimum cost
three and 76 factors at that cost. The complete cost polynomial is

```
0,0,0,76,304,694,1382,1588,1844,1490,1122,564,296
```

and its coefficients sum to 9,360. These are all factors of ONE fixed labeled
36-vertex graph, not all graphs of order 36 and not an asymptotic assertion.
Twelve altered graph/matching/factor inputs are rejected at semantic checks.
Two altered negative certificates with a required residual state removed are
rejected by the other implementation. No hash-only rejection is used.

execution.json records the actual Python version, source/input/output hashes,
start times, exit codes and bounded CPU/wall/memory/output settings. The final
four CPU caps are 25,20,30,25 seconds, outer wall caps ten seconds larger,
address space 512 MiB and each output 2 MiB. One worker and one thread are used.
The normal-form and subset searches also have internal deadlines; exact cover
has a 200,000-node cap. Reproduction: python3 -I -S run_bounded.py in this
candidate directory. Linux resource limits are required by that wrapper.

An early finite probe sampled one-defect completions. The archived
strict-cycle obstruction rules out using this probe for a universal inference. Its bounded sample is not used to support a descent theorem.
An exploratory parity calculation was also discarded: G has an even number
9,360 of factors, so an always-odd counting proof cannot work as stated.
These rejected ideas do not restart an admitted failed route or create an
original-domain nonexistence claim. Historical missing code/raw logs are not
recovered by the present new executions.

## 9. First open mathematical lemma and next atomic action

OPEN X: find, for every triangle-free simple 3-connected cubic root graph and
supplied M, a set S for which the gap multigraph satisfies (i)-(iii), or give
an eligible full graph with a complete no-factor certificate. The theorem
makes testing a proposed S easy; it does not prove any S exists. Full root
closure still needs X and the trusted bridge/faithfulness/admission steps.

Next atomic action: analyze an inclusion-minimal obstruction to this exact
allocation, retaining demand-two marks, loops and cyclic gap lengths. Test
whether exchanges of selected matching edges can repair every bad component
without assuming that a scalar residue sum is sufficient. If an exchange lemma
is proposed, freeze its hypotheses and attack it before using it to justify
termination. The old strictly decreasing simple-cycle rule and the newly
excluded internal-chord erasure rule must not be repeated.

The requested mathematical verifier/formalization work is described in the
companion request files. Current registered names have fixture scopes and no
accessible graph/proof-attestation workflow was found. This is a request,
not an attestation. No Lean elaboration, axiom report, EvidenceLink, Result or
Solution is supplied. All conclusions remain candidate_only. Research is
nonterminal; this checkpoint does not assert forced quota exhaustion.
