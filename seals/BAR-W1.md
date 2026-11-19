# BAR-W1 (DRAFT for the lead to seal): the one-node repulsive GPP core is spectrally stable for EVERY sigma0 in [1597/1000, 1983/1000]

Seat build-W, raid R3-WINDOW, 2026-11-19. Design: window/design/DESIGN-W3.md (supersedes W2 where it says so).
Instruments: window/build-W/ (RUN.md lists sha256 and commands). Pre-seal controls and calibration:
window/build-W/CALIBRATION.md. Nothing inside the window was certified pre-seal except the controls named below,
which are controls by design (the two leave-one-out cells and the injected-tau cell; all their ends are R2-certified
points).

## Claim (sealed)

For every sigma0 in [1597/1000, 1983/1000] there is a decaying one-node solution Sigma(sigma0) of the GPP system
(arXiv 2402.07998, alpha = 1, s = 1) with sigma(0) = sigma0, continuous in sigma0, equal to the certified node state
at each node and unique in the X-ball of radius r_u (per half-cell, recorded) around the Hermite predictor H_theta
(and, at the nodes, unique among decaying solutions in the node tube); for each of these states the spectrum of
J L on L^2(R^3; C^2) has no point with Re lambda > 0. In words: spectrally stable along the BR branch, unique in the
stated ball. Not claimed: uniqueness outside the ball; the edges (they remain the R2 brackets); nonlinear stability.

## Schedule

Nodes (23): 1597/1000, 1600/1000, 1605/1000, 1612/1000, 1625/1000, 33/20, 1675/1000, 17/10, 1725/1000, 7/4,
1775/1000, 9/5, 1825/1000, 37/20, 1875/1000, 19/10, 1925/1000, 39/20, 1962/1000, 1970/1000, 1976/1000,
1980/1000, 1983/1000 (assemble_w.NODES; tags n1597 ... n1983). Cells (22): consecutive pairs (c01 ... c22), every
cell at count radius R = 20.
Per node (job N:<tag>): certified tube (bg_tube unchanged, R1 = 26, prec 320, K 56, d = 1e-50), its JSON blob and
sha256, R1 brackets at R = 10, 14 (bracket.run unchanged), GREEN (alpha != 0, c != 0, tau checks, ||G_a||).
Per cell (job C:<id>): cell.run_cell with both node tubes read from the node blobs (sha checked).

## Per-cell outcome rules (verdict_w.py)

- HOLDS: BR' closes on both halves (Z1max < 1, self-map with rho_max, kappa(r_u) < 1, rho_max <= r_u), the tube
  X-diameters of both nodes are below r_u, one node and E < 0 at r_n, all 11 certificates at both ends are certified
  (CPOS H(w2) L = 0, 1, 2; RITZ H(w1) L = 0, 1, 2; CPOS H(0) L = 0, 1, 2 with k = 4, 3, 2 block vectors; count H(0)
  L = 3; PEN), every CC quadratic test passes (eta2 / eta2' / eta2 + M' Gam constants of DESIGN-W3 3.5), and the
  w-checks 0 <= w1 < w2 < |E(sigma0)| hold at both ends.
- INCONCLUSIVE: any of the above does not close; the failing step is recorded ("no drop L<n>", "BR" incl. "halves
  disagree", "CPOS", "RITZ", "K-row", "PEN", the certificate name for a CC failure). There is NO bisection under this
  bar (DESIGN-W3 amendment A1.5): a cell that does not close stays INCONCLUSIVE and the fallback below applies.
- FAILED: an end node is not certified (existence, n = 1 zeros, tail) or its R = 14 brackets do not give
  K = (2, 2, 2, 0) with consistent counts (node.py brackets_ok, build-3 verdict.K_of / consistency).
- VOID: a must-pass control (below) failed or is missing; a cell's tube sha differs from its node record; a cell job
  REJECTED its node data.
Window verdict: HOLDS on [1597/1000, 1983/1000] iff all 22 cells (or their sealed bisection) HOLD. Otherwise the
fallback is reported: the largest closed union of consecutive HOLDS cells (all components listed; SCOPE's second
outcome), plus each failing cell with its failing step. No goalpost moves: margins, R, levels and the pre-pass rules
are fixed by the sealed code.

## Controls (must pass, else VOID) - all already run pre-seal, results in CALIBRATION.md

1. XK at the nine G9 nodes: lower = upper at w- -+ 0.002 and w+ -+ 0.002, drop exactly 1 across w-, rise exactly 1
   across w+, kernel booked at w = 0: (upper, lower) = (4,3), (3,2), (2,2).
2. XU at 1595/1000 (L = 0) and 1985/1000 (L = 2): no pair w1 < w2 on the grid 0.01 j with lower(w1) - upper(w2) >= 1 in
   the named sector, no undecided count, the designed drop certified in the other two sectors (1985/1000 as j-range
   jobs merged by verdict_w.xu_merge). Rule SET AFTER SEEING XU-1985 DATA (pre-seal, lead decision): the scan runs
   over w = 0.01 j < w_max - 1e-3 (w_max = |E| - m/R - delta_L(R) - 1e-5 at the control node); an undecided scan point
   is re-counted at the same w with finer levels (recount.py: 1e-6, 1e-7; same tube sha) and counts only if both
   re-counted counts are decided; no neighbour-based exclusion. Why the top margin is irrelevant to IDXC as used:
   the cells count only at w1 < w2 <= max w+ = 1.4641 (largest certified positive-Krein frequency over the nine G9
   nodes, L = 0, 1, 2), while |E(sigma0)| >= 1.9 along the branch (certified BR bound, e.g. 1.9058 on LOO-161), so the
   target never counts within 0.4 of |E|, far beyond 1e-3.
3. LOO gates: [1597/1000, 33/20] with the tube of 161/100 (theta = 13/53) and [31/20, 1597/1000] with the tube of
   1595/1000 (theta = 45/47): BR closes, the interior certified tube lies in the BR ball of its half (X-distance <=
   rho_max), tube diameters < r_u.
4. XI: tau_b + 1e-3 bump (a and W, Gaussian at r = 3) injected into node b's tau data must be REJECTED. Scope
   (DESIGN-W3 A1.3): the overlap check proves that tau data are a solution of the ODE on the steps used, not that they
   are tau (tau + eps Z1 would pass); the identity of tau rests on provenance (GREEN recomputed in-process from the
   sha-checked node tube in every cell job).
5. XC (float): 5 interior points/sectors, lowest eigenvalue on the common subspace inside [chord - eta2, chord + eta2'].
   Exactly these 5 points (verdict_w checks the set).
6. R1REG: R1 brackets at 9/5 equal build-3/out/r1 (and the same tube sha). [PASS]
A control is rerun if any instrument sha changes (RUN.md). Results: CALIBRATION.md (final hashes).
7. Seal guard (guard_test.py): N:n1500 and C:c99 (no seal files, non-window tags) exit 2 with REFUSED.

## Disclosures

- Mock-informed: the float margins (PROBES P8, P11c), the float BR constants (P11b), the design probes, and every
  control above were run before this seal by the same seat that wrote this bar; the CC margin fractions (0.7, fallback
  0.35 of the float margin), R = 20 and the gap rule (frequencies > 0.05) were set after seeing calibration runs
  (PATCHES.md items 1-6). The audit-W patches (PATCHES.md item 10) were applied before the final control batch.
- The LOO-161 full cell (all 11 certificates at both ends, an R2-certified-point cell overlapping the window) was run as
  a pipeline and cost test: every certificate is certified, BR closes, and the only failing CC test is H(w2) L = 0 at
  the 1597/1000 end (certified margin 5.0e-5 against C0 = 9.0e-5 from rho_max = 2.2e-6 on this 0.053-wide cell).
  It is a control, not a window result. The window cell c01 = [1597/1000, 1600/1000] is 18 times narrower
  (Y0 ~ Delta^4): its C0 is expected below 1e-9; this is a projection, not a measurement.
- The referee's LOO example [7/4, 37/20] (width 0.1) does not close BR (Z1 = 1.17 on each half): reported, not a gate.
- Tube reuse in LOO (accepted by the lead as controls): the LOO gates use certified tubes at the R2 calibration point
  161/100 and the R2 unstable point 1595/1000, and the ends 31/20, 1597/1000, 33/20, all independent of the schedule
  nodes. 161/100 lies INSIDE the window; its tube is used only as a control comparison object, never as a schedule
  node certificate, and no statement of this bar rests on it.
- R1REG read the 9/5 tube from the seat's disk cache; the sha equals the R1 tube f8b0cc27...; XK built all nine
  tubes in-run and reproduced the R2 shas.
- Float steering (steer.py, the pre-pass in cell.py) chooses w1, w2, the explicit vectors and trial functions inside
  every sealed cell job, deterministically; floats never decide a certificate.
- XU rule disclosure: the XU top margin (1e-3) and the single-point re-count rule were set by the lead after the
  XU-1985 scan showed two non-decided points (w = 2.27: upper count undecided at levels 1e-5 and 1e-6, decided 4/4 at
  1e-7; w = 2.59, 5.5e-4 below w_max: the count did not finish in 900 s). No drop pair exists anywhere on the scan.
- Open referee items (DESIGN-W3 section 8): Lemma G, EXT constants, BR' items 2-3, the Z2hat profile. The seal should
  wait for that referee pass or carry it as a named dependency.

## Seal fields
```
formula_ref: <LAB>/window/design/DESIGN-W3.md:51-160
calibrated_on: CALIBRATION.md controls only (XK at the nine G9 nodes, XU at 1595/1000 and 1985/1000, LOO on [1597/1000, 33/20] and [31/20, 1597/1000], XI, XC float, R1REG); no window node or schedule cell was certified pre-seal
depends_on: 3ad051728e
null_not_symmetry: XU uses 1595/1000 and 1985/1000 (certified unstable points, a different answer: no drop in the named sector), XI uses injected non-kernel tau data (must be refused), LOO uses independent certified tubes at 161/100 and 1595/1000 (not relabels)
target_form: per cell: BR constants (Y0, Z1, Z2hat, rho_max, r_u, kappa) per half, tube diameters, 11 certificates per end with certified margins, CC booleans, w-checks, outcome in {HOLDS, FAILED, INCONCLUSIVE, VOID}; window: HOLDS on [1597/1000, 1983/1000] or the largest closed union of HOLDS cells
parameters: sigma0 nodes = fixed - the sealed schedule, value the 23 rationals of assemble_w.NODES; R = fixed - XK showed R = 14 moves the L = 0 crossing at w+, value 20; s_u = fixed - norm of DESIGN-W2 (s_u = 6, 12 both gave larger Z1), value 3; om = fixed - DESIGN-W2 weight, value 1 + (r/4)^2; r_x = fixed - match radius of GREEN, value the tube grid point nearest 8; theta sub-intervals = fixed - envelope resolution only, value 8 per half; CC margin fractions = 0.7, 0.35; Chebyshev degree = 30, 40 (first with relative fit error < 1e-3, else 50); M' = fixed - DESIGN-W2 CPOSL (d), value 5; K = fixed - Taylor order of all linear steps and Taylor models, value 24; precision = fixed - 320 bits (tube), 200 bits (linear), 64 bits (kernel sums)
instruments: itaylor.py, bg_tube.py, lincore.py, bracket.py, hw3.py, green.py, cell.py, node.py, assemble_w.py, verdict_w.py, steer.py, xc.py
tolerances: counts and margins are certified by sign; levels 1e-5 (XK, XU) and 1/1000 (brackets) are rigorous for every level > 0; CC decided by exact quadratic tests on 64 sub-intervals; no float enters a decision
ceiling: all 22 cells HOLD: stability proved for every sigma0 in [1597/1000, 1983/1000] as one interval (the complete proved stable window between the R2 edge brackets)
toy_model: the LOO-161 full cell (CALIBRATION.md) and the XK nodes
positive control: XU at 1595/1000 and 1985/1000 (certified unstable points must give no drop in the named sector) and XI (bad node data must be refused)
baseline: the nine certified points of R2 (3ad051728e and its R2 bar) and the float band of 2402.07998; the dumb baseline is a pointwise grid with no statement between the points
run_command: cd <LAB>/window/build-W ; verdict_w.py controls (must print all_pass true) ; for each node tag: echo sealed > SEALED-<tag>.ok ; assemble_w.py N:<tag> ; for each cell c01..c22: echo sealed > SEALED-<cid>.ok ; assemble_w.py C:<cid> ; verdict_w.py window   (each under memcap 8, each under 30 min, at most two at once, WSU unset)
```
