/* Exact mathematical model for the introductory linear-algebra lesson.
   No numerical eigenvalue routine is used: results follow from the matrix family. */
(function (root) {
  'use strict';
  function matrix(t) {
    if (!Number.isFinite(t)) throw new TypeError('t must be finite');
    return [[1, t], [0, 1]];
  }
  function apply(t, point) {
    if (!Array.isArray(point) || point.length !== 2 || !point.every(Number.isFinite)) {
      throw new TypeError('point must be a finite 2-vector');
    }
    const A = matrix(t);
    return [A[0][0] * point[0] + A[0][1] * point[1],
            A[1][0] * point[0] + A[1][1] * point[1]];
  }
  function determinant(t) {
    const A = matrix(t);
    return A[0][0] * A[1][1] - A[0][1] * A[1][0];
  }
  function eigenspaceDimensionAtOne(t) {
    matrix(t);
    return t === 0 ? 2 : 1;
  }
  const api = Object.freeze({ matrix, apply, determinant, eigenspaceDimensionAtOne });
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (root) root.ShearMath = api;
})(typeof window !== 'undefined' ? window : undefined);
