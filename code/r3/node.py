"""node.py - build-W node certificate (R3-WINDOW): certified tube (bg_tube, unchanged) + R1 brackets (bracket.run,
unchanged) + GREEN summary (alpha, c, ||G_a||_{FF->X}, tau checks) + certified 3-channel Krein counts.

Jobs (called by assemble_w.py):
  node(tag)        tube (built in-run, blob saved with its sha256), brackets at R = 10, 14, GREEN, Krein counts at
                   w = 0 and around the frequencies (when known), timings.
  xk(tag)          control XK at a G9 node: counts (upper at +lev, lower at -lev) at w- -+ 0.002, w+ -+ 0.002 per L
                   against build-3/out/<tag>/K<L>.json; kernel booked at w = 0: (upper, lower) = (4,3), (3,2), (2,2).
  xu(tag, L)       control XU at an unstable node: certified counts on the grid w = 0.01 j in (0, w_max); no pair
                   w1 < w2 with lower(w1) - upper(w2) >= 1 in the named sector.
"""
import sys, os, json, time, hashlib
from fractions import Fraction
from flint import arb
import itaylor as it
import bg_tube as bt
import bracket as br
import hw3
import green as gr

HERE = os.path.dirname(os.path.abspath(__file__))
B3OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'build-3', 'out')
OUT = os.path.join(HERE, 'out')

G9 = {'lo-s': '1597/1000', 'g165': '33/20', 'g170': '17/10', 'g175': '7/4', 'r1': '9/5', 'g185': '37/20',
      'g190': '19/10', 'g195': '39/20', 'hi-s': '1983/1000'}
UNSTABLE = {'lo-u': ('1595/1000', 0), 'hi-u': ('1985/1000', 2)}
XK_PATTERN = {0: (4, 3, 4), 1: (3, 2, 3), 2: (2, 1, 2)}      # N below w-, inside (w-, w+), above w+
XK_W0 = {0: (4, 3), 1: (3, 2), 2: (2, 2)}                    # (upper, lower) at w = 0 (kernel booked)


def label(sig0_str):
    x = float(Fraction(sig0_str))
    assert Fraction(repr(x)) == Fraction(sig0_str), 'float label must read back as the exact rational'
    return x


def tube(sig0_str, use_cache=False, log=print):
    """the certified point tube (bg_tube unchanged; R1 = 26, prec 320, K 56, d = 1e-50)."""
    bt.DISK_CACHE = use_cache
    return bt.get_tube(1, 1, label(sig0_str), 26.0, log=log, use_cache=use_cache)


def save_tube(tag, sig0_str):
    """write the exact JSON blob of the tube (as get_tube serialised it) next to the node output; return its sha."""
    x = label(sig0_str)
    key = 's%+d_n%d_sig%s_R%s_p%d_K%d_d%d_r0e-5_v5' % (1, 1, repr(x), repr(26.0), 320, 56, 50)
    blob = None
    for (k, uc), (b, src) in bt._MEM.items():
        if k == key:
            blob = b
    assert blob is not None
    d = os.path.join(OUT, tag); os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'tube.json'), 'wb') as f:
        f.write(blob)
    return hashlib.sha256(blob).hexdigest()


def load_tube(tag, sha_expected):
    """read a node's saved tube blob and decode it exactly as bg_tube.get_tube does; the sha must match."""
    fn = os.path.join(OUT, tag, 'tube.json')
    with open(fn, 'rb') as f:
        blob = f.read()
    sha = hashlib.sha256(blob).hexdigest()
    assert sha == sha_expected, 'tube blob sha mismatch for %s' % tag
    it.set_prec(320)
    D = json.loads(blob.decode('utf-8'))
    P = bt.deser
    steps = [dict(r=P(st['r']), h=P(st['h']), Y=[P(y) for y in st['Y']], B=[P(y) for y in st['B']]) for st in D['steps']]
    info = {k: (P(v) if isinstance(v, str) and (v.startswith('[') or v.startswith('B|')) else v) for k, v in D['info'].items()}
    Yend = [P(y) for y in D['Yend']]
    info['tube_sha256'] = sha; info['tube_source'] = 'node blob ' + tag
    return steps, info, Yend


def counts_at(bj, steps, info, sig0, L, w, lev, R, K=24):
    r0 = steps[0]['r']
    dl = hw3.delta_L(steps, info, bj, R, L)
    ext = hw3.ext_margin(info, R, dl, w, lev)
    up_ = hw3.count(bj, 1, sig0, info, L, it.exact(w), it.exact(lev), 'N', R, dl, K, r0, 'lo')
    lo_ = hw3.count(bj, 1, sig0, info, L, it.exact(w), -it.exact(lev), 'D', R, arb(0), K, r0, 'hi')
    return dict(w=w, lev=lev, upper=up_['count'] if (up_['ok'] and bool(ext > 0)) else None, lower=lo_['count'],
                ext=ext.str(5), why=(up_.get('why'), lo_.get('why')))


def xk(tag, use_cache=False, log=print):
    """control XK at the G9 node tag."""
    t0 = time.time()
    s0 = G9[tag]; x = label(s0)
    steps, info, Yend = tube(s0, use_cache, log=lambda *a: None)
    t_tube = time.time() - t0
    bj = hw3.setup(steps, Yend, 24)
    R = 20.0            # L = 0 near w+: the Neumann cut at R = 14 moves the crossing (FD and certified: w+ -> 1.199 at 7/4); R = 20 matches
    rows = []; ok = True
    for L in (0, 1, 2):
        K = json.load(open(os.path.join(B3OUT, tag, 'K%d.json' % L)))
        wm = K['neg']['w_mid']; wp = K['pos']['w_mid']
        pts = [(0.0, 1e-3)] + [(float(repr(round(w, 6))), 1e-5) for w in (wm - 0.002, wm + 0.002, wp - 0.002, wp + 0.002)]
        cs = [counts_at(bj, steps, info, x, L, w, lev, R) for (w, lev) in pts]
        pat = XK_PATTERN[L]
        c0 = cs[0]
        w0_ok = (c0['upper'], c0['lower']) == XK_W0[L]
        eq = all(c['upper'] is not None and c['upper'] == c['lower'] for c in cs[1:])
        seq = [cs[1]['upper'], cs[2]['upper'], cs[3]['upper'], cs[4]['upper']]
        pat_ok = eq and seq == [pat[0], pat[1], pat[1], pat[2]]
        drop = eq and (cs[1]['lower'] - cs[2]['upper'] == 1)
        rise = eq and (cs[4]['lower'] - cs[3]['upper'] == 1)
        rows.append(dict(L=L, w_minus=wm, w_plus=wp, w0=c0, counts=cs[1:], w0_booked_ok=w0_ok, lower_eq_upper=eq,
                         pattern_ok=pat_ok, drop_exactly_1=drop, rise_exactly_1=rise,
                         neg_sign=K['neg']['krein_sign'], pos_sign=K['pos']['krein_sign']))
        ok = ok and w0_ok and pat_ok and drop and rise
        log('  XK %s L%d: w0 %s/%s  counts %s  drop %s rise %s' % (tag, L, c0['upper'], c0['lower'],
                                                                   [(c['upper'], c['lower']) for c in cs[1:]], drop, rise))
    return dict(job='XK:' + tag, sig0=s0, R=R, tube_sha256=info['tube_sha256'], tube_source=info['tube_source'],
                rows=rows, PASS=bool(ok), tube_seconds=t_tube, seconds=time.time() - t0)


def xu(tag, wstep='0.01', use_cache=False, log=print, Ls=None, jlo=None, jhi=None):
    """control XU at an unstable node: certified count scan in the named sector, and the designed drop in the others.
    jlo, jhi (optional): scan only the grid points w = wstep j, jlo <= j <= jhi (a PART; the other sectors are checked
    only in the part with jlo = 1). Parts are merged by verdict_w.xu_merge, which re-applies the pair rule to the
    union and requires the parts to cover j = 1 .. jmax exactly."""
    import numpy as np
    import cell
    t0 = time.time()
    s0, Ln = UNSTABLE[tag]; x = label(s0)
    steps, info, Yend = tube(s0, use_cache, log=lambda *a: None)
    bj = hw3.setup(steps, Yend, 24)
    R = 20.0
    dl = hw3.delta_L(steps, info, bj, R, Ln)
    wmax = float((-info['E'] - info['m'] / arb(R) - dl - arb('1e-5')).lower())
    ws = Fraction(wstep)
    grid = []
    j = 1
    while float(ws * j) < wmax - 1e-9:
        grid.append(float(ws * j)); j += 1
    jmax = len(grid)
    part = jlo is not None
    if part:
        jhi = min(jhi, jmax)
        grid = grid[jlo - 1:jhi]
    res = dict(job='XU:' + tag, sig0=s0, named_L=Ln, R=R, tube_sha256=info['tube_sha256'], wmax=wmax, grid_step=wstep,
               jmax=jmax, jlo=jlo if part else 1, jhi=jhi if part else jmax)
    scan = []
    for w in grid:
        c = counts_at(bj, steps, info, x, Ln, w, 1e-5, R)
        scan.append((w, c['upper'], c['lower']))
    # no pair w1 < w2 with lower(w1) - upper(w2) >= 1  (an undecided count is reported, never counted as a pass)
    undecided = [s for s in scan if s[1] is None or s[2] is None]
    found = []
    for i, (w1, u1, l1) in enumerate(scan):
        for (w2, u2, l2) in scan[i + 1:]:
            if l1 is not None and u2 is not None and l1 - u2 >= 1:
                found.append((w1, w2, l1, u2))
    res.update(scan=scan, undecided=len(undecided), drop_pairs=found[:10], n_drop_pairs=len(found))
    # other sectors: the designed drop must be certified (float pre-pass picks w1, w2)
    others = {}
    if part and jlo != 1:
        res['other_sectors'] = None
        res['PASS'] = None
        res['outcome'] = 'part (merged by verdict_w)'
        res['seconds'] = time.time() - t0
        return res
    fd = cell.steer.FD(steps, Yend, R, N=900)
    for L in (0, 1, 2):
        if L == Ln:
            continue
        g = cell.gap_of(fd, L, wmax - 0.02)
        if g is None:
            others[L] = dict(drop=False, why='float pre-pass found no gap')
            continue
        w2 = float(repr(round(0.5 * (g['wm'] + g['wp']), 6))); w1 = float(repr(round(cell.W1F[L] * g['wm'], 6)))
        c2 = counts_at(bj, steps, info, x, L, w2, 1e-5, R); c1 = counts_at(bj, steps, info, x, L, w1, 1e-5, R)
        others[L] = dict(w1=w1, w2=w2, lower_w1=c1['lower'], upper_w2=c2['upper'],
                         drop=bool(c1['lower'] is not None and c2['upper'] is not None and c1['lower'] - c2['upper'] >= 1))
    res['other_sectors'] = others
    res['PASS'] = bool(len(found) == 0 and len(undecided) == 0 and all(o['drop'] for o in others.values()))
    res['outcome'] = 'INCONCLUSIVE (no drop in L = %d)' % Ln if len(found) == 0 else 'drop found (control FAILS)'
    res['seconds'] = time.time() - t0
    return res


def node(tag, sig0_str, log=print):
    """node certificate for the window run (after the seal)."""
    t0 = time.time()
    x = label(sig0_str)
    steps, info, Yend = tube(sig0_str, False, log=log)
    t_tube = time.time() - t0
    sha = save_tube(tag, sig0_str)
    assert sha == info['tube_sha256']
    t1 = time.time()
    B = br.run(1, 1, x, 26.0, [10.0, 14.0], 1e-3, [0, 1, 2, 3], log=log)
    t_br = time.time() - t1
    t2 = time.time()
    g = gr.Node(steps, info, Yend, x, log=log)
    G = g.apply(gr.FFUnit())
    t_g = time.time() - t2
    rec = dict(job='N:' + tag, sig0=sig0_str, tube_sha256=sha, existence_certified=info.get('existence_certified'),
               zeros=info.get('zeros'), tail_ok=info.get('tail_ok'), E=info['E'].str(12), m=info['m'].str(12),
               brackets={str(R): {str(L): {w: dict(upper=v[w]['upper'], lower=v[w]['lower']) for w in '+-'}
                                  for L, v in rr.items()} for R, rr in B['radii'].items()},
               D0={str(R): rr[0]['D0'].get('constrained_upper') for R, rr in B['radii'].items()},
               green=dict(alpha=g.alpha.str(10, radius=True), c=g.c.str(10, radius=True), beta=g.beta.str(10, radius=True),
                          tau_check=g.tau_check, G_FF_X=G['X'].str(6), D_int=G['D_int'].str(5), V_int=G['V_int'].str(5),
                          D_ext=G['D_ext'].str(5), V_ext_over_su=G['V_ext_over_su'].str(5),
                          tau_W_R1=g.tau_R1[1].str(8, radius=True)),
               seconds=dict(tube=t_tube, brackets=t_br, green=t_g, total=time.time() - t0))
    # audit-W N-1: the brackets must reproduce R1's K = (2, 2, 2, 0) (build-3 verdict.K_of / consistency at R = 14)
    import verdict as v3
    rows14 = B['radii'][14.0]
    Kd = {}
    try:
        cons = v3.consistency(rows14)
        for L in (0, 1, 2, 3):
            Kd[L] = v3.K_of(rows14, L)[0]
    except Exception as ex:                       # recorded, never a crash
        cons = 'error: %s' % ex
    rec['K14'] = [Kd.get(L) for L in (0, 1, 2, 3)]
    rec['bracket_consistency'] = cons
    rec['brackets_ok'] = (rec['K14'] == [2, 2, 2, 0] and cons == [])
    ok = bool(info.get('existence_certified') and info.get('zeros') == 1 and info.get('tail_ok') and rec['brackets_ok'])
    rec['ok'] = ok
    return rec
