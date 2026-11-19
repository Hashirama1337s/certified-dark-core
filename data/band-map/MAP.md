# MAP: where the one-node repulsive GPP state stops being linearly stable (R2-BAND, seat band-1)

**Everything here is NOT SEALED, float.** Double-precision B-spline Galerkin numbers, checked only by changing the
resolution. Nothing here is certified.

## Engine
- Engine: the blind seat's validated pipeline (core/blind/seat: bg.py, fem.py; spec.py's operators), copied to
  core/band/map/. The blind seat's files were not edited.
- Model: n = 1, repulsive, alpha = 1, eq. 9 units of 2402.07998. Spectrum of J diag(L+, L-) per sector L.
- Three changes to my copies only:
  1. bg.py `bracket_near`: brackets u0 around a guess carried over from the previous sigma0, using the same rtol as the
     bisection.
  2. bg.py tail start: the tail now starts 0.5 past the node. Without this, at 1.43 and 1.79 a grid sample sitting
     right on the node was taken as the start of the tail, which gave a bogus E of about -0.03 to -0.1. I recomputed
     both points after the fix, and a guard now rejects any such background.
  3. fem.py: the last breakpoint is clamped to R (a rounding error had raised a knot-order error).
- Background rtol is 1e-10. The blind seat showed it agrees with 1e-12 to about 5e-14 in E and u0.
- Box size is set by the background: R = max(40, 70/sqrt(-E)), N = 150 + 1.5 (R - 40), p = 7. Refined level:
  1.5 R, 1.67 N, p = 9. A third resolution (1.25 R, 1.35 N, p = 8) was used for some checks.
- "max Re lambda" leaves out |lambda| < 1e-5, which are the generalised-kernel pairs.
- Compute: about 25 minutes of wall-clock in total. Every run was under 10 min, at most 2 ran at once, all under
  memcap. Peak memory was 1.07 GB.

## Headline (float)
**The common stability band is [1.596312, 1.984129].**
- Lower edge: sigma_lo = 1.5963117 +- 1e-7, set by L = 0.
- Upper edge: sigma_hi = 1.9841288 +- 1e-7, set by L = 2.
- **Both edges are Krein collisions.** A negative-Krein internal mode meets a positive-Krein one, and the pair leaves
  the imaginary axis as a complex quartet.
- **Neither edge is a real crossing.** n(L+) and n(L-) do not change at either edge, and the VK quantity stays negative
  and smooth.

## 1. Sweeps

### Coarse sweep: sigma0 = 0.30 .. 5.00, step 0.05, L = 0..6 (95 points)
Below: max Re lambda (0 means below 1e-6, i.e. rounding at 1e-11 to 1e-10), at selected sigma0. Each L has at most 1
unstable eigenvalue (counted per quartet or per real pair) anywhere on the grid.

| sigma0 | E | m | L=0 | L=1 | L=2 | L=3 | L=4 | L=5 | L=6 |
|---|---|---|---|---|---|---|---|---|---|
| 0.30 | -0.30188 | 4.6213 | 0.019 | 0 | 0.0276 | 0 | 0 | 0 | 0 |
| 0.50 | -0.53740 | 6.3548 | 0.0241 | 0 | 0.0422 | 0 | 0 | 0 | 0 |
| 0.75 | -0.87843 | 8.4528 | 0.0419 | 0 | 0.0509 | 0 | 0 | 0 | 0 |
| 1.00 | -1.28062 | 10.6403 | 0.0546 | 0 | 0.0309 | 0 | 0 | 0 | 0 |
| 1.05 | -1.36934 | 11.0974 | 0.0562 | 0 | 0.00732 | 0 | 0 | 0 | 0 |
| 1.10 | -1.46102 | 11.5625 | 0.0575 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1.25 | -1.75478 | 13.0105 | 0.0581 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1.50 | -2.31201 | 15.6269 | 0.0403 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1.55 | -2.43439 | 16.1841 | 0.0294 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1.60 | -2.56060 | 16.7535 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1.75 | -2.96308 | 18.5377 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1.95 | -3.55810 | 21.1042 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2.00 | -3.71773 | 21.7809 | 0 | 0 | 0.0354 | 0 | 0 | 0 | 0 |
| 2.25 | -4.58412 | 25.3850 | 0 | 0 | 0.159 | 0 | 0 | 0 | 0 |
| 2.50 | -5.56851 | 29.3698 | 0 | 0 | 0.238 | 0 | 0 | 0 | 0 |
| 2.70 | -6.44400 | 32.8406 | 0 | 0 | 0.295 | 0 | 0 | 0 | 0 |
| 2.75 | -6.67531 | 33.7482 | 0 | 0 | 0.308 | 0.0897 | 0 | 0 | 0 |
| 3.00 | -7.90728 | 38.5269 | 0 | 0 | 0.373 | 0.381 | 0 | 0 | 0 |
| 3.50 | -10.75198 | 49.2947 | 0 | 0 | 0.487 | 0.82 | 0 | 0 | 0 |
| 4.00 | -14.10634 | 61.6737 | 0 | 0 | 0.582 | 1.27 | 0 | 0 | 0 |
| 4.05 | -14.46978 | 62.9998 | 0 | 0 | 0.59 | 1.31 | 0.236 | 0 | 0 |
| 4.50 | -17.96904 | 75.6530 | 0 | 0 | 0.656 | 1.72 | 1.45 | 0 | 0 |
| 5.00 | -22.33794 | 91.2230 | 0 | 0 | 0.709 | 2.18 | 2.32 | 0 | 0 |

Unstable grid intervals (grid resolution 0.05):

| L | Unstable on the grid | Where it is stable |
|---|---|---|
| 0 | 0.30 .. 1.55 | from 1.60 up to 5.00 |
| 1 | never | everywhere |
| 2 | 0.30 .. 1.05, and 2.00 .. 5.00 | the band [1.10, 1.95] |
| 3 | 2.75 .. 5.00 | below 2.75 |
| 4 | 4.05 .. 5.00 | below 4.05 |
| 5, 6 | never | everywhere |

- **Artifact, removed.** For sigma0 >= 3.75 the base grid shows a tiny real L=0 eigenvalue: 1e-5 at 3.75, rising to
  4.6e-4 at 5.0.
  - It is the generalised-kernel (phase / dE Jordan) pair, which splits by more than the 1e-5 filter at R = 40.
  - It disappears under refinement. At sigma0 = 4.0: 2.36e-5 at (40, 150, 7), then 8.1e-13 at (60, 250, 9) and 4.7e-13
    at (50, 202, 8). At sigma0 = 4.5: 1.18e-4 at the base grid, then 4.9e-13 and 2.5e-13.
  - The L = 0 entries in the table therefore drop it.
- Along the whole family, m increases and E decreases strictly with sigma0. So there is no mass extremum in [0.3, 5],
  and dm/dE = 2 VK < 0 throughout (VK runs from -4.14 to -1.77).

### Fine sweep: sigma0 = 1.30 .. 2.40, step 0.01, L = 0..14 (111 points)

| sigma0 | L=0 max Re | L=2 max Re | max over L = 1, 3..14 |
|---|---|---|---|
| 1.30 | 0.057 | 0 | 2.0e-10 |
| 1.40 | 0.0519 | 0 | 7.8e-11 |
| 1.50 | 0.0403 | 0 | 8.5e-11 |
| 1.55 | 0.0294 | 0 | 5.2e-11 |
| 1.57 | 0.0226 | 0 | 1.6e-10 |
| 1.58 | 0.0179 | 0 | 1.1e-10 |
| 1.59 | 0.0113 | 0 | 7.3e-11 |
| 1.60 | 0 | 0 | 1.1e-10 |
| 1.70 | 0 | 0 | 6.9e-11 |
| 1.80 | 0 | 0 | 9.6e-11 |
| 1.90 | 0 | 0 | 4.3e-11 |
| 1.98 | 0 | 0 | 2.7e-11 |
| 1.99 | 0 | 0.0214 | 6.0e-11 |
| 2.00 | 0 | 0.0354 | 7.7e-11 |
| 2.05 | 0 | 0.0735 | 5.6e-11 |
| 2.10 | 0 | 0.0994 | 3.6e-11 |
| 2.20 | 0 | 0.141 | 4.6e-11 |
| 2.30 | 0 | 0.176 | 9.1e-11 |
| 2.40 | 0 | 0.208 | 5.4e-11 |

- On [1.3, 2.4], only L = 0 (below 1.596) and L = 2 (above 1.984) are ever unstable. L = 1 and L = 3..14 never are:
  their worst max Re lambda is 2e-10, which is rounding.
- **Cutoff L = 3, with L = 13 and 14 as the two clean confirmers.**
  - Why: for every L from 3 to 14, at all 111 points, n(L+) = n(L-) = 0.
  - With no negative directions, the Hamiltonian-Krein count n(L+) + n(L-) = n_real + 2 n_complex + 2 n_negKrein
    allows no unstable eigenvalue.
  - The centrifugal term L(L+1)/r^2 only grows with L, so higher L stay positive as well. This step is inferred, not
    computed beyond L = 14.
  - L = 1 has n(L+) = n(L-) = 1 throughout, both used up by its one negative-Krein mode. L = 0 and L = 2 have counts
    (2, 1) and (1, 1).
- Two fine-grid points (1.43 and 1.79) were recomputed after the tail-start fix. They are clean and fit their
  neighbours.

## 2. The edges (bisected to under 1e-6 at the base grid and under 1e-7 at the refined grid)

| edge | sector | base (R, N, p) | base bracket | refined (R, N, p) | refined bracket |
|---|---|---|---|---|---|
| lower | L=0 | (43.8, 156, 7) | [1.59631165, 1.59631226] | (65.7, 261, 9) | [1.59631162, 1.59631172] |
| upper | L=2 | (40, 150, 7) | [1.98412842, 1.98412903] | (60, 250, 9) | [1.98412876, 1.98412883] |

**Float edges: sigma_lo = 1.5963117, sigma_hi = 1.9841288.** Band width 0.38782.

### Lower edge, sigma_lo = 1.5963117 (L = 0): Krein collision
On the stable side (above the edge), the negative-Krein L=0 mode moves up toward a positive-Krein mode coming down:

| sigma0 | w, Krein - | w, Krein + | gap |
|---|---|---|---|
| sigma_lo + 0.002 | 1.009964 | 1.022748 | 0.0128 |
| sigma_lo + 1e-4 | 1.013415 | 1.016272 | 0.0029 |
| at the edge | ~1.01476 (merge) | ~1.01476 (merge) | 0 |

- The negative-Krein mode is the one at w = 1.10491 at sigma0 = 9/5.
- The positive-Krein partner continues the blind seat's 1.25921 at 9/5.
- Below the edge they form a quartet lambda = +-a +- i b:
  - sigma_lo - 1e-4: a = 1.4266e-3, b = 1.014684
  - sigma_lo - 0.002: a = 6.3674e-3, b = 1.013172
- The two resolutions give a = 1.4246e-3 / 1.4266e-3 at -1e-4 and 6.3670e-3 / 6.3674e-3 at -0.002. These are
  measured from each grid's own edge, and the differences are consistent with the 3e-7 shift of the edge between grids.
- Growth follows a ~ 0.1427 sqrt(sigma_lo - sigma0), the square-root law of a generic Krein collision.
- Not a real crossing:
  - n(L+) = 2 and n(L-) = 1 on both sides.
  - VK = <L+^-1 r sigma, r sigma> = -2.2470 at the edge (-2.24779 at -0.002, -2.24618 at +0.002). Since VK =
    (1/2) dm/dE, dm/dE = -4.494 < 0, smooth.
  - The collision sits at w/|E| = 0.398, deep inside the gap 0 < w < |E| = 2.5510.

### Upper edge, sigma_hi = 1.9841288 (L = 2): Krein collision
On the stable side (below the edge):

| sigma0 | w, Krein - | w, Krein + | gap |
|---|---|---|---|
| sigma_hi - 0.002 | 0.450616 | 0.475560 | 0.0249 |
| sigma_hi - 1e-4 | 0.460883 | 0.466468 | 0.0056 |
| at the edge | ~0.46371 (merge) | ~0.46371 (merge) | 0 |

- The negative-Krein mode is the lowest L=2 mode (0.29681 at sigma0 = 9/5), climbing.
- The partner is the second L=2 mode (0.51795 at 9/5), falling.
- Above the edge, the quartet:
  - sigma_hi + 1e-4: a = 2.7909e-3, b = 0.463737
  - sigma_hi + 0.002: a = 1.24919e-2, b = 0.464325
- Growth follows a ~ 0.279 sqrt(sigma0 - sigma_hi).
- n(L+) = n(L-) = 1 on both sides. L=0 VK = -2.1171 (dm/dE = -4.234). The collision sits at w/|E| = 0.126, with
  |E| = 3.6666.

**For the certified run.** The growing eigenvalue (float), to enclose:

| sigma0 | sector | lambda |
|---|---|---|
| sigma_lo - 0.002 = 1.5943117 | L=0 | 6.367e-3 +- 1.01317 i |
| sigma_lo - 1e-4 | L=0 | 1.427e-3 +- 1.01468 i |
| sigma_hi + 1e-4 | L=2 | 2.791e-3 +- 0.46374 i |
| sigma_hi + 0.002 = 1.9861288 | L=2 | 1.2492e-2 +- 0.46433 i |

- On the stable side, the certified run must separate two imaginary-axis eigenvalues of opposite Krein sign. Their gaps:
  - L=0: 0.0128 at +0.002 and 0.0029 at +1e-4
  - L=2: 0.0249 at -0.002 and 0.0056 at -1e-4
- Brackets at +-0.002 are about 4x easier than at +-1e-4 (the gap scales like sqrt(distance)).

## 3. Comparison with the paper (2402.07998.txt:1073, :1124; Fig. 8 caption)
- The paper says the common stability band is "1.55 <~ sigma0 <~ 2.07" for L = 0..12, built from per-L bands with
  "one (two) unstable mode(s)" shading.
- **My band [1.59631, 1.98413] lies strictly inside the paper's.** It is narrower on both sides, by 0.046 at the bottom
  and 0.086 at the top.
- At the paper's two endpoints the state is clearly unstable, at three resolutions:

  | sigma0 | sector | lambda | resolutions (R, N, p) |
  |---|---|---|---|
  | 1.55 | L=0 | 0.029367442 +- 0.978168536 i | (44.9, 157, 7), (67.3, 262, 9), (80, 300, 7) |
  | 2.05 | L=2 | 0.073523517 +- 0.48414557 i | same three |

  2.05 lies inside the paper's band. At 2.07, max Re lambda = 0.085 at L=2.
- So the difference is not a convergence effect on my side. The paper's "<~" leaves room for this, and Fig. 8 could not
  be checked numerically from text alone (I have only the caption).
- Agreements with the paper:
  - The sectors match its qualitative picture: L=0 bands for the repulsive excited state, and L >= 3 stable inside the
    band ("for high enough L the stable band covers entirely the region").
  - Both edges have one unstable mode just outside (the paper's "lighter" shading).
- I see no second unstable mode in any L on [0.3, 5] (at most 1 per L per point).

## 4. Convergence
- Edge location, base grid vs refined grid:
  - Lower: midpoints 1.59631196 and 1.59631167, which differ by 3e-7.
  - Upper: midpoints 1.98412872 and 1.98412880, which differ by 8e-8.
  - Both are under 1e-5, and in fact under 1e-6. Each difference sits inside the coarser bisection bracket (6e-7), so
    the true resolution spread is at most about 3e-7.
- Growth rates just outside agree to 3 to 5 digits between resolutions:
  - Upper edge, +1e-4: 2.7899e-3 vs 2.7909e-3. At +0.002: 1.24917e-2 vs 1.24919e-2.
  - The remaining spread comes from each grid offsetting from its own edge.
  - At a fixed sigma0 (the paper-endpoint checks) all digits agree.
- The paper-endpoint checks agree to all 9 printed digits across three resolutions.
- The background is identical whatever continuation guess is used: at sigma0 = 1.594312, E = -2.54604866336 at both
  rtol values and with or without a guess.
- n(L+), n(L-) and the Krein signs are identical at both resolutions at all four offsets of both edges.

## 5. Plain-words notes (UNTESTED unless stated)
- **Tested:** both edges are mode collisions, not a mass turning point and not a change in the negative-direction
  count. Mass rises smoothly through both edges, and n(L+-) is fixed across them. The paper notes too that the band
  boundary "is not determined by a maximum mass state".
- **Tested:** the internal-mode Rydberg series near |E| plays no role at either edge. The colliding modes sit at 40% (L=0)
  and 13% (L=2) of |E|, and both modes are low, well-converged modes.
- UNTESTED: each edge is set by the same mode of the blind seat's 9/5 list, the single negative-Krein mode of that
  sector. The L=0 one (1.105 at 9/5) falls as sigma0 drops and meets a falling positive mode. The L=2 one (0.297 at
  9/5) rises as sigma0 grows and meets a falling positive mode.
  - L=1 also carries one negative-Krein mode (0.540 at 9/5) that never collides anywhere in [0.3, 5]. That makes L=1 the
    only low sector with a negative-Krein mode that never destabilises. Why its neighbours stay apart is an open
    curiosity.
- UNTESTED: the large-sigma0 instabilities at L=3 (from about 2.72) and L=4 (from about 4.02) look like a different
  mechanism.
  - In the coarse sweep, max n(L-) for L = 3, 4 reaches 1 while n(L+) stays 0. That is consistent with an L- eigenvalue
    passing through zero, which would be a real-crossing type onset (real pair) rather than a Krein collision.
  - This is not bisected or checked mode by mode. It lies outside the band and does not affect it.
- UNTESTED: the lower L=2 band (unstable 0.3 to about 1.07, stable above) and the L=0 band edge at 1.596 do not
  overlap. So the common band is set by L=0 below and by the second L=2 band above. Between about 1.07 and 1.596 only
  L=0 is unstable.
- UNTESTED: the near-degeneracy of the L=2 (Krein -) and L=3 (Krein +) lowest modes, flagged by the blind seat at 9/5,
  is harmless as expected, since they do not couple. L=3 stays at n(L+-) = 0 throughout [1.3, 2.4].

## Files (data/band-map/)
- Engine copies: bg.py, fem.py.
- Drivers: lite.py (spectrum summary), sweep.py (continuation sweep), edge.py (bisection plus edge detail), check.py
  (refinement of one point), analyze.py (writes MAP.json and map.png), mdtab.py (tables), dbg_bg*.py (background
  debugging).
- Data:
  - Sweeps: sw_cA0.json, sw_cA.json, sw_cB.json (coarse); sw_f1.json, sw_f2.json (fine).
  - Edges: edge_lo0.json, edge_lo1.json, edge_hi0.json, edge_hi1.json.
  - Checks: chk_*.json.
  - Logs: *.log.
- MAP.json: all tables, edge brackets and details, the artifact check, and the monotonicity flags.
- map.png: max Re lambda vs sigma0. Left: coarse sweep, L = 0..6. Right: fine sweep, the unstable L only, with the band
  and the paper's endpoints marked.

Commands, all as `python -u <script>`:
- Coarse: `sweep.py cA0 0.3 2.6 0.05 6` (stopped at 0.55 on the knot error), `sweep.py cA 0.55 2.6 0.05 6`,
  `sweep.py cB 2.65 5.0 0.05 6`.
- Fine: `sweep.py f1 1.30 1.85 0.01 14`, `sweep.py f2 1.86 2.40 0.01 14`.
- Edges: `edge.py lo0 1.59 1.60 0 0 1e-6`, `edge.py hi0 1.98 1.99 2 0 1e-6`, `edge.py lo1 1.5962 1.5964 0 1 1e-7`,
  `edge.py hi1 1.9840 1.9843 2 1 1e-7`.
- Checks: `check.py {1.43,1.79} 0,...,14 0`, `check.py {4.0,4.5} 0 0,1,2`, `check.py 1.55 0 0,1 80 300 7 2.5`,
  `check.py 2.05 2 0,1 80 300 7 2.5`.
- Assemble: `analyze.py`.
