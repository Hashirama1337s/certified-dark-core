"""kraw.py - Krawczyk existence/uniqueness test for the nonlinear eigenproblem M(par) v = 0, v_k0 = 1, in real (Krein,
par = w) or complex (Evans, par = lam) arithmetic.

  unknowns x = (par, v_j for j != k0) (column-scaled: M -> M D with D exact powers of two),
  F(x) = M(par) v,  J(x) = [M'(par) v | M e_j (j != k0)],
  K(X) = x~ - C F(x~) + (I - C J(X)) (X - x~),  C ~ J(x~)^-1 (any matrix).
  If K(X) lies in int(X) then F has exactly one zero in X and J is invertible there (Krawczyk 1969; Moore; Rump).
  For complex balls the mean-value inclusion holds componentwise in the convex hull of J(X) (integral form), so the
  test is valid for acb discs too.
"""
import math
import numpy as np
from flint import arb, acb


def _ball(field, c, r):
    if field == 'real':
        return arb(c) + arb(0, r)
    return acb(c) + acb(arb(0, r), arb(0, r))


def _pt(field, c):
    return arb(c) if field == 'real' else acb(c)


def _f(x):
    if isinstance(x, acb):
        return complex(float(x.real.mid()), float(x.imag.mid()))
    return float(x.mid())


def fmat(M):
    return np.array([[_f(x) for x in row] for row in M])


def _rad(x):
    if isinstance(x, acb):
        return max(float(x.real.rad()), float(x.imag.rad()))
    return float(x.rad())


def newton(evalpt, par0, field, iters=8, log=print, tol=1e-11):
    """float Newton on (par, v) using midpoints of certified evaluations (heuristic). evalpt(par, deriv) -> dict."""
    p = par0
    k0 = None
    for itn in range(iters):
        R = evalpt(_pt(field, p), True)
        if not R['ok']:
            raise RuntimeError(R['why'])
        M = fmat(R['M']); dM = fmat(R['dM'])
        sc = 1 / np.max(np.abs(M), axis=0)
        Ms = M * sc; dMs = dM * sc
        U, S, Vt = np.linalg.svd(Ms)
        v = np.conj(Vt[-1])
        if k0 is None:
            k0 = int(np.argmax(np.abs(v)))
        v = v / v[k0]
        F = Ms @ v
        J = np.column_stack([dMs @ v] + [Ms[:, j] for j in range(6) if j != k0])
        d = np.linalg.solve(J, -F)
        p = p + d[0]
        if field == 'real':
            p = float(np.real(p))
        log('    newton it %d: par=%s |F|=%.2e svmin/svmax=%.2e' % (itn, p, np.linalg.norm(F), S[-1] / S[0]))
        if abs(d[0]) < tol * max(1.0, abs(p)):
            break
    return p, k0, sc


def test(evalpt, evalbox, par, k0, D, field, rho_p, rho_v, vf=None, log=print):
    """one Krawczyk test around (par, vf); returns (inside, Kx, X, Rbox)."""
    def scaled(M):
        return [[M[i][j] * D[j] for j in range(6)] for i in range(6)]
    Rp = evalpt(_pt(field, par), False)
    if not Rp['ok']:
        return False, None, None, Rp, None
    Mp = scaled(Rp['M'])
    if vf is None:
        U, S, Vt = np.linalg.svd(fmat(Mp))
        vf = np.conj(Vt[-1]); vf = vf / vf[k0]
    if field == 'real':
        vf = np.real(vf)
    P = _ball(field, par, rho_p)
    Rb = evalbox(P, rho_p)
    if not Rb['ok']:
        return False, None, None, Rb, vf
    Mb = scaled(Rb['M']); dMb = scaled(Rb['dM'])
    idx = [j for j in range(6) if j != k0]
    z = _pt(field, 0)
    rv = rho_v if np.ndim(rho_v) else [rho_v] * 6
    Vb = [_pt(field, 1) if j == k0 else _ball(field, vf[j], rv[j]) for j in range(6)]
    vt = [_pt(field, 1) if j == k0 else _pt(field, vf[j]) for j in range(6)]
    Fx = [sum((Mp[i][j] * vt[j] for j in range(6)), z) for i in range(6)]
    J = [[sum((dMb[i][j] * Vb[j] for j in range(6)), z)] + [Mb[i][j] for j in idx] for i in range(6)]
    C = np.linalg.inv(fmat(J))
    Ca = [[_pt(field, C[i][j] if field == 'complex' else float(np.real(C[i][j]))) for j in range(6)] for i in range(6)]
    xt = [_pt(field, par)] + [vt[j] for j in idx]
    X = [P] + [Vb[j] for j in idx]
    dX = [X[i] - xt[i] for i in range(6)]
    CF = [sum((Ca[i][k] * Fx[k] for k in range(6)), z) for i in range(6)]
    CJ = [[sum((Ca[i][k] * J[k][j] for k in range(6)), z) for j in range(6)] for i in range(6)]
    Kx = [xt[i] - CF[i] + sum((((1 if i == j else 0) - CJ[i][j]) * dX[j] for j in range(6)), z) for i in range(6)]
    inside = all(X[i].contains_interior(Kx[i]) for i in range(6))
    return inside, Kx, X, Rb, vf


def certify(evalpt, evalbox, par0, field, rel=(1e-9, 1e-10, 1e-8, 1e-7), refine=1, log=print):
    p, k0, sc = newton(evalpt, par0, field, log=log)
    D = [arb(float(2.0 ** round(math.log2(x)))) for x in sc]
    best = None
    for rr in rel:
        rho_p = rr * max(1.0, abs(p))
        inside, Kx, X, Rb, vf = test(evalpt, evalbox, p, k0, D, field, rho_p, rr, log=log)
        log('   Krawczyk rel=%.0e: inside=%s  K(par)=%s' % (rr, inside, Kx[0].str(12, radius=True) if Kx else None))
        # epsilon-inflation (Rump): same centre, per-component radii grown to cover K(X)
        idx = [j for j in range(6) if j != k0]
        rv = [rr] * 6
        for _inf in range(4):
            if inside or Kx is None:
                break
            xt = [p] + [vf[j] for j in idx]
            rad = [abs(_f(Kx[i]) - xt[i]) + _rad(Kx[i]) for i in range(6)]
            rho_p = max(rho_p, 2 * rad[0])
            for t_, j in enumerate(idx):
                rv[j] = max(rv[j], 2 * rad[1 + t_])
            inside, Kx, X, Rb, vf = test(evalpt, evalbox, p, k0, D, field, rho_p, rv, vf=vf, log=log)
            log('   inflate %d: inside=%s  K(par)=%s' % (_inf, inside, Kx[0].str(12, radius=True) if Kx else None))
        if inside:
            best = (Kx, Rb, rr)
            break
    if best is None:
        return dict(ok=False, par_guess=p, k0=k0)
    for _ in range(refine):
        Kx, Rb, rr = best
        pc = _f(Kx[0]); vc = {}
        idx = [j for j in range(6) if j != k0]
        vf = np.zeros(6, dtype=complex if field == 'complex' else float); vf[k0] = 1
        rv = [0.0] * 6
        for t_, j in enumerate(idx):
            vf[j] = _f(Kx[1 + t_]); rv[j] = max(3 * _rad(Kx[1 + t_]), 1e-14)
        rho_p = max(3 * _rad(Kx[0]), 1e-14)
        inside, Kx2, X2, Rb2, _ = test(evalpt, evalbox, pc, k0, D, field, rho_p, rv, vf=vf, log=log)
        log('   refine: inside=%s K(par)=%s' % (inside, Kx2[0].str(15, radius=True) if Kx2 else None))
        if not inside:
            break
        best = (Kx2, Rb2, rr)
    Kx, Rb, rr = best
    idx = [j for j in range(6) if j != k0]
    vbox = [None] * 6
    vbox[k0] = _pt(field, 1)
    for t_, j in enumerate(idx):
        vbox[j] = Kx[1 + t_]
    v = [vbox[j] * D[j] for j in range(6)]
    return dict(ok=True, par=Kx[0], v=v, Rb=Rb, k0=k0, rel=rr)
