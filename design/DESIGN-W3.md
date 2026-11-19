# DESIGN-W3: spectral stability for EVERY sigma0 in [1597/1000, 1983/1000] - referee-W2 fixes applied, build choices fixed

Seat build-W, raid R3-WINDOW, 2026-11-19. Supersedes DESIGN-W2.md (kept unchanged; every section of W2 not named
below stands as written). Applies the four BLOCKING fixes and the five non-blocking fixes of
seats/referee-W2/REFEREE-DESIGN-W2.md, and fixes the build-level choices of the instruments in
window/build-W/ (hw3.py, green.py, cell.py, node.py, assemble_w.py, verdict_w.py). Labels as in W2: PROVED (written
here, not yet refereed in this form), CERTIFIED, PROBE-MEASURED / FLOAT, ESTIMATE. TARGETS-R1*.md were not read.

thesis: plank 2 (certified computation with explicit constants: a nine-point certificate becomes an interval certificate) - certified grid nodes plus perturbation arguments that use only counts, margins on common explicit subspaces and linear solves
target: W
reuses: PROOF-R1-v2 chain (B-EX, B-TAIL, brackets, D0, ESS, IDX, L>=3 monotonicity), build-3 instruments bg_tube.py / itaylor.py / lincore.py / bracket.py (byte-identical copies in build-W), DESIGN-W2 lemmas KC, IDXC, CC, CH, CPOSL, SHIFT, the nine R2 certified points with their Krawczyk Krein pairs (controls), graphical Krein signature (Kollar-Miller arXiv 1209.3185; Kollar-Bosak arXiv 1212.5691 Thm 4), grid-plus-perturbation (Hoang-Plum-Wieners ZAMP 60)
produces: BR with one fixed ball per half-cell, a uniqueness radius and a certified tube X-diameter; the GREEN kernel in the dichotomy basis {U2, V1, Z1, Z2} with the exterior lemma EXT; the exact residual quotient Q_theta evaluated on Taylor models; closed-form CH constants C0 + C1 theta(1 - theta); controls XK (kernel booked at w = 0), XU, XC, leave-one-out (LOO) and the injected-tau rejection (XI)

## 0. In plain words

DESIGN-W2 proved the window in three moves: counting instead of eigenvectors, convexity instead of interval
parameters, and a Newton-Kantorovich branch between certified nodes. The second referee found the moves sound and
asked for four repairs before the seal: one fixed ball for the branch with a real uniqueness statement, a control
that can actually catch bad node data (the old "wrong pairing" null could not), a control that checks the chord
inequality directly, and the kernel booked at w = 0 in the counter check. This file makes those repairs and writes
down exactly how the built instruments certify each constant, including the pieces W2 left to the build (the Green
kernel without cancellation, the exterior at infinity, and the residual without loss).

## 1. What changed from W2

| item | W2 | W3 |
|---|---|---|
| BR ball | rho(t) = 2 Y0(t)/(1 - Z1max), radius 0 at the nodes; uniqueness "in the tube" (vacuous: referee-W2 BR fix 1) | one FIXED ball rho_max per half-cell for all theta (uniform contraction, continuity); uniqueness in the X-ball of radius r_u with kappa(r_u) := Z1max + r_u Z2hat(r_u) < 1; certified tube X-diameter (incl. [0, r0] and [R1, inf)) < r_u (3.6, items 1, 4) |
| BR halves | node a over the whole cell | theta in [0, 1/2] linearised at a, [1/2, 1] at b (a <-> b, Delta -> -Delta symmetry of the Hermite predictor); the two fixed-point sets coincide at theta = 1/2 (3.6, item 1) |
| XU(c) | wrong-pairing BR null (WRONG: referee-W2) | removed. Replaced by LOO (mandatory, two cells, sealed gate) and XI (injected tau_b + 1e-3 bump must be REJECTED) (failure mode 3) |
| count radius | 14 (20 at end cells) | 20 everywhere: at R = 14 the Neumann cut moves the L = 0 crossing at w+ (7/4: 1.2043 -> about 1.199; build-W CALIBRATION) |
| XC | absent | float bracket control at 1.5985, 1.775, 1.98: lowest eigenvalue on the common subspace in [chord(m) - eta2, chord(m) + eta2'] (5.3) |
| XK at w = 0 | lower = upper = n(L+) + n(L-) (cannot pass: kernel) | kernel booked: (upper, lower) = (4, 3), (3, 2), (2, 2) for L = 0, 1, 2 (5.1) |
| tau | "built by GREEN" | built ONLY from certified marches (tau = lam1 Z1 + lam2 Z2 with lam from U1 + beta U2 at r_x; a-parts asserted to overlap); every consumer re-steps tau with the ODE and checks overlap with the next certified grid value (green.py, cell.half_tms) |
| Y0 | sum of ||G_a Q_k||_X | kernel sums of the exact quotient Q_theta (sympy division, remainder 0; reproduces referee-W2 w2_factor) on Taylor models over every step: no cancellation is ever done on boxes (3.6) |
| G_a | "kernel U(r) C V(t)^T in the dichotomy basis" | explicit formula with {U2, V1hat, Z1, Z2}, every term a product of two functions each marched in its stable direction (3.6b) |
| exterior | "max principle + Coulomb kernel" | lemma EXT (V1 at R1), max principle with constant 1/(kappa1^2 - 1/8) and the om'^2 term written out, Gauss law for v (3.6b) |
| E text | abs(E) >= 2.5 | abs(E(sigma0)) >= -u(sigma0)(R1) >= -(max_theta H_theta,2(R1) + rho s_u), about 1.9 at the low end (referee-W2 BR fix 3); E < 0 from u(sigma0)(r_n) < 0 |
| 8.4 | int r^2 tau^2 = 8.4 | 10.7 (referee-W2 w2_mid.log): norm(g_b - g_a)^2 about 10.7 Delta^2; M' Gam(1/2) about 8.3e-3 at Delta = 0.025 |
| B_m in CPOSL (d) | "B_m" (3-channel name) | B_m^P: the 2-channel L+(0) form (a, W) at level m (hw3.pen, chan 'P') |
| cost | 31 min cells | re-projected from measured unit costs: CALIBRATION.md / RUN.md |

## 2. Setting

As DESIGN-W2 section 2. Additionally: x := theta (1 - theta); E_mu(r) := exp(-mu (r - R1)), mu := min(kappa1_a,
kappa1_b)/2 (asserted mu >= 1/2); Wronskian [f, g] := f.g' - f'.g on data (a, W, a', W') of the reduced system
-Y'' + Q Y = F, Q = [[3 sigma^2 - u, sqrt2 sigma], [sqrt2 sigma, 0]], F = (r f1, -r f2/sqrt2) (DESIGN-W2 3.6).

## 3. The uniform argument (changes only)

### 3.6 Lemma BR (fixed ball, uniqueness radius). PROVED given the certified inputs; to referee

Half-cell H1: theta in [0, 1/2], node a, T_theta(z) := -G_a(R_theta + B_theta z + N_theta(z)) (W2 3.6). Half-cell H2:
the same with (a, b, Delta) -> (b, a, -Delta) and theta -> 1 - theta (h00(theta) = h01(1 - theta),
h10(theta) = -h11(1 - theta), so H_theta is the same function).

Certified constants per half:
- Y0max >= sup_theta ||G_a R_theta||_X, from the kernel sums of the profile (1/16) sum_k |Q_{c,k}(r)| 2^-k, c = 1, 2
  (R_theta = theta^2 (1 - theta)^2 sum_k Q_{c,k} theta^k; theta^2 (1 - theta)^2 <= 1/16 and theta^k <= 2^-k on [0, 1/2]).
- Z1max >= sup_theta ||G_a B_theta||_{X -> X}, profiles P1 = |6 sigma_a D1 + 3 D1^2 - D2|/om + s_u |D1|,
  P2 = 2 |D1|/om, sup over 8 sub-intervals of theta.
- Z2hat(r) such that ||G_a (N_theta(z) - N_theta(z'))||_X <= r Z2hat(r) ||z - z'||_X on the ball of radius r:
  N(z) - N(z') = (3 (sigma_a + D1)(z1 + z1') + (z1^2 + z1 z1' + z1'^2) - z2) (z1 - z1') - z1' (z2 - z2'),
  -(z1 + z1')(z1 - z1'), with |z1| <= r/om, |z2| <= s_u r: profiles P1 = 6 |sigma_a + D1|/om^2 + 3 r/om^3 + 2 s_u/om,
  P2 = 2/om^2 (this corrects the W2 profile list; referee-W2 noted W2's is conservative by 2 in the self-map).

**Theorem BR'.** Let rho_max := 2 Y0max/(1 - Z1max) and r_u >= rho_max with
(i) Y0max + Z1max rho_max + Z2hat(r_u) rho_max^2 <= rho_max, (ii) kappa(r_u) := Z1max + r_u Z2hat(r_u) < 1. Then:
1. For every theta in the half, T_theta maps the closed ball B(0, rho_max) into itself and is a contraction on
   B(0, r_u) (Lipschitz constant <= kappa(r_u), uniform in theta). Its fixed point z_theta is the unique solution of
   F(H_theta + z) = 0 with z in X, z1(0) = 0 and ||z||_X <= r_u. theta -> z_theta is continuous (uniform contraction
   on one fixed ball; T_theta is continuous in theta).
2. The two halves agree at theta = 1/2: the fixed points of T^a_{1/2} and T^b_{1/2} both solve F(H_{1/2} + z) = 0
   with z in X, z1(0) = 0 (the right inverse of L_a into X is unique: alpha != 0, section 3.6b). They are equal
   PROVIDED rho_max^a <= r_u^b and rho_max^b <= r_u^a (each fixed point then lies in the other half's uniqueness
   ball, where that contraction has exactly one such solution). This condition is CHECKED per cell (amendment A1.2).
3. Uniqueness in the node tube (fixes W2 item 4): if diam_X(tube_a) < r_u, every decaying solution with
   sigma(0) = sigma_a and u0 in the tube interval differs from Sigma_a by a fixed point of T_0 in B(0, r_u), hence is
   Sigma_a. diam_X(tube) is certified (cell.tube_diameter): grid values and the within-step spread of the K = 56
   Taylor coefficients of the tube (radius of the ball coefficients plus 2 |remainder| h^57), the [0, r0] series
   spread, and the exterior (|sigma| <= a1/r E, u = E + m/r +- a1^2/(4 kappa1^2 R1^2)).
4. Items 2, 3, 6, 7 of W2 3.6 hold with rho(t) replaced by rho_max. E(sigma0) < 0 and one node: u(sigma0)(r_n) <=
   H_theta,2(r_n) + rho_max s_u < 0 and |sigma(sigma0)(r_n)| >= |H_theta,1(r_n)| - rho_max/om(r_n) > 0 at r_n = r_x
   (about 8; u is decreasing for every solution, so u < 0 on [r_n, inf) and the convexity argument applies beyond
   r_n). |E(sigma0)| >= -u(sigma0)(R1) >= -(max over theta of H_theta,2(R1) + rho_max s_u) (referee-W2 fix 3).
5. The certified run stores rho_max, r_u, kappa(r_u), Y0max, Z1max, Z2hat for both halves.

Why rho need not vanish at the nodes: CH (3.5) now uses eta2(theta) <= C0 + C1 theta (1 - theta) with C0 = O(rho_max),
and the CC test m_a (1 - theta) + m_b theta - C0 - C1 theta (1 - theta) > 0 is decided exactly. With rho_max of order
1e-6 or less, C0 is two orders below the smallest end margin (7.8e-5 float at 1597/1000).

### 3.6b GREEN: the kernel of G_a, the nondegeneracy and the exterior. PROVED; to referee

Solutions: U1, U2 regular with (a', W')(0) = (1, 0), (0, 1), enclosed at r0 by an odd power series of order 29 in r
with the background series of bg_tube (same recursion) and a Volterra remainder (green.lin_series_start); marched
outward. V1: a decays, W -> 0 (lemma EXT); marched inward; normalised V1hat := V1/V1_a(r_x). rho := V1^perp (the
solutions whose a-part does not grow): V1 annihilates rho because [V1, y] -> 0 at infinity for every y in rho
(a_1 decays exponentially, W_1, W_1' -> 0, a_y bounded, W_y at most linear), and dim rho = 3.
Z1, Z2: the solutions with data at r_x (W, W') = (1, 0), (0, 1) and (a, a') solving [Z, V1hat] = 0, [Z, U2] = 0;
they span rho cap U2^perp. tau := U1 + beta U2, beta := -[U1, V1hat]/[U2, V1hat]; tau lies in rho cap U2^perp, so
tau = lam1 Z1 + lam2 Z2 with lam = (tau_W, tau_W')(r_x) (assertion: the a-parts overlap).

**Lemma G.** If alpha := [U2, V1hat] != 0 and c := [Z1, Z2] != 0, then for f in FF the unique solution y of
L_a y = f in X with y1(0) = 0 is y = int G(r, s) F(s) ds with
    s > r:  G(r, s) = -U2(r) V1hat(s)^T / alpha,
    s < r:  G(r, s) = -V1hat(r) U2(s)^T / alpha + (Z1(r) Z2(s)^T - Z2(r) Z1(s)^T) / c.
Proof. (i) Variation of parameters for -Y'' + Q Y = F with a basis b_k and S_jk = [b_j, b_k]: c' = -S^-1 B^T F.
(ii) With the Lagrangian pair Ut = (U2, tau) (regular) and Vt = (V1, V*) (a decays, W bounded; V* chosen in
span(V1, V2) with [U2, V*] = 0), W := [Ut_i, Vt_j] = diag(alpha, c') ([tau, V1] = 0, [U2, V*] = 0), and the
self-adjoint Green function is G^sa(r < s) = -Ut(r) W^-T Vt(s)^T, G^sa(r > s) = -Vt(r) W^-1 Ut(s)^T.
(iii) d(0) of G^sa F is -(1/c') int V*.F (U2_a'(0) = 0, tau_a'(0) = 1), so G_a F = G^sa F + tau (1/c') int V*.F;
for s > r the tau-terms cancel, for s < r one gets (tau(r) V*(s)^T - V*(r) tau(s)^T)/c'.
(iv) This antisymmetric expression is invariant under any change of basis of span(tau, V*) = rho cap U2^perp
(numerator and c scale by the same determinant), so (tau, V*) -> (Z1, Z2). (v) Uniqueness in X: a homogeneous
solution in X is regular with a'(0) = 0 and in rho, i.e. lambda U2 in V1^perp; alpha != 0 forces lambda = 0. []
Every product pairs a function at the smaller argument that does not grow inward (U2; Z1, Z2 are bounded inward
because the d(0)-response is bounded) with one at the larger argument that does not grow outward (V1hat; rho
elements), so the box enclosures need no cancellation. alpha != 0 replaces W2's pair (D_a != 0, d_E(0) != 0):
it is exactly "no regular solution with d(0) = 0 in rho", which is what BR and the parametrisation by sigma0 use.

**Lemma EXT (V1 at R1).** E(s) := exp(-kappa1 (s - R1)), S := sqrt2 a1/R1 (sqrt2 |sigma(s)| <= S E(s)),
kappa1^2 <= V := 3 sigma^2 - u <= Vmax := 3 (a1/R1)^2 + abs(E) on [R1, inf) (u decreasing to E).
(a) The decaying solution phi of a'' = V a (phi(R1) = 1) has rho = -phi'/phi in [kappa1, sqrt(Vmax)] on [R1, inf)
(Riccati rho' = rho^2 - V: above sqrt(Vmax) it blows up, below kappa1 it turns negative; both contradict decay).
(b) The Dirichlet-decaying Green function of -d^2 + V satisfies 0 <= G_D(r, s) <= exp(-kappa1 |r - s|)/(2 kappa1)
and d_r G_D(R1, s) = phi(s) <= E(s).
(c) V1 = (phi + alpha_, w) with alpha_ = -int G_D sqrt2 sigma w, w(r) = +int_r^inf (s - r) sqrt2 sigma a ds is a
contraction fixed point; |a| <= (1 + c_al) E, |W| <= c_w E^2, q := 3 S^2/(32 kappa1^4), c_al = q/(1 - q),
c_w = S (1 + c_al)/(4 kappa1^2); a'(R1) in [-sqrt(Vmax) - S c_w/(4 kappa1), -kappa1 + S c_w/(4 kappa1)],
|W(R1)| <= c_w, |W'(R1)| <= S (1 + c_al)/(2 kappa1).
The a'(R1) interval is wide (about 10 percent); it is carried as a scalar parameter delta (two point columns colA,
colB marched inward) and every V1-dependent quantity is a Moebius function of delta, enclosed by the hull of its
two end-point values. Because the delta-uncertainty lies along a direction that decays inward relative to V1
(factor exp(-2 kappa1 (R1 - r_x)), about 1e-27), V1hat(r_x) is tight (width about 1e-12, set by the W-box).

**Exterior outputs (r >= R1).** d: -Lap d + V d = f1 + sigma v with V >= kappa1^2. For psi = 1/om,
-Lap psi / psi = (4 - om)/(8 om^2) >= -1/128 >= -1/8 (the om'^2 term included: psi'' = -om''/om^2 + 2 om'^2/om^3);
the maximum principle (d, psi -> 0 at infinity) gives sup_{r>=R1} om |d| <= max(om(R1) |d(R1)|,
sup om |f1 + sigma v| / (kappa1^2 - 1/8)) (referee-W2 fix 4: constant 1/(kappa1^2 - 1/8)). v: Gauss law
r^2 v' = -int_0^r s^2 (f2 + 2 sigma d), so sup_{r>=R1} |v| <= |v(R1)| + R1 |v'(R1)| + int_R1^inf s |f2 + 2 sigma d|.
The two inequalities are solved jointly (the coupling 2 a1/(kappa1 om(R1)) is about 1e-12).
[0, r0]: y/r via U2(r)/r (series) for s > r; s < r crude with int_0^r s P <= r0^2 P/2.

### 3.5 CH constants (closed form). PROVED given BR'

With p_sig(r) := max(|ds - Delta tau_a1|, |ds - Delta tau_b1|), p_u likewise (H_theta - chord = theta (1 - theta) g,
g affine in theta, so |g| <= max of its end values), e_sig <= x p_sig + rho_max/om, e_u <= x p_u + rho_max s_u:
eta2(theta) <= C0 + C1 x with C1 = sup_r [3 ds^2 + 6 |sigma_lin| p_sig + p_u] + (4 Imax + 2 (Np/4 + rho sqrt8)) Np/(2L+1),
C0 = rho sup_r [6 |sigma_lin|/om + s_u] + (4 Imax + 2 (Np/4 + rho sqrt8)) rho sqrt8/(2L+1), Np = (int r p_sig^2)^(1/2),
int r/om^2 = 8; eta2' likewise with + 3 e_sig^2 and + 2 x int r ds^2/(2L+1); Gam(theta) <= G0 + G1 x with
N2p = (int r^2 p_sig^2)^(1/2), int r^2/om^2 = 16 pi. Exterior pieces: exp-small bounds for sigma, ds, tau_1 and the
c0 + c1/r form for u_b - u_a - Delta tau_2 (no loss of the cancellation at infinity).

### 3.7 Assembly (additions)

Each cell end carries 11 certificates: CPOS H(w2) (L = 0, 1, 2), RITZ H(w1) (L = 0, 1, 2), CPOS H(0) with
k = U+ + U- block vectors (4, 3, 2 for L = 0, 1, 2; gives L+-(L) > 0 on codimension U+-, hence N0 finite and, with the
exact kernels (K1), (K2) of sigma0, n(L-(0)), n(L+(1)) <= 1), count H(0) at L = 3 (k = 0), PEN (L = 0). The explicit
vectors are common to both ends. The CC test for each is the exact quadratic test in theta. RITZ uses
H(w)[x] = min over W of B[(x, W)]: the trial W is extended beyond Rc by W(Rc)(Rc/r)^L (cost (L/Rc) W(Rc)^2).

## Nodes

| id | claim | source | status | expected | depends | referee | lean |
|---|---|---|---|---|---|---|---|
| R1 | pointwise chain at any exact rational sigma0: B-EX, B-TAIL, brackets, D0, ESS, IDX, L >= 3 monotonicity, 3-D statement | proof/PROOF-R1-v2.md sections 3-7 | PROVED | - | - | referee-5 CORRECT; referee-7 transfer CORRECT WITH FIXES (text) | no |
| G9 | nine certified stable points with K = (2,2,2,0), Krein pairs (w-, w+) per L, tube sha per point | build-3/out/*/B.json, K0-K2.json | CERTIFIED | 9 | R1 | referee-7 CORRECT | no |
| KC | local Krein index identity, essential-spectrum proof | design/DESIGN-W2.md section 3.2 | PROVED | - | R1 | referee-W1 CORRECT WITH FIXES; referee-W2 step 5 CORRECT | no |
| IDXC | N_+ + 2 (N(w1) - N(w2)) <= K(L) | design/DESIGN-W2.md section 3.3 | PROVED | - | KC, R1 | referee-W1 CORRECT | no |
| CC | convexity cover on a common subspace | design/DESIGN-W2.md section 3.5 | PROVED | - | - | referee-W1 CORRECT | candidate |
| CH | chord inequalities, eta2 and eta2' | design/DESIGN-W2.md section 3.5; closed-form constants section 3.5 here | PROVED | - | BR | referee-W2 CORRECT | candidate |
| CPOSL | endpoint margin lemma (count, Haynsworth k vectors, exterior, penalised L = 0) | design/DESIGN-W2.md section 3.5 (B_m^P naming fixed here) | PROVED (to referee) | - | R1 | referee-W2 CORRECT WITH FIXES (text, applied) | no |
| BR | branch lemma with one fixed ball per half-cell, uniqueness radius r_u, tube X-diameter < r_u | section 3.6 | PROVED (to referee) | - | R1, G | referee-W2 CORRECT WITH FIXES (fixes applied here; re-read needed) | no |
| G | Green kernel of G_a in the basis {U2, V1hat, Z1, Z2}; nondegeneracy alpha != 0, c != 0; EXT; exterior max principle 1/(kappa1^2 - 1/8) | section 3.6b | PROVED (to referee) | - | R1 | NEW: referee | no |
| HW3 | instrument: 3-channel counts with per-step re-basing, W-level 0 asserted; CPOS with k forcing columns; RITZ Gram (exact polynomial parts + Taylor quadrature); PEN | window/build-W/hw3.py | CHECK (built; calibrated in CALIBRATION.md) | - | CPOSL | NEW: audit | no |
| GREEN | instrument: series start, EXT, delta-hull, Z basis, tau from marches only, kernel sums with exterior, apply(profile) | window/build-W/green.py | CHECK (built; calibrated in CALIBRATION.md) | [3, 25] | G | NEW: audit | no |
| CELL | instrument: cross-grid re-steps with tau overlap checks, Taylor-model residual quotient, BR', CH, CC tests | window/build-W/cell.py | CHECK (built; LOO and XI run pre-seal) | - | BR, CH, CC, HW3, GREEN | NEW: audit | no |
| XK | control: at the nine G9 nodes drop by exactly 1 across each certified w-, rise by exactly 1 across each w+, kernel booked at w = 0 | window/build-W/node.py against build-3/out/*/K*.json | CHECK (run pre-seal: CALIBRATION.md) | 1 | HW3, G9 | - | no |
| XU | control: nodes 1595/1000 (L = 0) and 1985/1000 (L = 2) show no drop in the named sector on the pair scan; the other sectors drop | window/build-W/node.py | CHECK (run pre-seal: CALIBRATION.md) | 0 | HW3, G9 | - | no |
| LOO | control: on [1597/1000, 33/20] (tube of 161/100, R2-certified, theta = 13/53) and [31/20, 1597/1000] (tube of 1595/1000, theta = 45/47) the certified interior tube lies in the BR ball of its half (X-distance <= rho_max); the referee's [7/4, 37/20] (width 0.1) does not close BR (Z1 = 1.17) and is reported only | window/build-W/cell.py | CHECK (run pre-seal: CALIBRATION.md) | 1 | CELL, G9 | - | no |
| XI | control: tau_b + 1e-3 bump injected into node b's tau data is REJECTED by the overlap check | window/build-W/cell.py | CHECK (run pre-seal: CALIBRATION.md) | 1 | CELL | - | no |
| XC | control (float): lowest eigenvalue on the common subspace at 1.5985, 1.775, 1.98 lies in [chord(m) - eta2, chord(m) + eta2'] | window/build-W/xc.py | CHECK (run pre-seal: CALIBRATION.md) | 1 | CH | - | no |
| NODES | point tubes at all 23 nodes (bg_tube unchanged) plus GREEN per node | window/build-W/node.py; run after seal | GAP (run after seal) | 23 | R1, GREEN | - | no |
| CELLS | every cell: BR', CH, the 11 CC tests per end, w-checks, one node, E < 0 | window/build-W/cell.py; run after seal | GAP (run after seal) | 22 | CELL, NODES, XK, XU, LOO, XI, XC | - | no |
| W | spectral stability for every sigma0 in [1597/1000, 1983/1000] along the BR branch (unique in the stated ball) | section 3.7 of DESIGN-W2 with the changes here | GAP (target; closes when CELLS hold on every cell) | - | R1, G9, IDXC, BR, CELLS | NEW: referee | no |

## Failure modes

1. **Counter miscounts.** XK at the nine nodes; one mismatch voids HW3. At w = 0 the kernel is booked:
   (upper, lower) must be (4, 3), (3, 2), (2, 2).
2. **Certificate vacuous (no drop where none exists).** XU: at 1595/1000 (L = 0) and 1985/1000 (L = 2) no frequency pair
   on the scan grid gives lower(w1) - upper(w2) >= 1 in the named sector; the other sectors must show their drop.
   A cell with an unstable end must come out INCONCLUSIVE with the failing step "no drop" in that sector.
3. **Bad node data accepted (the residual factorisation is identity-blind).** XI must REJECT; LOO must place the
   certified interior tube inside the BR ball at theta = 1/2 on both LOO cells. Either failure voids CELL.
4. **CH sign or size wrong.** XC (float) at three interior points; failure voids the CH constants.
5. **Margins vanish near the edges.** All cells use R = 20 and the explicit vectors of the end node with the smaller margin; if a cell fails
   it is bisected (depth <= 4); the fallback theorem is the largest closed union of HOLDS cells.
6. **A level leaks into the W channel.** Asserted in hw3._system (no 'one' term in Vw).
7. **Exterior or [0, r0] pieces unbounded or wrong.** Asserted: mu >= 1/2, kappa1^2 > 1/8, EXT q < 1/2, series
   remainder denominator > 1/2; GREEN's ||G_a|| must agree with the float P5 value (3.7 / 15.2 in W2 units) within a
   factor 2 (calibration).
8. **Run pathologies.** Every job carries a watchdog; an unfinished certificate is INCONCLUSIVE, never retried
   silently.

## 6. Schedule

Nodes and cells as DESIGN-W2 section 6 (23 nodes, 22 cells). Cost: measured per-node and per-cell times and the
projection are in window/build-W/CALIBRATION.md and RUN.md (SPEEDUP-W1's 31 min for cells was re-projected there).

## 8. Open items for the referee of W3

1. Lemma G step (iv)-(v) and the claim that Z1, Z2 do not grow inward (used only for efficiency: a violation shows
   up as a large rigorous bound, never as a wrong one).
2. Lemma EXT (a)-(c) constants.
3. BR' item 2 (agreement of the halves) and item 3 (tube diameter as the uniqueness gate).
4. The Z2hat profile (corrected here).


## Amendment W3-A1 (audit-W, 2026-11-19; seats/audit-W/AUDIT-W.md, verdict FIX FIRST, all patches applied)

1. **EXT sign (text).** In Lemma EXT (c), W'' = sqrt2 sigma a gives w(r) = +int_r^inf (s - r) sqrt2 sigma a ds (corrected
   in place above). Only absolute values enter the constants; no number changes.
2. **BR' item 2 condition.** The halves agree only if rho_max^a <= r_u^b and rho_max^b <= r_u^a (corrected in place
   above). cell.run_cell now checks it; a violation is the failing step 'BR' ('halves disagree').
3. **XI scope.** The overlap check proves that the tau data used are a solution of the ODE L_b y = 0 on every step
   used; it does not prove that they are tau (tau + eps Z1 would pass). The identity of tau rests on provenance:
   every cell job recomputes GREEN in-process from the sha-checked node tube blob, so no tau data ever enters from
   outside the job. XI tests that non-solution data are refused.
4. **Remark (audit).** c = [Z1, Z2] != 0 follows from alpha != 0, because rho cap U2^perp = span(U2, V1)^perp is
   symplectic; c is still certified separately.
5. **Bisection.** Not implemented. A cell that does not close stays INCONCLUSIVE (failing step recorded) and the
   fallback applies: the window verdict reports the largest closed union of consecutive HOLDS cells.
6. **Build fixes (no change to the lemmas):** green G-1 (the truncated sigma^2 tail in dQ), cell C-1 (linear term of
   the W correction in the exterior tau bound), C-2 (outward rounding on the decision path), C-3 (the [0, r0] sup and
   integrals of the CH constants from the exact-series Taylor models), C-4 (item 2 above), C-5 (one-node check needs
   sigma_a sigma_b > 0 at r_n), C-6 (missing float w2 recorded as INCONCLUSIVE 'CPOS'), Gram reach assertion at the
   cell.End call site; node N-1 (a node is ok only if its R = 14 brackets give K = (2,2,2,0) with consistent
   counts); verdict_w FAILED-by-brackets and exactly the 5 sealed XC points; assemble_w asserts WSU unset for N:/C:.
