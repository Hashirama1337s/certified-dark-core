"""Background stationary states of the dimensionless GPP system (arXiv 2402.07998 eq. 32):
    (1/r)(r sigma)'' = (s sigma^2 - u) sigma ,   (1/r)(r u)'' = -sigma^2 ,
  s=+1 repulsive, s=-1 attractive; u = E - U, U -> 0 at infinity so u -> E.
Shooting in u0 = u(0) at fixed sigma0, node count classification + bisection.
Tail beyond r_c replaced by the exact linear decaying solution (Whittaker W) of
  a'' = (k^2 - m/r) a , a = r sigma, k = sqrt(-E), m = int sigma^2 r^2 dr.
"""
import numpy as np
from scipy.integrate import solve_ivp
import mpmath as mp

R0 = 1e-4


def rhs(r, y, s):
    sg, dsg, u, du = y
    return [dsg, -2 * dsg / r + (s * sg * sg - u) * sg, du, -2 * du / r - sg * sg]


def init(sig0, u0, s, r=R0):
    c = (s * sig0**2 - u0) * sig0 / 6.0
    d = -sig0**2 / 6.0
    return [sig0 + c * r * r, 2 * c * r, u0 + d * r * r, 2 * d * r]


def count_nodes(sig0, u0, s, rmax=150.0, rtol=1e-12, method='DOP853'):
    def blow(r, y, s):
        return abs(y[0]) - 3 * sig0
    blow.terminal = True
    sol = solve_ivp(rhs, (R0, rmax), init(sig0, u0, s), args=(s,), method=method,
                    rtol=rtol, atol=1e-14 * sig0, events=blow, dense_output=False, max_step=0.05)
    sg = sol.y[0]
    k = int(np.sum(sg[1:] * sg[:-1] < 0))
    return k, sol


def shoot(sig0, s, n, ulo=None, uhi=None, rtol=1e-12, method='DOP853', rmax=150.0):
    # bracket: find u0 with k<=n (lo) and k>=n+1 (hi)
    if ulo is None:
        u = s * sig0**2 + 1e-6
        kprev = count_nodes(sig0, u, s, rmax, 1e-8, method)[0]
        assert kprev <= n
        while True:
            un = u + 0.02
            k = count_nodes(sig0, un, s, rmax, 1e-8, method)[0]
            if k >= n + 1:
                ulo, uhi = u, un
                break
            u = un
            assert u < s * sig0**2 + 100
    assert ulo is not None, "no bracket"
    for _ in range(200):
        mid = 0.5 * (ulo + uhi)
        if mid == ulo or mid == uhi:
            break
        k, _ = count_nodes(sig0, mid, s, rmax, rtol, method)
        if k <= n:
            ulo = mid
        else:
            uhi = mid
    return ulo, uhi


def profile(sig0, s, n, rtol=1e-12, method='DOP853', rmax=150.0, frac=1e-6):
    ulo, uhi = shoot(sig0, s, n, rtol=rtol, method=method, rmax=rmax)
    sols = []
    def blowp(r, y, s):
        return abs(y[0]) - 3 * sig0
    blowp.terminal = True
    for u0 in (ulo, uhi):
        sol = solve_ivp(rhs, (R0, rmax), init(sig0, u0, s), args=(s,), method=method,
                        rtol=rtol, atol=1e-14 * sig0, dense_output=True, max_step=0.05, events=blowp)
        sols.append(sol)
    # find r_c: last r where both solutions agree and |sigma| > frac*sig0 (monotone-tail region)
    rr = np.linspace(R0, rmax, 400001)
    y1 = sols[0].sol(rr)
    y2 = sols[1].sol(rr) if sols[1].t[-1] >= rmax else None
    t2max = sols[1].t[-1]
    t1max = sols[0].t[-1]
    sg = 0.5 * (sols[0].sol(np.minimum(rr, t1max))[0] + sols[1].sol(np.minimum(rr, t2max))[0])
    # walk outwards: stop where |sg| first drops below frac*sig0 after last node
    nodes = np.where(sg[1:] * sg[:-1] < 0)[0]
    assert len(nodes) >= n
    istart = nodes[n - 1] + 1 if n > 0 else 0
    idx = np.where(np.abs(sg[istart:]) < frac * sig0)[0]
    assert len(idx) > 0, "tail threshold not reached"
    rc = rr[istart + idx[0]]
    u0 = 0.5 * (ulo + uhi)
    # mean of two bracketing solutions on [R0, rc]
    def bgin(r):
        a = sols[0].sol(r)
        b = sols[1].sol(r)
        return 0.5 * (a + b)
    yc = bgin(np.array([rc]))[:, 0]
    sc, dsc, uc, duc = yc
    m = -rc * rc * duc           # r^2 u' = -int_0^r sigma^2 r^2
    E = uc + rc * duc            # u = E + m/r outside
    k = np.sqrt(-E)
    kap = m / (2 * k)
    mp.mp.dps = 30
    W = lambda r: mp.whitw(kap, 0.5, 2 * k * r)
    ac = rc * sc
    Wc = W(rc)
    dWc = mp.diff(W, rc)
    # derivative mismatch diagnostic: (r sigma)' at rc vs Whittaker log-derivative
    da_num = sc + rc * dsc
    da_tail = ac * float(dWc / Wc)
    info = dict(u0=u0, ulo=ulo, uhi=uhi, rc=rc, E_out=E, m_rc=m, k=k, kappa=kap,
                logder_mismatch=(da_num - da_tail) / abs(da_tail))
    return bgin, (rc, ac, Wc, W, E, m), info


class Background:
    def __init__(self, sig0, s, n, rtol=1e-12, method='DOP853', rmax=150.0, frac=1e-6):
        self.sig0, self.s, self.n = sig0, s, n
        self.bgin, (self.rc, self.ac, self.Wc, self.W, self.E, self.m), self.info = profile(
            sig0, s, n, rtol, method, rmax, frac)

    def eval(self, r):
        """sigma, u at array r (r>0)."""
        r = np.asarray(r, float)
        sg = np.empty_like(r)
        u = np.empty_like(r)
        inn = r <= self.rc
        if inn.any():
            y = self.bgin(r[inn])
            sg[inn] = y[0]
            u[inn] = y[2]
        out = ~inn
        if out.any():
            ro = r[out]
            sg[out] = self.ac * self.Wasym(ro) / (self.Wasym(np.array([self.rc]))[0] * ro)
            u[out] = self.E + self.m / ro
        return sg, u

    def integrals(self, nq=20000, rmaxq=None):
        """mass m=int sigma^2 r^2 dr, eq.33 E, T, F, D (paper eq. 14 normalisations)."""
        from numpy.polynomial.legendre import leggauss
        if rmaxq is None:
            rmaxq = self.rc + 60.0 / self.info['k']
        x, w = leggauss(64)
        edges = np.linspace(R0, rmaxq, 801)
        rq, wq = [], []
        for a, b in zip(edges[:-1], edges[1:]):
            rq.append(0.5 * (b - a) * x + 0.5 * (b + a))
            wq.append(0.5 * (b - a) * w)
        rq = np.concatenate(rq)
        wq = np.concatenate(wq)
        inn = rq <= self.rc
        sg, u = self.eval(rq)
        # derivative of sigma inside from ODE dense output
        dsg = np.zeros_like(rq)
        dsg[inn] = self.bgin(rq[inn])[1]
        # outside: numerical derivative of tail (tiny contribution)
        ro = rq[~inn]
        h = 1e-5
        sp_, _ = self.eval(ro + h)
        sm_, _ = self.eval(np.maximum(ro - h, self.rc + 1e-12))
        dsg[~inn] = (sp_ - sm_) / (ro + h - np.maximum(ro - h, self.rc + 1e-12))
        m = np.sum(wq * sg**2 * rq**2)
        Eint = self.info['u0'] - np.sum(wq * sg**2 * rq) - 0.5 * self.sig0**2 * R0**2   # eq. 33, incl. [0,R0] piece
        T = 0.5 * 4 * np.pi * np.sum(wq * dsg**2 * rq**2)
        F = 0.25 * 4 * np.pi * np.sum(wq * sg**4 * rq**2)
        U = self.E - u
        D = -0.25 * 4 * np.pi * np.sum(wq * U * sg**2 * rq**2)
        return dict(m=m, M4pi=4 * np.pi * m, E_eq33=Eint, T=T, F=F, D=D)


def _wasym(self, r, nterms=40):
    """Asymptotic series of W_{kappa,1/2}(2kr) up to the common factor (exact ratio needed only):
    W ~ e^{-z/2} z^kappa sum_n (1-kappa)_n (-kappa)_n / n! (-1/z)^n , z = 2 k r."""
    kap, k = self.info['kappa'], self.info['k']
    z = 2 * k * np.asarray(r, float)
    term = np.ones_like(z)
    tot = np.ones_like(z)
    nterms = int(min(nterms, max(2, np.min(z) / 2)))
    for nn in range(nterms):
        term = term * (1 - kap + nn) * (-kap + nn) / (nn + 1) * (-1.0 / z)
        tot = tot + term
        if np.all(np.abs(term) < 1e-17 * np.abs(tot)):
            break
    zc = 2 * k * self.rc
    return np.exp(-(z - zc) / 2) * (z / zc) ** kap * tot


Background.Wasym = _wasym
