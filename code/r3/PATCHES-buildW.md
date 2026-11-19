# PATCHES: build-3 -> build-W (R3-WINDOW)

Seat build-W, 2026-11-19. build-1/, build-2/, build-3/ were not touched (read and imported only via copies).

## Copied unchanged
The eleven build-3 instruments were copied byte-identically: itaylor.py, bg_tube.py, lincore.py, bracket.py,
tail.py, match.py, kraw.py, krein.py, evans.py, assemble.py, verdict.py. Their sha256 equal build-3/RUN.md (table in
RUN.md). None of them was edited. kraw/krein/evans/match/tail/assemble/verdict are not used by the window path
(kept for provenance; the R2 Krein values are read from build-3/out as control references).

## New files (instruments)
| file | role |
|---|---|
| hw3.py | HW3: 3-channel counts with the propagated state re-based after every step (march_rebase), W-level 0 asserted; CPOS (k forcing columns, Haynsworth LDL); RITZ Gram (exact polynomial parts + Taylor quadrature + crude [0, r0]); PEN (CPOSL (d), 2-channel B_m^P) |
| green.py | GREEN: odd-series start of U1, U2 (order 29), EXT lemma for V1, delta-hull, Z1/Z2 basis of rho cap U2^perp, tau from marches only, kernel in the basis {U2, V1hat, Z1, Z2}, apply(profile) with [0, r0] and exterior (max principle 1/(kappa1^2 - 1/8), Gauss law) |
| cell.py | CELL: cross-grid re-steps (bg_step, lin_step) with tau overlap checks (XI), Taylor models, exact residual quotient Q_theta (sympy, checked at random points: _sym_check), BR' per half, tube X-diameter, CH constants, float pre-pass + the 11 certificates per end, exact quadratic CC tests, LOO distance |
| node.py | node certificate (tube blob + sha, brackets, GREEN summary), controls XK and XU |
| assemble_w.py | job runner; POINTS (23 nodes) and CELLS (22) schedule; SEALED-<tag>.ok guard for N:/C: jobs |
| verdict_w.py | controls verdict; per-cell HOLDS / FAILED / INCONCLUSIVE / VOID; window verdict and largest closed union |
| steer.py | FLOAT steering only (finite differences, Chebyshev fits) |
| xc.py | control XC (FLOAT) |

Development scripts in dev/ are not instruments and are not on any proof path.

## Changes made during calibration (all before any sealed run)
1. hw3.count: the propagated columns are re-based after every step (an exact point matrix M; Y -> Y M), not only for
   the zero detection. Without it the L = 0 upper count at R = 20 near w+ was undecided at 7/4 (endpoint inertia).
2. XK and all cells use R = 20 (not 14): at R = 14 the Neumann cut moves the L = 0 crossing at w+ (7/4: 1.2043 ->
   about 1.199, both FD and certified), so XK at w+ - 0.002 read 4 instead of 3.
3. cell.tm_inv_r: python-flint `x ** n` of a positive interval can return a ball containing 0 (then 1/x^n = nan);
   replaced by repeated products. Rule recorded: no `**` on interval bases in denominators.
4. cell inner [0, r0] bounds: crude monomial bounds (Y0 = 2e-3, dominated by [0, r0]) replaced by Taylor models built
   from the exact series (Y0 = 4e-6 on the same cell).
5. cell.gap_of: frequencies below 0.05 (the w = 0 kernel) are not Krein drops (the first LOO run picked the region
   below the positive-Krein mode as the L = 0 gap).
6. LOO cells: the referee's example [7/4, 37/20] (width 0.1) does not close BR (Z1 = 1.17 on each half); the gates
   are [1597/1000, 33/20] with the R2-certified 161/100 tube and [31/20, 1597/1000] with the R2 tube of 1595/1000.
   [7/4, 37/20] is still run and reported (loo-185w).
7. green.SU reads an environment override (WSU) used only for one calibration experiment (s_u = 6, 12 both worse);
   the sealed runs must not set WSU (RUN.md asserts it).

## Lead decision 2026-11-19 (after the first report): XU split
8. node.xu gains optional jlo, jhi (scan a j-range of the same 0.01 grid; the other-sector drops are checked in the part
   with jlo = 1 only); assemble_w accepts XU:<tag>:<step>:<jlo>-<jhi>; verdict_w.xu_merge re-applies the pair rule to the
   union of the parts and requires the parts to tile j = 1 .. jmax exactly (same tube sha, same grid). The single-job
   path is unchanged. hw3.py, green.py, cell.py were NOT changed. Because node.py's hash changed, XK (nine nodes) and
   XU(1595) were rerun under the final hash (superseded outputs kept in out/controls/superseded/).
9. guard_test.py (new, test only): the seal guard refuses N:n1500 and C:c99 (non-window dummy tags) with exit 2.
10. **audit-W (seats/audit-W/AUDIT-W.md, FIX FIRST), all patches applied with the audit's patch text:**
   - green.py G-1: dQ includes 3|s| sum over degrees 2N+2..4N of |(p_sigma^2)_m| r0^(2m) (the truncated sigma^2 tail).
   - cell.py C-1: W1 = |tau_W'(R1)| + S Ab / kappa1 (linear growth of the W correction) in the exterior tau bound.
   - cell.py C-2: outward rounding on the decision path: H2up = up(ua U ub), |E| lower bound = -(up(ua U ub) + ...),
     Imax = up(arb((I1_a U I1_b).upper()).sqrt()), w-check uses it.exact(max(wa, wb)).
   - cell.py C-3: ch_constants takes the sup over [0, r0] (ips, ipu, ids, isl from inner_tms of both ends) into sup1,
     sup1p, sup0, sup0p and uses r0^2/2 ips^2, r0^3/3 ips^2, r0^2/2 ids^2, r0^3/3 ids^2 for the [0, r0] integrals
     (replacing the heuristic "first box x 4").
   - cell.py C-4: BR' item 2 checked: rho^a <= r_u^b and rho^b <= r_u^a, else failing step 'BR' ('halves disagree').
   - cell.py C-5: one-node check requires sigma_a(r_n) sigma_b(r_n) > 0.
   - cell.py C-6: a missing float w2 is recorded as INCONCLUSIVE step 'CPOS' (no crash).
   - cell.End: assert R1 > R + 1 (hw3.gram quadrature must reach Rc). hw3.py itself unchanged.
   - node.py N-1: node ok requires brackets_ok: K at R = 14 via build-3 verdict.K_of equal to (2, 2, 2, 0) and
     verdict.consistency empty.
   - assemble_w.py: N:/C: jobs assert WSU unset.
   - verdict_w.py: FAILED-by-brackets rule (node brackets_ok); XC must be exactly the 5 sealed points.
   - DESIGN-W3 amendment W3-A1: EXT sign, BR' item 2 condition, XI scope, c != 0 remark, no bisection; mirrored in
     BAR-W1. Every control was rerun once under the final hashes (superseded outputs in out/controls/superseded*/).
11. verdict_w.xu_merge: parts must tile j = 1 .. jtop; jtop excludes grid points within XU_TOP_MARGIN of w_max.
    XU_TOP_MARGIN = 0 (the sealed strict rule: every grid point counts). A margin of 1e-3 was coded and run once as a
    diagnostic, then set back to 0: changing it would change the control after seeing data, which is the lead's call.
    verdict_w only reads JSON, so no control was rerun for this change.
12. Lead decision on XU-1985 (pre-seal, set after seeing the XU-1985 data; disclosed in BAR-W1): verdict_w
    XU_TOP_MARGIN = 1e-3 (cells never count above max w+ = 1.4641 while |E| >= 1.9) and the single-point re-count rule
    (new recount.py; an undecided point counts only if a same-w, same-tube re-count at a finer level decides both
    counts). Only verdict_w controls and the one re-count job were run after this change.
