"""usage: edge.py tag a b L level tol   bisect sigma0 in [a,b] for onset of instability in sector L (one side stable,
other unstable; Re lambda > THR_E). Then report the spectrum at the edge +-0.002, +-1e-4. NOT SEALED, float."""
import sys, json, time
sys.path.insert(0, 'code/band-map')
import numpy as np
from lite import background, summarize, disc_auto

THR_E = 1e-7
tag, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
L, level, tol = int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6])
fn = f'data/band-map/edge_{tag}.json'
cache = {}


def ev(s0, Ls=None, nlow=10):
    bg = background(s0, None if not cache else cache[min(cache, key=lambda x: abs(x - s0))])
    cache[s0] = bg.info['u0']
    R, N, p, beta = disc_auto(bg.E, level)
    sp = summarize(bg, R, N, p, beta, Ls or (L,), nlow=nlow)
    return bg, sp, (R, N, p, beta)


t0 = time.time()
_, sa, _ = ev(a)
_, sb, _ = ev(b)
ua = sa[L]['maxre'] > THR_E
ub = sb[L]['maxre'] > THR_E
print(f"a={a} unstable={ua} maxre={sa[L]['maxre']:.3e} | b={b} unstable={ub} maxre={sb[L]['maxre']:.3e}", flush=True)
assert ua != ub, "no sign change"
hist = []
while b - a > tol:
    m = 0.5 * (a + b)
    _, sm, d = ev(m)
    um = sm[L]['maxre'] > THR_E
    hist.append([m, sm[L]['maxre'], sm[L]['unst'][:2]])
    print(f"  m={m:.8f} maxre={sm[L]['maxre']:.3e} unst={sm[L]['unst'][:2]} negK={sm[L]['negK'][:4]}", flush=True)
    if um == ua:
        a = m
    else:
        b = m
edge = 0.5 * (a + b)
print(f"EDGE L={L} level={level} in [{a:.8f}, {b:.8f}] disc={d} t={time.time()-t0:.0f}s", flush=True)
detail = {}
for off in (-0.002, -1e-4, 1e-4, 0.002):
    s0 = edge + off
    bg, sp, d = ev(s0, Ls=tuple(sorted({0, L})), nlow=12)
    detail[f"{off:+g}"] = dict(sig0=s0, E=float(bg.E), m=float(bg.m), disc=list(d), L={str(k): v for k, v in sp.items()})
    v = sp[L]
    print(f"  off={off:+g} s={s0:.6f} E={bg.E:.8f} m={bg.m:.8f} nL+={v['nLp']} nL-={v['nLm']} maxre={v['maxre']:.4e} "
          f"unst={v['unst'][:2]} negK={v['negK'][:4]} VK={sp[0].get('VK')}", flush=True)
    print(f"     low modes (w,krein): {[(round(w, 6), k) for w, k in v['low'][:10]]}", flush=True)
json.dump(dict(L=L, level=level, bracket=[a, b], edge=edge, disc_last=list(d), hist=hist, detail=detail),
          open(fn, 'w'), indent=1)
print("DONE", flush=True)
