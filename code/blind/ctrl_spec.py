"""Spectral positive controls:
 (a) repulsive n=0 ground state (paper Sec V.1: stable for all L) at sigma0 = 1.0
 (b) attractive n=0 at sigma0 = 0.19 (paper: stable) and 1.89 (paper: unstable at L=0, real lambda)
 (c) Vakhitov-Kolokolov identity <L+^{-1} r sigma, r sigma> = (1/2) dm/dE (finite differences in sigma0)
     for the target state sigma0 = 9/5 and for sigma0 = 1/2.
"""
import sys, json
sys.path.insert(0, 'code/blind')
import numpy as np
from bg import Background
from spec import analyse

res = {}
for (sig0, s, n, R) in [(1.0, +1, 0, 40.0), (0.19, -1, 0, 80.0), (1.89, -1, 0, 40.0)]:
    b = Background(sig0, s, n)
    print(f"CTRL sig0={sig0} s={s} n={n} E={b.E}", flush=True)
    out = analyse(b, R, 150, 7, 2.0, Ls=(0, 1), s=s, verbose=False)
    for L, o in out.items():
        print(f"  L={L} n(L+)={o['n_Lplus']} n(L-)={o['n_Lminus']} kerP={o['kernel_Lplus']} kerM={o['kernel_Lminus']} "
              f"maxRe={o['max_re_lambda']:.4e} unstable={o['unstable']} VK={o.get('VK_Lplus_inv')}", flush=True)
    res[f"{sig0}_{s}_{n}"] = {str(L): dict(n_Lplus=o['n_Lplus'], n_Lminus=o['n_Lminus'], max_re=o['max_re_lambda'],
                                           unstable=o['unstable']) for L, o in out.items()}

for sig0, R in [(1.8, 40.0), (0.5, 80.0)]:
    vals = {}
    for h in (2e-3, 1e-3):
        bp = Background(sig0 + h, +1, 1)
        bm = Background(sig0 - h, +1, 1)
        Ip, Im = bp.integrals(), bm.integrals()
        vals[h] = 0.5 * (Ip['m'] - Im['m']) / (bp.E - bm.E)
    b = Background(sig0, +1, 1)
    out = analyse(b, R, 150, 7, 2.0, Ls=(0,), s=+1, verbose=False)
    print(f"VK sig0={sig0}: <L+^-1 a0,a0>={out[0]['VK_Lplus_inv']!r}  (1/2)dm/dE fd h=2e-3: {vals[2e-3]!r}  h=1e-3: {vals[1e-3]!r}", flush=True)
    res[f"VK_{sig0}"] = dict(operator=out[0]['VK_Lplus_inv'], fd_2e3=vals[2e-3], fd_1e3=vals[1e-3])
json.dump(res, open('data/blind/ctrl_spec.json', 'w'), indent=1, default=str)
print("DONE", flush=True)
