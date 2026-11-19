# RESULT - blind replication seat: linear spectrum of the n=1 repulsive GPP state, sigma0 = 9/5

## Disclosures (read first)
- The brief gave no target numbers or functional forms. I did read the whole paper text, which the brief allowed. It
  contains qualitative results that bear on these answers: (i) Sec. V / Fig. 8 says the repulsive n=1 family has a
  "common stability band 1.55 <~ sigma0 <~ 2.07" for L = 0..12 (sigma0 = 9/5 lies inside it); (ii) excited states in the
  Schrodinger-Poisson limit (small sigma0) are radially unstable. It also gives the Fig. 5 numbers (attractive n=0:
  T, F at sigma0 = 0.19, 1.0, 1.89). I used those numbers only as a positive control. No numbers for the target state
  appear in the paper text.
- Fence: once I tried to Read a tool-output file of my own that had been saved under `<a session transcript folder>`
  (a transcript folder). The lab guard refused it and nothing was read. I opened no forbidden path.
- I identified no constants, so identify.py was not used. There is no checkpointing, so "resume_tested" does not apply.

## Units and conventions
I use the paper's eq. 9 dimensionless units: i psi_t = (-Lap + |psi|^2 + U) psi and Lap U = |psi|^2, with the repulsive
sign and alpha = 1 (the coefficient of the Poisson term in eq. 43b/45). Stationary state: psi = e^{-iEt} sigma(r), with
u = E - U and U -> 0 at infinity, so u(inf) = E. Background equations (eq. 32): (1/r)(r sigma)'' = (sigma^2 - u) sigma and
(1/r)(r u)'' = -sigma^2, with sigma(0) = sigma0 and u(0) = u0.
Mass: m = int_0^inf sigma^2 r^2 dr. The paper's M = 4 pi m; both are reported.

## Method (my own formulation, different from the paper's Chebyshev collocation)
1. Background: shooting in u0 with DOP853 (rtol 1e-12), using a 2nd-order regular series start at r = 1e-4. Bisection
   runs to machine precision on the classification "number of zeros before blow-up <= 1 vs >= 2". Beyond r_c (where
   |sigma| < 1e-6 sigma0) the profile is replaced by the exact decaying solution of the linear tail equation
   a'' = (k^2 - m/r) a, with a = r sigma and k = sqrt(-E). That solution is Whittaker W_{m/2k,1/2}(2kr), checked against
   mpmath. Outside r_c, u = E + m/r exactly, with E = u(r_c) + r_c u'(r_c) and m = -r_c^2 u'(r_c).
2. Linearisation, derived from eq. 19-22. Write sigma_pert = p + i q. Then p_t = L- q and q_t = -L+ p, i.e.
   lambda (A, C) = J L (A, C) with J = [[0, 1], [-1, 0]] and L = diag(L+, L-):
   - L- = -Lap_L + sigma^2 - u   (= H0 - E)
   - L+ = -Lap_L + 3 sigma^2 - u + 2 alpha sigma Lap_L^{-1}(sigma .)
   Here Lap_L^{-1} is the eq. 37 Green's kernel. (Check: with C = -iB this is exactly the paper's eq. 22/35.)
   In reduced variables a = r A: l- a = -a'' + [L(L+1)/r^2 + sigma^2 - u] a, and l+ a = (same with 3 sigma^2) + 2 sigma chi,
   where chi solves chi'' - L(L+1) chi/r^2 = sigma a, with chi(0) = 0 and chi ~ r^{-L} at infinity.
3. Discretisation: B-spline Galerkin (degree p, N intervals with sinh-graded breakpoints on [0, R]). a and d have
   Dirichlet conditions at 0 and R. chi lives in its own spline space with Dirichlet at 0 and the exact exterior Robin
   condition chi'(R) = -(L/R) chi(R), so the Poisson field has no truncation error. The nonlocal term enters as the
   Schur complement -2 alpha P K^{-1} P^T, which is symmetric and negative. The spectra come from (i) eigh of the
   M-symmetrised L+ and L-, giving n(L+-), and (ii) a dense eig of the 2n x 2n matrix [[0, L-], [-L+, 0]], giving
   lambda. Krein sign = sign <L xi, xi> = <L+ A, A> + <L- C, C>, evaluated on each eigenvector. Cross-check: the sign of
   <a, d> in the real form L+ a = w d, L- d = w a agrees for every mode.

## Positive controls (all run in the same code)
- Paper Fig. 5 (attractive n=0):
  - sigma0 = 0.19: T = 0.554195, F = 0.046102 (paper 0.558, 0.047).
  - sigma0 = 1.89: T = 11.382452, F = 5.264218 (paper 11.411, 5.282).
  - "sigma0 = 1.0 = max-mass state": I get T = 5.328119 and F = 1.730591 at exactly 1.0. Both of the paper's numbers
    (5.641, 1.887) are met together at sigma0 ~ 1.047 (T = 5.528221 / 5.661957 and F = 1.830453 / 1.898084 at
    1.03 / 1.05). That is consistent with the paper's max-mass state lying slightly above 1.0.
  - Verdict: agreement at the 0.3-2% level, i.e. the paper's 3-4 printed digits. Not a high-precision control.
- Internal identities (every background):
  - Virial eq. 26, D - 2T - 3F: -1.07e-09 (sigma0 = 9/5, D = 260.7, so 4e-12 relative) and -1.35e-10 (sigma0 = 1/2).
  - E N = 2T + 4F - 4D: residual 9e-12 and 5e-13.
  - E from the exterior match vs eq. 33: agree to 1.8e-11 (9/5) and 7e-12 (1/2).
- Spectral controls:
  - Repulsive n=0, sigma0 = 1: n(L+) = 1, n(L-) = 0 at L=0, no unstable modes at L = 0, 1. This matches the paper's
    stability statement.
  - Attractive n=0: at sigma0 = 0.19, no unstable mode at L = 0, 1. At sigma0 = 1.89, a real unstable eigenvalue
    lambda = 0.8945373242 appears at L=0 and the VK quantity changes sign to +0.339. This matches the paper's statement
    "unstable for sigma0 >~ 1" and the turning-point picture.
  - Vakhitov-Kolokolov identity <L+^{-1} r sigma, r sigma> = (1/2) dm/dE. This tests the nonlocal Poisson term against
    the background family, with dm/dE from finite differences in sigma0:
    - 9/5: operator -2.17285220829 vs FD -2.17285219577 (h = 1e-3) and -2.17285215812 (h = 2e-3). Richardson gives
      -2.1728522083.
    - 1/2: operator -3.34652339110 vs Richardson FD -3.3465233912.
    - PASS to about 1e-10.
  - Symmetry kernels (exact, found at the expected places):
    - L=0: L- (r sigma) = 0. Residual 3e-10; eigenvalue ~1e-14.
    - L=1: L+ (r sigma') = 0. Residual 2e-8; eigenvalue ~5e-14.
    - Galilean boost at L=1: L- (r^2 sigma) = -2 r sigma'. Residual 3e-9.
    - L+ at L=0 and L- at L=1 have no kernel.
    - L = 2, 3 have no kernels.
    - The generalised kernels (phase/dE at L=0, translation/boost at L=1) show up in J L as |lambda| <= 6e-7 pairs. This
      is the standard sqrt(eps) splitting of a 2x2 Jordan block. I exclude them from "max Re lambda".

## Results, sigma0 = 9/5 (repulsive, alpha = 1, n = 1)
Background:
- E = -3.10544025445 (+-2e-11; trusted to 10 decimals: -3.1054402544(5))
- u0 = 3.9390235754
- m = int sigma^2 r^2 dr = 19.158712546, so M = 4 pi m = 240.75548234
- Single node at r = 2.7853521306
- T = 78.64461853, F = 34.47300690, D = 260.70825775
- Virial D - 2T - 3F = -1.07e-09

Negative eigenvalue counts after removing the exact kernels:

| L | n(L+) | n(L-) | kernels removed |
|---|-------|-------|-----------------|
| 0 | 2 | 1 | L-: r sigma (phase) |
| 1 | 1 | 1 | L+: r sigma' (translation) |
| 2 | 1 | 1 | none |
| 3 | 0 | 0 | none |

Internal modes lambda = i w with 0 < w < |E| (converged; Krein sign in brackets):
- L=0: 0.5728495431 (+), **1.1049110805 (-)**, 1.2592133714 (+), 1.6950530232 (+), 1.9849674202 (+), 2.1940718974 (+), 2.3500559196 (+), 2.4694369460 (+)
- L=1: **0.5399256680 (-)**, 0.9510282377 (+), 1.4946824096 (+), 1.8449316531 (+), 2.0923466100 (+), 2.2739275224 (+), 2.4110408122 (+), 2.5170266071 (+)
- L=2: **0.2968148506 (-)**, 0.5179458643 (+), 1.2396528658 (+), 1.6726980251 (+), 1.9705958803 (+), 2.1847702815 (+), 2.3438400095 (+), 2.4651406337 (+)
- L=3: 0.2995950853 (+), 0.9778756726 (+), 1.4837222704 (+), 1.8377257957 (+), 2.0888660858 (+), 2.2725787241 (+), 2.4108067443 (+), 2.5173495475 (+)

The list is infinite. The long-range gravitational tail u = E + m/r gives both L+ and L- an attractive Coulomb tail
-m/r, so there is a Rydberg series of internal modes accumulating at w -> |E| from below. The computed modes obey
|E| - w ~ (m/2)^2 / n_eff^2 with n_eff close to an integer (L = 0, 2) or a half-integer (L = 1, 3) (n_eff values are in
RESULT.json). Above the listed modes each L has 12 further box-limited modes (w from about 2.56 to 3.09) that move with R.
All of them have Krein sign + in every run.

Stability:
- max Re lambda, excluding the generalised-kernel pairs: 5.5e-13 (L=0), 5.4e-12 (L=1), 7.6e-12 (L=2), 1.6e-11 (L=3).
  This is zero to rounding.
- No real or complex unstable eigenvalue at any L = 0..3, so the state is spectrally stable for L <= 3.
- Hamiltonian-Krein count check: n(L+) + n(L-) - n(D) = 2 x (number of negative-Krein imaginary pairs) holds at every L.
  - D at L=0 is the VK scalar (-2.1729 < 0, so n(D) = 1). At L=1 it is +(3/4) int r^2 sigma^2 > 0 (from the boost
    relation), so n(D) = 0.
  - Counts: L=0: 2+1-1 = 2 = 2x1. L=1: 1+1-0 = 2 = 2x1. L=2: 1+1 = 2 = 2x1. L=3: 0 = 0.
  - So the computed spectrum accounts for every negative direction; no unstable or negative-Krein mode is missing.

## Results, sigma0 = 1/2 (same n, sign, alpha), L = 0
Background:
- E = -0.5374049786 (+-5e-11)
- u0 = 0.7069464636
- m = 6.354776216, so M = 4 pi m = 79.85647311
- Node at r = 4.8726606510
- T = 6.36958761, F = 0.58721757, D = 14.50082793
- Virial residual -1.35e-10

L = 0:
- n(L+) = 2, n(L-) = 1 (kernel r sigma of L- removed). VK = -3.3465233911.
- **Unstable: a complex quartet lambda = +-0.0241322927 +- 0.2832272004 i**, so max Re lambda = 0.0241322927 (same to
  13 digits in all 4 runs).
- Internal imaginary modes, all Krein +: w = 0.1056087400, 0.3087816605, 0.3736871041, 0.4093059777, 0.4341014996,
  followed by the Rydberg tail (10 box-limited modes from 0.452 to 0.536).
- No negative-Krein imaginary mode remains. The count 2+1-1 = 2 equals one complex quartet. Reading of this (not
  tested further): the negative-Krein mode seen at 9/5 has collided with a positive-Krein mode and left the axis.

## Convergence
- sigma0 = 9/5: (R, N, p) = (40, 150, 7), (60, 250, 7), (80, 400, 9), plus (60, 250, 7) with the background at
  rtol 1e-10.
- sigma0 = 1/2: (80, 200, 7), (120, 300, 7), (160, 450, 9), plus (120, 300, 7) at rtol 1e-10.
- Every listed w changes by <= 2e-13 between the runs (<= 9e-12 for the last listed mode of each L). The complex lambda
  changes by < 2e-14.
- Background: DOP853 at rtol 1e-10 vs 1e-12 agrees to ~5e-14 in E and u0. A different integrator (LSODA) agrees to 4e-11
  in E, 8e-12 in u0 and 1e-10 in m. I therefore trust 10 decimals in w and lambda and 10 in E.
- n(L+-), the kernels and the Krein signs are identical in all runs.

## Surprises / curiosities (UNTESTED)
- The Rydberg (Coulomb) accumulation of internal modes at |E| makes "all eigenvalues 0 < w < |E|" an infinite set.
  Any comparison has to use the low, converged ones.
- The Rydberg quantum defect looks close to 0 for even L and close to 1/2 for odd L (n_eff 12.012 / 12.488 / 11.971 /
  12.4915 for L = 0..3). This is untested and may be a coincidence.
- The lowest L=2 mode (0.29681, Krein -) and the lowest L=3 mode (0.29960, Krein +) lie close together. A small change of
  sigma0 could make them collide, but L=2 and L=3 do not couple, so this alone gives no instability.

Files: data/blind/RESULT.json (all numbers as strings), RESULT.md, RUN.md,
raw_*.json and *.log (all runs), bg.py, fem.py, spec.py, run_main.py, ctrl_*.py, assemble.py, compare.py.
