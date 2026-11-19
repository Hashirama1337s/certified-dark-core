"""match.py - certified matching matrix M(lam) = [Reg(r_m) | Dec(r_m)] (6x6) for the per-L linearised GPP system,
and its lam-derivative, from: Frobenius-Volterra regular basis at r0 -> outward to r_m; certified decaying basis
(tail.py lemma at R1) -> inward to r_m. Optional Gram quadratures int a_i d_j on both sides (Krein form).

Channels (a, c, psi) [EVANS, complex lam]  or  (a, d, psi) [KREIN, real w; lam = i w, c = i d]:
  EVANS:  a'' = V+ a + lam c + 2 sigma psi,  c'' = V- c - lam a,  psi'' = ell/r^2 psi + sigma a
  KREIN:  a'' = V+ a - w d  + 2 sigma psi,   d'' = V- d - w a,    psi'' = ell/r^2 psi + sigma a
  V+ = ell/r^2 + 3 s sigma^2 - u,  V- = ell/r^2 + s sigma^2 - u.
Regular start: Y = r^(L+1) Z, Z'' + 2(L+1)/r Z' = Qt Z, Z(0) = I; on [0, r0] (second order, see frob_start):
  |Z - I| <= e1 = c/(1-c), c = r0^2 q/(2(2L+3)),  |Z'| <= e2 = r0 q (1+e1)/(2L+3),  q >= ||Qt||_inf (crude bounds).
  Columns are normalised by r0^(L+1):  Y(r0) = Z(r0),  Y'(r0) = ((L+1)/r0) Z(r0) + Z'(r0).
Decaying side: X~_j = Xhat_j + sum_i t~_ij G_i (tail.vectors); Xhat and G are integrated inward as separate columns.
"""
from flint import arb, acb, ctx
import itaylor as it
import lincore as lc
import tail as tl
import bg_tube as bt


def system(mode, L, s, par, nprim, deriv, gram_cols):
    """tail-diagonal channels (p, q, psi) [EVANS: p = a + i c, q = a - i c] or (P, Q, psi) [KREIN: P = a + d, Q = a - d]:
         p'' = (Vbar - i lam) p + s sigma^2 q + 2 sigma psi      P'' = (Vbar - w) P + s sigma^2 Q + 2 sigma psi
         q'' = s sigma^2 p + (Vbar + i lam) q + 2 sigma psi      Q'' = s sigma^2 P + (Vbar + w) Q + 2 sigma psi
         psi'' = (ell/r^2) psi + (sigma/2)(p + q)                 psi'' = (ell/r^2) psi + (sigma/2)(P + Q)
       Vbar = (V+ + V-)/2 = ell/r^2 + 2 s sigma^2 - u."""
    ell = L * (L + 1)
    if mode == 'evans':
        mp, mq = -acb(0, 1) * par, acb(0, 1) * par
        dA = [(0, 0, -acb(0, 1)), (1, 1, acb(0, 1))]
    else:
        mp, mq = -par, par
        dA = [(0, 0, arb(-1)), (1, 1, arb(1))]
    # each matrix entry is ONE combined jet (adding the constant inside the jet avoids interval cancellation loss)
    terms = {'VbP': [('ir2', ell), ('sig2', 2 * s), ('u', -1), ('one', mp)],
             'VbQ': [('ir2', ell), ('sig2', 2 * s), ('u', -1), ('one', mq)],
             'Vs': [('ir2', ell)]}
    A = [(0, 0, ('jet', 'VbP', 1)), (0, 1, ('jet', 'sig2', s)), (0, 2, ('jet', 'sig', 2)),
         (1, 0, ('jet', 'sig2', s)), (1, 1, ('jet', 'VbQ', 1)), (1, 2, ('jet', 'sig', 2)),
         (2, 0, ('jet', 'sig', arb('0.5'))), (2, 1, ('jet', 'sig', arb('0.5'))), (2, 2, ('jet', 'Vs', 1))]
    if s == 0:
        A = [t for t in A if not (t[2][0] == 'jet' and t[2][1] == 'sig2')]
    extra = [(nprim + j, j, dA) for j in range(nprim)] if deriv else []
    # Krein form: <a, d> = (1/4) int (P^2 - Q^2): quadratures int P_i P_j and int Q_i Q_j
    quads = [(None, (i, 0), (j, 0), False) for i in range(gram_cols) for j in range(gram_cols)] +             [(None, (i, 1), (j, 1), False) for i in range(gram_cols) for j in range(gram_cols)]
    if gram_cols == 0:
        quads = []
    return it.LinSys(3, A, extra=extra, quads=quads), terms


def frob_start(mode, L, s, sig0, u0, par, r0, deriv, real):
    sg = abs(it.exact(sig0)) + arb('0.01'); ua = abs(arb(u0)) + arb('0.01')
    bt.assert_start_margins(s, sig0, u0, r0, sg, ua)      # item 3: 0.01 margins checked from the crude enclosure
    ap = arb(abs(par).upper())
    q = 2 * (2 * abs(arb(s)) * sg * sg + ua + ap + abs(arb(s)) * sg * sg + 2 * sg) + sg
    r0 = arb(r0)
    c = r0 * r0 * q / (2 * (2 * L + 3))
    assert c < arb('0.25')
    e1 = c / (1 - c)
    e2 = r0 * q * (1 + e1) / (2 * L + 3)
    # d/dlam: ||dQt|| = 1 (row sums), Volterra: |dZ| <= r0^2 (1+e1 + q dZ)/(2(2L+3))
    cd = r0 * r0 / (2 * (2 * L + 3))
    e1d = cd * (1 + e1) / (1 - c)
    e2d = r0 * ((1 + e1) + q * e1d) / (2 * L + 3)
    B = arb(0, 1) if real else acb(arb(0, 1), arb(0, 1))
    one = arb(1) if real else acb(1)
    k = arb(L + 1) / r0
    # second-order Frobenius: Z = I + r^2 Z2 + O(r^4), Z2 = Qt(0)/(2(2L+3)), dZ = r^2 dQt/(2(2L+3)) + O(r^4).
    # Qt(r) = Qt0 + dQ(r), |dQ(r)| <= cq r^2 (sigma, u even; |sigma - sigma0| <= F r^2/6, |u - u0| <= sg^2 r^2/6).
    # Volterra: |Z - I - r^2 Z2| <= r^4 (cq + q y2)/(4(2L+5)), |Z' - 2 r Z2| <= r^3 (cq + q y2)/(2L+5),
    # with y2 = sup |Z - I|/r^2 <= q (1+e1)/(2(2L+3)).
    s_ = arb(s); sig0a = it.exact(sig0); u0a = arb(u0)    # sigma0 exact (1.80 -> 9/5), was arb(sig0) (the double)
    if mode == 'evans':
        mp, mq, dmp, dmq = -acb(0, 1) * par, acb(0, 1) * par, -acb(0, 1), acb(0, 1)
    else:
        mp, mq, dmp, dmq = -par, par, arb(-1), arb(1)
    Vb0 = 2 * s_ * sig0a * sig0a - u0a
    Q0 = [[Vb0 + mp, s_ * sig0a * sig0a, 2 * sig0a], [s_ * sig0a * sig0a, Vb0 + mq, 2 * sig0a],
          [sig0a / 2, sig0a / 2, one * 0]]
    dQ0 = [[dmp, one * 0, one * 0], [one * 0, dmq, one * 0], [one * 0, one * 0, one * 0]]
    Fm = (abs(s_) * sg * sg + ua) * sg
    dsig = Fm / 6; du = sg * sg / 6
    cq = 2 * (3 * abs(s_) * 2 * sg * dsig + du + 2 * dsig) + dsig
    y2 = q * (1 + e1) / (2 * (2 * L + 3))
    den = arb(2 * (2 * L + 3))
    # REFEREE-R1-FINAL item 6: the remainder bounds R4, R3 (and R4d, R3d) below omit the factors (1 + e1) and
    # 1/(1 - c) of the full Volterra estimate. They are covered by the factor-2 slack built into q and cq
    # (q = 2 x (row bound) + sg and cq = 2 x (max row) + dsig, both twice the true row bounds), with
    # (1 + e1)/(1 - c) = 1/(1 - c)^2 < 1.78 < 2 because c < 0.25 is asserted above (referee-3 item 5 re-derivation).
    R4 = r0 ** 4 * (cq + q * y2) / (4 * (2 * L + 5))
    R3 = r0 ** 3 * (cq + q * y2) / (2 * L + 5)
    d2 = (1 + e1) / den                        # sup |dZ|/r^2 (first-order, |dQt| = 1)
    R4d = r0 ** 4 * (1 * y2 + q * d2) / (4 * (2 * L + 5))
    R3d = r0 ** 3 * (1 * y2 + q * d2) / (2 * L + 5)
    cols = []
    for j in range(3):
        v = [one * 0] * 6
        for i in range(3):
            z = (one if i == j else one * 0) + r0 * r0 * Q0[i][j] / den + R4 * B
            zp = 2 * r0 * Q0[i][j] / den + R3 * B
            v[i] = z
            v[3 + i] = k * z + zp
        cols.append(v)
    dcols = []
    if deriv:
        for j in range(3):
            v = [one * 0] * 6
            for i in range(3):
                z = r0 * r0 * dQ0[i][j] / den + R4d * B
                zp = 2 * r0 * dQ0[i][j] / den + R3d * B
                v[i] = z
                v[3 + i] = k * z + zp
            dcols.append(v)
    return cols, dcols, dict(q=q, e1=R4, e2=R3)


def _mv(F, v, zero):
    """F given as a list of columns (each 6 entries): returns F v."""
    return [sum((F[k][i] * v[k] for k in range(6)), zero) for i in range(6)]


def _qf(u, A, v, zero):
    return sum((u[k] * A[k][l] * v[l] for k in range(6) for l in range(6)), zero)


def _ident(zero):
    one = zero + 1
    return [[one if i == k else zero for i in range(6)] for k in range(6)]


def matrix(bj, info, mode, L, s, sig0, par, r_m, deriv=False, gram=False, par_disc=None, disc_r=None, box_r=None,
           Ntail=10, K=24):
    """returns dict with M (6x6, rows p,q,psi,p',q',psi'), dM (if deriv), Gram matrices (if gram), tail data.
    Both sides integrate the FUNDAMENTAL MATRIX from exact identity data (6 columns, plus their lam-derivatives);
    the ball-valued initial data (Frobenius balls, tail data) are applied by one matrix product at r_m. This avoids
    the wrapping that a ball initial box suffers along the many steps (found on the complex controls)."""
    real = (mode == 'krein') and isinstance(par, arb)
    zero = arb(0) if real else acb(0)
    r0 = bj.r[0]
    u0 = info['u0']
    I6 = _ident(zero)
    Z6 = [[zero] * 6 for _ in range(6)]
    # ---- regular side
    sysr, terms = system(mode, L, s, par, 6, deriv, 6 if gram else 0)
    cols, dcols, fr = frob_start(mode, L, s, sig0, u0, par, r0, deriv, real)
    X0 = I6 + (Z6 if deriv else [])
    if gram:
        X0 = X0 + [[zero] * 72]
    Xr, n1 = lc.march(sysr, bj, X0, r0, r_m, K, terms=terms)
    Fr = Xr[:6]
    Reg = [_mv(Fr, c, zero) for c in cols]
    # ---- decaying side
    R1 = bj.r[-1]
    E = info['E']; m = info['m']
    if deriv:
        T = tl.lemma(mode, acb(par), E, m, L, R1, info['a1'], info['kappa1'], s, N=Ntail,
                     lam_disc=par_disc, gap=arb(disc_r) - arb(box_r))
    else:
        T = tl.lemma(mode, acb(par), E, m, L, R1, info['a1'], info['kappa1'], s, N=Ntail)
    if not T['ok']:
        return dict(ok=False, why='tail lemma: ' + T.get('why', '?'))
    Xh, G, dXh, dG, Tt, dTt = tl.vectors(mode, T, cauchy_r=disc_r, box_r=box_r, deriv=deriv, real=real)
    Xd, n2 = lc.march(sysr, bj, X0, R1, r_m, K, terms=terms)
    Fd = Xd[:6]
    XhM = [_mv(Fd, v, zero) for v in Xh]
    GM = [_mv(Fd, v, zero) for v in G]
    B = arb(0, 1) if real else acb(arb(0, 1), arb(0, 1))
    Ttr = arb(Tt.upper())
    dec = [[XhM[j][c] + sum((Ttr * B * GM[i][c] for i in range(3)), zero) for c in range(6)] for j in range(3)]
    M = [[Reg[j][i] for j in range(3)] + [dec[j][i] for j in range(3)] for i in range(6)]
    out = dict(ok=True, M=M, T=T, Td=None, frob=fr, steps=(n1, n2), Tt=Tt)
    if deriv:
        dFr = Xr[6:12]; dFd = Xd[6:12]
        dReg = [[a + b for a, b in zip(_mv(dFr, c, zero), _mv(Fr, dc, zero))] for c, dc in zip(cols, dcols)]
        dXhM = [[a + b for a, b in zip(_mv(dFd, v, zero), _mv(Fd, dv, zero))] for v, dv in zip(Xh, dXh)]
        dGM = [[a + b for a, b in zip(_mv(dFd, v, zero), _mv(Fd, dv, zero))] for v, dv in zip(G, dG)]
        dTr = arb(dTt.upper())
        ddec = [[dXhM[j][c] + sum((dTr * B * GM[i][c] + Ttr * B * dGM[i][c] for i in range(3)), zero) for c in range(6)]
                for j in range(3)]
        out['dM'] = [[dReg[j][i] for j in range(3)] + [ddec[j][i] for j in range(3)] for i in range(6)]
    if gram:
        Qr = Xr[-1]
        PPr = [[Qr[6 * k + l] for l in range(6)] for k in range(6)]
        QQr = [[Qr[36 + 6 * k + l] for l in range(6)] for k in range(6)]
        b0 = r0 * 8 * B
        out['Greg'] = [[(_qf(cols[i], PPr, cols[j], zero) - _qf(cols[i], QQr, cols[j], zero)) / 4 + b0
                        for j in range(3)] for i in range(3)]
        Qd = Xd[-1]
        PPd = [[Qd[6 * k + l] for l in range(6)] for k in range(6)]
        QQd = [[Qd[36 + 6 * k + l] for l in range(6)] for k in range(6)]
        D = Xh + G
        G6 = [[-(_qf(D[a], PPd, D[b], zero) - _qf(D[a], QQd, D[b], zero)) / 4 for b in range(6)] for a in range(6)]
        Gd = [[None] * 3 for _ in range(3)]
        for j in range(3):
            for k in range(3):
                g = G6[j][k]
                g += sum((Ttr * B * G6[3 + i][k] for i in range(3)), zero)
                g += sum((Ttr * B * G6[j][3 + l] for l in range(3)), zero)
                g += sum((Ttr * Ttr * B * G6[3 + i][3 + l] for i in range(3) for l in range(3)), zero)
                Gd[j][k] = g
        out['Gdec'] = Gd
    return out
