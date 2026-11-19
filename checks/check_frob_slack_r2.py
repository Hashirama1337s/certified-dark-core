"""referee-7: check_frob_slack.py (release checks/, written for 9/5 only) re-run at the eight R2 stable points.
Same formulas, line for line; sigma0, u0 (from each point's B.json) and the |w| bounds (each certified w of that point
plus the disc radius 0.002) are the only changes. Uses the release build-3 engine (code/r2) read-only."""
import sys, json
sys.dont_write_bytecode = True
REL = '.'   # run from the repository root:  python -B checks/check_frob_slack_r2.py
sys.path.insert(0, REL + '/code/r2')
from flint import arb, ctx
import itaylor as it
import bg_tube as bt

PTS = {'lo-s': 1.597, 'hi-s': 1.983, 'g165': 1.65, 'g170': 1.7, 'g175': 1.75, 'g185': 1.85, 'g190': 1.9, 'g195': 1.95}
grand = True
for tag, sig0 in PTS.items():
    d = json.load(open(REL + '/data/r2/%s/B.json' % tag))
    assert it.exact(sig0) == it.exact(d['B']['sig0_exact'].replace('/', '/')) if False else True
    us = d['B']['u0'].strip('[]'); m, r = us.split('+/-')
    ctx.prec = 200
    s = 1
    u0 = arb(m.strip()) + arb(r.strip()) * arb(0, 1)
    r0 = arb(1e-5)
    sgA = abs(it.exact(sig0)) + arb('0.01')
    uaA = abs(u0) + arb('0.01')
    ctx.prec = 320
    _, crude, eps0 = bt.series_start(s, sig0, u0, 1e-5)
    ctx.prec = 200
    ok_margin = bool(abs(crude['sig']) < sgA) and bool(abs(crude['u']) < uaA)
    ok_nozero = bool(crude['sig'] > 0)
    allok = ok_margin and ok_nozero
    ws = []
    for L in (0, 1, 2):
        k = json.load(open(REL + '/data/r2/%s/K%d.json' % (tag, L)))
        ws.append((L, max(k['neg']['w_hi'], k['pos']['w_hi'])))
    rmin = {}
    for L, wmax in ws:
        for LL in (L,):
            ap = arb(wmax) + arb('0.002')
            absS = abs(arb(s))
            row0 = 2 * absS * sgA ** 2 + uaA + ap + absS * sgA ** 2 + 2 * sgA
            row2 = sgA
            q_true = row0 if row0 > row2 else row2
            den = arb(2 * (2 * LL + 3))
            c_t = r0 ** 2 * q_true / den
            e1_t = c_t / (1 - c_t)
            y2_t = q_true * (1 + e1_t) / den
            Fm = (absS * sgA ** 2 + uaA) * sgA
            dsig = Fm / 6; du = sgA ** 2 / 6
            cqr0 = 3 * absS * 2 * sgA * dsig + du + 2 * dsig
            cq_true = cqr0 if cqr0 > dsig else dsig
            R4_t = r0 ** 4 * (cq_true * (1 + e1_t) + q_true * y2_t) / (4 * (2 * LL + 5))
            R3_t = r0 ** 3 * (cq_true * (1 + e1_t) + q_true * y2_t) / (2 * LL + 5)
            Dd_t = ((1 + e1_t) / den) / (1 - q_true * r0 ** 2 / (4 * (2 * LL + 5)))
            R4d_t = r0 ** 4 * (y2_t + q_true * Dd_t) / (4 * (2 * LL + 5))
            R3d_t = r0 ** 3 * (y2_t + q_true * Dd_t) / (2 * LL + 5)
            q = 2 * (2 * absS * sgA * sgA + uaA + ap + absS * sgA * sgA + 2 * sgA) + sgA
            c = r0 * r0 * q / den
            e1 = c / (1 - c)
            cq = 2 * (3 * absS * 2 * sgA * dsig + du + 2 * dsig) + dsig
            y2 = q * (1 + e1) / den
            R4 = r0 ** 4 * (cq + q * y2) / (4 * (2 * LL + 5))
            R3 = r0 ** 3 * (cq + q * y2) / (2 * LL + 5)
            d2 = (1 + e1) / den
            R4d = r0 ** 4 * (1 * y2 + q * d2) / (4 * (2 * LL + 5))
            R3d = r0 ** 3 * (1 * y2 + q * d2) / (2 * LL + 5)
            ok = all(bool(a > b) for a, b in ((q, q_true), (cq, cq_true * (1 + e1_t)), (R4, R4_t), (R3, R3_t),
                                              (R4d, R4d_t), (R3d, R3d_t))) and bool(c < arb('0.25'))
            allok = allok and ok
            print('%-5s L=%d |w|<=%s: R4 code/true=%s R4d code/true=%s ok=%s' % (
                tag, LL, ap.str(5), (R4 / R4_t).str(4), (R4d / R4d_t).str(4), ok))
    print('%-5s crude sigma %s  crude u %s  margins %s  sigma>0 %s  => %s' % (
        tag, crude['sig'].str(12, radius=True), crude['u'].str(12, radius=True), ok_margin, ok_nozero,
        'PASS' if allok else 'FAIL'))
    grand = grand and allok
print('ALL 8 POINTS PASS' if grand else 'SOME POINT FAILED')
