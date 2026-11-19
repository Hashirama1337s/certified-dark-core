"""Assemble MAP.json + plot from sweep/edge/check files. NOT SEALED, float."""
import json, glob
import numpy as np
D = 'data/band-map/'
ART = 1e-3   # coarse: real lambda below this at L=0, sigma0>=3.75 is the generalised-kernel pair (vanishes under refinement)


def load(tags):
    pts = []
    for t in tags:
        pts += json.load(open(D + f'sw_{t}.json'))
    return pts


coarse = load(['cA0', 'cA', 'cB'])
fine = load(['f1', 'f2'])
# replace the two points with a bad background (r_c bug, fixed) by their reruns
for s0 in (1.43, 1.79):
    c = json.load(open(D + f'chk_{s0:g}_0,1,2,3,4,5,6,7,8,9,10,11,12,13,14.json'))
    for i, p in enumerate(fine):
        if abs(p['sig0'] - s0) < 1e-9:
            fine[i] = dict(sig0=s0, E=c['E'], m=c['m'], disc=c['runs'][0]['disc'], L=c['runs'][0]['L'], rerun=True)
coarse = sorted({round(p['sig0'], 6): p for p in coarse}.values(), key=lambda p: p['sig0'])
fine = sorted(fine, key=lambda p: p['sig0'])


def unstable(p, L, thr):
    v = p['L'][str(L)]
    return v['maxre'] > thr


def intervals(pts, L, thr):
    out, cur = [], None
    for p in pts:
        u = unstable(p, L, thr)
        if u and cur is None:
            cur = [p['sig0'], p['sig0'], 0.0, 0]
        if u:
            cur[1] = p['sig0']
            cur[2] = max(cur[2], p['L'][str(L)]['maxre'])
            cur[3] = max(cur[3], p['L'][str(L)]['n_unst'])
        if not u and cur is not None:
            out.append(cur)
            cur = None
    if cur is not None:
        out.append(cur)
    return out


res = dict(label='NOT SEALED, float', coarse={}, fine={})
for L in range(7):
    thr = ART if L == 0 else 1e-6
    res['coarse'][L] = dict(unstable_grid_intervals=intervals(coarse, L, thr), threshold=thr,
                            max_nLp=max(p['L'][str(L)]['nLp'] for p in coarse),
                            max_nLm=max(p['L'][str(L)]['nLm'] for p in coarse))
for L in range(15):
    res['fine'][L] = dict(unstable_grid_intervals=intervals(fine, L, 1e-6),
                          max_maxre=max(p['L'][str(L)]['maxre'] for p in fine),
                          nLp_range=[min(p['L'][str(L)]['nLp'] for p in fine), max(p['L'][str(L)]['nLp'] for p in fine)],
                          nLm_range=[min(p['L'][str(L)]['nLm'] for p in fine), max(p['L'][str(L)]['nLm'] for p in fine)])
# artifact check at large sigma0, L=0
res['coarse_L0_artifact'] = {s: json.load(open(D + f'chk_{s}_0.json'))['runs'] for s in ('4', '4.5')}
res['coarse_L0_artifact'] = {s: [dict(disc=r['disc'], maxre=r['L']['0']['maxre'], unst=r['L']['0']['unst']) for r in runs]
                             for s, runs in res['coarse_L0_artifact'].items()}
# monotonicity of m, E
for name, pts in (('coarse', coarse), ('fine', fine)):
    m = np.array([p['m'] for p in pts]); E = np.array([p['E'] for p in pts])
    res[f'{name}_m_monotone_increasing'] = bool(np.all(np.diff(m) > 0))
    res[f'{name}_E_monotone_decreasing'] = bool(np.all(np.diff(E) < 0))
    res[f'{name}_VK_range'] = [min(p['L']['0']['VK'] for p in pts), max(p['L']['0']['VK'] for p in pts)]
res['edges'] = {}
for t in ('lo0', 'lo1', 'hi0', 'hi1'):
    e = json.load(open(D + f'edge_{t}.json'))
    res['edges'][t] = dict(L=e['L'], level=e['level'], bracket=e['bracket'], edge=e['edge'], disc=e['disc_last'],
                           detail={k: dict(sig0=v['sig0'], E=v['E'], m=v['m'],
                                           maxre=v['L'][str(e['L'])]['maxre'], unst=v['L'][str(e['L'])]['unst'][:2],
                                           negK=v['L'][str(e['L'])]['negK'], low=v['L'][str(e['L'])]['low'][:6],
                                           nLp=v['L'][str(e['L'])]['nLp'], nLm=v['L'][str(e['L'])]['nLm'],
                                           VK=v['L']['0'].get('VK')) for k, v in e['detail'].items()})
res['coarse_table'] = [dict(sig0=p['sig0'], E=p['E'], m=p['m'],
                            maxre={L: p['L'][str(L)]['maxre'] for L in range(7)},
                            n_unst={L: p['L'][str(L)]['n_unst'] for L in range(7)}) for p in coarse]
res['fine_table'] = [dict(sig0=p['sig0'], E=p['E'], m=p['m'],
                          maxre={L: p['L'][str(L)]['maxre'] for L in range(15)},
                          n_unst={L: p['L'][str(L)]['n_unst'] for L in range(15)}) for p in fine]
json.dump(res, open(D + 'MAP.json', 'w'), indent=1)
for k in ('coarse', 'fine'):
    for L, v in res[k].items():
        print(k, L, {kk: vv for kk, vv in v.items()})
for k in ('coarse_m_monotone_increasing', 'coarse_E_monotone_decreasing', 'coarse_VK_range', 'fine_VK_range'):
    print(k, res[k])
print(res['coarse_L0_artifact'])

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
for L in range(7):
    s = [p['sig0'] for p in coarse]
    y = [p['L'][str(L)]['maxre'] if (L > 0 or p['L']['0']['maxre'] > ART) else 0 for p in coarse]
    ax[0].plot(s, y, '-o', ms=2, label=f'L={L}')
ax[0].set_title('coarse sweep (NOT SEALED, float)'); ax[0].set_xlabel('sigma0'); ax[0].set_ylabel('max Re lambda'); ax[0].legend(fontsize=7)
for L in range(15):
    s = [p['sig0'] for p in fine]
    y = [p['L'][str(L)]['maxre'] for p in fine]
    if max(y) > 1e-6:
        ax[1].plot(s, y, '-o', ms=2, label=f'L={L}')
ax[1].axvspan(1.5963117, 1.9841288, color='g', alpha=0.15, label='common band (float)')
ax[1].axvline(1.55, color='k', ls=':', lw=1); ax[1].axvline(2.07, color='k', ls=':', lw=1, label='paper 1.55, 2.07')
ax[1].set_title('fine sweep L=0..14 (L=3..14 stable throughout)'); ax[1].set_xlabel('sigma0'); ax[1].legend(fontsize=7)
plt.tight_layout(); plt.savefig(D + 'map.png', dpi=110)
print('plot ok')
