"""referee-W3 independent checker for BAR-W1 (seal 5e6d7bfed0).

Reads build-W/out/cells/c*.json and build-W/out/n*/N.json (+ tube.json sha) and re-applies the sealed per-cell
HOLDS rule and the node rules with EXACT rational interval arithmetic on the printed arb balls
("[mid +/- rad]" printed by arb are rigorous enclosures). Imports nothing from build-W.
A check that passes here passes on enclosures that are at most as tight as the pipeline's, so it is a real pass.
"""
import json, os, re, sys, hashlib
from fractions import Fraction as F

BW = 'data/r3'
NODES = ['1597/1000', '1600/1000', '1605/1000', '1612/1000', '1625/1000', '33/20', '1675/1000', '17/10', '1725/1000',
         '7/4', '1775/1000', '9/5', '1825/1000', '37/20', '1875/1000', '19/10', '1925/1000', '39/20', '1962/1000',
         '1970/1000', '1976/1000', '1980/1000', '1983/1000']          # transcribed from BAR-W1.md "Schedule"
KUP = {'H(w2) L0': 3, 'H(w2) L1': 2, 'H(w2) L2': 1, 'H(0) L0': 4, 'H(0) L1': 3, 'H(0) L2': 2, 'H(0) L3': 0}
NAMES = ['H(w2) L0', 'H(w2) L1', 'H(w2) L2', 'RITZ L0', 'RITZ L1', 'RITZ L2', 'H(0) L0', 'H(0) L1', 'H(0) L2',
         'H(0) L3', 'PEN']
MP = F(5)

BALL = re.compile(r'^\[\s*([-+0-9.eE]+)\s*\+/-\s*([-+0-9.eE]+)\s*\]$')
EXACT = re.compile(r'^\[?\s*([-+0-9.eE]+)\s*\]?$')
FLOATS = []


def iv(s, where=''):
    """printed arb -> (lo, hi) as exact Fractions. A bare Python float is accepted but recorded in FLOATS."""
    if isinstance(s, (int, float)) and not isinstance(s, bool):
        FLOATS.append(where)
        x = F(s); return (x, x)
    s = str(s).strip()
    m = BALL.match(s)
    if m:
        c, r = F(m.group(1)), F(m.group(2))
        assert r >= 0
        return (c - r, c + r)
    m = EXACT.match(s)
    if m:
        x = F(m.group(1)); return (x, x)
    raise ValueError('unparsed %r at %s' % (s, where))


def fmin_quad(ma, mb, C0, C1):
    """exact min over t in [0,1] of (1-t) ma + t mb - C0 - C1 t (1-t) (C1 >= 0 so convex); returns (fmin, tstar)."""
    f = lambda t: (1 - t) * ma + t * mb - C0 - C1 * t * (1 - t)
    cands = [F(0), F(1)]
    if C1 > 0:
        ts = (C1 + ma - mb) / (2 * C1)
        if 0 < ts < 1:
            cands.append(ts)
    vals = [(f(t), t) for t in cands]
    return min(vals)


def ratio_min(ma, mb, C0, C1, n=2000):
    """REPORT ONLY: min over a grid of chord(m)(t) / (C0 + C1 t(1-t))."""
    best = None
    for i in range(n + 1):
        t = F(i, n)
        r = ((1 - t) * ma + t * mb) / (C0 + C1 * t * (1 - t))
        if best is None or r < best[0]:
            best = (r, t)
    return best


def node_check(tag, sig):
    d = json.load(open(os.path.join(BW, tag, 'N.json')))
    p = []
    sha = hashlib.sha256(open(os.path.join(BW, tag, 'tube.json'), 'rb').read()).hexdigest()
    if sha != d['tube_sha256']:
        p.append('tube.json sha %s != N.json %s' % (sha[:10], d['tube_sha256'][:10]))
    if F(d['sig0']) != F(sig):
        p.append('sig0 mismatch')
    if d.get('existence_certified') is not True: p.append('existence not certified')
    if d.get('zeros') != 1: p.append('zeros != 1')
    if d.get('tail_ok') is not True: p.append('tail not ok')
    E = iv(d['E'], tag + '.E')
    if not E[1] < 0: p.append('E not < 0')
    K = {}
    for R in ('10.0', '14.0'):
        rows = d['brackets'][R]
        for L in '0123':
            for w in '+-':
                u, l = rows[L][w]['upper'], rows[L][w]['lower']
                if u is None or l is None or u < l:
                    p.append('R%s L%s %s inconsistent %s/%s' % (R, L, w, u, l))
        r = rows
        K[R] = [d['D0'][R] + (r['0']['-']['upper'] - 1), (r['1']['+']['upper'] - 1) + r['1']['-']['upper'],
                r['2']['+']['upper'] + r['2']['-']['upper'], r['3']['+']['upper'] + r['3']['-']['upper']]
    if K['14.0'] != [2, 2, 2, 0]: p.append('K14 = %s' % K['14.0'])
    if d.get('K14') != K['14.0']: p.append('recorded K14 %s != recomputed %s' % (d.get('K14'), K['14.0']))
    g = d['green']
    for k in ('alpha', 'c'):
        lo, hi = iv(g[k], tag + '.' + k)
        if lo <= 0 <= hi: p.append('green %s contains 0' % k)
    if not (g['tau_check']['a_overlap'] and g['tau_check']['ap_overlap']): p.append('tau overlap')
    if d.get('ok') is not True: p.append('recorded ok false')
    return dict(tag=tag, sha=d['tube_sha256'], E=E, K14=K['14.0'], K10=K['10.0'], problems=p)


def cell_check(cid, a, b, nodes):
    d = json.load(open(os.path.join(BW, 'cells', cid + '.json')))
    p = []; info = {}
    if [F(x) for x in d['cell']] != [F(a), F(b)]: p.append('cell endpoints %s != schedule %s,%s' % (d['cell'], a, b))
    if d['R'] != 20.0: p.append('R = %s' % d['R'])
    ta, tb = 'n' + str(int(F(a) * 1000)), 'n' + str(int(F(b) * 1000))
    if d['tube_sha'] != [nodes[ta]['sha'], nodes[tb]['sha']]: p.append('tube sha differs from node record')
    # BR' both halves
    halves = []
    for h, br in enumerate(d['BR']):
        w = '%s.BR%d' % (cid, h)
        if br['ok'] is not True or br['selfmap'] is not True: p.append('%s recorded not ok' % w)
        Y0, Z1, Z2, ru, ka, rho = (iv(br[k], w + k) for k in ('Y0', 'Z1', 'Z2', 'r_u', 'kappa', 'rho'))
        if not Z1[1] < 1: p.append(w + ' Z1max >= 1')
        rho_f = 2 * Y0[1] / (1 - Z1[1])                     # upper bound of 2 Y0max / (1 - Z1max)
        if not (rho[0] <= rho_f and 2 * Y0[0] / (1 - Z1[0]) <= rho[1]): p.append(w + ' rho inconsistent with 2Y0/(1-Z1)')
        rs = max(rho[1], rho_f)                             # ball radius used for every check below
        if not Y0[1] + Z1[1] * rs + Z2[1] * rs * rs <= rs: p.append(w + ' self-map fails')
        kap = Z1[1] + ru[1] * Z2[1]
        if not kap < 1: p.append(w + ' kappa(r_u) >= 1')
        if not (ka[0] <= kap and Z1[0] + ru[0] * Z2[0] <= ka[1]): p.append(w + ' kappa inconsistent')
        if not rs <= ru[0]: p.append(w + ' rho_max > r_u')
        halves.append(dict(rho=rs, ru=ru, kappa=kap, Z1=Z1[1], Y0=Y0[1]))
    if not (halves[0]['rho'] <= halves[1]['ru'][0] and halves[1]['rho'] <= halves[0]['ru'][0]):
        p.append('halves disagree')
    dA, dB = iv(d['tube_diameter'][0], cid + '.dA'), iv(d['tube_diameter'][1], cid + '.dB')
    if not (dA[1] < halves[0]['ru'][0] and dB[1] < halves[1]['ru'][0]): p.append('tube diameter >= r_u')
    if d.get('tube_below_r_u') is not True: p.append('recorded tube_below_r_u false')
    if d.get('one_node_E_neg') is not True: p.append('one node / E<0 false')
    absE = iv(d['absE_lower'], cid + '.absE')
    info['absE_lo'] = absE[0]
    info['min_1mZ1'] = min(1 - h['Z1'] for h in halves)
    info['rho_over_ru'] = max(h['rho'] / h['ru'][0] for h in halves)
    info['kappa'] = max(h['kappa'] for h in halves)
    info['tubediam_over_ru'] = max(dA[1] / halves[0]['ru'][0], dB[1] / halves[1]['ru'][0])
    CH = {L: {k: iv(v, '%s.CH%s.%s' % (cid, L, k)) for k, v in d['CH'][L].items()} for L in '0123'}
    G = {k: iv(v, cid + '.Gam.' + k) for k, v in d['CH']['Gam'].items()}
    certs = d['certs']
    if sorted(certs) != sorted(NAMES): p.append('certificate set %s' % sorted(certs))
    cc = {}
    for name in NAMES:
        c = certs[name]; w = cid + '.' + name
        if c.get('ok') is not True or c.get('CC') is not True: p.append(w + ' recorded not ok/CC')
        ma, mb = iv(c['ma'], w + '.ma'), iv(c['mb'], w + '.mb')
        if not (ma[0] > 0 and mb[0] > 0): p.append(w + ' margin not > 0')
        L = str(c['L'])
        if name.startswith('H('):
            if c['kind'] != 'upper': p.append(w + ' kind')
            C0, C1 = CH[L]['C0'][1], CH[L]['C1'][1]
            for e in ('da', 'db'):
                x = c[e]
                k = KUP[name]
                if not (x['ok'] is True and x['ext_ok'] is True and x['nB'] == k and x['conj'] == k and x['endpoint'] == 0):
                    p.append('%s.%s count/ext: nB %s conj %s endpoint %s ext %s (k %d)' % (w, e, x['nB'], x['conj'], x['endpoint'], x['ext_ok'], k))
                if k > 0:
                    piv = [iv(s, w + '.piv') for s in (x['S_pivots'] or [])]
                    if len(piv) != k or not all(q[1] < 0 for q in piv): p.append('%s.%s S not neg-def from pivots' % (w, e))
        elif name.startswith('RITZ'):
            if c['kind'] != 'lower': p.append(w + ' kind')
            C0, C1 = CH[L]['C0p'][1], CH[L]['C1p'][1]
        else:
            if c['kind'] != 'pen' or c['L'] != 0: p.append(w + ' kind')
            C0 = CH['0']['C0'][1] + MP * G['G0'][1]; C1 = CH['0']['C1'][1] + MP * G['G1'][1]
            for e in ('da', 'db'):
                x = c[e]
                d2, mpp, sh, th = (iv(x[k], w + k) for k in ('d2', 'Mpp_d2', 'sherman', 'theta'))
                Mpp_lo = MP * (1 - th[1])
                if not (d2[1] < 0 and Mpp_lo * (-d2[1]) > 1 and sh[1] < 0 and 0 < th[0] and th[1] < 1):
                    p.append('%s.%s PEN conditions' % (w, e))
        fm, ts = fmin_quad(ma[0], mb[0], C0, C1)
        rr, tr = ratio_min(ma[0], mb[0], C0, C1)
        if not fm > 0: p.append(w + ' CC quadratic test FAILS on printed enclosures (min %.3e)' % float(fm))
        fl = c.get('float')
        fac = (float(ma[0]) / abs(fl[0]), float(mb[0]) / abs(fl[1])) if fl else None
        cc[name] = dict(fmin=fm, t=ts, ratio=rr, tr=tr, ma=ma[0], mb=mb[0], C0=C0, C1=C1, fac=fac)
    # w-checks: 0 <= w1 < w2 < |E| at both ends (|E| a certified lower bound)
    for L in '012':
        h = certs['H(w2) L' + L]; r = certs['RITZ L' + L]
        for wa_, w1_ in ((h['wa'], r['w1a']), (h['wb'], r['w1b'])):
            if not (0 <= F(w1_) < F(wa_) < absE[0]): p.append('w-check L%s fails (%s, %s, %s)' % (L, w1_, wa_, float(absE[0])))
        if h.get('w_check') is not True: p.append('recorded w_check false L' + L)
        info['w2max_L' + L] = max(h['wa'], h['wb'])
    if d.get('outcome') != 'HOLDS' or d.get('fails'): p.append('recorded outcome %s' % d.get('outcome'))
    return dict(cid=cid, problems=p, info=info, cc=cc)


def main():
    out = []
    pr = lambda *a: (print(*a), out.append(' '.join(str(x) for x in a)))
    nodes = {}
    for s in NODES:
        tag = 'n' + str(int(F(s) * 1000))
        nodes[tag] = node_check(tag, s)
    # tiling: consecutive exact rationals, strictly increasing, ends 1597/1000 and 1983/1000
    fr = [F(s) for s in NODES]
    assert fr[0] == F(1597, 1000) and fr[-1] == F(1983, 1000) and all(x < y for x, y in zip(fr, fr[1:]))
    cells = []
    for i in range(22):
        cid = 'c%02d' % (i + 1)
        cells.append(cell_check(cid, NODES[i], NODES[i + 1], nodes))
    nprob = sum(len(n['problems']) for n in nodes.values()) + sum(len(c['problems']) for c in cells)
    pr('== nodes ==')
    for t, n in nodes.items():
        pr(t, 'E', '%.10f' % float(n['E'][1]), 'K14', n['K14'], 'K10', n['K10'], 'problems', n['problems'] or 'none')
    pr('== cells ==')
    for c in cells:
        i = c['info']
        worst = min(c['cc'].items(), key=lambda kv: kv[1]['ratio'])
        pr('%s [%s, %s]  1-Z1min %.4f  kappa %.4f  rho/r_u %.3e  diam/r_u %.3e  |E|lo %.5f  w2max %.4f/%.4f/%.4f' % (
            c['cid'], NODES[int(c['cid'][1:]) - 1], NODES[int(c['cid'][1:])], float(i['min_1mZ1']), float(i['kappa']),
            float(i['rho_over_ru']), float(i['tubediam_over_ru']), float(i['absE_lo']), i['w2max_L0'], i['w2max_L1'], i['w2max_L2']))
        pr('    tightest CC: %s  min chord(m)/loss = %.3f at t=%.3f ; exact min f = %.3e at t=%.3f ; ma %.3e mb %.3e C0 %.3e C1 %.3e ; m/float %s' % (
            worst[0], float(worst[1]['ratio']), float(worst[1]['tr']), float(worst[1]['fmin']), float(worst[1]['t']),
            float(worst[1]['ma']), float(worst[1]['mb']), float(worst[1]['C0']), float(worst[1]['C1']),
            tuple(round(x, 3) for x in worst[1]['fac'])))
        facs = sorted(set(round(x, 2) for v in c['cc'].values() for x in v['fac']))
        pr('    margin fractions used:', facs, ' problems:', c['problems'] or 'none')
    allr = sorted(((v['ratio'], c['cid'], k) for c in cells for k, v in c['cc'].items()))[:8]
    pr('== 8 smallest chord(m)/loss ratios ==')
    for r, cid, k in allr:
        pr('  %s %-9s %.3f' % (cid, k, float(r)))
    pr('floats parsed as values (not arb balls):', sorted(set(FLOATS)) or 'none')
    pr('TOTAL PROBLEMS:', nprob)
    pr('VERDICT (referee-W3 checker):', 'ALL 22 CELLS HOLD, ALL 23 NODES OK, TILING EXACT' if nprob == 0 else 'NOT ALL HOLD')
    json.dump({'problems': nprob, 'lines': out}, open(os.path.join(os.path.dirname(__file__), 'logs', 'check_w3.json'), 'w', newline='\n'), indent=1)


if __name__ == '__main__':
    main()
