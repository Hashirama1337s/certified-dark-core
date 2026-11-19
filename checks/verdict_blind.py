"""Lead verdict for BAR-R1-BLIND (seal f47da860b7). Reads the blind seat's RESULT.json and scores PB1-PB5 and PC exactly as sealed."""
import json, sys
d = json.load(open(sys.argv[1]))
s = d['sigma0_9_5']; h = d['sigma0_1_2']
out = {}
E = float(s['background']['E']); m = float(s['background']['m_int_sigma2_r2_dr'])
out['PB1'] = 'HOLD' if (-3.1055 <= E <= -3.1054 and 19.158 <= m <= 19.159) else 'FAIL'
want_p, want_m = (2, 1, 1, 0), (1, 1, 1, 0)
got_p = tuple(s['L'][str(L)]['n_Lplus'] for L in range(4)); got_m = tuple(s['L'][str(L)]['n_Lminus'] for L in range(4))
allruns = all(len(set(s['L'][str(L)]['n_Lplus_all_runs'])) == 1 and len(set(s['L'][str(L)]['n_Lminus_all_runs'])) == 1 for L in range(4))
out['PB2'] = 'HOLD' if (got_p == want_p and got_m == want_m and allruns) else 'FAIL'
neg = [1.1049110805, 0.5399256680, 0.2968148506]; pos = [1.2592133714, 0.9510282377, 0.5179458643]
absE = abs(E); pb3 = pb4 = True; det = {}
for L in range(3):
    modes = [(float(x['w']), x['krein']) for x in s['L'][str(L)]['internal_modes_converged'] if 0 < float(x['w']) < absE]
    negs = [w for w, k in modes if k < 0]
    ok3 = len(negs) == 1 and abs(negs[0] - neg[L]) / neg[L] < 1e-4
    ok4 = any(k > 0 and abs(w - pos[L]) / pos[L] < 1e-4 for w, k in modes)
    det[L] = dict(neg=negs, ok3=ok3, ok4=ok4); pb3 &= ok3; pb4 &= ok4
out['PB3'] = 'HOLD' if pb3 else 'FAIL'; out['PB4'] = 'HOLD' if pb4 else 'FAIL'
mre = {L: s['L'][str(L)]['max_re_lambda_excluding_generalised_kernel'] for L in range(4)}
try:
    out['PB5'] = 'HOLD' if all(float(v) < 1e-3 for v in mre.values()) and len(s['discretisations']) >= 2 else 'FAIL'
except Exception as e:
    out['PB5'] = 'UNREADABLE %r' % (mre,)
L0 = h['L']['0']
lam = L0['unstable_mode']
out['PC_raw'] = lam
print(json.dumps(dict(scores=out, detail=det, maxRe=mre), indent=1, default=str))
print('PC raw:', json.dumps(lam, default=str))
print('maxRe run-to-run:', {L: s['L'][str(L)]['eigenvalues_Re_gt_1em7_all_runs'] for L in range(4)})
