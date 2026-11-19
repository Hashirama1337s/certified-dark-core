"""Main run: background + spectrum at given sigma0 for several discretisations.
usage: run_main.py sig0_num sig0_den Lmax tag R N p beta [R N p beta ...]"""
import sys, json, time
sys.path.insert(0, 'code/blind')
from fractions import Fraction
from bg import Background
from spec import analyse

num, den, Lmax, tag = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
rest = sys.argv[5:]
sig0 = num / den
s = +1
n = 1
res = {}
import os
RTOL = float(os.environ.get("BG_RTOL", "1e-12")); METH = os.environ.get("BG_METHOD", "DOP853")
for rtol in (RTOL,):
    t = time.time()
    b = Background(sig0, s, n, rtol=rtol, method=METH)
    I = b.integrals()
    vir = I['D'] - (2 * I['T'] + 3 * s * I['F'])
    EN = b.E * I['M4pi'] - (2 * I['T'] + 4 * s * I['F'] - 4 * I['D'])
    print(f"BG sig0={sig0} u0={b.info['u0']!r} E={b.E!r} E33={I['E_eq33']!r} m={I['m']!r} "
          f"T={I['T']!r} F={I['F']!r} D={I['D']!r} vir={vir:.2e} EN={EN:.2e} rc={b.rc} mism={b.info['logder_mismatch']:.1e} "
          f"t={time.time()-t:.1f}s", flush=True)
    res['background'] = dict(rtol=rtol, method=METH, u0=b.info['u0'], ulo=b.info['ulo'], uhi=b.info['uhi'], E=b.E, **I, virial_resid=vir, EN_resid=EN,
                             rc=b.rc, logder_mismatch=b.info['logder_mismatch'])
res['spectra'] = []
for i in range(0, len(rest), 4):
    R, N, p, beta = float(rest[i]), int(rest[i + 1]), int(rest[i + 2]), float(rest[i + 3])
    t = time.time()
    print(f"DISC R={R} N={N} p={p} beta={beta}", flush=True)
    out = analyse(b, R, N, p, beta, Ls=tuple(range(Lmax + 1)), s=s)
    print(f"  t={time.time()-t:.1f}s", flush=True)
    res['spectra'].append(dict(R=R, N=N, p=p, beta=beta, out={str(k): v for k, v in out.items()}))
json.dump(res, open(f'data/blind/raw_{tag}.json', 'w'), indent=1, default=str)
print("DONE", flush=True)
