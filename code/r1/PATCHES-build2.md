# PATCHES: build-1 -> build-2 (R1 instruments, referee-3 must-fix list)

Seat build-2, 2026-11-18. build-1/ untouched. Each entry is `file:line (build-1) -> file:line (build-2)`: old -> new,
mapped to the REFEREE-R1-FINAL item numbers (R1..R6 = "Must change before proved" 1..6; X = extra leak found by the
grep). No mathematics changed. kraw.py and verdict.py are byte-identical copies.

## New helpers (used by the fixes)
- itaylor.py:18-19, 25-48 (new). `exact(x)`: an arb ball around the exact rational a literal denotes (float read
  through `Fraction(repr(x))`, so 1.80 -> 9/5, 1e-3 -> 1/1000). `fup(x)` and `flo(x)`: floats rounded outward from an
  arb's ends, with `math.nextafter` when float() rounded inward. [R1, R2]
- bg_tube.py:116-134 (new). `assert_start_margins(s, sig0, u0, r0, sg, ua)` rebuilds the `series_start` crude
  enclosure on [0, r0]. It raises AssertionError unless sup|sigma| < sg and sup|u| < ua. Memoised. [R3]
- tail.py:31-34 (new). `amin(a, b)`: the arb lower end of the hull, the twin of the existing `amax`. [R2]

## Item 1: sigma0 exact (and other decimal parameters)
- bg_tube.py:72 -> 72-73. `S = [A(sig0)]` -> `sg0 = it.exact(sig0); S = [sg0]`.
- bg_tube.py:94 -> 95. `sg = abs(A(sig0)) + 1` -> `abs(sg0) + 1`.
- bg_tube.py:106 -> 107. `smax = abs(A(sig0)) + 1` -> `abs(sg0) + 1`.
- bg_tube.py:111 -> 112. crude `A(sig0)` (twice) -> `sg0`.
- match.py:51 -> 52. `abs(arb(sig0))` -> `abs(it.exact(sig0))`.
- match.py:70 -> 72. `sig0a = arb(sig0)` -> `sig0a = it.exact(sig0)`.
- bracket.py:41 -> 41. qbound `abs(arb(sig0))` -> `abs(it.exact(sig0))`.
- bracket.py:220 -> 222. gnorms `abs(arb(sig0))` -> `abs(it.exact(sig0))`.
- assemble.py:27 -> 27-31. TARGET keeps sig0 = 1.80 as the label. It adds `assert Fraction(repr(1.80)) == Fraction(9, 5)`
  and `sig0_exact = '9/5'`. Every instrument reads sigma0 only through `it.exact`.
- assemble.py:39-42 -> 43-47. bg_info writes `sig0_exact` into every background block.
- bracket.py:275 -> 280-283. The run header records `sig0_exact`.
- X. eps: bracket.py:287-288 -> 297-298. `arb(eps)` / `-arb(eps)` (the double nearest 1e-3) -> `epsA = it.exact(eps)`
  = 1/1000 exactly.
- Side effect: the C-B1 values 0.191 and 1.047 are now 191/1000 and 1047/1000 exactly. 0.5, 1.0, R, R1 and r_m are
  integers or dyadics, so they were already exact.
- Kept on purpose (not exact decimals). r0 = 1e-5 is the binary64 point 1.0000000000000000818e-5, used consistently
  as an exact point by the series start and the grid. It is a free numerical choice, not a claimed value. Also kept:
  the Cauchy disc radius 0.002, the Krawczyk box radii, Rfar, the step sizes and the u0 bracket offset. The u0 offset
  is the arb 10^-50, and u0 itself is an arb. Each of these is used as the same exact value in every place it enters.

## Item 2: tail.py Riccati
- tail.py:190-214 -> 195-224 (ric_integrate). Old: `if abs(rt - float(r.mid())) < 1e-9: r = arb(r_to)` snapped r
  without integrating the gap (up to 9.3e-15). New: when the remaining distance is within 1e-9 of the step, the step
  is the exact ball `hA = arb(r_to) - r` and it is integrated. Then `r = arb(r_to)` and the loop ends. Float h is now
  only the step-size heuristic.
- tail.py:256-257 -> 265-267. `infRe_d = arb(min(float(..), float(..)))` -> `amin(sd['minRe'], (rho_min - eps).lower())`.
  `supRe_g = arb(max(float(..), float(..)))` -> `amax(sg['maxRe'], (-(c - epsg)).upper())`.
- tail.py:299-300 -> 309-310. `cd = arb(min(float(..), float(..)))` -> `amin(cpD['cd'], cqD['cd'])`.
  `mu = 0.5 * arb(min(float(cd.lower()), float(kappa1.lower())))` -> `arb('0.5') * amin(cd, kappa1)`.

## Item 3: assert the 0.01 margins
- bracket.py:40-42 -> 40-44. qbound gains `r0=` and calls `bt.assert_start_margins(s, sig0, u0, r0, sg, ua)`.
  bracket.py:159 -> 161: count passes `r0=r0`.
- match.py:51 -> 53. frob_start calls `bt.assert_start_margins(s, sig0, u0, r0, sg, ua)`. match.py:17 -> 18 adds
  `import bg_tube as bt`.
- bracket.py:218-220 -> 220-223. gnorms gains the argument `s` and calls `bt.assert_start_margins(s, sig0, u0, r0, sg)`.
  bracket.py:210 -> 212: the call site passes `s`.
- All of these held in every control run. None raised.

## Item 4: exterior check minus eps
- bracket.py:283 -> 292-293. `ext = -E - m/R - dlt` -> `ext0 = -E - m/R - dlt` (the level-0 reserve, still passed
  unchanged to d0_node, bracket.py:293 -> 303) and `ext = ext0 - epsA`. `ext_ok = ext > 0` gates the upper counts at
  level +eps, as the design requires. Effect: every ext_margin printed is exactly 0.001 lower.

## Item 5: tube cache
- bg_tube.py:19. `pickle` removed.
- bg_tube.py:333-354 -> 353-397 (get_tube). Old: a pickle of ser() strings in cache/*.pkl, keyed v4, read
  unconditionally. New: a JSON document of ser() strings (decimal midpoint plus outward radius). No arb object is ever
  pickled. Every caller decodes the same blob. `info['tube_sha256']` = sha256 of the blob, and `info['tube_source']` =
  "built in this run" or "disk cache <file>". Key v5, file `cache/*.json`. A module flag `DISK_CACHE` and an argument
  `use_cache` are added, plus an in-process memo, so one process builds once. The wall time is removed from the blob,
  which keeps the sha reproducible.
- assemble.py:136-137 -> 142-146. Every target job sets `bt.DISK_CACHE = False`. The tube is rebuilt inside each
  target run, and the disk cache is neither read nor written.
- assemble.py:39 -> 43, assemble.py:67 -> 73, bracket.py:275 -> 280-283. `tube_sha256` and `tube_source` are written
  into target-B (B block and brackets header) and into each target-K output. The four target runs must report the same
  sha. The pre-seal build gave f8b0cc27d5885a45af4b7356a1e3f6f2e0e1445510e32842cf4710f9ecfce28b (out/target_bg_tube.log).
- bg_tube.py:363 -> 407-409. The CLI builds in memory (`use_cache=False`) and prints tube_sha256.

## Item 6: docstrings
- match.py:83 -> 86-89 (new comment above R4/R3). The omitted (1 + e1) and 1/(1 - c) factors are covered by the
  factor-2 slack in q and cq. (1 + e1)/(1 - c) = 1/(1 - c)^2 < 1.78 < 2 for c < 0.25 (asserted).
- krein.py:5 -> 5-6. "nondegenerate (so i w* is an algebraically simple eigenvalue)" -> "with J(w*, v*) invertible. (No
  algebraic-simplicity claim is made or needed.)". The referee cited krein.py:159, but the file has 88 lines. The phrase
  is at line 5.
- evans.py:4 -> 4-5. The same wording fix: "exactly one eigenvalue lam* in the lam-disc, algebraically simple" ->
  "exactly one zero (lam*, v*) of M(lam) v = 0, v_k0 = 1, in X (no algebraic-simplicity claim)".

## Extra float leaks found by the grep (X)
- X1. bracket.py:272 -> 277. `r0 = float(steps[0]['r'].mid())` -> `r0 = steps[0]['r']` (the tube's own start ball).
- X2. bracket.py:225 -> 228 (gnorms). Step selection by float compare -> `if bool(r + h <= arb(R))`, which skips only
  steps certainly inside [0, R]. Conservative.
- X3. bracket.py:241-252 -> 245-257 (wneumann_test, C-W). The sub-interval endpoints were `float(r.mid())` and
  `max/min` of floats, and the width was `arb(b_ - a_)`. Now they are ball endpoints: `a_ = r or arb(R)`,
  `b_ = r + h or R + 2`, and the width is `b_ - a_` in arb. Reported floats now use fup/flo (bracket.py:263-264 -> 268-269).
- X4. bracket.py:278 -> 287 (new). `assert st['r'] <= arb(R)` for the grid point used in I_in(R).
- X5. lincore.py:90, 98, 118, 129 -> 91, 100, 121, 133-135 (march). march had the same snap pattern as tail.py
  (stop when within 1e-15 of r_to). It now tracks the end point reached and raises unless that ball encloses r_to. It
  never raised in any control run.
- X6. assemble.py:42 -> 47. `virial_rel_upper = float(upper)` -> `it.fup(...)`. assemble.py:86 -> 92: C-B2
  `ratio_lo/hi = float()` -> `it.flo / it.fup`. evans.py:43 -> 44: `re_lower` -> `it.flo`. These are comparator inputs
  of verdict.py, now rounded outward.

## Seen and NOT changed
- evans.py:48 `center_on_real_axis = abs(float(lam.imag.mid())) < float(lam.imag.rad())` (C-P3 only). This is a float
  decision. The "uniqueness + conjugate symmetry => real" step also needs conj(lam*, v*), with v re-normalised after
  the p <-> q swap, to lie in the Krawczyk box X. That is an argument, not an instrument fix, so it is outside build-2's
  scope. It is not on the target path. Flagged for the lead/referee.
- Steering floats: lincore index_of/march compares, bg_tube step sizes and termination, tail.py Rfar and kap, and
  Newton guesses. Krawczyk centres, the preconditioner C and the powers-of-two column scaling D are any-matrix choices.
  Reporting floats (lam, eta, w_rad, theta, mu strings). verdict.py lo_hi parsing (comparator; verdict rules unchanged).
