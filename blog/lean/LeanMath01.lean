import Mathlib

namespace LeanMathSeries

-- Lagrange's identity in dimension two.
theorem lagrange_identity (a b c d : ℝ) :
    (a^2 + b^2) * (c^2 + d^2) - (a*c + b*d)^2 =
      (a*d - b*c)^2 := by
  ring

-- The squared Cauchy–Schwarz inequality.
theorem dot_sq_le (a b c d : ℝ) :
    (a*c + b*d)^2 ≤ (a^2 + b^2) * (c^2 + d^2) := by
  apply sub_nonneg.mp
  rw [lagrange_identity]
  exact sq_nonneg (a*d - b*c)

-- A concrete counterexample to equality for every pair of vectors.
example : ((1 : ℝ)*0 + 0*1)^2 ≠ (1^2 + 0^2)*(0^2 + 1^2) := by
  norm_num

#print axioms lagrange_identity
#print axioms dot_sq_le

end LeanMathSeries
