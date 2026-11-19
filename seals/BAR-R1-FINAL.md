# BAR-R1-FINAL (FOR SEALING): certified spectral stability of the n=1 repulsive GPP state at sigma0 = 1.80

Prepared by seat build-1, 2026-11-18, for the lead to seal. Design: DESIGN-R1-v3.md (this folder). Supersedes
BAR-R1-DRAFT.md and applies every blocking fix of REFEREE-R1-v2.md.

**Disclosure for the seal log.** The predictions below were written after the float smokes (SMOKE-R1.md,
SMOKE-R1-v2.md) and after reading the float values printed by referee-1 and referee-2. They are mock-informed
predictions, not blind ones. The verdict on T is a certificate, so a mock-informed prediction cannot move it; what is
pre-registered here is the reading of every outcome. This seat did not read TARGETS-R1*.md. The controls were run as
calibration before sealing (CALIBRATION.md); nothing at sigma0 = 1.80 was run except the background tube and its
virial identity.

## In plain words
A ball of ultralight dark matter with one hollow shell inside is claimed, from one group's numerics, to survive every
small shake. We test that claim at one fixed point of the claimed survival window. "Survive" means that no linear
perturbation, of any shape, grows exponentially. For each shape the computer counts, with proof, the directions in
which the energy goes down, and then accounts for every one of them by an oscillation that is proved not to grow.
The claim is refuted only if the computer encloses, with proof, a perturbation that grows. Anything in between is
reported as inconclusive. The test says nothing about large shakes (nonlinear or orbital stability).

## Inputs fixed
- System: 2402.07998 eqs. (9), (32), (35)-(37), (43); repulsive sign; dimensionless units of that paper; alpha = 1.
  n = 1. **sigma0 = 1.80 exactly** (fixed by the R1 brief before any count was seen).
- Background tube: R1 = 26, 320-bit arb, Taylor order 56, u0 bracket half-width 1e-50, series start r0 = 1e-5.
- Brackets: R = 10 and R = 14, eps = 1e-3, linear precision 200 bits, Taylor order 24.
- Krein matching: r_m = 8, tail start R1 = 26, far-field radius Rfar = max(2 R1, 30 m/|kappa^2|), Riccati order N = 10, Cauchy disc radius 0.002.
- Newton starting guesses (not predictions): w = 1.1048, 0.5400, 0.2968 (negative Krein, L = 0, 1, 2);
  1.2618, 0.9511, 0.5179 (positive-Krein controls).

## Pre-registered predictions (scored MATCH / MISS; descriptive, mock-informed)
- **P1 (counts).** At both R = 10 and R = 14, certified: upper#(L+ < +eps) <= (2, 2, 1, 0) and upper#(L- < +eps)
  <= (2, 1, 1, 0) for L = 0, 1, 2, 3; lower#(L+ < -eps) >= (2, 1, 1, 0) and lower#(L- < -eps) >= (1, 1, 1, 0).
- **P2 (constraint).** Node D0: n(B) = 2, d2 < 0, M |d2| > 1 at both radii, so n(L+(0) on (r sigma)^perp) <= 1.
  D1 = 3m/4 > 0 with m enclosed.
- **P3 (index).** K(0) <= 2, K(1) <= 2, K(2) <= 2, K(3) = 0 (definitions in DESIGN-R1-v3 node K).
- **P4 (Krein).** For L = 0, 1, 2 the Krawczyk test contracts around the guess, the certified w lies in (0, \|E\|),
  and <a, d> < 0 is certified. Descriptive location: L=0 in [1.0, 1.2], L=1 in [0.45, 0.65], L=2 in [0.2, 0.4];
  an eigenvalue outside these intervals with certified <a, d> < 0 still MATCHES (the sign is what is scored).

## Outcome of T (one of four; verdict.py target)
- **VOID** if any of: a must-pass control below fails; the background node B is not certified (zeros != 1, tail not
  certified, existence not certified, virial relative residual enclosure > 1e-6); an internal inconsistency
  (upper count < lower count at the same L and R; K(L) < 2 at an L = 0, 1, 2 with a certified negative-Krein pair, which
  would contradict IDX); a co-batched positive-Krein control not certified positive; C-R or C-W fails at sigma0 = 1.80.
- **FAILED (claim refuted)** if evans.py returns a Krawczyk-certified eigenvalue with Re lambda > 0 (lower end of the
  real-part enclosure > 0) in some sector at sigma0 = 1.80. This is the only kill condition. **No parity theorem is
  used: an odd K is never read as a growing mode.** The refutation search runs only if the stability certificate does
  not close, started from the float eigenvalues of that sector.
- **HOLDS** if not VOID and K(0), K(1), K(2) <= 2, K(3) = 0, D1 > 0, and I0, I1, I2 all certified (w in (0, \|E\|),
  <a, d> < 0). Then N_r = N_c = 0 at L = 0, 1, 2 (IDX), and L+-(L) >= eps > 0 for L >= 3 (TAIL), so no eigenvalue of
  J L has Re lambda > 0 in any (L, M) sector (SECT): linear (spectral) stability at sigma0 = 1.80.
- **INCONCLUSIVE** otherwise: an upper count above the bar, a <a, d> enclosure straddling 0, a Krawczyk test that does
  not contract, a tail lemma that does not close, without a certified Re lambda > 0 eigenvalue.

## Controls (must pass, else VOID). Comparators as implemented in verdict.py
- **C-B1 (CALIBRATION, not a test).** Attractive n = 0 background engine against 2402.07998 Fig. 5. The sigma0 values
  0.191 and 1.047 were matched POST HOC from referee floats, so the T windows are a calibration. At sigma0 = 0.191:
  T in [0.555, 0.561] and F in **[0.0465, 0.0475]** (rounding of the printed 0.047). At sigma0 = 1.047: T in
  [5.62, 5.66], F in [1.875, 1.900]. Virial relative residual enclosure <= 1e-6. For s = -1 the existence step of the
  tube is not certified (escape is not permanent for the attractive sign); this is stated, not hidden.
- **C-B2.** Schroedinger-Poisson E1/E0 at equal particle number (E/N^2 is scale invariant) in [0.1884, 0.1896]
  (math-ph/0208045 Table 1 rounding).
- **C-P1.** Repulsive n = 0 at sigma0 = 1.80: K(L) = 0 for L = 0..3 at R = 10 and 14 (so no growing mode at any L by
  IDX), through the same pipeline.
- **C-P2.** SP n = 1, L = 0: K(0) <= 2 certified at R = 20 and 28, and one Krawczyk-certified eigenvalue with
  Re lambda > 0 and Im lambda != 0 (a quartet, 2 negative directions) => exactly one quartet. Its value:
  Re lambda/(2\|E1\|) in [0.04059, 0.04961] (within 10% of 0.0451) and \|Im lambda\|/(2\|E1\|) in [0.31525, 0.33475]
  (within 3% of 0.325) (math-ph/0208045 Table 3; factor 2 from units, 2310.18405 lines 107-112).
  **Tolerance disclosure:** the 10% real-part gate was set after a 7% float mismatch (0.0482 vs 0.0451) had been seen;
  it is mock-informed. The 3% imaginary gate is set by the 2-digit source.
- **C-P3.** SP n = 1, L = 2: K(2) <= 1 certified at R = 20 and 28, and one Krawczyk-certified REAL eigenvalue lambda > 0
  (disc centred on the real axis; uniqueness plus conjugate symmetry) => exactly one real growing pair, matching
  2310.18405 Fig. 4 right panel and line 981. No parity is used.
- **C-R.** At sigma0 = 1.80 the brackets at R = 10 and R = 14 return identical certified counts (upper and lower, both
  operators, L = 0..3) and the same D0 result.
- **C-W.** At sigma0 = 1.80, R = 14: the w-Neumann exterior L = 0 Schur form is certified unbounded below
  (Q(X) = q_a(phi) - 2 s0^2 X < 0 at the printed X, slope -2 s0^2 < 0).
- **Positive-Krein co-batched controls (PK0-PK2).** In the target run, at the neighbours of the negative-Krein
  eigenvalues, krein.py must certify <a, d> > 0.
- **Null N1.** sigma0 = 0.50 (outside the band): evans.py must certify an eigenvalue with Re lambda > 0 at L = 0
  (float 0.0241 +- 0.2832 i). If it does not, the run is VOID. K(2) at sigma0 = 0.50 is reported only (descriptive).

## Descriptive only (reported, not scored)
- delta, the exterior margin \|E\| - m/R - delta, and eta at both radii; d2 against (1/2) dm/dE; the certified w and
  <a, d> enclosures; Krein separations; theta, mu, Tt of the tail lemma; the regime map to 2506.06442 and 2611.08602.

## Seal fields
```
formula_ref: <LAB-ROOT>/seats/frontier/dl/2402.07998.txt:745-757, <LAB-ROOT>/seats/frontier/dl/2402.07998.txt:822-861, <LAB-ROOT>/seats/frontier/dl/2402.07998.txt:955-971, <LAB>/build-1/DESIGN-R1-v3.md:42-73
calibrated_on: none - first bar of this raid; control windows from published tables (C-B2, C-P2, C-P3) and post-hoc calibration (C-B1); calibration run recorded in CALIBRATION.md
depends_on: none - no settled bar yet in DARK-2026-11-18
null_not_symmetry: sigma0 = 0.50 is a different background (outside the claimed band), not a relabel or a sign flip; it changes the answer from 0 to >= 1 growing mode
target_form: integer upper/lower counts per (L, R); n(B), d2 sign; Krawczyk enclosures of w and certified sign of <a,d> per L = 0, 1, 2; T in {HOLDS, FAILED, INCONCLUSIVE, VOID}
parameters: sigma0 = 1.80 fixed - single-point claim by design; R = 10, 14; eps = fixed - counts are rigorous for every eps > 0, value 1e-3; r_m = fixed - matching radius only moves enclosure widths, value 8; R1 = fixed - tail radius, C-R checks radius independence, value 26; precisions 320 (tube) / 200 (linear) bits
instruments: itaylor.py, bg_tube.py, lincore.py, bracket.py, tail.py, match.py, kraw.py, krein.py, evans.py, assemble.py, verdict.py
tolerances: counts are taken at +-eps = 1e-3 (rigorous for every eps > 0); all other outputs are interval enclosures read by sign or by window containment; C-P2 10% real-part gate is mock-informed (disclosed)
ceiling: the certificate is all-or-nothing per sector; best possible = HOLDS with every upper count equal to its lower count (exact indices) at both radii
toy_model: C-P1 (n = 0, same sigma0), C-P2/C-P3 (SP n = 1, published counts and values), CAL-K (SP n = 1, L = 1 Krein signs) through the same engine
positive control: C-P2 and C-P3 (published Schroedinger-Poisson n = 1 instabilities recovered with certified eigenvalues) and null N1 (sigma0 = 0.50 must show a certified growing mode)
baseline: the incumbent is the float stability claim of 2402.07998 (no certified count exists); the dumb baseline is C-P1, the n = 0 state, which must show zero negative directions beyond the trivial ones
run_command: four runs, each under memcap and under 30 min: assemble.py target-B ; assemble.py target-K0 ; assemble.py target-K1 ; assemble.py target-K2 ; then verdict.py controls ; verdict.py target   (assemble.py refuses any target job until SEALED.ok exists)
projected_target_time: target-B 1-2 min; target-K0, K1, K2 about 5-8 min each (20-25 min compute, each run < 30 min); Krawczyk first boxes 1e-9, 1e-10, 1e-8, 1e-7 relative with epsilon-inflation
```
