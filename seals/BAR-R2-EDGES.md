# BAR-R2-EDGES (DRAFT FOR SEALING): certified edges and a certified grid of the stability band of the one-node repulsive GPP state

Prepared by seat build-3, 2026-11-18, for the lead to seal with `depends_on 07faff6621`. Scope:
core/band/SCOPE.md (R2-BAND). Instruments: build-3/*.py, with sha256 in build-3/RUN.md. Changes from build-2 are in
build-3/PATCHES.md, and the control rerun is in build-3/CALIBRATION.md. This seat did not read TARGETS-R1*.md.

**Disclosure for the seal log.** The predictions below are mock-informed, not blind. They are read off the NOT SEALED
float map (core/band/map/MAP.md, MAP.json, edge_*.json, sw_f*.json). This seat also saw:
- the certified R1 result at 9/5 (build-2/out/target-*), re-run here as a regression;
- certified runs at the non-target point sigma0 = 161/100: the timing probe B:p161, whose counts equal the 9/5
  counts, and the separation control K0:p161 (L = 0: w- = 1.008777081, sign -; w+ = 1.042587431, sign +);
- two certified Evans runs at the non-target points 3/2 and 41/20 (the positive controls C-U150 and C-U205).

The lead added in-155 and in-200 on 11-18 at the prior-art gate's request. Their guesses are existing float-map rows
(chk_1.55_0.json and sw_f2.json at 2.00). An earlier calibration plan used 31/20 as a control. It was dropped before
any run at 31/20, and nothing at 31/20 or at 2 was run in certified form.

No proposed point was run, in float or certified form. The float Newton guesses for the proposed points were
interpolated or edge-fitted from existing float-map rows (build-3/aux/b3guess.py), not computed at those points. The
verdict at each point is a certificate, so a mock-informed prediction cannot move it. What is pre-registered here is
the reading of every outcome.

## In plain words
A float computation says that the one-shell dark-matter core is stable only for sigma0 between about 1.59631 and
1.98413. Below that window one oscillation (spherical, L = 0) starts to grow. Above it, an L = 2 oscillation does.
At each edge, two oscillations of opposite energy sign meet and turn into a growing pair. This bar asks the computer
to prove four things:
- just outside each edge (1.595 and 1.985), that a growing mode really exists;
- just inside each edge (1.597 and 1.983), that nothing grows;
- the same "nothing grows" at six points across the window;
- at the two inner points, that the two nearly colliding oscillations are certified as two different modes with
  opposite energy signs.

Each point is its own all-or-nothing certificate.

## Inputs fixed (every point)
- System and units: as BAR-R1-FINAL (2402.07998 eqs. (9), (32), (35)-(37), (43); repulsive; alpha = 1; n = 1).
- Background tube: R1 = 26, 320-bit arb, Taylor order 56, u0 bracket half-width 1e-50, r0 = 1e-5 (binary64).
- Brackets: R = 10 and R = 14, eps = 1/1000 exactly, 200 bits, Taylor order 24.
- Krein and Evans matching: r_m = 8, Riccati order N = 10.
- Cauchy disc:
  - K jobs: disc_r = min(0.002, gap/4), where gap = |pos guess - neg guess| of that sector;
  - U jobs: disc_r = min(0.002, Re(guess)/2).
- sigma0 enters every enclosure as the exact rational, through itaylor.exact. assemble.py asserts the read-back for
  every point.

| tag | sigma0 (exact) | mode | Newton guesses (float; not predictions) |
|---|---|---|---|
| lo-u | 1595/1000 | unstable, L = 0 | lam = 0.0051617 + 1.0137197 i |
| lo-s | 1597/1000 | stable | L0 (1.01157, 1.01906); L1 (0.4543, 0.80839); L2 (0.20178, 0.49162) |
| hi-s | 1983/1000 | stable | L0 (1.21808, 1.4641); L1 (0.62237, 1.088); L2 (0.45398, 0.47273) |
| hi-u | 1985/1000 | unstable, L = 2 | lam = 0.0082411 + 0.4639756 i |
| in-155 | 31/20 | unstable, L = 0 | lam = 0.029367442 + 0.978168536 i (chk_1.55_0.json) |
| in-200 | 2 | unstable, L = 2 | lam = 0.035387296 + 0.468617454 i (sw_f2.json, sigma0 = 2.00) |
| g165 | 33/20 | stable | L0 (1.02312, 1.0926); L1 (0.47605, 0.84468); L2 (0.22398, 0.50082) |
| g170 | 17/10 | stable | L0 (1.04814, 1.14914); L1 (0.49696, 0.87953); L2 (0.2464, 0.50821) |
| g175 | 7/4 | stable | L0 (1.07581, 1.20427); L1 (0.51825, 0.91498); L2 (0.27053, 0.51407) |
| g185 | 37/20 | stable | L0 (1.13497, 1.31444); L1 (0.56197, 0.98767); L2 (0.32601, 0.5191) |
| g190 | 19/10 | stable | L0 (1.16574, 1.37016); L1 (0.58438, 1.0249); L2 (0.35967, 0.51598) |
| g195 | 39/20 | stable | L0 (1.1971, 1.42652); L1 (0.60715, 1.06272); L2 (0.40233, 0.50402) |

Pairs are (negative-Krein w, positive-Krein partner w). The partner is the next mode above, which is the colliding
mode at the edge sectors. Guess gaps at the two inner edge points:
- L = 0 at 1597/1000: 0.0075, so disc_r = 0.00187;
- L = 2 at 1983/1000: 0.0187, so disc_r = 0.002.

The brief's "~0.011" for L = 2 at 1.983 does not match the float map. Its fit gives 0.0187, consistent with 0.0249
at hi - 0.002 and the square-root law. At every other point and sector, disc_r = 0.002 (the R1 value).

## Pre-registered predictions (scored MATCH / MISS; descriptive, mock-informed)
- **P1 (counts; every stable point; R = 10 and 14).**

  | count | L = 0 | L = 1 | L = 2 | L = 3 |
  |---|---|---|---|---|
  | upper#(L+ < +eps) | 2 | 2 | 1 | 0 |
  | upper#(L- < +eps) | 2 | 1 | 1 | 0 |
  | lower#(L+ < -eps) | 2 | 1 | 1 | 0 |
  | lower#(L- < -eps) | 1 | 1 | 1 | 0 |

  These are the 9/5 counts. The float map has n(L+-) constant on [1.3, 2.4] for every L. C-R: identical counts at
  both radii.
- **P2 (constraint; every stable point).** D0: n(B) = 2, d2 < 0 and M |d2| > 1 at both radii, so
  n(L+(0) on (r sigma)^perp) <= 1. D1 = 3m/4 > 0. (Float VK < 0 throughout the band.)
- **P3 (index; every stable point).** K = (K(0), K(1), K(2), K(3)) = (2, 2, 2, 0), using the definitions of
  DESIGN-R1-v3 node K and verdict.py K_of.
- **P4 (Krein; every stable point).** For L = 0, 1, 2:
  - the negative-Krein certificate contracts, w lies in (0, |E|), and <a, d> < 0 is certified;
  - the co-batched positive-Krein certificate contracts with <a, d> > 0;
  - the separation record is ok: each w lies within gap/4 of its own guess, the two certified w enclosures are
    disjoint, and each Cauchy disc stays clear of the other mode (disc_r sqrt 2 < the certified distance).

  Descriptive location: within 1e-3 of the negative guess (5e-4 at the two inner edge points). A miss in location
  with the right sign still MATCHES; the sign is what is scored.
- **P5 (growth; each unstable point).** U job: a Krawczyk-certified eigenvalue lam with lower end of Re lam > 0 in
  the named sector, at L = 0 for 1595/1000 and L = 2 for 1985/1000. Descriptive location:
  - 1595/1000: Re lam in [0.004, 0.0065] and Im lam in [1.012, 1.016];
  - 1985/1000: Re lam in [0.0065, 0.010] and Im lam in [0.462, 0.466].

  These windows are about +-20 % in Re around the float square-root fits and are not scored.
- **P5b (inside the paper's band; lead addition).** U job at in-155 and in-200: a Krawczyk-certified eigenvalue
  with lower end of Re lam > 0, in sector L = 0 at 31/20 and in sector L = 2 at 2. Descriptive location: within 1e-4
  of the float guess in Re and Im. The float values agree to 9 digits at three resolutions at 1.55 (MAP.md section 3).
  Both points lie inside the paper's claimed common band "1.55 <~ sigma0 <~ 2.07" (2402.07998.txt:1073, :1124).
  31/20 is its lower endpoint, which "<~" includes. HOLDS at either point proves that the paper's band, read as
  stated, contains a linearly unstable state.
- **P6 (edges; derived, scored with the four edge points).**
  - If lo-u and lo-s both HOLD: certified instability at 1595/1000 and certified stability at 1597/1000. The lower
    edge is bracketed as [sigma_lo-, sigma_lo+] = [1595/1000, 1597/1000] (float edge 1.5963117 inside).
  - If hi-s and hi-u both HOLD: the upper edge is bracketed as [1983/1000, 1985/1000] (float edge 1.9841288 inside).
  - A MATCH also needs the mechanism. The lower-side certified eigenvalue is non-real (|Im| lower end > 0), and so
    is the upper-side one: a quartet, as for a Krein collision. Real crossings are excluded only in this weak
    descriptive sense (counts unchanged across the edge; non-real growing eigenvalue).

## Outcome per point (verdict.py point <tag>; one of four)

**Stable points** (lo-s, hi-s, g165, g170, g175, g185, g190, g195). This is the R1 target rule unchanged, plus two
VOID reasons (the one-sha check and the separation check).
- **VOID** if any of these holds:
  - a must-pass control fails (C-B1, C-B2, C-P1, C-P2, C-P3, NULL, C-U150, C-U205);
  - the background node B is not certified (zeros != 1, tail not certified, existence not certified, or virial
    relative residual upper end > 1e-6);
  - an internal inconsistency (upper < lower at the same L and R; or K(L) < 2 at L = 0, 1, 2 with a certified
    negative-Krein pair);
  - a co-batched positive-Krein control is not certified positive;
  - C-R or C-W fails at that point;
  - the five outputs (B, brackets, K0, K1, K2) do not report one tube_sha256;
  - both Krein certificates of a sector contracted, but the separation record is not ok.
- **FAILED (point refuted)** if evans.py returns a Krawczyk-certified eigenvalue with Re lambda > 0 (lower end > 0) in
  some sector at that point. This is the only kill condition, and no parity theorem is used. The refutation search
  runs only if the stability certificate does not close. It starts from the float eigenvalues of the failing sector,
  and its output goes to out/<tag>/refute.json.
- **HOLDS** if the point is not VOID and all of these hold:
  - K(0), K(1), K(2) <= 2 and K(3) = 0;
  - D1 > 0;
  - I0, I1 and I2 are all certified (w in (0, |E|), <a, d> < 0).

  Then, by IDX, TAIL and SECT exactly as in PROOF-R1-v2 section 9.2, there is no eigenvalue of J L with
  Re lambda > 0 in any (L, M) sector: linear (spectral) stability at that sigma0.
- **INCONCLUSIVE** otherwise, with no certified Re lambda > 0 eigenvalue. Examples: an upper count above the bar, a
  <a, d> enclosure straddling 0, a Krawczyk test that does not contract, or a tail lemma that does not close.

**Unstable points** (lo-u, hi-u, in-155, in-200).
- **VOID** if a must-pass control fails (same list), if the background node B is not certified, or if B and the
  evans build do not report one tube_sha256.
- **HOLDS** if evans.py returns a Krawczyk-certified eigenvalue with lower end of Re lambda > 0 in the named sector.
  This proves linear instability at that sigma0 (an L^2 eigenvector of a growing mode; PROOF-R1-v2 Lemma 5.9 and
  consequences, complex form).
- **FAILED** cannot be returned by this bar. Refuting "unstable at sigma0" needs a stability certificate at that
  point, which is a stable job set under its own seal. It is stated here so that INCONCLUSIVE is never read as a
  refutation.
- **INCONCLUSIVE** otherwise: Krawczyk does not contract, or the real-part enclosure contains 0.

**Edge reading.** An edge bracket is claimed only when both of its points HOLD. If one edge point is INCONCLUSIVE,
that edge is reported unbracketed and the other points stand alone. A VOID point voids only itself, except that a
failed must-pass control voids every point.

## Controls
- **Must pass (else every point is VOID).**
  - C-B1, C-B2, C-P1, C-P2, C-P3 and NULL, exactly as sealed in 07faff6621 (windows in BAR-R1-FINAL; comparator
    verdict.py controls), re-run with build-3.
  - **C-U150** (new). U job at sigma0 = 3/2, L = 0: a certified eigenvalue with Re lambda > 0 and the background
    certified.
  - **C-U205** (new). The same at 41/20, L = 2.

  Both new controls are outside the float band, at points that are not sealed candidates. The float map has
  0.040313 + 0.939259 i at 1.50 (L = 0) and 0.073524 + 0.484146 i at 2.05 (L = 2). They are positive controls for the unstable route on this family at R1 = 26, r_m = 8
  (comparator verdict.py controls-r2).
- **Per point (stable).** C-R (R = 10 vs 14), C-W at R = 14, PK0-PK2 co-batched, the separation records, one
  tube sha.
- **Instrument calibration (not BAR controls).**
  - CAL-K as in R1.
  - CAL-KD and CAL-ED: CAL-K and the C-P2 enclosure with the disc shrunk to 0.0005. They must give the same Krein
    signs and overlapping enclosures.
  - The 9/5 regression (tag r1): the parameterised path must reproduce build-2's target outputs.

## Descriptive only (reported, not scored)
- delta, the exterior margins, eta, d2 against (1/2) dm/dE, the certified w and <a, d>, the separation distances,
  disc_r, theta, mu and Tt;
- the certified lam at lo-u and hi-u against the float square-root laws a ~ 0.1427 sqrt(sigma_lo - sigma0) and
  a ~ 0.279 sqrt(sigma0 - sigma_hi);
- the w(sigma0) curves across the grid.

## What is not claimed
- Stability is claimed only at the eight sealed points, not on the intervals between them. "Band" here means the
  float map's band, now with a certified grid inside it. Certified stability on a whole interval would need a
  continuity or perturbation argument that is not part of this bar.
- An edge bracket [a, b] says only that the state is certified unstable at a and certified stable at b. It does not
  say that the transition point is unique in [a, b].
- No claim of nonlinear or orbital stability, embedded eigenvalues, or Jordan structure at 0, as in PROOF-R1-v2
  section 12.

## Projected time (measured on build-3 calibration runs; RUN.md)
- B job: 107-120 s.
- K job: 408-681 s.
- U job: 459-474 s.
- Stable point: about 33 min of compute, or about 20 min of wall with two jobs at once.
- Unstable point: about 8 min.
- Full sealed set (8 stable + 4 unstable, including the lead's in-155 and in-200): about 5 h of compute, or about
  2.6 h of wall at two jobs at a time.
- Edge points plus in-155 and in-200: about 50 min of wall.
- Every single run is under 12 min.

## Seal fields
```
formula_ref: <LAB>/build-1/DESIGN-R1-v3.md:42-73
calibrated_on: none - no new comparator window is set for the R1 controls; C-U150 and C-U205 are sign tests (Re lambda > 0), and the build-3 rerun in CALIBRATION.md only checks that build-3 reproduces build-2
depends_on: 07faff6621
null_not_symmetry: sigma0 = 1/2 (NULL) and 3/2, 41/20 (C-U150, C-U205) are different backgrounds outside the float band, not relabels or sign flips; each changes the answer from 0 to at least 1 growing mode
target_form: per stable point: integer upper and lower counts per (L, R), n(B) and the sign of d2, Krawczyk enclosures of w and the certified sign of <a,d> for L = 0, 1, 2 with a separation record, T in {HOLDS, FAILED, INCONCLUSIVE, VOID}; per unstable point: a complex Krawczyk enclosure of lambda in the named sector, T in {HOLDS, INCONCLUSIVE, VOID}
parameters: sigma0 = fixed - one sealed claim per point by design, value 1595/1000, 1597/1000, 1983/1000, 1985/1000, 31/20, 2, 33/20, 17/10, 7/4, 37/20, 19/10, 39/20 (one per point); R = 10, 14; eps = fixed - counts are rigorous for every eps > 0, value 1/1000 exactly; r_m = fixed - matching radius only moves enclosure widths, value 8; R1 = fixed - tail radius and C-R checks radius independence, value 26; r0 = fixed - series start used consistently as an exact binary64 point, value 1e-5; disc_r = fixed - Cauchy-estimate domain only and never above the R1 value, value min(0.002, gap/4) for K jobs and min(0.002, Re(guess)/2) for U jobs; precision = fixed - one precision per stage, value 320 bits (tube) and 200 bits (linear)
instruments: itaylor.py, bg_tube.py, lincore.py, bracket.py, tail.py, match.py, kraw.py, krein.py, evans.py, assemble.py, verdict.py
tolerances: counts at plus or minus eps = 1/1000 (rigorous for every eps > 0); all other outputs are interval enclosures read by sign or by window containment; separation is decided on outward-rounded enclosure ends; C-P2 10 percent real-part gate is mock-informed (disclosed in 07faff6621)
ceiling: each point is all-or-nothing; best possible = both edges bracketed to width 0.002 around the float edges, each by a certified growing quartet outside and a certified stable point inside, plus eight certified stable points across [1.597, 1.983], plus two certified growing modes inside the paper's claimed band (31/20 at L = 0, 2 at L = 2)
toy_model: C-P1 (n = 0 at 9/5), C-P2 and C-P3 (SP n = 1), CAL-K, CAL-KD, CAL-ED and the 9/5 regression r1, all through the build-3 engine
positive control: C-P2, C-P3 and NULL (as in 07faff6621) plus C-U150 (L = 0 at 3/2) and C-U205 (L = 2 at 41/20): certified growing modes on the same family at R1 = 26, r_m = 8
baseline: the incumbent is the paper's float band "1.55 <~ sigma0 <~ 2.07" (2402.07998.txt:1073, :1124), the NOT SEALED float map [1.5963117, 1.9841288] and the certified single point 9/5 (07faff6621); the dumb baseline is C-P1, the n = 0 state, which must show zero negative directions beyond the trivial ones
run_command: cd <LAB>/build-3 ; echo sealed > SEALED-<tag>.ok ; per stable tag: assemble.py B:<tag> ; assemble.py K0:<tag> ; assemble.py K1:<tag> ; assemble.py K2:<tag> ; per unstable tag: assemble.py U:<tag> ; then verdict.py controls ; verdict.py controls-r2 ; verdict.py point <tag>   (each under memcap 8, each under 30 min, at most two at once; assemble.py refuses a point job until SEALED-<tag>.ok exists)
```
