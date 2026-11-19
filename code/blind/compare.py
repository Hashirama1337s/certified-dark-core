"""Match internal modes (0 < w < |E|) across discretisations; print per-L tables with max change."""
import sys, json
import numpy as np
files = sys.argv[1:]
runs = []
for f in files:
    d = json.load(open(f))
    for sp in d['spectra']:
        runs.append((f.split('raw_')[-1], sp, d['background']))
E = runs[0][2]['E']
print("background E per file:", [(r[0], r[2]['E'], r[2]['u0']) for r in runs[::1]])
Ls = sorted(runs[0][1]['out'].keys(), key=int)
for L in Ls:
    print(f"=== L={L}")
    for tag, sp, bgd in runs:
        o = sp['out'][L]
        print(f"  {tag} R={sp['R']} N={sp['N']} p={sp['p']}: n(L+)={o['n_Lplus']} n(L-)={o['n_Lminus']} "
              f"kerP={o['kernel_Lplus']} kerM={o['kernel_Lminus']} maxRe={o['max_re_lambda']:.2e} nmodes={len(o['modes'])}")
    ref = runs[-1][1]['out'][L]['modes']
    ref = [m for m in ref if m['w'] > 1e-4]
    print("  w (finest run) | krein | changes vs each other run")
    for m in ref:
        line = f"  {m['w']:.13f} {int(m['krein_LxiXi']):+d} |"
        for tag, sp, bgd in runs[:-1]:
            ws = np.array([x['w'] for x in sp['out'][L]['modes'] if x['w'] > 1e-4])
            if len(ws) == 0:
                line += " none"
                continue
            j = np.argmin(abs(ws - m['w']))
            kr = int(sp['out'][L]['modes'][[x['w'] > 1e-4 for x in sp['out'][L]['modes']].index(True) + j]['krein_LxiXi'])
            line += f" {ws[j]-m['w']:+.1e}({kr:+d})"
        print(line)
