# CALIBRATION: R1 controls re-run with the build-2 instruments (seat build-2, 2026-11-18)

Controls only. At sigma0 = 9/5 (n = 1), only the background tube and its virial identity were computed. Instruments
are listed in RUN.md, with sha256. The verdict table comes from `verdict.py controls` (out/controls_verdict.json,
out/verdict_controls.log). Raw outputs are in out/cal/*.json. "old" means build-1/out (instruments as sealed in
07faff6621) and "new" means build-2/out.

## Verdict (`verdict.py controls`, build-2)
C-B1 PASS, C-B2 PASS, C-P1 PASS, C-R(C-P1) PASS, C-W(C-P1) PASS, C-P2 PASS, C-W(SP) PASS, C-R(C-P2) PASS, C-P3 PASS,
C-R(C-P3) PASS, NULL PASS, CAL-K PASS. This is the same as build-1: all PASS.

## Old vs new (certified enclosures as printed)

| control | quantity | old (build-1) | new (build-2) | same to printed digits |
|---|---|---|---|---|
| C-B1 | T, sigma0 = 0.191 | 0.558401458204 +/- 1.13e-13 | 0.558401458204 +/- 1.13e-13 | yes |
| C-B1 | F, sigma0 = 0.191 | 0.0466781605948 +/- 4.58e-14 | 0.0466781605948 +/- 4.58e-14 | yes |
| C-B1 | T, sigma0 = 1.047 | 5.64187998321 +/- 6.18e-13 | 5.64187998321 +/- 6.19e-13 | yes (radius moves in the 3rd digit) |
| C-B1 | F, sigma0 = 1.047 | 1.88788680711 +/- 3.65e-12 | 1.88788680711 +/- 3.65e-12 | yes |
| C-B1 | virial rel. upper | 8.2255183e-15, 1.0258357e-14 | 8.2255184e-15, 1.0258357e-14 | yes (moves at 1e-8 rel.; exact sigma0 plus outward rounding) |
| C-B2 | E1/E0 at equal N | 0.189203706825 +/- 1.76e-13 | 0.189203706825 +/- 1.76e-13 | yes |
| C-P1 | counts (L+ up/lo ; L- up/lo), R = 10 and 14 | L0 1/1 ; 1/0, L1 1/0 ; 0/0, L2 0/0 ; 0/0, L3 0/0 ; 0/0 | identical | yes |
| C-P1 | D0, R = 10 | nB = 1, d2 = -1.605937254 +/- 4.67e-10, M = 2.494e7 | identical | yes |
| C-P1 | D0, R = 14 | nB = 1, d2 = -1.606070497 +/- 2.98e-10, M = 1.173e13 | identical | yes |
| C-P1 | ext_margin L0, R = 10 / 14 | 2.34924 / 2.73871 | 2.34824 / 2.73771 | moves by exactly -0.001 (item 4, -eps), as intended |
| C-W (C-P1) | Q(X) upper | -4.621730884485 | -4.621730884399 | moves at 1e-11 (ball sub-interval endpoints replace floats, X3) |
| C-P2 | counts L0, R = 20 and 28 | + 2/2 ; - 2/1 | identical | yes |
| C-P2 | D0 d2, R = 20 / 28 | -2.097812173 / -2.104693650 | identical | yes |
| C-P2 | lambda | 0.08827420126 + 0.5829039426 i (+- 1.41e-12) | identical | yes |
| C-P2 | lambda/(2\|E1\|) | 0.04817016568, 0.3180836427 | identical | yes |
| C-W (SP) | Q(X) upper | -2.894758928846183 | -2.8947589288461826 | yes (last float digit) |
| C-P3 | counts L2, R = 20 and 28 | + 1/1 ; - 0/0 | identical | yes |
| C-P3 | lambda | 0.09917673961 +/- 8.69e-13 (imag. midpoint 1.0e-32) | identical (imag. midpoint 1.0e-32) | yes |
| NULL | lambda (L = 0) | 0.02413229273 + 0.2832272004 i (+- 2.35e-13) | identical | yes |
| NULL | counts / D0, R = 24 and 32 (descriptive) | L0 + 2/2 ; - 2/1, nB = 2; L2 + 1/1 ; - 0/0 | identical | yes |
| CAL-K | negative Krein w, <a,d> | 0.1762794039 (+- 2.0e-19), -4.180824634e-4 (+- 9.6e-14) | identical | yes |
| CAL-K | positive Krein w, <a,d> | 0.3646045762 (+- 1.5e-17), +1.083262574e-3 (+- 1.1e-13) | identical | yes |
| target tube (pre-seal) | u0, E, m | 3.93902357538, -3.10544025447, 19.1587125456 | identical (now at sigma0 = 9/5) | yes |
| target tube (pre-seal) | virial, rel. | +-2.15e-13, +-8.21e-16 | identical | yes |
| target tube (pre-seal) | zeros, tail, existence | 1, certified, certified | identical | yes |

Every ext_margin in every control (C-P1, C-P2, C-P3, NULL) is exactly 0.001 lower, as item 4 requires. No ext_ok flag
changed. The smallest new margin is 0.269 (NULL, R = 24).

## Assertions added by build-2 (all held, none raised)
- The 0.01 margins of qbound, gnorms and frob_start, checked against the series_start crude enclosure (item 3).
- lincore.march: the end point reached encloses r_to (X5).
- bracket.run: the I_in grid point is certified <= R (X4).
- assemble.py: sigma0 = 1.80 maps to the rational 9/5 exactly (item 1).

## Tubes behind each control (sha256 of the JSON tube, written into each output; item 5)
| control | tube_sha256 | source |
|---|---|---|
| C-B1 | ef6bdfe8...8a102d (0.191), f7c698f9...02e5f9bc (1.047) | built fresh in build-2, then cached |
| C-B2 | 64573e77...8f018a84 (SP n=1), e0a52764...72ad698d (SP n=0) | built fresh |
| C-P1 | 8abf9553...3dd236e8 | built fresh |
| C-P2, C-P3 | 64573e77...8f018a84 | build-2 cache (the C-B2 SP n=1 tube) |
| NULL | 2a0d7c6c...4ec7a459 | built fresh |
| CAL-K | not recorded in its JSON (job_CALK writes no sha field); it loads the same cache file as C-P2 | build-2 cache |
| target (pre-seal) | f8b0cc27d5885a45af4b7356a1e3f6f2e0e1445510e32842cf4710f9ecfce28b | built in memory, not cached |

No build-1 cache file was read. build-2/cache holds only control tubes (*_v5.json). There is no sigma0 = 1.8, n = 1
tube in it.
