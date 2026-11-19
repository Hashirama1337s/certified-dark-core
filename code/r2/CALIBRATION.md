# CALIBRATION: R1 controls, the 9/5 regression and the R2 calibration jobs with the build-3 instruments

Seat build-3, 2026-11-18. No proposed R2 point was run. Raw outputs: out/cal/*.json, out/r1/, out/p161/, out/u150/,
out/u205/. Logs: logs/. Comparisons were made leaf by leaf with aux/b3compare.py, which checks string equality of
every printed value in the JSON. Timings, tube_source and keys new in build-3 are excluded from the comparison.

## Verdicts
- `verdict.py controls` (logs/verdict_controls.log): C-B1, C-B2, C-P1, C-R(C-P1), C-W(C-P1), C-P2, C-W(SP),
  C-R(C-P2), C-P3, C-R(C-P3), NULL and CAL-K all PASS. This matches build-2.
- `verdict.py controls-r2` (logs/verdict_controls_r2.log): C-U150, C-U205, CAL-KD and CAL-ED all PASS.
- `verdict.py point r1` (out/r1/verdict.json): **HOLDS**, with K = (2, 2, 2, 0), no void reasons, one tube sha
  f8b0cc27...ce28b and all eight must-pass controls PASS. This matches the build-2 target verdict (HOLDS,
  K = (2, 2, 2, 0)).

## R1 controls, build-2 vs build-3 (leaf by leaf)

| control | leaves compared | differing |
|---|---|---|
| C-B1 | 67 | 0 (T, F, virial, tube_sha256 identical) |
| C-B2 | 68 | 0 (E1/E0 0.189203706825 +/- 1.76e-13; both tube shas identical) |
| C-P1 | 568 | 0 (counts, D0, ext margins, C-W Q(X), tube sha identical) |
| C-P2 | 226 | 0 (counts, D0, lambda 0.08827420126 + 0.5829039426 i +/- 1.41e-12) |
| C-P3 | 186 | 0 (lambda 0.09917673961 +/- 8.69e-13) |
| NULL | 335 | 0 (lambda 0.02413229273 + 0.2832272004 i) |
| CAL-K | 44 | 0 (w-: 0.1762794039, <a,d> -4.180824634e-4; w+: 0.3646045762, <a,d> +1.083262574e-3) |

Every tube sha256 is unchanged from build-2. That includes the bg_tube series_start patch A4, whose effect sits below
the 320-bit serialisation floor.

## Regression of the parameterised path at 9/5 (tag r1), against build-2/out/target-*.json

| output | leaves compared | differing | the only differences |
|---|---|---|---|
| B:r1 vs target-B | 570 | 2 | job name; config.sig0 is now the string "9/5" instead of the label 1.8 |
| K0:r1 vs target-K0 | 46 | 2 | same two labels |
| K1:r1 vs target-K1 | 46 | 2 | same two labels |
| K2:r1 vs target-K2 | 46 | 2 | same two labels |

Every certified number is identical: counts, D0, delta, ext margins, C-W, D1, w, <a, d>, theta, mu and Tt. The tube
sha is f8b0cc27d5885a45af4b7356a1e3f6f2e0e1445510e32842cf4710f9ecfce28b in B, the brackets, K0, K1 and K2, equal to
the build-2 pre-seal value. Separation records at 9/5 (disc_r = 0.002, all ok): certified distances between the
negative- and positive-Krein w of 0.1543 (L = 0), 0.4111 (L = 1) and 0.2211 (L = 2).

| L | w- | <a,d>- | w+ | sign+ |
|---|---|---|---|---|
| 0 | 1.104911080 +/- 3.8e-16 | -3.061281342e-6 | 1.259213371 +/- 3.0e-15 | + |
| 1 | 0.5399256680 +/- 9.7e-18 | -6.212149350e-5 | 0.9510282377 +/- 5.6e-17 | + |
| 2 | 0.2968148506 +/- 2.2e-11 | -2.403151062e-4 | 0.5179458643 +/- 2.7e-11 | + |

## Disc adaptation (item 3)
- **What the disc does.** The Cauchy disc (krein.py:41, evans.py:117/122) is only the domain on which tail.lemma
  bounds the w-derivative of the tail error terms (dTt = Tt/(disc_r - box_r); match.py:155-157). Those terms are
  analytic in w through the Coulomb-channel Riccati data and do not see the eigenvalues of the full problem. So a
  disc that contains the other mode is not a mathematical defect.
- **What separating two close modes really needs.** Each Krawczyk box isolates its own zero (box radius about 1e-9
  relative, against a gap of 7.5e-3). The two certificates must land on two different modes, which is a steering
  issue. build-3 therefore records and gates (VOID if not ok) four things: capture within gap/4 of each guess,
  disjoint certified w boxes, opposite Krein signs (the PK rule), and, as the lead asked, a disc clear of the other
  mode (disc_r sqrt 2 < the certified distance).
- **Rule.** K jobs use disc_r = min(0.002, gap/4); U jobs use min(0.002, Re(guess)/2). It binds only at lo-s, L = 0,
  where disc_r = 0.00187.
- **Control CAL-KD** (CAL-K with disc 0.0005, a quarter of R1's): every printed digit of w and <a, d> is identical to
  CAL-K, for both modes, including the radii.
- **Control CAL-ED** (C-P2's enclosure with disc 0.0005): lambda is identical to C-P2 to every printed digit,
  including the radius.
- **Separation control at a non-target point** (K0:p161, sigma0 = 161/100, L = 0, gap 0.0338): w- =
  1.008777081 +/- 1.4e-13 (sign -) and w+ = 1.042587431 +/- 2.2e-13 (sign +). Capture, disjointness and disc-clear
  are all true; the certified distance is 0.033810.
- **Not tested directly.** A gap as small as 7.5e-3 at a non-target point: the only such points sit next to the
  edge and would pre-empt lo-s.

## Unstable route on the target family (positive controls; R1 = 26, r_m = 8, disc_r = 0.002)

| control | sigma0 | sector | certified lambda | Re lower end | background |
|---|---|---|---|---|---|
| C-U150 | 3/2 | L = 0 | 0.04031295638 + 0.9392591602 i (+/- 1.24e-12) | 0.0403129564 > 0 | zeros 1, existence certified, E = -2.31200973931 |
| C-U205 | 41/20 | L = 2 | 0.07352351727 + 0.4841455701 i (+/- 1.02e-11) | 0.0735235173 > 0 | zeros 1, existence certified, E = -3.88184209358 |

Both agree with the float map (0.040312956 + 0.939259160 i; 0.073523517 + 0.484145570 i) to all of the float map's
9 digits.

## Timing probe at the non-target point 161/100 (B:p161)
- Wall 107 s, tube included.
- Counts are identical to 9/5 at both radii: L0 + 2/2, - 2/1, with D0 n(B) = 2, d2 = -2.2389 and constrained upper
  1; L1 + 2/1, - 1/1; L2 1/1, 1/1; L3 0.
- Background: ext margins >= 0.762 (R = 10), the virial upper end 8.6e-16, C-W ok, and a1 = 1.41e-10 at R1 = 26.

## Assertions added in build-3 (none fired in any run)
- eval_sub/eval_at t in hull(0, h) (A3).
- march r_from is a grid ball (A2).
- The point() exact read-back.
- The Iin_lo clamp was never active.

## Provenance note (disclosure)
assemble.py and verdict.py were edited once mid-chain, at 20:57:52. The lead added in-155 and in-200, and the L = 0
positive control moved from 31/20 to 3/2. These edits touched only the POINTS / PROBE_TAGS table and the
controls-r2 names; no control job function changed. So C-B2, B:p161 (20:40-20:43), C-B1, C-P1, C-P2, C-P3, NULL
and CAL-K ran with the pre-edit assemble.py. The other nine instruments were byte-identical to the final ones, apart
from CRLF line ends restored on bg_tube.py and bracket.py at 20:41:35, which changed no content. The r1 regression,
C-U150, C-U205, CAL-KD, CAL-ED, K0:p161 and all verdicts ran with the final hashes in RUN.md. If the seal requires
every control to be produced by the final hashes, rerun `sh aux/run_chain.sh` up to NULL/CAL-K (about 25 min wall).
Nothing was ever run at 31/20 or 2.
