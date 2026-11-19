"""assemble_w.py - build-W job runner (R3-WINDOW): node / cell schedule, controls, seal guard.

Job kinds:
  N:<tag>          node certificate (node.node) -> out/<tag>/N.json            [needs SEALED-<tag>.ok]
  C:<cell id>      cell certificate (cell.run_cell) -> out/cells/<id>.json      [needs SEALED-<id>.ok]
  XK:<g9 tag>      control XK (node.xk)            -> out/controls/XK_<tag>.json (no seal: certified G9 nodes)
  XU:<tag>[:<step>[:<jlo>-<jhi>]] control XU (node.xu) -> out/controls/XU_<tag>.json or XU_<tag>_part<jlo>-<jhi>.json
  LOO:<name>       control leave-one-out cell     -> out/controls/LOO_<name>.json
  XI               control injected tau            -> out/controls/XI.json
  R1REG            regression: brackets at 9/5 equal build-3/out/r1/B.json counts
The window target (any N/C job) refuses to run unless the lead's SEALED-<tag>.ok exists (exit 2). Controls touch only
G9 nodes, the unstable control nodes 1595/1000 and 1985/1000, and the two LOO cells, by design."""
import sys, os, json, time
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

NODES = ['1597/1000', '1600/1000', '1605/1000', '1612/1000', '1625/1000', '33/20', '1675/1000', '17/10', '1725/1000',
         '7/4', '1775/1000', '9/5', '1825/1000', '37/20', '1875/1000', '19/10', '1925/1000', '39/20', '1962/1000',
         '1970/1000', '1976/1000', '1980/1000', '1983/1000']
def ntag(s):
    return 'n%04d' % int(Fraction(s) * 1000)
CELLS = [(NODES[i], NODES[i + 1]) for i in range(len(NODES) - 1)]
def ctag(i):
    return 'c%02d' % (i + 1)
END_CELLS = {0, len(CELLS) - 1}                      # R = 20 (DESIGN-W2 failure mode 4)
# LOO cells: interior node certified in R2 (B:p161, U:lo-u tubes); widths 0.053 / 0.047 (the referee's example
# [7/4, 37/20] has width 0.1: BR does not close there, Z1 = 1.17 (CALIBRATION.md), so it is reported, not used as gate)
LOO_CELLS = {'loo-161': ('1597/1000', '33/20', '161/100'), 'loo-1595': ('31/20', '1597/1000', '1595/1000'),
             'loo-185w': ('7/4', '37/20', '9/5')}
LOO_GATES = ('loo-161', 'loo-1595')
G9_SIGMA = {'1597/1000', '33/20', '17/10', '7/4', '9/5', '37/20', '19/10', '39/20', '1983/1000'}
assert all(Fraction(a) < Fraction(b) for a, b in CELLS) and Fraction(NODES[0]) == Fraction(1597, 1000) and Fraction(NODES[-1]) == Fraction(1983, 1000)


def sealed(tag):
    return os.path.exists(os.path.join(HERE, 'SEALED-%s.ok' % tag))


def dump(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(obj, f, indent=1, default=str)


def main(job):
    kind, _, arg = job.partition(':')
    t0 = time.time()
    import node as nd
    if kind in ('N', 'C'):
        assert 'WSU' not in os.environ, 'WSU must be unset for sealed jobs (green.SU = 3)'
    if kind == 'N':
        if not sealed(arg):
            print('REFUSED: %s needs SEALED-%s.ok' % (job, arg)); sys.exit(2)
        s0 = {ntag(s): s for s in NODES}[arg]
        rec = nd.node(arg, s0)
        dump(rec, os.path.join(HERE, 'out', arg, 'N.json'))
    elif kind == 'C':
        if not sealed(arg):
            print('REFUSED: %s needs SEALED-%s.ok' % (job, arg)); sys.exit(2)
        i = int(arg[1:]) - 1
        a, b = CELLS[i]
        import cell
        Na = json.load(open(os.path.join(HERE, 'out', ntag(a), 'N.json'))); Nb = json.load(open(os.path.join(HERE, 'out', ntag(b), 'N.json')))
        A = cell.NodeData(a, *nd.load_tube(ntag(a), Na['tube_sha256'])); B = cell.NodeData(b, *nd.load_tube(ntag(b), Nb['tube_sha256']))
        rec = cell.run_cell(A, B, R=20.0)        # R = 20 everywhere (XK calibration: R = 14 moves the L = 0 crossing at w+)
        dump(rec, os.path.join(HERE, 'out', 'cells', arg + '.json'))
    elif kind == 'XK':
        rec = nd.xk(arg)
        dump(rec, os.path.join(HERE, 'out', 'controls', 'XK_%s.json' % arg))
    elif kind == 'XU':
        tag, _, rest = arg.partition(':')
        step, _, rng = rest.partition(':')
        if rng:
            jlo, jhi = [int(v) for v in rng.split('-')]
            rec = nd.xu(tag, wstep=step or '0.01', jlo=jlo, jhi=jhi)
            dump(rec, os.path.join(HERE, 'out', 'controls', 'XU_%s_part%d-%d.json' % (tag, jlo, jhi)))
        else:
            rec = nd.xu(tag, wstep=step or '0.01')
            dump(rec, os.path.join(HERE, 'out', 'controls', 'XU_%s.json' % tag))
    elif kind == 'LOO':
        import cell
        a, b, c = LOO_CELLS[arg]
        A = cell.NodeData(a, *nd.tube(a)); B = cell.NodeData(b, *nd.tube(b)); C = cell.TubeOnly(c, *nd.tube(c))
        rec = cell.run_cell(A, B, R=20.0, loo=C, sectors=('--sectors' in sys.argv))
        rec['job'] = job
        dump(rec, os.path.join(HERE, 'out', 'controls', 'LOO_%s.json' % arg))
    elif kind == 'XI':
        import cell, numpy as np
        from flint import arb
        a, b, _ = LOO_CELLS['loo-161']
        A = cell.NodeData(a, *nd.tube(a)); B = cell.NodeData(b, *nd.tube(b))
        def inject(N, taug):
            """tau_b + 1e-3 bump (a and W parts, Gaussian bump centred at r = 3) at every grid point."""
            out = {}
            for i, v in taug.items():
                rr = N.bj.r[i]
                bump = (-(rr - 3) ** 2).exp() * arb('0.001')
                out[i] = [v[0] + bump, v[1] + bump, v[2], v[3]]
            return out
        rec = cell.run_cell(A, B, R=20.0, inject=inject, sectors=False)
        rec['job'] = 'XI'; rec['PASS'] = rec.get('outcome') == 'REJECTED'
        dump(rec, os.path.join(HERE, 'out', 'controls', 'XI.json'))
    elif kind == 'R1REG':
        import bracket as br
        B = br.run(1, 1, 1.8, 26.0, [10.0, 14.0], 1e-3, [0, 1, 2, 3])
        ref = json.load(open(os.path.join(nd.B3OUT, 'r1', 'B.json')))
        diffs = []
        refr = ref['brackets']['radii'] if 'brackets' in ref else ref['radii']
        for R, rr in B['radii'].items():
            for L, row in rr.items():
                for w in '+-':
                    a1 = (row[w]['upper'], row[w]['lower'])
                    rw = refr[str(R)][str(L)][w]
                    if a1 != (rw['upper'], rw['lower']):
                        diffs.append((R, L, w, a1, (rw['upper'], rw['lower'])))
                if L == 0:
                    if row['D0'].get('constrained_upper') != refr[str(R)][str(L)]['D0'].get('constrained_upper'):
                        diffs.append((R, 'D0'))
        rec = dict(job='R1REG', tube_sha256=B['tube_sha256'], ref_sha=ref.get('tube_sha256') or ref.get('brackets', {}).get('tube_sha256'),
                   diffs=diffs, PASS=(len(diffs) == 0), seconds=B['seconds'])
        dump(rec, os.path.join(HERE, 'out', 'controls', 'R1REG.json'))
    else:
        print('unknown job', job); sys.exit(1)
    print('%s done in %.0f s' % (job, time.time() - t0))


if __name__ == '__main__':
    main(sys.argv[1])
