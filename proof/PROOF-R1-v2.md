# PROOF-R1-v2: spectral stability of the one-node repulsive GPP state at sigma0 = 9/5

**Status: PROOF DRAFT v2, refereed (referee-3, referee-4, referee-5; engine audit audit-1).**

Moki & Julio (AI-assisted). Seat proof-1, raid R1, dark-sector hunt, 2026-11-18. Supersedes PROOF-R1.md, which is
kept unchanged.

**Blind replication pending.** A blind float replication is pending under seal f47da860b7. This seat has not opened
that folder and has seen none of its content.

### Changelog v1 -> v2 (referee-5 = core/seats/referee-5/REFEREE-R1-PROOF.md; audit-1 = core/seats/audit-1/AUDIT-ENGINES.md)

| change | where | referee item |
|---|---|---|
| U0 defined exactly. The theorem is now stated for U0' = [u_mid - 0.99e-50, u_mid + 0.99e-50], using the 60-digit u_mid from target_bg_tube.json, and containment U0' in U0 is checked by a tube rebuild (checks/check_U0.py) | section 1 | referee-5 section 1, blocking 1 |
| GAPS rewritten: A1 closed by audit-1; B1 closed as listed by referee-5; the remaining unaudited items listed; B2 kept as a disclosed list | section 13; also sections 9.2, 10, 11 | referee-5 section 13, blocking 2 |
| A line on the pending blind replication (seal f47da860b7) | header | referee-5 blocking 3 (lead decision) |
| Lemma 5.1 step 2 reworded: h(0) = 0 because psi and G_L(sigma a) are O(r^(L+1)) | 5.1 | referee-5 section 5, fix 1 |
| GAP C2 now also covers krein_ad, int_inner and int_outer, and states why the <a, d> column stays valid | 13, C2 | referee-5 section 5, fix 2 |
| Cross-reference "Lemma 6.2(ii)" corrected to "Theorem 6.2(ii)" | 6.1(b) | referee-5 section 6, cosmetic |
| Latent code items noted (not on the target path): the Iin_lo clamp, the "level -nu" docstring, and audit-1's four patches | 13, C4 and C6 | referee-5 section 4 and cosmetic list; audit-1 |

**Pinned inputs.** Seals 07faff6621 (build-1/BAR-R1-FINAL.md) and 6ad54f5713 (build-2/AMENDMENT-R1-1.md). Instruments
build-2/*.py; this seat recomputed all eleven sha256 and they equal build-2/RUN.md. Certified outputs
build-2/out/target-B.json, target-K0.json, target-K1.json, target-K2.json (with their .log files), target_verdict.json
and controls_verdict.json. All four target outputs report the same tube sha256
f8b0cc27d5885a45af4b7356a1e3f6f2e0e1445510e32842cf4710f9ecfce28b (checked by core/proof/checks/check_assembly.py).

**Conventions.**
- `file:N` is line N of build-2/file.
- `paper:N` is line N of <LAB-ROOT>/seats/frontier/dl/2402.07998.txt.
- `[m +/- r]` is a ball.
- `OPENED` means this seat read the source at the given locator.
- `STANDARD, not opened` marks a textbook fact used without opening any source. Each one is collected in GAPS (B2).
- "Code fact Cn" (section 10) is a property of the code that a proof step relies on. Those facts are what the code
  audit must confirm.
- All forms are real symmetric unless complexified explicitly.
- For a self-adjoint T bounded below with form t, `n(T)` is the supremum of the dimensions of subspaces of the form
  domain on which t is negative definite, and `#(T < c) := n(T - c)`. Every count below is proved in this subspace
  form.

---

## 0. In plain words

A cloud of ultralight dark matter can settle into a ball that its own gravity holds together, with a weak push
between the particles. One such ball has a single hollow shell inside it. A numerical study (arXiv 2402.07998) found
that, for a band of central densities, this shelled ball survives every small shake. We prove this at one point of
the band, central amplitude exactly 9/5, with the computer doing arithmetic that carries its own error bars.
"Survives" means that no small disturbance, of any shape, grows exponentially in time. The proof counts, with
certified error bars, the ways the ball's energy can go down: at most two in each shape class. It then shows that
those two are used up by one oscillation that provably carries negative energy, and a negative-energy oscillation
cannot grow. Nothing is claimed about large shakes, other central densities, or what happens over long times beyond
the linear equations.

---

## 1. Theorem

Let s = +1 (repulsive), alpha = 1, sigma0 = 9/5 exactly.

**The start interval.** U0 is the interval the code computes (bg_tube.py:278, U0 = (u - d).union(u + d) with
d = 10^-50 at bg_tube.py:270), for the tube with sha256 f8b0cc27d5885a45af4b7356a1e3f6f2e0e1445510e32842cf4710f9ecfce28b.
Its midpoint is recorded in build-2/out/target_bg_tube.json as

    u_mid = 3.93902357537910961270976242947912892526530674750036020337021 .

The theorem is stated for the exactly defined interval

    U0' := [u_mid - 0.99 x 10^-50 , u_mid + 0.99 x 10^-50] ,

which is contained in U0. checks/check_U0.py verifies this (log check_U0.log, ALL PASS). The script:
1. checks that the json u_mid and tube sha256 are the ones above;
2. checks that the 45-digit refine value in target-K0.log agrees with u_mid to better than 1e-44;
3. rebuilds the tube in memory exactly as the pre-seal command did, with no cache read or written, and gets the same
   sha256;
4. checks in 400-bit ball arithmetic that the computed U0 (decoded outward) contains U0'.

The margin is 10^-52, far above the 5 x 10^-60 rounding of the 60-digit midpoint. Every certified enclosure below is
uniform over U0, so it holds on U0'. Below, "U0" means U0' wherever the theorem is stated.

**Theorem.** Take any regular solution (sigma, u) of (2.1) with sigma(0) = 9/5 and u(0) = u0 in U0' that decays at
infinity and has exactly one zero. At least one such solution exists (Lemma 3.2). Let E = u(infinity). Let
A = J L be the linearised operator (2.4) on L^2(R^3; C^2). Then the spectrum of A contains no point with
Re lambda > 0, and in particular no eigenvalue. In fact the spectrum of A lies on the imaginary axis (Theorem 7.3).

**By-product (Corollary 4.6).** The Morse indices are exactly n(L+(L)) = 2, 1, 1, 0 and n(L-(L)) = 1, 1, 1, 0 for
L = 0, 1, 2, 3, and they are 0 for every L >= 3. The kernels are exactly ker L-(0) = span(r sigma) and
ker L+(1) = span(r sigma'). Every other sector kernel is trivial. In 3-D, ker L+ is spanned by the three
translations and ker L- by the phase direction sigma.

The state is the first excited (one-node) state of the paper (paper:768, "first excited (n=1)"). It is not the ground
state. sigma0 = 9/5 lies inside the band 1.55 <~ sigma0 <~ 2.07 that the paper reports as stable (paper:1073).

---

## 2. Setup

### 2.1 The system (OPENED: 2402.07998)

- Dimensionless GPP system (9a)-(9b), paper:400-412, and its operator form (10)-(12), paper:424-442:
  `H(psi) = -Delta +/- |psi|^2 + Delta^-1(|psi|^2)`, with `Delta^-1(f)(x) = -(1/4pi) int f(y)/|x-y| d^3y` (paper:442).
  The upper sign is the repulsive case (paper:353).
- Stationary states psi = e^{-iEt} sigma(x), (16)-(17), paper:514-528: `E sigma = H(sigma) sigma`.
- In radial form with u := E - U (paper:743), (32a)-(32b) (paper:751, 757) read

  (2.1)  `sigma'' + 2 sigma'/r = (s sigma^2 - u) sigma ,   u'' + 2 u'/r = -sigma^2 ,`

  with sigma(0) = sigma0, sigma'(0) = 0, u(0) = u0, u'(0) = 0 (paper:762), and E = u0 - int_0^inf sigma^2 r dr (33)
  (paper:778).

Elementary facts used throughout, for a regular solution on its interval of existence. Here
m(r) := int_0^r sigma^2 t^2 dt, I(r) := int_0^r sigma^2 t dt, and a := r sigma.

- (F1) r^2 u'(r) = -m(r), so u' <= 0.
- (F2) (u + r u')' = -r sigma^2, so u(r) + r u'(r) = u0 - I(r).
- (F3) For a decaying solution, with m := m(inf) and I1 := I(inf): E = u(inf) = u0 - I1, which is (33), and
  u(r) - E = int_r^inf m(t)/t^2 dt, which lies in [0, m/r]. Hence
  - (UB) -u(r) >= |E| - m/r and -u(r) <= -E;
  - tau(r) := m/r - (u(r) - E) = int_r^inf (m - m(t))/t^2 dt lies in [0, (m - m(r))/r].
- (F4) a'' = (s sigma^2 - u) a.

### 2.2 Linearisation (OPENED; re-derived by this seat, in agreement with referee-4 item A)

The ansatz (18) (paper:541) in (10) gives (19) (paper:554):
`i sigma_t = (H0 - E) sigma + 2 sigma0 K[sigma0 Re sigma]`, with K = +/-1 + Delta^-1 (20) (paper:563).

The mode ansatz (21) (paper:572) is sigma = (A+B) e^{lambda t} + (A-B)^* e^{lambda^* t}. It gives
Re sigma = A e^{lambda t} + c.c. The coefficient of e^{lambda t} is

    i lambda (A+B) = (H0-E)(A+B) + 2 sigma K[sigma A].

The conjugate of the coefficient of e^{lambda^* t} is

    -i lambda (A-B) = (H0-E)(A-B) + 2 sigma K[sigma A]

(H0 and K are real). Subtracting and adding these two gives (22a)-(22b) (paper:582, 588):

    i lambda A = (H0 - E) B ,     i lambda B = (H0 - E) A + 2 sigma K[sigma A].

U = Delta^-1(sigma^2) is the decaying solution of (9b), and u = E - U. Hence H0 - E = -Delta + s sigma^2 - u. Define

(2.2)  `L- := -Delta + s sigma^2 - u ,   L+ := -Delta + 3 s sigma^2 - u + 2 sigma Delta^-1 sigma .`

With C := -iB this becomes lambda A = L- C and lambda C = -L+ A, that is

(2.3)  `lambda (A, C) = J L (A, C) ,   J = [[0, 1], [-1, 0]] ,   L = diag(L+, L-) .`

On lambda = i w with C = i D: L+ A = w D and L- D = w A.

**Sectors.** Expanding in spherical harmonics, (34)-(37) (paper:818-861), gives (35) with Delta_L^-1 of (37)
(paper:861). The paper uses reduced functions a_L = r A_LM (paper:953) and states that (35) is independent of M
(paper:975). The reduced form is (43a)-(43b) (paper:961-971). (43b) carries a factor alpha (paper:971). alpha = 1 is
the value at which (43b) is the reduction of (35b)-(36b), and it is the value this theorem fixes. From (37), the
operator G_L := (d^2/dr^2 - ell/r^2)^-1 = r Delta_L^-1 r^-1 (paper:974; ell = L(L+1)) acting on reduced functions has
the kernel -(2L+1)^-1 r_<^(L+1) r_>^-L. The reason: r r~ r_<^L r_>^(-L-1) = r_<^(L+1) r_>^-L.

Per sector (L, M), on X := L^2(0, inf) of reduced functions, with Dirichlet condition at 0:

(2.4)  `L-(L) = -d^2 + ell/r^2 + s sigma^2 - u ,   L+(L) = -d^2 + ell/r^2 + 3 s sigma^2 - u + 2 sigma G_L sigma ,`

and A_L = J diag(L+(L), L-(L)). Write P_L := -d^2 + ell/r^2 >= 0, so that G_L = -P_L^-1. The kernel of P_L^-1,
k_L(r, t) = (2L+1)^-1 r_<^(L+1) r_>^-L, is positive.

The map A(x) -> (a_LM(r)) is unitary from L^2(R^3) onto the direct sum over (L, M) of L^2(0, inf). The 3-D
operators are the orthogonal direct sums of the sector operators, each repeated 2L+1 times. This is paper (35)-(37),
OPENED. The multipole expansion behind (37) is STANDARD, not opened.

**Domains.** Set H0 := -d^2 + ell/r^2 - E (in 3-D, -Delta - E). It is self-adjoint and H0 >= |E| > 0, since E < 0
(Lemma 3.3). Write L+- = H0 + V+-, with

    V- = s sigma^2 + (E - u) ,   V+ = 3 s sigma^2 + (E - u) - 2 sigma P_L^-1 sigma .

All three pieces are bounded: sigma is bounded, E - u is bounded and tends to 0 by (F3), and the last term is
Hilbert-Schmidt (Lemma 4.1). So L+- are self-adjoint on D(H0), and A is closed on D(H0)^2.

**Kernels (used to book zero modes).**
- (K1) L-(0) (r sigma) = 0. This is (F4).
- (K2) L+(1) (r sigma') = 0. The translates sigma(x - h e1) solve (17) with the same E, because Delta, |.|^2 and the
  convolution Delta^-1 commute with translations. The derivative of sigma -> H(sigma) sigma - E sigma in a real
  direction v is (-Delta + 3 s sigma^2 + Delta^-1(sigma^2) - E) v + sigma Delta^-1(2 sigma v) = L+ v. Differentiating
  at h = 0 therefore gives L+ d_1 sigma = 0. d_1 sigma = sigma'(r) x1/r is pure L = 1 with reduced radial function
  r sigma'. It decays exponentially (Lemma 3.3), so it lies in D(H0).

**The constraint space used by IDX.**
- Y_L := X x X for L >= 1.
- Y_0 := {(a, c) : <a, r sigma> = 0}.
- n(L | Y) is the supremum of the dimensions of subspaces of Y (intersected with the form domain) on which
  l[(a, c)] = q+(a) + q-(c) is negative definite.
- The form is diagonal and the constraint acts on a only, so n(L | Y_0) = n(q+ restricted to (r sigma)^perp) + n(q-)
  and n(L | Y_L) = n(L+(L)) + n(L-(L)) for L >= 1.

---

## 3. The background: existence (B-EX) and certified tail (B-TAIL)

### Lemma 3.1 (start interval [0, r0]; r0 = the binary64 number nearest 1e-5)

**Statement.** The regular solution of (2.1) with sigma(0) = 9/5 and u(0) = u0 in U0 exists on [0, r0] and is unique.
On that interval:
- |sigma - sigma0| <= F r^2/6 and |u - u0| <= sg^2 r^2/6, where sg = 9/5 + 1/100, ua = |u0| + 1/100 and
  F = (|s| sg^2 + ua) sg;
- hence sup|sigma| < sg, sup|u| < ua, and sigma > 0.

**Proof.**
1. Existence and uniqueness follow from the Volterra map (sigma, u) = (sigma0, u0) + V[(f_sigma, f_u)], with
   V[g](r) = int_0^r t^-2 int_0^t x^2 g(x) dx dt. On C[0, r0] it is a contraction with constant Lip r0^2/6 < 1/2
   (asserted at bg_tube.py:96-98; Banach fixed point, STANDARD).
2. Bootstrap. Let r~ be the supremum of the r <= r0 such that |sigma - sigma0| <= 1/100 and |u - u0| <= 1/100 on
   [0, r]. On [0, r~], |f_sigma| <= F, and V[1] = r^2/6 gives the two bounds.
3. Numerically, F r0^2/6 < 2.5e-10 and sg^2 r0^2/6 < 5.5e-11, both far below 1/100. So r~ = r0.
4. The code's own crude enclosure on [0, r0] (bg_tube.py:112) is sigma in [1.8000000000 +/- 2.10e-11] and
   u in [3.9390235754 +/- 7.67e-11] (checks/check_frob_slack.log). It agrees.

The 1/100 margins that bracket.qbound, bracket.gnorms and match.frob_start assume are therefore proved here
analytically. They are also asserted in code (bg_tube.py:119-132, called at bracket.py:43-44, bracket.py:223 and
match.py:53; referee-3 item 3).

### Lemma 3.2 (B-EX: existence inside the tube, s = +1)

**Statement.** For s >= 0 and n = 1, let Esc be the set of u0 whose solution has a radius r* with all of the
following:
- exactly n zeros of sigma on (0, r*];
- u(r*) < 0;
- a(r*) and a'(r*) both nonzero, with the sign (-1)^n sign(sigma0) (here a < 0 and a' < 0).

Let Z be the set of u0 whose solution has at least n + 1 zeros in its interval of existence. Then:
- Esc and Z are open and disjoint;
- every solution in Esc is unbounded (not localised);
- if u_lo is in Esc, u_hi is in Z, u_lo < u_hi, and the whole interval [u_lo, u_hi] has solutions on [0, R1], then
  some u0* in (u_lo, u_hi) lies in neither set, and its solution is global, decaying and has exactly n zeros.

**Proof.**
1. *Zeros are simple.* If sigma(r1) = sigma'(r1) = 0 for some r1 > 0, then sigma = 0 identically, by uniqueness for
   the first equation of (2.1), which is linear in sigma once u is given. That contradicts sigma0 != 0. Simple zeros
   are transversal, so the number of zeros on [0, r*] with sigma(r*) != 0 is locally constant in u0. Continuous
   dependence on u0 through the regular singular point holds because the Volterra fixed point of Lemma 3.1 depends
   continuously on u0 (STANDARD). With strict inequalities at r*, this makes Esc open, and Z is open for the same
   reason.
2. *Escape is permanent.* Let u0 be in Esc and r >= r*. By (F1), u(r) <= u(r*) < 0, so s sigma^2 - u > 0. While
   a < 0, (F4) gives a'' < 0, so a' <= a'(r*) < 0 and a < a(r*) < 0. Hence a never returns to 0: there are no more
   zeros, and |a| >= |a(r*)| + |a'(r*)| (r - r*), possibly with blow-up. In particular Esc and Z are disjoint
   (exactly n zeros against at least n + 1).
3. *Connectedness.* [u_lo, u_hi] is connected, and Esc and Z are disjoint relatively open sets containing u_lo and
   u_hi respectively. So some u0* in the interval lies in neither.
4. *The solution for u0* is global and decays.* The tube shows exactly one zero on [0, R1] = [0, 26]. None lies in
   [0, r0] (Lemma 3.1); the rest are counted by the step rule below. The tube also shows a(R1) < 0 and
   u(R1) < 0, uniformly over U0. Since u0* is not in Z, there are no further zeros, so a < 0 on [R1, r_max). Since
   u0* is not in Esc, a'(r) >= 0 for every r in [R1, r_max); otherwise r would be an escape radius. So
   a(R1) <= a < 0 and a' <= a'(R1), by a'' < 0. Hence a and a' are bounded, sigma is bounded, u' = -m(r)/r^2 is
   bounded, and the solution is global. Decay follows from Lemma 3.3.

**Certified inputs** (target-B.json; code facts C1, C2, C3):
- `B.classify.lo.result = "escape"` (zeros 1, r = 44.88) and `B.classify.hi.result = "zeros"` (zeros 2), at
  bg_tube.py:160-161, 175-181 and 272-275. These are the two balls around u -/+ 10^-50 (bg_tube.py:270), and they
  contain the two ends of U0 (bg_tube.py:278).
- `B.existence_certified = true` (bg_tube.py:277).
- `B.zeros = 1`. The step rule (bg_tube.py:158-168): a step with no zero needs a sigma box excluding 0; otherwise the
  sigma' box must exclude 0, so sigma is monotone on the step, and the step has exactly one zero iff the certified
  endpoint signs differ.
- `B.tail_ok = true`, which is a(R1) < 0 and u(R1) < 0 (bg_tube.py:292-293, 323).
- `B.u_R1 = [-2.36856669502 +/- 2.38e-12]`.

So some u0* in U0 gives a decaying one-node state. All later enclosures are uniform over U0, so they hold for every
such u0*.

### Lemma 3.3 (B-TAIL)

**Statement.** For every u0* as in Lemma 3.2 and every r >= R1 = 26, with kappa1 := sqrt(-u(R1)) (its certified
lower end) and a1 := |a(R1)| (its certified upper end):
- (i) a < 0 <= a', and |a(r)| <= a1 e^{-kappa1 (r - R1)};
- (ii) |a'(r)| <= (Vmax/kappa1) |a(r)|, with Vmax = s (a1/R1)^2 - u(R1) + m/R1;
- (iii) |sigma(r)| <= (a1/r) e^{-kappa1 (r-R1)}, and |sigma'(r)| <= (Vmax/kappa1 + 1/r)(a1/r) e^{-kappa1 (r-R1)};
- (iv) int_R1^inf sigma^2 r^2 <= a1^2/(2 kappa1), and int_R1^inf sigma^2 r <= a1^2/(2 kappa1 R1);
- (v) the tails of T, F and int sigma^2 u r^2 are bounded as in bg_tube.py:314-317.

Consequently E, m, I1 and u0 are enclosed as in target-B.json:
- `B.E = [-3.10544025447 +/- 3.02e-12]`
- `B.m = [19.1587125456 +/- 4.04e-11]`
- `B.I1 = [7.04446382985 +/- 3.92e-12]`
- `B.kappa1 = [1.53901484561 +/- 4.69e-12]`
- `B.a1 = [7.75859535966e-12 +/- 3.43e-24]`

These come from bg_tube.py:286-326: a1 at 289; kappa1 at 294-302; m = m_in + [0, tail] at 305-307;
I1 = I_in + [0, tail] at 306-309 with I_in = u0 - u - r u' by (F2); E = U0 - I1 at 310. In particular E < 0.

**Proof.**
1. Write b := -a > 0 on [R1, inf). By Lemma 3.2, b' <= 0.
2. By (F1), -u(r) >= -u(R1) = kappa1^2 for r >= R1. So b'' = (s sigma^2 - u) b >= kappa1^2 b.
3. Let g := b' + kappa1 b. Then g' = b'' + kappa1 b' >= kappa1 (kappa1 b + b') = kappa1 g. If g(r1) > 0 at some r1,
   then g >= g(r1) e^{kappa1 (r - r1)} grows without bound. But g <= kappa1 b <= kappa1 b(R1). Hence g <= 0, that is
   b' <= -kappa1 b, which gives (i).
4. Starting the same argument at any r >= R1 gives b(t) <= b(r) e^{-kappa1 (t - r)} for t >= r.
5. b' is increasing (b'' >= 0) and bounded above by 0. Its limit is 0, since otherwise b would tend to -inf. So
   |b'(r)| = int_r^inf b'' <= sup V int_r^inf b(r) e^{-kappa1 (t-r)} dt = (Vmax/kappa1) b(r), with
   V := s sigma^2 - u. The bound V <= Vmax uses sigma^2 = a^2/t^2 <= (a1/R1)^2 and, by (F3),
   -u(t) <= -E <= -u(R1) + m/R1, which is the code's negE_up. This gives (ii).
6. (iii) follows from sigma = a/r and sigma' = a'/r - a/r^2. (iv) and (v) are integrals of the exponential bounds.

kappa1^2 = -u(R1) <= s sigma^2 - u(r) for r >= R1, by (F1). The bound uses the upper end of u(R1) and the lower end of
kappa1 (bg_tube.py:302).

**Remark (VIR, not used by the proof).** The virial identity D = 2T + 3sF (26) (paper:644) holds with relative
residual `B.virial_rel = [+/- 8.21e-16]`. It is a consistency check only. It cannot detect a convention error shared by
the tube and the quadratures (referee-4 item D). The convention is tested by C-B1 against Fig. 5.

---

## 4. Certified counts: BR, BR-R0, BR-M, D0

### Lemma 4.1 (HS and the closed-form delta)

**Statement.** Let 0 < R <= inf and sigma_i := sigma 1_[0,R]. Then

    ||sigma P_L^-1 sigma - sigma_i P_L^-1 sigma_i||_HS <= sqrt(I1^2 - I_in(R)^2)/(2L+1),   I_in(R) := int_0^R sigma^2 r .

In particular ||sigma P_L^-1 sigma||_HS <= I1/(2L+1), which is node HS. Write
delta_L(R) := 2 sqrt(I1^2 - I_in(R)^2)/(2L+1). Then for all a,

    2 <sigma a, G_L sigma a> >= 2 <sigma_i a, G_L sigma_i a> - delta_L(R) ||a||^2 .

**Proof.**
1. The kernel bound: r_<^(L+1) r_>^-L = sqrt(r t) (r_</r_>)^(L+1/2) <= sqrt(r t).
2. With indicator functions, (sigma(r) sigma(t) - sigma_i(r) sigma_i(t))^2 = sigma(r)^2 sigma(t)^2 (1 - 1_i(r) 1_i(t))
   = sigma^2 sigma^2 - sigma_i^2 sigma_i^2.
3. Integrating, HS^2 <= (2L+1)^-2 int int (sigma^2 sigma^2 - sigma_i^2 sigma_i^2) r t = (I1^2 - I_in^2)/(2L+1)^2.
4. The operator norm is at most the HS norm, and G_L = -P_L^-1.

**Code.** I_in(R) is bounded below by its value at the last tube grid point that is certified <= R (bracket.py:287-288;
I_in is increasing by (F2)). delta is taken as an upper end (bracket.py:291). Values are in target-B.json
`brackets.radii.<R>.<L>.delta`:

| | L = 0 | L = 1 | L = 2 | L = 3 |
|---|---|---|---|---|
| R = 10 | 0.0881154 | 0.0293718 | 0.0176231 | 0.0125879 |
| R = 14 | 4.45979e-4 | 1.48660e-4 | 8.91958e-5 | 6.37113e-5 |

### Lemma 4.2 (SC: Schur complement in form sense)

**Statement.** Let W_L be the completion of C_c^inf(0, inf) in the norm P_L[w]^(1/2), where
P_L[w] = int (w'^2 + ell w^2/r^2). For L = 0 it contains functions that are constant near infinity. Let g be
continuous with int (1 + r)|g| < inf; here g = sigma a or sigma_i a, which decay exponentially. Then

    min over w in W_L of { P_L[w] + 2 sqrt2 <g, w> } = -2 <g, P_L^-1 g> ,   attained at w* = -sqrt2 P_L^-1 g .

**Proof.**
1. w* is regular at 0 and O(r^-L) at infinity, and w*' = O(r^(-L-1)) (for L = 0, w*' = sqrt2 int_r^inf g decays
   exponentially). So P_L[w*] < inf and w* lies in W_L.
2. For w in C_c^inf, integration by parts gives P_L(w*, w) = <P_L w*, w> = -sqrt2 <g, w>. Hence
   P_L[w] + 2 sqrt2 <g, w> = P_L[w - w*] - P_L[w*].
3. Both sides are continuous on W_L, because |w(r)| <= sqrt(r) P_L[w]^(1/2) and int sqrt(r)|g| < inf. So the identity
   extends to all of W_L.
4. P_L[w*] = 2 <g, P_L^-1 g>, which gives the minimum.

**Consequences.**
- q+(a) = min over w of Q2_L(a, w), with
  Q2_L(a, w) := q_loc(a) + P_L[w] + 2 sqrt2 <sigma a, w> and q_loc(a) := int a'^2 + (ell/r^2 + 3 s sigma^2 - u) a^2.
- By Lemma 4.1, q+(a) >= min over w of Q2^{delta,R}(a, w), where
  Q2^{delta,R}(a, w) := q_loc(a) - delta ||a||^2 + P_L[w] + 2 sqrt2 <sigma_i a, w>.
- Restricted to [0, R], this is the form of the 2x2 matrix Sturm system

      -Y'' + Q Y = lambda Y,   Y = (a, w),   Q = [[ell/r^2 + 3 s sigma^2 - u - delta, sqrt2 sigma], [sqrt2 sigma, ell/r^2]].

  This is bracket.py:6-7 and 58-60, where the shift -delta is in the a-channel only and the level lambda is in both
  channels. Referee-4 item A checked the minimum over w independently.
- Exterior of w: for w in W_L and R > 0, int_R^inf (w'^2 + ell w^2/r^2) >= (L/R) w(R)^2. To see this, note that
  w'^2 + ell w^2/r^2 = (w' + L w/r)^2 - (L w^2/r)', and liminf w^2/r = 0. For L >= 1 that follows from
  int w^2/r^2 < inf; for L = 0 the coefficient L vanishes. Equality holds for w(R)(R/r)^L.

### Lemma 4.3 (BR-R0: Robin start at r0 sandwiching the regular point)

**Statement.** Fix a real level lambda' and let Qt := Q - ell/r^2 - lambda' on [0, r0]. Suppose
q >= sup over [0, r0] of ||Qt||_inf (row sums). Let Phi = r^(L+1) Z, with Z(0) = I, be the regular matrix solution of
-Phi'' + (Q - lambda') Phi = 0, and set c := r0^2 q/(2(2L+3)) < 1/4. Then:
- (a) ||Z - I|| <= e1 := c/(1-c) and ||Z'|| <= e2 := r0 q (1+e1)/(2L+3) on [0, r0];
- (b) U_{lambda'}(r0) := Phi'(r0) Phi(r0)^-1 is symmetric, with spectrum in (L+1)/r0 +/- eta, where
  eta = e2/(1 - e1);
- (c) for every Psi in the form domain on [0, r0] (Psi(0) = 0) with Psi(r0) = c_v:
  int_0^r0 (|Psi'|^2 + Psi^T (Q - lambda') Psi) >= <U_{lambda'}(r0) c_v, c_v>,
  with equality for Psi = Phi Phi(r0)^-1 c_v.

**Proof.**
1. (a) Z = I + V_L[Qt Z], with V_L[g](r) = int_0^r t^(-2L-2) int_0^t x^(2L+2) g dx dt, and
   ||V_L[g]||(r) <= sup||g|| r^2/(2(2L+3)). So ||Z|| <= 1/(1-c) = 1 + e1. Then
   Z' = r^(-2L-2) int_0^r x^(2L+2) Qt Z gives e2.
2. (b) U = (L+1)/r + Z' Z^-1, and ||Z' Z^-1|| <= e2/(1 - e1).
   - The Wronskian Phi^T Phi' - Phi'^T Phi is constant (Q is symmetric) and tends to 0 as r -> 0, because Phi ~ r^(L+1).
     So Phi^T Phi' is symmetric, and therefore so is U.
   - The eigenvalues of a real symmetric matrix are bounded by any induced norm.
3. (c) Phi(r) is invertible on (0, r0], since ||Z - I|| < 1/3.
   - U solves U' = (Q - lambda') - U^2.
   - Picone identity: |Psi'|^2 + Psi^T (Q - lambda') Psi = (Psi^T U Psi)' + |Psi' - U Psi|^2.
   - Integrate over [eps, r0]. The boundary term at eps is at most |U(eps)| |Psi(eps)|^2
     <= ((L+1)/eps + eta) eps int_0^eps |Psi'|^2, which tends to 0.
   - Density extends the inequality to the whole form domain.

**Use.**
- U_lo := (L+1)/r0 - eta (times I) satisfies U_lo <= U_{lambda'}(r0) for every lambda' covered by q. Replacing
  <U_{lambda'} c, c> by <U_lo c, c> lowers the [0, r0] contribution, so U_lo is the valid choice for the upper counts.
- U_hi := (L+1)/r0 + eta satisfies U_hi >= U_{lambda'}(r0). Extending a trial function on [r0, R] by the [0, r0]
  minimiser of (c) costs at most <U_hi c, c>, so U_hi is the valid choice for the lower counts.
- Code: ustart, bracket.py:28-37, with c < 1/4 asserted at 32. qbound, bracket.py:40-51, bounds
  ||Q - ell/r^2 - lambda'|| for all |lambda'| <= |lambda| + nu. The bound includes 3 s sg^2, ua, delta, sqrt2 sg and
  |lambda| + nu, and sums the two row bounds. Lemma 3.1 justifies sg and ua.
- The assertion (pi/r0)^2 > q + 1 (bracket.py:164-165), which is Dirichlet positivity on [0, r0], is consistent with
  (c) but not needed by it.
- Certified eta values, about 6.3e-5 (L+ at L = 0) and decreasing in L, are in `up_detail.eta` and `lo_detail.eta`
  (descriptive).

### Lemma 4.4 (BR-M: count on [r0, R] with the endpoint term)

**Statement.** Let Q be continuous and symmetric on [r0, R] (r0 > 0), U0 a symmetric Robin matrix, and
S = diag(0, L/R) (S = 0 in the scalar case). Consider

    b[Y] = int_r0^R (|Y'|^2 + Y^T (Q - lambda) Y) + <U0 Y(r0), Y(r0)> + <S Y(R), Y(R)> ,

on all of H^1 ("N") or on {Y : Y_a(R) = 0} ("D", Dirichlet in the a-channel). Let Phi solve
-Phi'' + (Q - lambda) Phi = 0 with Phi(r0) = I and Phi'(r0) = U0, and assume Phi(R) is invertible. Then

    n(b) = sum over rho in (r0, R) of dim ker Phi(rho)  +  n_-( (U(R) + S) restricted to F ) ,   U(R) = Phi'(R) Phi(R)^-1 ,

where F = R^n for N and F = {(0, c_w)} for D. **Endpoint restriction rule:** the Dirichlet-a problem keeps only the
w-direction, so its endpoint term is n_-(U(R)_ww + L/R). In the scalar Dirichlet case the endpoint term is 0.

**Proof.**
1. *Decomposition.* Let H_D := {Y : Y(R) = 0} and H_Phi := {Phi C : Phi(R) C in F}.
   - Each Y in the N or D space splits as Y = (Y - Phi C) + Phi C with C = Phi(R)^-1 Y(R). The condition
     Y(R) in F holds in both cases, so Phi C lies in H_Phi.
   - For Y_D in H_D, integration by parts gives b(Y_D, Phi C) = Y_D(R)^T(...) = 0, using that Phi C solves the
     equation and satisfies the left natural condition (Phi C)' = U0 (Phi C) at r0.
   - Likewise b[Phi C] = <(U(R) + S) c, c> with c = Phi(R) C, because the r0 boundary terms cancel.
   - U(R) is symmetric, by the Wronskian argument of Lemma 4.3.
2. *Additivity.* For a b-orthogonal sum of finite-index forms, n(b) = n(b|H_D) + n(b|H_Phi).
   - ">=": the sum of two negative definite b-orthogonal subspaces is negative definite.
   - "<=": take nonnegative complements P_D in H_D and P_Phi in H_Phi, of codimensions n(b|H_D) and n(b|H_Phi).
     Their sum P = P_D + P_Phi is b-nonnegative, because the cross terms vanish. A negative definite V meets P
     only in 0, so dim V <= codim P.
3. *Dirichlet part: the Morse index theorem.* For rho in (r0, R], let mu_1(rho) <= mu_2(rho) <= ... be the eigenvalues
   of the problem on [r0, rho] with the Robin U0 at r0 and Dirichlet conditions at rho.
   - 0 is an eigenvalue at rho iff Phi(rho) C = 0 for some C != 0, with multiplicity dim ker Phi(rho). The solutions
     satisfying the left condition are exactly the Phi C.
   - Each branch mu_k is continuous and strictly decreasing in rho (STANDARD, not opened: domain monotonicity with
     unique continuation).
   - For rho close to r0 all mu_k > 0, since U0 >= (L+1)/r0 - eta > 0 and the Poincare constant of [r0, rho] blows
     up.
   - So n(b|H_D) = #{k : mu_k(R) < 0}. That is the number of branch crossings of 0 in (r0, R), each zero of Phi
     counted with multiplicity dim ker Phi(rho). At R itself there is no crossing, since Phi(R) is invertible.
4. *Simple zeros.* Here n = 2 and d/dr det Phi = tr(adj(Phi) Phi'). If dim ker Phi(rho) = 2, then Phi(rho) = 0 and
   adj(Phi(rho)) = 0, so det Phi has at least a double zero. A zero certified simple (d/dr det != 0) therefore has
   dim ker = 1.

**Code (fact C5).**
- ZeroCounter, bracket.py:75-118. If the enclosure of det over a sub-interval excludes 0, there is no zero. Otherwise,
  if d/dr det excludes 0, det is strictly monotone there and has exactly one zero iff the endpoint enclosures (which
  must exclude 0) have opposite signs. Otherwise the sub-interval is bisected, down to depth 30, after which the count
  fails and returns None. A zero on a sub-interval boundary forces failure, so it cannot be double-counted.
- endpoint_term, bracket.py:121-155: checks det Phi(R) != 0 at 135, symmetrises U at 139, applies the D rule at
  141-145, and gives the 2x2 inertia from det and trace at 146-155 (scalar case at 123-132).
- count = conjugate points + endpoint term (bracket.py:182). The march covers [r0, R] exactly and raises otherwise
  (lincore.py:133-135).

### Theorem 4.5 (BR: brackets)

Let L >= 0, R in {10, 14}, and eps = 1/1000 exactly (bracket.py:280).

- **(U+) Upper count for L+.** If ext := |E| - m/R - delta_L(R) - eps > 0, then #(L+(L) < eps) <= U+. Here U+ is the
  count at level +eps of the interior problem on [r0, R] with a-shift -delta_L(R), Robin U_lo at r0, a'(R) = 0, and
  w'(R) = -(L/R) w(R), that is S = diag(0, L/R).
- **(L+) Lower count for L+.** #(L+(L) < -eps) >= the count at level -eps of the problem with no shift, Robin U_hi,
  a(R) = 0 and the same Robin condition on w.
- **(U-), (L-)** are the scalar analogues, with delta = 0 and S = 0.

Counting at +/- eps is rigorous for every eps > 0: #(T <= 0) <= #(T < eps) and #(T < 0) >= #(T < -eps).

**Proof of (U+).**
1. Let V be a k-dimensional subspace of the form domain with q+(a) - eps||a||^2 < 0 on V minus 0. For a in V, take
   w = w*(a) := -sqrt2 P_L^-1 (sigma_i a), which is linear in a. By Lemmas 4.1-4.2,
   q+(a) >= Q2^{delta,R}(a, w*).
2. Split Q2^{delta,R}(a, w*) - eps||a||^2 into an interior part and exterior parts:
   - the interior form on [0, R] at level eps in both channels, plus eps ||w*||^2 on [0, R], plus (L/R) w*(R)^2;
   - the exterior w-part, int_R^inf (w'^2 + ell w^2/r^2) - (L/R) w(R)^2 >= 0 (Lemma 4.2);
   - the exterior a-part, int_R^inf a'^2 + (ell/r^2 + 3 s sigma^2 - u - delta - eps) a^2 >= ext ||a||^2 on [R, inf),
     using (UB) and s >= 0.
   There is no exterior coupling, since sigma_i = 0 beyond R.
3. So the interior form, including the boundary term (L/R) w(R)^2, is < 0 on the image of V. By Lemma 4.3(c) at
   lambda' = eps, the [0, r0] piece is >= <U_lo c, c>, so the [r0, R] form with Robin U_lo is < 0 on the image too.
4. *Injectivity.* If the image of a were 0 on [r0, R], the same chain would give q+(a) - eps||a||^2 >= 0.
5. So that form has a k-dimensional negative subspace, and Lemma 4.4 counts it.

**Proof of (L+).**
1. Let V be a k-dimensional subspace for the D problem at level -eps. Extend each Y in V to [0, r0] by the
   minimiser of Lemma 4.3(c) at level -eps, which costs at most <U_hi c, c>. Extend to [R, inf) with a = 0 and
   w = w(R)(R/r)^L, which costs exactly (L/R) w(R)^2. For L = 0 the extended w is constant, which lies in the
   homogeneous space W_0 of Lemma 4.2.
2. Then Q2_L(a_ext, w_ext) < -eps ||(a, w)||^2_[0,R] <= -eps ||a_ext||^2.
3. Hence q+(a_ext) + eps||a_ext||^2 <= Q2_L + eps||a_ext||^2 < 0 (Lemma 4.2).
4. The map is injective: if a_ext = 0, then Q2_L = P_L[w] >= 0.

**Proof of (U-) and (L-).** Identical, with no w-channel. The exterior reserve is |E| - m/R - eps >= ext.

**Certified counts** (target-B.json `brackets.radii.<R>.<L>.<+|->.upper/lower`). R = 10 and R = 14 give identical
counts (C-R).

| L | U+ (conj + endpoint) | lower+ | U- | lower- | ext (R = 10) | ext (R = 14) |
|---|---|---|---|---|---|---|
| 0 | 2 (2 + 0) | 2 | 2 (2 + 0) | 1 | [1.10045 +/- 3.65e-6] | [1.73551 +/- 4.81e-6] |
| 1 | 2 (1 + 1) | 1 | 1 (1 + 0) | 1 | [1.15920 +/- 2.79e-6] | [1.73581 +/- 2.13e-6] |
| 2 | 1 (1 + 0) | 1 | 1 (1 + 0) | 1 | [1.17095 +/- 4.08e-6] | [1.73587 +/- 1.60e-6] |
| 3 | 0 | 0 | 0 | 0 | [1.17598 +/- 1.10e-6] | [1.73590 +/- 2.93e-6] |

The ext column is `ext_margin`, which equals |E| - m/R - delta - eps (bracket.py:292-294; referee-3 item 4).

### Corollary 4.6 (kernel booking; exact indices)

**Booking.** Ran 1_(-inf,0)(L-(0)) plus span(r sigma) is a subspace on which q- - eps||.||^2 < 0. By (K1), r sigma is
q--orthogonal to the negative spectral subspace. So n(L-(0)) + 1 <= U-(0), that is n(L-(0)) <= 1. In the same way
(K2) gives n(L+(1)) <= U+(1) - 1 = 1. In addition:
- n(L-(1)) <= 1;
- n(L+(2)) <= 1 and n(L-(2)) <= 1;
- L+(3) >= eps and L-(3) >= eps, in form sense, because #(L+-(3) < eps) = 0.

**Exact indices.** Combined with the lower counts:
- n(L+(L)) = 2, 1, 1, 0 and n(L-(L)) = 1, 1, 1, 0 for L = 0..3;
- dim ker L-(0) = 1 and dim ker L+(1) = 1;
- ker L+(0) = 0, ker L-(1) = 0 and ker L+-(2) = 0;
- with Lemma 7.1, everything vanishes for L >= 3.

This is the "ceiling" of the BAR: every upper count equals its lower count once the booked kernels are counted. It
also proves that the state is nondegenerate. Descriptive by-product; it is not used by the theorem.

### Theorem 4.7 (D0: the constrained count at L = 0)

**Statement.** n(L+(0) restricted to (r sigma)^perp) <= n(B) - 1 = 1. Here B is the interior 2x2 operator on
[r0, R] at level 0 with:
- a-shift -delta_0(R);
- Robin U_lo at r0, computed with nu = 1, so that U_lo <= U_{+1}(r0);
- natural conditions a'(R) = 0 and w'(R) = 0 (for L = 0 the exterior harmonic is a constant, so S = 0).

**Proof.**
1. Let g := r sigma and f in the form domain with <f, g> = 0. Let w = w*(f) as in Theorem 4.5, and split
   [0, r0] (index 1), [r0, R] (index 2) and [R, inf) (index e). Write Y2 = (f2, w2).
2. By Lemmas 4.1-4.3, with the [0, r0] form taken at level +nu (DtN U_{+nu} >= U_lo):

       q(f) >= B[Y2] + nu ||Y1||^2 + c_ext ||f_e||^2 >= B[Y2] + nu ||f1||^2 + c_ext ||f_e||^2 ,

   with c_ext := |E| - m/R - delta_0(R) > 0, the exterior a-reserve at level 0.
3. Since <f, g> = 0, <f2, g2> = -<f1, g1> - <f_e, g_e>. By Cauchy-Schwarz,
   |<f2, g2>|^2 <= (nu||f1||^2 + c_ext||f_e||^2)(||g1||^2/nu + ||g_e||^2/c_ext). Hence

       q(f) >= P(Y2) := B[Y2] + M |<Y2, G>|^2 ,   G := (g2, 0) ,   M := 1/(||g1||^2/nu + ||g_e||^2/c_ext) .

4. If q < 0 on a k-dimensional V inside g^perp, the map f -> Y2(f) is injective, since Y2 = 0 would force
   q(f) >= 0. So n(P) >= k.
5. *Inertia (Haynsworth), proved directly.* Assume B is invertible and let h := B^-1 G and d2 := <h, G> = B[h] < 0.
   - Every Y splits as Y = Z + t h, with t = <Y, G>/d2 and <Z, G> = 0.
   - Then B(Z, h) = <Z, G> = 0, so B[Y] = B[Z] + t^2 d2 and <Y, G> = t d2.
   - Therefore P(Y) = B[Z] + t^2 |d2| (M|d2| - 1).
   - If M|d2| > 1, then n(P) = n(B restricted to G^perp). Also n(B) = n(B restricted to G^perp) + 1, by additivity
     over the B-orthogonal sum G^perp + span(h), on which B[h] < 0.
   - Hence n(P) = n(B) - 1.

**Code and certified values** (target-B.json `brackets.radii.<R>.0.D0`; code fact C6).
- n(B) is the level-0 count, side lo, nu = 1 (bracket.py:196).
- B is invertible because det Phi'(R) != 0 (bracket.py:206-208). At L = 0 with Neumann conditions in both channels,
  0 is an eigenvalue iff Phi'(R) C = 0 for some C != 0.
- h = Phi C + F_p, where the forcing column F_p solves -Y'' + Q Y = (g, 0) with F_p(r0) = F_p'(r0) = 0
  (bracket.py:68-71, 171-173). So h satisfies the left Robin condition for every C, and
  C = -Phi'(R)^-1 F_p'(R) (bracket.py:205-210).
- d2 = sum over c of C_c int Phi_{a,c} g + int F_{p,a} g (bracket.py:211), from quadratures (make_sys 71).
- ||g1||^2 <= sg^2 r0^3/3 (bracket.py:224). ||g_e||^2 sums tube boxes over every step that meets [R, R1], whole steps
  included, plus the tail a1^2/(2 kappa1) (bracket.py:226-234).
- c_ext is ext0, passed unchanged (bracket.py:292, 303).

| R | n(B) | d2 | M | M\|d2\| | constrained upper |
|---|---|---|---|---|---|
| 10 | 2 | [-2.041380387 +/- 3.15e-10] | [555.4 +/- 0.0353] | [1133.8 +/- 0.09] | 1 |
| 14 | 2 | [-2.172289605 +/- 1.42e-10] | [2.198e+7 +/- 1.46e+3] | [4.775e+7 +/- 6.3e+3] | 1 |

M|d2| was recomputed by checks/check_assembly.py. As a descriptive cross-check, the float values of
<L+(0)^-1 r sigma, r sigma> from referee-3 and referee-4 are -2.1727 and -2.17285. They agree in sign. The certified d2
belongs to the cut operator B, so it is not expected to match them exactly.

**K(L).** With Corollary 4.6 and Theorem 4.7, and the definitions of verdict.py:36-51:
- K(0) = [n(B) - 1] + [U-(0) - 1] = 1 + 1 = 2 >= n(L | Y_0);
- K(1) = [U+(1) - 1] + U-(1) = 2 >= n(L | Y_1);
- K(2) = U+(2) + U-(2) = 2;
- K(3) = 0.

These hold at both radii (check_assembly.log; target_verdict.json `K`).

---

## 5. The Krein nodes I0-I2: certified eigenvalues i w with negative Krein sign

### 5.1 The matching system

For real w (the KREIN mode, match.py:5-8):

    a'' = V+ a - w d + 2 sigma psi ,   d'' = V- d - w a ,   psi'' = (ell/r^2) psi + sigma a ,

with V+ = ell/r^2 + 3 s sigma^2 - u and V- = ell/r^2 + s sigma^2 - u. In the tail-diagonal channels P = a + d and
Q = a - d (re-derived by this seat; match.py:22-26, 35-40):

    P'' = (Vb - w) P + s sigma^2 Q + 2 sigma psi ,   Q'' = s sigma^2 P + (Vb + w) Q + 2 sigma psi ,   psi'' = (ell/r^2) psi + (sigma/2)(P + Q) ,

with Vb = ell/r^2 + 2 s sigma^2 - u. Each channel has exponents (L+1, -L) at 0.

**Lemma 5.1 (matched solution => eigenvector).** Suppose X = (P, Q, psi) is a real, nonzero solution on (0, inf)
that lies in the 3-dimensional regular subspace at 0 (all channels ~ r^(L+1)). Suppose also that for r >= R1,
P, P', Q and Q' are O(e^{-mu r}) for some mu > 0, while psi and psi' are bounded. Then xi := (a, i d), with
a = (P+Q)/2 and d = (P-Q)/2, is an eigenvector of A_L with eigenvalue i w. Also a and d are real.

*Proof.*
1. h := psi - G_L(sigma a) solves h'' = ell h/r^2, so h = alpha r^(L+1) + beta r^-L.
2. Both psi and G_L(sigma a) are O(r^(L+1)) at 0, so h(0) = 0. Since r^-L does not vanish at 0 (it equals 1 when
   L = 0), beta = 0. Both are bounded at infinity, so alpha = 0. Hence psi = G_L(sigma a), and
   L+ a = w d, L- d = w a hold classically.
3. a and d are C^2, behave like r^(L+1) at 0, and decay exponentially together with their derivatives. So they lie
   in D(H0). In 3-D, (a/r) Y_LM is in H^2 (STANDARD regularity, not opened).

### 5.2 Regular side: second-order Frobenius start with the factor-2 slack

**Lemma 5.2.** On [0, r0], let Phi = r^(L+1) Z be the regular 6x6 fundamental solution (3 columns) of the system
above, with Z(0) = I and Qt := Q - ell/r^2 (KREIN entries: Vb - ell/r^2 -/+ w, s sigma^2, 2 sigma, sigma/2). Let
Z2 := Qt(0)/(2(2L+3)) and let R4 and R3 be the code's constants. Then

    |Z(r0) - I - r0^2 Z2| <= R4 ,   |Z'(r0) - 2 r0 Z2| <= R3   (entrywise),

and the same holds for d/dw with R4d and R3d. So the columns `cols_j` (match.py:96-103), and `dcols_j`
(match.py:105-113), enclose the normalised regular data Y_j(r0) = Z(r0) e_j and
Y_j'(r0) = ((L+1)/r0) Z(r0) e_j + Z'(r0) e_j (and their w-derivatives).

*True bounds.* Here sg and ua are as in Lemma 3.1, and |w| <= ap.
- q_t := max(row0, row2), with row0 = 2|s| sg^2 + ua + ap + |s| sg^2 + 2 sg and row2 = sg. This bounds ||Qt||_inf.
- e1_t := c_t/(1 - c_t), with c_t = r0^2 q_t/(2(2L+3)).
- y2_t := q_t (1 + e1_t)/(2(2L+3)), which bounds sup|Z - I|/r^2 by Lemma 4.3(a).
- dsig := F/6 and du := sg^2/6, so that |sigma - sigma0| <= dsig r^2 and |u - u0| <= du r^2 (Lemma 3.1).
- cq_t := max(3|s| 2 sg dsig + du + 2 dsig, dsig), which bounds ||Qt(r) - Qt(0)||/r^2. The bound uses
  |sigma^2 - sigma0^2| <= 2 sg dsig r^2.

*Proof.*
1. Write Z - I - V_L[Qt(0)] = V_L[(Qt - Qt(0)) Z] + V_L[Qt(0)(Z - I)]. The integrand is bounded by
   (cq_t (1 + e1_t) + q_t y2_t) x^2.
2. V_L[x^2](r) = r^4/(4(2L+5)) gives the true value remainder
   R4_t = r0^4 (cq_t (1 + e1_t) + q_t y2_t)/(4(2L+5)).
3. Z' - 2 r Z2 = r^(-2L-2) int x^(2L+2)(...) gives R3_t = r0^3 (same)/(2L+5).
4. For d/dw (|dQt/dw| = 1 entrywise on the diagonal), the same steps with D_t := sup|dZ|/r^2 give
   D_t <= ((1+e1_t)/(2(2L+3)))/(1 - q_t r0^2/(4(2L+5))). Then R4d_t = r0^4 (y2_t + q_t D_t)/(4(2L+5)) and
   R3d_t = r0^3 (y2_t + q_t D_t)/(2L+5).

*Factor-2 slack.* The code uses the following (match.py:55, 83-94):
- q = 2 row0 + sg >= 2 q_t, since row0 >= 2 sg >= row2;
- cq = 2(3|s| 2 sg dsig + du + 2 dsig) + dsig >= 2 cq_t;
- R4 = r0^4 (cq + q y2)/(4(2L+5)), which drops the factor (1 + e1) on cq;
- d2 = (1 + e1)/den, which drops the factor 1/(1 - q r0^2/(4(2L+5))).

c < 1/4 is asserted (match.py:58), so e1 < 1/3. Then:
- cq >= 2 cq_t >= (1 + e1_t) cq_t;
- q y2 >= q_t y2_t, by monotonicity;
- q d2 >= 2 q_t (1+e1)/den >= q_t D_t, since 1/(1 - q r0^2/(4(2L+5))) < 2.

So every code constant bounds its true counterpart. This is referee-3 item 5 and the docstring at match.py:86-89.

*Check.* checks/check_frob_slack.py evaluates both sides in ball arithmetic at the target, for L = 0, 1, 2 and
|w| <= 1.27, 0.96, 0.53 (plus the disc radius 0.002). The code/true ratios are about 3.1 to 3.6 for R4 and R3 and
about 2.10 for R4d and R3d. The result is ALL PASS (checks/check_frob_slack.log).

The regular fundamental matrix Fr is propagated from r0 to r_m = 8 from exact identity data (match.py:146-151), and
Reg_j = Fr cols_j.

### 5.3 TAIL-LIN: the certified decaying basis on [R1, inf)

Throughout, R := R1 = 26 (the tube end; the true point 26 lies in the ball `bj.r[-1]`). The channel parameters are
k_P^2 = |E| - w and k_Q^2 = |E| + w. Write -u = |E| - m/r + tau, with tau in [0, (m - m(r))/r] (F3). Then

- P-row: P'' = (k_P^2 - m/r + ell/r^2) P + (2 s sigma^2 + tau) P + s sigma^2 Q + 2 sigma psi;
- Q-row: the same with k_Q, and with P and Q exchanged in the coupling;
- psi-row: psi'' = (ell/r^2) psi + (sigma/2)(P + Q).

The model channels are y'' = W y, with W = k^2 - m/r + ell/r^2 for P and Q, and W = ell/r^2 for psi. For psi the
solutions are phi_d = (r/R)^-L and phi_g = (r/R)^(L+1).

**Lemma 5.3 (far-field Riccati; channel, tail.py:83-117).** Let rho := -y'/y, which solves rho' = rho^2 - W. Let
rho_N = sum_{n<=N} c_n r^-n, N = 10, be the truncated asymptotic series. The coefficients come from
riccati_coeffs (tail.py:40-58): c0 = +k (decaying) or -k (growing), with the principal square root, and
c_n = (W_n - sum_{i=1}^{n-1} c_i c_{n-i} - (n-1) c_{n-1})/(2 c0), with W_1 = -m and W_2 = ell. By construction,
res := rho_N^2 - W - rho_N' has only terms r^-j with j > N (residual_coeffs, tail.py:61-73). Set:
- res_max := sum |e_j| Rf^-j, which bounds sup over r >= Rf of |res| (tail.py:90-92);
- rho_min := inf over [Rf, inf) of Re(+/- rho_N), computed on 64 sub-balls covering t = 1/r in [0, 1/Rf]
  (tail.py:94-101).

Then:
- **(d)** If rho_min > 0 and res_max < rho_min^2, there is a unique solution rho_d with
  |rho_d - rho_N| <= eps_d := res_max/rho_min on [Rf, inf). phi_d = exp(-int rho_d) is the decaying solution, with
  Re rho_d >= rho_min - eps_d > 0.
- **(g)** For the growing sign, write c := rho_min and res_g := res_max. Suppose a solution has
  |rho(Rf) - rho_N(Rf)| <= eta0, and set eps_g := 2(eta0 + res_g/(2c)). If
  eta0 + (eps_g^2 + res_g)/(2c) <= eps_g and eps_g < c (tail.py:260-264), then the solution exists on [Rf, inf),
  stays within eps_g of rho_N, and has Re rho <= -(c - eps_g) < 0.

*Proof.*
1. Write rho = rho_N + eta. Then eta' = 2 rho_N eta + eta^2 + res.
2. **(d)** Take eta = -int_r^inf exp(-int_r^s 2 rho_N)(eta^2 + res) ds. On the ball sup|eta| <= eps_d this map sends
   the ball into itself, because (eps_d^2 + res_max)/(2 rho_min) <= eps_d iff res_max <= rho_min^2. It is a
   contraction with constant eps_d/rho_min = res_max/rho_min^2 < 1. Banach's theorem gives rho_d.
3. **(g)** Write eta(r) = e^{int 2 rho_N} eta0 + int_Rf^r e^{int_s^r 2 rho_N}(eta^2 + res). Then
   |eta| <= eta0 + (sup|eta|^2 + res_g)(1 - e^{-2c(r-Rf)})/(2c). The second factor is < 1, so a continuity argument
   keeps |eta| < eps_g for all r, and the solution cannot blow up.

**Lemma 5.4 (near field; channel_full, tail.py:236-273).** Take Rf = max(2 R1, 30 m/|k^2|) (tail.py:241-242).
- rho_d is integrated inward from the ball rho_d(Rf) in rho_N(Rf) + eps_d ball (tail.py:253) down to R1.
  ric_integrate (tail.py:192-223) does this with the centred (mean-value) Taylor step _ric_step (tail.py:171-189),
  which runs on top of the validated step _hoe (tail.py:145-164).
- The final step is the exact ball arb(r_to) - r and it is integrated (tail.py:208-209; referee-3 item 2).
- The outputs are an enclosure rd of rho_d(R1) and, from the step boxes, inf Re rho_d over [R1, Rf]
  (tail.py:216-219).
- The growing solution is **defined** by rho_g(R1) := rho_N^g(R1), the series value, which is analytic in w
  (tail.py:258). It is integrated forward to Rf (tail.py:259) and closed by Lemma 5.3(g), with
  eta0 = |rho_g(Rf) - rho_N^g(Rf)| (tail.py:260).
- The lemma returns, all kept in arb (no float() calls; referee-3 item 2b; tail.py:266-271):
  - cd := inf over [R1, inf) of Re rho_d >= min(path minimum, rho_min - eps_d);
  - sup over [R1, inf) of Re rho_g <= max(path maximum, -(c - eps_g));
  - gamma = cd - sup Re rho_g and G = 1/gamma;
  - Pmax >= sup |rho_d| and sup |rho_g|.
- The derivative d rho_d/d w is integrated along with rho_d, by d' = 2 rho d - dk^2/dw. Its starting value at Rf is
  the series derivative plus a Cauchy bound eps_d(disc)/gap (tail.py:248-254). The derivative d rho_g/dw is the exact
  series derivative (tail.py:258).

**Lemma 5.5 (coupled bounded solutions; lemma, tail.py:276-324).** Let mu := (1/2) min(cd, kappa1) (tail.py:310). Let
B_mu be the space of continuous X on [R, inf) with the norm

    N(X) := max( sup e^{mu(r-R)} |P| , sup e^{mu(r-R)} |Q| , sup |psi| ) .

In each channel define

    S[f](r) := phi_d(r) int_R^r phi_g f / W_r + phi_g(r) int_r^inf phi_d f / W_r ,

with W_r the (constant) Wronskian. Let X0_j be the model decaying solution in channel j, normalised by
phi_d(R) = 1. Then X0_j lies in B_mu with N(X0_j) = 1. The map X -> X0_j + S[B1 X], where B1 is the coupling written
above, is a contraction on B_mu with constant theta = max(theta_pq, theta_psi) < 1/2, where

    theta_pq = G (D1 + 2 S1) ,   D1 = 4|s| a1^2/(2 kappa1 R^2) + 2 a1^2/(4 kappa1^2 R) ,   S1 = (a1/R)/(kappa1 - mu) ,
    theta_psi = a1/((2L+1)(kappa1 + mu))      (tail.py:311-317).

Its fixed point X_j = X0_j + E_j solves the full system, with N(E_j) <= e_val := theta/(1-theta) (tail.py:320). At R
the bounds are:
- |E_{j,i}(R)| <= e_val;
- |E_{j,i}'(R)| <= e_der := max(Pmax G (D1 + 2 S1)/(1-theta), ((L+1)/(2L+1))(a1/R)/((kappa1+mu)(1-theta)))
  (tail.py:322-324).

*Proof.*
1. *Kernel bounds.* For s < r, |phi_d(r) phi_g(s)/W_r| = |phi_d(r)/phi_d(s)|/|rho_d(s) - rho_g(s)|
   <= G e^{-cd (r-s)}. For s > r, |phi_g(r) phi_d(s)/W_r| <= G |phi_g(r)/phi_g(s)| <= G, since Re rho_g < 0.
   In the psi channel, phi_d = (r/R)^-L and phi_g = (r/R)^(L+1) give W_r = (2L+1)/R. The kernel is
   s^(L+1) r^-L/(2L+1) <= s/(2L+1) for s < r, and r^(L+1) s^-L/(2L+1) = r (r/s)^L/(2L+1) <= s/(2L+1) for s > r.
2. *P and Q rows.* |B1 X| <= N(X) [ (3|s| sigma^2 + tau)(s) e^{-mu(s-R)} + 2 |sigma(s)| ].
   - First term: multiplying by e^{mu(r-R)}, both kernel factors e^{-(cd-mu)(r-s)} and e^{-(c_g+mu)(s-r)} are <= 1,
     because mu < cd.
   - The two integration ranges partition [R, inf), so this term contributes
     <= G int_R^inf (3|s| sigma^2 + tau) <= G D1. By Lemma 3.3(iii), int sigma^2 <= a1^2/(2 kappa1 R^2), and
     int tau <= int_R^inf (m - m(s))/s <= a1^2/(4 kappa1^2 R). The code's 4|s| and the factor 2 are conservative.
   - Second term, s < r: e^{mu(r-R)} e^{-cd(r-s)} |sigma(s)| = e^{-(cd-mu)(r-s)} e^{mu(s-R)} |sigma(s)|
     <= (a1/R) e^{-(kappa1 - mu)(s-R)}.
   - Second term, s > r: e^{mu(r-R)} <= e^{mu(s-R)} and the kernel factor is <= 1, giving the same bound.
   - Over the partition, the second term contributes <= 2 (a1/R)/(kappa1 - mu) = 2 S1 (the 2 comes from 2 sigma psi).
3. *psi row.* |f_psi| <= |sigma| e^{-mu(s-R)} N(X), and the kernel is <= s/(2L+1). With s |sigma(s)| = |a(s)|
   <= a1 e^{-kappa1(s-R)}, this gives <= a1/((2L+1)(kappa1 + mu)) N(X).
4. The map is affine, so the same bounds give the contraction. The fixed point satisfies
   X'' = W_model X + B1 X by variation of parameters.
5. N(E_j) <= theta N(X_j) <= theta (1 + N(E_j)).
6. *Derivatives at R.* S[f]'(R) = phi_g'(R) int_R^inf phi_d f/W_r = -rho_g(R) S[f](R), because the boundary terms
   cancel. So |E'| <= |rho_g(R)| |E(R)| <= Pmax theta_pq/(1-theta) in the P and Q channels, and
   ((L+1)/R)|E_psi(R)| in the psi channel. The R-anchoring shows that E_j(R) actually lies along the growing
   directions; the code does not use this and treats (e_val, e_der) as a general error, which is weaker and valid.

**Lemma 5.6 (renormalisation; tail.py:325-351; vectors, tail.py:359-388).**
1. In channel i, decompose an error (e, e') with |e| <= e_val and |e'| <= e_der along v_d = (1, -rho_d,i(R)) and
   v_g = (1, -rho_g,i(R)) as e = alpha v_d + beta v_g. Solving gives
   - |alpha| <= dP_i := (e_der + |rho_g| e_val)/|rho_d - rho_g|;
   - |beta| <= tt_i := (e_der + |rho_d| e_val)/|rho_d - rho_g| (tail.py:342-346).
   For psi, rho_d = L/R and rho_g = -(L+1)/R.
2. Then X_j(R) = Xhat_j + sum_i alpha_ji Xhat_i + sum_i beta_ji G_i, where Xhat_j = v_d in channel j and
   G_i = v_g in channel i.
3. If 3 dPmax < 1/2 (tail.py:347), then (I + alpha) is invertible with ||(I+alpha)^-1|| <= Ainv := 1/(1 - 3 dPmax)
   in both the 1-norm and the infinity-norm (tail.py:351).
4. X~ := X (I+alpha)^-1 satisfies X~_j(R) = Xhat_j + sum_i t~_ij G_i with |t~_ij| <= Tt := 3 Tmax/(1 - 3 dPmax)
   (tail.py:350).
5. The X~_j are three linearly independent decaying solutions. If sum beta_j X~_j(R) = 0, then in each channel
   beta_i v_d + (sum_j t~_ij beta_j) v_g = 0, so beta_i = 0, since v_d and v_g are independent.
6. Xhat_j and G_i are integrated inward from R1 to r_m as separate columns of the fundamental matrix
   (match.py:162-169). The t~ uncertainty therefore never multiplies an inward-growing direction.

**Lemma 5.7 (uniform in w on a complex disc; Cauchy bounds).** krein.py:41 builds the disc D, a square of half-width
0.002 about the box centre. When it is passed (match.py:155-157), every constant in Lemmas 5.3-5.6 is computed on D:
- cpD and cqD (tail.py:300-307) feed cd, G, Pmax, rdB, rgB and hence Tt;
- the far-field eps also enters the derivative (tail.py:248-252).

rho_d is a uniform limit of analytic functions, rho_g is defined by an analytic value, and the contraction is uniform
on D. So X_j, alpha, beta and t~ are analytic on D. For w in the box, the closed disc of radius gap = 0.002 - box_r
lies in D, so |dt~/dw| <= Tt/gap (tail.py:387). With the variational columns of the fundamental matrix
(match.py:43, 172-180), this gives the enclosure dM of dM/dw over the box.

**Lemma 5.8 (eigenfunction tail for <a, d>; krein.py:56-61).** For X = sum_j beta_j X~_j on [R1, inf):

    N(X) <= Ainv (sum |beta_j|)/(1 - theta) ,

because N(X_k) <= 1/(1-theta) and ||(I+alpha)^-1||_1 <= Ainv. Hence

    | int_R1^inf (P^2 - Q^2)/4 | <= (1/4) int (|P|^2 + |Q|^2) <= N(X)^2/(4 mu) <= tailb/2 ,

with tailb := (Ainv sum|beta|)^2/((1-theta)^2 2 mu). The code adds tailb times a unit ball, which is conservative by a
factor 2 (as referee-3 noted).

### 5.4 Krawczyk on (w, v), and what K(X) in int(X) proves

Let M(w) = [Reg(r_m) | Dec(r_m)] be the 6x6 matrix (match.py:169-170). Its columns are the three regular solutions
and the three renormalised decaying solutions X~_j, each given as values and derivatives in (P, Q, psi) at r_m = 8.
M(w) is a well-defined real-analytic function of real w. The enclosure Mb over a box W contains M(w) for every w in
W, because t~ is replaced by a Tt-ball. dMb likewise contains dM/dw.

Work with the unknowns x = (w, y_j for j != k0), with v = D y, where D is a diagonal matrix of exact powers of two
(kraw.py:109), and set F(x) = M(w) D y with y_k0 = 1. Take a point x~ in X, any matrix C (a float inverse), and
J(X) = [dM(W) D Y | M(W) D e_j, j != k0] (kraw.py:94), which contains F'(x) for all x in X. The Krawczyk operator is
K(X) = x~ - C F(x~) + (I - C J(X))(X - x~) (kraw.py:102).

**Lemma 5.9.** If K(X) lies in int(X), componentwise (kraw.py:103), then F has a zero in X (Krawczyk 1969; Moore;
Rump: STANDARD, not opened). The zero is unique and J is regular there, but neither fact is used.

**Consequence.** There are w* in W and v* = (alpha*, beta*) with M(w*) v* = 0 and v*_k0 = 1.
1. Reg alpha* and -Dec beta* agree in value and derivative at r_m. By uniqueness for linear ODEs they form one
   solution on (0, inf).
2. That solution is regular at 0. On [R1, inf) it is a combination of the X~_j, so P and Q are O(e^{-mu r}) and psi
   is bounded.
3. It is nonzero: if alpha* = 0, then Dec beta* = 0 at r_m with beta* != 0, which contradicts Lemma 5.6.
4. By Lemma 5.1, i w* is an eigenvalue of A_L with a real eigenvector xi = (a, i d).
5. 0 < w* < |E| is certified in arb (krein.py:65; `in_gap = true`).

This is what the finite computation proves about the infinite-domain problem. The far-field matching makes "M(w*) is
singular" equivalent to "an L^2 solution exists" in the direction we use. The converse direction (no other
eigenvalues) is neither claimed nor needed.

### 5.5 The Krein sign

**Lemma 5.10.** <L xi, xi> = 2 w* <a, d>.

*Proof.* <L xi, xi> = <L+ a, a> + <L-(i d), i d> = w*<d, a> + <L- d, d> = w*<d, a> + w*<a, d>, with a and d real.

The sign does not depend on the normalisation. <a, d> = int_0^inf a d = (1/4) int (P^2 - Q^2), split into four
intervals:
- **[0, r0]:** |P_i|, |Q_i| <= ||Z|| <= 1 + e1 for the normalised regular columns, so each entry of the integrand is
  <= (1+e1)^2/2 < 8. The code uses 8 r0 times a unit ball (match.py:185).
- **[r0, r_m]:** Gram quadratures of the fundamental matrix contracted with cols (match.py:182-187), giving
  q1 = alpha^T G_reg alpha (krein.py:56).
- **[r_m, R1]:** -(1/4) times the inward quadratures, expanded in Xhat and G with t~ replaced by Tt-balls
  (match.py:188-201), giving q2 = beta^T G_dec beta (krein.py:57).
- **[R1, inf):** Lemma 5.8.

The certified values follow (target-K<L>.json `neg` and `pos`). w is taken from the final Krawczyk `refine` line of
target-K<L>.log, which is an outward arb string. The JSON `w` strings are not enclosures (GAP C2).

| L | role | w (Krawczyk box) | <a, d> | tail bound | theta | Tt |
|---|---|---|---|---|---|---|
| 0 | I0 (neg) | [1.10491108047488 +/- 4.15e-15] | -3.061281342e-6 +/- 4.63e-13 | 2.44e-20 | 3.69e-12 | 4.37e-11 |
| 0 | PK0 (pos) | [1.25921337137566 +/- 6.39e-15] | +4.507783361e-7 +/- 5.77e-13 | 5.61e-19 | 3.75e-12 | 4.59e-11 |
| 1 | I1 (neg) | [0.539925668013455 +/- 2.97e-16] | -6.212149350e-5 +/- 1.10e-13 | 8.69e-24 | 1.17e-12 | 1.39e-11 |
| 1 | PK1 (pos) | [0.951028237700108 +/- 2.59e-16] | +1.018646815e-4 +/- 2.29e-13 | 1.10e-19 | 1.21e-12 | 1.52e-11 |
| 2 | I2 (neg) | [0.2968148506 +/- 6.42e-11] | -2.403151062e-4 +/- 1.86e-7 | 1.84e-7 | 6.86e-13 | 8.13e-12 |
| 2 | PK2 (pos) | [0.5179458643 +/- 7.13e-11] | +6.296727417e-5 +/- 5.82e-8 | 5.77e-8 | 6.98e-13 | 8.45e-12 |

|E| = 3.10544... All six w lie in (0, |E|). The signs are decided in arb (krein.py:63). The positive-Krein co-batched
controls PK0-PK2 come out positive, as the BAR requires. The negative-Krein eigenvalues give, for each L in
{0, 1, 2}, an eigenvector xi_L with <L xi_L, xi_L> < 0 and eigenvalue i w with w > 0.

---

## 6. ESS and IDX

### Lemma 6.1 (ESS, with the referee-4 fix; in each sector and in 3-D)

**Statement.** Let Omega := C minus (i(-inf, -|E|] union i[|E|, inf)), which is open and connected. Let A = J L act
either in a sector or in 3-D, with A0 := J diag(H0, H0). Then:
- (a) for lambda in Omega, A0 - lambda is invertible, A - lambda = (I + K(lambda))(A0 - lambda), and
  K(lambda) := J V (A0 - lambda)^-1 is compact and analytic on Omega;
- (b) the eigenvectors of A with Re lambda > 0 (or with Re lambda < 0) span a space of dimension at most
  N0(L) := dim Ran 1_(-inf,0](L) < inf;
- (c) sigma(A) intersected with Omega is a discrete set of eigenvalues, each with a finite-rank Riesz projection
  P_lambda. In particular, every point of the spectrum with Re lambda != 0 is such an eigenvalue.

**Proof.**
1. **(a)** (A0)^2 = -diag(H0^2, H0^2), and A0 commutes with A0 + lambda, so (A0 - lambda)(A0 + lambda) =
   -(H0^2 + lambda^2) = -(H0 + i lambda)(H0 - i lambda). This is invertible iff +/- i lambda is not in
   sigma(H0), which is contained in [|E|, inf). So
   (A0 - lambda)^-1 = -(A0 + lambda)(H0^2 + lambda^2)^-1, which maps L^2 into D(H0)^2 boundedly.
   - V = diag(V+, V-) is bounded. Its multiplication parts s sigma^2 and (E - u) tend to 0 at infinity, which makes
     them relatively compact with respect to H0 (STANDARD, not opened). The part 2 sigma P_L^-1 sigma is
     Hilbert-Schmidt: in a sector by Lemma 4.1; in 3-D the kernel is sigma(x) sigma(y)/(2 pi |x - y|), whose HS norm
     is finite because int sigma^2(y)/|x-y|^2 dy <= 4 pi ||sigma||_inf^2 + ||sigma||_2^2.
   - Hence K(lambda) is compact, and it is analytic in lambda.
2. **(b)** (This is the referee-4 fix.) Let x_k be eigenvectors with eigenvalues lambda_k, all with Re lambda_k > 0.
   - By Theorem 6.2(ii) below, (lambda_j + conj lambda_k) <L x_j, x_k> = 0, so their span W is L-isotropic.
   - Let H_+ be the spectral subspace of L for (0, inf). For x != 0 in H_+ intersected with D(L), <L x, x> > 0.
     So W meets H_+ only in 0, and dim W <= codim H_+ = N0(L).
   - N0(L) is finite, and the proof does not use Weyl's theorem: Ran 1_(-inf,0](L+-(L)) is a subspace on which
     q+- - eps||.||^2 < 0, so its dimension is at most U+-(L) by Theorem 4.5.
     - N0(L(L)) <= U+(L) + U-(L), which is 4, 3, 2 and 0 for L = 0..3.
     - N0(L(L)) = 0 for L >= 3, by Corollary 7.2.
     - In 3-D, N0 <= 1x4 + 3x3 + 5x2 = 23.
   - The same argument works for Re lambda < 0.
3. **(c)** By (b), only finitely many points with Re lambda > 0 are eigenvalues. Pick lambda1 in Omega with
   Re lambda1 > 0 that is not one of them.
   - I + K(lambda1) is Fredholm of index 0. It is injective: if (I + K) y = 0, then x := (A0 - lambda1)^-1 y solves
     (A - lambda1) x = 0, so x = 0 and y = 0. Hence I + K(lambda1) is invertible.
   - The analytic Fredholm theorem (STANDARD, not opened) then gives the conclusion: (I + K(lambda))^-1 is
     meromorphic on Omega with finite-rank principal parts, so (A - lambda)^-1 = (A0 - lambda)^-1 (I + K)^-1 has
     the same property.

"Complement connected" alone is not enough (referee-4 item B). Step (b) supplies the resolvent point that step (c)
needs.

### Theorem 6.2 (IDX: direct index argument)

**Statement.** Fix a sector (L, M) and let N_+ := the sum of dim Ran P_lambda over all eigenvalues with
Re lambda > 0. N_+ is finite by Lemma 6.1. Let xi be an eigenvector for i w (w > 0) with <L xi, xi> < 0. Then

    N_+ + 2 <= n(L | Y_L) .

**Notation.** [x, y] := <J^-1 x, y> is a bounded sesquilinear form on X^2, and omega(x, y) := <L x, y> = [A x, y] for
x in D(A).
- For x, y in D(A): [x, A y] = <J^-1 x, J L y> = <J^T J^-1 x, L y> = -<x, L y>. So [A x, y] = -[x, A y].
- With R(mu) := (A - mu)^-1, this gives [R(mu) x, y] = -[x, R(-conj mu) y] for all x, y. To see this, apply
  [(A - mu) x', y'] = -[x', (A + conj mu) y'] to x' = R(mu) x and y' = R(-conj mu) y.
- Integrating over a small circle around lambda (the circle maps to a clockwise circle around -conj lambda) gives the
  Riesz identity

      [P_lambda x, y] = [x, P_{-conj lambda} y] ,   hence   omega(P_lambda x, y) = omega(x, P_{-conj lambda} y)

  for x in D(A). Here P_nu := 0 if nu is not in sigma(A).
- The resolvent at -conj mu exists whenever it exists at mu. Indeed A^* = -L J and J^-1 A J = L J = -A^*, so
  sigma(A) = -conj sigma(A). This holds per sector and in 3-D.

**Proof.**
1. **(i) Root spaces lie in Y.** For L >= 1 there is nothing to prove. For L = 0, let f(x) := <x_a, r sigma>. For
   x in D(A), f(A x) = <L- x_c, r sigma> = <x_c, L- r sigma> = 0 by (K1). If lambda != 0, A is invertible on the
   finite-dimensional invariant space Ran P_lambda, so every x in it equals A y with y in Ran P_lambda, and
   f(x) = 0. For the eigenvector xi, xi = A(xi/(i w)), so f(xi) = 0.
2. **(ii) Isotropy.** For x in Ran P_lambda and y in Ran P_mu, omega(x, y) = omega(x, P_{-conj lambda} P_mu y) = 0
   unless mu = -conj lambda. So E_+ := the sum of Ran P_lambda over Re lambda > 0 is omega-isotropic, and so is
   E_-, the sum over Re lambda < 0. The same computation for eigenvectors gives
   (lambda + conj mu) omega(x, y) = 0, which is what Lemma 6.1(b) uses.
3. **(iii) A negative N_+-plane.**
   - Let x be in E_+ with omega(x, E_-) = 0. For every y in D(A), omega(x, y) is the sum over Re lambda > 0 of
     omega(x, P_{-conj lambda} y), and each P_{-conj lambda} y lies in E_-. So omega(x, y) = 0.
   - D(A) is dense, so L x = 0 and A x = 0. A is invertible on E_+, so x = 0.
   - Symmetrically for E_-. So the pairing E_+ x E_- -> C is nondegenerate and dim E_- = N_+.
   - On E_+ + E_-, omega has the block matrix [[0, B], [B^*, 0]] with B invertible, whose eigenvalues are
     +/- (singular values of B). So E_+ + E_- contains a negative definite subspace V1 of complex dimension N_+.
4. **(iv) The Krein 2-plane.**
   - For x in Ran P_lambda with Re lambda != 0: omega(x, xi) = omega(x, P_{-conj lambda} xi) = 0, since
     -conj lambda != i w and the Riesz projection annihilates eigenvectors of other eigenvalues. Likewise for
     conj xi, which is an eigenvector for -i w.
   - omega(xi, conj xi) = [A xi, conj xi] = i w [xi, conj xi], and also = -[xi, A conj xi] = -i w [xi, conj xi].
     So [xi, conj xi] = 0 and omega(xi, conj xi) = 0.
   - omega(conj xi, conj xi) = omega(xi, xi) < 0, since L is real.
   - So Z_C = span_C(xi, conj xi) is negative definite. It is the complexification of span_R(Re xi, Im xi), which here
     is span((a, 0), (0, d)), the referee-3 reading.
5. **(v) Conclusion.**
   - V1 + Z_C is an omega-orthogonal sum of negative definite spaces, so it is negative definite. It has complex
     dimension N_+ + 2, because root vectors of distinct eigenvalues are independent.
   - It lies in the complexification of Y intersected with D(A), by step (i).
   - For a real symmetric form, the maximal dimension of a complex negative definite subspace of the
     complexification equals the real index (the spectral multiplicities are the same).

**Application.** At L = 0, 1, 2, Section 5 supplies xi with <L xi, xi> < 0, and Section 4 gives
n(L | Y_L) <= K(L) = 2. So N_+ + 2 <= 2, that is **N_+ = 0**. With Lemma 6.1(c), the spectrum of A_L has no point
with Re lambda > 0. No parity theorem is used. No algebraic simplicity of i w is used. The positive-Krein
eigenvalues are not used. Each (L, M) sector, for every M, has the same radial problem (paper:975).

---

## 7. TAIL (L >= 3), SECT, and the 3-D statement

### Lemma 7.1 (M: monotonicity in L, including the nonlocal term)

**Statement.** For f in the common form domain (H^1_0 for L >= 1):

    q+_{L+1}(f) >= q+_L(f) + 2(L+1) int f^2/r^2   and   q-_{L+1}(f) = q-_L(f) + 2(L+1) int f^2/r^2 .

**Proof.** For L-, ell(L+1) - ell(L) = 2(L+1). For L+, use Lemma 4.2:
Q2_{L+1}(f, w) = Q2_L(f, w) + 2(L+1) int (f^2 + w^2)/r^2 >= Q2_L(f, w) + 2(L+1) int f^2/r^2. Also
W_{L+1} is contained in W_L, since its norm is larger. Taking the infimum over W_{L+1}, which is at least the
infimum over W_L, gives the claim. Equivalently, P_{L+1} >= P_L implies <g, P_{L+1}^-1 g> <= <g, P_L^-1 g>, by the
variational formula of Lemma 4.2 (referee-3 item 8).

### Corollary 7.2 (TAIL)

L+-(3) >= eps (Corollary 4.6). By Lemma 7.1, L+-(L) >= eps for every L >= 3. If A x = lambda x with
Re lambda != 0 in such a sector, then (lambda + conj lambda)[x, x] = 0, so <L x, x> = lambda [x, x] = 0, and hence
x = 0. With Lemma 6.1(c), these sectors have no spectrum off the imaginary axis.

### Theorem 7.3 (3-D)

**Statement.** sigma(A) intersected with {Re lambda > 0} is empty, and sigma(A) is contained in iR.

**Proof.**
1. By Lemma 6.1 in 3-D, with N0 <= 23, any spectral point with Re lambda > 0 is an eigenvalue with eigenvector x in
   H^2(R^3)^2.
2. **SECT.** The orthogonal projections Pi_LM onto the sectors commute with A. This is because A is the direct sum of
   the A_L by paper (35)-(37): the background is radial, and Delta, multiplication by radial functions and the
   radial-kernel convolution Delta^-1 commute with rotations.
3. So Pi_LM x lies in D(A) and A Pi_LM x = lambda Pi_LM x. Some Pi_LM x != 0, which gives a sector eigenvalue with
   Re lambda > 0. That contradicts Theorem 6.2 for L <= 2 and Corollary 7.2 for L >= 3.
4. **Symmetry.** A^* = -L J, and J^-1 A J = L J = -A^*. So sigma(A) = sigma(-A^*) = -conj sigma(A), and there is no
   spectrum with Re lambda < 0 either.

This is the 3-D version of ESS that referee-4 asked for (item C): without it, a direct sum over infinitely many L
could carry spectrum that is not an eigenvalue of any single sector.

---

## 8. Remark on the controls: C-P3 realness via K(2) <= 1 (referee-4 item E)

C-P3 (Schroedinger-Poisson, s = 0, n = 1, sigma0 = 1, L = 2) certifies two things:
- K(2) = U+(2) + U-(2) = 1 at R = 20 and R = 28 (controls_verdict.json `C-P3.K2`);
- a complex Krawczyk box containing exactly one zero lambda* of M(lambda) v = 0, with
  Re lambda* in 0.09917673961 +/- 8.69e-13 and lower end > 0 (`lam_re`; cal/C-P3.json `evans.re_lower`).

Every lemma above holds for s >= 0, and the C-P3 background is existence-certified (cal/C-P3.json
`B.existence_certified = true`). Suppose Im lambda* != 0. Then lambda* and conj lambda* are distinct eigenvalues
(A is real) with Re > 0. Then N_+ >= 2 > K(2) >= n(L | Y) >= N_+, by Theorem 6.2 with no Krein term. That is a
contradiction, so lambda* is real.

This argument replaces the float flag `center_on_real_axis` (evans.py:48), which verdict.py:125 reads. It needs no
conjugate-symmetry-in-the-box step. The code is unchanged: this is a control, not on the target path, and C-P3 is
scored as sealed. The same reading applies to C-P2: K(0) <= 2 and a certified non-real lambda with Re > 0 give exactly
one quartet.

---

## 9. Assembly

### 9.1 Certified quantities used

| quantity | value | source (file: key) | used in |
|---|---|---|---|
| tube sha256 | f8b0cc27...ce28b, identical in all four target outputs | target-B.json `B.tube_sha256`, `brackets.tube_sha256`; target-K<L>.json `tube_sha256` | all |
| escape at u_lo | "escape", zeros 1 | target-B.json `B.classify.lo` | 3.2 |
| n+1 zeros at u_hi | "zeros", zeros 2 | `B.classify.hi` | 3.2 |
| existence certified | true | `B.existence_certified` | 3.2 |
| zeros on [0, 26] | 1 | `B.zeros` | 3.2 |
| a(R1) < 0, u(R1) < 0 | true; u(R1) = [-2.36856669502 +/- 2.38e-12] | `B.tail_ok`, `B.u_R1` | 3.2, 3.3 |
| kappa1 | [1.53901484561 +/- 4.69e-12] | `B.kappa1` | 3.3, 5.5 |
| a1 | [7.75859535966e-12 +/- 3.43e-24] | `B.a1` | 3.3, 4.7, 5.5 |
| E | [-3.10544025447 +/- 3.02e-12] | `B.E` | 4.5, 5, 6 |
| m | [19.1587125456 +/- 4.04e-11] | `B.m` | 4.5, 5.3 |
| I1 | [7.04446382985 +/- 3.92e-12] | `B.I1` | 4.1 |
| delta_L(R) | table in 4.1 | `brackets.radii.<R>.<L>.delta` | 4.5, 4.7 |
| ext margins | table in 4.5, all > 0 | `brackets.radii.<R>.<L>.ext_margin`, `ext_ok` | 4.5 |
| counts U+-, lower+- | table in 4.5 | `brackets.radii.<R>.<L>.<+-\|>.upper/lower`, `up_detail`, `lo_detail` (`ok = true`) | 4.5, 4.6 |
| D0 | n(B) = 2, d2 < 0, M\|d2\| > 1 at both R | `brackets.radii.<R>.0.D0` | 4.7 |
| K(L) | (2, 2, 2, 0) | target_verdict.json `K`; recomputed in check_assembly.log | 6.2 |
| I0, I1, I2 | w in (0, \|E\|), <a, d> < 0 | target-K<L>.json `neg.ok`, `neg.in_gap`, `neg.krein_sign`, `neg.krein_ad`; w from target-K<L>.log refine line | 5, 6.2 |
| PK0, PK1, PK2 | <a, d> > 0 | target-K<L>.json `pos.*` | controls |
| D1 = 3m/4 | [14.3690344092 +/- 3.03e-11] > 0 | target-B.json `D1` | BAR only (not needed by IDX at L = 1) |
| controls | C-B1, C-B2, C-P1, C-P2, C-P3, NULL: PASS | controls_verdict.json | VOID gate only |

### 9.2 The chain

1. **Background.** Lemmas 3.1-3.3 give a decaying one-node state for each u0* in U0, with E < 0 and certified tails.
2. **Brackets.** Lemmas 4.1-4.4 and Theorem 4.5 give the upper counts. With the kernel booking (Corollary 4.6) and D0
   (Theorem 4.7), n(L | Y_L) <= K(L) = 2 for L = 0, 1, 2, and L+-(3) >= eps.
3. **Krein nodes.** Lemmas 5.1-5.10 give, for L = 0, 1, 2, an eigenvalue i w_L with 0 < w_L < |E| and a real
   eigenvector of negative Krein sign.
4. **ESS.** Lemma 6.1 gives finite-rank Riesz projections off the imaginary axis.
5. **IDX.** Theorem 6.2 gives N_+ + 2 <= 2, so N_+ = 0, in every sector with L <= 2 and every M.
6. **TAIL.** Lemma 7.1 and Corollary 7.2 settle L >= 3.
7. **3-D.** Lemma 6.1 in 3-D and SECT (Theorem 7.3) give that the spectrum of J L on L^2(R^3) has no point with
   Re lambda > 0, and that it lies on iR.

Everything in steps 1-7 rests on the code facts of section 10. Those are now audited: audit-1 audited C1, C4 and C9,
and referee-5 audited C5-C8 and C10. The remaining scope is listed in GAP B1'. The argument also rests on the STANDARD
results
listed in GAP B2.

---

## 10. Code facts the proofs rely on (for the audit seat)

Each item is a property the text above assumes about build-2 as hashed in RUN.md.

- **C1 (itaylor.bg_step, itaylor.py:134-152).** If head + f^[K+1](rI, B) T^(K+1) lies in int(B) for
  T = hull(0, h), then the solution from every state in Y0 exists on [r, r+h], stays in B, and Y1 encloses it at
  r + h.
  - This must hold for ball-valued base points rc in the following sense: the tube's grid ball r_i contains a real
    point rho_i, Y_i encloses the state at rho_i for every u0 in U0, B_i encloses the state on [rho_i, rho_{i+1}],
    and rho_{i+1} - rho_i lies in the stored step h_i.
  - The last step ends exactly at 26 (bg_tube.py:149-151, 188).
  - The jet recursions bg_jets (itaylor.py:115-131) are the Taylor coefficients of (2.1) plus the quadratures.
- **C2 (bg_tube.series_start, bg_tube.py:68-113).** The returned ball contains the state at r0 for every u0 in U0, and
  the crude enclosure contains sigma and u on [0, r0].
- **C3 (bg_tube.integrate and finish, bg_tube.py:136-189 and 286-326).** The zero rule of Lemma 3.2; the escape and
  n+1-zeros classification; the formulas of Lemma 3.3. ser/deser are outward (bg_tube.py:335-350), so every decoded
  ball contains the encoded one.
- **C4 (itaylor.lin_step and eval_sub, itaylor.py:259-291; lincore.march, lincore.py:82-136).**
  - For every column and quadrature c, c(r+t) lies in sum C_k t^k + t^(K+1) R for t in hull(0, h).
  - The coefficient jets come from the tube state at the grid point (pt) and from the step box (box)
    (lincore.py:31-50).
  - The march reaches r_to exactly (lincore.py:133-135).
  - The combined jets of lincore.scaled (lincore.py:65-79) are the stated coefficient functions.
- **C5 (bracket.ZeroCounter, endpoint_term and count, bracket.py:75-185).** As stated after Lemma 4.4. Also: the
  columns start with Y = I and Y' = U (bracket.py:166-170), and make_sys builds exactly Q - lambda with the shift in
  the a-channel only (bracket.py:54-65).
- **C6 (bracket.d0_node and gnorms, bracket.py:188-234; run, bracket.py:273-310).** As stated after Theorem 4.7.
  Also: I_in is taken at a grid point certified <= R (bracket.py:287-288); ext = ext0 - eps gates the upper counts
  (bracket.py:292-299).
- **C7 (match.system and frob_start, match.py:21-114).** The P/Q/psi system as in 5.1, with the variational columns
  (match.py:43). frob_start encloses the normalised regular data (Lemma 5.2).
- **C8 (match.matrix, match.py:131-202).** Reg = Fr cols; Dec = Fd (Xhat + Tt-ball G); dM; the Gram matrices with
  the b0 = 8 r0 ball on [0, r0] and the sign of the inward quadrature.
- **C9 (tail.py).**
  - Lemmas 5.3-5.7 as implemented: the series and residual recursions (40-73); the sub-ball covering (94-101 and
    108-114); the HOE and centred mean-value Riccati step, which treats E, m and w as parameters through the
    variational quantities (120-189); the exact final step (208-209); the closure tests (260-268); the constants
    (309-351).
  - **Consistency requirement for the audit.** match.matrix calls lemma(mode, acb(par), E, m, ...) with E and m the
    tube balls, and the model channels in tail.py use exactly W = |E| -/+ w - m/r + ell/r^2. The perturbation
    tau = m/r - (u - E) and the sigma^2 terms must be the only terms put into D1.
- **C10 (kraw.test and certify, kraw.py:70-154; krein.krawczyk, krein.py:46-70).**
  - K(X) is formed as stated, with C any matrix. The test is componentwise contains_interior. v = D y with D exact
    powers of two.
  - The box Mb and dMb come from evalbox over the same real box W, with the disc of Lemma 5.7.
  - q1, q2 and tailb are as in 5.5. sign and in_gap are decided in arb.
- **C11 (assemble.py).** Every target job rebuilds the tube in-run (assemble.py:144-145). sigma0 enters only through
  itaylor.exact (9/5) (itaylor.py:27-34; assemble.py:30).

Audit-1 (core/seats/audit-1/) is auditing C1, C4 and C9. C2, C3, C5-C8, C10 and C11 are checked here at the formula
level only. This was the v1 wording. In v2: audit-1 (AUDIT-ENGINES.md) audited C1, C4 and C9 and found them
CORRECT. Referee-5 audited bracket.py (C5, C6), kraw (C10), the krein Gram and tail (C10), match.matrix (C8),
frob_start (C7) and the series_start derivation (C2) operation by operation. See GAP B1'.

---

## 11. Referee items addressed

| item | what this text does |
|---|---|
| ref-3 must-change 1 (sigma0 exact) | fixed in build-2 (PATCHES item 1); the theorem is stated at 9/5, and assemble.py:30 asserts it |
| ref-3 2 (tail.py exact last step, no float on bounds) | fixed (tail.py:208-209, 266-267, 309-310); used in Lemma 5.4 |
| ref-3 3 (assert the 0.01 margins) | fixed in code (bracket.py:43-44, 223; match.py:53), and proved analytically in Lemma 3.1 |
| ref-3 4 (exterior margin minus eps) | fixed (bracket.py:293); Theorem 4.5 uses ext = \|E\| - m/R - delta - eps; D0 uses ext0 |
| ref-3 5 (pin the tube) | four outputs, one sha (check_assembly.log) |
| ref-3 6 (Frobenius slack wording; "algebraically simple") | proof of the slack in Lemma 5.2, plus a numeric check; simplicity is used nowhere |
| ref-3 C-W weak | C-W is not on the proof path (section 12) |
| ref-4 1 (full proofs of B-EX, B-TAIL, BR-R0, BR-M incl. the Dirichlet-a rule, D0, TAIL-LIN, constants traced) | sections 3, 4.3, 4.4, 4.7, 5.3 |
| ref-4 2 (audit itaylor and tail line by line) | done: audit-1/AUDIT-ENGINES.md finds itaylor, tail and the stepping callers CORRECT on the target path (GAP A1 closed) |
| ref-5 blocking 1-2 and cosmetic items | see the changelog at the top |
| ref-4 B (ESS: one resolvent point; Weyl source) | Lemma 6.1(b)-(c); Weyl's theorem is not needed for finiteness (the counts give it); relative compactness and analytic Fredholm are STANDARD, not opened |
| ref-4 C (3-D ESS; "ground state" wording) | Lemma 6.1 in 3-D and Theorem 7.3; the state is called first excited (paper:768) |
| ref-4 E (C-P3 realness) | section 8 |
| ref-4 F (comparator strings) | GAP C2; the verdict path reads only arb-decided booleans and integers |
| ref-4 "verdict.py does not check the sha" | checks/check_assembly.py does |

---

## 12. What is not claimed

- **One point.** Only sigma0 = 9/5 (exact rational), s = +1, alpha = 1, n = 1. Nothing about the rest of the paper's
  band, other n, or other signs.
- **The state.** The theorem covers every decaying one-node solution with u0 in U0, an interval of width 2e-50. That
  only one such solution exists at sigma0 = 9/5 (in U0 or anywhere) is not claimed.
- **Linear and spectral only.** The claim is the location of the spectrum of the linearised operator. There is no
  claim of nonlinear stability, orbital stability, linear stability in the sense of bounded semigroup growth,
  absence of embedded eigenvalues in +/- i[|E|, inf), or of the Jordan structure at 0.
- **No count of imaginary eigenvalues.** Uniqueness of the Krawczyk zero is not used. "Exactly one eigenvalue in the
  box" is not claimed for the infinite-domain problem, and neither is algebraic simplicity.
- **Numerical choices.** r0 is the binary64 number nearest 1e-5. It is a free choice that enters every computation as
  the same exact point; it is not a claimed constant. The same holds for R = 10 and 14, R1 = 26, r_m = 8, eps = 1/1000,
  the disc radius 0.002, Rf and the step sizes.
- **Not part of the proof.** VIR, C-W, C-R, D1 and the positive-Krein controls are consistency checks or BAR gates.
  The C-B1 windows are post-hoc calibration, and the C-P2 real-part window is mock-informed (disclosed in the BAR).
- **No prior-art claim.** This text makes no claim of priority or novelty.

---

## 13. GAPS (rewritten in v2)

1. **A1: CLOSED.** core/seats/audit-1/AUDIT-ENGINES.md audited code facts C1, C4 and C9 against self-contained
   derivations and exact closed-form tests, including deliberately broken controls that do fail. Its verdicts:

   | routine | verdict |
   |---|---|
   | itaylor bg_step, lin_step, lin_jets, bg_jets | CORRECT (the enclosure holds at every point of the step, including ball base points and ball steps) |
   | ctx.prec handling | CORRECT (cannot corrupt) |
   | floats and mid() on the proof path | CORRECT (steering or mean-value centres only) |
   | tail riccati_coeffs, residual_coeffs, channel | CORRECT |
   | tail _hoe, _ric_step, ric_integrate | CORRECT |
   | tail.lemma | CORRECT (conservative: D1 is 6.0e-25 in code against 3.3e-25 derived; Tt is 3x loose) |
   | tail.channel_full | CORRECT WITH FIX (latent) |
   | lincore BgJets, march | CORRECT WITH FIX (latent) |
   | itaylor eval_sub, eval_at | CORRECT WITH FIX (latent) |
   | bg_tube integrate, finish (stepping) | CORRECT |
   | bg_tube series_start | CORRECT WITH FIX (cosmetic) |

   Its four latent patches are all off the target path and change no number:
   - (a) tail.py:354 should return drd = None when no Cauchy disc is passed. Without a disc the initial d rho/d lambda
     is not an enclosure, but every derivative use passes lam_disc (match.py:154-157, krein.py:39-42).
   - (b) lincore.py:88 accepts an r_from up to 1e-14 off the grid. Every caller passes bj.r[0] or bj.r[-1].
   - (c) itaylor eval_sub and eval_at do not check that t lies in hull(0, h). Their only caller stays inside the step.
   - (d) bg_tube.py:99-100 uses Python max() on balls, which is covered by the factor 2 and by H ~ r0^26.

2. **B1': operation-by-operation audit, mostly CLOSED.**
   - Referee-5 audited operation by operation, for interval soundness, and found each CORRECT:
     - bracket.py: ustart, qbound, ZeroCounter, endpoint_term, d0_node, gnorms, run (C5, C6);
     - kraw.test and certify (C10);
     - the krein Gram, tail and sign decisions (C10);
     - match.matrix assembly, including the Gram index layout and dM (C8);
     - match.frob_start, by derivation plus checks/check_frob_slack.py (C7);
     - the bg_tube.series_start Volterra derivation (C2).
   - B-EX, B-TAIL and the finish tails (C3) were checked by referee-5 and by audit-1 (stepping parts).
   - **Still not audited operation by operation:** verdict.py beyond K_of (comparators and VOID logic); evans.py, which
     is on the controls path only; tail.vectors in detail (audit-1 covered its constants); assemble.py beyond the
     sigma0 assertion and the in-run rebuild (C11, read by referee-5 at assemble.py:28-30 and 144-145). None of these
     produces an enclosure that the target theorem uses, except tail.vectors. For tail.vectors, the formulas Xhat_j,
     G_i and the Tt-ball split were re-derived here (Lemma 5.6) and its constants were audited by audit-1. Severity B
     for tail.vectors and C for the rest.
3. **B2 (B: disclosed list of standard results not opened).** Referee-5 judged these genuinely standard and their
   hypotheses satisfied here, but neither it nor this seat opened a source:
   - continuity and strict monotonicity in the endpoint of Dirichlet eigenvalues of 2x2 Sturm systems (Lemma 4.4
     step 3);
   - relative compactness of bounded potentials vanishing at infinity (Lemma 6.1);
   - the analytic Fredholm theorem (Lemma 6.1);
   - the Krawczyk existence theorem (Lemma 5.9);
   - min-max on finite intervals;
   - Banach contraction and continuous dependence at the regular singular point (Lemma 3.1, Lemma 3.2 step 1);
   - H^2 regularity of the matched solution (Lemma 5.1);
   - the multipole expansion behind paper (37).

   The HOE enclosure theorem is no longer on this list: audit-1 gave a self-contained proof of the step (integral
   remainder, convexity of boxes, first exit).
4. **C1 (C).** Uniqueness of the one-node state is not proved. The theorem is "for every such state with u0 in U0'"
   (sections 1 and 12).
5. **C2 (C).** The S() formatter at krein.py:66 prints a 10-digit midpoint with the unrounded ball radius. It affects:
   - **w strings, which are NOT enclosures.** For example "1.104911080 +/- 3.76e-16" does not contain the certified ball
     [1.10491108047488 +/- 4.15e-15]. Section 5 therefore takes w from the outward strings in target-K<L>.log.
   - **krein_ad, int_inner and int_outer** (and ad_over_parts), which use the same formatter. There, 10-digit
     truncation moves the midpoint by at most 5e-10 relative: for example 1.5e-15 absolute for
     krein_ad = -3.061281342e-6. That is below each printed radius (4.6e-13 and up), so these strings happen to be valid
     enclosures, and the <a, d> column of section 5.5 is valid.
   - **evans.py:42**, which feeds the C-P2 window comparator (controls only).

   No string is read on the target verdict path: the signs and in_gap are decided in arb. Fix: x.str(radius=True).
6. **C3 (C).** The float flag at evans.py:48 (C-P3) is still in the code. Section 8 gives the valid replacement argument
   (K(2) <= 1). Control path only.
7. **C4 (C, latent code and docs).** The bracket.py:195 docstring, and DESIGN-R1-v3 node D0, say "left Robin U_lo at
   level -nu". The correct statement is U_lo <= DtN at level +nu, which holds because qbound covers |lambda| + nu
   (Theorem 4.7). Wording only.
8. **C5 (C).** Lemma 5.5 does not use the fact that the error E_j(R) lies exactly along the growing directions. The
   code uses a weaker general-error decomposition (Lemma 5.6), which is valid and merely conservative, like D1's
   factors, Tt and the factor 2 in tailb.
9. **C6 (C, latent code).** bracket.py:288-291 does not clamp Iin_lo at 0, and a negative lower end would shrink delta,
   which is unsound (referee-5). On the target Iin_lo is about 7.04, so no number moves. Fix: Iin_lo = max(0, ...).
10. **C7 (C, doc).** DESIGN-R1-v3 node TAIL-LIN does not define D1 and S1. Their derivation is in Lemma 5.5 here and in
    audit-1 (audit-1 doc gap).

**Open lab item (not a mathematical gap).** Doctrine #31 needs a blind confirmation. A blind float replication is
pending under seal f47da860b7. This seat has not opened core/blind/.

No gap of severity A remains, in the mathematics or in the audited code on the target path.

---

*Checks run by this seat (each under memcap 8, own PIDs):*
- core/proof/checks/check_frob_slack.py, with log check_frob_slack.log: ALL PASS (under 1 s);
- core/proof/checks/check_assembly.py, with log check_assembly.log: ALL PASS (under 1 s). It also flags the six
  non-enclosure w strings of GAP C2;
- core/proof/checks/check_U0.py, with log check_U0.log: ALL PASS (about 2 min; peak 0.78 GB). It confirms the json
  u_mid and sha, the rebuilt tube sha f8b0cc27...ce28b, and that U0' is contained in the computed U0.

No file in build-1/ or build-2/ was modified. The checks import bg_tube and itaylor read-only, with bytecode writing
disabled, and the tube rebuild neither read nor wrote the cache.
