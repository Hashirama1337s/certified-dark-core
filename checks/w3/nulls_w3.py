"""referee-W3: the checker must be able to FAIL. Mutate copies of real JSON in memory and confirm each mutation is caught."""
import json, copy, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import check_w3 as C

BW = C.BW
real_load = json.load
MUT = {}


def fake_load(fh):
    d = real_load(fh)
    name = os.path.basename(os.path.dirname(fh.name)) + '/' + os.path.basename(fh.name)
    f = MUT.get(name)
    return f(copy.deepcopy(d)) if f else d


json.load = fake_load


def run(label, key, f, kind, args):
    MUT.clear(); MUT[key] = f
    r = C.node_check(*args) if kind == 'node' else C.cell_check(*args)
    print('%-58s caught=%s  %s' % (label, bool(r['problems']), r['problems'][:2]))
    return bool(r['problems'])


nodes = {('n' + str(int(C.F(s) * 1000))): C.node_check('n' + str(int(C.F(s) * 1000)), s) for s in C.NODES}
cargs = ('c05', C.NODES[4], C.NODES[5], nodes)
c01 = ('c01', C.NODES[0], C.NODES[1], nodes)
res = []
res.append(run('honest c05 (must NOT be caught)', 'none', None, 'cell', cargs) is False)


def scaleC1(d, fac=2.4):
    d['CH']['0']['C1'] = '[%r +/- 1e-9]' % (C.F(d['CH']['0']['C1'].split()[0][1:]) * C.F(fac)).__float__(); return d


res.append(run('c05 eta2 C1(L0) x 2.4 (CC must fail)', 'cells/c05.json', scaleC1, 'cell', cargs))
res.append(run('c05 eta2 C1(L0) x 2.2 (honest ratio 2.336: must pass)', 'cells/c05.json', lambda d: scaleC1(d, 2.2), 'cell', cargs) is False)


def bigZ1(d):
    d['BR'][1]['Z1'] = '[1.0001 +/- 1e-9]'; return d


res.append(run('c05 half-2 Z1 = 1.0001', 'cells/c05.json', bigZ1, 'cell', cargs))


def bigrho(d):
    d['BR'][0]['Y0'] = '[0.004 +/- 1e-9]'; return d


res.append(run('c05 half-1 Y0 = 4e-3 (rho > r_u)', 'cells/c05.json', bigrho, 'cell', cargs))


def piv(d):
    d['certs']['H(w2) L1']['db']['S_pivots'][0] = '[0.01 +/- 1e-6]'; return d


res.append(run('c05 positive Haynsworth pivot', 'cells/c05.json', piv, 'cell', cargs))


def nb(d):
    d['certs']['H(0) L0']['da']['nB'] = 5; return d


res.append(run('c05 H(0) L0 count 5', 'cells/c05.json', nb, 'cell', cargs))


def wck(d):
    d['certs']['RITZ L1']['w1b'] = d['certs']['H(w2) L1']['wb'] + 1e-6; return d


res.append(run('c05 w1 > w2 at end b', 'cells/c05.json', wck, 'cell', cargs))


def absE(d):
    d['absE_lower'] = '[1.05 +/- 1e-6]'; return d


res.append(run('c05 |E| lower 1.05 (< w2 L0)', 'cells/c05.json', absE, 'cell', cargs))


def sha(d):
    d['tube_sha'][1] = 'ab' + d['tube_sha'][1][2:]; return d


res.append(run('c05 tube sha altered', 'cells/c05.json', sha, 'cell', cargs))


def pen(d):
    d['certs']['PEN']['da']['sherman'] = '[0.001 +/- 1e-9]'; return d


res.append(run('c05 PEN Sherman-Morrison > 0', 'cells/c05.json', pen, 'cell', cargs))


def ma(d):
    d['certs']['H(w2) L0']['ma'] = '[5.03101e-5 +/- 8.74e-12]'; d['CH']['0']['C0'] = '[6e-5 +/- 1e-9]'; return d


res.append(run('c01 C0 above the end margin', 'cells/c01.json', ma, 'cell', c01))


def k14(d):
    d['brackets']['14.0']['2']['-']['upper'] = 2; return d


res.append(run('node n1650 bracket U-(2) = 2 (K14 != 2,2,2,0)', 'n1650/N.json', k14, 'node', ('n1650', '33/20')))


def alpha(d):
    d['green']['alpha'] = '[0 +/- 1e-3]'; return d


res.append(run('node n1650 alpha contains 0', 'n1650/N.json', alpha, 'node', ('n1650', '33/20')))
print('NULLS: %d/%d behave as required' % (sum(res), len(res)))
