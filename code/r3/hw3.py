"""hw3.py - build-W instrument (R3-WINDOW, DESIGN-W3 sections 3.5 and HW3): certified counts and margin certificates
for the Krein-count operator

    H_L(w) = [[L+(L), -w], [-w, L-(L)]]   on pairs (a, d) (reduced radial functions),

carried, exactly as bracket.py carries L+, by the 3-channel Schur system Y = (a, d, W):

    -Y'' + Q Y = 0,   Q = [[ell/r^2 + 3 s sigma^2 - u - delta - m, -w, sqrt2 sigma],
                           [-w, ell/r^2 + s sigma^2 - u - m, 0],
                           [sqrt2 sigma, 0, ell/r^2]].

The level m sits in the a and d channels ONLY (DESIGN-W2 CPOSL; failure mode 5; asserted below: the W channel never
carries a level). chan='P' is the 2-channel L+ system (a, W) used by the penalised L = 0 certificate.

What each function certifies (every decision in arb; floats only steer):
  count()  #(interior form < level) on [r0, R] = conjugate points of det Y + n_-((U(R) + S) on free directions)
           (PROOF Lemma 4.4 for n = 2, 3; DESIGN-W2 CPOSL (a)), with per-step column re-basing by an exact
           invertible point matrix (zeros of det(Y M) = zeros of det Y).  side 'lo' (Robin U_lo, Neumann a, d,
           a-shift -delta) gives the UPPER count, side 'hi' (Robin U_hi, Dirichlet a, d, no shift) the LOWER count.
  cpos()   CPOSL (c): H(w) >= m ||x||^2 for every x = (a, d) in the form domain with <x, p_j> = 0, j = 1..k.
           Needs: ext = |E| - m_bg/R - delta - |w| - m > 0; n(B_m) = k; B_m invertible (det of the natural-BC matrix
           at R excludes 0); S_ij = <B_m^-1 P_i, P_j> negative definite (certified LDL pivots < 0) [Haynsworth with
           k vectors, CPOSL (b)].
  ritz()   RITZ: Gram matrices of the 3-channel form B (level 0, no shift) on k+1 explicit trial triples
           Y_j = (a_j, d_j, W_j) supported in [0, Rc]; A + m M0 negative definite (M0 = Gram of the (a, d) parts)
           gives H(w) <= B[(x, W(x))] <= -m ||x||^2 on span{x_j}  (H[x] = min over W of B[(x, W)]).
  pen()    CPOSL (d): penalised L = 0 endpoint certificate Pen = q+ + M' <., g>^2 >= m on {p}^perp, g = r sigma.

The explicit functions p_j (CPOS) and the trial triples (RITZ) are polynomials given by Chebyshev coefficients
(exact binary64 numbers) on [0, Rc]; p_j vanish outside [r0, R] by definition (the inner products are taken over
[r0, R] only), trial functions are r (Rc - r) * Chebyshev (so they vanish at 0 and at Rc and are 0 beyond Rc).
"""
import sys, os, json, time, math
from fractions import Fraction
from flint import arb, arb_poly, arb_series, ctx
import itaylor as it
import lincore as lc
import bracket as br
import bg_tube as bt

SQ2 = None


def sq2():
    return arb(2).sqrt()


# ------------------------------------------------------------------ explicit polynomial functions
def cheb_to_poly(coef, Rc):
    """arb_poly in r of sum_k coef[k] T_k(2 r / Rc - 1); coef are python floats read EXACTLY (arb(float))."""
    Rc = arb(Rc)
    x = arb_poly([arb(-1), 2 / Rc])
    b1 = arb_poly([0]); b2 = arb_poly([0])
    for k in range(len(coef) - 1, 0, -1):
        b1, b2 = arb_poly([arb(coef[k])]) + 2 * x * b1 - b2, b1
    return arb_poly([arb(coef[0])]) + x * b1 - b2


class PolyFn:
    """f(r) = poly(r) on [0, Rc] (and the caller's convention outside). kind 'p': plain; 'trial': r (Rc - r) * Cheb."""

    def __init__(self, coef, Rc, kind='p'):
        self.coef = [float(c) for c in coef]
        self.Rc = arb(Rc)
        P = cheb_to_poly(self.coef, self.Rc)
        if kind == 'trial':
            P = P * arb_poly([arb(0), self.Rc, arb(-1)])
        elif kind == 'trialW':
            P = P * arb_poly([arb(0), arb(1)])
        self.P = P                      # monomial form: used only for EXACT polynomial integrals (no interval argument)
        self.kind = kind
        self.deg = len(self.coef) - 1 + {'p': 0, 'trial': 2, 'trialW': 1}[kind]
        self._cache = {}

    def full(self, rc, mult=None):
        """all Taylor coefficients of f about the POINT-like ball rc (Clenshaw on arb_series: no monomial cancellation).
        mult: None = the function itself; 'over_r' = f / r (trial kind only: (Rc - r) * Cheb)."""
        nfull = self.deg + 1
        if ctx.cap < nfull + 2:
            ctx.cap = nfull + 2          # python-flint truncates every series operation at ctx.cap terms
        x = arb_series([2 * rc / self.Rc - 1, 2 / self.Rc], prec=nfull)
        b1 = arb_series([0], prec=nfull); b2 = arb_series([0], prec=nfull)
        for k in range(len(self.coef) - 1, 0, -1):
            b1, b2 = arb(self.coef[k]) + 2 * x * b1 - b2, b1
        f = arb(self.coef[0]) + x * b1 - b2
        if self.kind == 'trial':
            if mult == 'over_r':
                f = f * arb_series([self.Rc - rc, arb(-1)], prec=nfull)
            else:
                f = f * arb_series([rc * (self.Rc - rc), self.Rc - 2 * rc, arb(-1)], prec=nfull)
        elif self.kind == 'trialW':
            if mult != 'over_r':
                f = f * arb_series([rc, arb(1)], prec=nfull)
        c = f.coeffs()
        return [c[k] if k < len(c) else arb(0) for k in range(nfull)]

    def jets(self, rc, n, h=None):
        """Taylor coefficients 0..n-1 of f about rc; with h, the box jets about rc + tball(h) (exact shift of the
        complete point expansion by the interval T = tball(h): f is a polynomial, so this is an enclosure)."""
        key = (rc.mid().str(40), rc.rad().str(5), n, None if h is None else arb(h).str(30, radius=True))
        if key not in self._cache:
            F = self.full(rc)
            if h is not None:
                F = arb_poly(F)(arb_poly([it.tball(h), arb(1)])).coeffs()
            self._cache[key] = [F[k] if k < len(F) else arb(0) for k in range(n)]
        return self._cache[key]

    def value(self, r):
        """enclosure of f over the ball/interval r (Clenshaw with the interval argument)."""
        r = arb(r)
        x = 2 * r / self.Rc - 1
        b1 = arb(0); b2 = arb(0)
        for k in range(len(self.coef) - 1, 0, -1):
            b1, b2 = arb(self.coef[k]) + 2 * x * b1 - b2, b1
        f = arb(self.coef[0]) + x * b1 - b2
        if self.kind == 'trial':
            f = f * r * (self.Rc - r)
        elif self.kind == 'trialW':
            f = f * r
        return f


class FnJets(lc.BgJets):
    """BgJets plus named explicit functions (their jets about every grid point and over every step box)."""

    def __init__(self, base, fns):
        self.__dict__.update({k: v for k, v in base.__dict__.items() if k not in ('_pt', '_box')})
        self._pt = {}; self._box = {}
        self._base = base
        self.fns = fns          # name -> PolyFn

    def pt(self, i):
        if i not in self._pt:
            d = dict(self._base.pt(i))
            n = len(d['sig'])
            rc = self.steps[i]['r'] if i < len(self.steps) else self.r[-1]
            for nm, f in self.fns.items():
                d[nm] = f.jets(rc, n)
            self._pt[i] = d
        return self._pt[i]

    def box(self, i):
        if i not in self._box:
            d = dict(self._base.box(i))
            n = len(d['sig'])
            st = self.steps[i]
            for nm, f in self.fns.items():
                d[nm] = f.jets(st['r'], n, h=st['h'])
            self._box[i] = d
        return self._box[i]


# ------------------------------------------------------------------ small dense arb linear algebra
def det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def inv(M):
    """inverse by cofactors (n <= 3); None if det contains 0."""
    n = len(M)
    d = det(M)
    if d.contains(0):
        return None
    if n == 1:
        return [[1 / d]]
    if n == 2:
        return [[M[1][1] / d, -M[0][1] / d], [-M[1][0] / d, M[0][0] / d]]
    cof = [[None] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            mm = [[M[a][b] for b in range(3) if b != j] for a in range(3) if a != i]
            cof[i][j] = (-1) ** (i + j) * (mm[0][0] * mm[1][1] - mm[0][1] * mm[1][0])
    return [[cof[j][i] / d for j in range(3)] for i in range(3)]


def ldl_pivots(M):
    """pivots of the symmetric LDL^T recursion (interval); None if a pivot contains 0."""
    n = len(M); A = [row[:] for row in M]; piv = []
    for k in range(n):
        p = A[k][k]
        if p.contains(0):
            return None
        piv.append(p)
        for i in range(k + 1, n):
            f = A[i][k] / p
            for j in range(k + 1, n):
                A[i][j] = A[i][j] - f * A[k][j]
    return piv


def inertia_neg(M):
    p = ldl_pivots(M)
    if p is None:
        return None
    return sum(1 for x in p if x < 0)


def symm(M):
    n = len(M)
    return [[(M[i][j] + M[j][i]) / 2 for j in range(n)] for i in range(n)]


# ------------------------------------------------------------------ zero counter with per-step re-basing
class ZCn(br.ZeroCounter):
    """conjugate points of det Y (n x n, n = 2 or 3) with per-step re-basing (DESIGN-W2 HW3; probe P10c):
    det(Y M) = det(Y) det(M) for an EXACT point matrix M with det(M) != 0 (asserted), so zeros and their simplicity
    are those of det Y. M = float inverse of mid(Y(step start)), scaled (steering only)."""

    def detfun(self, v):
        n = self.n
        y = [[v[c * 2 * n + i] for c in range(n)] for i in range(n)]
        yp = [[v[c * 2 * n + n + i] for c in range(n)] for i in range(n)]
        d = det(y); dd = arb(0)
        for c in range(n):                                   # Jacobi: d/dr det = sum over columns
            m = [[(yp[i][j] if j == c else y[i][j]) for j in range(n)] for i in range(n)]
            dd += det(m)
        return d, dd

    def on_step(self, rc, h, C, R, X0, X1):
        if self.fail:
            return
        import numpy as _np
        n = self.n
        Y0 = _np.array([[float(X0[c][i].mid()) for c in range(n)] for i in range(n)])
        try:
            Mf = _np.linalg.inv(Y0)
            if not _np.all(_np.isfinite(Mf)):
                raise ValueError
        except Exception:
            Mf = _np.eye(n)
        Mf = Mf / _np.abs(Mf).max()
        M = [[arb(float(Mf[c][cp])) for cp in range(n)] for c in range(n)]
        if det(M).contains(0):
            M = [[arb(1 if c == cp else 0) for cp in range(n)] for c in range(n)]
        Cs = []; Rs = []
        for cp in range(n):
            for i in range(2 * n):
                Cs.append([sum((C[c * 2 * n + i][k] * M[c][cp] for c in range(n)), arb(0)) for k in range(len(C[0]))])
                Rs.append(sum((R[c * 2 * n + i] * M[c][cp] for c in range(n)), arb(0)))
        self._h = arb(h)
        self._seg(Cs, Rs, arb(0), arb(h), 0, rc)


# ------------------------------------------------------------------ march with re-basing of the propagated state
def march_rebase(sysd, bj, X0, r_from, r_to, K, terms, n, nreg, nqc, on_step):
    """lincore.march (outward only) with the first nreg columns (and their quadrature slots) multiplied after every
    step by an EXACT point matrix M (float inverse of the midpoint n x n block, scaled; det M != 0 asserted).
    Y -> Y M leaves the conjugate points (det(Y M) = det Y det M), U(R) = Y' Y^-1 and the BVP solution Y C + F
    (C -> M^-1 C) unchanged, and keeps the columns well conditioned so the enclosures do not wrap (HW3 build note).
    The matrix products are exact ball arithmetic; M only steers."""
    import numpy as _np
    rt = arb(r_to)
    i = bj.index_of(r_from)
    assert bool(bj.r[i].mid() == arb(r_from).mid()) and bool(bj.r[i].rad() == arb(r_from).rad()), 'r_from must BE a grid point'
    X = X0; nst = 0; pos = bj.r[i]
    nq = len(X0[-1]) if sysd.quads else 0
    while True:
        rc = bj.r[i]
        if float(rc.mid()) >= float(rt.mid()) - 1e-15:
            break
        h = bj.steps[i]['h']
        if float((rc + h).mid()) > float(rt.mid()) + 1e-15:
            h = rt - rc
        pos = rc + h
        jp = lc.scaled(bj.pt(i), terms); jb = lc.scaled(bj.box(i), terms)
        X1, C, R, B = it.lin_step(sysd, jp, jb, X, h, K)
        if on_step:
            on_step(rc, h, C, R, X, X1)
        # re-base the regular columns
        Yf = _np.array([[float(X1[c][r_].mid()) for c in range(nreg)] for r_ in range(n)])
        try:
            Mf = _np.linalg.inv(Yf)
            if not _np.all(_np.isfinite(Mf)):
                raise ValueError
            Mf = Mf / _np.abs(Mf).max()
        except Exception:
            Mf = _np.eye(nreg)
        M = [[arb(float(Mf[c][cp])) for cp in range(nreg)] for c in range(nreg)]
        if det(M).contains(0):
            M = [[arb(1 if c == cp else 0) for cp in range(nreg)] for c in range(nreg)]
        newcols = [[sum((X1[c][k] * M[c][cp] for c in range(nreg)), arb(0)) for k in range(2 * n)] for cp in range(nreg)]
        Xn = newcols + [X1[c] for c in range(nreg, len(X1) - (1 if nq else 0))]
        if nq:
            Q = list(X1[-1])
            for cp in range(nreg):
                for l in range(nqc):
                    Q[cp * nqc + l] = sum((X1[-1][c * nqc + l] * M[c][cp] for c in range(nreg)), arb(0))
            Xn.append(Q)
        X = Xn
        i += 1; nst += 1
        if float((rc + h).mid()) >= float(rt.mid()) - 1e-15:
            break
    if not (pos - rt).contains(0):
        raise RuntimeError('march_rebase: reached r=%s, not r_to=%s' % (pos, rt))
    return X, nst


# ------------------------------------------------------------------ the count
def _system(s, L, chan, w, lev, delta, pnames, with_G):
    """LinSys for chan 'H' (a, d, W) or 'P' (a, W). Forcing columns: one per p (channel a <- -pa, d <- -pd) and,
    if with_G, one with a <- -g (g = r sigma, jet 'rsig'). Quadratures: int Y_col,a pa + Y_col,d pd for every column
    and every p, and int Y_col,a g if with_G."""
    ell = L * (L + 1)
    S2 = sq2()
    w = arb(w); lev = arb(lev); delta = arb(delta)
    if chan == 'H':
        n = 3
        terms = {'Va': [('ir2', ell), ('sig2', 3 * s), ('u', -1), ('one', -(delta + lev))],
                 'Vd': [('ir2', ell), ('sig2', s), ('u', -1), ('one', -lev)],
                 'Vw': [('ir2', ell)]}                                  # W channel: NO level (asserted design rule)
        A = [(0, 0, ('jet', 'Va', 1)), (0, 1, ('const', -w)), (0, 2, ('jet', 'sig', S2)),
             (1, 0, ('const', -w)), (1, 1, ('jet', 'Vd', 1)),
             (2, 0, ('jet', 'sig', S2)), (2, 2, ('jet', 'Vw', 1))]
        iW = 2
    else:
        assert w == 0
        n = 2
        terms = {'Va': [('ir2', ell), ('sig2', 3 * s), ('u', -1), ('one', -(delta + lev))],
                 'Vw': [('ir2', ell)]}
        A = [(0, 0, ('jet', 'Va', 1)), (0, 1, ('jet', 'sig', S2)), (1, 0, ('jet', 'sig', S2)), (1, 1, ('jet', 'Vw', 1))]
        iW = 1
    assert all(not (nm == 'Vw' and any(x[0] == 'one' for x in lst)) for nm, lst in terms.items()), 'level in W channel'
    fo = {}
    quads = []
    ncol = n + len(pnames) + (1 if with_G else 0)
    for l, (pa, pd) in enumerate(pnames):
        f = []
        if pa is not None:
            f.append((0, pa, -1))
        if chan == 'H' and pd is not None:
            f.append((1, pd, -1))
        assert f, 'empty explicit vector'
        fo[n + l] = f
    if with_G:
        fo[n + len(pnames)] = [(0, 'rsig', -1)]
    for c in range(ncol):
        for (pa, pd) in pnames:                       # two quadrature slots per vector (a part, d part), always
            quads.append((pa if pa is not None else 'zero', (c, 0), None, False))
            if chan == 'H':
                quads.append((pd if pd is not None else 'zero', (c, 1), None, False))
        if with_G:
            quads.append(('rsig', (c, 0), None, False))
    return it.LinSys(n, A, forcing=fo, quads=quads), terms, n, iW, ncol


def qbound3(s, sig0, u0, w, lev, delta, nu, r0, chan):
    """>= sum of the row bounds of Q~ = Q - ell/r^2 on [0, r0] (levels at lev + nu in a, d only); margins asserted."""
    sg = abs(it.exact(sig0)) + arb('0.01'); ua = abs(arb(u0)) + arb('0.01')
    bt.assert_start_margins(s, sig0, u0, r0, sg, ua)
    S2 = sq2()
    lv = abs(arb(lev)) + arb(nu)
    rowa = 3 * abs(arb(s)) * sg * sg + ua + abs(arb(delta)) + lv + abs(arb(w)) + S2 * sg
    rowd = abs(arb(s)) * sg * sg + ua + lv + abs(arb(w))
    roww = S2 * sg
    q = rowa + roww + (rowd if chan == 'H' else 0)
    return arb(q.upper())


def count(bj, s, sig0, info, L, w, lev, bc, R, delta, K, r0, side, chan='H', pvecs=None, with_G=False, nu=0):
    """#(interior form < 0) of the 3- (or 2-) channel problem on [r0, R] at level lev (a, d only).
    side 'lo': Robin U_lo, bc 'N' (natural: a' = d' = 0, W' = -(L/R) W)  -> upper count of #(H(w) < lev).
    side 'hi': Robin U_hi, bc 'D' (a = d = 0, W Robin)                   -> lower count of #(H(w) < lev).
    pvecs: list of (name_a, name_d) jets present in bj (FnJets) -> forcing columns + quadratures (CPOS)."""
    pnames = pvecs or []
    sysd, terms, n, iW, ncol = _system(s, L, chan, w, lev, delta, pnames, with_G)
    q = qbound3(s, sig0, info['u0'], w, lev, delta, nu, r0, chan)
    Ulo, Uhi, eta = br.ustart(L, q, r0)
    U = Ulo if side == 'lo' else Uhi
    assert (arb.pi() / arb(r0)) ** 2 > q + 1, 'no-conjugate-point condition on [0, r0] fails'
    cols = []
    for c in range(n):
        v = [arb(0)] * (2 * n); v[c] = arb(1); v[n + c] = U
        cols.append(v)
    for c in range(n, ncol):
        cols.append([arb(0)] * (2 * n))
    nq = len(sysd.quads)
    if nq:
        cols.append([arb(0)] * nq)
    zc = ZCn(n, K, n)
    nqc = (nq // ncol) if nq else 0
    X, nst = march_rebase(sysd, bj, cols, bj.r[0], R, K, terms, n, n, nqc, zc.on_step)
    Y = [[X[c][i] for c in range(n)] for i in range(n)]
    Yp = [[X[c][n + i] for c in range(n)] for i in range(n)]
    res = dict(L=L, chan=chan, w=float(arb(w).mid()), lev=float(arb(lev).mid()), bc=bc, side=side, R=R, steps=nst,
               conj=zc.count, fail=zc.fail)
    d = det(Y)
    if d.contains(0) or zc.fail:
        res.update(ok=False, why=zc.fail or 'det Y(R) contains 0', count=None)
        return res
    Yi = inv(Y)
    Um = [[sum((Yp[i][k] * Yi[k][j] for k in range(n)), arb(0)) for j in range(n)] for i in range(n)]
    Us = symm(Um)
    Us[iW][iW] = Us[iW][iW] + arb(L) / arb(R)
    if bc == 'D':
        m = Us[iW][iW]
        ep = None if m.contains(0) else (1 if m < 0 else 0)
    else:
        ep = inertia_neg(Us)
    if ep is None:
        res.update(ok=False, why='endpoint inertia undecided', count=None)
        return res
    res.update(ok=True, endpoint=ep, count=zc.count + ep)
    if pnames or with_G:
        res['X'] = X
        res['nq'] = nq
    return res


def _bvp_coeffs(X, n, iW, L, R, ncol):
    """natural BC at R for h = Y C + F:  (Y'(R) + S Y(R)) C = -(F'(R) + S F(R)),  S = diag(0.., L/R) on W."""
    SR = arb(L) / arb(R)
    M = [[X[c][n + i] + (SR * X[c][i] if i == iW else 0) for c in range(n)] for i in range(n)]
    Mi = inv(M)
    if Mi is None:
        return None, det(M)
    Cs = []
    for f in range(n, ncol):
        rhs = [-(X[f][n + i] + (SR * X[f][i] if i == iW else 0)) for i in range(n)]
        Cs.append([sum((Mi[c][i] * rhs[i] for i in range(n)), arb(0)) for c in range(n)])
    return Cs, det(M)


def ext_margin(info, R, delta, w, m):
    E = info['E']; mb = info['m']
    return -E - mb / arb(R) - arb(delta) - abs(arb(w)) - arb(m)


def delta_L(steps, info, bj, R, L):
    """delta_L(R) = (2/(2L+1)) sqrt(I1^2 - I_in(R)^2) with the referee-5 clamp (as bracket.run)."""
    i = bj.index_of(R); st = steps[i]
    assert bool(st['r'] <= arb(R))
    I1 = info['I1']; u0 = info['u0']
    Iin_lo = arb((u0 - st['Y'][2] - st['r'] * st['Y'][3]).lower())
    if not bool(Iin_lo >= 0):
        Iin_lo = arb(0)
    return arb((2 / arb(2 * L + 1) * ((I1 * I1).upper() - Iin_lo * Iin_lo).sqrt()).upper())


def cpos(bj0, steps, info, s, sig0, L, w, m, R, K, pfns, chan='H'):
    """CPOSL (c) at one node: H(w) >= m on {x : <x, p_j> = 0}. pfns: list of (PolyFn_a, PolyFn_d or None)."""
    t0 = time.time()
    r0 = steps[0]['r']
    dl = delta_L(steps, info, bj0, R, L)
    ext = ext_margin(info, R, dl, w, m)
    fns = {'zero': PolyFn([0.0], arb(R))}; pn = []
    for j, (fa, fd) in enumerate(pfns):
        if fa is not None:
            fns['p%da' % j] = fa
        if fd is not None:
            fns['p%dd' % j] = fd
        pn.append((('p%da' % j) if fa is not None else None, ('p%dd' % j) if fd is not None else None))
    bj = FnJets(bj0, fns)
    k = len(pfns)
    res = dict(kind='CPOS', L=L, w=float(arb(w).mid()), m=float(arb(m).mid()), R=R, k=k, chan=chan,
               delta=dl.str(6, radius=True), ext=ext.str(6, radius=True), ext_ok=bool(ext > 0))
    c = count(bj, s, sig0, info, L, w, m, 'N', R, dl, K, r0, 'lo', chan=chan, pvecs=pn)
    res.update(nB=c.get('count'), conj=c.get('conj'), endpoint=c.get('endpoint'), count_ok=c['ok'], why=c.get('why'))
    ok = bool(res['ext_ok'] and c['ok'] and c['count'] == k)
    if c['ok'] and k > 0:
        n = 3 if chan == 'H' else 2
        iW = n - 1
        X = c['X']; Q = X[-1]
        Cs, dM = _bvp_coeffs(X, n, iW, L, R, n + k)
        if Cs is None:
            ok = False; res['why'] = 'natural-BC matrix singular (B_m not invertible)'
        else:
            per = 2 if chan == 'H' else 1
            nqc = per * k                                 # quadratures per column
            def quad(col, l):
                b = col * nqc + l * per
                return Q[b] + (Q[b + 1] if per == 2 else 0)
            S = [[None] * k for _ in range(k)]
            for j in range(k):
                for l in range(k):
                    S[j][l] = sum((Cs[j][cc] * quad(cc, l) for cc in range(n)), arb(0)) + quad(n + j, l)
            Ss = symm(S)
            piv = ldl_pivots(Ss)
            negdef = piv is not None and all(bool(p < 0) for p in piv)
            res['S'] = [[x.str(8, radius=True) for x in row] for row in Ss]
            res['S_pivots'] = None if piv is None else [p.str(6, radius=True) for p in piv]
            res['S_negdef'] = bool(negdef)
            res['detM'] = dM.str(6, radius=True)
            ok = ok and negdef
    res['ok'] = bool(ok)
    res['seconds'] = time.time() - t0
    return res


# ------------------------------------------------------------------ RITZ (Gram of the 3-channel form)
def _ser(lst, n):
    return [lst[k] if k < len(lst) else arb(0) for k in range(n)]


def _mul(A, B, n):
    return [it.conv(A, B, k) for k in range(n)]


def gram(bj, steps, info, s, sig0, L, w, trials, Rc):
    """A_ij = B(Y_i, Y_j) (3-channel form at level 0 on [0, Rc]; Y_j = 0 beyond Rc and Y_j(Rc) = 0) and
    M0_ij = <x_i, x_j> (a, d parts). Polynomial parts (|Y'|^2, ell/r^2 Y^2, -2 w a d) are integrated EXACTLY
    (arb_poly); the background parts ((3 s sigma^2 - u) a^2, (s sigma^2 - u) d^2, 2 sqrt2 sigma a W) by rigorous
    Taylor quadrature along the tube grid on [r0, Rc] (pt jets to order Kq, remainder from box jets) plus a crude
    bound on [0, r0]."""
    ell = L * (L + 1); S2 = sq2(); w = arb(w); Rc = arb(Rc)
    nt = len(trials)
    zero = arb_poly([0])
    A = [[arb(0)] * nt for _ in range(nt)]; M0 = [[arb(0)] * nt for _ in range(nt)]
    # exact polynomial parts on [0, Rc]: every factor is expanded about the centre c = Rc/2 (stable Clenshaw series),
    # products are complete (no truncation), and int_{-H}^{H} t^k dt is exact (H = Rc/2).
    for tr in trials:
        assert tr[0].kind == 'trial' and tr[1].kind == 'trial', 'RITZ: a, d must vanish at 0 and at Rc'
        assert tr[2].kind in ('trial', 'trialW'), 'RITZ: W must vanish at 0'
    # W is extended beyond Rc by W(Rc) (Rc/r)^L: exterior cost exactly (L/Rc) W(Rc)^2 (PROOF Theorem 4.5 (L+) step 1;
    # L = 0: constant extension, cost 0); a = d = 0 beyond Rc, so no exterior coupling.
    WR = [tr[2].value(Rc) for tr in trials]
    cen = Rc / 2
    def ex(f, mult=None):
        return arb_poly(f.full(cen, mult))
    def integ(P):
        c = P.coeffs(); s_ = arb(0)
        for k in range(0, len(c), 2):
            s_ += c[k] * 2 * cen ** (k + 1) / (k + 1)
        return s_
    Ex = [[ex(f) for f in tr] for tr in trials]
    Ed = [[e.derivative() for e in row] for row in Ex]
    Er = [[ex(f, 'over_r') for f in tr] for tr in trials] if ell else None
    for i in range(nt):
        for j in range(i, nt):
            g = zero
            for c in range(3):
                g = g + Ed[i][c] * Ed[j][c]
                if ell:
                    g = g + ell * Er[i][c] * Er[j][c]          # ell/r^2 f_i f_j = ell (f_i/r)(f_j/r)
            g = g - w * (Ex[i][0] * Ex[j][1] + Ex[i][1] * Ex[j][0])
            A[i][j] = integ(g) + (arb(L) / Rc) * WR[i] * WR[j]
            M0[i][j] = integ(Ex[i][0] * Ex[j][0] + Ex[i][1] * Ex[j][1])
    # background parts on [r0, Rc] by Taylor quadrature
    Kq = bj.Kl
    n = Kq + 1
    r0 = steps[0]['r']
    for idx, st in enumerate(steps):
        r = st['r']; hh = st['h']
        if bool(r >= Rc):
            break
        if bool(r + hh > Rc):
            hh = Rc - r
            assert bool(hh > 0)
        jp = bj.pt(idx); jb = bj.box(idx)
        rI = r + it.tball(hh)
        def pots(J, N):
            Va = [3 * arb(s) * J['sig2'][k] - J['u'][k] for k in range(N)]
            Vd = [arb(s) * J['sig2'][k] - J['u'][k] for k in range(N)]
            Sg = [S2 * J['sig'][k] for k in range(N)]
            return Va, Vd, Sg
        Vap, Vdp, Sgp = pots(jp, n + 1)
        Vab, Vdb, Sgb = pots(jb, n + 1)
        fp = [[_ser(f.jets(r, n + 1), n + 1) for f in tr] for tr in trials]
        fb = [[_ser(f.jets(r, n + 1, h=hh), n + 1) for f in tr] for tr in trials]
        hp = [arb(hh) ** (k + 1) / (k + 1) for k in range(n + 1)]
        for i in range(nt):
            QYp = [_add(_mul(Vap, fp[i][0], n + 1), _mul(Sgp, fp[i][2], n + 1)), _mul(Vdp, fp[i][1], n + 1),
                   _mul(Sgp, fp[i][0], n + 1)]
            QYb = [_add(_mul(Vab, fb[i][0], n + 1), _mul(Sgb, fb[i][2], n + 1)), _mul(Vdb, fb[i][1], n + 1),
                   _mul(Sgb, fb[i][0], n + 1)]
            for j in range(i, nt):
                gp = [sum((it.conv(fp[j][c], QYp[c], k) for c in range(3)), arb(0)) for k in range(n)]
                gr = sum((it.conv(fb[j][c], QYb[c], n) for c in range(3)), arb(0))   # order-n coefficient over the box
                # int_0^h g = sum_{k<n} g_k h^(k+1)/(k+1) + int_0^h t^n R(t) dt, R(t) in gr (Lagrange; t^n >= 0)
                val = sum((gp[k] * hp[k] for k in range(n)), arb(0)) + gr * hp[n]
                A[i][j] = A[i][j] + val
    # crude [0, r0] part of the background terms
    sg = abs(it.exact(sig0)) + arb('0.01'); ua = abs(arb(info['u0'])) + arb('0.01')
    bt.assert_start_margins(s, sig0, info['u0'], r0, sg, ua)
    Vmax = 3 * abs(arb(s)) * sg * sg + ua + S2 * sg
    I0 = arb(0).union(r0)
    for i in range(nt):
        for j in range(i, nt):
            mi = max_abs([f.value(I0) for f in trials[i]]); mj = max_abs([f.value(I0) for f in trials[j]])
            A[i][j] = A[i][j] + arb(0, 1) * (r0 * Vmax * 3 * mi * mj)
    for i in range(nt):
        for j in range(i):
            A[i][j] = A[j][i]; M0[i][j] = M0[j][i]
    return A, M0


def _add(a, b):
    return [x + y for x, y in zip(a, b)]


def max_abs(vals):
    m = arb(0)
    for v in vals:
        m = arb(m.union(abs(v)).upper())
    return arb(m.upper())


def ritz(bj, steps, info, s, sig0, L, w, trials, Rc, m):
    """certify A + m M0 negative definite (and M0 positive definite): H(w) <= -m on span{x_j}."""
    t0 = time.time()
    A, M0 = gram(bj, steps, info, s, sig0, L, w, trials, Rc)
    mA = arb(m)
    T = [[A[i][j] + mA * M0[i][j] for j in range(len(A))] for i in range(len(A))]
    piv = ldl_pivots(T); pivM = ldl_pivots(M0)
    ok = (piv is not None and all(bool(p < 0) for p in piv) and pivM is not None and all(bool(p > 0) for p in pivM))
    return dict(kind='RITZ', L=L, w=float(arb(w).mid()), m=float(mA.mid()), k1=len(trials), Rc=float(arb(Rc).mid()),
                ok=bool(ok), pivots=None if piv is None else [p.str(6, radius=True) for p in piv],
                M0_pivots=None if pivM is None else [p.str(6, radius=True) for p in pivM],
                A=[[x.str(8, radius=True) for x in row] for row in A], seconds=time.time() - t0)


# ------------------------------------------------------------------ Pen (CPOSL (d), L = 0)
def pen(bj0, steps, info, s, sig0, m, R, K, pfn, Mp=5, nu=1):
    """Pen = q+ + M' <., g>^2 >= m on {p}^perp (L = 0, 2-channel L+ form; g = r sigma at THIS node).
    Exterior split (CPOSL (d)): theta in (0, 1) with M' (1/theta - 1)(||g1||^2/nu + ||g_e||^2/c') <= 1,
    c' = ext0 - m (ext0 = |E| - m/R - delta_0(R)); Robin at level m + nu. Then
    Pen[x] - m||x||^2 >= B_m[Y2] + M'' <Y2, G>^2, M'' = M'(1 - theta).  Certificate: n(B_m) = 2, s = <B_m^-1 ., .>
    on (P, G): d2 = s_GG < 0, M''|d2| > 1, and s_PP - M'' s_PG^2 / (1 + M'' d2) < 0."""
    t0 = time.time()
    r0 = steps[0]['r']
    dl = delta_L(steps, info, bj0, R, 0)
    ext0 = -info['E'] - info['m'] / arb(R) - dl
    cpr = ext0 - arb(m)
    g1, ge = br.gnorms(info, steps, R, r0, sig0, s)
    Mp = arb(Mp); nu = arb(nu)
    Kc = g1 / nu + ge / cpr
    # choose theta = 2 M' Kc / (1 + 2 M' Kc) (exact arb), then check M'(1/theta - 1) Kc <= 1
    theta = arb(((2 * Mp * Kc) / (1 + 2 * Mp * Kc)).upper())
    cond_theta = bool(theta < 1 and Mp * (1 / theta - 1) * Kc <= 1)
    Mpp = Mp * (1 - theta)
    bj = FnJets(bj0, {'p0a': pfn, 'zero': PolyFn([0.0], arb(R))})
    c = count(bj, s, sig0, info, 0, 0, m, 'N', R, dl, K, r0, 'lo', chan='P', pvecs=[('p0a', None)], with_G=True, nu=nu)
    res = dict(kind='PEN', m=float(arb(m).mid()), R=R, Mp=float(Mp.mid()), theta=theta.str(4), cprime=cpr.str(6),
               ext_ok=bool(cpr > 0), cond_theta=cond_theta, nB=c.get('count'), count_ok=c['ok'], why=c.get('why'))
    ok = bool(cpr > 0 and cond_theta and c['ok'] and c['count'] == 2)
    if c['ok']:
        X = c['X']; Q = X[-1]
        Cs, dM = _bvp_coeffs(X, 2, 1, 0, R, 4)
        if Cs is None:
            ok = False; res['why'] = 'B_m not invertible'
        else:
            # quads per column: [int Y_a p, int Y_a g]
            def qd(col, which):
                return Q[col * 2 + which]
            s_ = [[None] * 2 for _ in range(2)]
            for j in range(2):            # forcing j: 0 = P, 1 = G
                for l in range(2):
                    s_[j][l] = sum((Cs[j][cc] * qd(cc, l) for cc in range(2)), arb(0)) + qd(2 + j, l)
            ss = symm(s_)
            sPP, sPG, d2 = ss[0][0], ss[0][1], ss[1][1]
            c1 = bool(d2 < 0 and Mpp * abs(d2) > 1)
            sm = sPP - Mpp * sPG * sPG / (1 + Mpp * d2)
            c2 = bool(sm < 0)
            res.update(d2=d2.str(8, radius=True), Mpp_d2=(Mpp * abs(d2)).str(5), sPP=sPP.str(8, radius=True),
                       sPG=sPG.str(8, radius=True), sherman=sm.str(8, radius=True), c1=c1, c2=c2)
            ok = ok and c1 and c2
    res['ok'] = bool(ok)
    res['seconds'] = time.time() - t0
    return res


# ------------------------------------------------------------------ node setup helper
def setup(steps, Yend, K=24, prec=200):
    it.set_prec(prec)
    return lc.BgJets(1, steps, Yend, K)
