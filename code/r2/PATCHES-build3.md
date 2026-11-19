# PATCHES: build-2 -> build-3 (R2-BAND: the R1 pipeline at any sigma0 = p/q)

Seat build-3, 2026-11-18. build-1/ and build-2/ were not touched. The eleven instruments were copied from build-2
(sha256 equal to build-2/RUN.md before any change) and edited here only. Each entry is `file:line (build-2) ->
file:line (build-3)`. No mathematics of a certificate changed. kraw.py and match.py are byte-identical copies.
bg_tube.py and bracket.py keep build-2's CRLF line ends, so `diff` shows only the patch lines.

## A. audit-1's four latent patches (core/seats/audit-1/AUDIT-ENGINES.md)
- **A1. tail.py:354 -> 354 (lemma).** `drd=[chp['drd'], chq['drd'], acb(0)]` ->
  `drd=([chp['drd'], chq['drd'], acb(0)] if lam_disc is not None else None)`. Without a disc, channel_full sets
  epsd_d = 0, so drd is not an enclosure of d rho_d/d lam (audit-1, t_drd.log). Any disc-less use of the derivative
  (tail.py:382, vectors with deriv) now fails with a TypeError instead of silently using it. Every current caller
  passes a disc whenever the derivative is used (match.py:155-157).
- **A2. lincore.py:88 -> 88-89 (march).** `assert abs(float((bj.r[i] - arb(r_from)).mid())) < 1e-14` ->
  `assert bool(bj.r[i].mid() == arb(r_from).mid()) and bool(bj.r[i].rad() == arb(r_from).rad())`. r_from must BE the
  grid ball, not merely lie within 1e-14 of one. All callers pass bj.r[0] or bj.r[-1] (bracket.py:177, match.py:149, 163).
- **A3. itaylor.py:287-297 -> 287-299 (eval_sub, eval_at).** A new required argument `h` and
  `assert tball(h).contains(T)` (resp. `t`). The enclosure sum C_k t^k + t^(K+1) R holds only for t in hull(0, h).
  Caller bracket.py:94-104 -> 94-105 (ZeroCounter): on_step stores `self._h = arb(h)` and passes it to every
  eval_sub/eval_at. tball(h) = h/2 + (h/2)[-1, 1] contains hull(0, h) for a ball h, so the assertion cannot fire on a
  legal call. It never fired in any build-3 run.
- **A4. bg_tube.py:99-100 -> 99-101 (series_start).** `eps = max(Hs, Hu) / (1 - q) * 2` and `max(Hsd, Hud)` ->
  `arb(Hs.union(Hu).upper())` and `arb(Hsd.union(Hud).upper())`. Python max() on two overlapping balls is not an
  upper bound. Effect on numbers: none visible. H is about r0^26, about 1e-130, below the 320-bit ser() radius floor.
  Every tube sha256 in CALIBRATION.md is unchanged from build-2.

## B. referee-5's Iin_lo clamp (core/seats/referee-5/REFEREE-R1-PROOF.md, section 4)
- **B1. bracket.py:288 -> 288-291 (run).** After `Iin_lo = arb((u0 - Y2 - r Y3).lower())`, the new lines are
  `if not bool(Iin_lo >= 0): Iin_lo = arb(0)`. Iin_lo is an exact arb, so the comparison is decided. A negative lower
  end would otherwise shrink delta = (2/(2L+1)) sqrt(I1^2 - Iin_lo^2), which is unsound. It is inactive at every point
  run here: Iin_lo is about 7.04 at 9/5 and is positive in every bracket run.

## C. Parameterisation (assemble.py rewritten; verdict.py extended)
- **C1. assemble.py.** The R1 TARGET block, TARGET_KREIN and the target-B / target-K<L> jobs (build-2
  assemble.py:27-74) are replaced by:
  - **POINTS (assemble.py:49-67).** One entry per tag: sig0 as an exact rational string, the mode ('stable' or
    'unstable'), per-L Newton guesses (negative-Krein w, positive-Krein partner w), the unstable sector with a complex
    guess, and R1 = 26, r_m = 8, s = 1, n = 1 (the R1 values).
  - **point() (assemble.py:76-84).** Asserts that the float label handed to the instruments reads back through
    itaylor.exact as exactly that rational (`Fraction(repr(float(p/q))) == p/q`). This is the build-2 mechanism for
    9/5, now asserted for every point. No instrument reads sigma0 as a binary double.
  - **Job kinds `<KIND>:<tag>` (assemble.py:236-237).** B (= the R1 target-B), K0/K1/K2 (= target-K<L>), and U (new:
    the background plus evans.certify of one eigenvalue in the named sector). The outputs go to out/<tag>/<KIND>.json.
  - **Seal guard (assemble.py:242-248).** A point job refuses (exit 2) unless SEALED-<tag>.ok exists. The only
    exceptions are the calibration tags p161, u150 and u205 (PROBE_TAGS). assemble.py:72-73 asserts that none of
    their sigma0 values equals any sealed-candidate sigma0. I checked that B:lo-s, K0:g170 and U:hi-u all exit 2.
    SEALED-r1.ok was created by this seat for the 9/5 regression only, citing seal 07faff6621 + AMENDMENT-R1-1.
  - **Adaptive Cauchy disc (assemble.py:142, 159).** For K jobs, disc_r = min(0.002, gap/4), where gap is the
    distance between the two guesses of that sector. For U jobs, disc_r = min(0.002, Re(guess)/2). The nearest other
    eigenvalue of a quartet member a + ib is -a + ib, at distance 2a. The disc never grows beyond the R1 value 0.002.
  - **Separation record (assemble.py:116-137, written into every K output).** It records capture (each certified w
    within gap/4 of its own guess), disjointness of the two certified w enclosures (outward floats w_lo, w_hi), and
    disc_excludes_other (disc_r sqrt 2 < certified distance between the two boxes).
  - **Calibration jobs.** CAL-KD (CAL-K with disc 0.0005) and CAL-ED (C-P2's evans enclosure alone with disc 0.0005)
    test that the certificates do not depend on the disc size.
  - The control jobs C-B1 ... CAL-K are textually the build-2 functions. job_CALK now passes disc_r = 0.002
    explicitly, which equals the default.
  - Every point tube is rebuilt in-run (`bt.DISK_CACHE = False`), as for the R1 target.
- **C2. krein.py:67 -> 67-69.** The output gains `w_lo = it.flo(wv)`, `w_hi = it.fup(wv)` (outward) and `disc_r`.
  Output only.
- **C3. evans.py:46 -> 46-47.** The output gains `re_upper`, `im_lower` and `im_upper` (outward) and `disc_r`. Output
  only.
- **C4. verdict.py (appended after line 222; `controls()` and `target()` unchanged).**
  - `point <tag>` applies the R1 target rule to out/<tag>/. It adds three things: one tube sha across B, the
    brackets and K0-K2 (VOID otherwise); a new VOID reason when both Krein certificates of a sector contracted but
    the separation record is not ok; and the unstable rule.
  - `controls-r2` scores C-U150, C-U205, CAL-KD and CAL-ED.
  - The must-pass list for a point is the R1 list plus C-U150 and C-U205.

## D. Float-map bug check (band/map bg.py tail start on a grid sample at the node)
There is no analogue in build-2/build-3 bg_tube.py. The float map picks its tail-switch radius r_c from the samples
(band/map/bg.py:103-110: the first sample after the last node with |sigma| below a threshold), so a sample sitting on
the node was taken as the tail. bg_tube has no data-driven switch point:
- the tail always starts at the fixed R1 (bg_tube.py:149-151, 188), and finish() certifies a(R1) of the right sign
  and u(R1) < 0 (bg_tube.py:290-293);
- the zero count is certified step by step from the step box (bg_tube.py:158-168);
- a step endpoint whose sigma ball contains 0 raises RuntimeError ('sigma endpoint contains 0', bg_tube.py:165-166)
  instead of being counted or used.

Every target and control result also requires zeros == n. Nothing downstream (bracket, krein, evans, tail) uses a
sample-chosen radius.

## Seen and NOT changed
- evans.py:48 `center_on_real_axis` is still a float decision (control C-P3 only; flagged by build-2, not on any R2
  path).
- R1 = 26, r_m = 8, R = 10, 14, eps = 1/1000, r0, the precisions and the Krawczyk relative radii are the R1 values at
  every point. The positive controls u150 and u205 check them for the unstable route on this family.
