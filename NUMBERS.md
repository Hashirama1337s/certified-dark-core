# NUMBERS: every number in this release and the file it comes from

**In plain words.** Each number printed in README.md, PAPER.md, CITATION.cff or .zenodo.json is listed here once, with
the file in this repository that holds it and where in that file. `python tools/check_numbers.py` opens every file
named below and checks that the printed string is really there (line rows: on that line; key rows: in that JSON value).
Rows marked `external` come from a published paper and are not machine-checked.

Labels used in the text: **certified** = an outward-rounded ball-arithmetic enclosure from a sealed run;
**float** = double precision, checked only by changing the resolution, not certified.

Notes on reading the sources:
- The `w` strings in `data/r1/target-K<L>.json` are truncated midpoints and are **not** enclosures (proof, GAP C2).
  The certified `w` boxes are the `refine:` lines of `data/r1/target-K<L>.log`, used below.
- For the control eigenvalues (NULL, C-P2, C-P3) the `lam_re` / `lam_im` strings use the same truncating formatter.
  Only `re_lower` (an outward-rounded float) is quoted as certified; the imaginary parts are quoted as 10-digit values.
- Counts are integers read from `brackets/radii/<R>/<L>/<+|->/<upper|lower>` of `data/r1/target-B.json`; only three
  representative rows are listed, the full table is in PAPER.md section 4.2 and is identical at R = 10 and R = 14.

| id | printed | meaning | file | locator |
|---|---|---|---|---|
| N1 | `3.93902357537910961270976242947912892526530674750036020337021` | u_mid, midpoint of the start interval U0 (60 digits) | `data/r1/target_bg_tube.json` | `key u_mid` |
| N2 | `0.99 x 10^-50` | half-width of the exactly defined start interval U0' | `proof/PROOF-R1-v2.md` | `line 70` |
| N3 | `f8b0cc27d5885a45af4b7356a1e3f6f2e0e1445510e32842cf4710f9ecfce28b` | sha256 of the certified background tube (same in all four target outputs) | `data/r1/target-B.json` | `key B/tube_sha256` |
| N4 | `[-3.10544025447 +/- 3.02e-12]` | E, the chemical potential (energy eigenvalue) of the state | `data/r1/target-B.json` | `key B/E` |
| N5 | `[19.1587125456 +/- 4.04e-11]` | m = int sigma^2 r^2 dr (mass / 4 pi) | `data/r1/target-B.json` | `key B/m` |
| N6 | `[240.755482341 +/- 4.75e-10]` | N = 4 pi m, particle number in the paper units | `data/r1/target-B.json` | `key B/N` |
| N7 | `[7.04446382985 +/- 3.92e-12]` | I1 = int sigma^2 r dr | `data/r1/target-B.json` | `key B/I1` |
| N8 | `[1.53901484561 +/- 4.69e-12]` | kappa1 = sqrt(-u(26)), tail decay rate | `data/r1/target-B.json` | `key B/kappa1` |
| N9 | `[7.75859535966e-12 +/- 3.43e-24]` | a1 = absolute value of r sigma at r = 26 | `data/r1/target-B.json` | `key B/a1` |
| N10 | `[-2.36856669502 +/- 2.38e-12]` | u(26) | `data/r1/target-B.json` | `key B/u_R1` |
| N11 | `[+/- 8.21e-16]` | relative virial residual (consistency check only) | `data/r1/target-B.json` | `key B/virial_rel` |
| N12 | `[14.3690344092 +/- 3.03e-11]` | D1 = 3m/4 | `data/r1/target-B.json` | `key D1` |
| N13 | `escape` | classification at the lower end of U0 | `data/r1/target-B.json` | `key B/classify/lo/result` |
| N14 | `zeros` | classification at the upper end of U0 (two zeros) | `data/r1/target-B.json` | `key B/classify/hi/result` |
| N15 | `2.7853521306` | node radius of sigma (float, blind seat) | `data/blind/RESULT.json` | `key sigma0_9_5/background/node_radius` |
| N16 | `[0.0881154 +/- 4.45e-8]` | delta_0(10), nonlocal cut-off error, L = 0, R = 10 | `data/r1/target-B.json` | `key brackets/radii/10.0/0/delta` |
| N17 | `[1.10045 +/- 3.65e-6]` | exterior margin abs(E) - m/R - delta - eps, L = 0, R = 10 | `data/r1/target-B.json` | `key brackets/radii/10.0/0/ext_margin` |
| N18 | `[1.73551 +/- 4.81e-6]` | exterior margin, L = 0, R = 14 | `data/r1/target-B.json` | `key brackets/radii/14.0/0/ext_margin` |
| N19 | `2` | upper count #(L+(0) < eps), R = 14 | `data/r1/target-B.json` | `key brackets/radii/14.0/0/+/upper` |
| N20 | `1` | lower count #(L-(0) < -eps), R = 14 | `data/r1/target-B.json` | `key brackets/radii/14.0/0/-/lower` |
| N21 | `0` | upper count #(L+(3) < eps), R = 14 | `data/r1/target-B.json` | `key brackets/radii/14.0/3/+/upper` |
| N22 | `[-2.041380387 +/- 3.15e-10]` | d2 (constraint node D0), R = 10 | `data/r1/target-B.json` | `key brackets/radii/10.0/0/D0/d2` |
| N23 | `[-2.172289605 +/- 1.42e-10]` | d2 (constraint node D0), R = 14 | `data/r1/target-B.json` | `key brackets/radii/14.0/0/D0/d2` |
| N24 | `[1133.8 +/- 0.0894]` | M times abs(d2) at R = 10 (recomputed) | `checks/check_assembly.log` | `line 17` |
| N25 | `[4.775e+7 +/- 6.25e+3]` | M times abs(d2) at R = 14 (recomputed) | `checks/check_assembly.log` | `line 33` |
| N26 | `"0": 2` | K(0) = 2 (and K = (2, 2, 2, 0)) | `data/r1/target_verdict.json` | `key K` |
| N27 | `HOLDS` | verdict of the amended target run | `data/r1/target_verdict.json` | `key verdict` |
| N28 | `[1.10491108047488 +/- 4.15e-15]` | w of the negative-Krein eigenvalue, L = 0 (Krawczyk box) | `data/r1/target-K0.log` | `line 21` |
| N29 | `[1.25921337137566 +/- 6.39e-15]` | w of the positive-Krein control, L = 0 | `data/r1/target-K0.log` | `line 27` |
| N30 | `[0.539925668013455 +/- 2.97e-16]` | w, negative-Krein, L = 1 | `data/r1/target-K1.log` | `line 21` |
| N31 | `[0.951028237700108 +/- 2.59e-16]` | w, positive-Krein control, L = 1 | `data/r1/target-K1.log` | `line 26` |
| N32 | `[0.2968148506 +/- 6.42e-11]` | w, negative-Krein, L = 2 | `data/r1/target-K2.log` | `line 20` |
| N33 | `[0.5179458643 +/- 7.13e-11]` | w, positive-Krein control, L = 2 | `data/r1/target-K2.log` | `line 25` |
| N34 | `-3.061281342e-6 +/- 4.63e-13` | <a, d>, L = 0, negative-Krein | `data/r1/target-K0.json` | `key neg/krein_ad` |
| N35 | `-6.212149350e-5 +/- 1.10e-13` | <a, d>, L = 1, negative-Krein | `data/r1/target-K1.json` | `key neg/krein_ad` |
| N36 | `-0.0002403151062 +/- 1.86e-07` | <a, d>, L = 2, negative-Krein | `data/r1/target-K2.json` | `key neg/krein_ad` |
| N37 | `+4.507783361e-7` | <a, d>, L = 0, positive-Krein control (sign +) | `proof/PROOF-R1-v2.md` | `line 864` |
| N38 | `2.44e-20` | tail bound on <a, d> beyond r = 26, L = 0 | `data/r1/target-K0.json` | `key neg/tail_bound` |
| N39 | `3.69e-12` | contraction constant theta of the tail lemma, L = 0 | `data/r1/target-K0.json` | `key neg/theta` |
| N40 | `U0' contained in computed U0: True` | containment of the stated start interval | `checks/check_U0.log` | `line 6` |
| N41 | `3.1 to 3.6` | code/true ratio of the Frobenius remainder constants (R4, R3) | `proof/PROOF-R1-v2.md` | `line 665` |
| N42 | `ALL PASS` | check_assembly result | `checks/check_assembly.log` | `line 56` |
| N43 | `0.02413229272632793` | NULL, sigma0 = 1/2: certified lower end of Re lambda (L = 0) | `data/r1/cal/NULL.json` | `key evans/re_lower` |
| N44 | `0.2832272004` | NULL, sigma0 = 1/2: Im lambda (10-digit midpoint) | `data/r1/cal/NULL.json` | `key evans/lam_im` |
| N45 | `0.08827420125417403` | C-P2 (Schroedinger-Poisson n = 1, L = 0): lower end of Re lambda | `data/r1/cal/C-P2.json` | `key evans/re_lower` |
| N46 | `0.09917673961346397` | C-P3 (Schroedinger-Poisson n = 1, L = 2): lower end of the real growing eigenvalue | `data/r1/cal/C-P3.json` | `key evans/re_lower` |
| N47 | `[0.189203706825 +/- 1.76e-13]` | C-B2: E1/E0 of Schroedinger-Poisson at equal particle number | `data/r1/controls_verdict.json` | `key C-B2/ratio` |
| N48 | `[0.1884, 0.1896]` | C-B2 sealed window (math-ph/0208045 Table 1) | `seals/BAR-R1-FINAL.md` | `line 61` |
| N49 | `-3.1054402544` | E, blind float | `data/blind/RESULT.json` | `key sigma0_9_5/background/E` |
| N50 | `19.158712546` | m, blind float | `data/blind/RESULT.json` | `key sigma0_9_5/background/m_int_sigma2_r2_dr` |
| N51 | `1.1049110805` | w, negative-Krein, L = 0, blind float | `data/blind/verdict_blind.out` | `line 17` |
| N52 | `5.5e-13 (L=0), 5.4e-12 (L=1), 7.6e-12 (L=2), 1.6e-11 (L=3)` | max Re lambda per L, blind float | `data/blind/RESULT.md` | `line 106` |
| N53 | `complex quartet {+-0.0241322927 +- 0.2832272004 i}` | blind positive control at sigma0 = 1/2 | `data/blind/RESULT.json` | `key sigma0_1_2/L/0/unstable_mode/type` |
| N54 | `The common stability band is [1.596312, 1.984129]` | float band (headline) | `data/band-map/MAP.md` | `line 25` |
| N55 | `sigma_lo = 1.5963117 +- 1e-7` | float lower edge | `data/band-map/MAP.md` | `line 26` |
| N56 | `sigma_hi = 1.9841288 +- 1e-7` | float upper edge | `data/band-map/MAP.md` | `line 27` |
| N57 | `[1.59631162, 1.59631172]` | lower edge bracket, refined grid (65.7, 261, 9) | `data/band-map/MAP.md` | `line 126` |
| N58 | `[1.98412876, 1.98412883]` | upper edge bracket, refined grid (60, 250, 9) | `data/band-map/MAP.md` | `line 127` |
| N59 | `Band width 0.38782` | float band width | `data/band-map/MAP.md` | `line 129` |
| N60 | `~1.01476 (merge)` | collision frequency, lower edge (L = 0) | `data/band-map/MAP.md` | `line 138` |
| N61 | `~0.46371 (merge)` | collision frequency, upper edge (L = 2) | `data/band-map/MAP.md` | `line 161` |
| N62 | `a ~ 0.1427 sqrt(sigma_lo - sigma0)` | square-root growth below the lower edge | `data/band-map/MAP.md` | `line 147` |
| N63 | `a ~ 0.279 sqrt(sigma0 - sigma_hi)` | square-root growth above the upper edge | `data/band-map/MAP.md` | `line 168` |
| N64 | `w/\|E\| = 0.398` | lower collision at 40 % of abs(E) | `data/band-map/MAP.md` | `line 152` |
| N65 | `w/\|E\| = 0.126` | upper collision at 13 % of abs(E) | `data/band-map/MAP.md` | `line 169` |
| N66 | `-2.2470 at the edge` | VK = <L+^-1 r sigma, r sigma> at the lower edge (smooth, negative) | `data/band-map/MAP.md` | `line 150` |
| N67 | `0.029367442 +- 0.978168536 i` | float growing eigenvalue at sigma0 = 1.55 (L = 0), three resolutions | `data/band-map/MAP.md` | `line 195` |
| N68 | `0.073523517 +- 0.48414557 i` | float growing eigenvalue at sigma0 = 2.05 (L = 2), three resolutions | `data/band-map/MAP.md` | `line 196` |
| N69 | `\| 2.00 \| 0 \| 0.0354 \|` | float L = 2 growth rate at sigma0 = 2.00 | `data/band-map/MAP.md` | `line 102` |
| N70 | `by 0.046 at the bottom` | difference to the published band, both sides (0.046 low, 0.086 high) | `data/band-map/MAP.md` | `line 189` |
| N71 | `\| 3 \| 2.75 .. 5.00 \|` | L = 3 unstable on the coarse grid from 2.75 | `data/band-map/MAP.md` | `line 72` |
| N72 | `\| 4 \| 4.05 .. 5.00 \|` | L = 4 unstable on the coarse grid from 4.05 | `data/band-map/MAP.md` | `line 73` |
| N73 | `0.540 at 9/5` | L = 1 negative-Krein mode that never collides | `data/band-map/MAP.md` | `line 231` |
| N74 | `1595/1000` | R2 unstable point just below the lower edge | `seals/BAR-R2-EDGES.md` | `line 49` |
| N75 | `1983/1000` | R2 stable point just inside the upper edge | `seals/BAR-R2-EDGES.md` | `line 51` |
| N76 | `F r0^2/6 < 2.5e-10` | actual variation of sigma on [0, r0] (bootstrap of Lemma 3.1) | `proof/PROOF-R1-v2.md` | `line 211` |
| N77 | `[1.15920 +/- 2.79e-6]` | exterior margin, L = 1, R = 10 | `data/r1/target-B.json` | `key brackets/radii/10.0/1/ext_margin` |
| N78 | `[1.17095 +/- 4.08e-6]` | exterior margin, L = 2, R = 10 | `data/r1/target-B.json` | `key brackets/radii/10.0/2/ext_margin` |
| N79 | `[1.17598 +/- 1.10e-6]` | exterior margin, L = 3, R = 10 | `data/r1/target-B.json` | `key brackets/radii/10.0/3/ext_margin` |
| N80 | `Background rtol is 1e-10` | float map background tolerance | `data/band-map/MAP.md` | `line 17` |
| N81 | `R = max(40, 70/sqrt(-E))` | float map box radius (refined level: 1.5 R, 1.67 N, degree 9) | `data/band-map/MAP.md` | `line 18` |
| N82 | `all 9 printed digits across three resolutions` | agreement of the endpoint checks | `data/band-map/MAP.md` | `line 217` |
| N83 | `1595/1000, 1597/1000, 1983/1000, 1985/1000, 31/20, 2, 33/20, 17/10, 7/4, 37/20, 19/10, 39/20` | the twelve sealed R2 points | `seals/BAR-R2-EDGES.md` | `line 210` |
| N84 | `to width 0.002` | width of an edge bracket if both edge points HOLD | `seals/BAR-R2-EDGES.md` | `line 213` |
| N85 | `target-B.json wall 78 s` | logged wall time, target-B | `data/r1/target-B.log` | `line 35` |
| N86 | `target-K0.json wall 655 s` | logged wall time, target-K0 | `data/r1/target-K0.log` | `line 28` |
| N87 | `target-K1.json wall 621 s` | logged wall time, target-K1 | `data/r1/target-K1.log` | `line 27` |
| N88 | `target-K2.json wall 417 s` | logged wall time, target-K2 | `data/r1/target-K2.log` | `line 27` |
| N89 | `530.96` | wall time of the NULL control job (s) | `data/r1/cal/NULL.json` | `key wall_seconds` |
| N90 | `peak 0.79 GB` | peak memory of a target job | `data/r1/target-K0.log` | `line 29` |
| N91 | `Peak memory was 1.07 GB` | peak memory of the float map | `data/band-map/MAP.md` | `line 22` |
| N92 | `0.04817016568` | C-P2 certified ratio Re(lambda)/(2 abs(E1)) (published 0.0451) | `data/r1/controls_verdict.json` | `key C-P2/ratio_re` |
| N93 | `7% float mismatch (0.0482 vs 0.0451)` | mock-informed C-P2 window disclosure | `seals/BAR-R1-FINAL.md` | `line 69` |
| N94 | `which differ by 3e-7` | base vs refined lower-edge midpoints | `data/band-map/MAP.md` | `line 209` |
| N95 | `under 1e-6 at the base grid and under 1e-7 at the refined grid` | edge bisection tolerances | `data/band-map/MAP.md` | `line 122` |
| N96 | `relative 1e-4 of 1.1049110805` | sealed blind pass rule (relative 1e-4) | `seals/BAR-R1-BLIND.md` | `line 23` |
| N97 | `1.55 <~ sigma0 <~ 2.07` | published common stability band (L = 0..12) | `arXiv:2402.07998v2, Fig. 8 caption` | external |

## R2 certified numbers (BAR-R2-EDGES, seal 3ad051728e)

Boxes are the `refine:` lines of the R2 run logs (the JSON `w` / `lam` strings are not used). Edge brackets and point
values such as 1.595 are the exact sealed rationals (1595/1000 etc.); growth rates quoted as 0.0294 and 0.0354 are
roundings of the certified Re λ rows below.

| id | printed | meaning | file | locator |
|---|---|---|---|---|
| N98 | `"verdict": "HOLDS"` | verdict at sigma0 = 1597/1000 (stable point lo-s) | `data/r2/lo-s/verdict.json` | `line 75` |
| N99 | `[1.01156658375 +/- 2.89e-12]` | negative-Krein w, L = 0, sigma0 = 1597/1000 | `data/r2/logs/K0_lo-s.log` | `line 20` |
| N100 | `[1.01905618960 +/- 2.20e-12]` | positive-Krein partner w, L = 0, sigma0 = 1597/1000 | `data/r2/logs/K0_lo-s.log` | `line 25` |
| N101 | `-1.612233679e-6 +/- 7.95e-11` | <a,d> of the negative-Krein mode, L = 0, sigma0 = 1597/1000 | `data/r2/lo-s/K0.json` | `key neg/krein_ad` |
| N102 | `1.659832199e-6 +/- 8.89e-11` | <a,d> of the positive-Krein partner, L = 0, sigma0 = 1597/1000 | `data/r2/lo-s/K0.json` | `key pos/krein_ad` |
| N103 | `0.007489` | certified lower bound on the distance between the two w boxes | `data/r2/lo-s/K0.json` | `key separation/certified_separation_lower` |
| N104 | `[0.454300995393917 +/- 2.58e-16]` | negative-Krein w, L = 1, sigma0 = 1597/1000 | `data/r2/logs/K1_lo-s.log` | `line 19` |
| N105 | `[0.201778070 +/- 1.20e-10]` | negative-Krein w, L = 2, sigma0 = 1597/1000 | `data/r2/logs/K2_lo-s.log` | `line 20` |
| N106 | `"verdict": "HOLDS"` | verdict at sigma0 = 33/20 (stable point g165) | `data/r2/g165/verdict.json` | `line 75` |
| N107 | `[1.0231166878309 +/- 3.50e-14]` | negative-Krein w, L = 0, sigma0 = 33/20 | `data/r2/logs/K0_g165.log` | `line 20` |
| N108 | `[0.476046298668078 +/- 2.95e-16]` | negative-Krein w, L = 1, sigma0 = 33/20 | `data/r2/logs/K1_g165.log` | `line 20` |
| N109 | `[0.2239829738 +/- 5.79e-11]` | negative-Krein w, L = 2, sigma0 = 33/20 | `data/r2/logs/K2_g165.log` | `line 20` |
| N110 | `"verdict": "HOLDS"` | verdict at sigma0 = 17/10 (stable point g170) | `data/r2/g170/verdict.json` | `line 75` |
| N111 | `[1.04813654968334 +/- 6.83e-15]` | negative-Krein w, L = 0, sigma0 = 17/10 | `data/r2/logs/K0_g170.log` | `line 20` |
| N112 | `[0.496958900414915 +/- 1.01e-16]` | negative-Krein w, L = 1, sigma0 = 17/10 | `data/r2/logs/K1_g170.log` | `line 19` |
| N113 | `[0.2463961212 +/- 3.79e-11]` | negative-Krein w, L = 2, sigma0 = 17/10 | `data/r2/logs/K2_g170.log` | `line 20` |
| N114 | `"verdict": "HOLDS"` | verdict at sigma0 = 7/4 (stable point g175) | `data/r2/g175/verdict.json` | `line 75` |
| N115 | `[1.07581074350611 +/- 5.75e-15]` | negative-Krein w, L = 0, sigma0 = 7/4 | `data/r2/logs/K0_g175.log` | `line 20` |
| N116 | `[0.518253661596410 +/- 3.63e-16]` | negative-Krein w, L = 1, sigma0 = 7/4 | `data/r2/logs/K1_g175.log` | `line 21` |
| N117 | `[0.2705262718 +/- 4.21e-11]` | negative-Krein w, L = 2, sigma0 = 7/4 | `data/r2/logs/K2_g175.log` | `line 21` |
| N118 | `"verdict": "HOLDS"` | verdict at sigma0 = 37/20 (stable point g185) | `data/r2/g185/verdict.json` | `line 75` |
| N119 | `[1.13496776996447 +/- 1.92e-15]` | negative-Krein w, L = 0, sigma0 = 37/20 | `data/r2/logs/K0_g185.log` | `line 20` |
| N120 | `[0.561969440698342 +/- 2.05e-16]` | negative-Krein w, L = 1, sigma0 = 37/20 | `data/r2/logs/K1_g185.log` | `line 20` |
| N121 | `[0.3260149986 +/- 2.07e-11]` | negative-Krein w, L = 2, sigma0 = 37/20 | `data/r2/logs/K2_g185.log` | `line 21` |
| N122 | `"verdict": "HOLDS"` | verdict at sigma0 = 19/10 (stable point g190) | `data/r2/g190/verdict.json` | `line 75` |
| N123 | `[1.16574473209241 +/- 4.12e-15]` | negative-Krein w, L = 0, sigma0 = 19/10 | `data/r2/logs/K0_g190.log` | `line 20` |
| N124 | `[0.584378958602663 +/- 8.78e-17]` | negative-Krein w, L = 1, sigma0 = 19/10 | `data/r2/logs/K1_g190.log` | `line 20` |
| N125 | `[0.3596652774 +/- 3.80e-11]` | negative-Krein w, L = 2, sigma0 = 19/10 | `data/r2/logs/K2_g190.log` | `line 21` |
| N126 | `"verdict": "HOLDS"` | verdict at sigma0 = 39/20 (stable point g195) | `data/r2/g195/verdict.json` | `line 75` |
| N127 | `[1.19710410286268 +/- 2.65e-15]` | negative-Krein w, L = 0, sigma0 = 39/20 | `data/r2/logs/K0_g195.log` | `line 20` |
| N128 | `[0.607147685016223 +/- 5.12e-16]` | negative-Krein w, L = 1, sigma0 = 39/20 | `data/r2/logs/K1_g195.log` | `line 21` |
| N129 | `[0.4023308222 +/- 6.45e-11]` | negative-Krein w, L = 2, sigma0 = 39/20 | `data/r2/logs/K2_g195.log` | `line 20` |
| N130 | `"verdict": "HOLDS"` | verdict at sigma0 = 1983/1000 (stable point hi-s) | `data/r2/hi-s/verdict.json` | `line 75` |
| N131 | `[1.21807583965753 +/- 1.39e-15]` | negative-Krein w, L = 0, sigma0 = 1983/1000 | `data/r2/logs/K0_hi-s.log` | `line 20` |
| N132 | `[0.622368426994779 +/- 2.65e-16]` | negative-Krein w, L = 1, sigma0 = 1983/1000 | `data/r2/logs/K1_hi-s.log` | `line 21` |
| N133 | `[0.453984310 +/- 5.20e-10]` | negative-Krein w, L = 2, sigma0 = 1983/1000 | `data/r2/logs/K2_hi-s.log` | `line 21` |
| N134 | `[0.472730296 +/- 5.38e-10]` | positive-Krein partner w, L = 2, sigma0 = 1983/1000 | `data/r2/logs/K2_hi-s.log` | `line 25` |
| N135 | `-2.889527238e-6 +/- 2.99e-08` | <a,d> of the negative-Krein mode, L = 2, sigma0 = 1983/1000 | `data/r2/hi-s/K2.json` | `key neg/krein_ad` |
| N136 | `2.764440422e-6 +/- 2.90e-08` | <a,d> of the positive-Krein partner, L = 2, sigma0 = 1983/1000 | `data/r2/hi-s/K2.json` | `key pos/krein_ad` |
| N137 | `0.018745` | certified lower bound on the distance between the two w boxes | `data/r2/hi-s/K2.json` | `key separation/certified_separation_lower` |
| N138 | `[0.005159936765 +/- 9.79e-13]` | certified Re lambda, L = 0, sigma0 = 1595/1000 (lo-u) | `data/r2/logs/U_lo-u.log` | `line 20` |
| N139 | `[1.01371961231 +/- 4.07e-12]` | certified Im lambda, L = 0, sigma0 = 1595/1000 | `data/r2/logs/U_lo-u.log` | `line 20` |
| N140 | `[0.029367442235 +/- 6.23e-13]` | certified Re lambda, L = 0, sigma0 = 31/20 (in-155) | `data/r2/logs/U_in-155.log` | `line 19` |
| N141 | `[0.978168535545 +/- 7.14e-13]` | certified Im lambda, L = 0, sigma0 = 31/20 | `data/r2/logs/U_in-155.log` | `line 19` |
| N142 | `[0.0353872961 +/- 2.52e-11]` | certified Re lambda, L = 2, sigma0 = 2 (in-200) | `data/r2/logs/U_in-200.log` | `line 20` |
| N143 | `[0.4686174535 +/- 2.65e-11]` | certified Im lambda, L = 2, sigma0 = 2 | `data/r2/logs/U_in-200.log` | `line 20` |
| N144 | `[0.008240881 +/- 3.74e-10]` | certified Re lambda, L = 2, sigma0 = 1985/1000 (hi-u) | `data/r2/logs/U_hi-u.log` | `line 20` |
| N145 | `[0.463975628 +/- 5.55e-10]` | certified Im lambda, L = 2, sigma0 = 1985/1000 | `data/r2/logs/U_hi-u.log` | `line 20` |
| N146 | `3.26257829877873232632728523408544749250724679772354387125538` | u_mid (60 digits) at sigma0 = 1597/1000 | `checks/check_u0_r2.log` | `line 2` |
| N147 | `3.43211518960578683230289225606858139753236980535419033262268` | u_mid (60 digits) at sigma0 = 33/20 | `checks/check_u0_r2.log` | `line 4` |
| N148 | `3.59659207485142889921563217406404416977402901494387498760527` | u_mid (60 digits) at sigma0 = 17/10 | `checks/check_u0_r2.log` | `line 6` |
| N149 | `3.76554052577800818868878023500042080295687479763023181911048` | u_mid (60 digits) at sigma0 = 7/4 | `checks/check_u0_r2.log` | `line 8` |
| N150 | `4.11710126372510784661490336736586880648244811516454564809644` | u_mid (60 digits) at sigma0 = 37/20 | `checks/check_u0_r2.log` | `line 13` |
| N151 | `4.29983054407140852492383796452184831740940264326441840450233` | u_mid (60 digits) at sigma0 = 19/10 | `checks/check_u0_r2.log` | `line 15` |
| N152 | `4.48726521011202076693095150956315573980034448089016171545471` | u_mid (60 digits) at sigma0 = 39/20 | `checks/check_u0_r2.log` | `line 17` |
| N153 | `4.61357440252882992130093660916470009950424657162244902579940` | u_mid (60 digits) at sigma0 = 1983/1000 | `checks/check_u0_r2.log` | `line 19` |
| N154 | `ALL PASS` | U0'_p containment and tube sha256 at all eight R2 points (two batches) | `checks/check_u0_r2.log` | `line 10` |
| N155 | `ALL 8 POINTS PASS` | Frobenius slack at the eight R2 stable points | `checks/check_frob_slack_r2.log` | `line 33` |
| N156 | `[142.1 +/- 0.0222]` | M at lo-s, R = 10 (with d2 = [-1.916371072 +/- 3.79e-11]: M times abs(d2) about 272, the smallest at any R2 point) | `data/r2/lo-s/B.json` | `key brackets/radii/10.0/0/D0/M` |
| N157 | `2.86e-10` | bound on F r0^2/6 (Lemma 3.1) at all R2 points: at hi-s F = (sg^2 + abs(u0) + 1/100) sg with sg = 1983/1000 + 1/100 and u0 from data/r2/hi-s/B.json gives 2.855e-10, the largest (recomputed by the R2 referee and again for this release) | `data/r2/hi-s/B.json (derived)` | external |
