# CALIBRATION: build-W controls and unit costs (R3-WINDOW, pre-seal)

Seat build-W, 2026-11-19. No window node or schedule cell was certified. Every control ran with the instrument
hashes of RUN.md (verdict_w.py was written afterwards and only reads JSON). Raw outputs: out/controls/*.json,
out/controls/XC.jsonl; logs: logs/. Tubes were built in-run (bg_tube unchanged) except R1REG (seat disk cache; same
sha as R1) and the XC float backgrounds (design/probe caches, float only).

## Summary

| control | result | data |
|---|---|---|
| XK, nine G9 nodes, R = 20 | **PASS 27/27 sectors** | every node: kernel booked at w = 0 as (4,3), (3,2), (2,2); lower = upper at w- -+ 0.002 and w+ -+ 0.002; drop exactly 1 across every w-, rise exactly 1 across every w+; all nine tube sha256 equal the R2 shas |
| XU 1595/1000, L = 0 | **PASS** (INCONCLUSIVE, no drop in L = 0) | 171 grid points w = 0.01 j < 1.7130; 0 drop pairs; 0 undecided counts; counts only rise (3 -> 4 -> 5 -> 6 near the continuum); L = 1 drop certified (lower N(0.2721) = 3, upper N(0.6303) = 2), L = 2 drop certified (lower N(0) = 2, upper N(0.3461) = 1); 1148 s |
| XU 1985/1000, L = 2 | see the addendum at the end | |
| LOO-161: [1597/1000, 33/20], tube of 161/100 at theta = 13/53 | **PASS** | BR both halves: Y0 = 4.12e-7 / 4.03e-7, Z1 = 0.627 / 0.617, Z2hat = 32.1 / 31.6, rho_max = 2.21e-6 / 2.11e-6, r_u = 5.8e-3 / 6.1e-3, kappa(r_u) = 0.814 / 0.808; X-distance of the 161/100 tube to H_theta = 5.89e-8 <= rho_max (factor 38); tube X-diameters 5.7e-10, 2.6e-10 < r_u; one node and E < 0 at r_n; abs(E) >= 1.9058 |
| LOO-1595: [31/20, 1597/1000], tube of 1595/1000 at theta = 45/47 | **PASS** | BR: Z1 = 0.559 / 0.553, rho_max = 1.22e-6 / 1.18e-6, kappa = 0.779 / 0.776; X-distance 1.92e-9 <= rho_max of half 2 (1.18e-6); tube diameters 1.2e-9, 5.7e-10 < r_u |
| XI: tau_b + 1e-3 bump injected on [1597/1000, 33/20] | **PASS (REJECTED)** | "tau_B data at grid 1 do not match the certified re-step"; the same cell without injection is accepted (LOO-161) |
| XC (float) | **PASS 5/5** | table below |
| R1REG (brackets at 9/5) | **PASS** | every upper/lower count at R = 10, 14, L = 0..3 and the D0 constrained count equal build-3/out/r1; tube sha f8b0cc27... |
| loo-185w: the referee's example [7/4, 37/20] (width 0.1), tube of 9/5 | not a gate: **BR does not close** | Z1 = 1.168 / 1.143 >= 1 on the two halves (Y0 = 4.4e-6). The sup-norm route needs half-widths below about 0.04 (Z1 scales with theta Delta). The schedule's widest cell is 0.025. |

## XK details (counts upper/lower; R = 20; level 1e-3 at w = 0, 1e-5 elsewhere)

| node | L = 0: w=0; w- -0.002, w- +0.002, w+ -0.002, w+ +0.002 | L = 1 | L = 2 | wall |
|---|---|---|---|---|
| 1597/1000 | 4/3; 4/4 3/3 3/3 4/4 | 3/2; 3/3 2/2 2/2 3/3 | 2/2; 2/2 1/1 1/1 2/2 | 92 s |
| 33/20 | same pattern | same | same | 91 s |
| 17/10 | same | same | same | 90 s |
| 7/4 | same | same | same | 102 s |
| 9/5 | same | same | same | 135 s |
| 37/20 | same | same | same | 104 s |
| 19/10 | same | same | same | 127 s |
| 39/20 | same | same | same | 128 s |
| 1983/1000 | same | same | same | 103 s |

Calibration finding (PATCHES item 2): at R = 14 the L = 0 count at 7/4 read 4/3 at w+ - 0.002 = 1.2023. The FD of the
same Neumann interior problem shows why: the cut at R = 14 moves the positive-Krein crossing from 1.2043 to about
1.199 (the P channel is classically allowed up to r = m/(abs(E) - w), about 10.5). At R = 20 the certified and FD
counts both give 3. All cells therefore use R = 20.

## XC (float, N = 1000, R = 20; theta = position of the interior point)

| cell | point | L | m_a | m_b | true lowest eig on M | [chord - eta2, chord + eta2'] |
|---|---|---|---|---|---|---|
| [1.597, 1.6] | 1.5985 | 0 | 7.81e-5 | 5.34e-4 | 3.067e-4 | [2.804e-4, 3.413e-4] |
| [1.75, 1.8] | 1.775 | 0 | 0.02587 | 0.03448 | 0.03033 | [0.02316, 0.03970] |
| [1.75, 1.8] | 1.775 | 1 | 0.08367 | 0.08443 | 0.08445 | [0.08008, 0.08767] |
| [1.75, 1.8] | 1.775 | 2 | 0.04541 | 0.03716 | 0.04150 | [0.03792, 0.04372] |
| [39/20, 1.983] | 1.98 (theta = 10/11) | 2 | 6.28e-3 | 2.23e-4 | 8.71e-4 | [2.83e-4, 1.132e-3] |

(The "slip_bracket_fails" field in XC.jsonl is a trivially empty interval and carries no information.)

## GREEN calibration (failure mode 7)

At 7/4: ||G_a||_{FF -> X} <= 5.395 (d part 3.900, v part V_ext/s_u = 5.395, i.e. sup |v| <= 16.2 per unit FF norm);
float P5: sigma part 3.7, u part 15.2. Agreement within a factor 1.06. alpha = [U2, V1hat] = 412.44, c = [Z1, Z2] =
1.0170, beta = -2.4212 (all certified nonzero). tau checks: tau'(0) = 1 exactly up to 2.9e-11; tau_W(R1) = 42.889
gives v_tau(R1) = -2.333 against the finite-difference dE/dsigma0 + (dm/dsigma0)/R1 = -2.37 (P3a); tau_v(0) = 3.4241
= du0/dsigma0 (P5: 3.424). The a-parts of tau from U1 + beta U2 and from lam1 Z1 + lam2 Z2 overlap at r_x
(0.7330926461 +/- 3.5e-11).

## Full cell as a pipeline test (LOO-161 with all 11 certificates; a control cell, not a window result)

| certificate | end a 1597/1000 (certified m) | end b 33/20 | CC test |
|---|---|---|---|
| CPOS H(w2) L0 (w2 1.01530 / 1.05785) | 5.03e-5 | 5.25e-3 | FAIL: C0 = 9.05e-5 > m_a |
| RITZ H(w1) L0 (w1 0.9414 / 0.9516) | 0.0202 | 0.0271 | pass |
| CPOS H(w2) L1 | 0.0550 | 0.0562 | pass |
| RITZ L1 | 0.0262 | 0.0263 | pass |
| CPOS H(w2) L2 | 0.0482 | 0.0434 | pass |
| RITZ L2 (w1 = 0) | 0.0846 | 0.0970 | pass |
| CPOS H(0) L0 (k = 4) | 0.2876 | 0.2978 | pass |
| CPOS H(0) L1 (k = 3) | 0.1816 | 0.1859 | pass |
| CPOS H(0) L2 (k = 2) | 0.3779 | 0.3880 | pass |
| count H(0) L3 (k = 0) | 0.1742 | 0.1821 | pass |
| PEN (M' = 5) | 0.2291 | 0.2435 | pass |

CH constants on this cell (Delta = 0.053): L = 0: C0 = 9.05e-5, C1 = 0.0336, C0' = 9.05e-5, C1' = 0.0467; Gam: G0 = 2.1e-8,
G1 = 0.0347. Every certificate is certified at both ends; the single CC failure is the expected one: the end-node
margin at 1597/1000 (float 7.2e-5, certified 0.7 x) against C0 = rho_max (6 sigma/om + s_u) + nonlocal rho term on
this wide cell. For the schedule's first cell (Delta = 0.003) Y0 scales like Delta^4 (projection, not measured).
Unit cost: 221 s per cell (cross-grid 7.6 s, BR' + CH 9 s, certificates and pre-pass about 200 s).

## Unit costs and projection
See RUN.md: about 2.2 min per node and 3.7 min per cell; full run about 2.2 lane-hours, 1.1 h of wall on two lanes
(1.5 h with bisection contingency).

## Earlier dev findings (fixed before the final control runs; PATCHES.md)
python-flint `x ** n` on positive intervals can contain 0 (gave nan in 1/r Taylor models); crude [0, r0] bounds
inflated Y0 by 500x; the w = 0 kernel was taken for a Krein drop by the first pre-pass; un-re-based columns left the
L = 0 endpoint inertia undecided near w+ at R = 20.

## Addendum: XU at 1985/1000 (L = 2) - NOT COMPLETED (open control)
Started 06:55 under the 30-min cap (timeout 1790 s); stopped by the cap at 07:25 (memcap exit 143) before it wrote
its output. The L = 2 grid up to w_max (about abs(E) - m/20, larger than at 1595) has about 260 points at about 7 s per
count pair, i.e. about 30 min: one job cannot finish under the rule. It was NOT retried. To close it the scan must
be split into two jobs over j-ranges of the same 0.01 grid (a small change to node.xu plus a merge in verdict_w),
which changes node.py's hash and therefore, by RUN.md, requires rerunning XK and XU(1595) (about 35 min). This is
left to the lead's decision. verdict_w.py controls currently prints all_pass false for exactly this reason.

## FINAL BATCH under the final hashes (2026-11-19, after audit-W; supersedes the tables above where they differ)

Hashes: RUN.md. Superseded outputs: out/controls/superseded/ (pre-split node.py) and superseded2/ (pre-audit).
Numbers did not change (audit predicted < 1e-11): LOO-161 BR Z1 = 0.627 / 0.617, rho = 2.21e-6 / 2.11e-6, X-distance
5.89e-8; LOO-1595 X-distance 1.92e-9 <= rho 1.18e-6, Z1 = 0.559 / 0.553; loo-185w Z1 = 1.168 / 1.143 (not a gate).

| control | final result |
|---|---|
| XK, nine G9 nodes | PASS 9/9 (27/27 sectors; tube shas equal R2) |
| XU 1595/1000 (L = 0) | PASS: 171 points, 0 drop pairs, 0 undecided, L1 and L2 drops certified |
| XU 1985/1000 (L = 2) | **FAIL (not decided), strict rule**: 258 of 259 grid points scanned in 8 j-range parts (each 95-480 s), 0 drop pairs, L0 and L1 drops certified (lower N(1.1341) = 4 > upper N(1.3429) = 3; lower N(0.3740) = 3 > upper N(0.8564) = 2); BUT (a) at w = 2.27 (j = 227) the upper count is undecided (lower = 4; neighbours 4/4) and (b) the last point j = 259, w = 2.59, 5.5e-4 below w_max = 2.590546, does not finish: one single-point job ran 900 s and was stopped (j = 257, 258: about 100 s each). |
| LOO-161, LOO-1595 | PASS |
| XI | PASS (REJECTED) |
| XC | PASS 5/5, exactly the sealed points |
| R1REG | PASS |
| guard_test | PASS (N:n1500, C:c99 exit 2 with REFUSED) |

verdict_w.py controls: all_pass false (only XU:hi-u false; xu_detail: n = 258, jmax = 259, undecided 1, tiling_ok false).
Reading: no drop pair exists anywhere on the scanned grid at 1985/1000, so nothing contradicts "no drop in L = 2";
the failure is two non-decided counts close to the continuum edge (counts there climb 4 -> 6). Options for the lead
(none taken): (i) a scan-top margin, e.g. w < w_max - 1e-3 (excludes j = 259), plus a rule for an undecided count
(e.g. re-count at the same w with level 1e-6, or treat an undecided point as excluded when its two neighbours are
decided and equal); (ii) keep the strict rule and accept XU:hi-u as INCONCLUSIVE (then BAR-W1 is VOID by its own
rule until it is resolved). Both are changes made after seeing data and must be disclosed as such.

## XU-1985 resolution (lead decision, rule SET AFTER SEEING THE DATA, pre-seal)
- Re-count at w = 2.27 (recount.py, same tube sha 67dbe4533c9b...): level 1e-5 upper undecided (endpoint inertia),
  1e-6 undecided, **1e-7: upper 4 = lower 4** (decided). 72 s.
- Scan top: w < w_max - 1e-3 = 2.589546; j = 259 (w = 2.59) excluded. Evidence that the target never counts there:
  cells use w2 inside the certified gaps, max w+ over the nine G9 nodes and L = 0, 1, 2 is 1.4641 (1983/1000, L = 0),
  while |E| >= 1.9 along every branch (certified BR' bound, 1.9058 on LOO-161; node |E| from 2.553 at 1597/1000 to
  3.663 at 1983/1000). The smallest gap |E| - w2 the cells rely on is above 0.4, so delta = 1e-3.
- Result: XU:hi-u PASS (258 points, 0 undecided after the re-count, 0 drop pairs, L0 and L1 drops certified).
- `verdict_w.py controls`: **all_pass true**.
