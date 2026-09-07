import Mathlib

/-!
UNCOMPILED SPECIFICATION ONLY. Not included in the standalone core Lake build.
Before accepting any result, pin a compatible mathlib commit and compile this
file. The definitions below deliberately expose the remaining statements as
`def ... : Prop`, NOT as proved theorems or assumed lemmas.
-/
namespace R03Spec

variable {V : Type} [Fintype V]

/-- Finite vertex degree, specified through actual adjacency. -/
noncomputable def Degree (G : SimpleGraph V) (v : V) : Nat :=
  Nat.card {w : V // G.Adj v w}

def Cubic (G : SimpleGraph V) : Prop := ∀ v, Degree G v = 3

/-- Vertex, not edge, connectivity. The order guard excludes degenerate cases. -/
def ThreeVertexConnected (G : SimpleGraph V) : Prop :=
  4 ≤ Fintype.card V ∧
  ∀ S : Finset V, S.card ≤ 2 →
    (SimpleGraph.induce {v : V | v ∉ S} G).Connected

/-- A bijection enforces disjointness and coverage. Ambient chords are allowed. -/
structure P3Factor (G : SimpleGraph V) where
  blocks : Nat
  place : (Fin blocks × Fin 3) ≃ V
  edge01 : ∀ i, G.Adj (place (i,0)) (place (i,1))
  edge12 : ∀ i, G.Adj (place (i,1)) (place (i,2))

def TwoFactor (G F : SimpleGraph V) : Prop :=
  F ≤ G ∧ ∀ v, Degree F v = 2

/-- Cardinality of the entire F-component, not the ambient G-component. -/
noncomputable def ComponentOrder (F : SimpleGraph V) (v : V) : Nat :=
  Nat.card {w : V // F.Reachable v w}

def DivisibleTwoFactor (G F : SimpleGraph V) : Prop :=
  TwoFactor G F ∧ ∀ v, 3 ∣ ComponentOrder F v

def HasDivisibleTwoFactor (G : SimpleGraph V) : Prop :=
  ∃ F : SimpleGraph V, DivisibleTwoFactor G F

def PerfectMatching (G M : SimpleGraph V) : Prop :=
  M ≤ G ∧ ∀ v, Degree M v = 1

/-- Relative complement: E(G) minus E(M), on the SAME vertex type. -/
def MatchingComplement (G M : SimpleGraph V) : SimpleGraph V :=
  G ⊓ Mᶜ

def HasDivisibleComplement (G : SimpleGraph V) : Prop :=
  ∃ M : SimpleGraph V,
    PerfectMatching G M ∧ DivisibleTwoFactor G (MatchingComplement G M)

def ComplementBridgeTarget (G : SimpleGraph V) : Prop :=
  Cubic G → (HasDivisibleComplement G ↔ HasDivisibleTwoFactor G)

def CycleSplittingTarget (G : SimpleGraph V) : Prop :=
  HasDivisibleTwoFactor G → Nonempty (P3Factor G)

def brickEdges : List (Nat × Nat) :=
  [(0,1),(0,5),(1,2),(1,6),(2,3),(2,7),
   (3,8),(4,6),(4,7),(5,7),(5,8),(6,8)]

/-- Forward edge rule on labels 0..17+12q. Labels 9.. are c_j -> j+8.
No wrap edge survives deletion of c_0. Fin bounds restrict the chord range.
-/
def forwardEdge (q u v : Nat) : Prop :=
  (u,v) ∈ brickEdges ∨
  (9 ≤ u ∧ (v = u + 1 ∨ v = u + (6*q+5))) ∨
  (u = 0 ∧ v = 9) ∨
  (u = 3 ∧ v = 17 + 12*q) ∨
  (u = 4 ∧ v = 13 + 6*q)

def H (q : Nat) : SimpleGraph (Fin (18+12*q)) where
  Adj u v := u ≠ v ∧ (forwardEdge q u.val v.val ∨ forwardEdge q v.val u.val)
  symm := by
    intro u v h
    exact ⟨Ne.symm h.1, h.2.symm⟩
  loopless := by
    intro v h
    exact h.1 rfl

/-- The finite C02 claim, including every required domain predicate. -/
def FiniteTarget : Prop :=
  Cubic (H 0) ∧ ThreeVertexConnected (H 0) ∧
  Nonempty (P3Factor (H 0)) ∧ ¬ HasDivisibleComplement (H 0)

/-- The full family claim. This file does NOT provide a proof of it. -/
def FamilyTarget : Prop :=
  ∀ q : Nat, Cubic (H q) ∧ ThreeVertexConnected (H q) ∧
    Nonempty (P3Factor (H q)) ∧ ¬ HasDivisibleComplement (H q)

/-- A deliberately separate statement; nothing here proves or disproves it. -/
def RootProblem : Prop :=
  ∀ k : Nat, 0 < k → ∀ G : SimpleGraph (Fin (3*k)),
    Cubic G → ThreeVertexConnected G → Nonempty (P3Factor G)

end R03Spec
