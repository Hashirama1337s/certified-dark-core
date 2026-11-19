"""bg_tube.py - certified tube for a GPP background state (2402.07998 eqs. 32a-32b, a = r sigma).

    sigma'' + 2 sigma'/r = (s sigma^2 - u) sigma ,   u'' + 2 u'/r = -sigma^2 ,   sigma(0)=sigma0, u(0)=u0, regular.
    s = +1 repulsive, 0 Schroedinger-Poisson, -1 attractive.

Certificate (s >= 0; for s = -1 the existence step is NOT certified, calibration only):
  1. Series start on [0, r0] with a Volterra contraction remainder (rigorous ball at r0).
  2. Two point trajectories u_lo < u_hi, certified by interval Taylor integration:
       one ESCAPES  (exactly n zeros so far, then a*(-1)^n*sign(sigma0) < 0, a' of the same sign, u < 0), and
       the other has n+1 zeros.  Both sets are open and disjoint (escape is permanent: once u<0 and s>=0,
       a'' = (s sigma^2 - u) a pushes a away from 0), so some u0* in between is in neither.
  3. Tube: the interval u0 = [u_lo, u_hi] integrated to R1. It shows exactly n zeros, a of fixed sign on
     (last node, R1], u(R1) < 0. For the u0* of step 2 the solution is global, never escapes and so, for
     r >= R1, a' has the sign opposite to a, |a| decreases, and with kappa1^2 = -u(R1) <= s sigma^2 - u:
          |a(r)| <= |a(R1)| exp(-kappa1 (r - R1)),   |a'(r)| <= (Vmax/kappa1) |a(r)|.
  4. E, m, u0-E, T, F, the virial residual: tube quadratures + closed-form tail bounds.
Every solution inside the tube is covered, so every later certificate holds for all of them.
"""
import sys, os, json, time, math, hashlib
from flint import arb, ctx
import itaylor as it

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'cache')


def A(x):
    return arb(x)


# ------------------------------------------------------------------ float guess (not part of the proof)
def float_u0(s, n, sig0):
    import numpy as np
    from scipy.integrate import solve_ivp

    def rhs(r, y):
        sg, dsg, u, du = y
        return [dsg, (s * sg * sg - u) * sg - 2 * dsg / r, du, -sg * sg - 2 * du / r]

    def cls(u0):
        r0 = 1e-6
        y0 = [sig0, 0.0, u0, 0.0]
        ev0 = lambda r, y: y[0]
        evb = lambda r, y: abs(y[0]) - 3 * abs(sig0) - 1
        evb.terminal = True
        sol = solve_ivp(rhs, (r0, 300), y0, rtol=1e-11, atol=1e-13, events=(ev0, evb), max_step=0.05)
        return 1 if len(sol.t_events[0]) > n else -1

    u = 1e-3
    lo = None
    while cls(u) == -1:
        lo = u
        u *= 1.15
        if u > 1e4:
            raise RuntimeError('no bracket')
    hi = u
    lo = lo if lo is not None else -abs(hi)
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if cls(m) == 1:
            hi = m
        else:
            lo = m
    return 0.5 * (lo + hi)


# ------------------------------------------------------------------ series start on [0, r0]
def series_start(s, sig0, u0, r0, N=12):
    """rigorous enclosure of the state at r0 (and crude bounds on [0, r0]).
    sigma = sum S_j r^(2j), u = sum U_j r^(2j); remainder from the Volterra map V[g](r) = int_0^r t^-2 int_0^t x^2 g."""
    s = A(s)
    sg0 = it.exact(sig0)                      # sigma0 as the exact rational (1.80 -> 9/5), not the double
    S = [sg0]; U = [u0]
    def coeff_f(Sl, Ul, j):  # coefficient of r^(2j) of (s sigma^2 - u) sigma and of sigma^2
        S2 = sum((Sl[i] * Sl[j - i] for i in range(j + 1)), A(0))
        S2l = [sum((Sl[i] * Sl[k - i] for i in range(k + 1)), A(0)) for k in range(j + 1)]
        S3 = sum((S2l[i] * Sl[j - i] for i in range(j + 1)), A(0))
        US = sum((Ul[i] * Sl[j - i] for i in range(j + 1)), A(0))
        return s * S3 - US, S2
    for j in range(N):
        fs, f2 = coeff_f(S, U, j)
        d = A((2 * j + 2) * (2 * j + 3))
        S.append(fs / d); U.append(-f2 / d)
    # high-order part H = V[f(p)] - p (terms of degree > 2N): bound sup over [0,r0] crudely by summing
    # the polynomial f(p) coefficients above degree 2N-2 (computed exactly up to degree 6N).
    Sp = S + [A(0)] * (3 * N + 3); Up = U + [A(0)] * (3 * N + 3)
    Hs = A(0); Hu = A(0); Hsd = A(0); Hud = A(0)
    rr = A(r0)
    for j in range(N, 3 * N + 2):
        fs, f2 = coeff_f(Sp, Up, j)
        d = A((2 * j + 2) * (2 * j + 3))
        Hs += abs(fs / d) * rr ** (2 * j + 2); Hu += abs(f2 / d) * rr ** (2 * j + 2)
        Hsd += abs(fs / d) * (2 * j + 2) * rr ** (2 * j + 1); Hud += abs(f2 / d) * (2 * j + 2) * rr ** (2 * j + 1)
    # Lipschitz bound of (f_sigma, f_u) on the ball |sigma - sigma0| <= 1, |u - u0| <= 1 (max norm)
    sg = abs(sg0) + 1; ua = abs(u0) + 1
    Lip = abs(s) * 3 * sg * sg + ua + sg + 2 * sg
    q = rr * rr * Lip / 6
    assert q < A('0.5')
    eps = max(Hs, Hu) / (1 - q) * 2
    epsd = rr * Lip / 3 * eps + max(Hsd, Hud) * 2
    pv = lambda C, x: sum((C[j] * x ** (2 * j) for j in range(len(C))), A(0))
    pd = lambda C, x: sum((C[j] * (2 * j) * x ** (2 * j - 1) for j in range(1, len(C))), A(0))
    ball = arb(0, 1)
    sig = pv(S, rr) + eps * ball; sgd = pd(S, rr) + epsd * ball
    u = pv(U, rr) + eps * ball; ud = pd(U, rr) + epsd * ball
    # quadratures over [0, r0]: crude enclosures
    smax = abs(sg0) + 1
    QT = (A(0) + ball) * 0 + (sgd.abs_upper() ** 2) * rr ** 3 / 3 * (1 + ball) / 2 + 0 * ball
    QT = arb(0) + (sgd.abs_upper() ** 2 * rr ** 3 / 3) * (arb(1) + ball) / 2
    QF = (smax ** 4 * rr ** 3 / 3) * (arb(1) + ball) / 2
    QU = (smax ** 2 * ua * rr ** 3 / 3) * ball
    crude = dict(sig=sg0 + (abs(sig - sg0).abs_upper() + eps) * ball, u=u0 + (abs(u - u0).abs_upper() + eps) * ball)
    return [sig, sgd, u, ud, QT, QF, QU], crude, eps


_MARGIN_OK = {}


def assert_start_margins(s, sig0, u0, r0, sg, ua=None):
    """REFEREE-R1-FINAL item 3: the crude bounds |sigma| <= sg and |u| <= ua on [0, r0] used by bracket.qbound,
    bracket.gnorms and match.frob_start (sg = |sigma0| + 0.01, ua = |u0| + 0.01) are CHECKED here against the
    series_start crude enclosure; a violation raises (fails loudly)."""
    key = (s, repr(sig0), arb(u0).str(30, radius=True), arb(r0).str(30, radius=True), sg.str(30, radius=True),
           None if ua is None else ua.str(30, radius=True))
    if key in _MARGIN_OK:
        return
    _, crude, _ = series_start(s, sig0, u0, r0)
    if not bool(abs(crude['sig']) < sg):
        raise AssertionError('0.01 margin violated: sup|sigma| on [0, r0] = %s not < %s' % (crude['sig'], sg))
    if ua is not None and not bool(abs(crude['u']) < ua):
        raise AssertionError('0.01 margin violated: sup|u| on [0, r0] = %s not < %s' % (crude['u'], ua))
    _MARGIN_OK[key] = True


# ------------------------------------------------------------------ integration drivers
def integrate(s, n, sig0, u0, r0, Rmax, K, tol, mode, log=None, hmax=0.25):
    """mode 'classify' (point u0): run until escape or n+1 zeros certified. mode 'tube': run to Rmax and store steps."""
    Y, crude, eps0 = series_start(s, sig0, u0, r0)
    r = A(r0)
    steps = []
    zeros = 0
    sign_prev = 1 if sig0 > 0 else -1     # sign of sigma on (0, first node)
    exp_sign = sign_prev
    pending_zero = False
    nsteps = 0
    while True:
        J = it.bg_jets(s, r, [arb(y.mid()) for y in Y], K)
        h = it.suggest_h(J, K, tol, min(hmax, float((r / 14).mid())))
        if mode == 'tube' and float((r + h).mid()) > Rmax:
            h = float((A(Rmax) - r).mid())
            hA = A(Rmax) - r
        else:
            hA = A(h)
        Y1, B, J0 = it.bg_step(s, r, Y, hA, K)
        # zero bookkeeping for sigma over the step
        # (sigma has no zero on the step if its step box excludes 0; otherwise sigma' must exclude 0 on the box,
        #  so sigma is monotone there and has exactly one zero iff the certified endpoint signs differ)
        if B[0].contains(0):
            if B[1].contains(0):
                if mode == 'classify' and zeros > n:
                    return dict(result='zeros', r=float(r.mid()), zeros=zeros, steps=nsteps)
                if mode == 'classify':
                    return dict(result='undecided', r=float(r.mid()), zeros=zeros, steps=nsteps, width=float(Y[0].rad()))
                raise RuntimeError('zero count inconclusive at r=%s' % r.mid())
            if Y[0].contains(0) or Y1[0].contains(0):
                raise RuntimeError('sigma endpoint contains 0 near r=%s' % (r + hA).mid())
            if (Y[0] > 0) != (Y1[0] > 0):
                zeros += 1
        steps.append(dict(r=r, h=hA, Y=Y, B=B))
        r = r + hA
        Y = Y1
        nsteps += 1
        a = r * Y[0]
        ap = Y[0] + r * Y[1]
        if mode == 'classify':
            if zeros > n:
                return dict(result='zeros', r=float(r.mid()), zeros=zeros, steps=nsteps)
            sgn_n = exp_sign * (-1) ** n
            if zeros == n and Y[2] < 0 and s >= 0:
                if (sgn_n > 0 and a > 0 and ap > 0) or (sgn_n < 0 and a < 0 and ap < 0):
                    return dict(result='escape', r=float(r.mid()), zeros=zeros, steps=nsteps)
            if float(r.mid()) > Rmax:
                return dict(result='undecided', r=float(r.mid()), zeros=zeros, steps=nsteps,
                            width=float(Y[0].rad()))
        else:
            if log and nsteps % 50 == 0:
                log('  r=%.3f h=%.4f width(sigma)=%.2e sigma=%.3e' % (float(r.mid()), float(hA.mid()), float(Y[0].rad()), float(Y[0].mid())))
            if float(r.mid()) >= Rmax - 1e-12:
                return dict(steps=steps, Y=Y, r=r, zeros=zeros, crude=crude, eps0=eps0)


def float_traj_g(s, n, sig0, u0, r0, Rstar, K):
    """non-rigorous midpoint trajectory (arb midpoints): returns (a, a') at Rstar."""
    Y, _, _ = series_start(s, sig0, u0, r0)
    Y = [arb(y.mid()) for y in Y]
    r = A(r0)
    while float(r.mid()) < Rstar:
        J = it.bg_jets(s, r, Y, K)
        h = it.suggest_h(J, K, 1e-70, min(0.25, float((r / 4).mid())))
        if float(r.mid()) + h > Rstar:
            h = Rstar - float(r.mid())
        hA = A(h)
        Y = [arb(it.horner(J[i], hA).mid()) for i in range(it.NB)]
        r = r + hA
        if abs(float(Y[0].mid())) > 10 * abs(sig0) + 10:
            break
    return float(r.mid()), r * Y[0], Y[0] + r * Y[1]


def kap_guess(s, n, sig0, u0f, r0, K):
    """sqrt(-E) and turning radius m/|E| from a midpoint trajectory (E ~ u + r u'); heuristic. The radius is pushed
    out to 2.5 x the turning radius so that the estimate is taken outside the core."""
    Rg = 10.0
    for _ in range(3):
        Y, _, _ = series_start(s, sig0, A(u0f), r0)
        Y = [arb(y.mid()) for y in Y]
        r = A(r0)
        while float(r.mid()) < Rg:
            J = it.bg_jets(s, r, Y, K)
            h = it.suggest_h(J, K, 1e-40, min(0.25, float((r / 4).mid())))
            hA = A(h)
            Y = [arb(it.horner(J[i], hA).mid()) for i in range(it.NB)]
            r = r + hA
        E = float((Y[2] + r * Y[3]).mid())
        kap = math.sqrt(max(1e-4, -E)); mm = float((-r * r * Y[3]).mid())
        rt = max(1.0, mm / max(1e-4, -E))
        if 2.5 * rt <= Rg:
            break
        Rg = 2.5 * rt
    return kap, rt


def refine_u0(s, n, sig0, u0f, r0, K, kap, rt, target=1e-65, log=print):
    """staged secant on the growing-mode amplitude g = a' + kap a at increasing radii (heuristic; not a proof).
    The decaying solution biases the root by ~exp(-2 kap R*), so R* grows until that is below target."""
    u = A(u0f)
    err = 1e-10
    while True:
        Rstar = rt + math.log(1e-2 / err) / kap
        def g(x):
            rr, a, ap = float_traj_g(s, n, sig0, x, r0, Rstar, K)
            return ap + A(kap) * a if rr >= Rstar - 1e-9 else None
        du = A(err / 10)
        steps = []
        for _ in range(3):
            g0 = g(u); g1 = g(u + du)
            if g0 is None or g1 is None or (g1 - g0) == 0:
                raise RuntimeError('refine: left the linear regime at R*=%.2f' % Rstar)
            step = arb((-g0 * du / (g1 - g0)).mid())
            if abs(float(step.mid())) > 1e3 * err:
                raise RuntimeError('refine: step %.3e exceeds the error budget %.1e' % (float(step.mid()), err))
            u = u + step
            steps.append(float(step.mid()))
            du = A(max(abs(steps[-1]), err * 1e-6) / 10)
        err = max(1e4 * math.exp(-2 * kap * (Rstar - rt)), 10 * abs(steps[-1]), 10.0 ** (-ctx.prec * 0.28))
        log('  refine R*=%.1f u0=%s steps %s err %.1e' % (Rstar, u.mid().str(45, radius=False), ['%.1e' % x for x in steps], err))
        if err < target:
            return u


def tube(s, n, sig0, R1, prec=320, K=56, tol=1e-75, r0=1e-5, delta_exp=None, log=print):
    it.set_prec(prec)
    t0 = time.time()
    u0f = float_u0(s, n, sig0)
    log('float u0 = %.15g' % u0f)
    kap, rt = kap_guess(s, n, sig0, u0f, r0, K)
    log('kappa guess %.5f turning radius %.2f' % (kap, rt))
    u = refine_u0(s, n, sig0, u0f, r0, K, kap, rt, target=10.0 ** (-(delta_exp or 50) - 12), log=log)
    dex = delta_exp if delta_exp is not None else 50
    d = A(10) ** (-dex)
    out = {}
    for lab, uu in (('lo', u - d), ('hi', u + d)):
        c = integrate(s, n, sig0, uu, r0, 400.0, K, tol, 'classify')
        out[lab] = c
        log('  classify %s: %s' % (lab, c))
    kinds = {out['lo']['result'], out['hi']['result']}
    certified = (kinds == {'escape', 'zeros'}) and s >= 0
    U0 = (u - d).union(u + d)
    tb = integrate(s, n, sig0, U0, r0, R1, K, tol, 'tube', log=log)
    info = finish(s, n, sig0, U0, tb, R1)
    info.update(dict(classify=out, existence_certified=bool(certified), u_mid=u.mid().str(60, radius=False),
                     delta=float(d.mid()), prec=prec, K=K, r0=r0, seconds=time.time() - t0))
    return tb, info


def finish(s, n, sig0, U0, tb, R1):
    Y = tb['Y']; r = tb['r']
    sig, sp, u, up, QT, QF, QU = Y
    a1 = abs(r * sig).abs_upper()       # |a(R1)|
    a = r * sig; ap = sig + r * sp
    sgn_n = (1 if sig0 > 0 else -1) * (-1) ** n
    ok_sign = (a > 0) if sgn_n > 0 else (a < 0)
    ok_u = bool(u < 0)
    kap2 = -u
    if s < 0:
        kap2 = -u - (a1 / r) ** 2
    kap1 = kap2.sqrt() if kap2 > 0 else None
    res = dict(zeros=tb['zeros'], a_sign_ok=bool(ok_sign), u_R1_negative=ok_u, R1=float(r.mid()))
    if kap1 is None:
        res['tail_ok'] = False
        return res
    kap1 = arb(kap1.lower())
    ball = arb(0, 1)
    m_in = -r * r * up
    tail_m = a1 ** 2 / (2 * kap1)
    tail_I = a1 ** 2 / (2 * kap1 * r)
    m = m_in + tail_m * (1 + ball) / 2
    I_in = U0 - u - r * up
    I1 = I_in + tail_I * (1 + ball) / 2
    E = U0 - I1
    negE_up = (-u + m.upper() / r)
    Vmax = arb(abs(s)) * (a1 / r) ** 2 + negE_up
    dfac = Vmax / kap1 + 1 / r
    tail_T = dfac ** 2 * a1 ** 2 / (2 * kap1)
    tail_F = a1 ** 4 / (r * r * 4 * kap1)
    Eabs = abs(E).upper().union(abs(u).upper())
    tail_QU = arb(Eabs.upper()) * tail_m
    T = 2 * arb.pi() * (QT + tail_T * (1 + ball) / 2)
    F = arb.pi() * (QF + tail_F * (1 + ball) / 2)
    QUt = QU + tail_QU * ball
    D = -arb.pi() * (E * m - QUt)
    vir = D - (2 * T + 3 * arb(s) * F)
    res.update(dict(tail_ok=bool(ok_sign and ok_u), kappa1=kap1, a1=a1, E=E, m=m, N=4 * arb.pi() * m, I1=I1,
                    u0=U0, T=T, F=F, D=D, virial=vir, virial_rel=abs(vir) / abs(D),
                    sigma_R1=sig, up_R1=up, u_R1=u))
    return res


def s_(x, d=12):
    if isinstance(x, arb):
        return x.str(d, radius=True)
    return x


def ser(x):
    """lossless-enough serialisation of a ball: decimal midpoint (n digits) and an upward radius that also covers the
    midpoint rounding. (arb.str(radius=True) can drop the midpoint of a wide ball, which is valid but useless.)"""
    n = int(ctx.prec * 0.31) + 5
    m = x.mid()
    r = x.rad() + abs(m) * arb(10) ** (-(n - 3)) + arb(2) ** (-ctx.prec)
    return 'B|' + m.str(n, radius=False) + '|' + arb(r.upper()).str(8, radius=False, more=False)


def deser(sx):
    if isinstance(sx, str) and sx.startswith('B|'):
        _, m, r = sx.split('|')
        rr = arb(r)
        rr = rr * (1 + arb(10) ** -6)          # the 8-digit radius string is rounded: inflate by 1e-6 relative
        return arb(m) + arb(0, 1) * rr
    return arb(sx)


DISK_CACHE = True     # assemble.py sets this False for every target job: the tube is rebuilt inside the run
_MEM = {}             # in-process memo: key -> (blob bytes, source); one build per process


def get_tube(s, n, sig0, R1, prec=320, K=56, tol=1e-75, delta_exp=50, log=print, use_cache=None):
    """build (or, for controls, load from the disk cache) and return (steps, info, Yend).
    REFEREE-R1-FINAL item 5: no pickle. The tube is stored as a JSON document of ser() strings (decimal midpoint +
    outward radius; arb objects are never pickled). Every caller, cached or not, decodes the same JSON blob, and
    info['tube_sha256'] = sha256 of that blob is written into each output, so the tube behind every number is pinned.
    With use_cache False (all target jobs) the disk cache is neither read nor written: the tube is built in-run."""
    if use_cache is None:
        use_cache = DISK_CACHE
    key = 's%+d_n%d_sig%s_R%s_p%d_K%d_d%d_r0e-5_v5' % (s, n, repr(sig0), repr(R1), prec, K, delta_exp)
    mkey = (key, bool(use_cache))
    fn = os.path.join(CACHE, key + '.json')
    it.set_prec(prec)
    if mkey in _MEM:
        blob, src = _MEM[mkey]
    elif use_cache and os.path.exists(fn):
        with open(fn, 'rb') as f:
            blob = f.read()
        src = 'disk cache ' + os.path.basename(fn)
    else:
        tb, info = tube(s, n, sig0, R1, prec=prec, K=K, tol=tol, delta_exp=delta_exp, log=log)
        info = dict(info)
        build_s = info.pop('seconds', None)          # wall time is not part of the tube (keeps the sha reproducible)
        S = ser
        D = dict(steps=[dict(r=S(st['r']), h=S(st['h']), Y=[S(y) for y in st['Y']], B=[S(y) for y in st['B']]) for st in tb['steps']],
                 info={k: (S(v) if isinstance(v, arb) else v) for k, v in info.items()},
                 Yend=[S(y) for y in tb['Y']])
        blob = json.dumps(D, sort_keys=True, default=str).encode('utf-8')
        src = 'built in this run (%.0f s)' % (build_s or 0)
        if use_cache:
            os.makedirs(CACHE, exist_ok=True)
            with open(fn, 'wb') as f:
                f.write(blob)
    _MEM[mkey] = (blob, src)
    it.set_prec(prec)
    D = json.loads(blob.decode('utf-8'))
    P = deser
    steps = [dict(r=P(st['r']), h=P(st['h']), Y=[P(y) for y in st['Y']], B=[P(y) for y in st['B']]) for st in D['steps']]
    info = {k: (P(v) if isinstance(v, str) and (v.startswith('[') or v.startswith('B|')) else v) for k, v in D['info'].items()}
    Yend = [P(y) for y in D['Yend']]
    info['tube_sha256'] = hashlib.sha256(blob).hexdigest()
    info['tube_source'] = src
    return steps, info, Yend


if __name__ == '__main__':
    s = int(sys.argv[1]); n = int(sys.argv[2]); sig0 = float(sys.argv[3]); R1 = float(sys.argv[4])
    outp = sys.argv[5]
    prec = int(sys.argv[6]) if len(sys.argv) > 6 else 320
    dex = int(sys.argv[7]) if len(sys.argv) > 7 else 50
    t0 = time.time()
    steps, info, Yend = get_tube(s, n, sig0, R1, prec=prec, delta_exp=dex, use_cache=False)   # in-run, no cache
    out = {k: s_(v) for k, v in info.items()}
    print('tube_sha256', info['tube_sha256'])
    out['nsteps'] = len(steps)
    out['wall'] = time.time() - t0
    for k in ('E', 'm', 'T', 'F', 'D', 'virial', 'virial_rel', 'u0', 'kappa1', 'a1'):
        if k in info:
            print(k, s_(info[k]))
    print('zeros', info.get('zeros'), 'tail_ok', info.get('tail_ok'), 'existence_certified', info.get('existence_certified'))
    json.dump(out, open(outp, 'w'), indent=1, default=str)
    print('wall', out['wall'])
