# DESIGN-W2: spectral stability of the one-node repulsive GPP state for EVERY sigma0 in [1597/1000, 1983/1000]

Seat design-W1, raid R3-WINDOW, 2026-11-19. Supersedes DESIGN-W1.md (kept unchanged). Design only: no certified
target run. It closes the blocking items of seats/referee-W1/REFEREE-DESIGN-W1.md (items 1-8 of the lead's brief)
and folds in the gate result gate/PRIOR-ART-W2-KC.md as relayed by the lead (this seat did not open that file's
sources). Labels: PROVED (argument written here in full, not yet refereed in this form), PROBE-MEASURED (see
PROBES.md; float probes are not certificates), ESTIMATE. TARGETS-R1*.md were not read.

thesis: plank 2 (certified computation with explicit constants: a nine-point certificate becomes an interval certificate) - certified grid nodes plus perturbation arguments that use only counts and linear solves
target: W
reuses: PROOF-R1-v2 chain (B-EX, B-TAIL, BR brackets, D0, ESS, IDX, L>=3 monotonicity), build-3 instruments bg_tube.py / itaylor.py / lincore.py / bracket.py / tail.py unchanged, the nine R2 certified points with their Krawczyk Krein pairs (controls), band/map float map (steering only), graphical Krein signature (Kollar-Miller arXiv 1209.3185; Kollar-Bosak arXiv 1212.5691 Thm 4; Binding-Browne 1988), grid-plus-perturbation (Hoang-Plum-Wieners ZAMP 60)
produces: written infinite-dimensional proof of the local Krein index identity with essential spectrum (KC, for completeness - classical in finite dimensions), its use as a computer-assisted certificate (count drop instead of an eigenpair), convexity-cover lemma CC with chord inequality CH, branch lemma BR (Newton-Kantorovich between certified nodes), 3-channel matrix-Sturm counter hw3, constrained-positivity node CPOS, linear node instrument GREEN, the interval certificate

## 0. In plain words

The published result proves the shelled dark-matter ball is stable at nine values of its central amplitude. This
design extends that to every value in between, without ever carrying the amplitude as an interval through the
computation (which fails; Barker-Zumbrun 1601.00837 Remark 1.2 say the same).

1. Counting replaces eigenvectors. For a trial frequency w, count the negative directions of one fixed symmetric
   operator H(w). If the count drops between w1 and w2, the part of the spectrum on the imaginary axis between
   i w1 and i w2 carries a negative-energy direction. Together with the old count K(L) <= 2 this rules out
   instability. This is the classical "graphical Krein signature" index identity, used here as a certificate.
2. Convexity replaces interval parameters. Along a cell between two certified nodes the operator is, up to a small
   certified remainder, a straight-line mix of the two end operators. If both end operators have a certified
   positive MARGIN on one common explicit subspace, every operator in between is positive on that subspace, and
   that bounds its count. (Counts at the two ends alone would not be enough; the certificate is the pair of
   margins on a common subspace.)
3. The family of states between two nodes is enclosed by a Newton-Kantorovich argument that uses only linear
   solves at the nodes.

Float probes of the referee's next strike (PROBES P11): on the mid cell [7/4, 9/5] and on both end cells
[1597/1000, 1600/1000], [1980/1000, 1983/1000] the branch lemma closes with large room and the chord losses are 4 to
40 times below the margins. So the end cells can close and the full window [1597/1000, 1983/1000] stays the target.

## 1. What changed from W1

| item | W1 | W2 |
|---|---|---|
| KC, IDXC | called new | classical (graphical Krein signature; Kollar-Bosak Thm 4 eq. (14); Kollar-Miller Thm 7; Binding-Browne); our text is a written proof for the infinite-dimensional case with essential spectrum, "for completeness". The IDENTITY is stated and used (section 3.2) |
| KC step 5 | two STANDARD facts | written out (referee's argument) |
| BR | sketch, wrong nondegeneracy reason | full statement and proof (section 3.6): match determinant and d_E(0) != 0; forcing space with weight om^2 on the second component; Y0(t) <= t^2 (1-t)^2 Y*; one-node constancy |
| CH | eta2' had the nonlocal sign wrong | two separate lists (section 3.5) |
| CPOSL | sketch | written (section 3.5): Haynsworth with k vectors; penalised L = 0 count with each end's own g and the D0 exterior split; penalty M' = 5, so M' abs(d2) is about 10, not 1.09 |
| 3.7 | counts only | full list of what is needed at every sigma0 and how each is certified |
| XU | INCONCLUSIVE anywhere passes | failure must be "no drop" in the named sector with everything else closed; w-pair scan; BR content null |
| cost | 2 to 6 lane-hours, GREEN unprobed | GREEN marches probed (2.1 s); about 1.5 lane-hours, under 1 h wall on two lanes; SPEEDUP-W1.md |

## 2. Setting and notation

PROOF-R1-v2 sections 2-7 are used as is: per sector L the operators L+-(L), A = J L, Y_L, K(L), N_+, the forms
[x, y] = <J^-1 x, y> and omega(x, y) = <L x, y>, Omega, Riesz projections P_lambda. In addition:

- h_w(x, y) := <(L + i w J) x, y>, real w, abs(w) < abs(E): a Hermitian form on the form domain Q of L. With
  U = diag(1, i): U* (L + i w J) U = H(w) := [[L+, -w], [-w, L-]] on pairs (a, d). N(w) := n(h_w) = n(H(w)) on the
  whole sector space.
- (I1) For x in D(A), y in Q: h_w(x, y) = [(A - i w) x, y]. Proof: <(L + i w J) x, y> = <J^-1 (J L + i w J^2) x, y>
  and J^2 = -1.
- Nodes sigma_0 < ... < sigma_n (exact rationals, sigma_0 = 1597/1000, sigma_n = 1983/1000). On a cell [a, b] of
  width Delta: t in [0, 1], sigma0 = sigma_a + t Delta, "chord(f)" := (1 - t) f_a + t f_b, w_t := chord(w).
- Background map F(sigma, u) := (-Lap sigma + sigma^3 - u sigma, -Lap u - sigma^2), Lap = d^2/dr^2 + (2/r) d/dr.
  F = 0 is (2.1) with s = 1. Linearisation at a node a:
  L_a (d, v) := (-Lap d + (3 sigma_a^2 - u_a) d - sigma_a v, -Lap v - 2 sigma_a d).

## 3. The uniform argument

### 3.1 Theorem to be proved (node W)

For every sigma0 in [1597/1000, 1983/1000] there is a decaying one-node solution Sigma(sigma0) of (2.1) with
sigma(0) = sigma0; sigma0 -> Sigma(sigma0) is continuous; at each node it is the (unique, see BR) decaying solution
in that node's tube; and for each of these states the spectrum of J L on L^2(R^3; C^2) has no point with
Re lambda > 0. Wording of any release: "stable on [a, b], unstable at the certified points outside" (the form used
by Barker 2014 and Breden et al. 2025); the method class is credited, and neither the interval nor the count lemma
is called first. Not claimed: uniqueness of the one-node state at a given sigma0 outside the ball of BR; the edges.

### 3.2 Lemma KC (local Krein index identity; classical, proof written for completeness). PROVED; to referee

**Statement.** Fix a sector and 0 <= w1 < w2 < abs(E), neither an eigen-frequency of A. Let S be the sum of the
ranges of the Riesz projections of A for the eigenvalues i w, w1 < w < w2. Then S is finite-dimensional and

    N(w1) - N(w2) = n(h_w1 on S) - n(h_w2 on S),      n(h_w1 on S) = n(omega on S).

In particular n(omega on S) >= N(w1) - N(w2). In the semisimple case the right side of the identity is
(number of negative-Krein) - (number of positive-Krein) eigenvalues in i(w1, w2): a certified count DROP certifies
negative-Krein spectrum, and a certified count RISE certifies positive-Krein spectrum in the window.

**Credit.** Finite-dimensional statement and the graphical picture: Kollar-Bosak, arXiv 1212.5691, Theorem 4,
eq. (14); Kollar-Miller, SIAM Review 56 (2014), arXiv 1209.3185 (kappa = sign of d mu / d lambda; Theorems 6, 7);
Binding-Browne 1988. Those sources work in finite dimensions and call the extension straightforward (gate
PRIOR-ART-W2-KC; referee-W1 opened Kollar-Miller). The proof below covers essential spectrum and Jordan chains.
What the gate found open is the use of the identity as a computer-assisted certificate, and uniformly in a
parameter.

**Proof.**
1. Eigenvalues of A in Omega are discrete with finite-rank Riesz projections (Lemma 6.1(c)); i[w1, w2] is a compact
   subset of Omega. So S is finite-dimensional, S lies in D(A), A S is contained in S.
2. Riesz identity (PROOF Theorem 6.2): [P_lambda x, y] = [x, P_{-conj lambda} y], and -conj(i w) = i w. So P_S is
   [.,.]-symmetric, X = S + S' with S' := ker P_S, [S, S'] = 0, both A-invariant, and [.,.] is nondegenerate on S
   (compare Kollar-Pego, arXiv 1103.0157, Lemma 1).
3. By (I1), h_w(x, y) = [(A - i w) x, y] = 0 for x in S, y in S' and Q, every w. So N(w) = n(h_w on S) + n(h_w on S')
   (additivity over a form-orthogonal sum with one finite-dimensional summand, as PROOF Lemma 4.4 step 2).
4. On S: h_w is degenerate iff (A - i w) x = 0 for some nonzero x in S, i.e. iff i w is an eigenvalue in i(w1, w2).
   So h_w on S is nondegenerate for 0 <= w <= w1 and for w >= w2; its index is constant on [0, w1], hence
   n(h_w1 on S) = n(h_0 on S) = n(omega on S). Kernels and Jordan blocks of A at 0 lie in S' and play no role.
5. On S': n(h_w on S') is constant on [w1, w2] (referee-W1's argument).
   - Work in the Hilbert space S' with the inherited inner product. S' and Q is dense in S', because (I - P_S) maps Q
     into Q and P_S is bounded with range in D(A).
   - The form h_w restricted to S' and Q is closed and bounded below; its operator is
     T_w = T_w1 + (w - w1) Pi (i J) restricted to S' (Pi the orthogonal projection onto S'), a bounded perturbation of
     norm <= abs(w - w1). So the eigenvalues of T_w below its essential spectrum move continuously in w.
   - #(T_w < lam) <= #(H(w) < lam) by restriction (min-max). The essential spectrum of H(w) lies in
     [abs(E) - w, inf): the free part is diag(H0, H0) + w [[0, -1], [-1, 0]], unitarily diag(H0 - w, H0 + w) >=
     abs(E) - w, and V is relatively compact (as in Lemma 6.1). So the spectrum of T_w below abs(E) - w2 > 0 is
     discrete, for every w in [w1, w2].
   - If T_w y = 0, then h_w(y, .) vanishes on S' and Q and, by step 3, on S; so it vanishes on Q, and by the
     representation theorem y is in D(L) with (L + i w J) y = 0, i.e. A y = i w y. For w1 < w < w2 this puts y in S
     and S', so y = 0; w1 and w2 are not eigen-frequencies. Hence 0 is never an eigenvalue of T_w on [w1, w2], no
     eigenvalue crosses 0, and the number of negative eigenvalues is constant.
6. Subtract: N(w1) - N(w2) = n(h_w1 on S) - n(h_w2 on S).

**Robust form.** If #(H(w1) < -eps) >= k + 1 and #(H(w2) < +eps) <= k, the same holds for all frequencies within
eps of w1 and w2, so they can be moved off the discrete set of eigen-frequencies (this also covers w1 = 0 at
L = 2, moved to w1' in (0, eps)). Then N(w1') - N(w2') >= 1.

### 3.3 Lemma IDXC (Hamiltonian-Krein index plus the local identity; classical). PROVED; referee-W1 CORRECT

N_+ + 2 (N(w1) - N(w2)) <= n(L restricted to Y_L) <= K(L).
Proof as in DESIGN-W1 section 3.3 (referee-W1: CORRECT; 3999 finite-dimensional trials, 0 violations): a negative
d-plane Z in S (d = n(omega on S)), its conjugate in the spectral subspace of -i(w1, w2), and the negative N_+-plane
in E_+ + E_- are mutually omega-orthogonal and lie in Y_L. With K(L) = 2 and one drop: N_+ = 0.
(Credit: Kollar-Miller Theorem 7 gives the finite-dimensional index theorem.)

Count pattern (float P4 and referee-W1 nw_fd.py; prototype-certified at 7/4 and both end nodes, P10, P10c):

| L | N just below w- | on (w-, w+) | above w+ | w1 | w2 |
|---|---|---|---|---|---|
| 0 | 4 (3 below a positive-Krein mode near 0.48 to 0.55) | 3 | 4 | 0.93 w- | (w- + w+)/2 |
| 1 | 3 | 2 | 3 | 0.6 w- | (w- + w+)/2 |
| 2 | 2 | 1 | 2 | 0 | (w- + w+)/2 |

### 3.4 Lemma SHIFT (zeroth-order transfer). PROVED; referee-W1 CORRECT

As in DESIGN-W1 section 3.4. Used only as an independent control (C6) on two short cells.

### 3.5 Lemmas CC, CH, CPOSL

**Lemma CC (convexity cover). PROVED; referee-W1 CORRECT.** T_a, T_b, T closed Hermitian forms on one form domain.
- (upper) M a subspace of codimension k, T_a >= m_a and T_b >= m_b on M. If T >= chord(T) - eta2 and
  eta2 < chord(m), then T > 0 on M, so n(T) <= k and dim Ran 1_(-inf, 0](T) <= k.
- (lower) Nsp of dimension k + 1 with T_a <= -m_a, T_b <= -m_b on Nsp. If T <= chord(T) + eta2' and
  eta2' < chord(m), then n(T) >= k + 1.
The certificate is the pair of MARGINS on a COMMON subspace; endpoint counts alone do not imply anything inside.

**Lemma CH (chord inequalities). PROVED given BR; to referee.** On a cell let sigma_lin = chord(sigma),
Dsig = sigma_b - sigma_a, and let BR give pointwise bounds e_sig(r) >= abs(sigma(sigma0) - sigma_lin)(r),
e_u(r) >= abs(u(sigma0) - chord(u))(r). Write n_e := (int r e_sig^2 dr)^(1/2) and
I_lin := (1 - t) I1_a^(1/2) + t I1_b^(1/2) >= (int r sigma_lin^2)^(1/2). For H(w_t) (the off-diagonal part is exactly
affine) and c = 3 in the L+ block, c = 1 in the L- block:

Lower side (used for upper counts), H_sigma0(w_t) >= chord(H(w)) - eta2(t):
- local: c sigma^2 >= chord(c sigma^2) - c t (1 - t) Dsig^2 - 2 c abs(sigma_lin) e_sig, because
  c sigma_lin^2 = chord(c sigma^2) - c t (1 - t) Dsig^2 and c e^2 >= 0 is dropped;
- potential: -u >= chord(-u) - e_u;
- nonlocal (L+ block only): -2 sigma P^-1 sigma >= chord(-2 sigma P^-1 sigma) - (4 n_e I_lin + 2 n_e^2) / (2L + 1),
  because -2 sigma_lin P^-1 sigma_lin = chord(...) + 2 t (1 - t) Dsig P^-1 Dsig >= chord(...) (P^-1 >= 0), and the cross
  terms with e = sigma - sigma_lin are bounded in Hilbert-Schmidt norm by the kernel bound of Lemma 4.1.

      eta2(t) := sup_r [ 3 t (1 - t) Dsig^2 + 6 abs(sigma_lin) e_sig + e_u ] + (4 n_e I_lin + 2 n_e^2) / (2L + 1).

Upper side (used for lower counts), H_sigma0(w_t) <= chord(H(w)) + eta2'(t):
- local: c sigma^2 <= chord(c sigma^2) + 2 c abs(sigma_lin) e_sig + c e_sig^2 (the term -c t (1 - t) Dsig^2 helps and
  is dropped);
- potential: -u <= chord(-u) + e_u;
- nonlocal: now the convexity term is on the unfavourable side:
  -2 sigma P^-1 sigma <= chord(...) + 2 t (1 - t) (int r Dsig^2) / (2L + 1) + (4 n_e I_lin + 2 n_e^2) / (2L + 1).

      eta2'(t) := sup_r [ 6 abs(sigma_lin) e_sig + 3 e_sig^2 + e_u ]
                  + (2 t (1 - t) int r Dsig^2 + 4 n_e I_lin + 2 n_e^2) / (2L + 1).

Both vanish at t = 0, 1 and are bounded by t (1 - t) C_cell with certified C_cell (BR gives
e_sig, e_u <= t (1 - t) times certified profiles). PROBE-MEASURED (P11b, float): on [7/4, 9/5] max eta2 = 7.0e-3,
4.0e-3, 3.4e-3 and max eta2' = 9.5e-3, 3.6e-3, 2.4e-3 for L = 0, 1, 2; on the two end cells of width 0.003 all are
below 3.6e-5.

**Lemma CPOSL (endpoint margin on the complement of k explicit vectors). PROVED; to referee.**
Setting: one node, sector L, frequency w, margin m >= 0, radius R. Interior 3-channel form on [r0, R] for
Y = (a, d, W):

    B_m[Y] = int_r0^R ( abs(Y')^2 + Y^T Q_m Y ) + <U_lo Y(r0), Y(r0)> + (L/R) W(R)^2,
    Q_m = [[ell/r^2 + 3 sigma^2 - u - delta_L(R) - m, -w, sqrt2 sigma], [-w, ell/r^2 + sigma^2 - u - m, 0], [sqrt2 sigma, 0, ell/r^2]].

The level m sits in the a and d channels only (in PROOF Theorem 4.5 the level in the W channel is an optional
weakening; taking it 0 there is valid and removes the spurious W-mode of probe P1). U_lo is the Robin bound of
PROOF Lemma 4.3 for the 3 x 3 system at levels in [-m - 1, m + 1] (the lemma is stated for matrix systems).
Let p_1..p_k be explicit L^2 functions with values in R^2, supported in [r0, R], and P_j := (p_j, 0).

(a) Count. PROOF Lemma 4.4 holds for n = 3 with F the free boundary directions and S = diag(0, 0, L/R): the only
n-dependent step is "a simple zero of det Phi has a one-dimensional kernel"; for n = 3, dim ker Phi(rho) >= 2 means
rank <= 1, so adj Phi(rho) = 0 and (det Phi)' = tr(adj(Phi) Phi') = 0. Column re-basing by an exact invertible
point matrix per step does not change the zeros of det Phi.

(b) Haynsworth with k vectors. Let B be a closed form with finite negative index whose operator is invertible,
h_i := B^-1 P_i, S_ij := <h_i, P_j> = B(h_i, h_j). If S is negative definite, then n(B) = n(B on the complement of
the P_j) + k. Proof: every Y is Z + sum c_i h_i with c = S^-1 (<Y, P_j>)_j; then <Z, P_j> = 0 and B(Z, h_j) =
<Z, P_j> = 0, so the space is the B-orthogonal direct sum of {P}^perp and span(h), on which B is negative definite of
dimension k; additivity as in Lemma 4.4 step 2.

(c) Statement. If ext := abs(E) - m_bg/R - delta_L(R) - abs(w) - m > 0, n(B_m) = k (count, with det Phi(R)-type
nondegeneracy as in Theorem 4.7), and S is negative definite (k forcing columns as in bracket.d0_node), then
H(w)[x] >= m norm(x)^2 for every x = (a, d) in the form domain with <x, p_j> = 0, j = 1..k.
Proof: for such x let W* := -sqrt2 P_L^-1 (sigma_i a) (Lemma 4.2). As in the proof of Theorem 4.5 (U+):
H(w)[x] - m norm(x)^2 >= B_m[(a, d, W*) on [r0, R]] + (the [0, r0] piece minus <U_lo c, c>) + exterior. The [0, r0]
piece is >= <U_lo c, c> (Lemma 4.3(c)); the exterior W-part is >= 0 (Lemma 4.2); the exterior (a, d)-part is the
form of -d^2 + [[c_e - delta - m, -w], [-w, c_e - m]] with c_e >= abs(E) - m_bg/R, which is >= ext >= 0. The interior
piece is orthogonal to the P_j because the p_j vanish outside [r0, R]. By (a), (b): B_m >= 0 on {P}^perp.

(d) Penalised L = 0 count (the constraint a perp g(sigma0) = r sigma(sigma0)). For x perp g(sigma0) write
A_x = <x, g_a>, B_x = <x, g_b>, g_lin = chord(g), e_g = g(sigma0) - g_lin (BR bounds norm(e_g) <= gam_e). Then
<x, g_lin> = -<x, e_g> and

    (1 - t) A_x^2 + t B_x^2 = <x, g_lin>^2 + t (1 - t) (A_x - B_x)^2 <= Gam(t) norm(x)^2,
    Gam(t) := gam_e^2 + t (1 - t) norm(g_b - g_a)^2.

Hence, for any M' >= 0 and x perp g(sigma0):
q+_sigma0(x) >= chord(q+)(x) - eta2 norm(x)^2 >= [(1 - t) Pen_a + t Pen_b](x) - (eta2 + M' Gam(t)) norm(x)^2,
Pen_end := q+_end + M' <., g_end>^2. If Pen_a >= m_a and Pen_b >= m_b on a common codimension-1 subspace {p}^perp and
eta2 + M' Gam < chord(m), then q+_sigma0 > 0 on g(sigma0)^perp and p^perp, so
n(L+(0; sigma0) restricted to g(sigma0)^perp) <= 1.
Endpoint certificate for Pen_end >= m on p^perp (g_end is not compactly supported; exterior as in D0): split
[0, r0] (1), [r0, R] (2), [R, inf) (e). For theta in (0, 1) and nu', c' > 0,
<x, g>^2 >= (1 - theta) <x_2, g_2>^2 - (1/theta - 1) (norm(g_1)^2/nu' + norm(g_e)^2/c') (nu' norm(x_1)^2 + c' norm(x_e)^2).
Choose nu' <= the [0, r0] reserve (Robin at level m + nu', as in Theorem 4.7) and c' <= ext, and theta with
M' (1/theta - 1) (norm(g_1)^2/nu' + norm(g_e)^2/c') <= 1; norm(g_1)^2 <= sg^2 r0^3/3 and norm(g_e)^2 (tube boxes plus
tail, bracket.gnorms) are tiny, so theta is about 1e-3 or smaller. Then
Pen_end[x] - m norm(x)^2 >= B_m[Y_2] + M'' <Y_2, G>^2, M'' := M' (1 - theta), G := (g_2, 0).
With the 2 x 2 matrix s of <B_m^-1 ., .> on (P, G) (two forcing columns), d2 := s_GG: if n(B_m) = 2, d2 < 0 and
M'' abs(d2) > 1, then B' := B_m + M'' G G^T has n(B') = 1 (Theorem 4.7 step 5); by Sherman-Morrison
<B'^-1 P, P> = s_PP - M'' s_PG^2 / (1 + M'' d2); if this is negative, (b) with k = 1 gives n(B' on P^perp) = 0.
Choice of M': the R2 values are d2 in [-2.25, -1.91], so M' = 5 gives M'' abs(d2) about 10 (M' = 0.5 would give
1.09, too tight: referee-W1). The price is M' Gam: norm(g_b - g_a)^2 is about 8.4 Delta^2 (ESTIMATE from P5:
int r tau_sigma^2 = 3.4), so M' Gam(1/2) is about 0.026 at Delta = 0.05 and 0.007 at Delta = 0.025, against a margin
of order 0.1 (float P4: the next eigenvalue on the constrained space is 0.166 at 7/4). To be confirmed by the float
pre-pass per cell; if tight, halve the cell.

### 3.6 Lemma BR (the branch between two nodes). PROVED given the certified inputs of GREEN; to referee

**Node objects (exact functions, enclosed by GREEN).** At a node a let Sigma_a = (sigma_a, u_a) be any decaying
one-node solution in the tube. In reduced Schur variables Y = (a, W) = (r d, -r v / sqrt2) the equation L_a (d, v) = f
is -Y'' + Q Y = (r f1, -r f2 / sqrt2) with the symmetric Q of bracket.py at L = 0, level 0, delta = 0.
- Regular solutions: U (2 columns, Frobenius start at r0, PROOF Lemma 5.2 type bounds).
- Admissible at infinity: V_1 (a decays; from the tail lemma at R1, a-channel W-coupled as in tail.py with
  k^2 = abs(E)), V_2 (W -> constant, W' -> 0), and the inadmissible V_3 (W growing linearly, i.e. v -> a nonzero
  constant).
- **Match determinant.** D_a := det of the 4 x 4 matrix [U(r_x) | V_1(r_x), V_2(r_x)] (values and derivatives at a
  match radius r_x). D_a != 0 (interval) means there is no nonzero regular solution that is admissible at
  infinity with v(inf) = 0. It is certified by GREEN itself and does not rest on Corollary 4.6.
- tau^E_a := the unique solution of L_a tau = 0, regular, d decaying, v(inf) = 1 (exists and is unique because
  D_a != 0: solve [U | V_1, V_2] c = V_3 data). Write d_E(0) for its first component at r = 0.
- **Nondegeneracy in sigma0.** d_E(0) != 0, certified as an interval. This, not ker L+(0) = 0, is what allows the
  family to be parametrised by sigma0 (if d_E(0) = 0 the branch has a fold in sigma0). Then
  tau_a := tau^E_a / d_E(0) is the first variation with d(0) = 1.
- Solution operator G_a: for f in FF (below), G_a f := G^sa f - ((G^sa f)_1(0) / d_E(0)) tau^E_a, where G^sa f is the
  solution with v(inf) = 0 (kernel U(r) C V(t)^T for r < t and its transpose for r > t, C from the Wronskian-type
  pairing; evaluated in the dichotomy basis {growing regular, tau^E, V_1, V_2}, each marched along its stable
  direction; P12: one march takes about 1 s and keeps relative radius 1e-17 or better). G_a f is the unique solution
  y of L_a y = f, regular at 0, with y_1(0) = 0, y_1 -> 0, y_2 bounded.

**Spaces.** om(r) := 1 + (r/4)^2, s_u := 3.
- X: continuous pairs z = (d, v) on [0, inf) with d(0) = 0, norm max(sup abs(d) om, sup abs(v) / s_u).
- FF: continuous pairs f = (f1, f2), norm max(sup abs(f1) om, sup abs(f2) om^2). The weight om (not stronger) on f1
  is forced: products (u_a - u) y_1 tend to (E_a - E) y_1 at infinity, a constant times a function that is only
  O(1/om). The weight om^2 on f2 makes v - v(inf) = int_r^inf s^-2 int_0^s f2 x^2 dx ds converge (weight om alone
  gives a logarithmic divergence).
- On [R1, inf): the a-channel obeys the maximum principle with kappa1^2 = -u_a(R1) (abs(d) om <= sup abs(f1 + sigma_a v)
  om times a constant c_om / kappa1^2, c_om from om''/om <= 1/8); the v-channel is the explicit Coulomb kernel. On
  [0, r0]: Frobenius-Volterra bounds as in PROOF Lemma 4.3. These closed forms complete the kernel sums on
  [r0, R1].
- Certified node constant: G_a >= norm of G_a from FF to X.

**Predictor.** H_t := h00 Sigma_a + h01 Sigma_b + Delta (h10 tau_a + h11 tau_b), cubic Hermite in t
(h00 = 2t^3 - 3t^2 + 1, h01 = -2t^3 + 3t^2, h10 = t^3 - 2t^2 + t, h11 = t^3 - t^2). Its first component at r = 0 is
exactly sigma_a + t Delta. D_t := H_t - Sigma_a = h01 (Sigma_b - Sigma_a) + Delta (h10 tau_a + h11 tau_b).

**Residual, algebraic.** With N_a(d, v) := (3 sigma_a d^2 + d^3 - v d, -d^2) (so F(Sigma_a + z) = L_a z + N_a(z)),
F(Sigma_b) = 0, L_a tau_a = 0, L_b tau_b = 0:

    R_t := F(H_t) = -h01 N_a(Sigma_b - Sigma_a) - Delta h11 (L_b - L_a) tau_b + N_a(D_t),
    (L_b - L_a)(y) = ((3 sigma_b^2 - u_b - 3 sigma_a^2 + u_a) y_1 - (sigma_b - sigma_a) y_2, -2 (sigma_b - sigma_a) y_1).

No derivative of node data appears. R_t is a polynomial in t with coefficients in FF; R_0 = R_1 = 0 and
d/dt R_t = DF(H_t) dH_t/dt vanishes at t = 0 (L_a (Delta tau_a) = 0) and at t = 1 (L_b (Delta tau_b) = 0). So
R_t = t^2 (1 - t)^2 Q_t with Q_t a polynomial of degree <= 5 in t, and

    Y0(t) := norm(G_a R_t)_X <= t^2 (1 - t)^2 Y*,   Y* := sum over the t-coefficients of Q of norm(G_a Q_k)_X  (certified).

**Fixed-point map.** For z in X: F(H_t + z) = R_t + L_a z + B_t z + N_t(z) with multiplication operators
B_t z := ((3 (sigma_a + D_1)^2 - 3 sigma_a^2 - D_2) z_1 - D_1 z_2, -2 D_1 z_1) and
N_t(z) := (3 (sigma_a + D_1) z_1^2 + z_1^3 - z_2 z_1, -z_1^2) (D = D_t). Define T_t(z) := -G_a (R_t + B_t z + N_t(z)).
B_t z and N_t(z) lie in FF for z in X (every f1-term carries a factor O(1/om), every f2-term a factor O(1/om^2) or an
exponentially decaying D_1). A fixed point z of T_t is C^2, regular, and satisfies L_a z = -(R_t + B_t z + N_t(z)),
i.e. F(H_t + z) = 0 classically, with first component 0 at r = 0.
- Z1(t) >= norm(G_a B_t) from X to X: kernel sums with the certified coefficient profiles; Z1(0) = 0 and Z1 is
  bounded by t times a certified constant plus the second-order part.
- Z2(rho) >= Lipschitz constant of G_a N_t on the ball of radius rho, divided by rho: kernel sums with the profiles
  (6 abs(sigma_a + D_1) + 3 rho/om)/om + s_u, 1/om, 2/om.

**Theorem BR.** Suppose for all t in [0, 1] there is rho(t) >= 0 with
Y0(t) + Z1(t) rho + Z2(rho) rho^2 <= rho and Z1(t) + 2 Z2(rho) rho < 1 (it suffices that
Z1max < 1 and 4 Z2 Y* /16 < (1 - Z1max)^2, with rho(t) := 2 Y0(t) / (1 - Z1max)). Then:
1. T_t maps the closed ball of radius rho(t) into itself and is a contraction there (Banach); its fixed point z_t
   is unique in the ball and depends continuously on t (uniform contraction, T continuous in t).
2. Sigma(sigma0) := H_t + z_t solves (2.1), is regular, has sigma(0) = sigma0, and norm(Sigma(sigma0) - H_t)_X
   <= rho(t) <= 2 t^2 (1 - t)^2 Y* / (1 - Z1max), which vanishes at both ends.
3. z_0 = 0 and z_1 = 0, so the branch starts at Sigma_a and ends at Sigma_b.
4. Uniqueness in the tube: if Sigma_a' is another decaying solution in the tube of node a, z = Sigma_a' - Sigma_a
   is a fixed point of T_0 (R_0 = 0, B_0 = 0) of X-norm below the tube width; the contraction gives z = 0.
5. Decay and E < 0: u(sigma0)(R1) <= H_t,2(R1) + rho s_u < 0 (certified from the two tubes: about -1.9 to -2.8), and u
   is non-increasing (F1), so E(sigma0) <= u(sigma0)(R1) < 0; sigma = O(1/om) -> 0, and then PROOF Lemma 3.3 applies
   from any radius with u < 0 (a = r sigma is bounded and a'' = p a with p >= kappa^2 > 0), giving exponential decay.
6. One node. Let r* := m/abs(E) (u(r) <= E + m/r by (F3), so u < 0 and p = sigma^2 - u > 0 for r > r*). On
   (r*, inf) a bounded solution of a'' = p a with p > 0 has no zero: (a^2)'' = 2 a'^2 + 2 p a^2 >= 0, so a^2 is convex
   and bounded, hence non-increasing; a zero at r1 would force a = 0 on [r1, inf) and then a = 0 identically. Zeros
   of sigma are simple (PROOF Lemma 3.2 step 1), sigma(0) = sigma0 > 0, and with rbar := sup over t of r*
   (certified from the enclosures of m and E) sigma(sigma0)(rbar) != 0. The map t -> sigma(sigma0) is continuous in
   C^1[0, rbar] (continuity of z_t in X and the equation). So the number of zeros in (0, rbar) is constant in t; it
   is 1 at t = 0.
7. Outputs for CH: e_sig(r) := abs(H_t,1 - sigma_lin)(r) + rho(t)/om(r), e_u(r) := abs(H_t,2 - chord(u))(r) + rho(t) s_u,
   both t (1 - t) times certified profiles (H_t - chord = (h01 - t)(Sigma_b - Sigma_a) + Delta (h10 tau_a + h11 tau_b)
   and h01 - t, h10, h11 are divisible by t (1 - t)); gam_e from e_sig (norm of r e_sig on [0, R1] plus tails).

**Cross-grid evaluation.** Node b's functions are needed on node a's steps: one rigorous re-step (bg_step,
lin_step) from b's grid point below each radius; bookkeeping, no new mathematics.

**PROBE-MEASURED (P11b, float, finite differences, N = 1000, R = 20).**

| cell | max Y0 | Z1 at t = 1 | Z2 | max NK radius | true deviation at t = 1/2 (float solve) |
|---|---|---|---|---|---|
| [7/4, 9/5], Delta 0.05 | 5.1e-8 | 0.40 | 19.8 | 6.4e-8 | 3.4e-8 |
| [1597/1000, 1600/1000] | 5.4e-11 | 0.025 | 20.9 | 5.5e-11 | 2.2e-10 (float-solve noise level) |
| [1980/1000, 1983/1000] | 6.2e-11 | 0.023 | 18.5 | 6.2e-11 | not run |

Z1 uses node a's inverse over the whole cell; using the nearer node halves it. The float probe truncates at R = 20
and uses weight om on both forcing components; the certified version uses FF as defined above (the difference is
in the far tail and is exponentially small in the residual, but G_a must be recomputed in FF).

### 3.7 Assembly: what is needed at EVERY sigma0 of a cell, and how it is certified uniformly

| needed at sigma0 (for PROOF sections 6-7 and for KC, IDXC) | how it is certified for all t in [0, 1] |
|---|---|
| a decaying one-node solution with sigma(0) = sigma0 | BR items 2, 5, 6 |
| E(sigma0) < 0 (defines Omega, Lemma 6.1) | BR item 5: u(sigma0)(R1) < 0 from the two tubes and rho |
| V+-(sigma0) bounded, tending to their limits; nonlocal term Hilbert-Schmidt (Lemma 6.1) | holds for every decaying solution (PROOF 2.2, Lemma 4.1 with I1(sigma0) finite) |
| exact kernels (K1) L-(0) r sigma = 0 and (K2) L+(1) r sigma' = 0 at sigma0 | identities for any decaying solution of (2.1) (F4; translation), with exponential decay from BR item 5 |
| N0(L) finite for L = 0, 1, 2 (Lemma 6.1(b)) | CC upper with CPOSL margins: L+-(L; sigma0) > 0 on a subspace of codimension U+-(L) (2, 2, 1 and 2, 1, 1), kernel directions inside the excluded span |
| n(L-(0)) <= 1, n(L+(1)) <= 1, n(L-(1)) <= 1, n(L+-(2)) <= 1 | the same subspaces plus the kernel booking of Corollary 4.6 at sigma0 |
| n(L+(0) on (r sigma)^perp) <= 1 | CPOSL (d) with CC |
| K(L) <= 2 for L = 0, 1, 2 | the three lines above |
| L+-(3) > 0, hence L >= 3 by Lemma 7.1 at sigma0 | CC upper with k = 0: margins of L+-(3) at the two ends (R2: counts 0 up to shift 0.2, P2) minus eta2 |
| w2(t) < abs(E(sigma0)) and w1(t) >= 0 | chord(w2) <= 1.47 against abs(E) >= 2.5 from BR item 5 (certified inequality per cell) |
| N_L(w2(t)) <= k_L with margin, (k_0, k_1, k_2) = (3, 2, 1) | CC upper: CPOSL (c) at both ends on a common complement of k_L explicit vectors; needs chord(m) > eta2(t) for all t, checked as m_a + t (m_b - m_a) > t (1 - t) C_cell |
| N_L(w1(t)) >= k_L + 1 with margin | CC lower: Gram matrices of H_a(w1a), H_b(w1b) on k_L + 1 common explicit trial functions (node RITZ), minus eta2' |
| conclusion N_+ = 0 in sectors L <= 2, all M | IDXC with the robust form of KC |
| no spectrum off the axis for L >= 3; 3-D statement | PROOF Corollary 7.2 and Theorem 7.3 at sigma0 (N0 <= 23) |

Nothing in this list uses a Krawczyk certificate, an eigenvector or an interval-valued sigma0.

## Nodes

| id | claim | source | status | expected | depends | referee | lean |
|---|---|---|---|---|---|---|---|
| R1 | pointwise chain at any exact rational sigma0: B-EX, B-TAIL, brackets, D0, ESS, IDX, L >= 3 monotonicity, 3-D statement | proof/PROOF-R1-v2.md sections 3-7 | PROVED | - | - | referee-5 CORRECT; referee-7 transfer CORRECT WITH FIXES (text) | no |
| G9 | nine certified stable points with K = (2,2,2,0), Krein pairs (w-, w+) per L, tube sha per point | build-3/out/*/B.json, K0-K2.json | CERTIFIED | 9 | R1 | referee-7 CORRECT | no |
| I1 | h_w(x, y) = [(A - i w) x, y]; H(w) unitarily equivalent to L + i w J | section 2 | PROVED (to referee) | - | R1 | referee-W1 (inside KC) CORRECT | candidate |
| KC | local Krein index identity N(w1) - N(w2) = n(h_w1 on S) - n(h_w2 on S), n(h_w1 on S) = n(omega on S); classical in finite dimensions (Kollar-Bosak 1212.5691 Thm 4; Kollar-Miller 1209.3185), proof with essential spectrum written here | section 3.2 | PROVED (to referee) | - | I1, R1 | referee-W1 CORRECT WITH FIXES (step 5 now written; re-read needed) | no |
| IDXC | N_+ + 2 (N(w1) - N(w2)) <= K(L) | DESIGN-W1 section 3.3; section 3.3 | PROVED | - | KC, R1 | referee-W1 CORRECT | no |
| SHIFT | operator-norm transfer of counts (control only) | DESIGN-W1 section 3.4 | PROVED | - | R1 | referee-W1 CORRECT | candidate |
| CC | convexity cover: margins at both ends on a common subspace give the count inside | section 3.5 | PROVED | - | - | referee-W1 CORRECT | candidate |
| BR | branch lemma: continuous family of decaying one-node states between adjacent nodes, deviation from the Hermite predictor <= 2 t^2 (1-t)^2 Y* / (1 - Z1max); E < 0; one node; uniqueness in the node tubes | section 3.6 | PROVED (to referee) | - | R1 | NEW: referee (rewritten after referee-W1 GAP) | no |
| CH | chord inequalities with separate eta2 and eta2' | section 3.5 | PROVED (to referee) | - | BR | NEW: referee (rewritten after referee-W1 GAP) | candidate |
| CPOSL | endpoint margin lemma: 3-channel count, Haynsworth with k vectors, exterior block; penalised L = 0 count with each end's own g and the D0 exterior split | section 3.5 | PROVED (to referee) | - | R1, I1 | NEW: referee (written after referee-W1 SKETCH) | no |
| HW3 | instrument: certified 3-channel counts of H_L(w) with per-step re-basing, level in the a and d channels only, k forcing columns, Gram quadratures | design/probe/hw3.py (prototype, P10, P10c); build seat: window/build-4/hw3.py | GAP (prototype runs; build + audit this raid) | - | CPOSL | NEW: audit | no |
| GREEN | instrument: U, V_1..V_3, match determinant D_a != 0, tau^E, d_E(0) != 0, G_a in FF -> X, Y*, Z1, Z2, e_sig, e_u, gam_e per cell | build seat: window/build-4/green.py; cost prototype design/probe/p12_green_cost.py | GAP (not built; marches probed P12, float P5, P9, P11b) | [3, 25] | BR | NEW: audit | no |
| NODES | point tubes (B-EX, B-TAIL) at all nodes, bg_tube.py unchanged | build-3/bg_tube.py; run after seal | GAP (run after seal; 9 of 23 rebuild pinned shas) | 23 | R1, G9 | - | no |
| CK | every cell: the rows "N0 finite" to "L+-(3) > 0" of section 3.7 | CC + CPOSL + CH; run after seal | GAP (run after seal) | 2 | CC, CH, CPOSL, HW3, GREEN, NODES | - | no |
| CN2 | every cell, L = 0, 1, 2: N_L(w2(t)) <= (3, 2, 1) with margin | CC + CPOSL + CH; run after seal | GAP (run after seal) | [1, 3] | CC, CH, CPOSL, HW3, GREEN, NODES | - | no |
| CN1 | every cell, L = 0, 1, 2: N_L(w1(t)) >= (4, 3, 2) with margin | CC lower + CH; run after seal | GAP (run after seal) | [2, 4] | CC, CH, HW3, GREEN, NODES | - | no |
| XK | control: at the nine G9 nodes N_L drops by exactly 1 across each certified w- and rises by exactly 1 across each certified w+ (identity form of KC; pins the ordering near the edges) | HW3 against build-3/out/*/K*.json | GAP (run before the cells; must pass) | 1 | HW3, G9 | - | no |
| XU | must-fail controls (Failure modes item 2): cells containing a certified unstable point fail with "no drop" in the named sector while everything else closes; w-pair scan; BR content null | HW3 + GREEN + CC | GAP (run before the cells; must behave as stated) | 0 | HW3, GREEN, CC, G9 | - | no |
| W | spectral stability for every sigma0 in [1597/1000, 1983/1000] along the continuous family of BR | section 3.7 | GAP (target; closes when CK, CN1, CN2 hold on every cell) | - | R1, G9, IDXC, BR, CK, CN1, CN2, XK, XU | NEW: referee | no |

## Failure modes

1. **The 3-channel counter miscounts.** Control XK: at the nine certified nodes, for each L, lower count = upper
   count at w- - 0.002, w- + 0.002, w+ - 0.002, w+ + 0.002 (levels 1e-5), with a drop of exactly 1 across w- and a
   rise of exactly 1 across w+ (54 crossings; by the identity the rise certifies the positive-Krein partner
   independently of the R2 Krawczyk sign). At w = 0 the count must equal n(L+) + n(L-) from bracket.py. One
   mismatch voids the instrument.
2. **The certificate is vacuous.** Control XU, three parts, each logged with the failing step:
   (a) cells [1595/1000, 1597/1000] and [1983/1000, 1985/1000] (nodes at certified unstable points): BR, CK and the
   other two sectors must CLOSE, and the failure must be exactly "no count drop" in L = 0 (resp. L = 2). Any other
   failing step makes the control VOID, not passed.
   (b) at the node 1595/1000 (and 1985/1000) a scan of frequency pairs on a grid of step 0.01 in (0, abs(E) - m/R -
   delta): no pair with lower count N(w1) minus upper count N(w2) >= 1 in the named sector (the certified quartet
   leaves nothing on the axis there); the other sectors must show their drop.
   (c) BR content null: run the cell [7/4, 9/5] with node b's tube replaced by the tube of 37/20 (wrong pairing,
   labelled as 9/5). The Hermite predictor is then wrong by about 0.05 tau, the residual does not vanish at t = 1,
   and the NK condition must FAIL. A pass voids GREEN.
3. **BR constants wrong or optimistic.** Controls: (a) d_E(0) and tau against finite differences of certified
   node tubes (float P5, P11b: du0/dsigma0 3.424 against 3.470 centred); (b) leave-one-out: predictor of the cell
   [7/4, 37/20] evaluated at 9/5 against the certified R1 tube, difference inside rho(1/2); (c) float P11b values of
   Y0, Z1, Z2 are sealed as expectations (order of magnitude) for the certified ones.
4. **Margins vanish near the edges** (float: 7.3e-5 to 1e-4 at 1597/1000, L = 0; 2.2e-4 at 1983/1000, L = 2).
   Rules: end cells use R = 20 (delta_0(20) = 6.5e-7, P10c), margin levels of order 1e-5, the common subspace taken
   from the END node's own negative eigenvectors (P8 showed the averaged choice loses the sign there); the test is
   m_a + t (m_b - m_a) > t (1 - t) C_cell for all t in [0, 1], decided exactly as the positivity of a quadratic in t
   with certified coefficients. If a cell does not close it is bisected (depth <= 4); if it still fails, the theorem is stated
   for the largest union of closed cells and the failing cell is reported (SCOPE's second outcome).
5. **A level leaks into the auxiliary W channel** (P1). Rule and assert: m, eta in the a and d channels only; the
   W-channel level is 0. Control: P1 against P2 reproduced by the built instrument.
6. **Exterior block not positive** (needs abs(E) - m_bg/R - delta - abs(w) - m > 0; fails at R = 10 for L = 0).
   Assert; R >= 14 for L = 0. Control: counts agree at R = 14 and R = 20.
7. **Penalty and kernel handling at L = 0, 1** (M' Gam against the margin; kernel directions in the excluded
   span). Control C6: on two mid-window cells of half-width 0.005 recompute K(L) by SHIFT alone; same K required.
   The float pre-pass reports M'' abs(d2), s_PP - M'' s_PG^2/(1 + M'' d2) and M' Gam per cell before the seal.
8. **Run pathologies.** Without re-basing a count ran past 100 s (P10). Rule: per-step re-basing, a hard
   watchdog per count; an unfinished count is INCONCLUSIVE and is never retried silently.

## 6. Schedule and cost (details and the doctrine #33 pass: SPEEDUP-W1.md)

Nodes (23; G9 points in bold): **1597/1000**, 1600/1000, 1605/1000, 1612/1000, 1625/1000, **33/20**, 1675/1000,
**17/10**, 1725/1000, **7/4**, 1775/1000, **9/5**, 1825/1000, **37/20**, 1875/1000, **19/10**, 1925/1000, **39/20**,
1962/1000, 1970/1000, 1976/1000, 1980/1000, **1983/1000**. Cells: 22, widths 0.003 to 0.025.
PROBE-MEASURED support: the 0.05 cell [7/4, 9/5] closes in float with a factor 4 (max eta2 7.0e-3 against chord
margins 0.026 to 0.035; eta2' 9.5e-3 against 0.052), so the 0.025 cells have a factor of about 16; the end cells
close with factors above 10 (section 7).
Unit costs: tube 51 to 63 s (measured); GREEN marches 2.1 s for two (measured), ESTIMATE 20 s per node with
kernel sums and tau; brackets 25 s (measured); hw3 counts 1.2 to 2.2 s each (measured, prototype); CPOS and RITZ
ESTIMATE 6 s per sector and end.
Projection: nodes 23 x (63 + 20 + 25) s = 41 min; cells 22 x (2 ends x 4 sectors x about 8 s + 20 s BR sums) =
31 min; controls 15 min. About 1.5 lane-hours, under 1 h wall on two lanes; with a factor 2 contingency under 2 h
wall. Every job under 5 minutes.

Stages: 0 (before the seal) referee on sections 3.2, 3.5, 3.6; build and audit hw3 and green; XK and XU;
float pre-pass per cell. A: [33/20, 39/20]. B: the two end zones. Fallback: largest closed union.

## 7. The referee's next strike (float, PROBES P11): can the end cells close?

| cell | sector | margin at end a | margin at end b (common subspace from the end node) | max eta2 (t = 1/2) | worst ratio margin / eta2 over t | lower side: Ritz values, eta2' |
|---|---|---|---|---|---|---|
| [7/4, 9/5] | L = 0 | 0.0256 | 0.0351 | 7.0e-3 | 4.3 | -0.052 / -0.056, 9.5e-3 |
| [7/4, 9/5] | L = 1 | 0.082 | 0.084 | 4.0e-3 | 21 | -0.043 / -0.044, 3.6e-3 |
| [7/4, 9/5] | L = 2 | 0.046 | 0.037 | 3.4e-3 | 12 | -0.18 / -0.20, 2.4e-3 |
| [1597/1000, 1600/1000] | L = 0 | 7.8e-5 | 5.3e-4 (w2 = 1.0177) | 2.6e-5 | above 10 (12 at t = 1/2) | -0.029 / -0.030, 3.5e-5 |
| [1980/1000, 1983/1000] | L = 2 | 8.8e-4 (w2 = 0.4624) | 2.2e-4 | 1.2e-5 | above 40 | -0.29 / -0.29, 8.8e-6 |

So in float both end cells close and the largest closable window is the full target [1597/1000, 1983/1000]; no
end node has to move inward. The binding number is the certified margin at the two end nodes themselves (float
7.3e-5 to 1e-4 and 2.2e-4; the prototype counter certifies positivity there at level 1e-5, P10c). If CPOSL at an
end node cannot certify a margin above the chord loss slope (about 1e-4 per unit t on the first cell), the first
cell is shortened (eta2 scales with Delta^2) before any inward move is considered.

## 8. Risks and open questions

1. GREEN's certified G_a in the space FF (weight om^2) is not probed; the float G = 15.2 (P5) and Z2 about 20 were
   computed with weight om on a finite interval. BR has a factor of about 1e5 of room in Y0 on a 0.05 cell, so even
   a much larger G_a closes; Z1 (0.40 at Delta = 0.05 from one node) is the sensitive constant: use the nearer node
   and cells <= 0.025.
2. CPOSL (d): M' Gam against the L = 0 constrained margin is an ESTIMATE; the pre-pass decides per cell.
3. The constrained endpoint certificate at the end nodes needs explicit vectors p accurate enough that the loss
   (about abs(lambda_neg) times the squared error of p) stays below 1e-5: p accurate to 1e-3 suffices.
4. KC step 5 and sections 3.5, 3.6 are new text and need a referee pass; KC, IDXC, CC themselves were found correct.
5. The sources of the gate note W2-KC (Kollar-Bosak, Binding-Browne) were not opened by this seat; citations follow
   the lead's relay and referee-W1.
6. UNTESTED curiosity kept from W1 (referee-W1: 0 violations in 4000 finite-dimensional trials, still unproved in
   this setting): N_+ <= N(wa) + N(wb) - N(w) for wa < w < wb. Not used.

## 9. Credits for method

Graphical Krein signature and its index identities: Kollar-Miller (arXiv 1209.3185), Kollar-Bosak (arXiv
1212.5691), Binding-Browne (1988). Krein-form non-degeneracy on finite systems: Kollar-Pego (arXiv 1103.0157,
Lemma 1). Grid of certified points plus perturbation: Hoang-Plum-Wieners (ZAMP 60, 2009). Stability on a whole
parameter interval by interval arithmetic: Barker (arXiv 1401.5371); Breden-Payan-Reisch-Tang (arXiv 2504.05066).
Box cover with negative controls: Braz e Silva (Zenodo 10.5281/zenodo.23772125). Warning on naive interval
parameters: Barker-Zumbrun (arXiv 1601.00837, Remark 1.2).
