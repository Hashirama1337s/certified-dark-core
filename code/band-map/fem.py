"""B-spline Galerkin discretisation of the radial linearised GPP operators (own formulation).

Reduced variables a = r A (3D inner product int A B r^2 dr = int a b dr).
  l_-  a = -a'' + [L(L+1)/r^2 + s sigma^2 - u] a
  l_+  a = -a'' + [L(L+1)/r^2 + 3 s sigma^2 - u] a + 2 alpha sigma chi,
          chi'' - L(L+1) chi / r^2 = sigma a ,  chi(0)=0 , chi ~ r^-L at infinity
  (chi = r * Delta_L^{-1}(sigma a / r); this is the paper's eq. 37 kernel, derived here as an ODE).
Galerkin: a in B-spline space with Dirichlet at r=0 and r=R; chi in B-spline space with Dirichlet
at 0 and the exact exterior Robin condition chi'(R) = -(L/R) chi(R) (source vanishes for r>R).
Weak form for chi:  K chi = -F,  K = int chi_i' chi_j' + L(L+1)/r^2 chi_i chi_j + (L/R) chi_i(R) chi_j(R),
F_i = int sigma a C_i.   Hence  <a, 2 alpha sigma chi> = -2 alpha F^T K^{-1} F.
"""
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import BSpline
import scipy.linalg as sla


def breakpoints(R, N, beta):
    x = np.linspace(0, 1, N + 1)
    if beta == 0:
        return R * x
    bp = R * np.sinh(beta * x) / np.sinh(beta)
    bp[0], bp[-1] = 0.0, R   # band/map fix: rounding can put bp[-1] a hair above R (knot order error)
    return bp


class Basis:
    def __init__(self, R, N, p, beta, nq=None):
        bp = breakpoints(R, N, beta)
        self.R = R
        t = np.concatenate([[0.0] * p, bp, [R] * p])
        nb = len(t) - p - 1
        self.t, self.p, self.nb = t, p, nb
        if nq is None:
            nq = p + 4
        x, w = leggauss(nq)
        rq, wq = [], []
        for a, b in zip(bp[:-1], bp[1:]):
            rq.append(0.5 * (b - a) * x + 0.5 * (b + a))
            wq.append(0.5 * (b - a) * w)
        self.rq = np.concatenate(rq)
        self.wq = np.concatenate(wq)
        spl = BSpline(t, np.eye(nb), p, extrapolate=False)
        self.B = spl(self.rq)                  # (nq_tot, nb)
        self.dB = spl.derivative()(self.rq)
        self.B = np.nan_to_num(self.B)
        self.dB = np.nan_to_num(self.dB)
        # value at R of each basis function: only the last one is 1
        self.BR = np.zeros(nb)
        self.BR[-1] = 1.0


class RadialProblem:
    def __init__(self, bgr, basis, s=+1, alpha=1.0):
        """bgr: callable r -> (sigma, u)."""
        self.b = basis
        self.s, self.alpha = s, alpha
        self.sig, self.u = bgr(basis.rq)
        b = basis
        W = b.wq
        Ba = b.B[:, 1:-1]      # Dirichlet at 0 and R
        dBa = b.dB[:, 1:-1]
        Bc = b.B[:, 1:]        # Dirichlet at 0 only
        dBc = b.dB[:, 1:]
        self.Ba, self.dBa, self.Bc, self.dBc = Ba, dBa, Bc, dBc
        self.M = Ba.T @ (W[:, None] * Ba)
        self.S = dBa.T @ (W[:, None] * dBa)
        self.Mc = Bc.T @ (W[:, None] * Bc)
        self.Sc = dBc.T @ (W[:, None] * dBc)
        self.P = Ba.T @ ((W * self.sig)[:, None] * Bc)
        r = b.rq
        self.Vr2 = Ba.T @ ((W / r**2)[:, None] * Ba)
        self.Vs2 = Ba.T @ ((W * self.sig**2)[:, None] * Ba)
        self.Vu = Ba.T @ ((W * self.u)[:, None] * Ba)
        self.Kr2 = Bc.T @ ((W / r**2)[:, None] * Bc)
        self.Mchol = sla.cholesky(self.M, lower=True)

    def ops(self, L):
        s = self.s
        ll = L * (L + 1)
        Hm = self.S + ll * self.Vr2 + s * self.Vs2 - self.Vu
        K = self.Sc + ll * self.Kr2
        K[-1, -1] += L / self.b.R
        G = self.P @ np.linalg.solve(K, self.P.T)
        Hp = self.S + ll * self.Vr2 + 3 * s * self.Vs2 - self.Vu - 2 * self.alpha * G
        Hp = 0.5 * (Hp + Hp.T)
        Hm = 0.5 * (Hm + Hm.T)
        return Hp, Hm

    def sym(self, H):
        Li = sla.solve_triangular(self.Mchol, np.eye(len(H)), lower=True)
        A = Li @ H @ Li.T
        return 0.5 * (A + A.T), Li

    def coeffs_of(self, f):
        """L2 projection of a function given at quadrature points onto the a-space."""
        rhs = self.Ba.T @ (self.b.wq * f)
        return np.linalg.solve(self.M, rhs)
