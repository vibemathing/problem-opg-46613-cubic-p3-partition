# X3 integration: one exceptional endpoint, no internal deletion, and a genuine path repair

NONTERMINAL_CHECKPOINT. verdict=candidate_only.
Repository: vibemathing/problem-opg-46613-cubic-p3-partition.
Frozen base: 43150f0c82a16afe55a612384b6712fc0a21a401.
Primary owner math-proof; generation trust domain web-candidate-generation.

## 1. Scope, integration and the exact unfinished question

The host is finite, simple, triangle-free, cubic and 3-vertex-connected. Its
SUPPLIED perfect matching M leaves exactly three circles of order 2 modulo 3.
P3 means a selected two-edge path on three distinct vertices, not an induced
subgraph requirement. The hypothesis being attacked is the GLOBAL minimum
min_{S subset M} kappa(S)=3, not a positive local value in a positive host.

PR28/29 provide the physical gap iff, kappa=t+b+3u and simultaneous accounting.
PR30 supplies true-port cofactor gluing. PR31 provides noncrossing/four-chord
reductions. PR32 already supplies the zero-exception phase theorem and the
three-chord linkage. None of their host censuses is rerun. The uploaded
residual R01 report has SHA256
8b0d083ad776535c42f7cf8954a10a2fe7308503f88b4b44154893d7636abd8b.
Its rooted full-Q criterion is a specialization of the existing unit rank;
its triad rescue overlaps PR32 and is not reintroduced as a new discovery.
The old untransported namespace is neither copied nor silently marked merged.

The requested X2 expert single-activation and double-deletion statements were
not located with fixed source bytes in the current main candidate inventory,
refs, Issue3 continuation, X2 PR search, or cancellation code search. Their
identity, quantifiers and content hashes remain an integration gap. The old
untouched-bad-cycle activation and conditional tree/bicycle transfer are NOT
assumed to be identical to the expert's unnamed statements. No invented expert
lemma or reconstructed attribution is a dependency here. This gap does not
block this separate direct X3 construction.

Local DAG (no new admitted registry IDs): circle-only cofactors -> explicit
one-exception terminal tree -> actual cross-color edge -> host P3-factor;
marked-gap counting -> impossibility of ALL internal deletions in a subclass;
physical reconstruction -> checked joint exchange. OPEN: force a comparable
construction in every remaining host. This package does not close that step,
X2, root, statement-faithfulness or trusted admission.

## 2. The new arbitrary-size terminal theorem

Let C=(0,...,n-1), n=3m+2>=5. Let Q be any matching of chords not duplicating
circle edges. Put B=C+Q and P=V(C)-V(Q), the genuine ports. Gamma(B) joins p,q
in P iff B-{p,q} has a spanning P3-factor, allowing ALL internal chords.

THEOREM CANDIDATE. If at most ONE endpoint of Q is outside
Z={0,3,6,...,3m}, then Gamma(B) is connected. Chord count and physical circle
length are unbounded. Q need not be pairwise crossing, noncrossing or connected
in its interlacement graph. The theorem is about the unchanged local block;
no reduced block is used as a smaller root instance.

Write T[a,b] for consecutive triples on the integer interval a,...,b of
nonnegative length divisible by 3; an empty interval contributes no triples.
A pair at directed circular distance 1 modulo 3 has a circle-only cofactor:
its two remaining circle paths have orders divisible by 3. In particular,
three consecutive genuine ports make Gamma connected. Their adjacent pairs
connect them, and every other port has distance 1 modulo 3 to one of the three.

For n=5, the premise gives at most one chord. If absent, adjacent-pair deletion
connects all ports. If present, its endpoints have a common intervening circle
port x. B-x has a Hamilton cycle; deleting any other port leaves a three-vertex
Hamilton path. These cofactors give a star at x. Hence assume m>=2 below.

### 2.1 Zero exceptions and the seam exception

The zero-exception case is the PR32 construction, restated as a dependency.
Any unmatched vertex of Z has two port neighbors, giving three consecutive
ports. Otherwise all of Z is matched. Set A_i=3i+1, B_i=3i+2 for 0<=i<m,
and z=3m+1. Circle-only pairs A_i--B_(m-1) and A_0--B_i connect all ports except
z. If 0 is matched to y in Z, add the cofactor with holes 1,z:

    (0,y,y-1), T[2,y-2], T[y+1,3m].

This connects z to the same component. All selected edges are actual edges.

If the only exceptional endpoint is z itself, every A_i,B_i remains a port.
The same circle-only component already contains them all. Any additional port
in Z is adjacent to one of these ports, and so attaches to it. Thus Gamma is
connected without selecting a chord. The two boundary vertices 0 and 3m attach
respectively to 1 and 3m-1; no neighbor at the deleted seam is presumed present.

### 2.2 A nonboundary phase-two exception

Suppose the exceptional endpoint is c=3j+2, 0<=j<m-1. Every unmatched Z vertex
other than c+1 has two genuine port neighbors, so that case is already settled.
Otherwise all Z vertices except possibly c+1 are matched, including vertex 0.
The ports A_0,...,A_(m-1), and all B_i except B_j form ONE circle-only component:
B_(m-1) connects every A_i, and A_0 connects every remaining B_i. If c+1 is a
port, it attaches to its port neighbor c+2. Only z may remain separate.

Let y be the actual Q partner of 0. If y is in Z, use the cofactor in 2.1. If
y=c, instead use, with the SAME holes 1,z,

    (0,c,c+1), T[2,c-1], T[c+2,3m].

The path orders are c-2 and 3m-c-1, both nonnegative multiples of 3. This
completes the terminal tree in both cases, including c=2 and empty intervals.

### 2.3 The boundary phase-two exception: the genuinely new two-chord case

Now c=3m-1=n-3. Write r=3m, p=3m-2 and z=3m+1. Unless three consecutive ports
already settle the case, all Z except possibly r is matched. Circle-only
cofactors connect A_i,B_i for 0<=i<=m-2 into one component W containing 1.
The only other possible ports are p,z and possibly r. If r is a port, it
attaches to z by adjacency (and also to W at circular distance 4).

If 0 is NOT partnered to c, connect z to 1 by 2.1. The actual partner y of c
then lies in Z with 3<=y<=3m-3: y=0 was excluded, and y=r would duplicate a
circle edge. For holes 1,p use

    (c,y,y-1), (r,z,0), T[2,y-2], T[y+1,3m-3].

This connects p to W; the two path orders are y-3 and 3m-y-3.

If 0 IS partnered to c, connect z to 1 using

    (0,c,r), T[2,3m-2]                 (holes 1,z).

If r is a port, connect p to z with

    (0,c,r), T[1,3m-3]                 (holes p,z).

If r is matched, let y be its actual partner. Again 3<=y<=3m-3, because 0,c
are already paired. The following cofactor with holes 1,p uses BOTH real
internal chords 0-c and r-y:

    (c,0,z), (r,y,y-1), T[2,y-2], T[y+1,3m-3].

Every displayed triple has its center in the middle. Lists are pairwise
vertex-disjoint and cover exactly the local vertex set minus the named holes.
The formulas include y=3 and y=3m-3, not just interior positions.

### 2.4 Phase-one exceptions and completeness

For an exceptional endpoint c=3j+1 other than z, reflect the cyclic labels by
x -> 3m-x modulo n. This preserves circle edges and Z, fixes z, and maps c to
a phase-two vertex. Apply 2.2 or 2.3 and reflect every complete triple back.
These cases exhaust every position of a single exceptional endpoint. They
supply actual terminal edges and partitions, not merely a residue count.

This is a direct finite-case algebraic proof for every m. The 64 bounded
implementation examples below are not its finite-to-infinite bridge.

## 3. This includes a genuine common-residual family

Suppose ALL endpoints are in Z union {c}, with c=3m-1. Then NO internal chord
e has a local cofactor B-V(e), even allowing any subset of all other chords.
Simplicity is important: cr is a circle edge, not an allowed chord.

Assume such a cofactor uses h other chords. Mark their 2h endpoints and the
two holes. One B extension is supplied per used chord, so total physical gap
demand must equal h. If c is not marked, all marks are phase zero: one circular
arc has residue 2 and the others residue 0, giving demand 4h+3.
If c is marked but r=3m is not marked, the same residues result after rotating
at the first phase-zero mark following c. Demand is again 4h+3.
If both c and r are marked, their consecutive special arc residues are 2,1,2,
with all other marked arcs residue 0. The demand is 4h. Here h>=1: h=0 would
make the deleted chord cr a forbidden duplicate circle edge. In every case
D>h, a contradiction. All unused chord endpoints remain ordinary vertices
of the recomputed full physical gaps; no host edge or vertex was erased.

Thus this whole arbitrary-chord subclass has no three-chord rescue, and its
full-Q rooted criterion fails at every root. Nevertheless Section2 constructs
Gamma connected. More internal-deletion search CANNOT close this subclass;
the true-port construction is the alternative exchange. This strengthens the
zero-exception failure already in PR32 without contradicting it.

## 4. Host lifting, including a path quotient with no opposite edge

Color a genuine port by which other complementary circle contains its M
partner. A mixed circle has both colors. Connected Gamma has an edge p-q
between colors; use THAT edge's complete local cofactor, not a superposition
of several incompatible cofactors. At the outside partner w of p, choose its
circle successor z and make (p,w,z). The rest of this outside circle is a path
of order L-2 divisible by 3; tile it in triples. Repeat in the other circle
for q. These three vertex regions are disjoint and cover the original host.

No matching edge between the two outside circles is needed. This proof works
in a path quotient's middle circle, not just in a triangle quotient. It does
not extend the opposite-edge-dependent internal-deletion rule to that middle.
The matching selected by the final factor is read as E(factor) intersect M.
It may contain four or more M edges; no cost-three bound is asserted.

Let theta(C,Q) be the minimum, over cyclic origins, of the number of internal
endpoints not congruent to zero modulo 3. The reflected proof gives the same
conclusion for either circle orientation. The new theorem implies that every
mixed circle in a hypothetical X3 host must have theta>=2. This is a necessary
restriction only, not a characterization or a proof that such hosts exist.

## 5. A NEW 54-vertex common-residual positive host

V54 has circles 0..25, 26..36, 37..53. Its matching is exactly
(0,23),(1,35),(2,53),(3,15),(4,26),(5,37),(6,18),(7,49),(8,28),
(9,21),(10,42),(11,45),(12,24),(13,27),(14,34),(16,40),(17,30),
(19,52),(20,32),(22,39),(25,43),(29,33),(31,36),(38,46),(41,47),
(44,50),(48,51).
All 81 host edges are the circle edges and this 27-edge matching, separately
listed in host.json. There is NO matching edge between the two outside circles.
This is not any old G24/G42/G60/H42/N48/P30/J30/T30/U54 fixture.

Its central Q={(0,23),(3,15),(6,18),(9,21),(12,24)} has one exceptional endpoint
23, a non-complete interlacement graph and theta=1. There are ten endpoints
but only nine phase-zero positions in a 26-cycle, so theta cannot be zero.
By Section3 every internal-pair deletion is impossible. The consumer checks
all 80 local root/subset demand certificates, NOT all subsets of the host M.
The full-Q demand is 16 on five owners, not the four units required by a
rooted full-Q cofactor. Hence this lies in the requested COMMON residual.

Holes 1 and 22 have the Section2.3 cofactor
(23,0,25),(24,12,11),(2,3,4),(5,6,7),(8,9,10),
(13,14,15),(16,17,18),(19,20,21).
Their partners are 35 and 39 in different outside circles. Append
(1,35,36),(26,27,28),(29,30,31),(32,33,34),
(22,39,40),(41,42,43),(44,45,46),(47,48,49),(50,51,52),(53,37,38).
This is a full eighteen-path factor. It uses FOUR original M edges.
The host is positive and has kappa_*=0, not a counterexample to X3 or root.

Start with S={(1,35),(22,39)}, with (s,D,nu,u,kappa)=(2,5,2,0,3).
Simultaneously add (0,23),(12,24). The central active order is
0,1,12,22,23,24 and the demands are 0,1,0,0,0,1. The outside demands are
one each. New (s,D,nu,u,kappa)=(4,4,4,0,0). Actual B extensions are
0->25,12->11,35->36,39->40; A ends are23,24,1,22.

The old maximum slot assignment is explicitly fixed on the two units of the
changed middle gap. None of its physical keys survives, so retained=[], loss=2.
Four recorded alternating augmentations produce the new maximum matching.
Delta s=2, Delta D=-1, Delta u=0, hence

    2(a-loss)=4 > 1=Delta s+Delta D+3Delta u,
    Delta kappa=2-1+4-8=-3.

All full gap paths, labels, owners, unit indices, retained matches and costs
are regenerated. Several insertions into one old gap are not added separately.
Intermediate single-edge monotonicity is neither needed nor asserted.

## 6. Computation scope and open integration/admission gaps

construct.py implements the theorem and freezes 64 local examples at orders
5..50, with 1098 full cofactor partitions. check.py imports no producer or old
verifier: it checks adjacency/coverage and terminal connectivity, regenerates
physical gaps by successor walking, computes owner rank using masks, and
replays all retained matches and alternating augmentations. It checks all
1486 vertex-deletion sets of size at most two on the NEW V54, all 80 local
negative-demand states, the full factor, and 20 semantic mutations.

These examples do not prove arbitrary-size existence: the proof is Sections2-4.
No old host census is repeated. Both final bounded stages are recorded in
execution.json, with actual interpreter and source/input/output hashes, exits,
wall observations, CPU25s/wall35s/AS512MiB/per-output2MiB/one worker. They remain
in the SAME generation trust domain. No Lean elaboration, axiom audit, trusted
verifier receipt or closure gate has executed. The request is not Evidence.

FIRST OPEN LEMMA: a mixed-target block for which every circular labeling has
at least two off-phase internal endpoints, no triad rescue, and no full-Q
rooted solution. Host cuts/Menger connectivity have not been shown to force
one of the cofactor patterns or a different strict exchange there. In a path
middle, that new proof still cannot use a nonexistent opposite edge. X2 local
lemmas, even after their source identity is recovered, would remain conditional
exchange tools rather than a root existence proof. All canonical obligations
remain open; no protected record, Result or Solution is changed.
