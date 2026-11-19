"""usage: sweep.py tag s_start s_stop step Lmax [level]   (continuation in sigma0; writes sw_<tag>.json incrementally)
NOT SEALED, float."""
import sys, json, time
sys.path.insert(0, 'code/band-map')
import numpy as np
from lite import point

tag = sys.argv[1]
a, b_, h = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
Lmax = int(sys.argv[5])
level = int(sys.argv[6]) if len(sys.argv) > 6 else 0
nstep = int(round((b_ - a) / h))
sigs = [round(a + i * h, 10) for i in range(nstep + 1)]
res = []
u0g = None
fn = f'data/band-map/sw_{tag}.json'
for s0 in sigs:
    d, u0g = point(s0, tuple(range(Lmax + 1)), u0guess=u0g, level=level)
    res.append(d)
    line = ' '.join(f"{L}:{v['maxre']:.1e}/{v['n_unst']}" for L, v in d['L'].items())
    print(f"s={s0:.4f} E={d['E']:.6f} m={d['m']:.4f} VK={d['L']['0'].get('VK', 0):.4f} t={d['t']:.1f}s(bg {d['t_bg']:.1f}) | {line}", flush=True)
    json.dump(res, open(fn, 'w'))
print("DONE", flush=True)
