import Lean
import Lean.Elab.Tactic.Omega

/-!
Candidate source, NOT compiled in the producing session.
These are arithmetic endpoints. The two degree-sum hypotheses must be
proved from a graph before this lemma can be used in the C02 theorem.
-/
namespace R03

theorem boundary_count_from_bipartition
    (small inside boundary : Nat)
    (hsmall : inside = 2 * small)
    (hlarge : inside + boundary = 2 * (small + 1)) :
    boundary = 2 := by
  omega

theorem family_order (q : Nat) :
    2 * (6 * q + 5) + 8 = 18 + 12 * q := by
  omega

theorem family_right_brick_order (q : Nat) :
    2 * (6 * q + 5) - 1 = 3 * (4 * q + 3) := by
  omega

theorem family_nonisomorphic_order_obstruction (p q : Nat)
    (h : 18 + 12 * p = 18 + 12 * q) : p = q := by
  omega

theorem five_is_not_divisible_by_three : ¬ (3 ∣ (5 : Nat)) := by
  decide

end R03
