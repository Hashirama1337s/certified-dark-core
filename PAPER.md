# A linearly stable excited dark-matter core, proved at nine points: certified spectral stability of the one-node Gross-Pitaevskii-Poisson state, and certified brackets of its stability-band edges

**Moki & Julio** (AI-assisted)

Version 1.0, 2026. Every number below is traced to a file of this repository in `NUMBERS.md`, and
`tools/check_numbers.py` checks each one. Certified numbers are outward-rounded balls `[mid +/- rad]` from ball
arithmetic; numbers marked **float** are double-precision values checked only by changing the resolution.

---

> **The magic trick.** A computer that only does arithmetic it can prove counts every way a one-shell dark-matter
> ball could lose energy. It finds at most two in each shape class. Then it finds, in each of the three shape classes
> that have any, a wobble that provably carries negative energy, and a negative-energy wobble uses up exactly two of
> those directions. Nothing is left over for a growing mode. So no small shake of any shape can grow exponentially.

> **In plain words**
>
> If dark matter is an ultralight particle, it can settle into a ball that its own gravity holds together, with a weak
> push between the particles. Such balls are discussed as the dense cores at the centres of dark-matter halos. The
> lowest-energy ball is well understood. The next one up has a single hollow shell inside it: the field changes sign
> once on the way out. Shelled balls of this kind are usually unstable.
>
> In 2024 Chávez Nambo, Diez-Tejedor, Roque and Sarbach (arXiv:2402.07998) computed, with careful numerics, that for
> a narrow window of central densities the one-shell ball survives every small shake. To our knowledge (search of arXiv to 16 November,
> INSPIRE and Zenodo to 17-18 November 2026), nobody had proved it at any point of that window.
>
> **What we proved.** At central amplitude σ0 = 9/5 exactly, no small disturbance of any shape grows exponentially
> in time. The proof is computer-assisted: every number the computer uses carries a guaranteed error bar. The same
> certificate then holds at eight more points spread across the window, from 1.597 to 1.983.
>
> **What we mapped.** With ordinary (float) numerics, bisected on a refined grid and checked against a coarser one, the
> window is
> [1.5963117, 1.9841288]. That is a little narrower than the published 1.55 to 2.07. At each edge, two wobbles of
> opposite energy sign meet and turn into a growing pair: a **Krein collision**. Certified runs then pinned both edges:
> the state is proved unstable at 1.595 and stable at 1.597, stable at 1.983 and unstable at 1.985. It is also proved
> unstable at 1.55 and at 2.00, two points inside the published range.
>
> **What we did not prove.** Nothing about large shakes, long-time nonlinear behaviour, the points between the
> certified ones (there the window is a float result), or whether real galaxies contain such cores.

---

## Abstract

We study the Gross-Pitaevskii-Poisson (GPP) system, a nonrelativistic model of a self-gravitating condensate of
ultralight bosons with a repulsive quartic self-interaction, in the dimensionless units of arXiv:2402.07998. Its first
excited (one-node) spherical stationary state was reported there, from numerics, to be linearly stable for central
amplitudes 1.55 ≲ σ0 ≲ 2.07.

**Result A (certified; internally refereed; blind float replication).** At σ0 = 9/5 exactly, for every decaying one-node solution whose
central potential lies in an explicit interval of width 2·0.99·10⁻⁵⁰, the linearised operator J L on L²(R³; C²) has
no spectrum with Re λ > 0; its spectrum lies on the imaginary axis. The proof combines (i) a certified enclosure of
the background, with an existence argument; (ii) certified upper and lower brackets of the Morse indices of the
self-adjoint operators L+ (which contains the nonlocal Poisson term) and L− in every angular sector, which give the exact
indices n(L+) = (2, 1, 1, 0) and n(L−) = (1, 1, 1, 0) for L = 0..3; (iii) a constrained count at L = 0; (iv)
Krawczyk-certified purely imaginary eigenvalues of negative Krein signature at L = 0, 1, 2; (v) a direct Hamiltonian
index inequality, N₊ + 2 ≤ n(L|Y) ≤ 2, which forces N₊ = 0 in those sectors; and (vi) a monotonicity argument for
every L ≥ 3 and an assembly in three dimensions. All six negative- and positive-Krein frequencies were reproduced to
ten digits by a blind float computation that saw only the paper (sealed pass rule: relative 1e-4; the ten-digit agreement is a POST HOC observation).

**Result B (float map, certified grid and certified edge brackets) (certified; sealed; one internal referee).** A double-precision continuation in σ0 over L = 0..14 gives the
common stability band [1.5963117, 1.9841288] (edges bracketed to ±1·10⁻⁷ on the refined grid; base and refined grids agree to 3·10⁻⁷). Both edges are Krein collisions: the
L = 0 negative-Krein mode at the lower edge and the L = 2 one at the upper edge meet a positive-Krein partner and leave
the axis as a complex quartet, with the Morse indices unchanged. The sectors (L = 0 below, L = 2 above) agree with
Fig. 8 of arXiv:2402.07998. A sealed certified test (twelve points, all HOLD) proves linear stability at
1597/1000, 33/20, 17/10, 7/4, 37/20, 19/10, 39/20 and 1983/1000, and linear instability (a certified growing quartet)
at 1595/1000 and 31/20 (L = 0) and at 2 and 1985/1000 (L = 2). The float edges therefore lie in certified brackets
[1.595, 1.597] and [1.983, 1.985]. Stability between the certified points is not claimed. The points 31/20 = 1.55 and 2
lie inside the published range 1.55 ≲ σ0 ≲ 2.07.

---

## 1. Results

Throughout: repulsive sign s = +1, coupling α = 1 of (43b) in arXiv:2402.07998, one node (n = 1), the paper's
dimensionless units.

**Theorem A (spectral stability at σ0 = 9/5).** Let u_mid be the 60-digit number recorded in
`data/r1/target_bg_tube.json` and U0' = [u_mid − 0.99·10⁻⁵⁰, u_mid + 0.99·10⁻⁵⁰]. Take any regular solution (σ, u) of
the radial system (2.1) with σ(0) = 9/5, u(0) ∈ U0', that decays at infinity and has exactly one zero. At least one
such solution exists. Let A = J L be its linearisation (2.3) on L²(R³; C²). Then σ(A) ⊂ iR; in particular A has no
eigenvalue with Re λ > 0.

**By-product (exact indices).** n(L+(L)) = 2, 1, 1, 0 and n(L−(L)) = 1, 1, 1, 0 for L = 0, 1, 2, 3, and both are 0 for
every L ≥ 3. ker L−(0) = span(rσ) and ker L+(1) = span(rσ′); every other sector kernel is trivial.

**The certified state.**

| quantity | certified value |
|---|---|
| E (chemical potential) | [-3.10544025447 +/- 3.02e-12] |
| m = ∫σ²r²dr | [19.1587125456 +/- 4.04e-11] |
| N = 4πm | [240.755482341 +/- 4.75e-10] |
| zeros of σ on [0, 26] | 1 (node near r = 2.7853521306, float) |
| tube sha256 | f8b0cc27d5885a45af4b7356a1e3f6f2e0e1445510e32842cf4710f9ecfce28b |

**The three negative-energy wobbles** (λ = i w, Krawczyk boxes; Krein sign decided in ball arithmetic):

| L | w, negative Krein | ⟨a, d⟩ | w, positive-Krein control |
|---|---|---|---|
| 0 | [1.10491108047488 +/- 4.15e-15] | -3.061281342e-6 +/- 4.63e-13 | [1.25921337137566 +/- 6.39e-15] |
| 1 | [0.539925668013455 +/- 2.97e-16] | -6.212149350e-5 +/- 1.10e-13 | [0.951028237700108 +/- 2.59e-16] |
| 2 | [0.2968148506 +/- 6.42e-11] | -0.0002403151062 +/- 1.86e-07 | [0.5179458643 +/- 7.13e-11] |

**Result B.** Float common stability band [1.5963117, 1.9841288]; lower edge set by L = 0, upper edge by L = 2;
both edges are Krein collisions (float, Section 7). Certified (Section 7.4): stable at nine points including 9/5;
unstable at 1595/1000, 31/20, 2 and 1985/1000; edges bracketed in [1.595, 1.597] and [1.983, 1.985].

---

## 2. Setup

### 2.1 The model (arXiv:2402.07998, eqs. (9)-(17), (32)-(33))

The dimensionless GPP system is i∂ₜψ = H(ψ)ψ with H(ψ) = −Δ + s|ψ|² + Δ⁻¹(|ψ|²), with s = +1 (repulsive
self-interaction), where Δ⁻¹f(x) = −(1/4π)∫f(y)/|x − y| dy. Stationary states ψ = e^{−iEt}σ(x) satisfy Eσ = H(σ)σ. For
radial σ and u := E − U (U = Δ⁻¹σ² the gravitational potential), (32a)-(32b) read

(2.1)  σ″ + 2σ′/r = (sσ² − u)σ,   u″ + 2u′/r = −σ²,   σ(0) = σ0, σ′(0) = 0, u(0) = u0, u′(0) = 0,

with E = u0 − ∫₀^∞σ²r dr (33). Elementary facts used throughout, with m(r) = ∫₀^r σ²t²dt and a := rσ:
r²u′ = −m(r) ≤ 0; u(r) − E = ∫_r^∞ m(t)/t² dt ∈ [0, m/r]; a″ = (sσ² − u)a.

### 2.2 Linearisation

The perturbation ansatz (18), (21) of arXiv:2402.07998 gives, after re-derivation (independently checked by two
internal referees), with C := −iB,

(2.2)  L− = −Δ + sσ² − u,   L+ = −Δ + 3sσ² − u + 2σΔ⁻¹(σ ·),

(2.3)  λ(A, C) = J L (A, C),   J = [[0, 1], [−1, 0]],   L = diag(L+, L−).

L+ contains the nonlocal Poisson term. On λ = iw with C = iD: L+A = wD and L−D = wA.

### 2.3 Sectors

Spherical harmonics (eqs. (34)-(37), (43)) reduce J L to a direct sum over (L, M) of radial operators on
X = L²(0, ∞) (reduced functions a = r·A_LM, Dirichlet at 0), each repeated 2L + 1 times:

(2.4)  L−(L) = −d² + ℓ/r² + sσ² − u,   L+(L) = −d² + ℓ/r² + 3sσ² − u + 2σG_Lσ,   ℓ = L(L + 1),

with G_L = −P_L⁻¹, P_L = −d² + ℓ/r², whose kernel is −(2L + 1)⁻¹ r_<^{L+1} r_>^{−L}. Writing L± = H0 + V± with
H0 = −d² + ℓ/r² − E ≥ |E| > 0, all of V± is bounded (the nonlocal part is Hilbert-Schmidt), so L± are self-adjoint on
D(H0). Two kernels are explicit: L−(0)(rσ) = 0 (phase) and L+(1)(rσ′) = 0 (translation).

---

## 3. Strategy

The question "does any small disturbance grow?" is a question about the non-self-adjoint operator J L. For a
Hamiltonian operator of this form, eigenvalues off the imaginary axis, and imaginary eigenvalues of negative Krein
signature, both consume negative directions of the self-adjoint operator L. We use one inequality of that kind,
proved directly in Section 4.5 (no parity theorem, no simplicity assumption):

  N₊ + 2 ≤ n(L | Y_L)   whenever a negative-Krein imaginary eigenvalue exists in the sector,

where N₊ counts eigenvalues with Re λ > 0 (with multiplicity) and n(L | Y_L) is the number of negative directions of L
on a constraint space (the phase direction is removed at L = 0). The proof therefore needs, per sector:

1. a certified **upper** count n(L | Y_L) ≤ K(L) = 2 for L = 0, 1, 2 (Sections 4.2-4.3);
2. a certified **negative-Krein eigenvalue** i w, 0 < w < |E|, for L = 0, 1, 2 (Section 4.4);
3. L±(L) ≥ ε > 0 for L ≥ 3 (Section 4.6), so those sectors have nothing to give;
4. the functional analysis that makes "eigenvalue" the only thing that can sit off the axis, and the step from
   sectors to three dimensions (Sections 4.5-4.6).

The full proof, with every lemma written out and every code fact it relies on, is
[proof/PROOF-R1-v2.md](proof/PROOF-R1-v2.md) (about 1,300 lines), shipped as the referees read it: its header line
"blind replication pending" predates the blind result (HOLD, Section 6). This section and the next condense it
faithfully; lemma numbers below are those of the proof file. In the proof, build-2/<file> is code/r1/<file> (line
numbers unchanged) and build-2/out/ is data/r1/.

---

## 4. Proof structure

### 4.1 The background (Lemmas 3.1-3.3)

**Lemma 3.1 (start, r0 = the binary64 number nearest 10⁻⁵).** For u0 ∈ U0 the regular solution exists and is unique on
[0, r0], with |σ − σ0| ≤ F r²/6 and |u − u0| ≤ sg² r²/6 (sg = 9/5 + 1/100, F = (sg² + |u0| + 1/100)sg).
*Proof:* the Volterra map V[g](r) = ∫₀^r t⁻²∫₀^t x²g dx dt is a contraction on C[0, r0] (constant < 1/2); a bootstrap
keeps σ and u within 1/100 of their centre values, far above the actual variation (below 2.5·10⁻¹⁰).

**Lemma 3.2 (existence inside the tube, s ≥ 0).** Let Esc be the set of u0 whose solution "escapes" (exactly one zero,
then u < 0 with a and a′ of one strict sign at some radius), and Z the set with at least two zeros. Both are open and
disjoint, and every escaping solution is unbounded. If the ends of an interval lie in Esc and Z respectively, some u0*
in between lies in neither, and its solution is global, decaying and has exactly one zero.
*Proof:* zeros are simple, so zero counts are locally constant in u0; escape is permanent because u ≤ u(r*) < 0 forces
a″ < 0 while a < 0; connectedness gives u0*; the certified tube then shows exactly one zero on [0, 26] with a(26) < 0
and u(26) < 0 uniformly over U0, so u0* has bounded a, a′ and the solution is global.
*Certified inputs:* lower end of U0 classified `escape`, upper end `zeros` (two zeros); existence certified; one zero on
[0, 26].

**Lemma 3.3 (tail).** For r ≥ R1 = 26, with κ1 = √(−u(26)) and a1 = |a(26)|:
|a(r)| ≤ a1 e^{−κ1(r − 26)}, |a′| ≤ (V_max/κ1)|a|, and the tails of m, I1 and E are enclosed.
*Proof:* b = −a satisfies b″ ≥ κ1² b and b′ ≤ 0; g = b′ + κ1 b obeys g′ ≥ κ1 g and is bounded, hence g ≤ 0.
*Certified:* κ1 = [1.53901484561 +/- 4.69e-12], a1 = [7.75859535966e-12 +/- 3.43e-24], u(26) = [-2.36856669502 +/- 2.38e-12],
so E < 0.

### 4.2 Certified counts (Lemmas 4.1-4.4, Theorem 4.5, Corollary 4.6)

**Lemma 4.1 (the nonlocal term, Hilbert-Schmidt).** With σ_i = σ·1_[0,R] and I_in(R) = ∫₀^R σ²r,
‖σP_L⁻¹σ − σ_iP_L⁻¹σ_i‖_HS ≤ √(I1² − I_in(R)²)/(2L + 1). So cutting the Poisson coupling at R costs at most
δ_L(R) = 2√(I1² − I_in²)/(2L + 1) in form sense. *Proof:* r_<^{L+1}r_>^{−L} ≤ √(rt).
Certified example: δ_0(10) = [0.0881154 +/- 4.45e-8].

**Lemma 4.2 (Schur complement in form sense).** For g = σa,
min over w of { P_L[w] + 2√2⟨g, w⟩ } = −2⟨g, P_L⁻¹g⟩, attained at w* = −√2 P_L⁻¹g. Hence the nonlocal form q+ is the
minimum over an auxiliary field w of a **local** 2×2 Sturm form in Y = (a, w), with potential matrix
[[ℓ/r² + 3sσ² − u − δ, √2σ], [√2σ, ℓ/r²]]. This turns the count for the nonlocal L+ into a count for a local matrix
Sturm-Liouville problem.

**Lemma 4.3 (left end).** On [0, r0] the regular matrix solution Φ = r^{L+1}Z satisfies ‖Z − I‖ ≤ c/(1 − c) with
c = r0²q/(2(2L + 3)) < 1/4; the Dirichlet-to-Neumann matrix at r0 is symmetric with spectrum in (L + 1)/r0 ± η, and a
Picone identity gives the sandwich used for the upper (U_lo) and lower (U_hi) counts.

**Lemma 4.4 (counting on [r0, R]).** For the form b[Y] = ∫(|Y′|² + Yᵀ(Q − λ)Y) + boundary terms,
n(b) = Σ_{ρ ∈ (r0, R)} dim ker Φ(ρ) + n₋((U(R) + S)|_F), with U(R) = Φ′(R)Φ(R)⁻¹. *Proof:* b-orthogonal
decomposition into the Dirichlet part and the span of solutions; the Dirichlet part by the Morse index theorem
(branch monotonicity in the endpoint). The code certifies each conjugate point as a simple zero of det Φ (sign change
plus nonvanishing derivative on a sub-interval) and the 2×2 endpoint inertia from det and trace.

**Theorem 4.5 (brackets).** With ε = 1/1000 and R ∈ {10, 14}: if the exterior margin |E| − m/R − δ_L(R) − ε > 0, then
#(L+(L) < ε) is at most the certified interior count U+ (Robin U_lo, a-shift −δ); and #(L+(L) < −ε) is at least the
count of the Dirichlet-a problem without shift (Robin U_hi). The same for L− without the w-channel.
*Proof of the upper bound:* a negative subspace of q+ − ε is mapped, through w*(a) and the cut of Lemma 4.1, injectively
into a negative subspace of the interior form; the exterior parts are nonnegative because of the margin.

Certified counts (identical at R = 10 and R = 14):

| L | upper #(L+ < ε) | lower #(L+ < −ε) | upper #(L− < ε) | lower #(L− < −ε) | exterior margin (R = 10) |
|---|---|---|---|---|---|
| 0 | 2 | 2 | 2 | 1 | [1.10045 +/- 3.65e-6] |
| 1 | 2 | 1 | 1 | 1 | [1.15920 +/- 2.79e-6] |
| 2 | 1 | 1 | 1 | 1 | [1.17095 +/- 4.08e-6] |
| 3 | 0 | 0 | 0 | 0 | [1.17598 +/- 1.10e-6] |

**Corollary 4.6 (kernel booking, exact indices).** The explicit kernel rσ is q−-orthogonal to the negative spectral
subspace of L−(0), so n(L−(0)) + 1 ≤ 2; likewise n(L+(1)) + 1 ≤ 2. With the lower counts, every upper count equals its
lower count once the kernels are booked: the exact indices of Section 1.

### 4.3 The constraint at L = 0 (Theorem 4.7)

**Theorem 4.7.** n(L+(0) restricted to (rσ)^⊥) ≤ n(B) − 1 = 1, where B is the interior 2×2 operator at level 0.
*Proof:* the constraint ⟨f, rσ⟩ = 0 moves, by Cauchy-Schwarz, onto the interior with weight M; then a direct
Haynsworth inertia argument gives n(P) = n(B) − 1 once d2 = ⟨B⁻¹G, G⟩ < 0 and M|d2| > 1.
Certified: n(B) = 2 at both radii; d2 = [-2.041380387 +/- 3.15e-10] (R = 10) and [-2.172289605 +/- 1.42e-10] (R = 14);
M|d2| = [1133.8 +/- 0.0894] and [4.775e+7 +/- 6.25e+3].

**K(L).** n(L | Y_0) ≤ [n(B) − 1] + [U−(0) − 1] = 2; n(L | Y_1) ≤ [U+(1) − 1] + U−(1) = 2; n(L | Y_2) ≤ U+(2) + U−(2) = 2;
K(3) = 0. So **K = (2, 2, 2, 0)**.

### 4.4 The negative-Krein eigenvalues (Lemmas 5.1-5.10)

For real w the eigenvalue problem is a 3-channel ODE system for (P, Q, ψ) = (a + d, a − d, Poisson field). An eigenvalue
i w is certified by matching a 3-dimensional regular subspace at 0 to a 3-dimensional decaying subspace at infinity at
r_m = 8, with a Krawczyk test on (w, v).

- **Lemma 5.1 (matched solution ⇒ eigenvector).** A real nonzero solution that is regular at 0 and decays (P, Q) with
  bounded ψ gives an eigenvector ξ = (a, i d) of A_L with eigenvalue i w: the auxiliary field is forced to equal
  G_L(σa) because the difference is harmonic, vanishes at 0 and is bounded.
- **Lemma 5.2 (Frobenius start).** Second-order Frobenius data at r0 with explicit remainders; the code's constants
  exceed the true ones by a factor of about 3.1 to 3.6 (checked in ball arithmetic, `checks/check_frob_slack.log`).
- **Lemmas 5.3-5.7 (the decaying basis on [26, ∞)).** A far-field Riccati series to order 10 with a contraction for
  the residual; an inward certified Riccati integration to r = 26; a contraction (constant θ < 1/2) for the coupled
  bounded solutions in an exponentially weighted norm; renormalisation so that every uncertainty multiplies only
  decaying directions; and Cauchy bounds on a complex disc for the w-derivative.
- **Lemma 5.9 (Krawczyk).** If K(X) ⊂ int(X), the matching determinant has a zero (w*, v*) in X, which by Lemma 5.1
  is an eigenvalue i w* with 0 < w* < |E|.
- **Lemma 5.10 (Krein sign).** ⟨Lξ, ξ⟩ = 2w*⟨a, d⟩. The sign of ⟨a, d⟩ = (1/4)∫(P² − Q²) is certified on four intervals
  (a crude bound on [0, r0], Gram quadratures on [r0, 8] and [8, 26], and the tail bound of the contraction beyond 26).

Certified values: the table in Section 1. Tail bound at L = 0: 2.44e-20; contraction constant θ = 3.69e-12.

### 4.5 Essential spectrum and the index inequality (Lemma 6.1, Theorem 6.2)

**Lemma 6.1.** On Ω = C ∖ (i(−∞, −|E|] ∪ i[|E|, ∞)), A − λ = (I + K(λ))(A0 − λ) with K(λ) compact and analytic. The
eigenvectors with Re λ > 0 span an L-isotropic space, so their number is bounded by the (finite, certified) number of
nonpositive directions of L; this supplies one resolvent point, and the analytic Fredholm theorem then shows that every
spectral point off the imaginary axis is an isolated eigenvalue with a finite-rank Riesz projection. This holds per
sector and in three dimensions.

**Theorem 6.2 (index inequality).** In a sector, let N₊ be the total algebraic multiplicity of eigenvalues with
Re λ > 0, and ξ an eigenvector for i w (w > 0) with ⟨Lξ, ξ⟩ < 0. Then N₊ + 2 ≤ n(L | Y_L).
*Proof:* (i) root spaces with λ ≠ 0 lie in the constraint space (the phase direction is annihilated); (ii) the Riesz
projections satisfy ω(P_λx, y) = ω(x, P_{−λ̄}y), so the unstable and stable root spaces E₊, E₋ are ω-isotropic and
paired nondegenerately, which yields a negative definite subspace of dimension N₊ in E₊ + E₋; (iii) span(ξ, ξ̄) is a
negative definite 2-plane ω-orthogonal to it. Their sum is negative definite of dimension N₊ + 2.

**Application.** At L = 0, 1, 2: N₊ + 2 ≤ K(L) = 2, so **N₊ = 0**.

### 4.6 All other sectors and three dimensions (Lemma 7.1, Corollary 7.2, Theorem 7.3)

**Lemma 7.1 (monotonicity in L, nonlocal term included).** q+_{L+1}(f) ≥ q+_L(f) + 2(L + 1)∫f²/r², and the same for q−.
For L+ this uses the variational formula of Lemma 4.2: P_{L+1} ≥ P_L implies ⟨g, P_{L+1}⁻¹g⟩ ≤ ⟨g, P_L⁻¹g⟩.

**Corollary 7.2.** L±(3) ≥ ε, hence L±(L) ≥ ε for all L ≥ 3, and an eigenvector with Re λ ≠ 0 would have ⟨Lx, x⟩ = 0:
impossible. **Theorem 7.3.** The sector projections commute with A (the background is radial), so a three-dimensional
eigenvalue with Re λ > 0 would give a sector eigenvalue, contradicting the above; and σ(A) = −conj σ(A) rules out
Re λ < 0. Hence σ(A) ⊂ iR.

### 4.7 What the proof rests on

- **Code facts.** Eleven properties of the instruments (proof, Section 10), audited operation by operation by an
  engine-audit seat (Taylor and tail engines, with closed-form tests and deliberately broken controls that fail) and by
  an internal referee (counting, Krawczyk, Krein Gram and tail, matching). Four latent defects off the target path
  were found; they change no number and are fixed in the R2 instruments (`code/r2/`).
- **Standard results used without opening a source** (listed in the proof, GAP B2): domain monotonicity of Dirichlet
  eigenvalues of 2×2 Sturm systems, relative compactness of decaying potentials, the analytic Fredholm theorem, the
  Krawczyk theorem, min-max, Banach's fixed point and continuous dependence, H² regularity, the multipole expansion.
- **Ball arithmetic** (Arb through python-flint 0.9.0) is trusted. No step is checked in a proof assistant.

---

## 5. Certified values

All from `data/r1/` (seal 07faff6621, amended 6ad54f5713), one background tube for all four outputs.

| quantity | value | file |
|---|---|---|
| u_mid | 3.93902357537910961270976242947912892526530674750036020337021 | target_bg_tube.json |
| E | [-3.10544025447 +/- 3.02e-12] | target-B.json `B.E` |
| m | [19.1587125456 +/- 4.04e-11] | `B.m` |
| I1 | [7.04446382985 +/- 3.92e-12] | `B.I1` |
| κ1 | [1.53901484561 +/- 4.69e-12] | `B.kappa1` |
| a1 | [7.75859535966e-12 +/- 3.43e-24] | `B.a1` |
| D1 = 3m/4 | [14.3690344092 +/- 3.03e-11] | `D1` |
| relative virial residual | [+/- 8.21e-16] | `B.virial_rel` (consistency only) |
| K | (2, 2, 2, 0) | target_verdict.json |
| verdict | HOLDS | target_verdict.json |

The Krein table is in Section 1. Counts and D0 are in Sections 4.2-4.3.

---

## 6. Controls and verification

**Sealed controls (all PASS, `data/r1/controls_verdict.json`).**

- **NULL (σ0 = 1/2, outside the band).** The same pipeline must find growth, and does: a Krawczyk-certified L = 0
  eigenvalue with Re λ ≥ 0.02413229272632793 and Im λ ≈ 0.2832272004.
- **Schrödinger-Poisson n = 1 (no self-interaction), published instabilities.** C-P2 (L = 0, a quartet; window from
  Harrison, Moroz and Tod, Table 3): Re λ ≥ 0.08827420125417403 (the 10% real-part window was set after a 7% float
  mismatch: mock-informed, disclosed in the bar; certified ratio 0.04817 vs the published 0.0451); C-P3 (L = 2, a real
  growing pair, as in Fig. 4 (right panel, first excited, ℓ = 0) of arXiv:2310.18405): λ ≥ 0.09917673961346397.
- **C-B2.** E1/E0 of Schrödinger-Poisson at equal particle number: [0.189203706825 +/- 1.76e-13], inside the sealed
  window [0.1884, 0.1896] from Harrison, Moroz and Tod, Table 1.
- **C-P1.** The nodeless repulsive state at 9/5: K(L) = 0 for L = 0..3 at both radii.
- **C-B1 (calibration, matched after the fact).** The attractive nodeless background against Fig. 5 of
  arXiv:2402.07998.
- **C-R, C-W, positive-Krein controls.** Identical counts at R = 10 and 14; the exterior Schur form is unbounded below
  as it must be; the three positive-Krein neighbours are certified positive.

**Independent checks.**

- **Blind replication (sealed, f47da860b7, HOLD).** A separate seat saw only the paper and the definition of the
  object, chose its own method (B-spline Galerkin with an exact exterior condition for the Poisson field), and was
  scored by a script against predictions hashed before it ran. It reproduced E and m, every count, all three
  negative-Krein frequencies and all three positive-Krein neighbours to all ten printed digits (sealed pass rule: relative 1e-4; the ten-digit agreement is a POST HOC observation), max Re λ ≤ 1.6·10⁻¹¹
  at L = 0..3, and the growing quartet at σ0 = 1/2 (`data/blind/`, `checks/verdict_blind.py`). It is a float
  computation: a replication, not a certificate.
- **Three non-blind float checks** by internal referees (finite differences twice, Chebyshev collocation once) agree
  with every count, all six frequencies and all six Krein signs (they saw the certified values, so they are not
  blind).
- **Proof checks** (`checks/`): the start interval U0' is contained in the computed one (tube rebuilt from scratch, same
  sha256); the Frobenius slack holds; the assembly of every certified input into K = (2, 2, 2, 0) and the six Krein
  signs is recomputed (`ALL PASS`).
- **Review.** Two internal hostile referee rounds on the design before any instrument existed (referee-1, referee-2);
  referee-3 on the sealed run (σ0 entered exactly plus four code fixes, applied through the amendment); referee-4, blind to referee-3, on the
  whole chain; an engine audit (audit-1); referee-5 on the written proof (fixes applied in v2). These are internal lab
  checks, not external peer review. R2 (the twelve-point test) was reviewed by one internal hostile referee (referee-7). It re-derived all twelve verdicts from the released files with an independent script, re-ran the Frobenius check at the eight stable points, and checked the text, the numbers and privacy. An earlier release referee (referee-6) reviewed the R1 parts of this release. The build-3 engine changes were checked by the 9/5 regression and the disc controls, not by a separate engine audit. The R2 certified points have no blind replication. These are internal lab checks, not external peer review.

---

## 7. The stability band (Result B)

### 7.1 The float map (NOT certified)

Engine: the blind seat's B-spline Galerkin code (`code/band-map/`), with three local fixes described in
`data/band-map/MAP.md`. Background tolerance 10⁻¹⁰; box radius R = max(40, 70/√(−E)); a refined level with 1.5 R,
1.67 N and degree 9.

- Coarse sweep: σ0 = 0.30..5.00 in steps of 0.05, L = 0..6. Fine sweep: σ0 = 1.30..2.40 in steps of 0.01, L = 0..14.
- **Band.** [1.5963117, 1.9841288]. Lower-edge bracket at the refined grid [1.59631162, 1.59631172]; upper-edge
  bracket [1.98412876, 1.98412883]. Width 0.38782.
- **Sectors.** On [1.3, 2.4] only L = 0 (below the band) and L = 2 (above it) are ever unstable. For L = 3..14,
  n(L+) = n(L−) = 0 at every fine-grid point, so these sectors cannot carry growth; the centrifugal term then keeps
  higher L positive (inferred, not computed beyond L = 14).
- **Further out (coarse grid).** L = 3 is unstable from 2.75 and L = 4 from 4.05 on the grid; L = 1, 5, 6 never.

![The float band map: growth rate against central amplitude for each angular sector, coarse sweep left and fine sweep right, with the float band and the published band marked](figures/band-map.svg)

### 7.2 The mechanism at each edge (float)

- **Lower edge, L = 0.** On the stable side the negative-Krein L = 0 mode (the one at w ≈ 1.105 at 9/5) rises toward a
  positive-Krein mode coming down; they merge near w ≈ 1.01476 and leave the axis as a quartet ±a ± ib, with
  a ≈ 0.1427 √(σ_lo − σ0). The collision sits at w/|E| = 0.398, well inside the gap 0 < w < |E|.
- **Upper edge, L = 2.** The lowest L = 2 mode (negative Krein, w ≈ 0.297 at 9/5) climbs and meets the second L = 2 mode
  (positive Krein) near w ≈ 0.46371; above the edge a ≈ 0.279 √(σ0 − σ_hi). The collision sits at w/|E| = 0.126.
- **Not a real crossing, not a mass extremum.** n(L+) and n(L−) are the same on both sides of each edge; the
  Vakhitov-Kolokolov quantity ⟨L+⁻¹rσ, rσ⟩ is smooth and negative (−2.2470 at the lower edge); the mass increases
  strictly along the family.
- The square-root law of the growth rate is the signature of a generic Krein collision (Hamiltonian-Hopf).

![Krein collision at each edge: the negative-Krein frequency and its positive-Krein partner meet at the edge and become one growing pair](figures/krein-collision.svg)

### 7.3 The certified test (sealed design, BAR-R2-EDGES, seal 3ad051728e)

Twelve points, each its own all-or-nothing certificate, with the R1 pipeline made parametric in σ0 = p/q (`code/r2/`;
changes in the bar and in PATCHES.md, part B):

- just outside each edge, a certified growing eigenvalue: 1595/1000 (L = 0) and 1985/1000 (L = 2);
- just inside each edge, the full R1 stability certificate: 1597/1000 and 1983/1000, plus a certified separation of
  the two nearly colliding modes with opposite Krein signs;
- six interior points: 33/20, 17/10, 7/4, 37/20, 19/10, 39/20 (stability certificate);
- two points inside the published band where the float map shows growth: 31/20 (L = 0) and 2 (L = 2).

If both points of an edge HOLD, that edge is bracketed in an interval of width 0.002 containing the float edge.
Stability is claimed only at the sealed points, not on the intervals between them.

### 7.4 Certified outcomes (BAR-R2-EDGES settled HOLD; all twelve points HOLD; all controls PASS)

Every point HOLDS. All must-pass controls (C-B1, C-B2, C-P1, C-P2, C-P3, NULL, C-U150, C-U205) PASS under the final
instrument hashes, and the disc checks CAL-KD and CAL-ED PASS (`data/r2/controls_verdict.json`,
`data/r2/controls_r2_verdict.json`, `data/r2/R2_all_verdicts.json`). Boxes are the `refine:` lines of the run logs in
`data/r2/logs/`; as in R1, the `w` and `lam` strings in the JSON files are not used.

**Certified growing modes (linear instability proved).** A Krawczyk-certified eigenvalue with Re λ > 0 in the named
sector; the imaginary part is nonzero, so each is a quartet ±Re λ ± i Im λ:

| σ0 | sector | certified λ (Re + i Im, Krawczyk box) | verdict |
|---|---|---|---|
| 1595/1000 | L = 0 | [0.005159936765 +/- 9.79e-13] + i·[1.01371961231 +/- 4.07e-12] | HOLDS |
| 31/20 | L = 0 | [0.029367442235 +/- 6.23e-13] + i·[0.978168535545 +/- 7.14e-13] | HOLDS |
| 2 | L = 2 | [0.0353872961 +/- 2.52e-11] + i·[0.4686174535 +/- 2.65e-11] | HOLDS |
| 1985/1000 | L = 2 | [0.008240881 +/- 3.74e-10] + i·[0.463975628 +/- 5.55e-10] | HOLDS |

**Certified spectral stability at eight more points** (the full R1 certificate at each point: K = (2, 2, 2, 0) at
R = 10 and 14, D0, D1 > 0, a negative-Krein eigenvalue certified in each of L = 0, 1, 2 with its positive-Krein
neighbour certified positive, one tube sha256 per point, and the separation record):

| σ0 | verdict | K | w⁻ at L = 0 | w⁻ at L = 1 | w⁻ at L = 2 |
|---|---|---|---|---|---|
| 1597/1000 | HOLDS | (2, 2, 2, 0) | [1.01156658375 +/- 2.89e-12] | [0.454300995393917 +/- 2.58e-16] | [0.201778070 +/- 1.20e-10] |
| 33/20 | HOLDS | (2, 2, 2, 0) | [1.0231166878309 +/- 3.50e-14] | [0.476046298668078 +/- 2.95e-16] | [0.2239829738 +/- 5.79e-11] |
| 17/10 | HOLDS | (2, 2, 2, 0) | [1.04813654968334 +/- 6.83e-15] | [0.496958900414915 +/- 1.01e-16] | [0.2463961212 +/- 3.79e-11] |
| 7/4 | HOLDS | (2, 2, 2, 0) | [1.07581074350611 +/- 5.75e-15] | [0.518253661596410 +/- 3.63e-16] | [0.2705262718 +/- 4.21e-11] |
| 37/20 | HOLDS | (2, 2, 2, 0) | [1.13496776996447 +/- 1.92e-15] | [0.561969440698342 +/- 2.05e-16] | [0.3260149986 +/- 2.07e-11] |
| 19/10 | HOLDS | (2, 2, 2, 0) | [1.16574473209241 +/- 4.12e-15] | [0.584378958602663 +/- 8.78e-17] | [0.3596652774 +/- 3.80e-11] |
| 39/20 | HOLDS | (2, 2, 2, 0) | [1.19710410286268 +/- 2.65e-15] | [0.607147685016223 +/- 5.12e-16] | [0.4023308222 +/- 6.45e-11] |
| 1983/1000 | HOLDS | (2, 2, 2, 0) | [1.21807583965753 +/- 1.39e-15] | [0.622368426994779 +/- 2.65e-16] | [0.453984310 +/- 5.20e-10] |

**The two nearly colliding modes just inside each edge** (both certified, opposite Krein signs, disjoint boxes):

| σ0 | L | negative-Krein mode | positive-Krein partner | certified gap between the boxes |
|---|---|---|---|---|
| 1597/1000 | 0 | [1.01156658375 +/- 2.89e-12] (−), ⟨a,d⟩ = -1.612233679e-6 +/- 7.95e-11 | [1.01905618960 +/- 2.20e-12] (+), ⟨a,d⟩ = 1.659832199e-6 +/- 8.89e-11 | ≥ 0.007489 |
| 1983/1000 | 2 | [0.453984310 +/- 5.20e-10] (−), ⟨a,d⟩ = -2.889527238e-6 +/- 2.99e-08 | [0.472730296 +/- 5.38e-10] (+), ⟨a,d⟩ = 2.764440422e-6 +/- 2.90e-08 | ≥ 0.018745 |

**What this proves, and what it does not.**
- **Certified:** linear (spectral) stability at nine points across the window, 1597/1000, 33/20, 17/10, 7/4, 9/5 (R1),
  37/20, 19/10, 39/20 and 1983/1000; linear instability at 1595/1000 (L = 0), 31/20 (L = 0), 2 (L = 2) and
  1985/1000 (L = 2).
- **Certified edge brackets:** the state is certified unstable at 1.595 and certified stable at 1.597, and certified
  stable at 1.983 and unstable at 1.985. So a change from instability to stability lies in [1.595, 1.597] and one from
  stability to instability lies in [1.983, 1.985]. The float edges 1.5963117 and 1.9841288 lie inside these brackets.
  The certificates do not say that each transition is a single point.
- **Not certified:** stability between the certified points. The window [1.5963117, 1.9841288] as a whole is a float
  result: certified at nine points and float-mapped continuously in between.
- **Mechanism, certified in the weak sense of the bar:** each certified growing eigenvalue just outside an edge is
  non-real (a quartet), and just inside each edge the two colliding modes are certified with opposite Krein signs and
  separated (gap at least 0.007489 at 1597/1000 and 0.018745 at 1983/1000). The collision itself is a float
  observation.
- **How the proof transfers.** The eight R2 stable points use the R1 proof chain (PROOF-R1-v2, Sections 3-7, 9.2)
  with σ0 = p/q in place of 9/5. Every point-dependent input is a certified output of that point's run and was
  re-checked from the files by the R2 referee. Those inputs are the background flags, identical counts at R = 10 and 14
  (0 at L = 3, as the L ≥ 3 argument needs), positive exterior margins, D0 (n(B) = 2, d2 < 0, M|d2| ≥ 272), K = (2, 2,
  2, 0), the three negative-Krein certificates with 0 < w < |E|, and one tube sha256. Lemma 3.1 holds with
  sg = σ0 + 1/100 (F r0²/6 ≤ 2.86e-10 at all eight points). The Frobenius slack argument does not depend on σ0.
  `checks/check_frob_slack_r2.py` repeats the 9/5 check at the eight points (ALL PASS). The parametrised instruments are
  in `code/r2/` (changes: `code/r2/PATCHES-build3.md`); the 9/5 regression with them reproduces R1
  (`code/r2/CALIBRATION.md`).
- **The start interval at each R2 point, written exactly.** `checks/check_u0_r2.py` rebuilds each point's tube in
  memory exactly as its B job did (disk cache off), confirms the tube sha256 recorded in `data/r2/<tag>/B.json`, and
  checks in 400-bit ball arithmetic that U0'_p = [u_mid − 0.99·10⁻⁵⁰, u_mid + 0.99·10⁻⁵⁰] lies inside the computed
  start interval (log `checks/check_u0_r2.log`: ALL PASS at all eight points). So the theorem of Section 1 holds as
  stated at every one of the nine points, with U0' replaced by U0'_p:

| σ0 | u_mid (60 digits) | tube sha256 |
|---|---|---|
| 1597/1000 | 3.26257829877873232632728523408544749250724679772354387125538 | `a972731286c2559b…` |
| 33/20 | 3.43211518960578683230289225606858139753236980535419033262268 | `bcf501cf76088e21…` |
| 17/10 | 3.59659207485142889921563217406404416977402901494387498760527 | `5f55659ab04e2a95…` |
| 7/4 | 3.76554052577800818868878023500042080295687479763023181911048 | `10d6a3259cff74b9…` |
| 37/20 | 4.11710126372510784661490336736586880648244811516454564809644 | `851df5904ccad216…` |
| 19/10 | 4.29983054407140852492383796452184831740940264326441840450233 | `87934ed628e76d6f…` |
| 39/20 | 4.48726521011202076693095150956315573980034448089016171545471 | `3a07fc8c0824cc63…` |
| 1983/1000 | 4.61357440252882992130093660916470009950424657162244902579940 | `2226779189e2c3ff…` |

  **Theorem A at nine points.** For σ0 ∈ {1597/1000, 33/20, 17/10, 7/4, 9/5, 37/20, 19/10, 39/20, 1983/1000}, every
  regular solution of (2.1) with σ(0) = σ0 and u(0) ∈ U0'_p (U0' at 9/5) that decays and has exactly one zero has
  σ(J L) ⊂ iR.

### 7.5 Comparison with the published band

arXiv:2402.07998 reports, for L = 0..12, a common stability band 1.55 ≲ σ0 ≲ 2.07 (Fig. 8). Our float band lies
inside it, narrower by 0.046 at the bottom and 0.086 at the top. At the published endpoints our float computation finds
growth that is identical to all nine printed digits at three resolutions: 0.029367442 ± 0.978168536 i at σ0 = 1.55
(L = 0) and 0.073523517 ± 0.48414557 i at σ0 = 2.05 (L = 2); at σ0 = 2.00 the L = 2 growth rate is 0.0354. The paper
does not state its σ0 scan step, and "≲" leaves room for a coarser grid; our float edges are bracketed to ±1·10⁻⁷
on the refined grid (base and refined grids agree to 3·10⁻⁷). Section 7.4 certifies growth at σ0 = 31/20 = 1.55 (L = 0)
and σ0 = 2 (L = 2), both inside the published range. Section 8 says how we read this.

---

## 8. Fairness and credit

- **Chávez Nambo, Diez-Tejedor, Roque and Sarbach (arXiv:2402.07998)** built everything this work stands on: the
  model and its units, the linearisation and the sector decomposition, an analytic proof that no unstable modes exist
  for large enough L (their Section IV.4), and the numerical discovery of the band itself. The sectors at the edges,
  L = 0 below and L = 2 above, are visible in their Fig. 8; we credit them for it. Our float band is narrower than their
  stated 1.55 to 2.07, and the certified test confirms the difference at two points: the stated range contains
  σ0 = 31/20 = 1.55 (its lower end, which "≲" includes) and σ0 = 2, where the state is now certified linearly unstable
  (L = 0 and L = 2, growth rates about 0.0294 and 0.0354). Their pioneering result stands in substance: a narrow stable
  window exists, it is bounded by L = 0 below and L = 2 above exactly as their Fig. 8 shows, and it contains certified
  stable points. What changes is its extent. Their text does not state the σ0 resolution of the scan behind Fig. 8,
  and "≲" marks the ends as approximate; with a refined scan, the float window is [1.5963117, 1.9841288], and its edges
  lie in the certified brackets [1.595, 1.597] and [1.983, 1.985]. We read this as a refinement of their band, made
  possible by their model, code and figures. The same group re-showed the band in their Proca-star work
  (arXiv:2512.04376).
- **What is new here, to our knowledge** (prior-art search of arXiv to 16 November, INSPIRE and
  Zenodo to 17-18 November 2026): the first rigorous proof that the first excited (one-node) GPP state is linearly stable at any
  σ0 (here at nine points); refined band edges (float) with certified brackets of width 0.002; the identification of
  both edges as Krein collisions (float); and the first
  certified Hamiltonian-Krein index argument in which a negative-Krein eigenvalue must be certified (nonzero Krein
  index), for an operator with a nonlocal (Poisson) term. Earlier rigorous results on excited states cover large L
  ([CDRS] Sec. IV.4), a toy kernel ([MM]) and a symmetry-restricted class ([CS26]). The two nonlocal counts we found
  have one negative direction and no negative-Krein eigenvalue (Cadiot, arXiv:2403.18718; analytically, Georgiev and
  Stefanov, arXiv:1702.03374).
- **Brito, Herdeiro, Radu, Sanchis-Gual and Zilhão (arXiv:2506.06442)** studied relativistic excited boson stars by
  3+1 evolution and state that their runs do not allow them to verify the narrow band.
- **Harrison, Moroz and Tod (math-ph/0208045)** found numerically that excited Schrödinger-Newton states are radially
  unstable; their Table 1 gives our control C-B2.
- **Index theory.** The Hamiltonian-Krein accounting we use is classical (Kapitula, Kevrekidis and Sandstede;
  Kapitula and Stefanov, arXiv:1210.6005; Chugunova and Pelinovsky, math/0602386; Lin and Zeng, arXiv:1703.04016).
  We prove the one inequality we need directly.
- **Method neighbours.** Computer-assisted spectral stability for other equations: Cadiot (arXiv:2403.18718,
  arXiv:2505.03091), Beck and Jaquette (arXiv:2105.06895), van der Aalst and Cadiot (arXiv:2509.16693).
- **Our own corrections** (none of this was published): the first sealed run entered σ0 as the double nearest 1.8;
  an internal referee caught it together with an un-integrated gap in one Riccati step, float conversions of bounds,
  unasserted margins, an exterior margin without −ε and an unpinned tube cache; all were fixed under a sealed amendment
  and the run repeated at 9/5 exactly, with the same certified midpoints to every printed digit (radii differ in the
  last digits). The R2 float map found and fixed a tail-start bug in its own copy of the blind seat's background
  code. A duplicate seal of the same file is listed as VOID.

---

## 9. What we do not claim

- **Nine points, not an interval.** Stability is certified at σ0 = 9/5 (R1) and at the eight R2 points, with s = +1,
  α = 1, n = 1; instability at the four R2 unstable points. Nothing is certified between those points: there the
  window [1.5963117, 1.9841288] is a float result. An edge bracket [a, b] does not say that the transition in it is a
  single point.
- **Linear and spectral only.** No nonlinear or orbital stability; no claim about bounded growth of the linear
  semigroup, embedded eigenvalues in ±i[|E|, ∞), or the Jordan structure at 0. For excited states of other nonlinear
  Schrödinger equations, internal modes of negative Krein signature are known to be able to cause nonlinear
  instability (Cuccagna, arXiv:0801.4237; Kevrekidis, Pelinovsky and Saxena, arXiv:1412.1522).
- **Uniqueness of the state.** The theorem holds for every decaying one-node solution with u0 in U0'; that there is
  only one is not proved. At the R2 points, read U0'_p (the table in Section 7.4) for U0'.
- **No count of imaginary eigenvalues** and no algebraic simplicity.
- **One unchecked field in the R2 verdict code.** For the unstable points, `code/r2/verdict.py` (`point_unstable`)
  does not compare the sector of the certified eigenvalue with the sealed sector, while `controls_r2` does. The sector
  comes from the fixed point table in `code/r2/assemble.py`, and the sealed sector (0, 2, 0, 2) was confirmed from the
  outputs by the R2 referee. The sealed instruments are not changed.
- **The float map certifies nothing.** Its band, edges, mechanism and growth laws are float results.
- **No astrophysical claim.** Whether such cores exist in real halos is outside this work.
- **Numerical choices** (r0, R = 10 and 14, R1 = 26, r_m = 8, ε = 1/1000, disc radii, step sizes) are fixed points of
  the computation, not claimed constants.

---

## 10. Open doors

- **Stability on a whole interval, not a grid.** Nine points are certified stable; a continuity or perturbation
  argument between them would give the proved stable window as an interval.
  *Status:* UNTESTED; not part of any sealed test. *Start here:* the R2 outputs in `data/r2/` and the margins they
  record (exterior margins, M|d2|, the Krein separations).
  *Ceiling:* the exact, proved stable window of a one-shell dark-matter core.
- **Why L = 1 never breaks.** L = 1 carries a negative-Krein mode too (w ≈ 0.540 at 9/5), but on the whole float range
  [0.3, 5] it never collides. *Status:* UNTESTED observation from the float map. *Ceiling:* a structural reason that
  one sector of an excited core is always protected.
- **A different mechanism at large σ0.** On the coarse grid L = 3 becomes unstable from 2.75 and L = 4 from 4.05, and
  there n(L−) rises to 1 while n(L+) stays 0, which looks like a real crossing rather than a Krein collision.
  *Status:* UNTESTED; not bisected. *Start here:* `code/band-map/edge.py` at L = 3.
- **Nonlinear fate.** Whether the proved negative-energy wobbles let the core decay over long times under
  nonlinear coupling. *Status:* open; Section 9 cites the general mechanism. *Ceiling:* whether a stable excited core
  is stable in the sense that matters for halos.
- **The relativistic counterpart.** Excited boson stars with self-interaction in general relativity: the 3+1 study of
  arXiv:2506.06442 could not resolve the band. *Status:* open according to that paper. *Start here:* the certified
  Newtonian edges as targets for the relativistic family.

---

## 11. Sealed tests

| test | seal | what | verdict |
|---|---|---|---|
| R1 | 07faff6621 | spectral stability, first run (σ0 entered as the double nearest 1.8) | HOLD (superseded by the amendment) |
| R1 duplicate | dbcc9f9278 | same file sealed twice | VOID |
| R1 amendment | 6ad54f5713 | referee-3 fixes, re-run at σ0 = 9/5 exactly | HOLD |
| R1 blind | f47da860b7 | blind float replication | HOLD (PB1-PB5, PC) |
| R2 | 3ad051728e | certified edges and grid, 12 points | HOLD (all 12 points) |

Sealed texts: `seals/`. Every bar's predictions and pass rules were hashed before its run. The R1 predictions were
written after float smokes (mock-informed, disclosed in the bar); the R1 verdict is a certificate and cannot be moved by
them. The same holds for the R2 predictions (read off the float map, disclosed in BAR-R2-EDGES). The R1 items P1-P4
were sealed as MATCH/MISS predictions; they scored MATCH and are shown with the HOLD chip. The shipped copies have
local folder names replaced (PATCHES.md, part A); the original sha256 of each sealed file is listed there.

---

## References

Labels: OPENED = the lab read the full text; ABSTRACT = abstract or record only.

- [CDRS] E. Chávez Nambo, A. Diez-Tejedor, A. A. Roque, O. Sarbach, "On the linear stability of nonrelativistic
  selfinteracting boson stars", arXiv:2402.07998 (v2). OPENED. Model eqs. (9)-(17), (32)-(37), (43); large-L proof
  Sec. IV.4; band "1.55 ≲ σ0 ≲ 2.07" in the Fig. 8 caption; Fig. 8 read as a page image.
- [CDPRS] E. Chávez Nambo, G. Diaz-Andrade, A. Diez-Tejedor, E. Preciado-Govea, A. A. Roque, O. Sarbach, "Linear
  stability of nonrelativistic Proca stars", arXiv:2512.04376 (v2). OPENED (footnote 10, Sec. V.B.1, Fig. 5).
- [BHRSZ] M. Brito, C. Herdeiro, E. Radu, N. Sanchis-Gual, M. Zilhão, "Stability and collisions of excited spherical
  boson stars: glimpses of chains and rings", arXiv:2506.06442. OPENED.
- [HMT] R. Harrison, I. Moroz, K. P. Tod, "A numerical study of the Schrodinger-Newton equation 1: Perturbing the
  spherically-symmetric stationary states", math-ph/0208045. OPENED.
- [CRS] E. Chávez Nambo, A. A. Roque, O. Sarbach, "Are nonrelativistic ground state ℓ-boson stars only stable for ℓ=0
  and ℓ=1?", arXiv:2310.18405. OPENED (Fig. 4: the L = 2 real growing pair of control C-P3; unit factor for C-P2).
- [Cad1] M. Cadiot, "Constructive proofs of existence and stability of solitary waves in the Whitham and
  capillary-gravity Whitham equations", arXiv:2403.18718. OPENED.
- [Cad2] M. Cadiot, "Stability analysis for localized solutions in PDEs and nonlocal equations on R^m",
  arXiv:2505.03091. ABSTRACT.
- [vdAC] L. van der Aalst, M. Cadiot, "Existence proofs of traveling wave solutions on an infinite strip for the
  suspension bridge equation and proof of orbital stability", arXiv:2509.16693. ABSTRACT.
- [MM] M. Maeda, S. Masaki, "An example of stable excited state on nonlinear Schrödinger equation with nonlocal
  nonlinearity", arXiv:1109.2653. OPENED (by our prior-art gate).
- [CS26] E. Chávez Nambo, O. Sarbach, "Existence of nonrelativistic ℓ- and multi-ℓ-boson stars and their radial
  stability", arXiv:2605.27529. ABSTRACT.
- [BJ] M. Beck, J. Jaquette, "Validated spectral stability via conjugate points", arXiv:2105.06895. ABSTRACT.
- [GS] V. Georgiev, A. Stefanov, "On the classification of the spectrally stable standing waves of the Hartree
  problem", arXiv:1702.03374. OPENED.
- [KS] T. Kapitula, A. Stefanov, "A Hamiltonian-Krein (instability) index theory for KdV-like eigenvalue problems",
  arXiv:1210.6005. ABSTRACT.
- [CP] M. Chugunova, D. Pelinovsky, "Count of eigenvalues in the generalized eigenvalue problem", math/0602386.
  ABSTRACT.
- [LZ] Z. Lin, C. Zeng, "Instability, index theorem, and exponential trichotomy for Linear Hamiltonian PDEs",
  arXiv:1703.04016. ABSTRACT.
- [KKS] T. Kapitula, P. G. Kevrekidis, B. Sandstede, Physica D 195 (2004) 263, DOI 10.1016/j.physd.2004.03.018.
  Cited for the classical count; not opened.
- [Cuc] S. Cuccagna, "On instability of excited states of the nonlinear Schrödinger equation", arXiv:0801.4237.
  ABSTRACT.
- [KPS] P. G. Kevrekidis, D. E. Pelinovsky, A. Saxena, "When Does Linear Stability Not Exclude Nonlinear
  Instability?", arXiv:1412.1522. ABSTRACT.
- [Kra] R. Krawczyk, "Newton-Algorithmen zur Bestimmung von Nullstellen mit Fehlerschranken", Computing 4 (1969)
  187-201, DOI 10.1007/BF02234767. Standard; not opened.
- [Arb] F. Johansson, Arb (ball arithmetic), used through python-flint 0.9.0.

---

*Prepared with AI assistance; what was checked, and by what, is stated above.*
