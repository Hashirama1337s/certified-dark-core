# AMENDMENT-R1-1 (FOR SEALING): instrument fixes to BAR-R1-FINAL (amends seal 07faff6621)

Prepared by seat build-2, 2026-11-18, for the lead to seal with `--amends 07faff6621`. It applies the must-fix list of
REFEREE-R1-FINAL.md (seat referee-3). This seat did not read TARGETS-R1*.md. Nothing at sigma0 = 9/5 was run except the
background tube and its virial identity.

## In plain words
The referee found no mathematical hole in the sealed test, but found four places where the code was not yet airtight.
sigma0 was entered as the computer number nearest 1.8, not 1.80 itself. One routine jumped a tiny un-integrated gap.
Some bounds were rounded to the nearest float instead of outward. A few assumed margins were never checked. These are
now fixed and the controls have been re-run. The test itself does not change. The target is run once more with the
fixed code and scored by the same rules, and that result replaces the earlier HOLD.

## What is unchanged
The pre-registered predictions P1-P4, the four outcomes of T (VOID, FAILED, HOLDS, INCONCLUSIVE) with their exact
conditions, every control (C-B1, C-B2, C-P1, C-P2, C-P3, C-R, C-W, PK0-PK2, null N1, and CAL-K as instrument
calibration), every comparator window, the disclosures, and the descriptive-only list are all exactly as in
<LAB>/build-1/BAR-R1-FINAL.md. verdict.py is byte-identical (sha256 d9c06bbc...992b). FAILED
still means only one thing: a Krawczyk-certified eigenvalue with Re lambda > 0. No parity theorem is used.

## What changes (instrument fixes only; detail in build-2/PATCHES.md)
1. Referee item 1. sigma0 now enters every enclosure as the exact rational 9/5, through `itaylor.exact`: bg_tube.py
   series start, match.py Frobenius start, bracket.py qbound and gnorms. assemble.py asserts that 1.80 maps to 9/5. eps
   enters as exactly 1/1000. The C-B1 values become 191/1000 and 1047/1000.
2. Referee item 2. tail.py ric_integrate integrates the final step exactly (h = arb(r_to) - r) instead of snapping
   across the gap. The hull ends at tail.py (inf Re rho_d, sup Re rho_g, cd, mu) stay in arb, with no float().
3. Referee item 3. The 0.01 margins of bracket.qbound, bracket.gnorms and match.frob_start are asserted from the
   series_start crude enclosure. A violation raises.
4. Referee item 4. The exterior check for the upper counts is |E| - m/R - delta - eps > 0. The level-0 reserve passed
   to D0 is unchanged.
5. Referee item 5. There is no pickle. The tube is stored as JSON strings, and every output carries the sha256 of the
   tube it used. Target jobs rebuild the tube inside the run and never read or write the cache. The pre-seal build gives
   tube sha256 f8b0cc27d5885a45af4b7356a1e3f6f2e0e1445510e32842cf4710f9ecfce28b, and all four target outputs must
   report it.
6. Referee item 6. The docstrings now say that the Frobenius slack covers the omitted factors (match.py). The
   "algebraically simple" claim is dropped from krein.py (line 5; the referee's line 159 does not exist) and from
   evans.py.
7. Extra float leaks found by grep, fixed the same way. The bracket r0 is now the tube's start ball. C-W sub-interval
   endpoints are balls. gnorms step selection uses certain comparisons. The I_in grid point is asserted to be <= R.
   lincore.march raises unless its end point encloses r_to. The verdict comparator inputs (virial_rel_upper, the C-B2
   ratio bounds, evans re_lower) are rounded outward.

The instruments are now code/r1/*.py, with sha256 as in build-2/RUN.md:
itaylor 2d933b90d3f9740b1809a082836ec474e2abc0669f720f6cb76277a68e0e4283,
bg_tube 1800c276ed0da529581471de27f000a1c802added3a7ac7519cface0acb0e81b,
lincore b0ca17b86b75734be089d2a1da11f443acdc256d022f17560722ac09a7caa1bb,
bracket bddd76228b293c1f85ab6aca77a3b1ae066530926ee87b2c0275f8ed9d50391c,
tail e9b339c5d75d1d4e507ef81837a6fe34a9556c359c2c7bff757144c52ccedb6c,
match 3dbce1e54283c9e61e994c50b03f068777723a01a65f48839c10996be84b3632,
kraw b70ee710932a4cccd96991ddc739611ff4b21680df3a5db1b75f9a5d24c99b6b,
krein 4c795a2aa41724ea2eb75e491c3cddf2daaf812b061cb9e62414f394cb3170be,
evans ba9353bed6fc0223aff76dd8463b5a0043074516505012b14d11f68552624d65,
assemble 9aebf3322a6a6e7250c0c702579373542cb8fcb22e131c097126314dd934beeb,
verdict d9c06bbcdf3fa1b60fa6a9fcde9aaadde15f89d0aac011797a81d4ad6e45992b.

## Controls re-run with the fixed instruments
All controls were re-run under build-2. See build-2/CALIBRATION.md for the old-vs-new table and the verdict.py
controls result. Every count, every D0 node and every certified eigenvalue agrees with build-1 to the printed digits.
The only movements are the intended ones. ext_margin is exactly 0.001 lower (item 4). Radii and the virial upper
bound move at the 1e-13 relative level for C-B1 (exact decimal sigma0). The C-W Q(X) bound moves at the 1e-11 level
(ball endpoints). A control that fails under build-2 makes the target VOID, exactly as in BAR-R1-FINAL.

## The rerun and how it is scored
The target is run once, with the fixed instruments, by the commands in build-2/RUN.md (four jobs, each under memcap
and under 30 min). It is scored by the same verdict.py rules: target, then controls. Whatever this run returns
(HOLDS, FAILED, INCONCLUSIVE or VOID) supersedes the earlier HOLD of 07faff6621. That HOLD was certified at
sigma0 = fl(1.8) and is no longer the result. If the four target outputs do not report one and the same tube_sha256,
the run is VOID. There is no second attempt under this amendment. Projected time: target-B 2-3 min, and each target-K
6-9 min including the in-run tube rebuild of about 100 s. That is about 25-30 min of compute, or about 15 min of wall
with two jobs in parallel.

## Not changed and flagged (outside this amendment)
evans.py:48 decides "centre on the real axis" for C-P3 by a float compare. The step from uniqueness plus conjugate
symmetry to a real eigenvalue also needs the conjugate zero (re-normalised after the p <-> q swap) to lie in the
Krawczyk box. That is an argument, not an instrument fix. It is not on the target path, and C-P3 is scored exactly as
sealed.

## Seal fields
```
formula_ref: <LAB>/build-1/DESIGN-R1-v3.md:42-73
calibrated_on: none - no new threshold is set; every control window is the one sealed in 07faff6621, and the build-2 control rerun in CALIBRATION.md only checks that the fixed instruments reproduce build-1
depends_on: 07faff6621
null_not_symmetry: sigma0 = 1/2 is a different background outside the claimed band, which changes the answer from 0 to at least 1 growing mode; it is unchanged from 07faff6621
target_form: integer upper and lower counts per (L, R); n(B) and the sign of d2; Krawczyk enclosures of w and the certified sign of <a,d> for L = 0, 1, 2; T in {HOLDS, FAILED, INCONCLUSIVE, VOID}; same as 07faff6621
parameters: sigma0 = fixed - single-point claim by design, now entered exactly, value 9/5; R = 10, 14; eps = fixed - counts are rigorous for every eps > 0, value 1/1000 exactly; r_m = fixed - matching radius only moves enclosure widths, value 8; R1 = fixed - tail radius and C-R checks radius independence, value 26; r0 = fixed - series start point used consistently as an exact binary64 point, value 1e-5; precision = fixed - tube and linear stages use one precision each, value 320 bits (tube) and 200 bits (linear)
instruments: itaylor.py, bg_tube.py, lincore.py, bracket.py, tail.py, match.py, kraw.py, krein.py, evans.py, assemble.py, verdict.py
tolerances: counts are taken at plus or minus eps = 1/1000 (rigorous for every eps > 0, so no headroom is needed); all other outputs are interval enclosures read by sign or by window containment; the 0.01 start margins are asserted against the crude enclosure (true variation about 1e-10, so the margin is 8 orders of headroom); C-P2 10 percent real-part gate is mock-informed (disclosed in 07faff6621)
ceiling: the certificate is all-or-nothing per sector; best possible = HOLDS with every upper count equal to its lower count at both radii, now at sigma0 = 9/5 exactly
toy_model: C-P1 (n = 0, same sigma0), C-P2 and C-P3 (SP n = 1, published counts and values), CAL-K (SP n = 1, L = 1 Krein signs), all re-run through the fixed engine
positive control: C-P2 and C-P3 (published Schroedinger-Poisson n = 1 instabilities recovered with certified eigenvalues) and null N1 (sigma0 = 1/2 must show a certified growing mode), re-run under build-2
baseline: the incumbent is the float stability claim of 2402.07998 and the earlier HOLD at sigma0 = fl(1.8) under 07faff6621; the dumb baseline is C-P1, the n = 0 state, which must show zero negative directions beyond the trivial ones
run_command: cd code/r1 ; assemble.py target-B ; assemble.py target-K0 ; assemble.py target-K1 ; assemble.py target-K2 ; verdict.py controls ; verdict.py target   (each under memcap 8, each under 30 min, at most two at once; assemble.py refuses until build-2/SEALED.ok exists)
```
