# Global-minimum normalization and simultaneous gap surgery

Status: NONTERMINAL_CHECKPOINT. Verdict: candidate_only.
Primary owner: math-proof. Trust domain: web-candidate-generation.
Repository: vibemathing/problem-opg-46613-cubic-p3-partition.
Source/base: 29e101f446712c4d786251dd2e7943de80bb6fa8.

## 1. Frozen question, reuse and exact open objective

The root asks for a spanning P3-factor in every finite simple 3-vertex-connected
cubic graph of positive order divisible by three. A P3 is a selected path on
three distinct vertices, not necessarily an induced path. Here the host is also
triangle-free, and cubicity makes its order a positive multiple of six. The
triangle-free bridge in PR25 is reused, not re-audited or treated as root truth.

Fix an actual supplied perfect matching M and F=G-M. Both the normal form and
its physical-incidence lifting are already candidate material in PR26/28.
For S subset M, write s=|S|, D for the total gap demand, nu for the maximum
slot-to-owner matching size, and u for the number of untouched F-cycles whose
orders are not divisible by three. The exact previous potential is

    kappa(S)=s+D-2nu+3u.

It is nonnegative and is zero exactly when the original graph has a P3-factor
whose intersection with M is S. The present goal is to exclude a positive
GLOBAL minimum of kappa, not merely to find improvements from some sampled S.
That goal is NOT completed here.

Document-local dependency chain (not new admitted record IDs):
physical gap equations -> demand-unit rank -> activation normalization ->
222 extremal dichotomy -> conditional physical surgeries -> OPEN availability
of an improving simultaneous exchange. Root additionally needs the existing
triangle-free bridge, matching-existence dependency and trusted closure.

The component-rank idea also occurs in an orphan historical exchange-r02
packet on branch head 351b3183f251e0849bdee471e4bd180dbf52fb60. Only that packet
is present in its added tree; its named program/output files are absent and its
PR27 binding is wrong. We neither claim the rank idea as new nor use the packet's
unrecovered executions as verification. Its Psi used a different untouched-cycle
penalty. All statements here concern the exact kappa with coefficient THREE.

## 2. Demand-unit graph and exact deficit identity

An active endpoint is an endpoint of an edge of S. On each touched F-cycle,
keep its actual cyclic order. If a gap has d F-edges between consecutive active
endpoints, its internal order is d-1 and its demand is r=(d-1) mod 3 in {0,1,2}.
Each selected M edge is a supply-one owner. An owner chooses exactly one of its
two endpoints as B, and exactly one neighboring gap for the B pair; the other
endpoint is an A singleton. Internal matching chords remain actual owners with
two distinct physical ends. Untouched cycles need order divisible by three.

Define L_S with vertex set S, including isolated owners. For every demand unit
of a gap, put one labeled edge joining the owners of its two boundary endpoints.
Thus r=2 gives two parallel edges. Equal owners give loops. These auxiliary
loops are not loops in the simple host graph. This unit graph differs from the
earlier graph K_S, where demand-two gaps were encoded as forced marks.

For a connected component C with v vertices and e edges, the maximum matching
of its edge-slots to distinct incident vertices has size min(v,e). Proof: if C
is a tree, orient away from a root and assign each edge to its farther endpoint,
saturating all e=v-1 slots. Otherwise choose a spanning tree plus one extra edge
and orient its unique cycle cyclically and its attached trees outward. This
assigns exactly one chosen edge to each vertex, saturating all v owners. A loop
is a one-edge cycle; parallel edges can form a two-edge cycle. The upper bound
min(v,e) is immediate. No other component shares an owner or slot.

Consequently, letting t count tree components and b=sum_C max(0,e_C-v_C),

    nu = sum_C min(v_C,e_C),
    kappa(S) = sum_C |v_C-e_C| + 3u = t+b+3u.                 (1)

In particular kappa=0 iff every unit component is unicyclic and u=0. This is a
feasibility identity, NOT a factor-count formula for artificially labeled
identical demand slots. Counting factors still requires physical-incidence
multiplicities, as in PR26/28.

If kappa=0, allocate each slot to a distinct owner. A demand-two gap must use
both different owners; two slots incident only with the same owner cannot be
saturated. A demand-one loop permits either physical end, choose one. Restore
that owner's B pair at the allocated physical end and join its other A end
along the M edge. In each gap, r end vertices have been consumed; the remaining
nonnegative order is a multiple of three and is tiled by consecutive triples.
All active endpoints and all internal gap vertices are used once. Conversely,
a factor restricted to F produces exactly such an allocation. Thus the unit
form still lifts in BOTH directions to actual P3 components on the UNCHANGED
host. No reduction of simplicity, cubicity, connectivity or modulus is hidden.

## 3. Inclusion-minimal Hall obstructions are bicycles

Let Y be an inclusion-minimal slot set with |Y|>|N(Y)|. Consider only its unit
edges and incident owners. Some connected component is deficient; minimality
forces it to be the entire set. Deleting any one edge gives a nondeficient set,
so |Y|-1 <= |N(Y)|, and hence |Y|=|N(Y)|+1. An owner of degree one would disappear
on deletion of its unique edge, preserving deficiency, contrary to minimality.
Thus every owner has degree at least two, counting a loop twice.

The connected graph has cycle rank two and

    sum_v (degree(v)-2)=2.

After suppressing degree-two paths there is either one vertex of degree four
or two vertices of degree three. These give precisely two loops sharing a
vertex, three paths between two vertices, or two loops joined by a path.
Before suppression these are respectively tight handcuff, theta and loose
handcuff shapes, including permitted loop and parallel degeneracies. Deleting
any edge of each shape leaves a pseudoforest, so each really is minimal.
This direct proof, rather than an unexamined theorem name, supplies the claim.

A positive potential can also come entirely from surplus owners in trees.
Then no Hall-deficient demand set exists. Both t and b must be retained; Hall
search alone cannot describe every nonfeasible state.

## 4. A strict normalization step: touch every bad cycle

**Activation lemma.** If C is an untouched F-cycle of nonzero order modulo three,
then for EVERY matching edge e incident with C,

    kappa(S union {e}) < kappa(S).                            (2)

The edge is not already selected. This does not assert descent for arbitrary
single-edge toggles once all bad cycles are touched.

### 4.1 Both ends in untouched cycles

If both ends lie in C, activating them gives one new owner and loops with total
demand R. For |C|=1 mod3, R=2; for |C|=2 mod3, R=0 or 3. The new contribution
|1-R| is 1 or 2, replacing the old penalty 3.

If the ends lie on different untouched cycles, each has just one new active
endpoint and creates (L-1) mod3 loops on the new owner. If both cycles were bad,
the combined demand is 0,1 or 2 and the old penalty was 6. If exactly one was
bad, the demands sum to 2 or 3 and the old penalty was 3. In every case the new
|1-R| is strictly smaller. Other components are unchanged.

### 4.2 One end in an untouched bad cycle, the other in a touched gap

Let the new owner be z. The bad cycle contributes ell loops at z, where ell=0
for residue one and ell=1 for residue two. Splitting the touched gap replaces
r parallel a--b edges by p a--z edges and q z--b edges, where

    p,q in {0,1,2},       r=(p+q+1) mod3.

This includes a=b, old loops, zero arms, and repeated edge slots. Put
phi(L)=sum |v-e|, including isolated vertices. The increase in phi is bounded by:

| (p,q), allowing reversal | r | ell=0 | ell=1 |
|---|---:|---:|---:|
| (0,0) | 1 | 2 | 1 |
| (0,1) | 2 | 2 | 1 |
| (0,2) or (1,1) | 0 | 1 | 2 |
| (1,2) | 1 | 1 | 2 |
| (2,2) | 2 | 1 | 2 |

Here is a complete bound proof. Every connected deficit c=v-e is an integer
at most one. Adding or deleting one edge changes phi by exactly one in absolute
value: within a component c changes by one; when joining components use
|c1+c2-1|-|c1|-|c2| for c1,c2<=1.

For (0,0), delete one edge and add a separate z; its contribution is 1-ell.
This gives 2-ell. For (0,1), remove two parallel edges, then attach z by one edge
at b and ell loops. If deleting the pair leaves its old component connected,
its original c<=-1 becomes c+2, giving a phi increase at most zero before the
new loop. If deletion separates a and b into components with deficits c1,c2,
the complete change is

    |c1|+|c2-ell|-|c1+c2-2| <= 2-ell  (ell=0 or 1).

To check this inequality, split into c1=c2=1, exactly one equal to 1, or both
nonpositive; these exhaust integers <=1. Equal original endpoints remain in
the connected case. The new single edge with z changes neither endpoint
component's deficit, except for the ell loops.

For (0,2), attaching z by a doubled edge changes c to c-1-ell. For (1,1), either
the old endpoints share a component with that same deficit change, or they
belong to different components and the triangle inequality bounds the change
by 1+ell. For (1,2) and (2,2), the replacement preserves old connectivity,
adds one vertex and a net two edges, again changing c to c-1-ell. Since c<=1,
the absolute-value increase is at most 1+ell. This proves every table entry.

Thus phi increases by at most two, while u decreases by one. Equation (1)
gives Delta kappa<=-1. This proves (2) for all cases, not merely the finite
abstract graphs used as regression tests.

**Consequence.** Every global minimizer of kappa touches every bad F-cycle.
Starting with any S, repeatedly activating an edge on an untouched bad cycle
strictly lowers kappa and lowers u. This normalization terminates after at most
the initial number of bad cycles. It does not promise kappa=0 after u reaches 0.

## 5. Global positive minima in three-cycle 222 have two normal forms

Assume n=0 mod3 and u=0. Summing gap lengths gives

    D == n-2s == s (mod3),       b-t == D-s == 0 (mod3).       (3)

Untouched cycles have zero residue and do not change the calculation. Thus
kappa=t+b cannot equal one. This applies to any number of F-cycles.

Now suppose F has exactly three cycles, all of residue two. Connectedness of G
makes the cross-edge cycle quotient connected. Choose two actual M edges whose
quotient is a spanning tree. Each leaf cycle has one active endpoint and creates
one demand-one loop on its owner. The middle cycle has two active endpoints;
its two gap demands sum to either zero or three, since its length is 2 mod3.
In the former case the unit graph consists of two separate loops and kappa=0.
In the latter it consists of two owners, a loop at each, and three parallel
middle-gap demand edges, giving kappa=5-2=3. Therefore

    min_S kappa(S) belongs to {0,2,3}.                        (4)

If the global minimum is positive, the following alternatives are exhaustive:

- Value 2: any minimizer has u=0, exactly one tree component and exactly one
  bicyclic component (e=v+1); every other component is unicyclic.
- Value 3: choose a minimum-cardinality minimizer. It has two selected cross
  edges and the five-edge/two-owner unit graph just described. Indeed the
  chosen two-edge quotient tree must have value 3 under this hypothesis.
  No empty or singleton S can be a minimizer, since it leaves a bad cycle
  untouched and violates the activation lemma.

An arbitrary value-three state could instead have three trees and no excess,
but the special two-edge minimizer is available when the GLOBAL minimum is
three in the 222 setting. This is not a statement that every positive local
minimum has either of these global-minimizer forms.

For the standard value-three graph, the three middle-gap unit edges form a
minimal theta Hall obstruction, and a loop at each owner with a connecting
edge forms a minimal loose handcuff. This fixes small abstract cores while
retaining arbitrarily long physical gaps and all unselected matching chords.

No argument in this section excludes values 2 or 3. Doing so is the next open
mathematical obligation. In particular (4) does not bound the number of M edges
in a P3-factor by three; G42's required four edges remain fully compatible.

## 6. Exact accounting for simultaneous additions AND deletions

Let S'=(S minus R) union A, with no bound on |R|+|A|. Recompute all activity
orders and gaps in every affected cycle. A common demand slot is retained only
when its whole physical key (cycle, full gap path, two owners, unit label) is
unchanged and its assigned owner survives.

Take a maximum old slot matching of size nu. Delete exactly l matching pairs
which cannot be retained. On the NEW slot graph perform a augmentations from
the retained matching, producing a matching of size nu-l+a. This implies

    kappa(S') <= kappa(S) + Delta s + Delta D + 3 Delta u
                              + 2l - 2a.                    (5)

It is equality when the new matching is maximum. Each augmentation is a simple
alternating path beginning at an unmatched slot and ending at an unmatched
owner; toggling it increases cardinality by one. All inherited matches retain
actual valid incidences by their physical keys. Thus (5) is a complete finite
certificate, not an appeal to a matching on the wrong old demand graph.

A sufficient strict-exchange condition is

    2(a-l) > Delta s + Delta D + 3 Delta u.                  (6)

Only the endpoint comparison matters; no intermediate one-edge step is assumed
to descend. If two changed endpoints occur in the same old gap, their combined
new gaps must be computed simultaneously, not by adding two independent split
formulas. The executable traces rebuild the whole affected cycle precisely.

On G24, S indices {0,3} -> {0,2,3,4} give Delta s=2, Delta D=-1, Delta u=0,
l=2,a=4, so (5) gives -3. The intermediate {0,2,3} remains at kappa=3.
On G42, {0,3} -> {0,1,10,12} removes index 3 and adds 1,10,12. The same
accounting gives -3 and the final set has FOUR edges. Both traces include
full gap lists, all alternating paths, B/A roles and full P3 partitions.
These are new accounting checks of five fixed selected sets, NOT repetitions
of the previous full 4096/1562/5985-subset enumerations.

These control exchanges use known final feasible sets. They validate the
certificate rule, but cannot prove that a successful endpoint always exists
in an unknown graph without already knowing a factor.

## 7. Three conditional physical surgeries

All statements here assume u=0 and a new matching edge with its endpoints in
TWO DISTINCT old gaps. Each listed hypothesis is checked on actual cyclic
positions, not only on the unit graph. None asserts universal availability.

### 7.1 Transfer a cycle from a bicycle to a tree

Suppose t=b=1. At one endpoint the old gap has demand one and splits as (0,0),
removing a nonbridge unit edge from the bicyclic component. At the other,
p+q-r=2, and every participating old owner lies in the unique tree component:
include owners of nonzero arms and of an old edge if r>0. The tree cannot
contain a demand-two doubled edge. Its possible splits are r=0 with (0,2),
(1,1),(2,0), or r=1 with (1,2),(2,1).

The bicycle loses one nonbridge edge and becomes connected unicyclic. In the
tree, the replacement preserves connectedness, adds the new owner and a net
two edges, giving e=v. Both become unicyclic, others are unchanged; kappa falls
from two to zero. Physical lifting from Section 2 gives an actual P3-factor.

### 7.2 Reduce excess three to one tree and one bicycle

Suppose t=0,b=3. Both endpoints split demand-one gaps as (0,0). Assume removing
those two unit edges leaves every old component cyclic (equivalently, the
remaining slots can saturate all old owners). Their total excess drops from
three to one. The new owner is isolated, so t'=1,b'=1 and kappa changes 3->2.
The two affected slots may be in the same component. Connectivity of each old
component need not persist; the no-new-tree hypothesis is what is used.

### 7.3 Consume three surplus trees

Suppose t=3,b=0. Both endpoints split demand-zero gaps as (1,1), and the four
resulting arms together meet all three tree components. They may also meet
unicyclic components. The star through the new owner joins these components;
its resulting deficit is 3+1-4=0. Everything else remains unicyclic, so kappa
falls 3->0. This supply-surplus case matters for arbitrary cycle counts, even
though Section 5 permits a different cardinality-minimal 222 representative.

A hypothetical global minimizer must avoid every applicable surgery above.
Proving that it cannot avoid all suitable multi-edge surgeries requires a
physical reachability argument not supplied by the abstract Hall bicycle.
Bicircular matroid exchange on a FIXED ground graph does not solve this: when
S changes, the ground slots and their endpoint incidences change as well.

## 8. New executions, separate code paths and exact scope

The scripts import no earlier constructor/verifier core. surgery.py uses unit
component counts and explicit alternating matchings. check.py imports neither
surgery.py nor the producer; it uses successor walks, a residual-capacity matrix
max flow and a separate used-owner-mask DP for abstract tests. They remain in
the same generator trust domain; no trusted-verifier status is asserted.

Four bounded stages ran with Python 3.13.5, each CPU 25 seconds, wall 35 seconds,
address space 512 MiB, each produced file at most 1 MiB, one worker/thread.
All exit codes were zero and all stderr files empty. Actual commands, UTC start
times, wall/CPU/RSS observations and exact source/output SHA-256 are in
execution.json. No Lean elaboration or axiom report was produced.

The new scope is:
- Twenty deterministic labeled hosts at orders 30,36,42,48,60,72 with 3,4,5,6,9
  complementary cycles. Complete edge lists, specified M and explicit factors
  are in new-hosts.json. The separate consumer checks all 26102 vertex-deletion
  sets for THESE hosts. Every factor proves min kappa=0 by nonnegativity.
- 232 specified selected states, 542 bad-cycle activations, 143 inclusion-minimal
  Hall certificates, and 12 two-edge quotient-tree 222 controls.
- 36 distinct conditional surgeries: 6 cycle transfers, 29 excess-three
  reductions, and 1 three-tree merge. They are finite tests of the hypotheses,
  not a theorem that some hypothesis always holds.
- All 53496 abstract activation cases with 1..3 old owners, loop/pair
  multiplicities 0..2, every eligible split and both new-loop choices, checked
  by component counts and separately by explicit owner-mask assignment DP.
- Nineteen semantic mutations rejected at their designated assertions: malformed
  selected owners, gaps, demand units, rank/conflict claims, Hall sets, P3
  partitions, center roles, simultaneous additions and augmentation accounting.
  Mutation rejection does not rely on a changed input hash.

This is not an isomorphism-reduced graph census. No complete global no-factor
object, positive min-kappa graph or root counterexample was found. Resource
limits raise errors, never UNSAT. The 20 positive factors avoid any need to
claim a search over every perfect matching: a displayed factor normalizes for
any supplied M by its actual intersection with that M.

## 9. First unresolved exchange lemma and admission boundary

For three-cycle 222 the remaining minimal-counterexample attack has TWO cases:
X2: exclude a positive global minimum two (one tree and one bicyclic component);
X3: exclude a global minimum three represented by two owners, their two loops,
and the three parallel middle-gap units. In each case construct actual sets R,A
and augmentations satisfying (6), tracking every changed physical gap. This
availability claim remains OPEN. The conditional surgeries do not close X2/X3.

For arbitrary cycle count, Sections 2-4 and 6-7 already hold. The missing extra
step is a quotient/residue grouping or ear-exchange invariant that bounds and
transfers simultaneous tree surplus and multi-cycle excess while preserving
all gap incidences. The special upper bound three from Section 5 has not been
proved for arbitrary cycle count and is not asserted there.

The web principal has no signing authority. A scoped request asks registered
verifiers to replay fixed bytes and review the general proof/faithfulness/axiom
obligations. The observed workflow checks only transport, not this mathematics.
Both canonical obligations, previous raw-output gaps and pending C08 Lean remain
open. The orphan exchange-r02 branch is separately recorded, not merged or
silently counted as delivered. This candidate does not produce a Result or
Solution and does not constitute terminal closure.
