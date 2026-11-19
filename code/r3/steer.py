"""steer.py - FLOAT steering for build-W (NOT an instrument; nothing here is a certificate).
Finite-difference operators at a node from the certified tube's midpoints; choice of the explicit vectors p_j (CPOS)
and trial triples (RITZ) as Chebyshev coefficients; float margins for the pre-pass. Every number produced here only
selects inputs that the arb instruments then certify or reject."""
import numpy as np
from flint import arb
import itaylor as it


def state_at(steps, Yend, r, K=40):
    lo, hi = 0, len(steps) - 1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if float(steps[m]['r'].mid()) <= r:
            lo = m
        else:
            hi = m - 1
    st = steps[lo]
    J = it.bg_jets(1, arb(st['r'].mid()), [arb(y.mid()) for y in st['Y']], K)
    t = arb(r) - arb(st['r'].mid())
    return [float(it.horner(J[i], t).mid()) for i in range(4)]


class FD:
    def __init__(self, steps, Yend, R, N=900):
        self.R = R; self.N = N; self.dr = R / N
        self.r = self.dr * np.arange(1, N + 1)
        old = it.ctx.prec
        it.set_prec(320)
        st = np.array([state_at(steps, Yend, float(ri)) for ri in self.r])
        it.set_prec(old)
        self.sig = st[:, 0]; self.u = st[:, 2]

    def ops(self, L):
        N, dr, r = self.N, self.dr, self.r
        ell = L * (L + 1)
        D2 = (np.diag(2 * np.ones(N)) - np.diag(np.ones(N - 1), 1) - np.diag(np.ones(N - 1), -1)) / dr ** 2
        D2[-1, -1] = 1 / dr ** 2                       # Neumann at R
        P = D2 + np.diag(ell / r ** 2); P[-1, -1] = 1 / dr ** 2 + ell / r[-1] ** 2 + (L / r[-1]) / dr
        Pi = np.linalg.inv(P)
        Lm = D2 + np.diag(ell / r ** 2 + self.sig ** 2 - self.u)
        Lp = D2 + np.diag(ell / r ** 2 + 3 * self.sig ** 2 - self.u) - 2 * (self.sig[:, None] * Pi * self.sig[None, :])
        return Lp, Lm, Pi

    def H(self, L, w):
        Lp, Lm, _ = self.ops(L)
        I = np.eye(self.N)
        return np.block([[Lp, -w * I], [-w * I, Lm]])

    def Wof(self, L, a):
        """W = -sqrt2 P^-1 (sigma a)  (the minimising auxiliary channel)."""
        _, _, Pi = self.ops(L)
        return -np.sqrt(2) * Pi @ (self.sig * a)


def cheb_fit(r, f, Rc, deg, kind='p'):
    x = 2 * r / Rc - 1
    T = np.polynomial.chebyshev.chebvander(x, deg)
    if kind == 'trial':
        T = T * (r * (Rc - r))[:, None]
    elif kind == 'trialW':
        T = T * r[:, None]
    c, *_ = np.linalg.lstsq(T, f, rcond=None)
    return [float(v) for v in c]


def cheb_eval(c, r, Rc, kind='p'):
    v = np.polynomial.chebyshev.chebval(2 * r / Rc - 1, c)
    return v * (r * (Rc - r)) if kind == 'trial' else (v * r if kind == 'trialW' else v)
