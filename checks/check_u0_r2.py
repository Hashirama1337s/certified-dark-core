"""check_u0_r2.py - the check_U0.py check at the eight R2 stable points (BAR-R2-EDGES, seal 3ad051728e).

For each tag: rebuilds the point's background tube in memory exactly as the B job did (code/r2/bg_tube.get_tube with
s = 1, n = 1, the sigma0 label of the point, R1 = 26, disk cache off: nothing read or written), confirms that the
rebuilt tube sha256 equals data/r2/<tag>/B.json B.tube_sha256, prints the 60-digit u_mid, and checks in 400-bit ball
arithmetic that U0'_p = [u_mid - 0.99e-50, u_mid + 0.99e-50] is contained in the computed start interval U0.
Run from the repository root:  python -B checks/check_u0_r2.py [tag ...]     (about 80-120 s per point)
Default tags: lo-s g165 g170 g175 g185 g190 g195 hi-s.
"""
import json
import sys
from fractions import Fraction
sys.dont_write_bytecode = True
sys.path.insert(0, 'code/r2')
from flint import arb, ctx
import bg_tube as bt

TAGS = sys.argv[1:] or ['lo-s', 'g165', 'g170', 'g175', 'g185', 'g190', 'g195', 'hi-s']
bt.DISK_CACHE = False
allok = True
for tag in TAGS:
    B = json.load(open('data/r2/%s/B.json' % tag, encoding='utf-8'))
    F = Fraction(B['config']['sig0_exact'])
    label = float(F)
    assert Fraction(repr(label)) == F
    steps, info, Yend = bt.get_tube(1, 1, label, 26.0, use_cache=False, log=lambda *a: None)
    c1 = info['tube_sha256'] == B['B']['tube_sha256']
    umid = info['u_mid']
    ctx.prec = 400
    U0 = info['u0']
    U0p = (arb(umid) - arb('0.99e-50')).union(arb(umid) + arb('0.99e-50'))
    c2 = bool(U0.contains(U0p))
    ok = c1 and c2
    allok &= ok
    print('%-5s sigma0 = %-9s u_mid = %s' % (tag, B['config']['sig0_exact'], umid))
    print("      tube sha256 %s matches B.json: %s ; U0'_p contained in computed U0: %s ; %s"
          % (info['tube_sha256'], c1, c2, 'PASS' if ok else 'FAIL'))
    sys.stdout.flush()
print('ALL PASS' if allok else 'SOME CHECK FAILED')
