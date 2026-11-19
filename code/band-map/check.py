"""usage: check.py sig0 Ls(comma) levels(comma) [R N p beta ...]   refinement check of one point. NOT SEALED, float."""
import sys, json
sys.path.insert(0, 'code/band-map')
from lite import background, summarize, disc_auto

s0 = float(sys.argv[1])
Ls = tuple(int(x) for x in sys.argv[2].split(','))
levels = [int(x) for x in sys.argv[3].split(',')] if sys.argv[3] != '-' else []
extra = sys.argv[4:]
b = background(s0)
print(f"s={s0} E={b.E!r} m={b.m!r} u0={b.info['u0']!r}", flush=True)
discs = [disc_auto(b.E, lv) for lv in levels]
for i in range(0, len(extra), 4):
    discs.append((float(extra[i]), int(extra[i + 1]), int(extra[i + 2]), float(extra[i + 3])))
out = []
for d in discs:
    sp = summarize(b, *d, Ls, nlow=14)
    for L, v in sp.items():
        print(f" disc={d} L={L} nL+={v['nLp']} nL-={v['nLm']} maxre={v['maxre']:.6e} unst={[(round(a,9),round(c,9)) for a,c in v['unst'][:3]]} "
              f"negK={[round(w,7) for w in v['negK']]} VK={v.get('VK')}", flush=True)
        print(f"    low={[(round(w,6),k) for w,k in v['low']]}", flush=True)
    out.append(dict(disc=list(d), L={str(k): v for k, v in sp.items()}))
json.dump(dict(sig0=s0, E=b.E, m=b.m, runs=out), open(f'data/band-map/chk_{s0:g}_{sys.argv[2]}.json', 'w'), indent=1)
