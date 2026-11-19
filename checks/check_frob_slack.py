"""check_frob_slack.py - proof seat check (PROOF-R1, section 3.6). Read-only use of build-2.

Recomputes, at the target (s = 1, sigma0 = 9/5, u0 from target-B, r0 = binary64 1e-5), the second-order Frobenius
remainder bounds with ALL factors kept (the 'true' bounds derived in PROOF-R1.md 3.6), and compares them with the
constants match.frob_start actually uses (q, cq, R4, R3, R4d, R3d). Also rebuilds the series_start crude enclosure and
checks the 0.01 margins and the zero-free start interval [0, r0].
PASS means: every code constant >= the corresponding true bound.
Run:  python -B checks/check_frob_slack.py
"""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'code/r1')
from flint import arb, ctx
import itaylor as it
import bg_tube as bt

ctx.prec = 200
s = 1
sig0 = 1.80
u0 = arb('3.93902357538') + arb('8.91e-13') * arb(0, 1)      # target-B.json B.u0 (outward string)
r0 = arb(1e-5)                                               # the binary64 point, as in the build
sgA = abs(it.exact(sig0)) + arb('0.01')
uaA = abs(u0) + arb('0.01')

# --- start margins and zero-free start (series_start crude enclosure, 320 bits as in the tube)
ctx.prec = 320
_, crude, eps0 = bt.series_start(s, sig0, u0, 1e-5)
ctx.prec = 200
ok_margin = bool(abs(crude['sig']) < sgA) and bool(abs(crude['u']) < uaA)
ok_nozero = bool(crude['sig'] > 0)
print('crude sigma on [0,r0]:', crude['sig'].str(12, radius=True), ' crude u:', crude['u'].str(12, radius=True))
print('0.01 margins hold:', ok_margin, '   sigma > 0 on [0, r0]:', ok_nozero)

allok = ok_margin and ok_nozero
for L in (0, 1, 2):
    for par in (arb('1.27'), arb('0.96'), arb('0.53')):   # |w| bounds above every certified w (+ disc radius 0.002)
        ap = arb(abs(par).upper()) + arb('0.002')
        absS = abs(arb(s))
        # true row bounds of Qt (infinity norm), PROOF 3.6
        row0 = 2 * absS * sgA ** 2 + uaA + ap + absS * sgA ** 2 + 2 * sgA
        row2 = sgA
        q_true = row0 if row0 > row2 else row2
        den = arb(2 * (2 * L + 3))
        c_t = r0 ** 2 * q_true / den
        e1_t = c_t / (1 - c_t)
        y2_t = q_true * (1 + e1_t) / den
        Fm = (absS * sgA ** 2 + uaA) * sgA
        dsig = Fm / 6; du = sgA ** 2 / 6
        cqr0 = 3 * absS * 2 * sgA * dsig + du + 2 * dsig
        cq_true = cqr0 if cqr0 > dsig else dsig
        R4_t = r0 ** 4 * (cq_true * (1 + e1_t) + q_true * y2_t) / (4 * (2 * L + 5))
        R3_t = r0 ** 3 * (cq_true * (1 + e1_t) + q_true * y2_t) / (2 * L + 5)
        Dd_t = ((1 + e1_t) / den) / (1 - q_true * r0 ** 2 / (4 * (2 * L + 5)))
        R4d_t = r0 ** 4 * (y2_t + q_true * Dd_t) / (4 * (2 * L + 5))
        R3d_t = r0 ** 3 * (y2_t + q_true * Dd_t) / (2 * L + 5)
        # code constants (match.py:55-94, same formulas)
        q = 2 * (2 * absS * sgA * sgA + uaA + ap + absS * sgA * sgA + 2 * sgA) + sgA
        c = r0 * r0 * q / den
        e1 = c / (1 - c)
        cq = 2 * (3 * absS * 2 * sgA * dsig + du + 2 * dsig) + dsig
        y2 = q * (1 + e1) / den
        R4 = r0 ** 4 * (cq + q * y2) / (4 * (2 * L + 5))
        R3 = r0 ** 3 * (cq + q * y2) / (2 * L + 5)
        d2 = (1 + e1) / den
        R4d = r0 ** 4 * (1 * y2 + q * d2) / (4 * (2 * L + 5))
        R3d = r0 ** 3 * (1 * y2 + q * d2) / (2 * L + 5)
        ok = all(bool(a > b) for a, b in ((q, q_true), (cq, cq_true * (1 + e1_t)), (R4, R4_t), (R3, R3_t),
                                          (R4d, R4d_t), (R3d, R3d_t))) and bool(c < arb('0.25'))
        allok = allok and ok
        print('L=%d |w|<=%s: c=%s  R4 code/true=%s  R3 code/true=%s  R4d code/true=%s  ok=%s' % (
            L, ap.str(4), c.str(3), (R4 / R4_t).str(4), (R3 / R3_t).str(4), (R4d / R4d_t).str(4), ok))
print('ALL PASS' if allok else 'SOME CHECK FAILED')
