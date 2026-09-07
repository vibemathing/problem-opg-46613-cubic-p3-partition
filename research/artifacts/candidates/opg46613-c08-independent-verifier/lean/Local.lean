import Lean
import Lean.Elab.Tactic.Omega

/-!
Candidate source, NOT compiled in the producing session.
All exhaustive proof attempts use `decide`, not compiler-trusting evaluation.
The state bit ordering is exactly the 12 edges below; boundary bits attach at
vertices 0, 3, 4, in that order. No global graph theorem is asserted here.
-/
namespace R03

set_option maxRecDepth 200000
set_option maxHeartbeats 0

def bit (mask index : Nat) : Nat := (mask / (2 ^ index)) % 2

def internalEdges : List (Nat × Nat) :=
  [(0,1),(0,5),(1,2),(1,6),(2,3),(2,7),
   (3,8),(4,6),(4,7),(5,7),(5,8),(6,8)]

def internalDegree (s v : Nat) : Nat :=
  match v with
  | 0 => bit s 0 + bit s 1
  | 1 => bit s 0 + bit s 2 + bit s 3
  | 2 => bit s 2 + bit s 4 + bit s 5
  | 3 => bit s 4 + bit s 6
  | 4 => bit s 7 + bit s 8
  | 5 => bit s 1 + bit s 9 + bit s 10
  | 6 => bit s 3 + bit s 7 + bit s 11
  | 7 => bit s 5 + bit s 8 + bit s 9
  | 8 => bit s 6 + bit s 10 + bit s 11
  | _ => 0

def boundaryDegree (b v : Nat) : Nat :=
  match v with
  | 0 => bit b 0
  | 3 => bit b 1
  | 4 => bit b 2
  | _ => 0

def boundaryCount (b : Nat) : Nat := bit b 0 + bit b 1 + bit b 2

abbrev LocalValid (s b : Nat) : Prop :=
  ∀ v : Fin 9, internalDegree s v.val + boundaryDegree b v.val = 2

abbrev InternalAdj (s u v : Nat) : Prop :=
  ∃ i : Fin 12, bit s i.val = 1 ∧
    (internalEdges[i.val]! = (u,v) ∨ internalEdges[i.val]! = (v,u))

/-- Independent incidence count from the actual edge table. -/
def countedInternalDegree (s v : Nat) : Nat :=
  ((List.range 12).filter (fun i =>
    decide (bit s i = 1 ∧
      ((internalEdges[i]!).1 = v ∨ (internalEdges[i]!).2 = v)))).length

/-- Prevent a transcription error in the nine hand-written degree equations. -/
theorem internal_degree_faithful : ∀ s : Fin 4096, ∀ v : Fin 9,
    internalDegree s.val v.val = countedInternalDegree s.val v.val := by
  decide

/-- An ordered, closed five-vertex cycle certificate in the local fragment.
Closure is explicit; a mere 5-cycle sitting inside a larger component would
NOT satisfy this predicate. Boundary incidences at its vertices must be zero.
-/
abbrev ClosedFive (s b : Nat) (c : List Nat) : Prop :=
  c.length = 5 ∧ c.Nodup ∧
  c.all (fun v => decide (v < 9)) = true ∧
  (∀ i : Fin 5, InternalAdj s (c[i.val]!) (c[(i.val + 1) % 5]!)) ∧
  (∀ v : Fin 9, v.val ∈ c → boundaryDegree b v.val = 0) ∧
  (∀ u v : Fin 9, u.val ∈ c → InternalAdj s u.val v.val → v.val ∈ c)

theorem boundary_cases : ∀ b : Fin 8,
    boundaryCount b.val = 2 → b.val = 3 ∨ b.val = 5 ∨ b.val = 6 := by
  decide

/-- Each theorem covers ALL 4096 choices of internal edges. -/
theorem valid_boundary_3 : ∀ s : Fin 4096,
    LocalValid s.val 3 ↔ s.val = 1518 ∨ s.val = 3989 := by
  decide

theorem valid_boundary_5 : ∀ s : Fin 4096,
    LocalValid s.val 5 ↔ s.val = 1785 ∨ s.val = 2910 := by
  decide

theorem valid_boundary_6 : ∀ s : Fin 4096,
    LocalValid s.val 6 ↔ s.val = 2791 ∨ s.val = 3387 := by
  decide

theorem certificate1518 : ClosedFive 1518 3 [1,2,7,4,6] := by decide
theorem certificate3989 : ClosedFive 3989 3 [4,6,8,5,7] := by decide
theorem certificate1785 : ClosedFive 1785 5 [2,3,8,5,7] := by decide
theorem certificate2910 : ClosedFive 2910 5 [1,2,3,8,6] := by decide
theorem certificate2791 : ClosedFive 2791 6 [0,1,2,7,5] := by decide
theorem certificate3387 : ClosedFive 3387 6 [0,1,6,8,5] := by decide

/-- Intended local obstruction theorem: no assumptions about the remote brick.
To apply globally one must PROVE restriction to these masks is faithful.
-/
theorem local_obstruction (s : Fin 4096) (b : Fin 8)
    (hv : LocalValid s.val b.val) (hb : boundaryCount b.val = 2) :
    ∃ c : List Nat, ClosedFive s.val b.val c := by
  rcases boundary_cases b hb with h3 | h5 | h6
  · have hv3 : LocalValid s.val 3 := by simpa only [h3] using hv
    rcases (valid_boundary_3 s).mp hv3 with hs | hs
    · exact ⟨[1,2,7,4,6], by simpa only [hs,h3] using certificate1518⟩
    · exact ⟨[4,6,8,5,7], by simpa only [hs,h3] using certificate3989⟩
  · have hv5 : LocalValid s.val 5 := by simpa only [h5] using hv
    rcases (valid_boundary_5 s).mp hv5 with hs | hs
    · exact ⟨[2,3,8,5,7], by simpa only [hs,h5] using certificate1785⟩
    · exact ⟨[1,2,3,8,6], by simpa only [hs,h5] using certificate2910⟩
  · have hv6 : LocalValid s.val 6 := by simpa only [h6] using hv
    rcases (valid_boundary_6 s).mp hv6 with hs | hs
    · exact ⟨[0,1,2,7,5], by simpa only [hs,h6] using certificate2791⟩
    · exact ⟨[0,1,6,8,5], by simpa only [hs,h6] using certificate3387⟩

end R03
