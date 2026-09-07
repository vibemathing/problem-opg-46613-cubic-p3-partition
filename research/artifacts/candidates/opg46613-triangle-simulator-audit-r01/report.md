# R03: audit of the 45-vertex triangle simulator

Status: RESULT_CANDIDATE_READY / triangle-free-reduction-audited.
Verdict: candidate_only. Primary owner: math-proof.
Repository: vibemathing/problem-opg-46613-cubic-p3-partition.
Source revision: db657865c432d10c6f57b6355f0ab17c42f57a09.
Source: research/artifacts/candidates/opg46613-root-r07/triangle-free-root-reduction.md,
Git blob 28fbdcd073b1216a1263d9a8ad5a7c6eedc5b6c4.
Companion root-equivalences.md was read for the three-sum definition, not assumed
as a proof of the root or of the deletion/edge-avoidance statements.

This is a newly executed, same-generation-domain audit, not a trusted-verifier
receipt. It does not recover missing historical programs or logs. No Lean
elaboration or axiom audit was performed. Original candidates remain unchanged.

## 1. Frozen theorem and dependency chain

Let R assert that every finite simple 3-vertex-connected cubic graph of order
3k, k>0, has a spanning subgraph consisting of k vertex-disjoint paths of length
two. These paths are selected, not necessarily induced. Let R_tf restrict the
same universal statement to triangle-free graphs.

Audited candidate: the explicit cell T below has exactly the ordered P3
interface of a triangle; its capped graph is simple cubic 3-vertex-connected;
replacing each of t triangles in a root-domain graph of order n gives a
triangle-free root-domain graph of order n+42t <= 15n with a P3-factor iff the
original has one. Consequently R iff R_tf. This proves neither R nor R_tf.

Dependency chain: frozen H data -> H properties and three Hamilton cycles ->
J certificates plus AAA exclusion -> T certificates plus BBB exclusion -> exact
interface equality -> arbitrary-outside gluing lemma -> capped connectivity and
triangle contraction checks -> finite sequence of host-preserving replacements.
Every nontrivial general implication is proved below, separately from testing.

## 2. Complete label conventions and finite graph checks

input.json contains every edge, not merely a graph name or opaque identifier.
H uses labels 0..17. Edges are the cycle (0,1,...,17,0) plus
(0,5),(1,8),(2,13),(3,10),(4,15),(6,11),(7,14),(9,16),(12,17).
Its neighbors of 0 are r0=1,r1=5,r2=17.

J uses labels 0..20: label 0 is a NEW vertex w, labels 1..17 are H-0,
and 18,19,20 are p0,p1,p2. Edges are those of H avoiding old 0 plus
(0,18),(0,19),(0,20),(1,18),(5,19),(17,20).
Jcap adds vertex 21 with edges to 18,19,20.

T uses left J on 0..20, right J with every label increased by 21, and
q0=42,q1=43,q2=44. Add (18+i,42+i),(39+i,42+i) for i=0,1,2.
Tcap adds vertex 45 with edges to 42,43,44.
The reference triangle has labels and ports 0,1,2 and its three edges.
The cap orders are 22 and 46; the 21-vertex J is not itself cubic at its ports.

Fresh results (ports have degree two; other vertices degree three):

|Graph|Vertices|Edges|Girth|All deletions of at most two vertices checked|
|---|---:|---:|---:|---:|
|H|18|27|6|172|
|J|21|30|6|not requested internally|
|Jcap|22|33|4|254|
|T|45|66|6|not requested internally|
|Tcap|46|69|6|1082|

All listed graphs except the triangle are bipartite in the computed coloring.
Only H's bipartiteness is needed. Simple/cubic/cap tests were recomputed from
edge lists using the new code, not inherited from the previous R07 audit.
That audit used a DIFFERENT eighteen-vertex graph and was not rerun.

### H: girth, interlacement and Hamilton certificates

All matching chords connect even to odd labels. Hence H is bipartite. Their
cyclic distances on (0,...,17) are 5,7,7,7,7,5,7,7,5, never three. A four-cycle
with one chord is therefore impossible. A four-cycle with two chords requires
a pairing of their endpoints into two consecutive cycle-edge pairs; checking
the 36 unordered pairs of listed chords excludes this. More than two matching
edges cannot occur in a four-cycle. The defining cycle alone has length 18.
The displayed cycle (0,1,2,3,4,5,0) has length six. Thus girth is exactly six.
The executable check separately computes shortest alternative paths for every
edge and obtains the same girth; no graph catalogue is used.

The three Hamilton cycles are exactly

    (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17)
    (0,1,8,7,14,15,4,3,2,13,12,17,16,9,10,11,6,5)
    (0,17,12,13,14,7,8,1,2,3,4,15,16,9,10,11,6,5).

Each has eighteen distinct labels and all its successive and closing edges
belong to H. At 0 they cover the three pairs {1,17},{1,5},{5,17}.

Name the nine listed chords A,B,C,D,E,F,G,I,J. The verified interlacements
AB,AC,AD,AE,BF,BG,CI,CJ form a spanning tree of their interlacement graph.
A nontrivial edge cut of a Hamiltonian graph meets its spanning cycle in a
positive even number of edges. A cut of size at most two must therefore consist
of two cycle edges and no chord. Each side is one nonempty cyclic interval.
Each vertex's matching partner stays on its side, so both intervals contain
chords. Chords in different intervals do not interlace; the interlacement graph
would disconnect. This proves that H has no cut of size below three.

For any simple cubic graph with no edge cut of size below three:
(1) a cut vertex would have to supply three edges to each of two components;
(2) two adjacent deleted vertices supply only four edges to components whose
boundaries each require three; (3) two nonadjacent deleted vertices supply six
edges, so exactly two components remain, each with boundary three. Each meets
both deleted vertices, since case (1) is excluded. One component C has two
edges to u and one to v. Then delta(C union {u}) has size 3+3-4=2. All cases
contradict the edge-cut bound. Orders are at least four, so this establishes
3-vertex-connectivity. The fresh 172-deletion enumeration is an additional
check of H, not a replacement for these general cut cases.

## 3. Exact meaning and exhaustive state classification

Each of the three ports is a distinct vertex with exactly one outside edge.
Orient selected P3 edges from center to leaf. State 0 means no outside edge is
selected. State A means a singleton port receives an outside center's edge.
State B means a port is the center of an internal pair and sends the remaining
selected edge to an outside leaf. Internal P3s cover all other cell vertices.
A P3 crossing twice may leave TWO A singletons if its center is outside; these
are both counted. A cell vertex cannot have two outside incidences, so there
is no omitted state with an internal center and two outside leaves.

With a A-ports and b B-ports, the exact identity is

    |cell| = 3*(number of internal P3s) + a + 2b.

For |cell| divisible by three and a+b<=3, the solutions are (a,b)=(0,0),
(3,0),(0,3),(1,1). Thus among all 27 ordered words in {0,A,B}^3 only
000, AAA, BBB and the six ordered permutations of 0AB can occur. The other
18 states have explicit nonzero residues in stdout.json. No port-symmetry
quotient is used.

|State|Triangle|J|T|
|---|---:|---:|---:|
|000|1|1|1|
|0AB|1|1|1|
|0BA|1|1|1|
|A0B|1|1|1|
|AAA|1|0|1|
|AB0|1|1|1|
|B0A|1|1|1|
|BA0|1|1|1|
|BBB|0|1|0|

All other 18 states are 0 for all three cells. This is an existence table,
not an enumeration of the number of all possible tilings. The new exact-cover
solver independently obtains it and saves a full cover for every 1 entry.
The complete certificate table in stdout.json, key interface_tables, lists every
singleton, oriented B pair and P3 for each positive ordered state.

### J positive states and the complete AAA impossibility certificate

Put A0=H-0 (not to be confused with a boundary-state letter). Deleting 0 from
the supplied Hamilton cycles yields Hamilton paths of A0 ending at each ri.
For each pair rj,rk, choose the cycle using both incident edges at 0 and delete
the consecutive triple rj,0,rk. The remainder is a spanning fifteen-vertex
path of A0-{rj,rk}. Cutting such a path into successive triples is a P3 cover.

For J state 000, use (pi,w,pj) and then the eighteen-vertex path pk followed
by the A0 Hamilton path starting at rk. For A at pi and B at pj, use singleton
pi and the pair (pj,w), and the same eighteen-vertex path through pk. For BBB,
use (pi,w),(pj,rj),(pk,rk) centered at the ports and tile the fifteen-vertex
path. These constructions work for every ORDERED distinct i,j,k.

For AAA all three ports are singleton blocks. Vertex w=0 is adjacent only to
those ports, so in the remaining graph w is isolated. No internal P3 can cover
it. This is a complete UNSAT certificate; it is not a search timeout.
For the reference triangle, BBB would need six distinct vertices in three
pairs but only three vertices exist. These two certificates plus residue cover
all false entries for J and the triangle.

## 4. T positive certificates and the BBB role audit

For 000 use J_left in BBB, completing its three B pairs by q0,q1,q2, and
J_right in 000. For AAA use all q as singleton blocks and tile both J copies
internally. For A at qi, B at qj, 0 at qk use J_left with A at pj, B at pk,
0 at pi. Select qj->pj and pk->qk; the former completes the outer B pair and
the latter completes an internal P3. Tile J_right in 000. All blocks are
vertex-disjoint and their selected incidences have the stated center roles.
The direct solver's certificates need not use these particular constructions;
both the explicit existence construction and each computed cover are audited.

For outer BBB each qi is already a CENTER using its outside edge. It must
select exactly one of its two internal neighbors, in left or right J. The
chosen edge is directed qi->pi. Hence the J-side port is A, not B. Each
unselected J-side port is 0. The port in J cannot be a center as well: a selected
P3 edge never joins two centers. Nor can qi select both J neighbors, which
would give it three selected incidences when its outer B edge is included.

There are exactly eight choices of side for the three qi. The resulting
ordered signatures are the complementary 0/A words:

    LLL: AAA / 000       LLR: AA0 / 00A
    LRL: A0A / 0A0       LRR: A00 / 0AA
    RLL: 0AA / A00       RLR: 0A0 / A0A
    RRL: 00A / AA0       RRR: 000 / AAA.

A nonempty 0/A signature on J has a A-ports and b=0. Its residue equation
forces a=3; that implication uses the order 21 and all three ports, not an
assumption about connectedness of its internal pieces. States with one or
two A-ports fail the residue check; AAA fails the isolated-w certificate.
Thus all eight choices are impossible. This excludes T BBB completely.
The new direct exact-cover check also exhausts the eight boundary-pair choices
and returns no cover, without importing the claimed signature table as a rule.
No leaking boundary state or direction reversal was found.

## 5. Capped connectivity and internal girth

For two disjoint simple cubic 3-connected graphs, remove one cap vertex on
each side and join their three distinct neighbors by a bijection. Simplicity
holds since all new edges run between disjoint sides with distinct endpoints;
every lost incidence is restored. To prove 3-connectivity after at most two
further vertex deletions D, first put all deletions on one side. Every component
on that uncapped side must contain a surviving cap neighbor: otherwise restoring
the cap could not connect it in the original 3-connected graph minus D. The
other uncapped side is connected and joins all those components. If there is
one deletion on each side, each side is its original graph minus at most two
vertices counting the cap, and is connected. At most two of the three disjoint
joining edges are destroyed; at least one survives. These cases also cover
zero or one further deletion. The three-sum lemma is therefore valid.

Jcap is the three-sum of H and K3,3: use parts {w,cap,u} and {p0,p1,p2},
remove u and H's vertex 0, and join pi to ri. Tcap is obtained from K3,3 on
parts {z,u1,u2},{q0,q1,q2} by replacing u1 and u2 by the uncapped J cells.
Apply the preceding lemma twice. Their exact finite deletion checks also pass.

Any J cycle not in A0 runs through w and two p ports. An A0 path between ri,rj
has length at least four, because it closes via ri-0-rj to a cycle of H.
Therefore such a new cycle has length at least eight. A0 contains the six-cycle
(6,7,8,9,10,11,6), so J has girth exactly six and its port distances are two.
A T cycle not in one J must switch sides through q. It uses at least two q
vertices, four attachment edges and a path between distinct ports in each J.
Its length is at least 4+2+2=8. A six-cycle in J survives. Distinct q terminals
are at distance four, attained through p_i,w,p_j in one J.
Do not confuse the capped J girth FOUR with the internal J girth SIX.

## 6. Arbitrary outside factors: both directions

Let C be either the triangle or T, with the prescribed three one-edge ports.
Restriction of an ambient P3-factor gives exactly the local pieces of Section 3.
Keep every selected edge wholly outside C and every selected cut edge, including
its center-to-leaf direction. Replace the internal partition by any certificate
for the SAME ordered state in the other cell. An A singleton is completed by its
original outside center. A B pair is completed by its original outside endpoint.
If one outside center had two cell endpoints, its two A incidences are both
preserved. All other pieces are internal P3s.

Thus every selected edge still joins a center of selected degree two to a leaf
of selected degree one, and no block overlaps or loses a vertex. Longer paths
and cycles cannot appear. This constructs the new factor in either direction.
No matching, complementary two-factor, induced-path constraint, or outside
factor-existence assumption is added. The finite checker additionally assembles
96 compatible state/port-bijection gluings of triangle or T against J and checks
every resulting P3 partition; the universal implication is the proof above.

## 7. All root-domain and termination checks

A root-domain cubic graph has even order by the degree sum and order divisible
by three, so n is a positive multiple of six, in particular n>=6. Its edge cuts
have size at least three: a side with one or two vertices has boundary at least
three or four by simplicity/cubicity. For a cut of size at most two both sides
therefore have at least three vertices. Deleting the at most two endpoints on
one side leaves vertices on both sides and separates them, contradicting
3-vertex-connectivity.

Contract ONE triangle and delete its three internal loops. The quotient Q is
loopless cubic, n-2>=4, and every cut of Q lifts to a cut of G. Hence Q is
3-edge-connected. Parallel edges between u,v would give delta({u,v})=6-2m<=2
for multiplicity m>=2; {u,v} is a nonempty proper subset since |Q|>=4. Thus Q
is simple. Apply the cubic cut-case proof above to get 3-vertex-connectivity.
This also proves that the three external neighbors of the original triangle
are distinct. Replace the contracted vertex by T using the three-sum with Tcap.
The replacement is simple cubic 3-connected and changes the order by +42.

Two triangles sharing only one vertex would give degree at least four. Two
sharing an edge form a diamond: the shared-edge endpoints have all three
neighbors inside it. If the two other diamond vertices are adjacent the entire
component is K4, impossible for a connected eligible graph. Otherwise deleting
those two vertices separates the shared-edge endpoints from a nonempty outside
(the order is at least six), contradicting 3-connectivity. So all t triangles
are vertex-disjoint, whence 3t<=n.

A simple cycle crossing the replaced cell uses exactly two of its three cut
edges, an internal path between distinct T terminals of length at least four,
and an outside path between distinct neighbors of length at least one. Its
length is at least seven. No new triangle is created, and triangles outside
the replaced one persist unchanged. Therefore the number of unconverted
original triangles decreases by exactly one per step. Induction on that finite
number (base t=0; the step uses the same proved host and interface lemmas)
terminates after t steps. The invariants are the host domain and factor
existence in both directions. Final order is n+42t<=15n and remains 0 mod 6.

The checker also executes two replacements in the triangular prism, checks
orders 6,48,90, checks every vertex deletion set of size at most two at each
stage, and verifies the explicitly carried 000-state factors. The final graph
has no triangle. This is a boundary control, not a census or induction proof.

If R_tf holds, transform any root graph as above, apply R_tf there, and compress
the factor in reverse order. This proves R. R implies R_tf by domain restriction.
A counterexample can therefore be transformed into a triangle-free counterexample,
but the transformation INCREASES order. It says nothing about a smallest
counterexample being triangle-free. Four- and five-cycles avoiding all triangles
may survive, and high cyclic edge-connectivity is not preserved.

## 8. Exact computation, mutations, reproducibility, and open admission

Run python3 run_bounded.py in this candidate directory, with a fresh output
directory name as its optional argument. It freezes resource limits before
launching one worker: python3 -I -S checker.py. The archived execution.json is
an actual new run, not a copy of old timings. The stdout contains all 81 state
decisions, 24 complete positive covers, negative residue and exact-cover outcomes,
eight BBB choices, 96 actual gluings, graph properties and the 15 mutation results.
Both fixed programs use only the standard library and import no old verifier.

For every state the solver removes A singletons, enumerates ALL injective B
neighbor choices, then lists every possible center with each unordered pair of
its remaining neighbors. Its exact-cover recursion branches over all rows that
cover a chosen uncovered vertex. A residual connected component with order not
0 mod 3 is impossible to tile and is soundly rejected. Every recursive step
removes exactly three vertices. All rejected branches are exhausted before a
false decision; positive decisions stop at one explicit cover and do NOT count
all covers. The deterministic 200000-node guard raises an error, never UNSAT.
The port-state enumeration and B choices are finite, and external time/memory
caps record resource failure rather than mathematical failure.

Fifteen mutations attack duplicate/deleted host edges, two Hamilton errors,
false interlacement, missing J/cap edges, repeated ports, false interface entries,
corrupted P3s, coverage omission, reversed B center, missing A, and forged J AAA
in the BBB elimination. All are rejected by semantic checks, not input hashes.
No probability or asymptotic heuristic is used; all port orders are retained.

First open assurance gap: a suitably scoped registered verifier must replay the
frozen finite package and separately audit the general gluing/domain proof.
research/verifiers.json registers fixture-policy identities but does not provide
a graph-proof verification workflow. The sole workflow is web-candidate-gate,
which validates transport and does not run this checker or Lean. The local
lean/lake/elan probe found no executable. No attestation or EvidenceLink is made.
admission-request.json records the request, user authorization, exact fingerprints,
capability mismatch/dispatch limitations and the prohibition on self-signing.
Even verification of this equivalence lemma would not prove R or close a root
Result/Solution. Both canonical obligations remain open, and the obsolete DAG
strengthening dependency is not used or edited. Historical missing originals
and pending C08 Lean remain explicitly unchanged.
