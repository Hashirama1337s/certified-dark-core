"""check_U0.py - proof seat check for PROOF-R1-v2 section 1 (referee-5 blocking item 1). Read-only use of build-2.

1. Text check: u_mid in build-2/out/target_bg_tube.json equals the string used in PROOF-R1-v2; the 45-digit refine
   value in target-K0.log is a prefix-consistent rounding of it; the json tube sha is f8b0cc27...
2. Rebuild check: rebuilds the target tube in memory exactly as the pre-seal CLI did (get_tube(1, 1, 1.8, 26.0,
   use_cache=False); no cache read or written), confirms the same tube_sha256, and checks in ball arithmetic that
   U0' = [u_mid - 0.99e-50, u_mid + 0.99e-50] is contained in the computed U0 (info['u0'], outward-decoded).
Run:  python -B checks/check_U0.py   (about 2 min)
"""
import sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, 'code/r1')
from flint import arb, ctx

OUT = 'data/r1/'
UMID = '3.93902357537910961270976242947912892526530674750036020337021'
SHA = 'f8b0cc27d5885a45af4b7356a1e3f6f2e0e1445510e32842cf4710f9ecfce28b'
ok = True
j = json.load(open(OUT + 'target_bg_tube.json'))
c1 = j['u_mid'] == UMID and j['tube_sha256'] == SHA
print('json u_mid and tube sha match the text:', c1); ok &= c1
log45 = None
for line in open(OUT + 'target-K0.log'):
    if 'refine R*=84.3' in line:
        log45 = line.split('u0=')[1].split()[0]
ctx.prec = 400
c2 = log45 is not None and abs(arb(log45) - arb(UMID)) < arb('1e-44')
print('target-K0.log refine value %s agrees with u_mid to < 1e-44:' % log45, c2); ok &= c2

import bg_tube as bt
steps, info, Yend = bt.get_tube(1, 1, 1.8, 26.0, use_cache=False, log=lambda *a: None)
c3 = info['tube_sha256'] == SHA
print('rebuilt tube sha256 =', info['tube_sha256'], 'match:', c3); ok &= c3
ctx.prec = 400
U0 = info['u0']
lo = arb(UMID) - arb('0.99e-50'); hi = arb(UMID) + arb('0.99e-50')
U0p = lo.union(hi)
print('computed U0 =', U0.str(70, radius=True))
print("U0'        =", U0p.str(70, radius=True))
c4 = bool(U0.contains(U0p))
print("U0' contained in computed U0:", c4); ok &= c4
c5 = info.get('u_mid') == UMID
print('rebuilt info u_mid equals text:', c5); ok &= c5
print('ALL PASS' if ok else 'SOME CHECK FAILED')
