"""cell.py - build-W instrument (R3-WINDOW, DESIGN-W3 sections 3.5-3.7): one cell [a, b] end to end.

  BR   branch lemma on each half (theta in [0, 1/2] linearised at node a, [1/2, 1] at node b by the a<->b, Delta -> -Delta
       symmetry of the Hermite predictor): Y0 from the EXACT quotient R_theta = theta^2 (1 - theta)^2 Q_theta (symbolic,
       DESIGN-W3 3.6), Z1, Z2 kernel sums (green.Node.apply), one fixed ball rho_max per half, uniqueness radius r_u
       with contraction kappa(r_u) = Z1max + r_u Z2hat(r_u) < 1, certified tube X-diameter < r_u (BR item 4), E < 0,
       |E| > w2, one node (u < 0 and sigma != 0 at r_n).
  CH   eta2(theta) <= C0 + C1 theta (1 - theta), eta2'(theta) <= C0' + C1' theta (1 - theta) per L, and Gam(theta).
  CC   per sector and end: CPOS H(w2) (k = 3, 2, 1), RITZ H(w1) (k + 1), CPOS H(0) (k = U+ + U- = 4, 3, 2), count H(0) L = 3
       (k = 0), PEN (L = 0); margins at both ends on COMMON explicit vectors; decided by exact quadratic tests in theta.
  IDXC conclusion per sector: N(w1) >= k + 1 and N(w2) <= k uniformly => one drop; with K(L) <= 2 => N_+ = 0.

Node b's functions on node a's grid (cross-grid) are produced ONLY by rigorous re-steps (it.bg_step, it.lin_step) from
node b's certified grid data; tau data are re-stepped over every b-step used and must overlap the next certified grid
value (an injected tau is refused). Taylor models (TM) carry every cancellation exactly in coefficient space.
Floats: only the deterministic pre-pass (steer.py) choosing w1, w2, explicit vectors, trial functions, levels m.
"""
import sys, os, json, time, math, hashlib
from fractions import Fraction
import numpy as np
from flint import arb, arb_poly, ctx
import itaylor as it
import lincore as lc
import bracket as br
import bg_tube as bt
import green as gr
import hw3
import steer

SU = arb(gr.SU)
OM = gr.om
up = gr.up
absup = gr.absup


class Reject(Exception):
    pass


# ------------------------------------------------------------------ Taylor models on one step [0, h], h > 0
class TM:
    __slots__ = ('p', 'rem', 'h', 'K')

    def __init__(self, coeffs, rem, h, K):
        self.p = coeffs if isinstance(coeffs, arb_poly) else arb_poly(list(coeffs[:K + 1]))
        self.rem = arb(rem); self.h = h; self.K = K

    @property
    def T(self):
        return it.tball(self.h)

    def _new(self, p, rem):
        return TM(p, rem, self.h, self.K)

    def __add__(self, o):
        if isinstance(o, TM):
            return self._new(self.p + o.p, self.rem + o.rem)
        return self._new(self.p + arb_poly([arb(o)]), self.rem)
    __radd__ = __add__

    def __neg__(self):
        return self._new(-self.p, -self.rem)

    def __sub__(self, o):
        return self + (-o)

    def __rsub__(self, o):
        return (-self) + o

    def __mul__(self, o):
        if not isinstance(o, TM):
            return self._new(self.p * arb(o), self.rem * arb(o))
        K = self.K; T = self.T
        P = self.p * o.p
        lo = P.truncate(K + 1)
        hi = P.right_shift(K + 1)
        rem = hi(T) + self.rem * o.p(T) + o.rem * self.p(T) + T ** (K + 1) * self.rem * o.rem
        return self._new(lo, rem)
    __rmul__ = __mul__

    def ev(self, t1=None, t2=None):
        T = self.T if t1 is None else arb(t1).union(arb(t2))
        return self.p(T) + T ** (self.K + 1) * self.rem


def tm_inv_r(rc, h, K):
    """1/r about rc: coefficients (-1)^k / rc^(k+1); remainder: the (K+1)-coefficient over the box."""
    ic = 1 / rc
    c = [ic]
    for k in range(K):
        c.append(-c[-1] * ic)
    rI = rc + it.tball(h)
    iI = 1 / rI                       # python-flint x ** n of an interval can contain 0: use repeated products
    rem = arb(1)
    for k in range(K + 2):
        rem = rem * iI
    rem = rem * (-1) ** (K + 1)
    return TM(c, rem, h, K)


# ------------------------------------------------------------------ node bundle
class NodeData:
    """certified tube + GREEN at one node (sig0 exact rational string)."""

    def __init__(self, sig0_str, steps, info, Yend, K=24, nsub=1, log=print):
        self.sig0_str = sig0_str
        self.sig0 = float(Fraction(sig0_str))
        assert Fraction(repr(self.sig0)) == Fraction(sig0_str), 'float label must read back as the exact rational'
        self.steps, self.info, self.Yend = steps, info, Yend
        self.K = K
        t0 = time.time()
        self.g = gr.Node(steps, info, Yend, self.sig0, K=K, nsub=nsub, log=log)
        self.bj = self.g.bj
        self.green_seconds = time.time() - t0
        self.sysd, self.terms = self.g.sysd, self.g.terms
        self.taug = self.g.tau_grid()
        ex = self.g.ex
        # exterior data (DESIGN-W3 3.6b, EXT): mu = kappa1/2, exp-small and c0 + c1/r forms
        k1 = ex['k1']; R1 = self.g.R1; a1 = ex['a1']
        self.k1 = k1; self.a1 = a1; self.R1 = R1
        self.E = info['E']; self.m = info['m']
        tR = self.g.tau_R1
        mu = k1 / 2
        Ab = absup(tR[0]) + 1
        S = ex['S']
        W0p = absup(tR[1]) + S * Ab / (k1 * k1)
        W1 = absup(tR[3]) + S * Ab / k1                               # audit-W C-1: linear growth of the W correction
        Cf = S / (2 * k1) * (W0p + W1 / (arb(1).exp() * (k1 - mu))) * (1 / (k1 - mu) + 1 / (k1 + mu))
        assert Cf < 1
        self.tau_a_ext = up(absup(tR[0]) + Cf)                         # |tau_a(r)| <= this * E_mu(r), r >= R1
        S2 = gr.sq2()
        self.tau_v_c0 = -S2 * tR[3]                                    # v_tau = c0 + c1/r +- eps_v on [R1, inf)
        self.tau_v_c1 = -S2 * (tR[1] - R1 * tR[3])
        self.tau_v_eps = up(S2 * S * Ab / k1)
        self.u_eps = up(a1 * a1 / (4 * k1 * k1 * R1 * R1))           # u = E + m/r +- u_eps on [R1, inf)
        self.sig_ext = up(a1 / R1)                                     # |sigma| <= sig_ext * E_mu
        self.mu = mu


# ------------------------------------------------------------------ cross-grid Taylor models (one half)
def _bg_tm(J0, JB, idx, h, K):
    return TM(J0[idx][:K + 1], JB[idx][K + 1], h, K)


def half_tms(A, B, other=None, inject=None):
    """For every step i of node A's grid: TMs of sa, ua, sb, ub, ta1, ta2, tb1, tb2 (tau in d, v variables).
    other: optional NodeData C (leave-one-out): also sc, uc. inject: test hook (control) that perturbs B's tau data."""
    K = A.K
    S2 = gr.sq2()
    taugB = dict(B.taug)
    if inject is not None:
        taugB = inject(B, taugB)
    out = []
    checked = set()
    _t0 = time.time()
    for i in range(len(A.steps)):
        st = A.steps[i]; rc = st['r']; h = st['h']
        rI = rc + it.tball(h)
        jp = A.bj.pt(i); jb = A.bj.box(i)
        sa = TM(jp['sig'][:K + 1], jb['sig'][K + 1], h, K); ua = TM(jp['u'][:K + 1], jb['u'][K + 1], h, K)
        # tau_A over its own step (re-step + overlap check with the next certified grid value)
        X1, C, R, _ = it.lin_step(A.sysd, lc.scaled(jp, A.terms), lc.scaled(jb, A.terms), [A.taug[i]], h, K)
        if not all(X1[0][k].overlaps(A.taug[i + 1][k]) for k in range(4)):
            raise Reject('tau_A data at grid %d do not match the certified re-step' % (i + 1))
        ta_a = TM(C[0], R[0], h, K); ta_W = TM(C[1], R[1], h, K)
        res = dict(i=i, r=rc, h=h, sa=sa, ua=ua)
        for tag, N, taug in (('b', B, taugB), ('c', other, None)):
            if N is None:
                continue
            j = N.bj.index_of(rc)
            if bool(N.bj.r[j] > rc):          # certainly above: take the grid point below (equal balls stay)
                j -= 1
            assert j >= 0
            rj = N.bj.r[j]
            Yj = N.steps[j]['Y'] if j < len(N.steps) else N.Yend
            hj = rc - rj
            if hj.contains(0) and bool(abs(hj) < arb('1e-40')):
                Yi = Yj
            else:
                Yi, _, _ = it.bg_step(1, rj, Yj, hj, K)
            Y1, Bx, J0 = it.bg_step(1, rc, Yi, h, K)
            J0 = it.bg_jets(1, rc, Yi, K + 1)
            JB = it.bg_jets(1, rI, Bx, K + 1)
            res['s' + tag] = _bg_tm(J0, JB, 0, h, K); res['u' + tag] = _bg_tm(J0, JB, 2, h, K)
            if tag == 'b':
                jpB = lc.scaled(N.bj._derive(rc, J0, K + 1), N.terms)
                jbB = lc.scaled(N.bj._derive(rI, JB, K + 1), N.terms)
                # re-step tau_B from its grid point j; check the full b-step against the next certified value
                if j not in checked:
                    Xf, _, _, _ = it.lin_step(N.sysd, lc.scaled(N.bj.pt(j), N.terms), lc.scaled(N.bj.box(j), N.terms),
                                              [taug[j]], N.steps[j]['h'], K)
                    if not all(Xf[0][k].overlaps(taug[j + 1][k]) for k in range(4)):
                        raise Reject('tau_B data at grid %d do not match the certified re-step (injected or corrupt)' % (j + 1))
                    checked.add(j)
                if hj.contains(0) and bool(abs(hj) < arb('1e-40')):
                    tBi = taug[j]
                else:
                    Xr, _, _, _ = it.lin_step(N.sysd, lc.scaled(N.bj.pt(j), N.terms), lc.scaled(N.bj.box(j), N.terms),
                                              [taug[j]], hj, K)
                    tBi = Xr[0]
                Xb, Cb, Rb, _ = it.lin_step(N.sysd, jpB, jbB, [tBi], h, K)
                tb_a = TM(Cb[0], Rb[0], h, K); tb_W = TM(Cb[1], Rb[1], h, K)
        ir = tm_inv_r(rc, h, K)
        res['ta1'] = ta_a * ir; res['ta2'] = ta_W * ir * (-S2)
        if B is not None:
            res['tb1'] = tb_a * ir; res['tb2'] = tb_W * ir * (-S2)
        out.append(res)
        if i % 50 == 0:
            print("    half_tms step %d/%d [%.0fs]" % (i, len(A.steps), time.time() - _t0), flush=True)
    return out


# ------------------------------------------------------------------ the exact residual quotient (sympy, DESIGN-W3 3.6)
def Q_coeffs(sa, ds, du, ta1, ta2, tb1, tb2, D):
    """Q1[0..5], Q2[0..2] with R_theta = theta^2 (1 - theta)^2 (sum Q1[k] theta^k, sum Q2[k] theta^k); D = Delta (arb).
    Generated from the symbolic division (remainder 0; referee-W2 w2_factor.log), expanded verbatim."""
    D2 = D * D; D3 = D2 * D
    x = ta1 * D + tb1 * D - ds * 2          # (Delta ta1 + Delta tb1 - 2 ds)
    Q1 = [None] * 6
    Q1[0] = (ta1 * ta1 * sa) * (3 * D2) - (ta1 * ta2) * D2 + (ds * ds * tb1) * (3 * D) + (ds * sa * tb1) * (6 * D) \
        - (ds * tb2) * D - (du * tb1) * D - ds * ds * ds * 3 - (ds * ds * sa) * 9 + (ds * du) * 3
    Q1[1] = (ta1 * ta1 * ta1) * D3 - (sa * ta1 * ta1) * (6 * D2) - (sa * ta1 * tb1) * (6 * D2) + (ta1 * ta2) * (2 * D2) \
        + (ta1 * tb2) * D2 + (ta2 * tb1) * D2 + (ds * ds * tb1) * (3 * D) + (ds * sa * ta1) * (18 * D) \
        + (ds * sa * tb1) * (6 * D) - (ds * ta2) * (3 * D) - (ds * tb2) * D - (du * ta1) * (3 * D) - (du * tb1) * D \
        - ds * ds * ds * 4 - (ds * ds * sa) * 12 + (ds * du) * 4
    Q1[2] = -(ta1 * ta1 * ta1) * (4 * D3) - (ta1 * ta1 * tb1) * (3 * D3) + (ds * ta1 * ta1) * (9 * D2) \
        + (sa * ta1 * ta1) * (3 * D2) + (sa * ta1 * tb1) * (6 * D2) + (sa * tb1 * tb1) * (3 * D2) - (ta1 * ta2) * D2 \
        - (ta1 * tb2) * D2 - (ta2 * tb1) * D2 - (tb1 * tb2) * D2 + (ds * ds * tb1) * (3 * D) - (ds * sa * ta1) * (12 * D) \
        - (ds * sa * tb1) * (12 * D) + (ds * ta2) * (2 * D) + (ds * tb2) * (2 * D) + (du * ta1) * (2 * D) \
        + (du * tb1) * (2 * D) - ds * ds * ds * 5 + (ds * ds * sa) * 12 - (ds * du) * 4
    Q1[3] = x * ((ta1 * ta1) * (2 * D2) + (ta1 * tb1) * D2 - (ds * ta1) * (4 * D) + ds * ds) * 3
    Q1[4] = -(x * x) * (ta1 * (4 * D) + tb1 * D - ds * 5)
    Q1[5] = x * x * x
    Q2 = [-(ta1 * ta1) * D2 - (ds * tb1) * (2 * D) + ds * ds * 3,
          (ta1 * D - ds) * x * 2,
          -(x * x)]
    return Q1, Q2


def _sym_check():
    """the generated Q formulas against the symbolic definition of R_theta at random numbers (assertion, float)."""
    rng = np.random.default_rng(7)
    for _ in range(5):
        v = rng.normal(size=8); sa, ds, du, ta1, ta2, tb1, tb2, D = v
        t = rng.uniform()
        h01 = -2 * t ** 3 + 3 * t ** 2; h10 = t ** 3 - 2 * t ** 2 + t; h11 = t ** 3 - t ** 2
        Na = lambda d, w: (3 * sa * d * d + d ** 3 - w * d, -d * d)
        d1 = h01 * ds + D * (h10 * ta1 + h11 * tb1); d2 = h01 * du + D * (h10 * ta2 + h11 * tb2)
        sb = sa + ds; ub = 0.3 + du
        n1, n2 = Na(ds, du); m1, m2 = Na(d1, d2)
        lb1 = (3 * sb * sb - ub - 3 * sa * sa + 0.3) * tb1 - ds * tb2; lb2 = -2 * ds * tb1
        R1 = -h01 * n1 - D * h11 * lb1 + m1; R2 = -h01 * n2 - D * h11 * lb2 + m2
        Q1, Q2 = Q_coeffs(sa, ds, du, ta1, ta2, tb1, tb2, D)
        w = t * t * (1 - t) ** 2
        assert abs(R1 - w * sum(Q1[k] * t ** k for k in range(6))) < 1e-9 * (1 + abs(R1))
        assert abs(R2 - w * sum(Q2[k] * t ** k for k in range(3))) < 1e-9 * (1 + abs(R2))
    return True


# ------------------------------------------------------------------ exterior profile objects for green.apply
class ExtProfile(gr.TableProfile):
    """interior per-box table + exterior form P1 <= al1 E_mu + be1/om, P2 <= al2 E_mu + be2/om^2 on [R1, inf)."""

    def __init__(self, node, p1, p2, inner, al1, be1, al2, be2, mu):
        R1 = node.R1; k = node.ex['k1']; o = OM(R1)
        assert mu >= arb('0.5'), 'om^2 E_mu must be decreasing (mu >= 1/2)'
        tail = (up(al1 * (R1 / (k + mu) + 1 / (k + mu) ** 2) + be1 * R1 / o / k),
                up(al2 * (R1 / (2 * k + mu) + 1 / (2 * k + mu) ** 2) + be2 * R1 / (o * o) / (2 * k)))
        ext = dict(sup_omP1=up(al1 * o + be1), int_sP2=up(al2 * (R1 / mu + 1 / mu ** 2) + be2 * 8 / o))
        gr.TableProfile.__init__(self, node, p1, p2, inner, tail, ext)


# ------------------------------------------------------------------ BR on one half
HALF_THETAS = 8


def br_half(A, B, D, tms, log=print):
    """BR on theta in [0, 1/2] linearised at A (D = sigma_B - sigma_A, signed exact arb)."""
    t0 = time.time()
    g = A.g
    S2 = gr.sq2()
    nsub = g.nsub
    # per box: Y0 profile (sum |Q_k| 2^-k / 16), D-envelopes for Z1/Z2, CH envelopes
    p1y = []; p2y = []; p1z = []; p2z = []; d1max = []; ch = []
    thetas = [(arb(k) / (2 * HALF_THETAS), arb(k + 1) / (2 * HALF_THETAS)) for k in range(HALF_THETAS)]
    def herm(tI):
        T = tI[0].union(tI[1])
        return (-2 * T ** 3 + 3 * T ** 2, T ** 3 - 2 * T ** 2 + T, T ** 3 - T ** 2)
    hs = [herm(tI) for tI in thetas]
    for X in tms:
        if X["i"] % 50 == 0:
            print("    br_half step %d [%.0fs]" % (X["i"], time.time() - t0), flush=True)
        sa, ua, sb, ub = X['sa'], X['ua'], X['sb'], X['ub']
        ta1, ta2, tb1, tb2 = X['ta1'], X['ta2'], X['tb1'], X['tb2']
        ds = sb - sa; du = ub - ua
        Q1, Q2 = Q_coeffs(sa, ds, du, ta1, ta2, tb1, tb2, D)
        h = X['h']
        for m in range(nsub):
            t1 = h * m / nsub; t2 = h * (m + 1) / nsub
            a = sum((absup(Q1[k].ev(t1, t2)) * arb(2) ** (-k) for k in range(6)), arb(0)) / 16
            c = sum((absup(Q2[k].ev(t1, t2)) * arb(2) ** (-k) for k in range(3)), arb(0)) / 16
            p1y.append(up(a)); p2y.append(up(c))
            rI = X['r'] + t1.union(t2)
            o = OM(arb(rI.lower()))
            sav = sa.ev(t1, t2); dsv = ds.ev(t1, t2); duv = du.ev(t1, t2)
            ta1v, ta2v, tb1v, tb2v = ta1.ev(t1, t2), ta2.ev(t1, t2), tb1.ev(t1, t2), tb2.ev(t1, t2)
            best1 = arb(0); best2 = arb(0); dm = arb(0)
            for (h01, h10, h11) in hs:
                D1 = (h01 * ds + (h10 * ta1 + h11 * tb1) * D).ev(t1, t2)
                D2 = (h01 * du + (h10 * ta2 + h11 * tb2) * D).ev(t1, t2)
                P1 = abs(6 * sav * D1 + 3 * D1 * D1 - D2) / o + SU * abs(D1)
                P2 = 2 * abs(D1) / o
                best1 = up(best1.union(P1)); best2 = up(best2.union(P2)); dm = up(dm.union(abs(D1)))
            p1z.append(best1); p2z.append(best2); d1max.append(dm)
            # CH: p_sig = max(|-ds + D ta1|, |ds - D tb1|), p_u likewise; ds itself; sigma envelopes
            ps = up(abs((ds - ta1 * D).ev(t1, t2)).union(abs((ds - tb1 * D).ev(t1, t2))))
            pu = up(abs((du - ta2 * D).ev(t1, t2)).union(abs((du - tb2 * D).ev(t1, t2))))
            ch.append(dict(r=rI, h=h / nsub, ps=ps, pu=pu, ds=absup(dsv), sl=up(abs(sav).union(abs(sb.ev(t1, t2)))),
                           sa=sav, sb=sb.ev(t1, t2), ua=ua.ev(t1, t2), ub=ub.ev(t1, t2)))
    log('    BR half: TM profiles [%.1fs]' % (time.time() - t0))
    # exterior constants (r >= R1)
    mu = arb(min(A.mu, B.mu).lower())
    sA, sB = A.sig_ext, B.sig_ext
    tA1, tB1 = up(A.tau_a_ext / A.R1), up(B.tau_a_ext / B.R1)       # |tau_1| <= . E_mu
    aD = absup(D)
    dsx = up(sA + sB)
    # bounded quantities on [R1, inf): |u_B - u_A| <= |dE| + |dm|/R1 + 2 eps ; |tau_2| <= |c0| + |c1|/R1 + eps
    dux = up(abs(B.E - A.E) + abs(B.m - A.m) / A.R1 + A.u_eps + B.u_eps)
    tA2 = up(abs(A.tau_v_c0) + abs(A.tau_v_c1) / A.R1 + A.tau_v_eps)
    tB2 = up(abs(B.tau_v_c0) + abs(B.tau_v_c1) / B.R1 + B.tau_v_eps)
    # Y0 exterior: every term of Q has >= 1 exp-small factor in {sa, ds, ta1, tb1}; bound each |Q_k| by the same
    # expression with all symbols replaced by their bounds and E_mu factored once (E_mu <= 1)
    cY1 = up(sum((absup(_absQ1(k, sA, dsx, dux, tA1, tA2, tB1, tB2, aD)) * arb(2) ** (-k) for k in range(6)), arb(0)) / 16)
    cY2 = up(sum((absup(_absQ2(k, dsx, tA1, tB1, aD)) * arb(2) ** (-k) for k in range(3)), arb(0)) / 16)
    # inner [0, r0]: Taylor models from the exact series (no cancellation lost)
    ia_, ib_ = inner_tms(A), inner_tms(B)
    ids = ib_['sig'] - ia_['sig']; idu = ib_['u'] - ia_['u']
    iQ1, iQ2 = Q_coeffs(ia_['sig'], ids, idu, ia_['t1'], ia_['t2'], ib_['t1'], ib_['t2'], D)
    iY1 = up(sum((absup(iQ1[k].ev()) * arb(2) ** (-k) for k in range(6)), arb(0)) / 16)
    iY2 = up(sum((absup(iQ2[k].ev()) * arb(2) ** (-k) for k in range(3)), arb(0)) / 16)
    iD1 = arb(0); iD2 = arb(0)
    for (h01, h10, h11) in hs:
        iD1 = up(iD1.union(abs((h01 * ids + (h10 * ia_['t1'] + h11 * ib_['t1']) * D).ev())))
        iD2 = up(iD2.union(abs((h01 * idu + (h10 * ia_['t2'] + h11 * ib_['t2']) * D).ev())))
    inn = dict(sa=absup(ia_['sig'].ev()))
    profY = ExtProfile(g, p1y, p2y, (iY1, iY2), cY1, arb(0), cY2, arb(0), mu)
    rY = g.apply(profY)
    Y0 = rY['X']
    # Z1: exterior D1 <= (dsx/2 + aD (4/27 tA1 + 1/8 tB1)) E_mu (|h01| <= 1/2, h10 <= 4/27, |h11| <= 1/8 on [0, 1/2]);
    #     |D2| <= dux/2 + aD (4/27 tA2 + tB2/8);  P1 om <= |6 sa D1 + 3 D1^2| om + |D2| + s_u om |D1|
    D1x = up(dsx / 2 + aD * (arb(4) / 27 * tA1 + tB1 / 8))
    D2x = up(dux / 2 + aD * (arb(4) / 27 * tA2 + tB2 / 8))
    al1 = up(6 * sA * D1x + 3 * D1x * D1x + SU * D1x)
    D1i = iD1; D2i = iD2
    profZ1 = ExtProfile(g, p1z, p2z, (up(6 * inn['sa'] * D1i + 3 * D1i ** 2 + D2i + SU * D1i), up(2 * D1i)),
                        al1, D2x, up(2 * D1x), arb(0), mu)
    rZ1 = g.apply(profZ1)
    Z1 = rZ1['X']
    def summ(r_):
        return {k: r_[k].str(4) for k in ('D_int', 'V_int', 'D_ext', 'V_ext_over_su', 'd_r0', 'v_r0')}
    diag = dict(Y0=summ(rY), Z1=summ(rZ1), p1y_max=max(p1y, key=lambda v: float(v.mid())).str(3),
                p1y_argmax=float(g.boxes[max(range(len(p1y)), key=lambda q: float(p1y[q].mid()))]['r'].mid()),
                p1z_max=max(p1z, key=lambda v: float(v.mid())).str(3),
                p1z_argmax=float(g.boxes[max(range(len(p1z)), key=lambda q: float(p1z[q].mid()))]['r'].mid()),
                ext=dict(cY1=cY1.str(3), cY2=cY2.str(3), al1=al1.str(3), D2x=D2x.str(3), iY1=iY1.str(3)))
    if not Z1 < 1:
        return dict(ok=False, why='Z1 >= 1 (%s)' % Z1.str(5), Y0=Y0.str(5), Z1=Z1.str(5), diag=diag, seconds=time.time() - t0)
    # Z2 profile at radius r: P1 = 6|sa + D1|/om^2 + 3 r/om^3 + 2 s_u/om, P2 = 2/om^2
    def z2(rr):
        p1 = []; p2 = []
        for b, dm in zip(g.boxes, d1max):
            o = OM(arb(b['r'].lower()))
            sab = absup(A.steps[b['i']]['B'][0])
            p1.append(up(6 * (sab + dm) / o ** 2 + 3 * rr / o ** 3 + 2 * SU / o)); p2.append(up(2 / o ** 2))
        sg = abs(it.exact(A.sig0)) + arb('0.01')
        prof = ExtProfile(g, p1, p2, (up(6 * (sg + D1i) + 3 * rr + 2 * SU), arb(2)),
                          up(6 * (sA + D1x)), up(3 * rr + 2 * SU), arb(0), arb(2), mu)
        return g.apply(prof)['X']
    # uniqueness radius r_u and fixed ball rho_max
    Z2a = z2(arb('0.01'))
    r_u = up((1 - Z1) / (2 * Z2a))
    r_u = arb(min(float(r_u.lower()), 0.01))
    r_u = arb(r_u.lower())
    Z2u = z2(r_u)
    kappa = Z1 + r_u * Z2u
    rho = up(2 * Y0 / (1 - Z1))
    selfmap = Y0 + Z1 * rho + Z2u * rho * rho <= rho
    ok = bool(kappa < 1 and selfmap and rho <= r_u)
    return dict(ok=ok, Y0=Y0, Z1=Z1, Z2=Z2u, r_u=r_u, diag=diag, kappa=kappa, rho=rho, selfmap=bool(selfmap), ch=ch,
                ext=dict(mu=mu, dsx=dsx, dux=dux, tA1=tA1, tB1=tB1, tA2=tA2, tB2=tB2),
                seconds=time.time() - t0, why=None if ok else 'BR closure failed')


def inner_tms(N, K=24):
    """Taylor models on [0, r0] (base 0, h = r0) of sigma, u, tau1, tau2 at node N from the exact series (bg series
    with the tube's u0 interval; U1 + beta U2 odd series): the series remainders and the truncated orders widen the
    constant coefficient (f(t) in p(t) + [-err, err])."""
    g = N.g
    r0 = N.steps[0]['r']
    S2 = gr.sq2(); B = arb(0, 1)
    def tm_even(coef, err):
        p = [arb(0)] * (K + 1); extra = arb(0)
        for j, c in enumerate(coef):
            if 2 * j <= K:
                p[2 * j] = c
            else:
                extra += abs(c) * r0 ** (2 * j)
        p[0] = p[0] + (err + extra) * B
        return TM(p, arb(0), r0, K)
    ser1, ser2, beta = g.ser1, g.ser2, g.beta
    eps = ser1['eps_bg']
    sig = tm_even(ser1['S'], eps); u = tm_even(ser1['U'], eps)
    c1 = [ser1['ys'][k][0] + beta * ser2['ys'][k][0] for k in range(len(ser1['ys']))]
    c2 = [-S2 * (ser1['ys'][k][1] + beta * ser2['ys'][k][1]) for k in range(len(ser1['ys']))]
    e1 = ser1['Eover'] + abs(beta) * ser2['Eover']
    t1 = tm_even(c1, e1); t2 = tm_even(c2, S2 * e1)
    return dict(sig=sig, u=u, t1=t1, t2=t2, r0=r0)


def inner_symbols(A, B):
    """|.| bounds on [0, r0] of sa, ds, du, tau components (series_start crude enclosures; tau = U1 + beta U2 via the
    series Y/r enclosures)."""
    r0 = A.steps[0]['r']
    _, ca, _ = bt.series_start(1, A.sig0, A.info['u0'], r0)
    _, cb, _ = bt.series_start(1, B.sig0, B.info['u0'], r0)
    S2 = gr.sq2()
    def tau(N):
        o1 = N.g.ser1['over_r']; o2 = N.g.ser2['over_r']
        return absup(o1[0] + N.g.beta * o2[0]), absup(S2 * (o1[1] + N.g.beta * o2[1]))
    t1a, t2a = tau(A); t1b, t2b = tau(B)
    return dict(sa=absup(ca['sig']), ds=absup(cb['sig'] - ca['sig']), du=absup(cb['u'] - ca['u']),
                ta1=t1a, ta2=t2a, tb1=t1b, tb2=t2b)


def _absQ1(k, sa, ds, du, ta1, ta2, tb1, tb2, D):
    """|Q1[k]| bound with nonnegative inputs: every monomial taken with |coefficient| (exterior use)."""
    D2 = D * D; D3 = D2 * D
    x = ta1 * D + tb1 * D + ds * 2
    if k == 0:
        return 3 * D2 * sa * ta1 ** 2 + D2 * ta1 * ta2 + 3 * D * ds ** 2 * tb1 + 6 * D * ds * sa * tb1 + D * ds * tb2 + D * du * tb1 + 3 * ds ** 3 + 9 * ds ** 2 * sa + 3 * ds * du
    if k == 1:
        return (D3 * ta1 ** 3 + 6 * D2 * sa * ta1 ** 2 + 6 * D2 * sa * ta1 * tb1 + 2 * D2 * ta1 * ta2 + D2 * ta1 * tb2 + D2 * ta2 * tb1
                + 3 * D * ds ** 2 * tb1 + 18 * D * ds * sa * ta1 + 6 * D * ds * sa * tb1 + 3 * D * ds * ta2 + D * ds * tb2 + 3 * D * du * ta1
                + D * du * tb1 + 4 * ds ** 3 + 12 * ds ** 2 * sa + 4 * ds * du)
    if k == 2:
        return (4 * D3 * ta1 ** 3 + 3 * D3 * ta1 ** 2 * tb1 + 9 * D2 * ds * ta1 ** 2 + 3 * D2 * sa * ta1 ** 2 + 6 * D2 * sa * ta1 * tb1
                + 3 * D2 * sa * tb1 ** 2 + D2 * ta1 * ta2 + D2 * ta1 * tb2 + D2 * ta2 * tb1 + D2 * tb1 * tb2 + 3 * D * ds ** 2 * tb1
                + 12 * D * ds * sa * ta1 + 12 * D * ds * sa * tb1 + 2 * D * ds * ta2 + 2 * D * ds * tb2 + 2 * D * du * ta1 + 2 * D * du * tb1
                + 5 * ds ** 3 + 12 * ds ** 2 * sa + 4 * ds * du)
    if k == 3:
        return 3 * x * (2 * D2 * ta1 ** 2 + D2 * ta1 * tb1 + 4 * D * ds * ta1 + ds ** 2)
    if k == 4:
        return x * x * (4 * D * ta1 + D * tb1 + 5 * ds)
    return x ** 3


def _absQ2(k, ds, ta1, tb1, D):
    x = ta1 * D + tb1 * D + ds * 2
    if k == 0:
        return D * D * ta1 ** 2 + 2 * D * ds * tb1 + 3 * ds ** 2
    if k == 1:
        return 2 * (ta1 * D + ds) * x
    return x * x


# ------------------------------------------------------------------ tube X-diameter (BR item 4)
def tube_diameter(N):
    """sup over the tube of the X-distance between any two solutions it contains (u0 in the tube interval):
    grid values and the within-step spread of the K = 56 Taylor coefficients (rad of the ball coefficients) + 2 |rem|
    h^57, the [0, r0] series spread, and the exterior (both decaying: |sigma| <= a1/r E; u = E + m/r +- eps)."""
    steps, info = N.steps, N.info
    old = ctx.prec
    it.set_prec(320)
    Kt = 56
    dmax = arb(0); vmax = arb(0)
    for st in steps:
        r = st['r']; h = st['h']
        J0 = it.bg_jets(1, r, st['Y'], Kt)
        JB = it.bg_jets(1, r + it.tball(h), st['B'], Kt + 1)
        for idx, w in ((0, 'd'), (2, 'v')):
            spread = sum((2 * arb(J0[idx][k].rad()) * abs(h) ** k for k in range(Kt + 1)), arb(0)) \
                + 2 * absup(JB[idx][Kt + 1]) * abs(h) ** (Kt + 1)
            if w == 'd':
                dmax = up(dmax.union(spread * OM(r + h)))
            else:
                vmax = up(vmax.union(spread / SU))
    # [0, r0]: the series polynomial with the u0 interval; sigma(0) = sigma0 exactly
    r0 = steps[0]['r']
    S, U = gr.bg_series(1, N.sig0, info['u0'])
    I0 = arb(0).union(r0)
    ps = sum((S[j] * I0 ** (2 * j) for j in range(len(S))), arb(0))
    pu = sum((U[j] * I0 ** (2 * j) for j in range(len(U))), arb(0))
    _, _, eps = bt.series_start(1, N.sig0, info['u0'], r0)
    dmax = up(dmax.union((2 * arb(ps.rad()) + 2 * eps) * OM(r0)))
    vmax = up(vmax.union((2 * arb(pu.rad()) + 2 * eps) / SU))
    # exterior
    R1 = N.R1
    dext = up(2 * N.a1 * OM(R1) / R1)
    vext = up((2 * arb(info['E'].rad()) + 2 * arb(info['m'].rad()) / R1 + 2 * N.u_eps) / SU)
    it.set_prec(old)
    return up(dmax.union(vmax).union(dext).union(vext))


# ------------------------------------------------------------------ CH constants for the whole cell
def ch_constants(A, B, chA, chB, rho, ext):
    """eta2(theta) <= C0 + C1 x, eta2'(theta) <= C0p + C1p x (x = theta (1 - theta)), per L; Gam(theta) <= G0 + G1 x.
    chA: per-box CH envelopes on A's grid (half 1); chB: on B's grid (half 2; same quantities, roles swapped).
    rho: max of the two halves' rho_max."""
    S8 = arb(8).sqrt(); N2o = 4 * arb.pi().sqrt()
    D = it.exact(Fraction(B.sig0_str) - Fraction(A.sig0_str))
    sup1 = arb(0); sup0 = arb(0); sup1p = arb(0); sup0p = arb(0)
    # audit-W C-3: the sup over r in [0, r0] from the exact-series Taylor models
    ia, ib = inner_tms(A), inner_tms(B)
    ids = ib['sig'] - ia['sig']; idu = ib['u'] - ia['u']
    ips = up(abs((ids - ia['t1'] * D).ev()).union(abs((ids - ib['t1'] * D).ev())))
    ipu = up(abs((idu - ia['t2'] * D).ev()).union(abs((idu - ib['t2'] * D).ev())))
    ids_ = absup(ids.ev())
    isl = up(abs(ia['sig'].ev()).union(abs(ib['sig'].ev())))
    sup1 = up(sup1.union(3 * ids_ ** 2 + 6 * isl * ips + ipu))
    sup1p = up(sup1p.union(6 * isl * ips + 3 * ips * (ips / 4 + rho) + ipu))
    sup0 = up(sup0.union(6 * isl + SU))
    sup0p = up(sup0p.union(6 * isl + SU + 3 * (ips / 4 + rho)))
    Ip = arb(0); I2p = arb(0); Ids = arb(0); I2ds = arb(0)
    for chl in (chA, chB):
        for c in chl:
            o = OM(arb(c['r'].lower()))
            sl = c['sl']
            sup1 = up(sup1.union(3 * c['ds'] ** 2 + 6 * sl * c['ps'] + c['pu']))
            sup1p = up(sup1p.union(6 * sl * c['ps'] + 3 * c['ps'] * (c['ps'] / 4 + rho / o) + c['pu']))
            sup0 = up(sup0.union(6 * sl / o + SU))
            sup0p = up(sup0p.union(6 * sl / o + SU + 3 * (c['ps'] / 4 + rho / o) / o))
    # radial integrals on A's grid only (each r covered once), plus exterior
    for c in chA:
        ru = up(c['r'].upper()); hh = absup(c['h'])
        Ip += hh * ru * c['ps'] ** 2; I2p += hh * ru * ru * c['ps'] ** 2
        Ids += hh * ru * c['ds'] ** 2; I2ds += hh * ru * ru * c['ds'] ** 2
    r0 = A.steps[0]['r']
    # [0, r0]: the inner Taylor-model bounds (audit-W C-3)
    Ip += r0 ** 2 / 2 * ips ** 2; I2p += r0 ** 3 / 3 * ips ** 2
    Ids += r0 ** 2 / 2 * ids_ ** 2; I2ds += r0 ** 3 / 3 * ids_ ** 2
    mu = ext['mu']; R1 = A.R1
    aD = absup(it.exact(Fraction(B.sig0_str) - Fraction(A.sig0_str)))
    cps = up(ext['dsx'] + aD * (ext['tA1'] + ext['tB1']))          # p_sig <= cps E_mu on [R1, inf)
    Ip += cps ** 2 * (R1 / (2 * mu) + 1 / (4 * mu ** 2)); I2p += cps ** 2 * (R1 ** 2 / (2 * mu) + R1 / (2 * mu ** 2) + 1 / (4 * mu ** 3))
    Ids += ext['dsx'] ** 2 * (R1 / (2 * mu) + 1 / (4 * mu ** 2)); I2ds += ext['dsx'] ** 2 * (R1 ** 2 / (2 * mu) + R1 / (2 * mu ** 2) + 1 / (4 * mu ** 3))
    # p_u on [R1, inf): |-(dE + dm/r) + D (c0 + c1/r)| (+ eps) <= max at r = R1 or r -> inf (monotone in 1/r)
    puext = arb(0)
    for (N, sgn) in ((A, 1), (B, -1)):
        C0 = -(B.E - A.E) + D * N.tau_v_c0; C1 = -(B.m - A.m) + D * N.tau_v_c1
        e = A.u_eps + B.u_eps + aD * N.tau_v_eps
        puext = up(puext.union(abs(C0 + C1 / R1) + e).union(abs(C0) + e))
    sup1 = up(sup1.union(puext + 3 * ext['dsx'] ** 2 + 6 * (A.sig_ext + B.sig_ext) * cps))
    sup1p = up(sup1p.union(puext + 6 * (A.sig_ext + B.sig_ext) * cps + 3 * cps ** 2))
    Np = up(Ip.sqrt()); N2p = up(I2p.sqrt())
    Imax = up(arb(A.info['I1'].union(B.info['I1']).upper()).sqrt())                 # audit-W C-2
    out = {}
    for L in range(4):
        den = arb(2 * L + 1)
        # n_e <= x Np + rho sqrt8 ; 2 n_e^2 <= 2 (Np/4 + rho sqrt8) n_e
        nl1 = (4 * Imax + 2 * (Np / 4 + rho * S8)) * Np / den
        nl0 = (4 * Imax + 2 * (Np / 4 + rho * S8)) * rho * S8 / den
        C1 = up(sup1 + nl1); C0 = up(rho * sup0 + nl0)
        C1p = up(sup1p + nl1 + 2 * Ids / den); C0p = up(rho * sup0p + nl0)
        out[L] = dict(C0=C0, C1=C1, C0p=C0p, C1p=C1p)
    # Gam(theta) = gam_e^2 + x ||g_b - g_a||^2, gam_e <= x N2p + rho N2o
    G1 = up((N2p / 4 + rho * N2o) * N2p + I2ds); G0 = up((N2p / 4 + rho * N2o) * rho * N2o)
    out['Gam'] = dict(G0=G0, G1=G1)
    out['aux'] = dict(Np=Np, N2p=N2p, Ids=up(Ids), I2ds=up(I2ds), puext=puext)
    return out


def quad_pos(ma, mb, C0, C1):
    """decide (1 - t) ma + t mb - C0 - C1 t (1 - t) > 0 for all t in [0, 1] (exact arb; 64 sub-intervals if needed)."""
    def f(T):
        return (1 - T) * ma + T * mb - C0 - C1 * T * (1 - T)
    if not (f(arb(0)) > 0 and f(arb(1)) > 0):
        return False
    for k in range(64):
        T = arb(k).union(arb(k + 1)) / 64
        c = (arb(k) + arb('0.5')) / 64
        # centred form: f(T) in f(c) + f'(T)(T - c), f'(t) = mb - ma - C1 (1 - 2t)
        val = f(c) + (mb - ma - C1 * (1 - 2 * T)) * (T - c)
        if not val > 0:
            return False
    return True


# ------------------------------------------------------------------ leave-one-out distance (control gate)
class TubeOnly:
    """a certified tube used only as a comparison object (leave-one-out): no GREEN."""

    def __init__(self, sig0_str, steps, info, Yend, K=24):
        self.sig0_str = sig0_str; self.sig0 = float(Fraction(sig0_str))
        self.steps, self.info, self.Yend, self.K = steps, info, Yend, K
        self.bj = lc.BgJets(1, steps, Yend, K)
        k1 = info['kappa1']; a1 = info['a1']; R1 = self.bj.r[-1]
        self.R1 = R1; self.sig_ext = up(a1 / R1); self.E = info['E']; self.m = info['m']
        self.u_eps = up(a1 * a1 / (4 * k1 * k1 * R1 * R1)); self.mu = k1 / 2


def loo_distance(A, B, C, tms, D, theta, ext):
    """X-distance bound between the certified tube of C (sigma0_C = sigma_A + theta D) and the predictor H_theta."""
    th = it.exact(theta)
    h01 = -2 * th ** 3 + 3 * th ** 2; h10 = th ** 3 - 2 * th ** 2 + th; h11 = th ** 3 - th ** 2
    dmax = arb(0); vmax = arb(0)
    for X in tms:
        sa, ua, sb, ub, sc, uc = X['sa'], X['ua'], X['sb'], X['ub'], X['sc'], X['uc']
        e1 = sc - sa - h01 * (sb - sa) - (X['ta1'] * h10 + X['tb1'] * h11) * D
        e2 = uc - ua - h01 * (ub - ua) - (X['ta2'] * h10 + X['tb2'] * h11) * D
        rI = X['r'] + it.tball(X['h'])
        dmax = up(dmax.union(abs(e1.ev()) * OM(arb(rI.upper()))))
        vmax = up(vmax.union(abs(e2.ev()) / SU))
    # [0, r0]: Taylor models from the exact series of A, B (with tau) and C (sigma, u only)
    ia_, ib_ = inner_tms(A), inner_tms(B)
    r0 = A.steps[0]['r']
    Sc, Uc = gr.bg_series(1, C.sig0, C.info['u0'])
    _, _, epsc = bt.series_start(1, C.sig0, C.info['u0'], r0)
    def tme(coef, err):
        p = [arb(0)] * 25; extra = arb(0)
        for j, c in enumerate(coef):
            if 2 * j <= 24:
                p[2 * j] = c
            else:
                extra += abs(c) * r0 ** (2 * j)
        p[0] = p[0] + (err + extra) * arb(0, 1)
        return TM(p, arb(0), r0, 24)
    sc_, uc_ = tme(Sc, epsc), tme(Uc, epsc)
    e1 = sc_ - ia_['sig'] - h01 * (ib_['sig'] - ia_['sig']) - (ia_['t1'] * h10 + ib_['t1'] * h11) * D
    e2 = uc_ - ia_['u'] - h01 * (ib_['u'] - ia_['u']) - (ia_['t2'] * h10 + ib_['t2'] * h11) * D
    dmax = up(dmax.union(abs(e1.ev()) * OM(r0))); vmax = up(vmax.union(abs(e2.ev()) / SU))
    # exterior r >= R1
    aD = absup(D)
    dext = up(OM(A.R1) * (C.sig_ext + (1 + absup(h01)) * A.sig_ext + absup(h01) * B.sig_ext
                          + aD * (absup(h10) * ext['tA1'] + absup(h11) * ext['tB1'])))
    C0 = (C.E - A.E) - h01 * (B.E - A.E) - D * (h10 * A.tau_v_c0 + h11 * B.tau_v_c0)
    C1 = (C.m - A.m) - h01 * (B.m - A.m) - D * (h10 * A.tau_v_c1 + h11 * B.tau_v_c1)
    eps = C.u_eps + A.u_eps + B.u_eps + aD * (absup(h10) * A.tau_v_eps + absup(h11) * B.tau_v_eps)
    vext = up((abs(C0 + C1 / A.R1).union(abs(C0)) + eps) / SU)
    return dict(X=up(dmax.union(vmax).union(dext).union(vext)), d_int=dmax, v_int=vmax, d_ext=dext, v_ext=vext,
                inner_note='[0, r0] by exact series Taylor models')


# ------------------------------------------------------------------ float pre-pass (deterministic steering) and CC sectors
UPM = {0: (2, 2), 1: (2, 1), 2: (1, 1), 3: (0, 0)}       # (U+, U-) of PROOF Theorem 4.5 / Corollary 4.6
KL = {0: 3, 1: 2, 2: 1}                                   # k_L = N(w2)
W1F = {0: 0.93, 1: 0.6, 2: 0.0}                           # w1 = f_L w-  (DESIGN-W2 3.3)


def krein_freqs(fd, L, wmax):
    """FLOAT: positive real eigen-frequencies w of A = J L (FD), sorted, below wmax."""
    Lp, Lm, _ = fd.ops(L)
    N = fd.N
    M = np.block([[np.zeros((N, N)), Lm], [-Lp, np.zeros((N, N))]])
    ev = np.linalg.eigvals(M)
    ws = sorted(float(e.imag) for e in ev if abs(e.real) < 1e-6 * max(1.0, abs(e)) and 1e-3 < e.imag < wmax)
    return ws


def nneg(fd, L, w):
    ev = np.linalg.eigvalsh(fd.H(L, w))
    return int((ev < 0).sum()), ev


def gap_of(fd, L, wmax):
    """FLOAT: the frequency gap (w-, w+) with N = k_L entered by a drop from k_L + 1; None if absent ('no drop')."""
    ws = [w for w in krein_freqs(fd, L, wmax) if w > 0.05]   # w ~ 0: kernel / zero modes, not a Krein drop
    k = KL[L]
    pts = [0.05] + ws + [wmax]
    prev = None
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        if b - a < 1e-4:
            continue
        n, _ = nneg(fd, L, 0.5 * (a + b))
        if n == k and prev is not None and prev[0] == k + 1:
            return dict(wm=a, wp=b, below=prev)
        prev = (n, a, b)
    return None


def fitvec(fd, v, R, kind='p'):
    for deg in (30, 40, 50):
        c = steer.cheb_fit(fd.r, v, R, deg, kind)
        err = np.abs(steer.cheb_eval(c, fd.r, R, kind) - v).max() / max(np.abs(v).max(), 1e-300)
        if err < 1e-3:
            break
    return c


def float_margin_on(H, P):
    """lowest eigenvalue of H restricted to the orthogonal complement of the columns of P (FD vectors)."""
    if P.shape[1] == 0:
        return float(np.linalg.eigvalsh(H)[0])
    Qq, _ = np.linalg.qr(P, mode='complete')
    C = Qq[:, P.shape[1]:]
    return float(np.linalg.eigvalsh(C.T @ H @ C)[0])


class End:
    """one cell end: node data + FD steering object at radius R."""

    def __init__(self, N, R):
        self.N = N; self.R = R
        assert float(N.R1.mid()) > R + 1, 'RITZ Gram quadrature must reach Rc < R1 (audit-W, hw3.gram)'
        self.fd = steer.FD(N.steps, N.Yend, R, N=900)
        self.bj = hw3.setup(N.steps, N.Yend, N.K)
        dl = hw3.delta_L(N.steps, N.info, self.bj, R, 0)
        self.wmax = float((-N.info['E'] - N.info['m'] / arb(R) - dl).lower()) - 0.02


def _pfns(fd, vecs, R):
    """FD eigenvectors (columns of length 2N) -> list of (PolyFn_a or None, PolyFn_d or None) and the fitted FD matrix."""
    N = fd.N; out = []; cols = []
    for v in vecs.T:
        v = v / np.sqrt(fd.dr)
        a, d = v[:N], v[N:]
        na, nd = np.linalg.norm(a), np.linalg.norm(d)
        fa = fitvec(fd, a, R) if na > 1e-8 * (na + nd) else None
        fdd = fitvec(fd, d, R) if nd > 1e-8 * (na + nd) else None
        out.append((hw3.PolyFn(fa, R) if fa is not None else None, hw3.PolyFn(fdd, R) if fdd is not None else None))
        cols.append(np.concatenate([steer.cheb_eval(fa, fd.r, R) if fa is not None else np.zeros(N),
                                    steer.cheb_eval(fdd, fd.r, R) if fdd is not None else np.zeros(N)]))
    return out, (np.array(cols).T if cols else np.zeros((2 * N, 0)))


def cert_cpos(e, L, w, k_vecs, mf):
    """certify CPOS at one end with m = 0.7 mf, fallback 0.35 mf (deterministic)."""
    N = e.N
    res = dict(ok=False, why='float margin not positive (%.3g)' % mf)
    for fac in ('0.7', '0.35'):
        m = arb(mf) * arb(fac)
        if not m > 0:
            break
        res = hw3.cpos(e.bj, N.steps, N.info, 1, N.sig0, L, it.exact(w), m, e.R, N.K, k_vecs)
        if res['ok']:
            res['m_cert'] = m
            return res
    res['m_cert'] = None
    return res


def _slim(r):
    return {k: r.get(k) for k in ('ok', 'nB', 'conj', 'endpoint', 'ext_ok', 'S_negdef', 'S_pivots', 'why', 'seconds')}


def sector_certs(ea, eb, log=print):
    """the 11 certificates at both ends with common explicit vectors."""
    out = {}
    R = ea.R
    wmax = min(ea.wmax, eb.wmax)
    for L in (0, 1, 2):
        ga = gap_of(ea.fd, L, wmax); gb = gap_of(eb.fd, L, wmax)
        if ga is None or gb is None:
            why = 'no drop in L = %d (float pre-pass: no gap with N = %d entered by a drop at %s)' % (
                L, KL[L], ' and '.join(x for x, g in (('a', ga), ('b', gb)) if g is None))
            out['H(w2) L%d' % L] = dict(ok=False, L=L, why=why, step='no drop')
            out['RITZ L%d' % L] = dict(ok=False, L=L, why=why, step='no drop')
            log('    sector L%d: NO DROP' % L)
            continue
        k = KL[L]
        def best_w2(fd, g):
            best = None
            for f in (0.3, 0.4, 0.5, 0.6, 0.7):
                w = g['wm'] + f * (g['wp'] - g['wm'])
                n, ev = nneg(fd, L, w)
                if n == k and (best is None or ev[k] > best[1]):
                    best = (w, ev[k])
            return best
        bwa = best_w2(ea.fd, ga); bwb = best_w2(eb.fd, gb)
        if bwa is None or bwb is None:                                             # audit-W C-6: record, never crash
            why = 'CPOS H(w2) L=%d: float pre-pass found no w2 with N = %d inside the gap' % (L, k)
            out['H(w2) L%d' % L] = dict(ok=False, L=L, why=why, step='CPOS')
            out['RITZ L%d' % L] = dict(ok=False, L=L, why=why, step='CPOS')
            continue
        (wa, mua), (wb, mub) = bwa, bwb
        wa = float(repr(round(wa, 6))); wb = float(repr(round(wb, 6)))
        src = ea if mua <= mub else eb
        evs, V = np.linalg.eigh(src.fd.H(L, wa if src is ea else wb))
        pf, P = _pfns(src.fd, V[:, :k], R)
        ma_f = float_margin_on(ea.fd.H(L, wa), P); mb_f = float_margin_on(eb.fd.H(L, wb), P)
        ca = cert_cpos(ea, L, wa, pf, ma_f); cb = cert_cpos(eb, L, wb, pf, mb_f)
        ok = bool(ca['ok'] and cb['ok'])
        out['H(w2) L%d' % L] = dict(ok=ok, L=L, kind='upper', wa=wa, wb=wb, float=(ma_f, mb_f), ma=ca['m_cert'],
                                    mb=cb['m_cert'], da=_slim(ca), db=_slim(cb),
                                    why=None if ok else 'CPOS H(w2) L=%d not certified' % L, step=None if ok else 'CPOS')
        # RITZ at w1 = f_L w- (each end its own w-)
        w1a = float(repr(round(W1F[L] * ga['wm'], 6))); w1b = float(repr(round(W1F[L] * gb['wm'], 6)))
        e1a, V1a = np.linalg.eigh(ea.fd.H(L, w1a)); e1b, V1b = np.linalg.eigh(eb.fd.H(L, w1b))
        src, Vs = (ea, V1a) if e1a[k] >= e1b[k] else (eb, V1b)
        Nn = src.fd.N
        trials = []
        for j in range(k + 1):
            v = Vs[:, j] / np.sqrt(src.fd.dr); a, d = v[:Nn], v[Nn:]
            W = src.fd.Wof(L, a)
            trials.append((hw3.PolyFn(fitvec(src.fd, a, R, 'trial'), R, 'trial'),
                           hw3.PolyFn(fitvec(src.fd, d, R, 'trial'), R, 'trial'),
                           hw3.PolyFn(fitvec(src.fd, W, R, 'trialW'), R, 'trialW')))
        res = {}
        from scipy.linalg import eigh as geigh
        for tag, e, w1 in (('a', ea, w1a), ('b', eb, w1b)):
            A_, M0 = hw3.gram(e.bj, e.N.steps, e.N.info, 1, e.N.sig0, L, it.exact(w1), trials, it.exact(R))
            top = float(geigh(np.array([[float(x.mid()) for x in row] for row in A_]),
                              np.array([[float(x.mid()) for x in row] for row in M0]), eigvals_only=True)[-1])
            r_ = dict(ok=False, why='float Ritz value not negative (%.3g)' % top)
            for fac in ('0.7', '0.35'):
                m = arb(-top) * arb(fac)
                if not m > 0:
                    break
                r_ = hw3.ritz(e.bj, e.N.steps, e.N.info, 1, e.N.sig0, L, it.exact(w1), trials, it.exact(R), m)
                if r_['ok']:
                    r_['m_cert'] = m
                    break
            if not r_.get('ok'):
                r_['m_cert'] = None
            r_['float_top'] = top
            res[tag] = r_
        okr = bool(res['a']['ok'] and res['b']['ok'])
        out['RITZ L%d' % L] = dict(ok=okr, L=L, kind='lower', w1a=w1a, w1b=w1b, ma=res['a']['m_cert'], mb=res['b']['m_cert'],
                                   float=(res['a']['float_top'], res['b']['float_top']),
                                   why=None if okr else 'RITZ L=%d not certified' % L, step=None if okr else 'RITZ')
        log('    sector L%d: w2 %.5f/%.5f H(w2) %s ; w1 %.4f/%.4f RITZ %s' % (L, wa, wb, ok, w1a, w1b, okr))
    # H(0) K-rows (block vectors) and L = 3
    for L in (0, 1, 2, 3):
        upl, uml = UPM[L]; k = upl + uml
        Ha = ea.fd.H(L, 0.0); Hb = eb.fd.H(L, 0.0)
        eva = np.linalg.eigvalsh(Ha); evb = np.linalg.eigvalsh(Hb)
        src = ea if eva[k] <= evb[k] else eb
        ev, V = np.linalg.eigh(src.fd.H(L, 0.0))
        Nn = src.fd.N
        nplus = sum(1 for j in range(k) if np.linalg.norm(V[:Nn, j]) > np.linalg.norm(V[Nn:, j]))
        if nplus != upl:
            out['H(0) L%d' % L] = dict(ok=False, L=L, why='float block split %d != U+ = %d' % (nplus, upl), step='K-row')
            continue
        pf, P = _pfns(src.fd, V[:, :k], R)
        ma_f = float_margin_on(Ha, P); mb_f = float_margin_on(Hb, P)
        ca = cert_cpos(ea, L, 0.0, pf, ma_f); cb = cert_cpos(eb, L, 0.0, pf, mb_f)
        ok = bool(ca['ok'] and cb['ok'])
        out['H(0) L%d' % L] = dict(ok=ok, L=L, kind='upper', float=(ma_f, mb_f), ma=ca['m_cert'], mb=cb['m_cert'],
                                   da=_slim(ca), db=_slim(cb), why=None if ok else 'H(0) L=%d not certified' % L,
                                   step=None if ok else 'K-row')
        log('    H(0) L%d: %s (float margins %.3g / %.3g)' % (L, ok, ma_f, mb_f))
    # PEN (L = 0): Pen = L+(0) + M' <., g>^2, M' = 5
    Mp = 5.0
    pens = []
    for e in (ea, eb):
        Lp, _, _ = e.fd.ops(0)
        g = e.fd.r * e.fd.sig
        pens.append(Lp + Mp * e.fd.dr * np.outer(g, g))
    eva = np.linalg.eigh(pens[0]); evb = np.linalg.eigh(pens[1])
    srcv = eva if eva[0][1] <= evb[0][1] else evb
    fd0 = ea.fd
    cp = fitvec(fd0, srcv[1][:, 0] / np.sqrt(fd0.dr), R)
    pv = steer.cheb_eval(cp, fd0.r, R)[:, None]
    mf = [float_margin_on(pens[0], pv), float_margin_on(pens[1], pv)]
    pres = []
    for e, m_f in zip((ea, eb), mf):
        r_ = dict(ok=False)
        for fac in ('0.7', '0.35'):
            m = arb(m_f) * arb(fac)
            if not m > 0:
                break
            r_ = hw3.pen(e.bj, e.N.steps, e.N.info, 1, e.N.sig0, m, R, e.N.K, hw3.PolyFn(cp, R), Mp=5)
            if r_['ok']:
                r_['m_cert'] = m
                break
        if not r_.get('ok'):
            r_['m_cert'] = None
        pres.append(r_)
    okp = bool(pres[0]['ok'] and pres[1]['ok'])
    out['PEN'] = dict(ok=okp, L=0, kind='pen', float=tuple(mf), ma=pres[0]['m_cert'], mb=pres[1]['m_cert'],
                      da={k_: pres[0].get(k_) for k_ in ('d2', 'Mpp_d2', 'sherman', 'theta', 'why')},
                      db={k_: pres[1].get(k_) for k_ in ('d2', 'Mpp_d2', 'sherman', 'theta', 'why')},
                      why=None if okp else 'PEN not certified', step=None if okp else 'PEN')
    log('    PEN: %s (float %.3g / %.3g)' % (okp, mf[0], mf[1]))
    return out


# ------------------------------------------------------------------ the cell
def _s(v):
    return v.str(6) if hasattr(v, 'str') else v


def run_cell(A, B, R=14.0, inject=None, loo=None, log=print, sectors=True):
    """A, B: NodeData of the two ends (sigma_A < sigma_B). loo: optional TubeOnly of an interior node (control).
    Outcome HOLDS / INCONCLUSIVE (failing step named) / REJECTED (injected data, XI)."""
    t0 = time.time()
    _sym_check()
    D = it.exact(Fraction(B.sig0_str) - Fraction(A.sig0_str))
    rec = dict(cell=[A.sig0_str, B.sig0_str], R=R, tube_sha=[A.info.get('tube_sha256'), B.info.get('tube_sha256')])
    try:
        tms1 = half_tms(A, B, other=loo, inject=inject)
        tms2 = half_tms(B, A)
    except Reject as ex:
        rec.update(outcome='REJECTED', why=str(ex), seconds=time.time() - t0)
        return rec
    log('  cross-grid TMs [%.1fs]' % (time.time() - t0))
    b1 = br_half(A, B, D, tms1, log=log)
    b2 = br_half(B, A, -D, tms2, log=log)
    rec['BR'] = [{k: _s(v) for k, v in b.items() if k not in ('ch', 'ext')} for b in (b1, b2)]
    fails = []
    brok = bool(b1['ok'] and b2['ok'])
    if not brok:
        fails.append(('BR', 'BR closure failed: %s / %s' % (b1.get('why'), b2.get('why'))))
    if brok and not bool(b1['rho'] <= b2['r_u'] and b2['rho'] <= b1['r_u']):      # audit-W C-4 (BR' item 2)
        fails.append(('BR', 'halves disagree')); brok = False
    rho = up(b1['rho'].union(b2['rho'])) if ('rho' in b1 and 'rho' in b2) else None
    if 'r_u' in b1 and 'r_u' in b2:
        dA = tube_diameter(A); dB = tube_diameter(B)
        rec['tube_diameter'] = [dA.str(3), dB.str(3)]
        rec['tube_below_r_u'] = bool(dA < b1['r_u'] and dB < b2['r_u'])
        if not rec['tube_below_r_u']:
            fails.append(('BR', 'tube X-diameter not below r_u'))
    if loo is not None and 'rho' in b1 and 'rho' in b2:
        th = (Fraction(loo.sig0_str) - Fraction(A.sig0_str)) / (Fraction(B.sig0_str) - Fraction(A.sig0_str))
        dist = loo_distance(A, B, loo, tms1, D, th, b1['ext'])
        bh = b1 if th <= Fraction(1, 2) else b2          # the BR ball of the half that contains theta
        rec['LOO'] = dict(theta=str(th), X=dist['X'].str(5), rho=bh['rho'].str(5), inside=bool(dist['X'] <= bh['rho']),
                          parts={k: dist[k].str(4) for k in ('d_int', 'v_int', 'd_ext', 'v_ext')})
    if rho is None or not brok:
        rec.update(outcome='INCONCLUSIVE', failing_step='BR', fails=fails, seconds=time.time() - t0)
        return rec
    chc = ch_constants(A, B, b1['ch'], b2['ch'], rho, b1['ext'])
    rec['CH'] = {str(L): {k: v.str(5) for k, v in chc[L].items()} for L in range(4)}
    rec['CH']['Gam'] = {k: v.str(5) for k, v in chc['Gam'].items()}
    log('  BR + CH [%.1fs]' % (time.time() - t0))
    # one node and E < 0 at r_n = r_x of node A, |E| lower bound at R1 (BR' item 4)
    ch1 = b1['ch']; nsub = A.g.nsub
    cx = ch1[A.g.ix * nsub]
    H1lo = arb(min(abs(cx['sa']).lower(), abs(cx['sb']).lower())) - cx['ps'] / 4
    H2up = up(cx['ua'].union(cx['ub'])) + cx['pu'] / 4                             # audit-W C-2
    one_node = bool(cx['sa'] * cx['sb'] > 0 and H1lo - rho / OM(cx['r']) > 0 and H2up + rho * SU < 0)   # C-5
    cR = ch1[-1]
    absE_lo = -(up(cR['ua'].union(cR['ub'])) + cR['pu'] / 4 + rho * SU)            # audit-W C-2
    rec['one_node_E_neg'] = one_node; rec['absE_lower'] = absE_lo.str(6)
    if not one_node:
        fails.append(('BR', 'one-node / E < 0 check at r_n failed'))
    if not sectors:
        rec.update(outcome='INCONCLUSIVE' if fails else 'BR-ONLY', fails=fails, seconds=time.time() - t0)
        return rec
    ea = End(A, R); eb = End(B, R)
    sc = sector_certs(ea, eb, log=log)
    rec['certs'] = {}
    for name, c in sc.items():
        row = {k: _s(v) for k, v in c.items()}
        if c.get('ok'):
            L = c['L']
            if c['kind'] == 'upper':
                cc = quad_pos(c['ma'], c['mb'], chc[L]['C0'], chc[L]['C1'])
            elif c['kind'] == 'lower':
                cc = quad_pos(c['ma'], c['mb'], chc[L]['C0p'], chc[L]['C1p'])
            else:
                Mp = arb(5)
                cc = quad_pos(c['ma'], c['mb'], chc[0]['C0'] + Mp * chc['Gam']['G0'], chc[0]['C1'] + Mp * chc['Gam']['G1'])
            row['CC'] = bool(cc)
            if not cc:
                fails.append((name, 'CC test failed (margins vs chord loss)'))
        else:
            row['CC'] = False
            fails.append((name, c.get('why')))
        rec['certs'][name] = row
    for L in (0, 1, 2):
        h = sc.get('H(w2) L%d' % L, {}); r = sc.get('RITZ L%d' % L, {})
        if h.get('ok') and r.get('ok'):
            okw = bool(r['w1a'] < h['wa'] and r['w1b'] < h['wb'] and it.exact(max(h['wa'], h['wb'])) < absE_lo)
            rec['certs']['H(w2) L%d' % L]['w_check'] = okw
            if not okw:
                fails.append(('H(w2) L%d' % L, 'w-check failed'))
    rec['fails'] = fails
    rec['outcome'] = 'HOLDS' if not fails else 'INCONCLUSIVE'
    steps_ = sorted(set('no drop L%s' % f[0][-1] if (f[1] and 'no drop' in str(f[1])) else f[0] for f in fails))
    rec['failing_steps'] = steps_
    rec['seconds'] = time.time() - t0
    return rec
