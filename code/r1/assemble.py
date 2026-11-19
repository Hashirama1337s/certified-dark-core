"""assemble.py - runs the certified instruments for one named job and writes one JSON of node results.

Jobs (see BAR-R1-FINAL.md):
  target-B   n=1 repulsive, sigma0 = 1.80, R1 = 26: background (B, virial), brackets R = 10, 14, L = 0..3 (CU*, CL*,
             D0, C-R), w-Neumann test at R = 14 (C-W)
  target-K0, target-K1, target-K2   Krein node I_L and the co-batched positive-Krein control PK_L (one run per L)
             ** sealed: run only after the lead seals BAR-R1-FINAL (assemble.py refuses without SEALED.ok) **
  C-B1     attractive n=0 at sigma0 = 0.191 and 1.047 (calibration: sigma0 values are post hoc)
  C-B2     Schroedinger-Poisson n=0 and n=1 at sigma0 = 1 (E/N^2 ratio)
  C-P1     repulsive n=0 at sigma0 = 1.80: brackets R = 10, 14, L = 0..3 (+ C-R on this background, + C-W)
  C-P2     SP n=1 sigma0 = 1, L = 0: brackets R = 20, 28 (+D0) and the certified quartet (evans)
  C-P3     SP n=1 sigma0 = 1, L = 2: brackets R = 20, 28 and the certified real pair (evans)
  NULL     repulsive n=1 at sigma0 = 0.50, L = 0: certified quartet (evans); brackets L = 0, 2 at R = 24, 32
  CAL-K    SP n=1 sigma0 = 1, L = 1: krein.py on one negative- and one positive-Krein eigenvalue (instrument calibration)
"""
import sys, os, json, time
from flint import arb
import bg_tube as bt
import bracket as br
import krein as kr
import evans as ev
import itaylor as it

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')

TARGET = dict(s=1, n=1, sig0=1.80, R1=26.0)
# REFEREE-R1-FINAL item 1: every instrument reads sigma0 through itaylor.exact, i.e. as the exact rational below
# (an arb ball around 9/5), never as the binary double 1.8000000000000000444...
assert it.Fraction(repr(TARGET['sig0'])) == it.Fraction(9, 5)
TARGET['sig0_exact'] = '9/5'
# Newton starting guesses only (float values from DESIGN/referee-2 smoke); the certificate decides.
TARGET_KREIN = {0: dict(neg=1.1048, pos=1.2618), 1: dict(neg=0.5400, pos=0.9511), 2: dict(neg=0.2968, pos=0.5179)}


def S(x, d=12):
    return x.str(d, radius=True) if isinstance(x, arb) else x


def bg_info(s, n, sig0, R1):
    steps, info, Yend = bt.get_tube(s, n, sig0, R1)
    keep = ('E', 'm', 'N', 'I1', 'u0', 'T', 'F', 'D', 'virial', 'virial_rel', 'kappa1', 'a1', 'zeros', 'tail_ok',
            'existence_certified', 'R1', 'u_R1', 'classify', 'delta', 'prec', 'K', 'tube_sha256', 'tube_source')
    d = {k: S(info[k]) for k in keep if k in info}
    d['nsteps'] = len(steps)
    d['sig0_exact'] = str(it.Fraction(repr(sig0)))
    d['virial_rel_upper'] = it.fup(info['virial_rel']) if 'virial_rel' in info else None   # outward (was float())
    return d, info


def job_target_B():
    """target part 1: background, virial, brackets (CU, CL, D0, C-R) and C-W."""
    t0 = time.time()
    c = TARGET
    out = dict(job='target-B', config=c)
    out['B'], info = bg_info(c['s'], c['n'], c['sig0'], c['R1'])
    out['D1'] = S(3 * info['m'] / 4)
    out['brackets'] = br.run(c['s'], c['n'], c['sig0'], c['R1'], [10.0, 14.0], 1e-3, [0, 1, 2, 3])
    out['CW'] = br.wneumann_test(c['s'], c['n'], c['sig0'], c['R1'], 14.0)
    out['seconds'] = time.time() - t0
    return out


def job_target_K(L):
    """target parts 2-4: Krein node I_L and its co-batched positive-Krein control PK_L (one run per L)."""
    t0 = time.time()
    c = TARGET
    bj, info = kr.build(c['s'], c['n'], c['sig0'], c['R1'])
    g = TARGET_KREIN[L]
    out = dict(job='target-K%d' % L, config=c, L=L,
               neg=kr.krawczyk(bj, info, L, c['s'], c['sig0'], g['neg'], 8.0),
               pos=kr.krawczyk(bj, info, L, c['s'], c['sig0'], g['pos'], 8.0))
    out['tube_sha256'] = info.get('tube_sha256'); out['tube_source'] = info.get('tube_source')
    out['seconds'] = time.time() - t0
    return out


def job_CB1():
    out = dict(job='C-B1')
    out['sig0.191'], _ = bg_info(-1, 0, 0.191, 66.0)
    out['sig1.047'], _ = bg_info(-1, 0, 1.047, 31.0)
    return out


def job_CB2():
    out = dict(job='C-B2')
    d0, i0 = bg_info(0, 0, 1.0, 28.0)
    d1, i1 = bg_info(0, 1, 1.0, 48.0)
    out['n0'] = d0; out['n1'] = d1
    rat = (i1['E'] / (i1['N'] * i1['N'])) / (i0['E'] / (i0['N'] * i0['N']))
    out['E1_over_E0_equal_N'] = S(rat)
    out['ratio_lo'] = it.flo(rat); out['ratio_hi'] = it.fup(rat)          # outward (was float())
    return out


def job_CP1():
    out = dict(job='C-P1', config=dict(s=1, n=0, sig0=1.80, R1=20.0))
    out['B'], _ = bg_info(1, 0, 1.80, 20.0)
    out['brackets'] = br.run(1, 0, 1.80, 20.0, [10.0, 14.0], 1e-3, [0, 1, 2, 3])
    out['CW'] = br.wneumann_test(1, 0, 1.80, 20.0, 14.0)
    return out


def job_SP(Ls, name):
    out = dict(job=name, config=dict(s=0, n=1, sig0=1.0, R1=48.0))
    out['B'], info = bg_info(0, 1, 1.0, 48.0)
    out['brackets'] = br.run(0, 1, 1.0, 48.0, [20.0, 28.0], 1e-3, Ls)
    bj, info = ev.build(0, 1, 1.0, 48.0)
    if name == 'C-P2':
        out['evans'] = ev.certify(bj, info, 0, 0, 1.0, complex(0.0883, 0.5829), 10.0)
    else:
        out['evans'] = ev.certify(bj, info, 2, 0, 1.0, complex(0.0992, 0.0), 10.0)
    out['CW'] = br.wneumann_test(0, 1, 1.0, 48.0, 20.0)
    return out


def job_NULL():
    out = dict(job='NULL', config=dict(s=1, n=1, sig0=0.5, R1=60.0))
    out['B'], info = bg_info(1, 1, 0.5, 60.0)
    out['brackets'] = br.run(1, 1, 0.5, 60.0, [24.0, 32.0], 1e-3, [0, 2])
    bj, info = ev.build(1, 1, 0.5, 60.0)
    out['evans'] = ev.certify(bj, info, 0, 1, 0.5, complex(0.0241, 0.2832), 14.0)
    return out


def job_CALK():
    out = dict(job='CAL-K', config=dict(s=0, n=1, sig0=1.0, R1=48.0, L=1))
    bj, info = kr.build(0, 1, 1.0, 48.0)
    out['neg'] = kr.krawczyk(bj, info, 1, 0, 1.0, 0.1763, 10.0)
    out['pos'] = kr.krawczyk(bj, info, 1, 0, 1.0, 0.3646, 10.0)
    return out


JOBS = {'target-B': job_target_B, 'target-K0': lambda: job_target_K(0), 'target-K1': lambda: job_target_K(1),
        'target-K2': lambda: job_target_K(2), 'C-B1': job_CB1, 'C-B2': job_CB2, 'C-P1': job_CP1,
        'C-P2': lambda: job_SP([0], 'C-P2'), 'C-P3': lambda: job_SP([2], 'C-P3'), 'NULL': job_NULL, 'CAL-K': job_CALK}


if __name__ == '__main__':
    name = sys.argv[1]
    if name.startswith('target') and not os.path.exists(os.path.join(HERE, 'SEALED.ok')):
        print('refusing: the target run waits for the seal (create SEALED.ok only after the lead seals AMENDMENT-R1-1)')
        sys.exit(2)
    if name.startswith('target'):
        bt.DISK_CACHE = False      # REFEREE-R1-FINAL item 5: the target tube is rebuilt inside this run, never cached
    t0 = time.time()
    res = JOBS[name]()
    res['wall_seconds'] = time.time() - t0
    os.makedirs(os.path.join(OUT, 'cal'), exist_ok=True)
    fn = os.path.join(OUT, (name + '.json') if name.startswith('target') else os.path.join('cal', name + '.json'))
    json.dump(res, open(fn, 'w'), indent=1, default=str)
    print('wrote', fn, 'wall %.0f s' % res['wall_seconds'])
