"""xc.py - control XC (FLOAT; DESIGN-W3 failure mode 4, referee-W2): at interior float points the lowest eigenvalue
of H_sigma0(w_theta) on the common subspace M must lie in [chord(m) - eta2(theta), chord(m) + eta2'(theta)].
A sign slip in CH makes it fail. FLOAT throughout (finite differences, N = 1000, R = 20): not a certificate.
Backgrounds: node states from the cached certified tubes (midpoints) and float solves at the interior points
(design/probe/fbg.py, read-only; allowed float neighbourhoods of certified nodes). Usage: xc.py xa xb xm L w2a w2b"""
import sys, os, json
import numpy as np
PROBE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'design', 'probe')
sys.path.insert(0, PROBE)
sys.dont_write_bytecode = True
from fbg import grid, state, watchdog

watchdog(280)
xa, xb, xm = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
L = int(sys.argv[4]); w2a, w2b = float(sys.argv[5]), float(sys.argv[6])
N = 1000; R = 20.0; dr, r = grid(N, R)
om = 1 + (r / 4) ** 2; su = 3.0
Sa, Sb, Sm = state(xa), state(xb), state(xm)
Dl = xb - xa; th = (xm - xa) / Dl
k = {0: 3, 1: 2, 2: 1}[L]


def tau_of(S):
    """first variation by the FD linear solve (p11b_br.py build)."""
    sig, u = S[:, 0], S[:, 2]; n = 2 * N - 1; A = np.zeros((n, n))
    for jj in range(1, N + 1):
        if jj >= 2: A[jj - 1, jj - 2] = 2 / dr ** 2 + 3 * sig[jj - 1] ** 2 - u[jj - 1]
        if jj - 1 >= 2: A[jj - 1, jj - 3] = -1 / dr ** 2
        if jj + 1 <= N: A[jj - 1, jj - 1] = -1 / dr ** 2
        A[jj - 1, N - 1 + jj - 1] = -sig[jj - 1]
    for jj in range(1, N):
        A[N + jj - 1, N - 1 + jj - 1] = 2 / dr ** 2
        if jj - 1 >= 1: A[N + jj - 1, N - 1 + jj - 2] = -1 / dr ** 2
        A[N + jj - 1, N - 1 + jj] = -1 / dr ** 2
        if jj >= 2: A[N + jj - 1, jj - 2] = -2 * sig[jj - 1]
    rhs = np.zeros(n)
    rhs[0] = -(2 / dr ** 2 + 3 * sig[0] ** 2 - u[0]) * dr; rhs[1] = dr / dr ** 2; rhs[N] = 2 * sig[0] * dr
    y = np.linalg.solve(A, rhs)
    ta = np.concatenate([[dr], y[:N - 1]]); tb = y[N - 1:]
    return ta / r, tb / r


def H(S, w):
    sig, u = S[:, 0], S[:, 2]; ell = L * (L + 1)
    D2 = (np.diag(2 * np.ones(N)) - np.diag(np.ones(N - 1), 1) - np.diag(np.ones(N - 1), -1)) / dr ** 2
    D2[-1, -1] = 1 / dr ** 2
    P = D2 + np.diag(ell / r ** 2); P[-1, -1] = 1 / dr ** 2 + ell / r[-1] ** 2 + (L / r[-1]) / dr
    Lm = D2 + np.diag(ell / r ** 2 + sig ** 2 - u)
    Lp = D2 + np.diag(ell / r ** 2 + 3 * sig ** 2 - u) - 2 * (sig[:, None] * np.linalg.inv(P) * sig[None, :])
    I = np.eye(N)
    return np.block([[Lp, -w * I], [-w * I, Lm]])


ta = tau_of(Sa); tb = tau_of(Sb)
sa, ua, sb, ub = Sa[:, 0], Sa[:, 2], Sb[:, 0], Sb[:, 2]
ds, du = sb - sa, ub - ua
h01 = -2 * th ** 3 + 3 * th ** 2; h10 = th ** 3 - 2 * th ** 2 + th; h11 = th ** 3 - th ** 2
Hs = sa + h01 * ds + Dl * (h10 * ta[0] + h11 * tb[0]); Hu = ua + h01 * du + Dl * (h10 * ta[1] + h11 * tb[1])
rho = max((np.abs(Sm[:, 0] - Hs) * om).max(), (np.abs(Sm[:, 2] - Hu)).max() / su)     # float deviation as NK radius
slin = (1 - th) * sa + th * sb
es = np.abs(Hs - slin) + rho / om
eu = np.abs(Hu - ((1 - th) * ua + th * ub)) + rho * su
n_r = lambda f: np.sqrt(np.sum(r * f * f) * dr)
ne = n_r(es); I1l = (1 - th) * n_r(sa) + th * n_r(sb)
eta2 = (3 * th * (1 - th) * ds ** 2 + 6 * np.abs(slin) * es + eu).max() + (4 * ne * I1l + 2 * ne ** 2) / (2 * L + 1)
eta2p = (6 * np.abs(slin) * es + 3 * es ** 2 + eu).max() + (2 * th * (1 - th) * n_r(ds) ** 2 + 4 * ne * I1l + 2 * ne ** 2) / (2 * L + 1)
Ha, Hb = H(Sa, w2a), H(Sb, w2b)
ea_, Va = np.linalg.eigh(Ha); eb_, Vb = np.linalg.eigh(Hb)
src = Va if ea_[k] <= eb_[k] else Vb
Qq, _ = np.linalg.qr(src[:, :k], mode='complete'); C = Qq[:, k:]
ma = np.linalg.eigvalsh(C.T @ Ha @ C)[0]; mb = np.linalg.eigvalsh(C.T @ Hb @ C)[0]
wt = (1 - th) * w2a + th * w2b
mt = np.linalg.eigvalsh(C.T @ H(Sm, wt) @ C)[0]
chord = (1 - th) * ma + th * mb
lo, hi = chord - eta2, chord + eta2p
ok = bool(lo <= mt <= hi)
# negative control: a sign slip (eta2' with the nonlocal convexity term on the wrong side, i.e. the W1 error) must
# not be needed; report also the bracket with eta2 and eta2' swapped in sign (must FAIL for a sign slip to be caught)
slip_lo, slip_hi = chord + eta2, chord - eta2p          # an empty interval: any value fails it
res = dict(cell=[xa, xb], point=xm, theta=th, L=L, w_theta=wt, m_a=ma, m_b=mb, chord=chord, true=mt, eta2=eta2,
           eta2p=eta2p, bracket=[lo, hi], PASS=ok, rho_float=rho, slip_bracket_fails=bool(not (slip_lo <= mt <= slip_hi)))
print(json.dumps(res), flush=True)
os._exit(0)
