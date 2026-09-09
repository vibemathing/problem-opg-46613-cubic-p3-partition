# X3 eight-residue linkage: phase concentration and a genuine third-chord repair

Status: NONTERMINAL_CHECKPOINT. Verdict: candidate_only.
Primary owner: math-proof. Generation trust domain: web-candidate-generation.
Repository: vibemathing/problem-opg-46613-cubic-p3-partition.
Base: 21bda0987a3008c3fe22c63d79f0a8e339832c94.
No general X3, X2, root or trusted closure is claimed.

## 1. Frozen scope and exact remaining question

G is finite, simple, triangle-free, cubic and 3-vertex-connected. The supplied
perfect matching M has exactly three complementary cycles, each of order 2
modulo 3. Thus the total order is a positive multiple of six. P3 means a selected
two-edge path on three distinct vertices, without an induced-path requirement.
For a complementary circle C, B contains C and ALL its internal M chords Q.
P is the set of genuine ports whose M partners lie outside C. Gamma(B) joins
p,q in P when B-{p,q} admits a P3-factor. A relation edge is not an M edge.

PR28/29's full physical gap system and kappa=t+b+3u, PR30's cofactor gluing,
and PR31's four-chord/noncrossing results are reused with their candidate ceiling.
The current main already contains those packages. The supplied earlier crossing
archive is still a distinct untransported object: report SHA-256
88b66ba6dafb263d89cae8403aa3320d2398574b097015d39695abbff13d3735.
Its pair lemma is restated below to avoid a hidden dependency on undelivered
code. None of the old host enumerations or named controls is executed here.

The actual target is an escape from a hypothetical GLOBAL minimum kappa_*=3.
A positive value at a particular S in a positive host is not such a minimum.
We prove two conditional, arbitrary-size exclusions, and check new physical
exchanges. We do NOT prove that every remaining host meets either condition.

Local dependency DAG (not newly admitted registry IDs):
exact gap tiling -> pair filter / triple-link certificate;
clique endpoint induction -> phase-concentration cofactor theorem;
each local construction -> unchanged-host gluing or exact kappa=2 repair;
OPEN -> physical availability outside these two classes, then X2/root/closure.

## 2. The inherited eight types and their premise

For crossing chords ac,bd in cyclic order a,b,c,d, let A,B,C,D be positive
physical arc lengths, with residues alpha,beta,gamma,delta and total 2 mod3.
Using only the other chord, deletion of a,c is possible exactly when

 alpha+beta=1;
 or alpha+beta=0, alpha!=0, gamma=1;
 or alpha+beta=2, alpha=1, gamma!=0                         (modulo 3).

Indeed the two open circle paths have orders A+B-1 and C+D-1. Either both are
0 mod3, or the other chord must join a singleton A in a residue-one path to a
centered adjacent pair B in a residue-two path. On the former path its singleton
position is 0 mod3; on the latter its center position is 0 or 1 mod3. These
positions are A-1 and C-1. The remaining path pieces tile in consecutive triples,
including empty pieces. This proves the arbitrary-length statement, not just
its residue representatives. Rotate for deletion of b,d.

The failure set for BOTH deletions is exactly the rotations of 0002 and 0212:
0002,0020,0200,2000,0212,2120,1202,2021. Failure is only relative to this family.

When the OTHER two circles have an M edge g, a cofactor of B-{x,y}, for an
internal chord xy, gives a state of kappa=2: include xy, every M edge used by
that cofactor, and g. If h internal M edges are used in the cofactor, the local
unit graph has h+1 owners and h saturated demand units, hence one tree and
otherwise unicycles. The owner g carries two outside loop demands and has
rank one, contributing one excess unit. Thus globally s=D=h+2, nu=h+1,u=0.

Consequently the eight-type filter is necessary in every circle of a hypothetical
X3 TRIANGLE quotient. In a PATH quotient it is necessary for leaf circles, but
NOT automatically for the mixed middle circle, which has no opposite g. All
new theorems below state separately when they need this premise.

## 3. An unbounded theorem: all chord endpoints in one circular phase

Suppose C has order n=3m+2. Choose a cyclic labeling 0,...,n-1 in which EVERY
endpoint of Q has label 0 modulo 3. Q may have arbitrarily many crossing chords.
Then Gamma(B) is connected, by the following explicit construction.

If any multiple of three x is not a chord endpoint, it is a genuine port. Its
two circle neighbors are also ports, giving three consecutive ports. Adjacent
ports have a cofactor using the remaining circle path. For any other port p,
its three directed distances from these consecutive ports cover all residues,
so one has distance 1 modulo 3. Deleting that pair leaves two paths whose
orders are divisible by three. These edges give a connected terminal graph.
This also covers a triple straddling the cyclic labeling seam: use cyclic
distances, not linear subtraction without reduction.

Otherwise ALL m+1 multiples of three are matched internally. The ports are

 A_i=3i+1, B_i=3i+2  (0<=i<m), and z=3m+1.

Circle-only cofactor edges A_i--B_(m-1) for every i and A_0--B_i for i<m-1
connect all ports except z. Let 0--3j be the actual Q edge at 0, where 1<=j<=m.
For holes A_0=1 and z, take (0,3j,3j-1), centered at 3j. Tile the paths
2,...,3j-2 and 3j+1,...,3m in triples. Their orders are 3j-3 and 3m-3j. This
adds the relation edge z--A_0 and proves connectivity. Empty endpoint paths
are allowed. Every edge used is an actual circle edge or the actual chord at 0.
No other Q edge is deleted from B; it is merely unused by this cofactor.

The construction gives a spanning terminal tree with full positive cofactors
for any n and any Q satisfying the phase hypothesis. It does not require
triangle-freeness or host connectivity as hidden local assumptions.

### 3.1 A complete failure certificate for the internal-deletion subroute

In this SAME phase-concentrated family, NO internal chord xy has a cofactor
B-{x,y}, even when every other internal chord is allowed. To see this, suppose
a factor used h other Q edges. Its selected endpoints plus the two holes give
2h+2 marked vertices, all of phase zero. Exactly one circular marked gap crosses
the labeling seam and has arc residue 2; all others have residue 0. Their total
interior demand is

 D=2(2h+1)+1=4h+3.

Only h B extensions are available, one per selected chord. The equality D=h is
impossible for h>=0. Unselected chord endpoints remain ordinary circle vertices
in this argument; they were not erased. This is an all-subset analytic failure
certificate for a RESTRICTED repair family, not a full-graph UNSAT certificate.
The explicit terminal cofactors above coexist with it.

This identifies an important branch change: in a phase-concentrated core,
searching for a removable internal matching pair can never succeed. The terminal
pair construction, not an extra unproved internal-chord augmentation, supplies
the factor. It works in path quotients as well as triangle quotients.

## 4. Arbitrarily large 0002 cliques force the phase hypothesis

Assume k>=2 internal chords are pairwise crossing and EVERY pair has arc-residue
word a rotation of 0002. This refers to ALL internal chords of the block, not
an isolated clique subset with ignored surrounding endpoints. Then the 2k
successive endpoint gaps have exactly one residue 2 and all other residues 0.

Proof by induction on k. The case k=2 is the hypothesis. In a pairwise-crossing
matching, the endpoint word is a_1,...,a_k,b_1,...,b_k with pairs a_i b_i:
fix a chord, put one endpoint of every other chord on each of its arcs, and
pairwise crossing forces the same order in both halves. Thus paired endpoints
are antipodal in the endpoint word. Consecutive endpoints belong to distinct
chords, so each successive full-endpoint gap is one of the four pair gaps for
those two chords and has residue 0 or 2.

For k>=3 delete the two marks of any one chord from the ENDPOINT WORD, retaining
all actual vertices and lengths in the physical circle. The remaining k-1
chords still meet the hypothesis; their new endpoint gaps have no residue 1 by
induction. The two deleted marks are nonadjacent and each merges exactly two
old successive gaps. Two adjacent old residue-2 gaps would merge to residue 1.
Applying this to the chord at every mark proves there are no adjacent residue-2
gaps anywhere. For any such deletion, merging 0+0 or 0+2 preserves the NUMBER
of residue-2 gaps. The smaller word has exactly one, so the original word does
also. This proves the induction and terminates at k=2.

Start the labeling immediately after the unique residue-2 gap. Every chord
endpoint then has coordinate 0 mod3. Section3 constructs Gamma(B). Thus a mixed
circle whose whole chord set is this 0002 clique supplies a full host P3-factor
for ARBITRARY k and physical arc lengths. It excludes this X3 class without
an opposite-edge premise. A connected but non-complete interlacement graph,
or a clique containing a 0212 pair, is NOT covered by this theorem.

## 5. A genuine third-chord repair among the 0212 survivors

Let x0,...,x5 occur cyclically, with chords

 e0=x0-x2, e1=x1-x4, e2=x3-x5,

and successive arc residues (1,2,1,2,1,1). Each chord by itself fails the
circle-only internal deletion test. The two crossing pairs have words 1202
and 0212, so BOTH survive the old pair filter.

Nevertheless delete the central chord endpoints x1,x4. Choose x2 as B extending
toward its predecessor on the arc x1->x2, and x3 as B extending toward its
successor on x3->x4. The A endpoints are x0,x5. The special triples are

 (x0,x2, predecessor_C(x2)), (x5,x3, successor_C(x3)).

The six marked-gap interior demands are exactly (0,1,0,1,0,0). Each indicated
neighbor exists since the corresponding arc length is 2 mod3 and positive.
Subtracting these two consumed vertices leaves nonnegative multiples of three
in every gap; tile them consecutively. This is a complete arbitrary-length
cofactor construction using the other TWO chords, and permits arbitrary unused
additional chords in the unchanged block. With an opposite g, Section2 gives
s=D=4,nu=3,u=0,kappa=2. No intermediate single-edge descent is assumed.

### 5.1 Exact extent of this three-chord step

The finite symbolic audit considers every CONNECTED three-chord interlacement
diagram, all six arc residues of total 2, and retains exactly cases with no
circle-only removable chord and every crossing pair among the eight survivors.
There are 96 path-interlacement signatures and 24 triangle-interlacement
signatures: 120 total. For each possible deleted chord, its two remaining
chords each have five choices (unselected, or either end extending either way).
Every one of the 25 choices has its first violated physical gap recorded, or
is recorded as a valid complete role assignment.

Exactly SIX signatures permit a deletion; they are the rotations/reflections
of the above path pattern. Every one of their three chords can be deleted,
giving 18 positive deletion queries. The other 342 queries fail within these
three selected chords. In particular all 24 clique signatures still fail the
internal-deletion test. This is not a certificate against using a fourth chord
or against terminal cofactors. The concrete representatives use arc lengths
r+3, so are simple and triangle-free; a separate unordered-triple exact-cover
consumer agrees on every query. The general length claim follows instead from
the proved marked-gap restriction/tiling correspondence, not representative
size. Disconnected three-chord diagrams are outside this declared census.

## 6. Two NEW complete hosts and exact simultaneous accounting

No old named control graph is replayed. Each host is specified by its circle
orders and ALL matching edges; the certificate also lists its whole edge set.
All graph properties and spanning factors are checked on these new objects.

### 6.1 T30: third-chord chain, triangle quotient, strict 3->2

Circles are 0..13,14..21,22..29. M is
(0,5),(2,8),(6,11),(7,10),(9,12),
(1,14),(3,22),(4,25),(13,28),
(15,18),(16,21),(17,23),(19,26),(20,29),(24,27).
The first circle has five internal chords. None is circle-removable, and all
its crossing pairs survive the eight-type test. Its chain (6,11),(7,10),(9,12)
is the new third-chord motif. Delete9,12 and use the local cofactor

 (11,6,5),(10,7,8),(13,0,1),(2,3,4).

The opposite edge is17-23. Exchange old S={(1,14),(3,22)} for
S'={(6,11),(7,10),(9,12),(17,23)}. In the middle circle the new active order
is6,7,9,10,11,12 and its demands are0,1,0,0,0,1. There are two outside loop
demands. The new state has a supply-surplus tree and one excess-demand component,
so kappa=2. The separately saved full host factor is NOT attributed to this S';
new_factor is null. T30 is positive, not an X3 or root counterexample.

### 6.2 U54: opposite edge ABSENT, unbounded phase theorem, strict 3->0

Circles are0..28,29..39,40..53. The first circle has all five internal chords
(0,15),(3,18),(6,21),(9,24),(12,27), pairwise crossing, all of type0002.
Its sorted ports are1,2,4,5,7,8,10,11,13,14,16,17,19,20,22,23,25,26,28.
The first nine connect in order to30,31,32,33,35,36,37,38,39; the last ten
connect in order to41,42,43,44,47,48,49,50,52,53. Remaining internal M edges
are(29,34),(40,45),(46,51). These formulas specify the whole27-edge matching.
There is NO edge of M between the second and third circles: the quotient is
a path. The local pair1,28 has cofactor

 (0,15,14),(2,3,4),(5,6,7),(8,9,10),(11,12,13),
 (16,17,18),(19,20,21),(22,23,24),(25,26,27).

Add cross triples(1,30,31),(28,53,40); remaining outside triples are
(32,33,34),(35,36,37),(38,39,29),
(41,42,43),(44,45,46),(47,48,49),(50,51,52).
This is a full18-path factor. Old S={(1,30),(28,53)} changes to S plus(0,15).
The central new active order is0,1,15,28, with demands0,1,0,0; outside demands
are one each. Roles at the terminal endpoint are B15->14,B30->31,B53->40,
with the matched A ends0,1,28. No opposite edge has been smuggled into the proof.

### 6.3 Full physical-gap losses, not additive insertions

A retained old matched demand requires identical circle, whole gap path, owner
pair and unit label, plus the surviving assigned owner. Both old matches in
both records are deliberately fixed on the changed middle gaps, and neither
survives. The consumer checks this choice is maximum, then replays each new
alternating augmentation on the NEW demand graph.

|host|old(s,D,nu,u,kappa)|new(s,D,nu,u,kappa)|Delta s|Delta D|loss|augment|margin|
|---|---|---|---:|---:|---:|---:|---:|
|T30|(2,5,2,0,3)|(4,4,3,0,2)|2|-1|2|3|1|
|U54|(2,5,2,0,3)|(3,3,3,0,0)|1|-2|2|3|3|

Margin=2(a-loss)-Delta s-Delta D-3Delta u is positive. Equality holds in the
potential accounting because both new matchings are maximum. Every active
order, gap, A/B flag and loss is regenerated, not inferred from edge counts.
Neither host is a claimed minimum counterexample. Both have full positive
factors, so no complete no-P3 certificate or positive global minimum is claimed.

## 7. Actual bounded checks, sources and trust ceiling

Two final stages, produce.py and check.py, ran with Python3.13.5, CPU25s,
wall35s, address-space512MiB, each output file2MiB, one worker. Both exited0
with empty stderr; exact UTC starts, elapsed times, interpreter/source/input/
output SHA-256 values are in execution.json. The consumer imports no producer
or old verifier. It uses unordered-triple cover, owner-mask DP, successor-walk
gaps and component merging, as against the producer's role search, augmenting
allocation and degree/cut BFS. All remain in the SAME generation trust domain.

Checks:120 complete triple signatures,18 positive and342 negative deletion
queries; six new phase-clique blocks with5,8,12 chords and200 entire terminal
cofactors; ALL466 and1486 deletion sets of size<=2 for T30 and U54; two physical
exchanges;20 semantic mutations rejected. Reversing a P3's endpoint order is
explicitly accepted. Finite checks are pressure tests for the general phase
and clique inductions, not their proof. Initial exploration is non-exhaustive
and is separately marked; it found no positive global-minimum host.

External source check: Kelmans, arXiv:0910.2766, abstract/metadata retrieved
2026-09-09. Its equivalence statements are not a root proof or a proof of the
new endpoint phase/linkage lemmas. No external theorem is silently imported
into those elementary constructions. No novelty priority claim is made.

Registered verification, statement-faithfulness, axiom/escape audit and closure
remain unexecuted. No Lean elaboration or self-signed Evidence is supplied.
Historical untransported crossing/noncross/X3-r01/orphan packages remain distinct.
This new packet does not merge or clear those transactions.

## 8. Precise next physical obligation

The 0002 clique class is excluded constructively, in both quotient types. The
0212 triple-link motif is excluded when its opposite edge exists. What remains
includes non-complete crossing graphs, mixed 0002/0212 cliques, and path-middle
blocks outside these conditions. The original eight-type necessity itself must
NOT be carried to a path's middle circle without its missing opposite-edge
premise. No argument here forces either new configuration in every hypothetical
X3 host or excludes kappa_*=2.

Next atomic action: retain full endpoint order and two target colors while
following a transition between distinct residue phases in a non-complete or
mixed-type crossing component. Prove it exposes a cross-color terminal cofactor,
or a multi-circle exchange with u=0,D=s,t=b<=1. An unweighted Menger ear alone
is not that certificate. A fourth-chord insertion must rebuild the whole gap
state, not sum independent insertions. General X3/X2/root remain open.
