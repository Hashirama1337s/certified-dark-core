# DESIGN-W1: spectral stability of the one-node repulsive GPP state for EVERY sigma0 in [1597/1000, 1983/1000]

Seat design-W1, raid R3-WINDOW, 2026-11-19. Design only: no certified target run was made. Every claim below is
labelled PROVED (full argument written here, not yet refereed), SKETCH (argument outlined, a proof seat must write it),
PROBE-MEASURED (a number from core/window/design/PROBES.md; float probes are not certificates), or ESTIMATE.
TARGETS-R1*.md were not read. Inputs read: window/SCOPE.md, proof/PROOF-R1-v2.md, build-3/*.py + PATCHES.md + RUN.md +
CALIBRATION.md, build-3/out/<tag>/*.json, band/map/MAP.md, seats/referee-7, window/gate/PRIOR-ART-W1.md.

thesis: plank 2 (certified computation with explicit constants: a nine-point certificate becomes an interval certificate) - the window is covered by a grid of certified nodes plus perturbation arguments that use only counts
target: W
reuses: PROOF-R1-v2 chain (B-EX, B-TAIL, BR, D0, ESS, IDX, L>=3 monotonicity), build-3 instruments bg_tube.py / itaylor.py / lincore.py / bracket.py / tail.py unchanged, the nine R2 certified points and their Krawczyk Krein pairs (as controls), band/map float map (steering only)
produces: Krein-count lemma KC (a negative-Krein eigenvalue from two counts, no eigenvector), index inequality IDXC, convexity-cover lemma CC, branch lemma BR with a certified first variation, 3-channel matrix-Sturm counter hw3 for H(w) = [[L+, -w], [-w, L-]], constrained-positivity node CPOS, the interval certificate itself

## 0. In plain words

The published result proves the shelled dark-matter ball is stable at nine values of its central amplitude. This
design extends that to every value in between. Carrying the amplitude as an interval through the old computation
does not work (the enclosures blow up; the literature says the same: Barker-Zumbrun 1601.00837, Remark 1.2). The
route here is "certified grid points plus a perturbation argument" (the idea of Hoang-Plum-Wieners, ZAMP 60, 2009),
made possible by three observations:

1. A vibration with negative energy can be detected by counting. For a trial frequency w, count the negative
   directions of one fixed symmetric operator H(w). If the count drops when w is raised from w1 to w2, a
   negative-energy vibration sits between w1 and w2. No eigenvector has to be computed.
2. Counts are robust. They survive any change of the background that is small in operator norm, and, better, a
   count certified at both ends of a cell on a common test subspace holds everywhere inside the cell, because the
   operator depends on the cell coordinate almost linearly (convexity).
3. The family of backgrounds between two certified nodes can be enclosed by a Newton-Kantorovich argument that
   uses only linear computations at the nodes.

Probes at certified grid points show the counts close in seconds (prototype, PROBES P10) and that cells as wide
as the existing grid spacing 0.05 are spectrally fine in the middle of the window (float, PROBES P8).

## 1. Answers to the six design questions

**Q1. What carries stability across a box?**
- Route (a) is sound and needs nothing beyond pointwise facts. PROVED (by inspection of PROOF-R1-v2 Theorem 6.2):
  the IDX argument at a given sigma0 uses only (i) n(L restricted to Y_L) <= K(L) = 2 and (ii) ONE eigenvector xi
  with eigenvalue i w, w > 0, and <L xi, xi> < 0. It uses no positive-Krein eigenvalue, no simplicity, no
  continuity in sigma0, no separation from the Rydberg series or from the continuum edge. So "for every sigma0 in
  the box, (i) and (ii)" gives stability for every sigma0 in the box. Route (b) (signature continuity with a
  uniform gap including the Rydberg series) is not needed and is rejected.
- But a parametric Krawczyk for (ii) is NOT feasible: PROBES P3b gives cond(J) = 3.3e3 and a C-norm 1.4e3 for the
  Krawczyk Jacobian at 7/4, L = 0, so the interval hull of M(w; sigma0) over a box must have relative width below
  about 1e-4, while M varies intrinsically by about 10 x (box width) (ESTIMATE from d kappa / d sigma0 = 0.78 and
  the 18-unit inward march). That forces boxes of width 1e-5 or a Taylor-model integrator in sigma0. Rejected.
- Recommended: replace (ii) by the Krein-count lemma KC (section 3.2) and get the uniformity in sigma0 from
  lemmas SHIFT and CC (sections 3.4, 3.5). Then everything certified on a cell is a count.

**Q2. Background tube with interval sigma0?** No. The direct interval Taylor stepper inflates widths by wrapping:
in the R2 logs a start width 2e-50 in u0 is 7e-42 in sigma at r = 3.4, 1.5e-38 at r = 10 and 1.9e-31 at r = 21
(PROBE-MEASURED, build-3/logs/K0_lo-s.log, B_g175.log). A sigma0-ball of width h would need h < 1e-11 to keep 1e-2
accuracy at r = 10. Lighter tubes are not faster and lose the classify step (PROBES P6). The design never
integrates a sigma0-interval. The family between two nodes is enclosed by lemma BR (section 3.6).
Sensitivities (PROBE-MEASURED, P3a, P5): du0/dsigma0 = 3.42 to 3.47, dE/dsigma0 = -2.85, dm/dsigma0 = 12.4,
sup abs(d sigma / d sigma0) = 1.00, sup abs(dV+/dsigma0) = 7.1, sup abs(dV-/dsigma0) = 2.2.

**Q3. Brackets with interval sigma0.** Not needed as intervals. PROBES P2: at 7/4, R = 14, all upper counts
(L+: 2, 2, 1, 0; L-: 2, 1, 1, 0 for L = 0..3) are unchanged when the a-channel shift is raised by eta up to 0.2;
they break at 0.3. So the R1 counts tolerate any background change of operator norm below 0.2. P1 shows the level
must NOT be raised in the auxiliary W channel (a spurious W-mode appears near (pi / 2R)^2 = 0.0126 at R = 14): the
budget goes into the a-channel shift only. D0 has M abs(d2) >= 272 at every node (referee-7), far above 1. The
L >= 3 argument is uniform because L+-(3) >= eps + eta at the nodes (P2: 0 counts up to eta = 0.2).

**Q4. Parametric Krawczyk.** Rejected (Q1). The separation of the opposite-Krein partner still matters, but only
through one number: the height mu of the lowest positive eigenvalue of H(w2) with w2 between w- and w+. Float
values (P4, P8): mu = 0.026 (L = 0), 0.08 (L = 1), 0.046 (L = 2) at 7/4; mu is about 1e-4 at the two end nodes
(L = 0 at 1597/1000, L = 2 at 1983/1000), where the gaps are 0.0075 and 0.0187. The prototype counter still
resolves the drop at both end nodes at level 1e-5 (P10c).

**Q5. Cost.** Section 6: 23 nodes, 22 cells, about 2 lane-hours by the measured unit costs, 6 lane-hours with a
factor 3 for the unbuilt instruments and bisections. Every job is under 5 minutes.

**Q6. Shortcuts found.** (1) the count drop replaces the eigenpair; (2) convexity in the cell coordinate replaces
interval parameters; (3) L = 1 never comes near a collision: its margins are the largest (0.08 above, 0.04 below),
so L = 1 could take cells of width 0.1; (4) the end nodes of the window are already certified points, so no cell
has to approach an edge more closely than 1597/1000 and 1983/1000.

## 2. Setting and notation

All of PROOF-R1-v2 sections 2-7 is used as is. Per sector L: L+-(L), A = J L, Y_L, K(L), N_+ (total algebraic
multiplicity of eigenvalues with Re lambda > 0), [x, y] = <J^-1 x, y>, omega(x, y) = <L x, y>, Omega, Riesz
projections P_lambda. New objects:

- h_w(x, y) := <(L + i w J) x, y> for real w with abs(w) < abs(E). It is a Hermitian form (i J is Hermitian) on the
  form domain of L. With U = diag(1, i), U* (L + i w J) U = H(w) := [[L+, -w], [-w, L-]], a real symmetric operator
  on pairs (a, d). N(w) := n(h_w) = n(H(w)) on the whole sector space (no constraint).
- Identity (I1): for x in D(A) and y in the form domain, h_w(x, y) = [(A - i w) x, y].
  Proof: <(L + i w J) x, y> = <J^-1 (J L + i w J^2) x, y> = [(A - i w) x, y], since J^2 = -1. PROVED.
- Eigenvalue i w of A with real eigenvector data (a, d) is the same as H(w)(a, d) = 0 (PROOF section 2.2).
- Nodes: sigma_0 < sigma_1 < ... < sigma_n, exact rationals, sigma_0 = 1597/1000, sigma_n = 1983/1000. Cell j is
  [sigma_j, sigma_j+1], width Delta_j, coordinate t in [0, 1].

## 3. The uniform argument

### 3.1 Theorem to be proved (node W)

For every sigma0 in [1597/1000, 1983/1000] there is a decaying one-node solution Sigma(sigma0) of (2.1) with
sigma(0) = sigma0; the map sigma0 -> Sigma(sigma0) is continuous; at each node it is the state certified there;
and for each of these states the spectrum of J L on L^2(R^3; C^2) contains no point with Re lambda > 0.
Not claimed: uniqueness of the one-node state at a given sigma0 beyond the Newton-Kantorovich ball of BR; the
edges; anything nonlinear.

### 3.2 Lemma KC (Krein count). PROVED here, one STANDARD step; to referee

**Statement.** Fix a sector and 0 <= w1 < w2 < abs(E), neither an eigen-frequency. Let S be the sum of the ranges
of the Riesz projections of A for the eigenvalues i w with w1 < w < w2. Then S is finite-dimensional and
n(omega restricted to S) >= N(w1) - N(w2).

**Proof.**
1. The eigenvalues of A in Omega are discrete with finite-rank Riesz projections (Lemma 6.1(c)), and
   i[w1, w2] is a compact subset of Omega. So S is finite-dimensional, S is contained in D(A), A S = S-invariant.
2. Riesz identity (PROOF Theorem 6.2, notation): [P_lambda x, y] = [x, P_{-conj lambda} y]. For lambda = i w,
   -conj lambda = lambda, so P_S is [.,.]-symmetric. Hence X = S + S' with S' = ker P_S, [S, S'] = 0, both
   A-invariant, and [.,.] is nondegenerate on S (it is nondegenerate on X because J is invertible). This is the
   non-degeneracy of the Krein form on a finite system of eigenvalues (compare Kollar-Pego, arXiv 1103.0157,
   Lemma 1, as reported in PRIOR-ART-W1 M13; not opened by this seat).
3. By (I1), for x in S and y in S' (form domain): h_w(x, y) = [(A - i w) x, y] = 0 for every w. So S and S' are
   h_w-orthogonal for every w, and N(w) = n(h_w on S) + n(h_w on S') (additivity over an orthogonal sum, as in
   PROOF Lemma 4.4 step 2).
4. On S, h_w is degenerate iff (A - i w) x = 0 for some nonzero x in S (by (I1) and step 2), that is iff i w is an
   eigenvalue of A in i(w1, w2). So h_w on S is nondegenerate for 0 <= w <= w1, and its index is constant there
   (a continuous family of nondegenerate Hermitian matrices). Hence n(h_w1 on S) = n(h_0 on S) = n(omega on S).
5. On S', n(h_w on S') is constant for w in [w1, w2]. If y in S' is in the kernel of the form h_w restricted to
   S', then h_w(y, .) vanishes on S' and, by step 3, on S; so (L + i w J) y = 0, A y = i w y, and y lies in S (if
   w1 < w < w2) or is zero (w = w1, w2 are not eigen-frequencies); in both cases y = 0. The essential spectrum of
   H(w) is contained in [abs(E) - abs(w), inf) (relative compactness as in Lemma 6.1; STANDARD, not opened). The
   negative eigenvalues of the operator of h_w on S' depend continuously on w (the family is a bounded
   perturbation, norm abs(w - w')) and cannot cross 0. STANDARD min-max continuity, not opened.
6. N(w1) - N(w2) = n(h_w1 on S) - n(h_w2 on S) <= n(h_w1 on S) = n(omega on S).

**Remark.** In the semisimple case this is the graphical Krein signature: an eigenvalue branch mu(w) of H(w) through
0 at w* has mu'(w*) = -2 <a, d> / norm^2, so an upward crossing is a negative-Krein eigenvalue (Kollar-Miller,
SIAM Review 56 (2014); cited from memory, NOT OPENED: the prior-art seat must open it before any text cites it).
KC needs no semisimplicity and no strict sign of <a, d>.

**Robust form used by the instruments.** If #(H(w1) < -eps) >= k + 1 and #(H(w2) < +eps) <= k with eps > 0, the
same holds for all frequencies within eps of w1, w2 (the change of H is w-times a norm-1 operator), so w1 and w2
can be moved off the discrete set of eigen-frequencies. Then N(w1) - N(w2) >= 1.

### 3.3 Lemma IDXC (index inequality with a count drop). PROVED here; to referee

**Statement.** In a sector L, for 0 <= w1 < w2 < abs(E) as in KC:  N_+ + 2 (N(w1) - N(w2)) <= n(L restricted to Y_L).

**Proof.** Let Z be an omega-negative-definite subspace of S of dimension d = n(omega on S) >= N(w1) - N(w2) (KC).
Its complex conjugate conj Z lies in the spectral subspace of -i(w1, w2) and is omega-negative definite of the same
dimension (L is real). By the Riesz identity omega(P_lambda x, y) = omega(x, P_{-conj lambda} y), the spaces
E_+ + E_-, S and conj S are mutually omega-orthogonal (their eigenvalue sets are disjoint and each is closed under
lambda -> -conj lambda). E_+ + E_- contains a negative N_+-plane V1 (PROOF Theorem 6.2 step (iii)). So
V1 + Z + conj Z is negative definite of dimension N_+ + 2d, and it lies in the complexification of Y_L (root
spaces of nonzero eigenvalues lie in Y: Theorem 6.2 step (i)). The complex index equals the real index (step (v)).

**Use.** With K(L) = 2 (PROOF section 4) and one certified drop N(w1) - N(w2) >= 1: N_+ <= 0. This is Theorem 6.2
with the certified eigenvector replaced by two counts. At the nine R2 nodes both certificates exist and must agree.

Expected count pattern (float, P4; prototype-certified at 7/4 and at both end nodes, P10):

| L | N(w) on (0+, w-) | on (w-, w+) | above w+ | w1 used | w2 used |
|---|---|---|---|---|---|
| 0 | 4 just below w- (3 on (0+, 0.5), a positive-Krein mode near 0.5-0.6 raises it to 4) | 3 | 4 | 0.93 w- | (w- + w+)/2 |
| 1 | 3 (2 + the translation-kernel branch, which is negative for w > 0 because <L-^-1 r sigma', r sigma'> = 3m/4 > 0) | 2 | 3 | 0.6 w- | (w- + w+)/2 |
| 2 | 2 | 1 | 2 | 0 | (w- + w+)/2 |

### 3.4 Lemma SHIFT (operator-norm transfer). PROVED (elementary); to referee

If the backgrounds at sigma0 and at a node c satisfy, as operators on the sector space,
diag(V+(sigma0) - V+(c), V-(sigma0) - V-(c)) >= -eta (including the nonlocal term, for which the Hilbert-Schmidt
bound of Lemma 4.1 gives norm <= 2 (I1(sigma0)^(1/2) + I1(c)^(1/2)) (int r (sigma - sigma_c)^2)^(1/2) / (2L+1)),
then #(T(sigma0) < 0) <= #(T(c) < eta) for T = L+, L-, H(w), and symmetrically for lower counts. In the Schur
systems the shift eta enters the a (and d) channels only, never the W channel (PROBES P1 against P2).
This is the zeroth-order (Hoang-Plum-Wieners) transfer. It is enough for the K(L) counts on cells of half-width
0.007 (budget 0.2 against about 26 x half-width at L = 0, ESTIMATE) and is kept as an independent recomputation
on two cells (control C6). It is too weak near the edges (mu about 1e-4), which is why CC is the main tool.

### 3.5 Lemma CC (convexity cover). PROVED (elementary); to referee

**Statement.** Let T_a, T_b, T be closed Hermitian forms on one form domain, 0 <= t <= 1.
- (upper) Let M be a subspace of codimension k with T_a >= m_a and T_b >= m_b on M (m_a, m_b real numbers times the
  norm squared). If T >= (1 - t) T_a + t T_b - eta2 and eta2 < (1 - t) m_a + t m_b, then T > 0 on M and n(T) <= k.
- (lower) Let Nsp be a subspace of dimension k + 1 with T_a <= -m_a and T_b <= -m_b on Nsp. If
  T <= (1 - t) T_a + t T_b + eta2 and eta2 < (1 - t) m_a + t m_b, then n(T) >= k + 1.

**Proof.** A convex combination of forms bounded below by m_a, m_b on M is bounded below by the same combination
of the bounds. A negative-definite subspace meets M only in 0, so its dimension is at most codim M. The lower
part is the definition of n.

**Why it applies.** H(w) is affine in w, and the potentials are, up to a second-order remainder, affine along the
chord between two nodes: with w_t = (1 - t) w_a + t w_b,

    H_sigma0(w_t) >= (1 - t) H_a(w_a) + t H_b(w_b) - eta2(t)      and      <= ... + eta2'(t)       (CH)

where sigma0 = sigma_a + t Delta. So ONE pair of endpoint certificates on a common subspace covers the whole cell,
and the frequency used may differ at the two ends (it follows the window between w- and w+).

**Lemma CH (the chord inequality). PROVED given BR; to referee.** Write sigma_lin = (1 - t) sigma_a + t sigma_b and
e_sigma = sigma(sigma0) - sigma_lin, e_u = u(sigma0) - u_lin (bounded by BR). Then pointwise and in form sense:
- 3 sigma^2 >= chord(3 sigma^2) - 3 t (1 - t) sup(sigma_b - sigma_a)^2 - 6 sup(abs(sigma_lin) abs(e_sigma)) - ...
  (because 3 sigma_lin^2 = chord(3 sigma^2) - 3 t (1 - t) (sigma_b - sigma_a)^2); the same with factor 1 for L-;
- -u >= chord(-u) - sup abs(e_u);
- -2 sigma P_L^-1 sigma >= chord(-2 sigma P_L^-1 sigma) - HS(e_sigma), because
  -2 sigma_lin P^-1 sigma_lin = chord(...) + 2 t (1 - t) (sigma_b - sigma_a) P^-1 (sigma_b - sigma_a) and P^-1 >= 0
  (the nonlocal term has the favourable sign), and the cross terms with e_sigma are bounded in Hilbert-Schmidt
  norm by (4 norm(r^(1/2) e_sigma) I1^(1/2) + 2 norm(r^(1/2) e_sigma)^2) / (2L + 1) (kernel bound of Lemma 4.1).
The sum of the losses is eta2(t); the upper version eta2'(t) is the same list with the signs reversed.
ESTIMATE: eta2 about 0.01 at Delta = 0.05 and about 0.0025 at Delta = 0.025 (from sup abs(d2 sigma / d sigma0^2)
of order 2; to be replaced by certified values from BR).

**Endpoint certificates (node CPOS). SKETCH; proof seat.** "T_end >= m on M = {x : <x, p_j> = 0, j = 1..k}" for the
half-line operator T_end = H_end(w) is proved through the interior Schur system exactly as PROOF Theorem 4.5 (U+):
the constraint vectors p_j are explicit functions supported in [r0, R] (float fits of the k negative eigenvectors,
written as polynomial-times-exponential sums; they are data, not certified objects), so the constraint acts on the
interior piece only and no reserve term is needed (unlike D0). For the interior operator B_m (level m, a-shift
delta_L(R), Robin U_lo, natural conditions): if n(B_m) = k (3-channel count) and the k x k matrix
S_ij = <B_m^-1 P_i, P_j> is negative definite (k forcing columns, as in d0_node), then n(B_m on the orthogonal
complement of the P_j) = n(B_m) - k = 0 (Haynsworth with k vectors: the proof of Theorem 4.7 step 5 with a k-plane).
The lower certificate needs no count: a Gram matrix of the form on k + 1 explicit trial functions supported in
[r0, R] (node RITZ), with the nonlocal term evaluated by one forcing march per trial function.

**K(L) and L >= 3 on a cell.** The same CC mechanism gives, for every sigma0 in the cell:
- L+-(3) >= m > 0 (k = 0, M = whole space), hence L >= 3 by PROOF Lemma 7.1 at that sigma0;
- #(L-(L) <= 0) and #(L+(L) <= 0) bounded by the R1 upper counts (2, 1, 1 and 2, 2, 1), with the kernel directions
  r sigma and r sigma' simply included in the excluded span (the kernel booking of Corollary 4.6 is then applied at
  sigma0 with the exact kernels of that sigma0);
- the constrained count at L = 0: for x orthogonal to g(sigma0) = r sigma(sigma0), abs(<x, g_ref>) <= gamma norm(x)
  with gamma = norm(g(sigma0) - g_ref) from BR, and q+(x) >= [chord - eta2 - M' gamma^2](x) + M' abs(<x, g_ref>)^2
  for any M' >= 0; the right side is affine in t, so CC applies with endpoint certificates of the penalised
  operator (the D0 node with level shift and M' of order 1 / abs(d2), about 0.5; the R2 margins M abs(d2) >= 272
  leave room). SKETCH; proof seat.

### 3.6 Lemma BR (the branch between two nodes). SKETCH; this is the main open proof and instrument

**Statement.** For adjacent nodes a < b with certified tubes: there is a continuous family Sigma(sigma0),
sigma_a <= sigma0 <= sigma_b, of decaying one-node solutions, equal at the two ends to the solutions in the two
tubes, with certified bounds on e_sigma, e_u (weighted sup norms) and on g(sigma0) - g_ref.

**Route.** Reduced variables a = r sigma, b = r u. The linearisation at a node is the L = 0 Schur system at level 0
(a'' = (3 sigma^2 - u) a - sigma b, b'' = -2 sigma a), with a(0) = b(0) = 0, a'(0) = d sigma0, a decaying. Its
inverse exists because ker L+(0) = 0 (PROOF Corollary 4.6). Space X: max(sup abs(d sigma) om(r), sup abs(d u) / s_u)
with om = 1 + (r / 4)^2, s_u = 3.
1. Node quantities (instrument GREEN, linear marches on the point tube only): the first variation tau_a (regular
   2-column solution from r0, decaying solution from R1, 2 x 2 match); a certified bound G_a on the X-norm of the
   inverse, from enclosures of the kernel Phi(r) C Psi(t) step by step (products of an outward-growing and an
   inward-growing factor; no cancellation) plus closed-form tails on [0, r0] and [R1, inf).
2. Predictor: cubic Hermite in sigma0 from (Sigma_a, tau_a, Sigma_b, tau_b).
3. Newton-Kantorovich (radii-polynomial form) with approximate inverse L_a^-1: Y0 = norm(L_a^-1 F(H_t)),
   Z1 = norm(L_a^-1 (DF(H_t) - L_a)), Z2 from the quadratic and cubic terms (constant about 6.25 in this norm).
   F is a cubic polynomial map, so the residual of the predictor is an explicit expression in the node data.
4. One node: zeros of sigma are simple (PROOF Lemma 3.2 step 1) and the tail has a fixed sign, so the zero count is
   constant along a continuous family. By-product: the solution in each node tube is unique in the X-ball.

**Feasibility (PROBE-MEASURED, float).** P5: the linear problem reproduces du0/dsigma0 = 3.424 and
dE/dsigma0 = -2.81 at 7/4 (finite difference of certified tubes: 3.470, -2.847 at the midpoint 1.775), and
G = 15.2 in the unoptimised norm (sigma-part 3.7). P9: with the actual coefficient change between the tubes at 7/4
and 9/5, Z1 per unit sigma0 is 8.0 in the norm (r_w = 4, s_u = 3), so the node linearisation is a valid approximate
inverse out to a distance of about 0.06. Cells of width 0.025 to 0.05 are therefore plausible. The crude a-priori
version (quantitative implicit function theorem with Lipschitz constants only) gives 8e-4 (P5) and is rejected.

**Fallback if GREEN cannot be certified in sup norm.** Use SHIFT only, with the L^2 gap of L+(0) from shifted
counts as the inverse bound; ESTIMATE cell half-width 1e-4 (the Sobolev step loses a factor 25 to 50), about 4000
nodes: not feasible for the whole window. Then certify the largest sub-window the budget allows and report.

### 3.7 Assembly on one cell

For every sigma0 in cell j, with t its coordinate:
1. BR: the state Sigma(sigma0) exists; CH gives eta2(t), eta2'(t), gamma.
2. CC + CPOS at both ends: K(L) <= 2 for L = 0, 1, 2 and L+-(3) >= m > 0.
3. CC + CPOS at both ends: N_L(w2(t)) <= k_L, with (k_0, k_1, k_2) = (3, 2, 1).
4. CC + RITZ at both ends: N_L(w1(t)) >= k_L + 1.
5. IDXC: N_+ <= K(L) - 2 = 0 in sectors L = 0, 1, 2 (every M); PROOF Corollary 7.2 for L >= 3; Theorem 7.3 for 3-D.
Nothing in steps 2-5 uses a Krawczyk certificate, an eigenvector or an interval-valued sigma0.

## Nodes

| id | claim | source | status | expected | depends | referee | lean |
|---|---|---|---|---|---|---|---|
| R1 | pointwise chain at any exact rational sigma0: B-EX, B-TAIL, BR brackets, D0, ESS, IDX, L >= 3 monotonicity, 3-D statement | proof/PROOF-R1-v2.md sections 3-7 | PROVED | - | - | referee-5 CORRECT; referee-7 transfer to R2 points CORRECT WITH FIXES (text) | no |
| G9 | nine certified stable points 1597/1000 .. 1983/1000 with K = (2,2,2,0), Krein pairs (w-, w+) per L, tube sha per point | build-3/out/*/B.json, K0-K2.json, R2_all_verdicts.json | CERTIFIED | 9 | R1 | referee-7 CORRECT | no |
| I1 | h_w(x, y) = [(A - i w) x, y] for x in D(A); H(w) = [[L+, -w], [-w, L-]] is unitarily equivalent to L + i w J | this design section 2 | PROVED (to referee) | - | R1 | NEW: referee | candidate |
| KC | Krein count: n(omega on S) >= N(w1) - N(w2) for the spectral subspace S of i(w1, w2) | this design section 3.2 | PROVED (to referee) | - | I1, R1 | NEW: referee | no |
| IDXC | N_+ + 2 (N(w1) - N(w2)) <= n(L on Y_L) <= K(L) | this design section 3.3 | PROVED (to referee) | - | KC, R1 | NEW: referee | no |
| SHIFT | operator-norm transfer of counts, shift in the a and d channels only | this design section 3.4 | PROVED (to referee) | - | R1 | NEW: referee | candidate |
| CC | convexity cover: endpoint bounds on a common subspace give the count on the whole cell | this design section 3.5 | PROVED (to referee) | - | - | NEW: referee | candidate |
| BR | branch lemma: continuous family of one-node states between adjacent nodes with certified deviation from the Hermite predictor | this design section 3.6 (sketch); proof seat | GAP (sketch; proof seat writes it; this raid) | - | R1 | NEW: referee | no |
| CH | chord inequality (CH): H_sigma0(w_t) >= chord - eta2(t), <= chord + eta2'(t), nonlocal term with favourable sign | this design section 3.5 | PROVED (to referee) | - | BR | NEW: referee | candidate |
| CPOSL | endpoint lemma: n(B_m) = k and S negative definite imply T_end >= m on the complement of k explicit vectors (3-channel BR-R0, BR-M, exterior block, Haynsworth with k vectors); penalised version for the L = 0 constraint | this design section 3.5 (sketch); extends PROOF Lemmas 4.3-4.5, Theorem 4.7 | GAP (sketch; proof seat; this raid) | - | R1, I1 | NEW: referee | no |
| HW3 | instrument: certified 3-channel counts of H_L(w) with per-step column re-basing | window/design/probe/hw3.py (prototype, P10); build seat makes window/build-4/hw3.py | GAP (prototype runs; build + audit this raid) | - | CPOSL | NEW: audit | no |
| GREEN | instrument: first variation tau and sup-norm inverse bound G at a node; Hermite predictor; NK radii; eta2, gamma | build seat, window/build-4/green.py | GAP (not built; float probes P5, P9) | [3, 20] | BR | NEW: audit | no |
| NODES | point tubes (B-EX, B-TAIL) at all nodes, existing bg_tube.py unchanged | build-3/bg_tube.py; run after seal | GAP (run after seal; 9 of 23 rebuild pinned shas) | 23 | R1, G9 | - | no |
| CK | for every cell: K(L) <= 2 at L = 0, 1, 2 and L+-(3) >= m > 0, uniformly in the cell | CC + CPOSL + CH; run after seal | GAP (run after seal) | 2 | CC, CH, CPOSL, HW3, GREEN, NODES | - | no |
| CN2 | for every cell and L = 0, 1, 2: N_L(w2(t)) <= (3, 2, 1) uniformly | CC + CPOSL + CH; run after seal | GAP (run after seal) | [1, 3] | CC, CH, CPOSL, HW3, GREEN, NODES | - | no |
| CN1 | for every cell and L = 0, 1, 2: N_L(w1(t)) >= (4, 3, 2) uniformly (Gram matrix on explicit trial functions) | CC lower + CH; run after seal | GAP (run after seal) | [2, 4] | CC, CH, HW3, GREEN, NODES | - | no |
| XK | control: at the nine G9 nodes the count N_L(w) drops by 1 across each certified w- and rises by 1 across each certified w+ (two independent instruments) | HW3 against build-3/out/*/K*.json | GAP (run before the cells; must pass) | 1 | HW3, G9 | - | no |
| XU | must-fail control: no certificate on a cell that contains a certified unstable point (1595/1000, 1985/1000, 31/20, 2) | HW3 + CC on cells [1595/1000, 1597/1000] and [1983/1000, 1985/1000] | GAP (run before the cells; must be INCONCLUSIVE) | 0 | HW3, CC, G9 | - | no |
| W | spectral stability for every sigma0 in [1597/1000, 1983/1000] along the continuous family of BR | section 3.7 | GAP (target; closes when CK, CN1, CN2 hold on every cell) | - | R1, G9, IDXC, BR, CK, CN1, CN2, XK, XU, SHIFT | NEW: referee | no |

## Failure modes

1. **The 3-channel counter miscounts** (Morse index of a 3 x 3 system, endpoint inertia, re-basing). Control XK:
   at the nine certified nodes the counts must drop by exactly 1 across each of the 27 certified negative-Krein w
   and rise by 1 across each of the 27 certified positive-Krein w (levels +-1e-5, frequencies w +- 0.002); lower
   count = upper count on both sides. A single mismatch voids the instrument. Extra: at w = 0 the count must equal
   n(L+) + n(L-) from bracket.py (2-channel instrument) at every node.
2. **The certificate is vacuous (would pass anywhere).** Control XU: the full cell pipeline is run on cells that
   contain the certified unstable points 1595/1000 and 1985/1000. It must end INCONCLUSIVE in the offending sector
   (L = 0 below, L = 2 above). A pass there voids the route. Second check: with w1 and w2 both placed below w-
   the drop must be 0.
3. **BR constants are wrong or too optimistic** (G, Z1, the Hermite residual). Controls: (a) du0/dsigma0 and
   dE/dsigma0 from GREEN against the finite differences of certified node tubes (3.42 against 3.47 at 7/4 in float,
   P5); (b) leave-one-out: build the predictor on the cell [7/4, 37/20] and compare it at 9/5 with the certified
   R1 tube; the difference must lie inside the certified NK radius; (c) the two tubes of a cell must satisfy the
   chord bound at t = 0 and t = 1 trivially (eta2 = 0), a wiring test.
4. **Margins vanish near the edges** (mu about 1e-4 at the end nodes; delta_L(R) at R = 14 is 4e-4 to 7e-4 for
   L = 0, larger than mu). Rule: end cells use R = 20 (delta = 6.5e-7 at 1597/1000, P10c) and level 1e-5; cells
   are bisected (new node at the midpoint) up to depth 4 when a cell certificate does not close; if a cell still
   does not close, the theorem is stated for the largest union of closed cells and the failing cell is reported
   with its numbers (the SCOPE's second outcome).
5. **A level or shift leaks into the auxiliary W channel** and creates a spurious count (seen in P1: +1 at
   eps = 0.03, R = 14). Rule and assert: eta and m enter the a and d channels only; the W-channel level stays at
   eps <= 1e-3 < (pi / 2R)^2 / 4. Control: P1 against P2 reproduced by the built instrument.
6. **The exterior block is not positive** (needs abs(E) - m/R - delta - w - eps > 0; fails at R = 10 for L = 0
   where w2 is about 1.14). Assert in the instrument; R >= 14 for L = 0. Control: C-R, the counts must agree at
   two radii (14 and 20).
7. **Kernel and constraint handling on a cell** (r sigma, r sigma' move with sigma0; the L = 0 constraint vector
   moves). Control C6: on two mid-window cells of half-width 0.005 recompute K(L) by SHIFT alone (zeroth order, no
   convexity, no reference vectors); the two routes must give the same K.
8. **Run pathologies**: a zero of det Y that the bisection cannot isolate ran for more than 100 s in the prototype
   without re-basing (P10). Rule: per-step re-basing by an exact point matrix (det of the transformed columns has
   the same zeros); a hard watchdog per count; a count that does not finish is INCONCLUSIVE, never retried silently.

## 6. Cost model and schedule

Measured unit costs (PROBES; machine otherwise idle unless noted):
- point tube 51 to 63 s (78 to 102 s inside the two-lane R2 runs);
- R1 brackets, two radii, L = 0..3, with D0: 23 to 27 s; one 2-channel count 0.5 s;
- one 3-channel count with re-basing 1.2 to 2.2 s (prototype);
- GREEN, CPOS forcing columns, RITZ: not built; ESTIMATE 60 s per node and 120 s per cell.

Recommended nodes (23; the nine G9 points in bold are rebuilt with their pinned shas):
**1597/1000**, 1600/1000, 1605/1000, 1612/1000, 1625/1000, **33/20**, 1675/1000, **17/10**, 1725/1000, **7/4**,
1775/1000, **9/5**, 1825/1000, **37/20**, 1875/1000, **19/10**, 1925/1000, **39/20**, 1962/1000, 1970/1000,
1976/1000, 1980/1000, **1983/1000**.
Cells: 22, widths 0.003 to 0.025. The widths are an ESTIMATE from float margins (P8: a common subspace works with
no visible loss over the 0.05 cell [7/4, 9/5]; mu at the end nodes is 1e-4) and from the BR radius 0.06 (P9). A
float pre-pass (not part of the proof) fixes w1, w2, the vectors p_j and the trial functions per cell.

Budget: nodes 23 x (80 + 60 + 40) s = 69 min; cells 22 x 120 s = 44 min; controls XK, XU, C6 about 15 min. About
2 lane-hours; with a factor 3 for the unbuilt instruments and up to 20 bisection nodes, 6 lane-hours, that is 3 to
4 hours of wall time on two lanes. Chunking: one job per node (under 5 min) and one job per cell (under 5 min);
no job near the 30-minute limit. Heavy evening compute is not needed.

Staged plan:
- Stage 0 (before the seal): proof seat writes KC, IDXC, CC, CH, CPOSL, BR in full; referee; build seat makes
  hw3 and green with audits; controls XK and XU are run and must behave as stated.
- Stage A: the middle window [33/20, 39/20] (13 nodes, 12 cells, margins 0.008 to 0.09).
- Stage B: the two end zones [1597/1000, 33/20] and [39/20, 1983/1000] with level 1e-5, R = 20 and bisection.
- If Stage B fails in a cell: publish Stage A plus the closed part of Stage B, with the failing cell described.

## 7. Risks and open questions

1. BR is the critical unproved piece. Its sup-norm inverse bound has only float support (P5, P9). If the certified
   G or Z1 come out several times larger, cells shrink in proportion (more nodes, each about 3 minutes).
2. KC step 5 uses two STANDARD facts not opened (essential spectrum of H(w); continuity of negative eigenvalues of
   a restricted form family). A referee should decide whether the restricted-form argument on S' needs more care
   (S' is not L^2-orthogonal to S; only form-orthogonal).
3. The convexity cover needs the endpoint certificates at the END nodes with margin about 1e-4; the prototype
   resolves the plain count at level 1e-5 there (P10c) but the constrained version (CPOS) is untested.
4. The explicit vectors p_j and trial functions must be evaluated on two different tube grids; they are closed-form
   functions, so this is bookkeeping, but it is new code.
5. The counts for L = 0 rely on the pattern 3, 4, 3, 4 including a low positive-Krein mode near 0.5-0.6 seen only in
   float (P4). w1 is placed just below w- so the pattern further down does not matter, but the pre-pass must check
   it per cell.
6. Prior art for KC: the graphical Krein signature (Kollar-Miller) is cited from memory and was not opened. The
   count-drop certificate itself was not searched by this seat; the prior-art seat should gate "negative-Krein
   eigenvalue certified by a drop in the negative index of L + i w J" before any novelty wording.
7. UNTESTED curiosity (surfaced, not used): by convexity of h_w in w, on the complement of the unstable root
   spaces n(h_w) at an interior frequency is at most the sum at two outer frequencies; this gives
   N_+ <= N(wa) + N(wb) - N(w) for wa < w < wb, an eigenvector-free instability bound that needs no count at w = 0.
   For L = 2 it already gives N_+ <= 2 N(w2) - N(0) = 0. For L = 0, 1 the kernels at w = 0 make it too weak
   on the full space (it gives 1), so the design uses IDXC with K(L) instead.

## 8. Credits for method (from the prior-art gate, window/gate/PRIOR-ART-W1.md)

Grid of certified points plus a perturbation argument: Hoang-Plum-Wieners, ZAMP 60 (2009). Stability over a whole
parameter interval by interval arithmetic: Barker, arXiv 1401.5371. Nonlocal problem stable on a parameter interval:
Breden-Payan-Reisch-Tang, arXiv 2504.05066. Box cover with negative controls: Braz e Silva, Zenodo
10.5281/zenodo.23772125. Warning that naive interval parameters fail: Barker-Zumbrun, arXiv 1601.00837, Remark 1.2.
Krein-form non-degeneracy on finite systems: Kollar-Pego, arXiv 1103.0157, Lemma 1. This seat opened none of them;
the wording follows the gate file.
