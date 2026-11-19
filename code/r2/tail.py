"""tail.py - certified decaying subspace of the linearised GPP system on [R, inf) (lemma TAIL-LIN, PAPER).

Setting (r >= R = R1, the end of the background tube). The linear system in (a, c, psi) is
    a'' = V+ a + 2 sigma psi + lam c ,   c'' = V- c - lam a ,   psi'' = (ell/r^2) psi + sigma a      (EVANS, complex lam)
    a'' = V+ a + 2 sigma psi - w d ,     d'' = V- d - w a ,     psi'' = (ell/r^2) psi + sigma a      (KREIN, lam = i w, c = i d)
with V+- = W0 + dV+-,  W0 = ell/r^2 + |E| - m/r,  dV+ = 3 s sigma^2 + tau,  dV- = s sigma^2 + tau,
tau = m/r - (u - E) in [0, M_t(r)/r].  Background tail (bg_tube): |sigma(r)| <= (a1/r) exp(-kappa1 (r-R)).
Model channels:  p = a + i c (EVANS) / P = a + d (KREIN):  y'' = (kp^2 - m/r + ell/r^2) y,  kp^2 = |E| - i lam  / |E| - w
                 q = a - i c         / Q = a - d        :  y'' = (kq^2 - m/r + ell/r^2) y,  kq^2 = |E| + i lam  / |E| + w
                 psi:  y'' = (ell/r^2) y,  phi_d = r^-L,  phi_g = r^(L+1).
Step 1 (Riccati): rho = -phi'/phi solves rho' = rho^2 - W. The truncated asymptotic series rho_N = sum_{n<=N} c_n r^-n
  (c_0 = +kappa decaying, -kappa growing) has residual res_N; the true rho = rho_N + eta with |eta| <= eps = res_max/rho_min
  on [R, inf), by the contraction eta = -int_r^inf exp(-2 int rho_N)(eta^2 + res) (decaying) or the forward analogue
  (growing), valid when res_max < rho_min^2.
Step 2 (coupling): Volterra map X = X0 + S[B1 X] with the R-anchored dichotomy kernels; in the norm
  N(X) = max(sup e^{mu(r-R)}|p|, sup e^{mu(r-R)}|q|, sup|psi|) it is a contraction with constant theta (explicit, below),
  so the three bounded (decaying) solutions are X0_j + E_j with N(E_j) <= theta/(1-theta).
Step 3: the basis is renormalised at R so that in every channel the error lies along the growing direction only
  (X~ = X A^-1); inward integration then damps it.  All bounds hold uniformly for lam in an acb ball (analytic in lam),
  which gives Cauchy bounds for d/dlam of the error parts.
"""
from flint import arb, acb, ctx
import itaylor as it


def amax(a, b):
    """an arb >= both (upper bound of the hull)."""
    return arb(arb(a).union(arb(b)).upper())


def amin(a, b):
    """an arb <= both (lower bound of the hull; exact, no float rounding)."""
    return arb(arb(a).union(arb(b)).lower())


def _sq(x):
    return x.sqrt()


def riccati_coeffs(kap2, m, ell, N, sign):
    """c_n and dc_n/dkap2 for rho = sum c_n r^-n (sign +1 decaying, -1 growing). kap2, m: acb/arb."""
    k = acb(kap2).sqrt()
    if sign < 0:
        k = -k
    dk = 1 / (2 * k)                       # d kappa / d kap2 (for the chosen branch, sign included)
    c = [k]; dc = [dk]
    for n in range(1, N + 1):
        sm = acb(0); dsm = acb(0)
        for i in range(1, n):
            sm += c[i] * c[n - i]
            dsm += 2 * c[i] * dc[n - i]
        Wn = -acb(m) if n == 1 else (acb(ell) if n == 2 else acb(0))
        prev = (n - 1) * c[n - 1] if n >= 2 else acb(0)
        dprev = (n - 1) * dc[n - 1] if n >= 2 else acb(0)
        cn = (-sm + Wn - prev) / (2 * c[0])
        dcn = (-dsm - dprev - 2 * dc[0] * cn) / (2 * c[0])
        c.append(cn); dc.append(dcn)
    return c, dc


def residual_coeffs(c, ell, m, kap2):
    """res = rho_N^2 - W - rho_N' as a polynomial in t = 1/r (exact cancellation of degrees <= N)."""
    N = len(c) - 1
    e = {}
    for i in range(N + 1):
        for j in range(N + 1):
            e[i + j] = e.get(i + j, acb(0)) + c[i] * c[j]
    for n in range(1, N + 1):              # -rho' = + n c_n r^-(n+1)
        e[n + 1] = e.get(n + 1, acb(0)) + n * c[n]
    e[0] = e.get(0, acb(0)) - acb(kap2)
    e[1] = e.get(1, acb(0)) + acb(m)
    e[2] = e.get(2, acb(0)) - acb(ell)
    return {k: v for k, v in e.items() if k > N}


def poly_t(c, t):
    s = acb(0)
    for a in reversed(c):
        s = s * t + a
    return s


def channel(kap2, m, ell, R, N, nsub=64):
    """certified data for one Coulomb channel on [R, inf): rho_N (decaying & growing), eps bounds, constants."""
    out = {}
    tR = 1 / arb(R)
    for sign, lab in ((1, 'd'), (-1, 'g')):
        c, dc = riccati_coeffs(kap2, m, ell, N, sign)
        res = residual_coeffs(c, ell, m, kap2)
        res_max = arb(0)
        for k, v in res.items():
            res_max += abs(v).upper() * tR ** k
        # inf of sign*Re rho_N and sup |rho_N| over t in [0, 1/R]
        rmin = None; pmax = arb(0)
        for j in range(nsub):
            t = (arb(j) + arb(0.5) + arb(0.5) * arb(0, 1)) * tR / nsub
            v = poly_t(c, t)
            lo = (sign * v.real).lower()
            rmin = lo if rmin is None or lo < rmin else rmin
            pmax = pmax.union(abs(v).upper()) if pmax != 0 else abs(v).upper()
        rmin = arb(rmin)
        ok = bool(rmin > 0 and res_max < rmin * rmin)
        eps = res_max / rmin if ok else None
        out[lab] = dict(c=c, dc=dc, res_max=res_max, rho_min=rmin, eps=eps, ok=ok, pmax=arb(pmax.upper()),
                        rhoR=poly_t(c, acb(tR)), drhoR=poly_t(dc, acb(tR)))
    d, g = out['d'], out['g']
    if d['ok'] and g['ok']:
        # gamma = inf Re(rho_d - rho_g) - eps_d - eps_g
        gam = None
        for j in range(nsub):
            t = (arb(j) + arb(0.5) + arb(0.5) * arb(0, 1)) * tR / nsub
            v = (poly_t(d['c'], t) - poly_t(g['c'], t)).real.lower()
            gam = v if gam is None or v < gam else gam
        out['gamma'] = arb(gam) - d['eps'] - g['eps']
        out['G'] = 1 / out['gamma'] if out['gamma'] > 0 else None
        out['Pmax'] = arb((d['pmax'] + d['eps']).union(g['pmax'] + g['eps']).upper())
    return out


def _ric_jets(rc, Y0, k2, dk2, m, ell, K, trackd=True):
    """jets of rho' = rho^2 - W (W = k2 - m/r + ell/r^2), d' = 2 rho d - dk2 (d = d rho/d lam), and, if Y0 has 5
    entries, of the variational quantities v1 = d rho/d rho0, v2 = d d/d rho0, v3 = d d/d d0."""
    ir = it.inv_r_jet(rc, K); ir2 = it.inv_r2_jet(rc, K)
    W = [k2 - m * ir[0] + ell * ir2[0]] + [-m * ir[k] + ell * ir2[k] for k in range(1, K + 1)]
    var = len(Y0) == 9
    J = [[y] for y in Y0]
    for k in range(K):
        rho, d = J[0], J[1]
        rr = it.conv(rho, rho, k); rd = it.conv(rho, d, k)
        new = [(rr - W[k]) / (k + 1), (2 * rd - (dk2 if (k == 0 and trackd) else 0)) / (k + 1)]
        if var:
            # v1 = d rho/d rho0, v2 = d d/d rho0, v3 = d d/d d0, p = d rho/d lam and q = d d/d lam at fixed initial data
            v1, v2, v3, p, q = J[2], J[3], J[4], J[5], J[6]
            new += [2 * it.conv(rho, v1, k) / (k + 1), 2 * (it.conv(v1, d, k) + it.conv(rho, v2, k)) / (k + 1),
                    2 * it.conv(rho, v3, k) / (k + 1), (2 * it.conv(rho, p, k) - (dk2 if k == 0 else 0)) / (k + 1),
                    2 * (it.conv(p, d, k) + it.conv(rho, q, k)) / (k + 1),
                    # sm = d rho/d m, zm = d d/d m at fixed initial data (dW/dm = -1/r)
                    (2 * it.conv(rho, J[7], k) + ir[k]) / (k + 1),
                    2 * (it.conv(J[7], d, k) + it.conv(rho, J[8], k)) / (k + 1)]
        for i in range(len(J)):
            J[i].append(new[i])
    return J


def _hoe(rc, Y0, h, k2, dk2, m, ell, K, maxit=30, trackd=True):
    n = len(Y0)
    T = it.tball(h)
    J0 = _ric_jets(rc, Y0, k2, dk2, m, ell, K, trackd)
    head = [it.horner(J0[i], T) for i in range(n)]
    tiny = arb(2) ** (-ctx.prec + 20)
    B = [it.inflate(x, arb('0.1'), tiny + abs(x).upper() * arb(2) ** (-ctx.prec // 2)) for x in head]
    rI = arb(rc) + T
    TK = T ** (K + 1)
    for _ in range(maxit):
        JB = _ric_jets(rI, B, k2, dk2, m, ell, K + 1, trackd)
        new = [head[i] + JB[i][K + 1] * TK for i in range(n)]
        if all(B[i].contains_interior(new[i]) for i in range(n)):
            break
        B = [B[i] if B[i].contains_interior(new[i]) else it.inflate(B[i].union(new[i]), arb('0.5'), tiny) for i in range(n)]
    else:
        return None, None
    ha = arb(h)
    Y1 = [it.horner(J0[i], ha) + JB[i][K + 1] * ha ** (K + 1) for i in range(n)]
    return Y1, B


def _cmid(x):
    return acb(x.real.mid(), x.imag.mid())


def _ric_step(rc, Y0, h, k2, dk2, m, ell, K, trackd=True):
    """centred (mean-value) step: Y1 = Y1(mid Y0) + J(box) (Y0 - mid Y0). The Riccati flow contracts in the stable
    direction, which a naive interval Taylor step cannot see; the mean-value form does."""
    c = [_cmid(Y0[0]), _cmid(Y0[1])]
    k2c = _cmid(acb(k2))
    mc = arb(arb(m).mid())
    Yc, Bc = _hoe(rc, c, h, k2c, dk2, mc, ell, K, trackd=trackd)
    if Yc is None:
        return None, None
    z = acb(0)
    Yv, Bv = _hoe(rc, [Y0[0], Y0[1], acb(1), z, acb(1), z, z, z, z], h, k2, dk2, m, ell, K, trackd=trackd)
    if Yv is None:
        return None, None
    d0 = Y0[0] - c[0]; d1 = Y0[1] - c[1]
    dl = (acb(k2) - k2c) / dk2
    dm = acb(arb(m) - mc)
    Y1 = [Yc[0] + Yv[2] * d0 + Yv[5] * dl + Yv[7] * dm,
          Yc[1] + Yv[3] * d0 + Yv[4] * d1 + Yv[6] * dl + Yv[8] * dm]
    return Y1, Bv


def ric_integrate(r_from, r_to, rho0, drho0, k2, dk2, m, ell, K=24, trackd=True):
    """rigorous integration of (rho, d rho) from r_from to r_to; returns end values and path statistics
    (inf Re rho, sup Re rho, sup |rho| over all step boxes)."""
    r = arb(r_from); rT = arb(r_to); rt = float(rT.mid())
    Y = [acb(rho0), acb(drho0)]
    kap = float(abs(acb(k2)).sqrt().mid())
    st = dict(minRe=None, maxRe=None, maxAbs=arb(0), steps=0)
    sgn = 1 if rt > float(r.mid()) else -1
    final = False
    while not final:
        rf = float(r.mid())
        rem = abs(rt - rf)
        h = min(0.4 / max(kap, 1e-3), rf / 6, rem)          # step-size heuristic only (float is not in the enclosure)
        for _try in range(12):
            # REFEREE-R1-FINAL item 2: the last step is the exact ball h = arb(r_to) - r and it IS integrated
            # (build-1 snapped r to r_to when within 1e-9, leaving a gap of up to 9.3e-15 un-integrated)
            final = (rem - h) < 1e-9
            hA = (rT - r) if final else arb(sgn * h)
            Y1, B = _ric_step(r, Y, hA, k2, dk2, m, ell, K, trackd)
            if Y1 is not None:
                break
            h = h / 2
        else:
            raise RuntimeError('Riccati step failed at r=%g' % rf)
        lo = B[0].real.lower(); hi = B[0].real.upper(); ab = abs(B[0]).upper()
        st['minRe'] = lo if st['minRe'] is None or lo < st['minRe'] else st['minRe']
        st['maxRe'] = hi if st['maxRe'] is None or hi > st['maxRe'] else st['maxRe']
        st['maxAbs'] = amax(st['maxAbs'], ab)
        st['steps'] += 1
        r = rT if final else r + hA
        Y = Y1
    return Y[0], Y[1], st


def series_mv(k2, m, ell, N, sign, R):
    """rho_N(R) for k2 in a ball by the mean-value form: rho_N(k2c) + (d rho_N/d k2)(ball) (k2 - k2c)."""
    k2 = acb(k2)
    k2c = acb(k2.real.mid(), k2.imag.mid())
    t = acb(1 / arb(R))
    c0, _ = riccati_coeffs(k2c, m, ell, N, sign)
    _, dcb = riccati_coeffs(k2, m, ell, N, sign)
    return poly_t(c0, t) + poly_t(dcb, t) * (k2 - k2c)


def channel_full(k2, dk2, m, ell, R1, N, k2_disc=None, gap=None, Rfar=None, trackd=True):
    """decaying / growing Riccati data of one Coulomb channel on [R1, inf):
       far field [Rfar, inf): asymptotic series + contraction (channel());  [R1, Rfar]: rigorous Riccati integration
       (inward for the decaying solution, which is backward-stable; forward for the growing one, forward-stable).
       The growing solution is DEFINED by rho_g(R1) = rho_N^g(R1) (exact, analytic in lam)."""
    if Rfar is None:
        Rfar = max(2.0 * float(arb(R1).mid()), 30.0 * float(arb(m).upper()) / float(abs(acb(k2)).lower()))
    far = channel(k2, m, ell, Rfar, N)
    if not (far['d']['ok'] and far['g']['ok']):
        return dict(ok=False, why='far-field series lemma failed at Rfar=%g' % Rfar)
    ball = acb(arb(0, 1), arb(0, 1))
    epsd_d = arb(0)
    if k2_disc is not None:
        farD = channel(k2_disc, m, ell, Rfar, N)
        if not farD['d']['ok']:
            return dict(ok=False, why='far-field lemma failed on the disc')
        epsd_d = farD['d']['eps'] / gap
    rho0 = series_mv(k2, m, ell, N, 1, Rfar) + far['d']['eps'] * ball
    drho0 = (far['d']['drhoR'] * dk2 + epsd_d * ball) if trackd else acb(0)
    rd, drd, sd = ric_integrate(Rfar, R1, rho0, drho0, k2, dk2, m, ell, trackd=trackd)
    tR1 = acb(1 / arb(R1))
    cg, dcg = riccati_coeffs(k2, m, ell, N, -1)
    g0 = series_mv(k2, m, ell, N, -1, R1); dg0 = (poly_t(dcg, tR1) * dk2) if trackd else acb(0)
    rgF, drgF, sg = ric_integrate(R1, Rfar, g0, dg0, k2, dk2, m, ell, trackd=trackd)
    eta0 = abs(rgF - far['g']['rhoR']).upper()
    c = far['g']['rho_min']; resg = far['g']['res_max']
    epsg = 2 * (eta0 + resg / (2 * c))
    if not (eta0 + (epsg * epsg + resg) / (2 * c) <= epsg and epsg < c):
        return dict(ok=False, why='growing far-field closure failed')
    # item 2: hull ends kept in arb (build-1 passed them through float(), which rounds to nearest, not outward)
    infRe_d = amin(sd['minRe'], (far['d']['rho_min'] - far['d']['eps']).lower())
    supRe_g = amax(sg['maxRe'], (-(c - epsg)).upper())
    if not (infRe_d > 0 and supRe_g < 0):
        return dict(ok=False, why='Riccati sign condition failed (inf Re rho_d=%s, sup Re rho_g=%s)' % (infRe_d, supRe_g))
    gamma = infRe_d - supRe_g
    Pmax = amax(amax(sd['maxAbs'], far['d']['pmax'] + far['d']['eps']), amax(sg['maxAbs'], far['g']['pmax'] + epsg))
    return dict(ok=True, rd=rd, drd=drd, rg=g0, drg=dg0, cd=infRe_d, G=1 / gamma, Pmax=Pmax, Rfar=Rfar,
                eps_far_d=far['d']['eps'], eps_far_g=epsg, steps=(sd['steps'], sg['steps']))


def lemma(mode, lam, E, m, L, R, a1, kappa1, s, N=10, mu_frac='0.5', lam_disc=None, gap=None):
    """certified tail data at R = R1. lam: acb ball (EVANS: lam; KREIN: w). With lam_disc (a complex disc containing
    lam's box, gap = disc radius - box radius) the coupling constants are computed uniformly on the disc and the
    far-field Cauchy bound enters d rho_d / d lam."""
    ell = L * (L + 1)
    lam = acb(lam)
    absE = -E
    def k2s(l):
        l = acb(l)
        if mode == 'evans':
            return acb(absE) - acb(0, 1) * l, acb(absE) + acb(0, 1) * l
        return acb(absE) - l, acb(absE) + l
    dk2p, dk2q = (-acb(0, 1), acb(0, 1)) if mode == 'evans' else (acb(-1), acb(1))
    k2p, k2q = k2s(lam)
    res = dict(ok=False)
    if lam_disc is not None:
        k2pD, k2qD = k2s(lam_disc)
    else:
        k2pD = k2qD = None
    chp = channel_full(k2p, dk2p, m, ell, R, N, k2pD, gap)
    chq = channel_full(k2q, dk2q, m, ell, R, N, k2qD, gap)
    if not (chp['ok'] and chq['ok']):
        res['why'] = 'channel: ' + (chp.get('why') or chq.get('why'))
        return res
    if lam_disc is not None:                        # uniform constants on the disc
        cpD = channel_full(k2pD, dk2p, m, ell, R, N, trackd=False)
        cqD = channel_full(k2qD, dk2q, m, ell, R, N, trackd=False)
        if not (cpD['ok'] and cqD['ok']):
            res['why'] = 'channel on disc: ' + (cpD.get('why') or cqD.get('why'))
            return res
    else:
        cpD, cqD = chp, chq
    R = arb(R)
    cd = amin(cpD['cd'], cqD['cd'])                          # item 2: arb lower ends, no float()
    mu = arb(mu_frac) * amin(cd, kappa1)
    D1 = 4 * abs(arb(s)) * a1 * a1 / (2 * kappa1 * R * R) + 2 * a1 * a1 / (4 * kappa1 * kappa1 * R)
    S1 = (a1 / R) / (kappa1 - mu)
    Gm = amax(cpD['G'], cqD['G'])
    th_pq = Gm * (D1 + 2 * S1)
    th_psi = a1 / ((2 * L + 1) * (kappa1 + mu))
    th = amax(th_pq, th_psi)
    if not th < arb('0.5'):
        res['why'] = 'coupling contraction failed (theta=%s)' % th
        return res
    eX = th / (1 - th)
    Pm = amax(cpD['Pmax'], cqD['Pmax'])
    eXp = Pm * Gm * (D1 + 2 * S1) / (1 - th)
    ePsi_p = (arb(L + 1) / (2 * L + 1)) * (a1 / R) / (kappa1 + mu) / (1 - th)
    e_val = eX; e_der = amax(eXp, ePsi_p)
    # channel directions at R: v_d = (1, -rho_d), v_g = (1, -rho_g); psi: rho_d = L/R, rho_g = -(L+1)/R
    # rho_d(R1) is enclosed directly (inward Riccati integration); rho_g(R1) is the exact defining value
    rd = [chp['rd'], chq['rd'], acb(arb(L) / R)]
    rg = [chp['rg'], chq['rg'], acb(-arb(L + 1) / R)]
    if lam_disc is not None:
        rdD = [cpD['rd'], cqD['rd'], acb(arb(L) / R)]
        rgD = [cpD['rg'], cqD['rg'], acb(-arb(L + 1) / R)]
    else:
        rdD, rgD = rd, rg
    epsd = [arb(0), arb(0), arb(0)]
    epsg = [arb(0), arb(0), arb(0)]
    rdB = rdD
    rgB = rgD
    # errors e (values), e' (derivatives) in channel i for every vector: |e| <= e_val, |e'| <= e_der (plus, for the
    # model vector itself, the Riccati eps in its own derivative: absorbed below in rdB)
    dPmax = arb(0); Tmax = arb(0)
    for i in range(3):
        den = (rdB[i] - rgB[i])
        dP = (e_der + abs(rgB[i]).upper() * e_val) / abs(den).lower()
        tt = (e_der + abs(rdB[i]).upper() * e_val) / abs(den).lower()
        dPmax = amax(dPmax, dP)
        Tmax = amax(Tmax, tt)
    if not 3 * dPmax < arb('0.5'):
        res['why'] = 'renormalisation failed'
        return res
    Tt = 3 * Tmax / (1 - 3 * dPmax)          # |t~_ij| <= Tt
    Ainv_norm = 1 / (1 - 3 * dPmax)          # ||A^-1||_inf
    res.update(dict(ok=True, mu=mu, theta=th, eX=eX, e_der=e_der, Tt=Tt, Ainv=Ainv_norm, rd=rd, rg=rg, rdB=rdB, rgB=rgB,
                    epsd=epsd, epsg=epsg, D1=D1, S1=S1, G=Gm, dk2=(dk2p, dk2q),
                    drd=([chp['drd'], chq['drd'], acb(0)] if lam_disc is not None else None), drg=[chp['drg'], chq['drg'], acb(0)],
                    Rfar=(chp['Rfar'], chq['Rfar']), eps_far=(chp['eps_far_d'], chq['eps_far_d'])))
    return res


def vectors(mode, T, Tdisc=None, cauchy_r=None, box_r=None, deriv=False, real=False):
    """renormalised decaying basis at R, split as  X~_j = Xhat_j + sum_i t~_ij G_i  with |t~_ij| <= Tt:
       Xhat_j: channel j data (1, -rho_d_j(R)) (rho_d = rho_N + eta, |eta| <= eps_d), zero in the other channels;
       G_i:    channel i data (1, -rho_g_i(R)) exactly (the growing Riccati solution is chosen with eta_g(R) = 0).
    The G_i are integrated as their own columns (they decay inward), so the t~ uncertainty never multiplies an
    inward-growing direction.  T: lemma on the Krawczyk box (explicit parts); Tdisc: lemma on the Cauchy disc.
    Returns (Xhat, G, dXhat, dG, Tt, dTt) in (a, c|d, psi, a', c'|d', psi') coordinates."""
    ball = acb(arb(0, 1), arb(0, 1))
    TT = Tdisc or T
    Tt = TT['Tt']
    epsd = TT['epsd']
    gap = (arb(cauchy_r) - arb(box_r)) if deriv else None
    Xh, G, dXh, dG = [], [], [], []
    z = (acb(0), acb(0))
    for j in range(3):
        ch = [z, z, z]
        ch[j] = (acb(1), -(T['rd'][j] + epsd[j] * ball))
        Xh.append(_to_acd(mode, ch, real))
        ch = [z, z, z]
        ch[j] = (acb(1), -T['rg'][j])
        G.append(_to_acd(mode, ch, real))
        if deriv:
            ch = [z, z, z]
            ch[j] = (acb(0), -(T['drd'][j] + (epsd[j] / gap) * ball))
            dXh.append(_to_acd(mode, ch, real))
            ch = [z, z, z]
            ch[j] = (acb(0), -T['drg'][j])
            dG.append(_to_acd(mode, ch, real))
    dTt = (Tt / gap) if deriv else None
    return Xh, G, dXh, dG, Tt, dTt


def _to_acd(mode, ch, real):
    """channel coordinates (p|P, q|Q, psi, derivatives): the linear system is integrated in the tail-diagonal basis."""
    (p, pp), (q, qp), (s_, sp) = ch
    v = [p, q, s_, pp, qp, sp]
    if real:
        v = [x.real for x in v]
    return v
