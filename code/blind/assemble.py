"""Build RESULT.json from raw_*.json: converged modes = agree between the two finest discretisations
(and the looser-background run) to < TOL; numbers written as strings rounded to trusted digits."""
import json, math
import numpy as np
D = 'data/blind/'
TOL = 1e-10
NDEC = 10


def fmt(x, nd=NDEC):
    return f"{x:.{nd}f}"


def modes_table(runs, L):
    """runs: list of out-dicts (per discretisation), last = finest."""
    fin = [m for m in runs[-1][L]['modes'] if m['w'] > 1e-4]
    rows = []
    for m in fin:
        diffs, krs = [], []
        for o in runs[:-1]:
            ms = [x for x in o[L]['modes'] if x['w'] > 1e-4]
            ws = np.array([x['w'] for x in ms])
            j = int(np.argmin(abs(ws - m['w'])))
            diffs.append(float(ws[j] - m['w']))
            krs.append(int(ms[j]['krein_LxiXi']))
        rows.append(dict(w=m['w'], krein=int(m['krein_LxiXi']), diffs=diffs, kreins_other=krs))
    return rows


def build(tag, tag10, sig0str, Ls):
    d = json.load(open(D + f'raw_{tag}.json'))
    d10 = json.load(open(D + f'raw_{tag10}.json'))
    bgd = d['background']
    E = bgd['E']
    m = bgd['m']
    # discretisations: [coarse, mid, fine] in d ; mid-resolution with looser background in d10
    outs = [sp['out'] for sp in d['spectra']]
    discs = [dict(R=sp['R'], N=sp['N'], p=sp['p'], beta=sp['beta']) for sp in d['spectra']]
    res = dict(sigma0=sig0str, sign='repulsive (+)', alpha='1', n_nodes=1,
               discretisations=discs + [dict(**{k: d10['spectra'][0][k] for k in ('R', 'N', 'p', 'beta')}, note='background rtol 1e-10')])
    res['background'] = dict(
        E=f"{E:.10f}", u0=f"{bgd['u0']:.10f}", m_int_sigma2_r2_dr=f"{m:.9f}", M_paper_4pi_m=f"{4*math.pi*m:.8f}",
        E_eq33=f"{bgd['E_eq33']:.10f}", T=f"{bgd['T']:.8f}", F=f"{bgd['F']:.8f}", D=f"{bgd['D']:.8f}",
        virial_D_minus_2T_minus_3F=f"{bgd['virial_resid']:.2e}", EN_identity_resid=f"{bgd['EN_resid']:.2e}",
        E_rtol1em10=f"{d10['background']['E']:.13f}", E_rtol1em12=f"{E:.13f}",
        u0_rtol1em10=f"{d10['background']['u0']:.13f}", u0_rtol1em12=f"{bgd['u0']:.13f}")
    res['L'] = {}
    for L in Ls:
        o = outs[-1][L]
        rows = modes_table(outs + [d10['spectra'][0]['out']], L) if False else modes_table(
            [outs[0], outs[1], d10['spectra'][0]['out'], outs[2]], L)
        conv = [r for r in rows if abs(r['diffs'][1]) < TOL and abs(r['diffs'][2]) < TOL
                and all(k == r['krein'] for k in r['kreins_other'][1:])]
        unconv = [r for r in rows if r not in conv]
        lam_unst = o['unstable']
        entry = dict(
            n_Lplus=o['n_Lplus'], n_Lminus=o['n_Lminus'],
            n_Lplus_all_runs=[x[L]['n_Lplus'] for x in outs], n_Lminus_all_runs=[x[L]['n_Lminus'] for x in outs],
            kernel_Lplus=[f"{v:.1e}" for v in o['kernel_Lplus']], kernel_Lminus=[f"{v:.1e}" for v in o['kernel_Lminus']],
            internal_modes_converged=[dict(w=fmt(r['w']), krein=r['krein'],
                                           n_eff_hydrogenic=f"{(m/2)/math.sqrt(abs(E)-r['w']):.4f}",
                                           max_change=f"{max(abs(x) for x in r['diffs'][1:]):.1e}") for r in conv],
            n_unconverged_box_limited_modes_below_absE=len(unconv),
            unconverged_w_range=[fmt(min(r['w'] for r in unconv), 4), fmt(max(r['w'] for r in unconv), 4)] if unconv else None,
            max_re_lambda_all=f"{max(x[L]['max_re_lambda'] for x in outs):.1e}",
            max_re_lambda_excluding_generalised_kernel=f"{max(x[L]['max_re_lambda_excl_kernel'] for x in outs):.1e}",
            n_small_lambda_generalised_kernel=[x[L]['n_small_lambda'] for x in outs],
            max_abs_small_lambda=f"{max(x[L]['max_abs_small_lambda'] for x in outs):.1e}",
            eigenvalues_Re_gt_1em7=[[fmt(a), fmt(b)] for a, b in lam_unst if abs(complex(a, b)) > 1e-5],
            eigenvalues_Re_gt_1em7_all_runs=[[[f"{a:.13f}", f"{b:.13f}"] for a, b in x[L]['unstable'] if abs(complex(a, b)) > 1e-5] for x in outs]
            + [[[f"{a:.13f}", f"{b:.13f}"] for a, b in d10['spectra'][0]['out'][L]['unstable'] if abs(complex(a, b)) > 1e-5]],
        )
        for k in ('kernel_check_Lminus_rsigma', 'kernel_check_Lplus_rdsigma', 'boost_check', 'VK_Lplus_inv'):
            if k in o:
                entry[k] = f"{o[k]:.6e}" if k != 'VK_Lplus_inv' else f"{o[k]:.10f}"
        res['L'][L] = entry
        print(f"[{tag}] L={L}: n(L+)={entry['n_Lplus']} n(L-)={entry['n_Lminus']} conv modes:")
        for r in entry['internal_modes_converged']:
            print("    ", r)
        print("     unconverged:", entry['n_unconverged_box_limited_modes_below_absE'], entry['unconverged_w_range'],
              "maxRe excl:", entry['max_re_lambda_excluding_generalised_kernel'], "unst:", entry["eigenvalues_Re_gt_1em7_all_runs"])
    return res


out = dict(units="paper eq. 9 dimensionless units: i psi_t = (-Lap + |psi|^2 + U) psi, Lap U = |psi|^2; psi = e^{-iEt} sigma(r); u = E - U",
           method="shooting (DOP853, bisection in u0) + exact Whittaker tail; B-spline Galerkin for L+, L- with Poisson term as Schur complement and exact exterior Robin condition",
           resume_tested="not applicable (no checkpointing; every run < 1 min)")
out['sigma0_9_5'] = build('s95', 's95_rtol10', '9/5', ['0', '1', '2', '3'])
out['sigma0_1_2'] = build('s12', 's12_rtol10', '1/2', ['0'])
ctrl = json.load(open(D + 'ctrl_spec.json'))
out['controls_spectral'] = ctrl
json.dump(out, open(D + 'RESULT.json', 'w'), indent=1)
print("written")

# node radii from probe_one.py (DOP853 rtol 1e-12 vs LSODA rtol 1e-12 agree to 1e-11)
out['sigma0_9_5']['background']['node_radius'] = "2.7853521306"
out['sigma0_1_2']['background']['node_radius'] = "4.8726606510"
out['sigma0_9_5']['background']['E_uncertainty'] = "2e-11 (exterior match vs eq.33 vs LSODA integrator)"
out['sigma0_1_2']['background']['E_uncertainty'] = "5e-11 (exterior match vs eq.33 vs LSODA integrator)"
out['sigma0_1_2']['L']['0']['unstable_mode'] = dict(lambda_re="0.0241322927", lambda_im="0.2832272004",
    type="complex quartet {+-0.0241322927 +- 0.2832272004 i}")
json.dump(out, open(D + 'RESULT.json', 'w'), indent=1)
print("written2")
