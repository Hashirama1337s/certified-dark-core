"""bracket.py - certified upper and lower counts of negative eigenvalues of L+(L), L-(L) (node BR), the constrained
L = 0 count (node D0/IDX), and the w-Neumann unit test (control C-W).

Forms (AUDIT-USE-R1-v2 items 2, 5b; REFEREE-R1-v2 item 2):
  L-(L) = -d^2 + ell/r^2 + s sigma^2 - u
  L+(L) = -d^2 + ell/r^2 + 3 s sigma^2 - u + 2 sigma G_L sigma,  written as the 2x2 Schur system in (a, w):
          -Y'' + Q Y = lam Y,  Q = [[ell/r^2 + 3 s sigma^2 - u - delta, sqrt2 sigma], [sqrt2 sigma, ell/r^2]]
          (the shift -delta enters the a-channel ONLY; the w-channel keeps P = -d^2 + ell/r^2 > 0).
UPPER count  #(L <= 0) <= #(interior problem < +eps):  a'(R) = 0 (Neumann), w'(R) = -(L/R) w(R) (exact exterior
             Robin), a-shift -delta with delta = (2/(2L+1)) sqrt(I1^2 - I_in(R)^2) (closed form), valid when
             |E| - m/R - delta > 0 (checked).  Left end: Robin start Y'(r0) = U_lo Y(r0), U_lo <= U_true(r0).
LOWER count  #(L < 0) >= #(Dirichlet interior problem < -eps): a(R) = 0, same Robin w, no shift, U_hi >= U_true.
Count at level lam (Morse index theorem with endpoint term):
     #(eig < lam) = #{r in (r0, R): det Y(r) = 0}  +  n_-( (U(R) + S) restricted to the free boundary directions )
     U(R) = Y'(R) Y(R)^-1,  S = diag(0, L/R);  Dirichlet-a keeps only the w-direction.
Zeros of det Y are certified step by step: the step enclosure excludes 0, or d/dr det Y excludes 0 on a
sub-interval (then at most one simple zero, counted by the certified endpoint signs).
"""
import sys, os, json, time
from flint import arb, ctx
import itaylor as it
import lincore as lc
import bg_tube as bt

SQ2 = None


def ustart(L, q, r0):
    """Robin start: eigenvalues of U_true(r0) lie in (L+1)/r0 +- eta (Frobenius-Volterra, Y = r^(L+1) Z)."""
    r0 = arb(r0)
    c = r0 * r0 * q / (2 * (2 * L + 3))
    assert c < arb('0.25')
    e1 = c / (1 - c)
    e2 = r0 * q * (1 + e1) / (2 * L + 3)
    eta = e2 / (1 - e1)
    base = arb(L + 1) / r0
    return base - eta, base + eta, eta


def qbound(s, sig0, u0, L, which, lam, delta, nu=0, r0=None):
    sg = abs(it.exact(sig0)) + arb('0.01')
    ua = abs(arb(u0)) + arb('0.01')
    if r0 is not None:   # item 3: the 0.01 margins are asserted from the series_start crude enclosure on [0, r0]
        bt.assert_start_margins(s, sig0, u0, r0, sg, ua)
    sq2 = arb(2).sqrt()
    # infinity-norm bound of Q~ = Q - ell/r^2 - lam on [0, r0] (sum of the two row bounds >= max)
    if which == '+':
        d1 = 3 * abs(arb(s)) * sg * sg + ua + abs(arb(delta)) + abs(arb(lam)) + nu + sq2 * sg
        d2 = sq2 * sg + abs(arb(lam)) + nu
        return arb((d1 + d2).upper())
    return arb((abs(arb(s)) * sg * sg + ua + abs(arb(lam)) + nu).upper())


def make_sys(s, L, which, lam, delta, forcing=False):
    ell = L * (L + 1)
    sq2 = arb(2).sqrt()
    if which == '+':
        terms = {'Va': [('ir2', ell), ('sig2', 3 * s), ('u', -1), ('one', -(arb(delta) + arb(lam)))],
                 'Vw': [('ir2', ell), ('one', -arb(lam))]}
        A = [(0, 0, ('jet', 'Va', 1)), (0, 1, ('jet', 'sig', sq2)), (1, 0, ('jet', 'sig', sq2)), (1, 1, ('jet', 'Vw', 1))]
        n = 2
    else:
        terms = {'Va': [('ir2', ell), ('sig2', s), ('u', -1), ('one', -arb(lam))]}
        A = [(0, 0, ('jet', 'Va', 1))]
        n = 1
    fo = {}
    quads = []
    if forcing:
        # extra column (index n) is the particular solution of Y'' = Q Y - (g, 0), g = r sigma; quadratures int Y_a g
        fo = {n: [(0, 'rsig', -1)]}
        quads = [('rsig', (c, 0), None, False) for c in range(n + 1)]   # int y_a(col c) * g dr
    return it.LinSys(n, A, forcing=fo, quads=quads), terms, n


class ZeroCounter:
    def __init__(self, n, K, ncols):
        self.n = n; self.K = K; self.count = 0; self.fail = None; self.ncols = ncols

    def detfun(self, v):
        n = self.n
        # v: flat list: col c occupies v[c*2n:(c+1)*2n] (values then derivatives)
        if n == 1:
            return v[0], v[1]
        y = [[v[c * 4 + i] for c in range(2)] for i in range(2)]
        yp = [[v[c * 4 + 2 + i] for c in range(2)] for i in range(2)]
        det = y[0][0] * y[1][1] - y[0][1] * y[1][0]
        dd = yp[0][0] * y[1][1] + y[0][0] * yp[1][1] - yp[0][1] * y[1][0] - y[0][1] * yp[1][0]
        return det, dd

    def on_step(self, rc, h, C, R, X0, X1):
        if self.fail:
            return
        m = 2 * self.n * self.ncols
        Cs = C[:m]; Rs = R[:m]
        self._h = arb(h)
        self._seg(Cs, Rs, arb(0), arb(h), 0, rc)

    def _seg(self, C, R, t1, t2, depth, rc):
        v = it.eval_sub(C, R, t1, t2, self.K, self._h)
        det, dd = self.detfun(v)
        if not det.contains(0):
            return
        if not dd.contains(0):
            d1, _ = self.detfun(it.eval_at(C, R, t1, self.K, self._h))
            d2, _ = self.detfun(it.eval_at(C, R, t2, self.K, self._h))
            if d1.contains(0) or d2.contains(0):
                if depth > 30:
                    self.fail = 'det endpoint contains 0 near r=%s' % float((rc + t1).mid())
                    return
            else:
                if (d1 > 0) != (d2 > 0):
                    self.count += 1
                return
        if depth > 30:
            self.fail = 'zero of det Y not isolated near r=%s' % float((rc + t1).mid())
            return
        tm = (t1 + t2) / 2
        self._seg(C, R, t1, tm, depth + 1, rc)
        self._seg(C, R, tm, t2, depth + 1, rc)


def endpoint_term(Y, Yp, n, L, R, bc):
    """n_- of (U + S) on the free boundary directions; returns (count, det, ok)."""
    if n == 1:
        y, yp = Y[0][0], Yp[0][0]
        if y.contains(0):
            return None, y, False
        if bc == 'D':
            return 0, y, True
        u = yp / y
        if u.contains(0):
            return None, u, False
        return (1 if u < 0 else 0), u, True
    a, b, c, d = Y[0][0], Y[0][1], Y[1][0], Y[1][1]
    det = a * d - b * c
    if det.contains(0):
        return None, det, False
    inv = [[d / det, -b / det], [-c / det, a / det]]
    U = [[Yp[i][0] * inv[0][j] + Yp[i][1] * inv[1][j] for j in range(2)] for i in range(2)]
    U01 = (U[0][1] + U[1][0]) / 2
    S11 = arb(L) / arb(R)
    if bc == 'D':
        m = U[1][1] + S11
        if m.contains(0):
            return None, m, False
        return (1 if m < 0 else 0), m, True
    M00 = U[0][0]; M11 = U[1][1] + S11
    dt = M00 * M11 - U01 * U01
    tr = M00 + M11
    if dt.contains(0):
        return None, dt, False
    if dt < 0:
        return 1, dt, True
    if tr.contains(0):
        return None, tr, False
    return (2 if tr < 0 else 0), dt, True


def count(bj, s, sig0, u0, L, which, lam, bc, R, delta, K, r0, side, nu=0, with_forcing=False):
    """#(eig < lam) of the interior problem on [0, R]. side 'lo' uses U_lo (upper bound), 'hi' uses U_hi."""
    sysd, terms, n = make_sys(s, L, which, lam, delta, forcing=with_forcing)
    q = qbound(s, sig0, u0, L, which, lam, delta, nu, r0=r0)
    Ulo, Uhi, eta = ustart(L, q, r0)
    U = Ulo if side == 'lo' else Uhi
    pi2 = (arb.pi() / arb(r0)) ** 2
    assert pi2 > q + 1, 'no-conjugate-point condition on [0, r0] fails'
    cols = []
    for c in range(n):
        v = [arb(0)] * (2 * n)
        v[c] = arb(1); v[n + c] = U
        cols.append(v)
    if with_forcing:
        cols.append([arb(0)] * (2 * n))
        cols.append([arb(0)] * (n + 1))
    zc = ZeroCounter(n, K, n)
    X, nst = lc.march(sysd, bj, cols, bj.r[0], R, K, terms=terms, on_step=zc.on_step)
    Y = [[X[c][i] for c in range(n)] for i in range(n)]
    Yp = [[X[c][n + i] for c in range(n)] for i in range(n)]
    ep, val, ok = endpoint_term(Y, Yp, n, L, R, bc)
    res = dict(L=L, which=which, lam=float(arb(lam).mid()), bc=bc, side=side, conj=zc.count, endpoint=ep,
               endpoint_val=val.str(8, radius=True), ok=bool(ok and zc.fail is None), fail=zc.fail, steps=nst,
               eta=float(eta.mid()))
    res['count'] = (zc.count + ep) if res['ok'] else None
    if with_forcing:
        res['X'] = X
    return res


def d0_node(bj, s, sig0, u0, R, delta, K, r0, info, steps, ext, nu=1):
    """node D0 (constrained count). For f in H^1(0,inf) with <f, g> = 0, g = r sigma:
         q(f) >= Q_[r0,R](f2, w2) + <U_nu c, c> + nu ||f1||^2 + c_ext ||f_e||^2
       and |<f2, g2>| <= |<f1,g1>| + |<f_e,g_e>|, so q(f) >= P(f2) := B[f2] + M |<f2, g2>|^2 with
         M = 1 / (||g1||^2/nu + ||g_e||^2/c_ext)      (Cauchy-Schwarz on the two reserves).
       Inertia (Haynsworth): n(B + M g g^T) = n(B) - 1 when B is invertible, d2 = <B^-1 g, g> < 0 and M > 1/|d2|.
       Hence n(L+(0) on (r sigma)^perp) <= n(B) - 1.
       B: 2x2 operator on [r0, R]: Neumann a, w' = 0 (L = 0 Robin), a-shift -delta, left Robin U_lo at level -nu."""
    res = count(bj, s, sig0, u0, 0, '+', arb(0), 'N', R, delta, K, r0, 'lo', nu=nu, with_forcing=True)
    if not res['ok']:
        return dict(ok=False, why='level-0 count of B failed', nB=None)
    X = res.pop('X')
    n = 2
    Yp = [[X[c][n + i] for c in range(n)] for i in range(n)]
    Fpp = [X[2][n + i] for i in range(n)]
    Q = X[3]                        # [int Y_a0 g, int Y_a1 g, int Fp_a g] over [r0, R]
    # F = Y C + Fp ; right BC (L = 0): a' = 0 and w' = 0  ->  Y'(R) C = -Fp'(R)
    rhs = [-Fpp[0], -Fpp[1]]
    dt = Yp[0][0] * Yp[1][1] - Yp[0][1] * Yp[1][0]
    if dt.contains(0):
        return dict(ok=False, why='BVP matrix singular', nB=res['count'])
    C0 = (rhs[0] * Yp[1][1] - Yp[0][1] * rhs[1]) / dt
    C1 = (Yp[0][0] * rhs[1] - Yp[1][0] * rhs[0]) / dt
    d2 = C0 * Q[0] + C1 * Q[1] + Q[2]
    g1, ge = gnorms(info, steps, R, r0, sig0, s)
    M = 1 / (g1 / nu + ge / ext)
    ok = bool(d2 < 0 and M * abs(d2) > 1)
    return dict(ok=ok, nB=res['count'], d2=d2.str(10, radius=True), M=M.str(4, radius=True),
                g1=g1.str(3), ge=ge.str(3), constrained_upper=(res['count'] - 1) if ok else None,
                detail=res)


def gnorms(info, steps, R, r0, sig0, s):
    """||g||^2 (g = r sigma) on [0, r0] (crude) and on [R, inf) (tube boxes on [R, R1] + tail bound)."""
    sg = abs(it.exact(sig0)) + arb('0.01')
    bt.assert_start_margins(s, sig0, info['u0'], r0, sg)      # item 3 (bracket.py:220)
    g1 = sg * sg * arb(r0) ** 3 / 3
    tot = arb(0)
    for st in steps:
        r = st['r']; h = st['h']
        if bool(r + h <= arb(R)):          # skip only steps certainly inside [0, R] (was a float compare)
            continue
        rI = r + it.tball(h)
        a_box = rI * st['B'][0]
        tot += h * (a_box * a_box).abs_upper()
    tail = info['a1'] ** 2 / (2 * info['kappa1'])
    return arb(g1.upper()), arb((tot + tail).upper())


def wneumann_test(s, n, sig0, R1, R, log=print):
    """control C-W: with a Neumann cut of the w-channel at R, the exterior L = 0 Schur form is unbounded below.
    Test pair: a = phi = sin^2(pi (r-R)/2) on [R, R+2]; w = C on [R, R+X], linear to 0 on [R+X, R+2X].
    Q(phi, w) = q_a(phi) + 2 sqrt2 C s0 + C^2/X with s0 = int sigma phi; at C = -sqrt2 s0 X:  Q = q_a(phi) - 2 s0^2 X."""
    steps, info, Yend = bt.get_tube(s, n, sig0, R1, log=log)
    it.set_prec(200)
    pi = arb.pi()
    s0 = arb(0); s2 = None; uu = None
    Ra = arb(R); R2 = Ra + 2
    for st in steps:
        r = st['r']; h = st['h']; rh = r + h
        if bool(rh <= Ra) or bool(r >= R2):
            continue
        # sub-interval [max(r, R), min(r+h, R+2)] in ball arithmetic (was float endpoints of the step)
        a_ = r if bool(r >= Ra) else Ra
        b_ = rh if bool(rh <= R2) else R2
        x = a_.union(b_)
        ph = (1 - (pi * (x - R)).cos()) / 2                       # = sin^2(pi (x-R)/2), which lies in [0, 1]
        plo = ph.lower()
        ph = (arb(0) if plo < 0 else arb(plo)).union(arb(ph.upper()))   # intersect with [0, inf) (no float rounding)
        s0 += (b_ - a_) * st['B'][0] * ph
        sq = st['B'][0] * st['B'][0]
        s2 = sq if s2 is None else s2.union(sq)
        uu = st['B'][2] if uu is None else uu.union(st['B'][2])
    # q_a(phi) = int phi'^2 + (3 s sigma^2 - u) phi^2 <= pi^2/4 + (3|s| max sigma^2 + max(-u)) * 3/4
    qa = pi * pi / 4 + (3 * abs(arb(s)) * arb(s2.upper()) + arb((-uu).upper())) * arb(3) / 4
    if s0.contains(0):
        return dict(ok=False, why='s0 not certified nonzero')
    s0lo = arb(abs(s0).lower()); qau = arb(qa.upper())
    X = arb((qau / (s0lo * s0lo)).upper())
    Qx_up = qau - 2 * s0lo * s0lo * X                               # Q(X) <= q_a,up - 2 |s0|_lo^2 X
    return dict(ok=bool(Qx_up < 0), R=R, s0_lo=it.flo(s0lo), s0_hi=it.fup(abs(s0)), qa_upper=it.fup(qau),
                X=it.fup(X), Q_at_X_upper=it.fup(Qx_up), slope_upper=it.fup(-2 * s0lo * s0lo),
                note='Q(X) <= q_a - 2 s0^2 X -> -inf as X -> inf (w-Neumann exterior Schur form unbounded below)')


def run(s, n, sig0, R1, Rs, eps, Ls, K=24, prec_lin=200, with_D0=True, log=print):
    t0 = time.time()
    steps, info, Yend = bt.get_tube(s, n, sig0, R1, log=log)
    it.set_prec(prec_lin)
    r0 = steps[0]['r']                 # the tube's own start point as a ball (was float(steps[0]['r'].mid()))
    bj = lc.BgJets(s, steps, Yend, K)
    E = info['E']; m = info['m']; I1 = info['I1']; u0 = info['u0']
    epsA = it.exact(eps)               # eps = 1e-3 -> exactly 1/1000 (was arb(1e-3), the double)
    res = dict(s=s, n=n, sig0=sig0, sig0_exact=str(it.Fraction(repr(sig0)) if isinstance(sig0, float) else sig0),
               R1=R1, eps=eps, K=K, E=E.str(12, radius=True), m=m.str(12, radius=True),
               tube_sha256=info.get('tube_sha256'), tube_source=info.get('tube_source'), radii={})
    for R in Rs:
        i = bj.index_of(R)
        st = steps[i]
        assert bool(st['r'] <= arb(R)), 'grid point used for I_in(R) is not certified <= R'
        Iin_lo = arb((u0 - st['Y'][2] - st['r'] * st['Y'][3]).lower())   # I_in(r) is increasing in r
        if not bool(Iin_lo >= 0):      # referee-5: clamp the lower end at 0 (a negative end would shrink delta)
            Iin_lo = arb(0)
        rr = {}
        for L in Ls:
            dlt = arb((2 / arb(2 * L + 1) * ((I1 * I1).upper() - Iin_lo * Iin_lo).sqrt()).upper())
            ext0 = -E - m / arb(R) - dlt                # exterior reserve at level 0 (D0 node, unchanged)
            ext = ext0 - epsA                           # item 4: upper counts are at level +eps: |E| - m/R - delta - eps
            row = dict(delta=dlt.str(6, radius=True), ext_margin=ext.str(6, radius=True), ext_ok=bool(ext > 0))
            for which in '+-':
                dl = dlt if which == '+' else arb(0)
                up = count(bj, s, sig0, u0, L, which, epsA, 'N', R, dl, K, r0, 'lo')
                lo = count(bj, s, sig0, u0, L, which, -epsA, 'D', R, arb(0), K, r0, 'hi')
                row[which] = dict(upper=up['count'] if row['ext_ok'] else None, lower=lo['count'], up_detail=up, lo_detail=lo)
                log('  R=%g L=%d %s: upper #(<+eps)=%s  lower #(<-eps)=%s  delta=%s [%.0fs]' % (
                    R, L, which, up['count'], lo['count'], row['delta'], time.time() - t0))
            if with_D0 and L == 0:
                d0 = d0_node(bj, s, sig0, u0, R, dlt, K, r0, info, steps, ext0)
                row['D0'] = d0
                log('  R=%g D0 node: n(B)=%s d2=%s M=%s ok=%s -> n(L+(0)|g-perp) <= %s' % (
                    R, d0.get('nB'), d0.get('d2'), d0.get('M'), d0.get('ok'), d0.get('constrained_upper')))
            rr[L] = row
        res['radii'][R] = rr
    res['seconds'] = time.time() - t0
    return res


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('s', type=int); ap.add_argument('n', type=int); ap.add_argument('sig0', type=float)
    ap.add_argument('R1', type=float); ap.add_argument('out')
    ap.add_argument('--R', default='14'); ap.add_argument('--L', default='0,1,2,3'); ap.add_argument('--eps', type=float, default=1e-3)
    ap.add_argument('--noD0', action='store_true'); ap.add_argument('--K', type=int, default=24)
    ap.add_argument('--wtest', type=float, default=None)
    a = ap.parse_args()
    if a.wtest is not None:
        res = wneumann_test(a.s, a.n, a.sig0, a.R1, a.wtest)
        print(res)
        json.dump(res, open(a.out, 'w'), indent=1, default=str)
        sys.exit(0)
    Rs = [float(x) for x in a.R.split(',')]
    Ls = [int(x) for x in a.L.split(',')]
    res = run(a.s, a.n, a.sig0, a.R1, Rs, a.eps, Ls, K=a.K, with_D0=not a.noD0)
    json.dump(res, open(a.out, 'w'), indent=1, default=str)
    print('seconds', res['seconds'])
