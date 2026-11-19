"""green.py - build-W instrument GREEN (R3-WINDOW, DESIGN-W3 section 3.6 / 3.6b): certified Green kernel of the
background linearisation L_a at a certified node a, and the X-norm bounds the branch lemma BR needs.

Reduced variables (DESIGN-W2 3.6): Y = (a, W) = (r d, -r v / sqrt2), L_a z = f  <=>  -Y'' + Q Y = F,
    Q = [[3 sigma^2 - u, sqrt2 sigma], [sqrt2 sigma, 0]],   F = (r f1, -r f2 / sqrt2).
(This is bracket.make_sys(1, 0, '+', 0, 0): the L = 0 Schur system at level 0, no shift.)
Spaces: om(r) = 1 + (r/4)^2, s_u = 3;  ||z||_X = max(sup om |d|, sup |v| / s_u);  ||f||_FF = max(sup om |f1|, sup om^2 |f2|).

Solution operator G_a (DESIGN-W3 3.6b): y = G_a f is the unique solution with y regular, d(0) = a'(0) = 0, a not
growing (y in rho := {solutions with no exponentially growing a-part} = V1^perp), W at most linear (v bounded).
With the Wronskian [f, g] := f.g' - f'.g (constant on solutions) and
    U2  : regular solution, a'(0) = 0, W'(0) = 1                (marched outward from r0; series start)
    V1  : a decays, W -> 0  (EXT lemma at R1; marched inward; scale fixed by a(r_x) = 1: V1hat)
    Z1, Z2 : basis of rho cap U2^perp, data at r_x: W = 1, W' = 0 / W = 0, W' = 1, a, a' from [Z, V1hat] = [Z, U2] = 0
    alpha := [U2, V1hat],  c := [Z1, Z2]   (both certified != 0: the nondegeneracy of DESIGN-W3 BR)
the kernel of G_a is (every term a product of a function at the smaller argument that does not grow inward and a
function at the larger argument that does not grow outward, so no cancellation is needed on boxes):
    s > r:  G(r, s) = - U2(r) V1hat(s)^T / alpha
    s < r:  G(r, s) = - V1hat(r) U2(s)^T / alpha + (Z1(r) Z2(s)^T - Z2(r) Z1(s)^T) / c.
tau (first variation, d(0) = 1): tau = U1 + beta U2, beta = -[U1, V1hat]/[U2, V1hat] (U1: a'(0) = 1, W'(0) = 0);
it lies in rho cap U2^perp, so tau = lam1 Z1 + lam2 Z2 with (lam1, lam2) = (tau_W, tau_W')(r_x); the a-parts are
checked to overlap (assertion). tau is built ONLY from certified marches (DESIGN-W3 fix; injected data are refused).

Everything is ball arithmetic; floats only steer (grid index of r_x, sub-box count, midpoints for re-basing).
"""
import sys, os, json, time, math, hashlib
from flint import arb, ctx
import itaylor as it
import lincore as lc
import bracket as br
import bg_tube as bt

SU = int(os.environ.get("WSU", "3"))      # s_u of the X norm (DESIGN-W2: 3); env override for calibration only


def om(r):
    r = arb(r)
    return 1 + (r / 4) ** 2


def sq2():
    return arb(2).sqrt()


def up(x):
    return arb(arb(x).upper())


def absup(x):
    return arb(abs(arb(x)).upper())


def hull(a, b):
    return a.union(b)


# ------------------------------------------------------------------ background series at 0 (as bg_tube.series_start)
def bg_series(s, sig0, u0, N=12):
    """the Taylor coefficients S_j, U_j of sigma = sum S_j r^(2j), u = sum U_j r^(2j) (bg_tube.series_start recursion,
    copied verbatim so that the same polynomial p is used; u0 may be the tube interval)."""
    sA = arb(s)
    sg0 = it.exact(sig0)
    S = [sg0]; U = [arb(u0)]
    for j in range(N):
        S2 = sum((S[i] * S[j - i] for i in range(j + 1)), arb(0))
        S2l = [sum((S[i] * S[k - i] for i in range(k + 1)), arb(0)) for k in range(j + 1)]
        S3 = sum((S2l[i] * S[j - i] for i in range(j + 1)), arb(0))
        US = sum((U[i] * S[j - i] for i in range(j + 1)), arb(0))
        d = arb((2 * j + 2) * (2 * j + 3))
        S.append((sA * S3 - US) / d); U.append(-S2 / d)
    return S, U


def lin_series_start(s, sig0, u0, r0, e, M=14):
    """regular solution of Y'' = Q Y with Y(0) = 0, Y'(0) = e (e a 2-vector), enclosed at r0 (value and derivative)
    and over [0, r0] as Y/r. Odd power series sum_k y_k r^(2k+1) with Q_N built from the series coefficients;
    remainder: E'' = Q E + rho, E(0) = E'(0) = 0, |rho| <= (truncation polynomial) + |Q - Q_N| |P| on [0, r0];
    Volterra: |E| <= rho_max r^2 / (2 (1 - q r0^2 / 2)), |E'| <= r0 (q E_max + rho_max)."""
    N = 12
    S, U = bg_series(s, sig0, u0, N)
    _, crude, eps = bt.series_start(s, sig0, u0, r0)            # eps: sup |sigma - p_sigma|, |u - p_u| on [0, r0]
    S2c = [sum((S[i] * S[j - i] for i in range(j + 1)), arb(0)) for j in range(N + 1)]
    Qaa = [3 * arb(s) * S2c[j] - U[j] for j in range(N + 1)]
    QaW = [sq2() * S[j] for j in range(N + 1)]
    def Qmul(j, y):
        return [Qaa[j] * y[0] + QaW[j] * y[1], QaW[j] * y[0]]
    ys = [[arb(e[0]), arb(e[1])]]
    for k in range(M):
        acc = [arb(0), arb(0)]
        for j in range(min(k, N) + 1):
            t = Qmul(j, ys[k - j]); acc = [acc[0] + t[0], acc[1] + t[1]]
        d = arb((2 * k + 3) * (2 * k + 2))
        ys.append([acc[0] / d, acc[1] / d])
    r0 = arb(r0)
    # truncation residual: degrees 2m+1, m >= M (sum over j + k = m, j <= N, k <= M)
    rho_t = arb(0)
    for m in range(M, M + N + 1):
        acc = [arb(0), arb(0)]
        for j in range(N + 1):
            k = m - j
            if 0 <= k <= M:
                t = Qmul(j, ys[k]); acc = [acc[0] + t[0], acc[1] + t[1]]
        rho_t += (abs(acc[0]) + abs(acc[1])) * r0 ** (2 * m + 1)
    sg = abs(crude['sig']).upper(); sg = arb(sg)
    ua = arb(abs(crude['u']).upper())
    q = 3 * abs(arb(s)) * sg * sg + ua + sq2() * sg              # >= max row sum of |Q| on [0, r0]
    I0 = arb(0).union(r0)
    P0 = [sum((ys[k][i] * I0 ** (2 * k + 1) for k in range(M + 1)), arb(0)) for i in range(2)]
    Pmax = max(absup(P0[0]), absup(P0[1]))
    dQ = 3 * abs(arb(s)) * eps * (2 * sg + eps) + eps + sq2() * eps   # >= |Q - Q_N| (row sum) on [0, r0]
    # audit-W G-1: Qaa uses the truncated S2c; add the part of p_sigma^2 above degree 2N
    tr = arb(0)
    for m_ in range(N + 1, 2 * N + 1):
        tr += abs(sum((S[i] * S[m_ - i] for i in range(m_ - N, N + 1)), arb(0))) * r0 ** (2 * m_)
    dQ = dQ + 3 * abs(arb(s)) * tr
    rho = rho_t + dQ * Pmax
    den = 1 - q * r0 * r0 / 2
    assert den > arb('0.5')
    Emax = rho * r0 * r0 / (2 * den)
    Epmax = r0 * (q * Emax + rho)
    B = arb(0, 1)
    val = [sum((ys[k][i] * r0 ** (2 * k + 1) for k in range(M + 1)), arb(0)) + Emax * B for i in range(2)]
    der = [sum((ys[k][i] * (2 * k + 1) * r0 ** (2 * k) for k in range(M + 1)), arb(0)) + Epmax * B for i in range(2)]
    # Y/r on [0, r0]: P/r = sum y_k r^(2k) (interval) and |E|/r <= rho_max r0 / (2 den)
    over_r = [sum((ys[k][i] * I0 ** (2 * k) for k in range(M + 1)), arb(0)) + (rho * r0 / (2 * den)) * B for i in range(2)]
    return dict(val=val, der=der, over_r=over_r, Emax=Emax, Epmax=Epmax, q=q, sg=sg, ua=ua, ys=ys,
                Eover=up(rho * r0 / (2 * den)), eps_bg=eps, S=S, U=U)


# ------------------------------------------------------------------ exterior lemma EXT (DESIGN-W3 3.6b)
def ext_lemma(info, R1):
    """V1 on [R1, inf) normalised a(R1) = 1, a decaying, W -> 0. With E(s) = exp(-kappa1 (s - R1)),
    S = sqrt2 a1 / R1 (so sqrt2 |sigma(s)| <= S E(s)), kappa1^2 <= V := 3 sigma^2 - u <= Vmax := 3 (a1/R1)^2 + |E|:
      |a(s)| <= (1 + c_al) E(s),  |W(s)| <= c_w E(s)^2,
      a'(R1) in [-sqrt(Vmax) - S c_w/(4 kappa1), -kappa1 + S c_w/(4 kappa1)],  |W(R1)| <= c_w,  |W'(R1)| <= S (1 + c_al)/(2 kappa1),
    q = 3 S^2/(32 kappa1^4) < 1, c_al = q/(1 - q), c_w = S (1 + c_al)/(4 kappa1^2)."""
    k1 = info['kappa1']; a1 = info['a1']
    R1 = arb(R1)
    S = sq2() * a1 / R1
    Vmax = 3 * (a1 / R1) ** 2 + abs(info['E'])
    q = 3 * S * S / (32 * k1 ** 4)
    assert q < arb('0.5')
    cal = q / (1 - q)
    cw = S * (1 + cal) / (4 * k1 * k1)
    dap = S * cw / (4 * k1)
    ap_lo = -Vmax.sqrt() - dap
    ap_hi = -k1 + dap
    Wp = S * (1 + cal) / (2 * k1)
    return dict(k1=k1, a1=a1, S=up(S), Vmax=up(Vmax), cal=up(cal), cw=up(cw), ap_lo=arb(ap_lo.lower()),
                ap_hi=arb(ap_hi.upper()), W=up(cw), Wp=up(Wp))


# ------------------------------------------------------------------ marches with box records
class Rec:
    """records, for every tube step crossed, the enclosure of every column component over sub-boxes of the step."""

    def __init__(self, bj, nsub, ncomp):
        self.bj = bj; self.nsub = nsub; self.ncomp = ncomp
        self.box = {}            # step index -> list over sub-boxes of list of component enclosures
        self.pt = {}             # grid index -> column data at that grid point (from the certified march)

    def hook(self, K):
        def f(rc, h, C, R, X0, X1):
            ha = arb(h)
            i = self.bj.index_of(rc)
            if float(ha.mid()) < 0:
                i -= 1           # inward step from r_{i+1} down to r_i
            subs = []
            for m in range(self.nsub):
                if float(ha.mid()) > 0:
                    t1 = ha * m / self.nsub; t2 = ha * (m + 1) / self.nsub
                else:                                                   # inward: sub-box m counted from the low end
                    t1 = ha * (self.nsub - m) / self.nsub; t2 = ha * (self.nsub - m - 1) / self.nsub
                v = it.eval_sub(C[:self.ncomp], R[:self.ncomp], t1, t2, K, ha)
                subs.append(v)
            self.box[i] = subs
            if float(ha.mid()) > 0:
                self.pt.setdefault(i, X0); self.pt[i + 1] = X1
            else:
                self.pt.setdefault(i + 1, X0); self.pt[i] = X1
        return f


def wr(f, g):
    """Wronskian [f, g] = f.g' - f'.g for data (a, W, a', W')."""
    return f[0] * g[2] + f[1] * g[3] - f[2] * g[0] - f[3] * g[1]


class Node:
    """GREEN at one certified node. steps/info/Yend: the certified tube (bg_tube.get_tube)."""

    def __init__(self, steps, info, Yend, sig0, s=1, K=24, prec=200, r_x=8.0, nsub=1, log=print):
        t0 = time.time()
        it.set_prec(prec)
        self.steps, self.info, self.Yend, self.sig0, self.s, self.K = steps, info, Yend, sig0, s, K
        self.bj = bj = lc.BgJets(s, steps, Yend, K)
        self.sysd, self.terms, n = br.make_sys(s, 0, '+', arb(0), arb(0))
        assert n == 2
        self.r0 = steps[0]['r']; self.R1 = bj.r[-1]
        self.ix = bj.index_of(r_x); self.rx = bj.r[self.ix]
        self.nsub = nsub
        NB = len(steps)
        self.NB = NB
        # 1. regular columns U1, U2 (series start), outward r0 -> r_x -> R1
        self.ser1 = lin_series_start(s, sig0, info['u0'], self.r0, (1, 0))
        self.ser2 = lin_series_start(s, sig0, info['u0'], self.r0, (0, 1))
        c1 = self.ser1['val'] + self.ser1['der']; c2 = self.ser2['val'] + self.ser2['der']
        recU = Rec(bj, nsub, 8)
        Xa, _ = lc.march(self.sysd, bj, [c1, c2], bj.r[0], self.rx, K, terms=self.terms, on_step=recU.hook(K))
        self.U1x, self.U2x = Xa[0], Xa[1]
        Xb, _ = lc.march(self.sysd, bj, Xa, self.rx, self.R1, K, terms=self.terms, on_step=recU.hook(K))
        self.U2R1 = Xb[1]
        self.recU = recU
        log('  GREEN: U columns marched [%.1fs]' % (time.time() - t0))
        # 2. V1 candidates colA (with the W-box), colB; inward R1 -> r_x -> r0
        ex = ext_lemma(info, self.R1)
        self.ex = ex
        rho_m = arb(((-ex['ap_lo'] - ex['ap_hi']) / 2).mid())        # exact point (steering)
        B = arb(0, 1)
        colA = [arb(1), ex['W'] * B, -rho_m, ex['Wp'] * B]
        colB = [arb(0), arb(0), arb(1), arb(0)]
        self.delta = (ex['ap_lo'] + rho_m, ex['ap_hi'] + rho_m)      # a'(R1) = -rho_m + delta
        recV = Rec(bj, nsub, 8)
        Xc, _ = lc.march(self.sysd, bj, [colA, colB], self.R1, self.rx, K, terms=self.terms, on_step=recV.hook(K))
        self.Ax, self.Bx = Xc[0], Xc[1]
        Xd, _ = lc.march(self.sysd, bj, Xc, self.rx, bj.r[0], K, terms=self.terms, on_step=recV.hook(K))
        self.Ar0, self.Br0 = Xd[0], Xd[1]
        self.recV = recV
        log('  GREEN: V1 columns marched [%.1fs]' % (time.time() - t0))
        # 3. V1hat = (colA + delta colB) / (colA_a + delta colB_a)(r_x): hull over the two delta end points
        self.nu = hull(self.Ax[0] + self.delta[0] * self.Bx[0], self.Ax[0] + self.delta[1] * self.Bx[0])
        assert not self.nu.contains(0)
        self.V1x = self.v1hat(self.Ax, self.Bx)
        # 4. Wronskians, beta, alpha
        self.alpha = wr(self.U2x, self.V1x)
        assert not self.alpha.contains(0), 'alpha = [U2, V1] contains 0 (no certified G_a)'
        self.beta = -wr(self.U1x, self.V1x) / self.alpha
        # 5. Z1, Z2 at r_x: W-data fixed, (a, a') from [Z, V1hat] = 0 and [Z, U2] = 0
        V, U = self.V1x, self.U2x
        # [Z, V] = za V' - za' V + zW VW' - zW' VW = 0 ; same with U  ->  [[V2, -V0], [U2, -U0]] (za, za') = -(zW VW' - zW' VW, ...)
        Mz = [[V[2], -V[0]], [U[2], -U[0]]]
        dz = Mz[0][0] * Mz[1][1] - Mz[0][1] * Mz[1][0]
        assert not dz.contains(0)
        Zs = []
        for (zW, zWp) in ((arb(1), arb(0)), (arb(0), arb(1))):
            rhs = [-(zW * V[3] - zWp * V[1]), -(zW * U[3] - zWp * U[1])]
            za = (rhs[0] * Mz[1][1] - Mz[0][1] * rhs[1]) / dz
            zap = (Mz[0][0] * rhs[1] - rhs[0] * Mz[1][0]) / dz
            Zs.append([za, zW, zap, zWp])
        self.Z1x, self.Z2x = Zs
        self.c = wr(self.Z1x, self.Z2x)
        assert not self.c.contains(0), 'c = [Z1, Z2] contains 0'
        recZ = Rec(bj, nsub, 8)
        Xe, _ = lc.march(self.sysd, bj, Zs, self.rx, bj.r[0], K, terms=self.terms, on_step=recZ.hook(K))
        self.Zr0 = Xe
        Xf, _ = lc.march(self.sysd, bj, Zs, self.rx, self.R1, K, terms=self.terms, on_step=recZ.hook(K))
        self.ZR1 = Xf
        self.recZ = recZ
        log('  GREEN: Z columns marched [%.1fs]' % (time.time() - t0))
        # 6. tau = U1 + beta U2 = lam1 Z1 + lam2 Z2 ; consistency of the a-parts at r_x (assertion)
        tx = [self.U1x[k] + self.beta * self.U2x[k] for k in range(4)]
        self.lam = (tx[1], tx[3])
        chk_a = self.lam[0] * self.Z1x[0] + self.lam[1] * self.Z2x[0]
        chk_ap = self.lam[0] * self.Z1x[2] + self.lam[1] * self.Z2x[2]
        self.tau_check = dict(a_overlap=bool(chk_a.overlaps(tx[0])), ap_overlap=bool(chk_ap.overlaps(tx[2])),
                              a_U=tx[0].str(10, radius=True), a_Z=chk_a.str(10, radius=True))
        assert self.tau_check['a_overlap'] and self.tau_check['ap_overlap'], 'tau not in span(Z1, Z2): %s' % self.tau_check
        self.tau_x = tx
        self.tau_R1 = [self.lam[0] * Xf[0][k] + self.lam[1] * Xf[1][k] for k in range(4)]
        self.tau_r0 = [self.ser1['val'][0] + self.beta * self.ser2['val'][0], self.ser1['val'][1] + self.beta * self.ser2['val'][1],
                       self.ser1['der'][0] + self.beta * self.ser2['der'][0], self.ser1['der'][1] + self.beta * self.ser2['der'][1]]
        self._provenance = hashlib.sha256(('%s|%s|%s' % (info.get('tube_sha256'), self.beta.str(40, radius=True),
                                                          self.lam[0].str(40, radius=True))).encode()).hexdigest()
        self.seconds_cols = time.time() - t0
        self._boxes()
        self._inner_outer()
        self.kern = None

    def tau_grid(self):
        """tau data (a, W, a', W') at every grid point, built ONLY from the certified Z marches (tau = lam1 Z1 + lam2 Z2).
        Every consumer re-steps these data with the ODE and checks overlap (cell.py), so injected data are refused."""
        out = {}
        for i, X in self.recZ.pt.items():
            out[i] = [self.lam[0] * X[0][k] + self.lam[1] * X[1][k] for k in range(4)]
        return out

    def v1hat(self, A, Bc):
        """V1hat data from colA, colB data (any radius): hull over the delta end points of (A + d B)/(A_a + d B_a)(r_x)."""
        out = []
        for k in range(len(A)):
            v0 = (A[k] + self.delta[0] * Bc[k]) / (self.Ax[0] + self.delta[0] * self.Bx[0])
            v1 = (A[k] + self.delta[1] * Bc[k]) / (self.Ax[0] + self.delta[1] * self.Bx[0])
            out.append(hull(v0, v1))
        return out

    # -------------------------------------------------------------- box enclosures of every basis function
    def _boxes(self):
        """per sub-box b (increasing r): radius interval, and enclosures of U2, V1hat, Z1, Z2, tau (a, W, a', W')."""
        bx = []
        for i in range(self.NB):
            st = self.steps[i]
            for m in range(self.nsub):
                rI = (st['r'] + st['h'] * m / self.nsub).union(st['r'] + st['h'] * (m + 1) / self.nsub)
                Ub = self.recU.box[i][m]; Vb = self.recV.box[i][m]; Zb = self.recZ.box[i][m]
                U2 = Ub[4:8]
                V1 = self.v1hat(Vb[0:4], Vb[4:8])
                Z1 = Zb[0:4]; Z2 = Zb[4:8]
                tau = [self.lam[0] * Z1[k] + self.lam[1] * Z2[k] for k in range(4)]
                bx.append(dict(i=i, m=m, r=rI, h=st['h'] / self.nsub, U2=U2, V1=V1, Z1=Z1, Z2=Z2, tau=tau))
        self.boxes = bx

    def _inner_outer(self):
        """bounds on [0, r0] (Gronwall from r0 inward: |Y|+|Y'| <= (|Y(r0)|+|Y'(r0)|) e^{(1+q) r0}) and at R1."""
        q = self.ser1['q']
        fac = (arb(1) + q) * self.r0
        fac = fac.exp()
        def gron(v):
            m = sum((absup(x) for x in v), arb(0)) * fac
            return [arb(0, 1) * m for _ in range(4)]
        V1r0 = self.v1hat(self.Ar0, self.Br0)
        self.inner = dict(V1=gron(V1r0), Z1=gron(self.Zr0[0]), Z2=gron(self.Zr0[1]),
                          U2_over_r=self.ser2['over_r'], U2=[arb(0).union(self.r0) * self.ser2['over_r'][k] for k in range(2)])

    # -------------------------------------------------------------- kernel
    def kernel(self, prec=64):
        """|G| upper bounds for every (r-box, s-box) pair: 4 entries (aa, aW, Wa, WW) as arb upper values."""
        if self.kern is not None:
            return self.kern
        t0 = time.time()
        old = ctx.prec
        ctx.prec = prec
        bx = self.boxes; nb = len(bx)
        ia = 1 / self.alpha; ic = 1 / self.c
        Um = [[b['U2'][0], b['U2'][1]] for b in bx]
        Vm = [[b['V1'][0] * ia, b['V1'][1] * ia] for b in bx]
        Z1 = [[b['Z1'][0], b['Z1'][1]] for b in bx]
        Z2 = [[b['Z2'][0] * ic, b['Z2'][1] * ic] for b in bx]
        K = []
        for i in range(nb):
            row = []
            Ui = Um[i]; Vi = Vm[i]; Z1i = Z1[i]; Z2i = Z2[i]
            for j in range(nb):
                if j > i:
                    g = [Ui[p] * Vm[j][q] for p in (0, 1) for q in (0, 1)]
                else:
                    g = [Vi[p] * Um[j][q] - Z1i[p] * Z2[j][q] + Z2i[p] * Z1[j][q] for p in (0, 1) for q in (0, 1)]
                    if j == i:
                        g2 = [Ui[p] * Vm[j][q] for p in (0, 1) for q in (0, 1)]
                        g = [hull(x, y) for x, y in zip(g, g2)]
                row.append([up(abs(x)) for x in g])
            K.append(row)
        ctx.prec = old
        self.kern = K
        self.kernel_seconds = time.time() - t0
        return K

    # -------------------------------------------------------------- apply to a forcing profile
    def apply(self, prof, prec=64):
        """X-norm bound of y = G_a f for every f with |f1| <= P1, |f2| <= P2 (profile object, see Profile).
        Returns dict(X=bound, D_int, V_int, D_ext, V_ext, rows...)."""
        K = self.kernel(prec)
        old = ctx.prec
        ctx.prec = prec
        bx = self.boxes; nb = len(bx)
        S2 = sq2()
        Ia = []; IW = []
        for b in bx:
            p1, p2 = prof.box(b['r'])
            hb = absup(b['h'])
            Ia.append(up(hb * up(b['r'].upper()) * p1)); IW.append(up(hb * up(b['r'].upper()) * p2 / S2))
        # [0, r0] input: int_0^r0 s P ds <= r0^2/2 sup P
        p1i, p2i = prof.inner()
        r0 = self.r0
        Ia0 = up(r0 * r0 / 2 * p1i); IW0 = up(r0 * r0 / 2 * p2i / S2)
        # tail input s >= R1 (only s > r): |V1hat_a| <= (1+c_al) E / |nu|, |V1hat_W| <= c_w E^2 / |nu|
        ex = self.ex
        nu_lo = arb(abs(self.nu).lower())
        TA1, TA2 = prof.ext_tail(self)
        Ta = up((1 + ex['cal']) / nu_lo * TA1)
        TW = up(ex['cw'] / nu_lo * TA2 / S2)
        inner = self.inner
        ia = arb(1) / arb(abs(self.alpha).lower())
        icl = arb(1) / arb(abs(self.c).lower())
        dmax = arb(0); vmax = arb(0)
        rows = []
        for i in range(nb):
            Kr = K[i]
            sa = arb(0); sw = arb(0)
            for j in range(nb):
                g = Kr[j]
                sa += g[0] * Ia[j] + g[1] * IW[j]
                sw += g[2] * Ia[j] + g[3] * IW[j]
            # [0, r0] input (s < r): |V1hat(r)| |U2(s)| / |alpha| + (|Z1(r)||Z2(s)| + |Z2(r)||Z1(s)|) / |c|
            b = bx[i]
            Ua_in = absup(inner['U2'][0]); UW_in = absup(inner['U2'][1])
            z1a, z1w = absup(inner['Z1'][0]), absup(inner['Z1'][1]); z2a, z2w = absup(inner['Z2'][0]), absup(inner['Z2'][1])
            V1a, V1w = absup(b['V1'][0]), absup(b['V1'][1])
            Z1a, Z1w, Z2a, Z2w = [absup(b[k][c]) for k in ('Z1', 'Z2') for c in (0, 1)]
            ga = [V1a * Ua_in * ia + (Z1a * z2a + Z2a * z1a) * icl, V1a * UW_in * ia + (Z1a * z2w + Z2a * z1w) * icl]
            gw = [V1w * Ua_in * ia + (Z1w * z2a + Z2w * z1a) * icl, V1w * UW_in * ia + (Z1w * z2w + Z2w * z1w) * icl]
            sa += ga[0] * Ia0 + ga[1] * IW0
            sw += gw[0] * Ia0 + gw[1] * IW0
            # tail input s >= R1
            Ua, UW = absup(b['U2'][0]), absup(b['U2'][1])
            sa += Ua * ia * (Ta + TW)
            sw += UW * ia * (Ta + TW)
            rI = b['r']
            rlo = arb(rI.lower())
            wd = up(om(arb(rI.upper())) / rlo)
            wv = up(S2 / (rlo * SU))
            dd = up(wd * sa); vv = up(wv * sw)
            rows.append((dd, vv, up(sa), up(sw)))
            dmax = arb(dmax.union(dd).upper()); vmax = arb(vmax.union(vv).upper())
        # outputs on [0, r0]: y(r)/r for s > r uses U2(r)/r; the s < r parts are crude (s in [0, r] only)
        Uor = inner['U2_over_r']
        sa0 = arb(0); sw0 = arb(0)
        for j in range(nb):
            V = bx[j]['V1']
            va, vw = absup(V[0]), absup(V[1])
            sa0 += absup(Uor[0]) * ia * (va * Ia[j] + vw * IW[j])
            sw0 += absup(Uor[1]) * ia * (va * Ia[j] + vw * IW[j])
        sa0 += absup(Uor[0]) * ia * (Ta + TW); sw0 += absup(Uor[1]) * ia * (Ta + TW)
        # s in [0, r] (r <= r0): |G(r,s)|/r <= |V1hat(r)||U2(s)/s| / |alpha| + 2 |Z|^2 / (|c| r) and int_0^r s P <= r^2 P/2
        crude = 2 * (sum((absup(x) for x in inner['V1'][:2]), arb(0)) * (absup(Uor[0]) + absup(Uor[1])) * ia * r0 * r0 / 2
                 + 2 * sum((absup(x) for x in inner['Z1'][:2]), arb(0)) * sum((absup(x) for x in inner['Z2'][:2]), arb(0)) * icl * r0 / 2)
        sa0 += crude * (p1i + p2i); sw0 += crude * (p1i + p2i)
        d_in = up(om(r0) * sa0); v_in = up(S2 / SU * sw0)
        dmax = arb(dmax.union(d_in).upper()); vmax = arb(vmax.union(v_in).upper())
        # exterior r >= R1 (max principle + Gauss)
        last = rows[-1]
        R1 = self.R1
        dR1 = up(last[2] / arb(R1.lower()))                 # |d(R1)| <= |a|/R1 over the last box
        vR1 = up(S2 * last[3] / arb(R1.lower()))
        # |v'(R1)| <= R1^-2 int_0^R1 s^2 (P2 + 2 |sigma| |d|) ds  (Gauss); |d| on box <= rows[i][0]/om
        g = arb(0)
        for i, b in enumerate(bx):
            st = self.steps[b['i']]
            sig = absup(st['B'][0])
            p1, p2 = prof.box(b['r'])
            ru = up(b['r'].upper())
            g += absup(b['h']) * ru * ru * (p2 + 2 * sig * rows[i][0] / om(arb(b['r'].lower())))
        g += r0 ** 3 / 3 * (p2i + 2 * (abs(it.exact(self.sig0)) + arb('0.01')) * d_in)
        vpR1 = up(g / (arb(R1.lower()) ** 2))
        k1 = ex['k1']; a1 = ex['a1']
        oR1 = om(R1)
        sig_om = up(a1 * oR1 / arb(R1.lower()))              # sup_{r >= R1} om |sigma|  (decreasing, see DESIGN-W3)
        ext = prof.ext(self)                                 # sup om P1, int s P2 on [R1, inf)
        # Vext <= |v(R1)| + R1 |v'(R1)| + int_R1^inf s P2 + 2 a1 Dext int_R1^inf E/om   ;  int E/om <= 1/(kappa1 om(R1))
        A2 = up(vR1 + R1 * vpR1 + ext['int_sP2']); B2 = up(2 * a1 / (k1 * oR1))
        den = k1 * k1 - arb(1) / 8
        assert den > 0
        A1 = up(ext['sup_omP1'] / den); B1 = up(sig_om / den)
        D0 = up(om(R1) * dR1)
        # Dext <= max(D0, A1 + B1 Vext), Vext <= A2 + B2 Dext
        dd = 1 - B1 * B2
        assert dd > 0
        Dext = up(D0.union((A1 + B1 * A2) / dd))
        Vext = up(A2 + B2 * Dext)
        ctx.prec = old
        X = up(dmax.union(vmax).union(Dext).union(Vext / SU))
        return dict(X=X, D_int=dmax, V_int=vmax, D_ext=Dext, V_ext_over_su=up(Vext / SU), d_r0=d_in, v_r0=v_in,
                    rows=rows)


# ------------------------------------------------------------------ profiles
class Profile:
    """pointwise upper bounds P1 >= |f1|, P2 >= |f2|; interface: box(rI) -> (P1, P2) sup over the r-interval,
    inner() on [0, r0], ext_tail(node) -> (int_R1^inf E s P1, int_R1^inf E^2 s P2), ext(node) -> dict(sup_omP1, int_sP2)."""


class FFUnit(Profile):
    """the unit ball of FF: P1 = 1/om, P2 = 1/om^2 (gives ||G_a||_{FF -> X})."""

    def box(self, rI):
        o = om(arb(rI.lower()))
        return up(1 / o), up(1 / (o * o))

    def inner(self):
        return arb(1), arb(1)

    def ext_tail(self, node):
        R1 = node.R1; k1 = node.ex['k1']; o = om(R1)
        return up(R1 / o / k1), up(R1 / (o * o) / (2 * k1))          # s/om, s/om^2 decreasing for s >= 4

    def ext(self, node):
        return dict(sup_omP1=arb(1), int_sP2=up(8 / om(node.R1)))


class TableProfile(Profile):
    """profile given per box of the node's grid (list aligned with node.boxes), plus inner and exterior data."""

    def __init__(self, node, p1, p2, inner, ext_tail, ext):
        self.map = {}
        for b, a, c in zip(node.boxes, p1, p2):
            self.map[(b['r'].mid().str(30), b['r'].rad().str(5))] = (up(a), up(c))
        self._inner = inner; self._tail = ext_tail; self._ext = ext

    def box(self, rI):
        return self.map[(rI.mid().str(30), rI.rad().str(5))]

    def inner(self):
        return self._inner

    def ext_tail(self, node):
        return self._tail

    def ext(self, node):
        return self._ext
