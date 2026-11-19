"""itaylor.py - self-contained interval Taylor (Moore / HOE) integrator over python-flint arb/acb balls.

Theorem used (high-order enclosure, Corliss-Rihm 1996; Nedialkov-Jackson-Corliss 1999):
  if  sum_{k<=K} y_k(Y0) t^k + t^(K+1) f^[K+1](r_I, B)  lies in int(B) for all t in [0,h]
  then the solution from every y0 in Y0 exists on [r, r+h] and stays in B, and
  y(r+h) in sum_{k<=K} y_k(Y0) h^k + h^(K+1) f^[K+1](r_I, B).
Here f^[k] is the k-th Taylor-coefficient function (computed by jet recursions), evaluated with
base point r_I = [r, r+h] (hull) and state box B. This is valid for either sign of h.

Two steppers:
  bg_step   - the GPP background  sigma'' + 2 sigma'/r = (s sigma^2 - u) sigma,  u'' + 2u'/r = -sigma^2,
              with quadratures QT' = sigma'^2 r^2, QF' = sigma^4 r^2, QU' = sigma^2 u r^2.
  lin_step  - linear second-order systems  Y'' = A(r) Y + F(r) + sum_src M Y_src  (many columns),
              with quadratures q' = coef(r) * y_a * (conj) y_b.  The coefficient jets of A (at the base
              point, and over the step box) are supplied by the caller from the background tube.
No floating point enters any enclosure: all arithmetic is arb/acb ball arithmetic.
"""
import math
from fractions import Fraction
from flint import arb, acb, ctx


def set_prec(bits):
    ctx.prec = bits


def exact(x):
    """ball enclosure of the EXACT rational a parameter literal denotes (REFEREE-R1-FINAL item 1):
    a float is read as the shortest decimal that round-trips (repr), so 1.80 -> 9/5, 1e-3 -> 1/1000, never the
    binary double 1.8000000000000000444...; a str or Fraction is read exactly; an arb is returned unchanged."""
    if isinstance(x, arb):
        return x
    f = Fraction(repr(x)) if isinstance(x, float) else Fraction(x)
    return arb(f.numerator) / arb(f.denominator)


def fup(x):
    """a float >= the upper end of the arb x (outward rounding; float() alone rounds to nearest)."""
    u = arb(x).upper()
    f = float(u)
    return math.nextafter(f, math.inf) if arb(f) < u else f


def flo(x):
    """a float <= the lower end of the arb x (outward rounding)."""
    l = arb(x).lower()
    f = float(l)
    return math.nextafter(f, -math.inf) if arb(f) > l else f


def tball(h):
    """the interval hull of 0 and h (h an arb, either sign)."""
    h = arb(h)
    return h / 2 + (h / 2) * arb(0, 1)


def inflate(x, fac, add):
    if isinstance(x, acb):
        return acb(inflate(x.real, fac, add), inflate(x.imag, fac, add))
    return x + arb(0, 1) * (x.rad() * fac + add)


def union(a, b):
    return a.union(b)


def contains_int(B, X):
    return B.contains_interior(X)


def horner(c, t):
    r = c[-1] * 0
    for a in reversed(c):
        r = r * t + a
    return r


def conv(A, B, k):
    """k-th coefficient of the product of two jets (lists)."""
    s = A[0] * B[k]
    for j in range(1, k + 1):
        s += A[j] * B[k - j]
    return s


def inv_r_jet(rc, n):
    inv = 1 / rc
    out = [inv]
    for _ in range(n):
        out.append(-out[-1] * inv)
    return out


def r2_jet(rc, n):
    z = rc * 0
    out = [rc * rc, 2 * rc, z + 1] + [z] * max(0, n - 2)
    return out[:n + 1]


def r1_jet(rc, n):
    z = rc * 0
    out = [rc, z + 1] + [z] * max(0, n - 1)
    return out[:n + 1]


def inv_r2_jet(rc, n):
    ir = inv_r_jet(rc, n)
    return [conv(ir, ir, k) for k in range(n + 1)]


# ---------------------------------------------------------------- background
NB = 7  # sigma, sigma', u, u', QT, QF, QU


def bg_jets(s, rc, y0, K):
    """Taylor coefficients 0..K of the background state about base point rc (arb, may be an interval)."""
    S = [y0[0]]; P = [y0[1]]; U = [y0[2]]; V = [y0[3]]
    QT = [y0[4]]; QF = [y0[5]]; QU = [y0[6]]
    ir = inv_r_jet(rc, K)
    r2 = r2_jet(rc, K)
    S2 = []; S3 = []; US = []; PI = []; VI = []; PP = []; S4 = []; S2U = []
    sa = arb(s)
    for k in range(K):
        S2.append(conv(S, S, k)); S3.append(conv(S2, S, k)); US.append(conv(U, S, k))
        PI.append(conv(P, ir, k)); VI.append(conv(V, ir, k))
        dp = sa * S3[k] - US[k] - 2 * PI[k]
        dv = -S2[k] - 2 * VI[k]
        PP.append(conv(P, P, k)); S4.append(conv(S2, S2, k)); S2U.append(conv(S2, U, k))
        QT.append(conv(PP, r2, k) / (k + 1)); QF.append(conv(S4, r2, k) / (k + 1)); QU.append(conv(S2U, r2, k) / (k + 1))
        S.append(P[k] / (k + 1)); P.append(dp / (k + 1)); U.append(V[k] / (k + 1)); V.append(dv / (k + 1))
    return [S, P, U, V, QT, QF, QU]


def bg_step(s, rc, Y0, h, K, maxit=30):
    """one rigorous step; returns (Y1, B, jets0) with B the enclosure over the whole step."""
    T = tball(h)
    J0 = bg_jets(s, rc, Y0, K)
    head = [horner(J0[i], T) for i in range(NB)]
    B = [inflate(head[i], arb("0.1"), arb(2) ** (-ctx.prec + 20) + abs(head[i]).upper() * arb(2) ** (-ctx.prec // 2)) for i in range(NB)]
    rI = rc + T
    TK = T ** (K + 1)
    for it in range(maxit):
        JB = bg_jets(s, rI, B, K + 1)
        new = [head[i] + JB[i][K + 1] * TK for i in range(NB)]
        if all(contains_int(B[i], new[i]) for i in range(NB)):
            break
        B = [B[i] if contains_int(B[i], new[i]) else inflate(union(B[i], new[i]), arb('0.5'), arb(2) ** (-ctx.prec + 20)) for i in range(NB)]
    else:
        raise RuntimeError('bg_step: a priori enclosure failed at r=%s h=%s' % (rc, h))
    hK = arb(h) ** (K + 1)
    Y1 = [horner(J0[i], arb(h)) + JB[i][K + 1] * hK for i in range(NB)]
    return Y1, B, J0


def suggest_h(J, K, tol, hmax):
    """step-size heuristic from the last Taylor coefficients (not part of the proof)."""
    m = 0.0
    for c in J[:4]:
        for k in (K - 1, K):
            a = abs(float(c[k].mid()))
            if a > 0:
                m = max(m, (a / tol) ** (1.0 / k))
    if m == 0:
        return hmax
    return min(hmax, 0.8 / m)


# ---------------------------------------------------------------- linear systems
class LinSys:
    """Y'' = A(r) Y + F(r) + sum over extra (tgt, src, M) of M Y_src ;  n channels, columns given at step time.

    A_spec: dict (i,j) -> name of a coefficient jet ('c:<value>' entries are constants handled by caller)
    The caller provides, per step, a dict name -> jet (point) and name -> jet (box)."""

    def __init__(self, n, A_terms, extra=None, forcing=None, quads=None):
        # A_terms: list of (i, j, coef) where coef is either ('jet', name, scale) or ('const', value)
        self.n = n
        self.A = A_terms
        self.extra = extra or []      # (tgt_col, src_col, [(i, j, const)])
        self.forcing = forcing or {}  # col -> list of (channel, name, scale)
        self.quads = quads or []      # (name_or_None, (col, comp), (col, comp), conj2)


def lin_jets(sys, jets, X0, K):
    """Taylor coefficients 0..K of all columns and quadratures. X0: list of columns; each column is a list of
    2n entries (values then derivatives); quadrature initial values appended as X0q (list) via X0[-1] if quads."""
    n = sys.n
    ncol = len(X0) - (1 if sys.quads else 0)
    Yv = [[[X0[c][i]] for i in range(n)] for c in range(ncol)]
    Yd = [[[X0[c][n + i]] for i in range(n)] for c in range(ncol)]
    # order columns so that sources of 'extra' are computed first within each order (they are: extra only uses Yv)
    for k in range(K):
        newd = []
        for c in range(ncol):
            acc = []
            for i in range(n):
                acc.append(None)
            for (i, j, coef) in sys.A:
                if coef[0] == 'const':
                    t = coef[1] * Yv[c][j][k]
                else:
                    jt = jets[coef[1]]
                    t = conv(jt, Yv[c][j], k)
                    if coef[2] != 1:
                        t = t * coef[2]
                acc[i] = t if acc[i] is None else acc[i] + t
            for (ch, name, scale) in sys.forcing.get(c, []):
                t = jets[name][k] * scale
                acc[ch] = t if acc[ch] is None else acc[ch] + t
            for (tgt, src, M) in sys.extra:
                if tgt != c:
                    continue
                for (i, j, cst) in M:
                    t = cst * Yv[src][j][k]
                    acc[i] = t if acc[i] is None else acc[i] + t
            newd.append(acc)
        for c in range(ncol):
            for i in range(n):
                Yv[c][i].append(Yd[c][i][k] / (k + 1))
                a = newd[c][i]
                Yd[c][i].append((a if a is not None else Yv[c][i][k] * 0) / (k + 1))
    Q = []
    if sys.quads:
        q0 = X0[-1]
        for qi, (name, f1, f2, cj) in enumerate(sys.quads):
            c1, p1 = f1
            A1 = Yv[c1][p1] if p1 < n else Yd[c1][p1 - n]
            if f2 is None:
                prod = list(A1[:K])
            else:
                c2, p2 = f2
                A2 = Yv[c2][p2] if p2 < n else Yd[c2][p2 - n]
                if cj:
                    A2 = [x.conjugate() for x in A2]
                prod = [conv(A1, A2, k) for k in range(K)]
            if name is not None:
                jt = jets[name]
                prod = [conv(jt, prod, k) for k in range(K)]
            Q.append([q0[qi]] + [prod[k] / (k + 1) for k in range(K)])
    cols = [[Yv[c][i] for i in range(n)] + [Yd[c][i] for i in range(n)] for c in range(ncol)]
    return cols, Q


def _flat(cols, Q):
    out = []
    for col in cols:
        out.extend(col)
    out.extend(Q)
    return out


def _unflat(vals, ncol, n, nq):
    cols = [vals[c * 2 * n:(c + 1) * 2 * n] for c in range(ncol)]
    if nq:
        cols.append(vals[ncol * 2 * n:])
    return cols


def lin_step(sys, jets_pt, jets_box, X0, h, K, maxit=30):
    """one rigorous step of the linear system. Returns (X1, coeffs_flat, rem_flat) where every component c obeys
       c(r+t) in sum_k coeffs[c][k] t^k + t^(K+1) rem[c]   for t in [0,h] (or [h,0])."""
    n = sys.n
    nq = len(sys.quads)
    ncol = len(X0) - (1 if nq else 0)
    T = tball(h)
    cols, Q = lin_jets(sys, jets_pt, X0, K)
    C = _flat(cols, Q)
    head = [horner(c, T) for c in C]
    tiny = arb(2) ** (-ctx.prec + 20)
    B = [inflate(x, arb("0.1"), tiny + abs(x).upper() * arb(2) ** (-ctx.prec // 2)) for x in head]
    TK = T ** (K + 1)
    for it in range(maxit):
        cb, qb = lin_jets(sys, jets_box, _unflat(B, ncol, n, nq), K + 1)
        R = [c[K + 1] for c in _flat(cb, qb)]
        new = [head[i] + R[i] * TK for i in range(len(head))]
        if all(contains_int(B[i], new[i]) for i in range(len(B))):
            break
        B = [B[i] if contains_int(B[i], new[i]) else inflate(union(B[i], new[i]), arb('0.5'), tiny) for i in range(len(B))]
    else:
        raise RuntimeError('lin_step: a priori enclosure failed (h=%s)' % h)
    ha = arb(h)
    hK = ha ** (K + 1)
    X1 = [horner(C[i], ha) + R[i] * hK for i in range(len(C))]
    return _unflat(X1, ncol, n, nq), C, R, B


def eval_sub(C, R, t1, t2, K, h):
    """enclosure of every component over t in [t1, t2] (sub-interval of the step [0, h]; asserted, audit-1)."""
    T = arb(t1).union(arb(t2))
    assert tball(h).contains(T), 'eval_sub: t outside hull(0, h)'
    TK = T ** (K + 1)
    return [horner(c, T) + r * TK for c, r in zip(C, R)]


def eval_at(C, R, t, K, h):
    t = arb(t)
    assert tball(h).contains(t), 'eval_at: t outside hull(0, h)'   # audit-1 latent patch
    tK = t ** (K + 1)
    return [horner(c, t) + r * tK for c, r in zip(C, R)]
