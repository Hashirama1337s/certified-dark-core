"""assemble.py (build-3) - runs the certified instruments for one named job and writes one JSON of node results.

build-3 generalises the R1 target to any point sigma0 = p/q (R2-BAND). Point jobs are named <KIND>:<tag>:
  B:<tag>     background (B, virial), brackets R = 10, 14, L = 0..3 (CU*, CL*, D0, C-R), w-Neumann test at R = 14 (C-W)
  K0:<tag>, K1:<tag>, K2:<tag>
              Krein node I_L (negative-Krein guess) and the co-batched positive-Krein control PK_L (its colliding /
              next-above partner), one run per L; Cauchy disc radius disc_r = min(0.002, gap/4) (gap = guess gap),
              plus the separation record of the two certified w (capture, disjointness, disc excludes the other mode)
  U:<tag>     background (B) and a complex Krawczyk enclosure (evans.py) of one eigenvalue with Re lam > 0 in the named
              sector, from a float guess; disc_r = min(0.002, Re(guess)/2)
  A point is run in mode 'stable' (B + K0 + K1 + K2) or mode 'unstable' (U only).
  ** every point job refuses to run unless SEALED-<tag>.ok exists (one file per job set) **, except the calibration
  tags in PROBE_TAGS, whose sigma0 is asserted NOT to be any sealed-candidate point.
Controls (identical to build-2; see BAR-R1-FINAL.md):
  C-B1     attractive n=0 at sigma0 = 0.191 and 1.047 (calibration: sigma0 values are post hoc)
  C-B2     Schroedinger-Poisson n=0 and n=1 at sigma0 = 1 (E/N^2 ratio)
  C-P1     repulsive n=0 at sigma0 = 1.80: brackets R = 10, 14, L = 0..3 (+ C-R on this background, + C-W)
  C-P2     SP n=1 sigma0 = 1, L = 0: brackets R = 20, 28 (+D0) and the certified quartet (evans)
  C-P3     SP n=1 sigma0 = 1, L = 2: brackets R = 20, 28 and the certified real pair (evans)
  NULL     repulsive n=1 at sigma0 = 0.50, L = 0: certified quartet (evans); brackets L = 0, 2 at R = 24, 32
  CAL-K    SP n=1 sigma0 = 1, L = 1: krein.py on one negative- and one positive-Krein eigenvalue (instrument calibration)
New build-3 calibration jobs (not R1 controls):
  CAL-KD   CAL-K with the Cauchy disc shrunk to 0.0005 (disc-adaptation check: the certificate must not depend on it)
  CAL-ED   C-P2's evans enclosure alone with the disc shrunk to 0.0005 (same check, complex route)
"""
import sys, os, json, time, math
from fractions import Fraction
from flint import arb
import bg_tube as bt
import bracket as br
import krein as kr
import evans as ev
import itaylor as it

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')

DISC_MAX = 0.002          # the R1 Cauchy disc radius; build-3 never uses a larger one

# ---------------------------------------------------------------------------------------------------------------------
# Points. sig0 is the exact rational; the float label handed to the instruments must read back as exactly that
# rational through itaylor.exact (Fraction(repr(float))) - asserted in point(). Newton guesses are float starting
# values only (from the NOT SEALED float map core/band/map: edge fits through the +-1e-4 and +-0.002 offsets of
# edge_lo1.json / edge_hi1.json, otherwise linear interpolation of sw_f1/sw_f2; script aux/b3guess.py). The
# certificate decides; a guess never enters an enclosure.
#   krein: {L: (neg guess, pos guess)}   unstable: (L, complex guess)
# ---------------------------------------------------------------------------------------------------------------------
R1_KREIN = {0: (1.1048, 1.2618), 1: (0.5400, 0.9511), 2: (0.2968, 0.5179)}      # build-2 TARGET_KREIN, unchanged
POINTS = {
    # regression of the parameterised path: the R1 point (sealed 07faff6621 + AMENDMENT-R1-1, already certified)
    'r1':    dict(sig0='9/5', mode='stable', krein=R1_KREIN),
    # R2-BAND proposed points (sealed candidates)
    'lo-u':  dict(sig0='1595/1000', mode='unstable', unstable=(0, complex(0.0051617, 1.0137197))),
    'lo-s':  dict(sig0='1597/1000', mode='stable', krein={0: (1.01157, 1.01906), 1: (0.4543, 0.80839), 2: (0.20178, 0.49162)}),
    'hi-s':  dict(sig0='1983/1000', mode='stable', krein={0: (1.21808, 1.4641), 1: (0.62237, 1.088), 2: (0.45398, 0.47273)}),
    'hi-u':  dict(sig0='1985/1000', mode='unstable', unstable=(2, complex(0.0082411, 0.4639756))),
    'g165':  dict(sig0='33/20', mode='stable', krein={0: (1.02312, 1.0926), 1: (0.47605, 0.84468), 2: (0.22398, 0.50082)}),
    'g170':  dict(sig0='17/10', mode='stable', krein={0: (1.04814, 1.14914), 1: (0.49696, 0.87953), 2: (0.2464, 0.50821)}),
    'g175':  dict(sig0='7/4', mode='stable', krein={0: (1.07581, 1.20427), 1: (0.51825, 0.91498), 2: (0.27053, 0.51407)}),
    'g185':  dict(sig0='37/20', mode='stable', krein={0: (1.13497, 1.31444), 1: (0.56197, 0.98767), 2: (0.32601, 0.5191)}),
    'g190':  dict(sig0='19/10', mode='stable', krein={0: (1.16574, 1.37016), 1: (0.58438, 1.0249), 2: (0.35967, 0.51598)}),
    'g195':  dict(sig0='39/20', mode='stable', krein={0: (1.1971, 1.42652), 1: (0.60715, 1.06272), 2: (0.40233, 0.50402)}),
    # calibration tags (NOT sealed candidates): timing probe and unstable-route positive controls on the same family
    'p161':  dict(sig0='161/100', mode='stable', krein={0: (1.00878, 1.04259), 1: (0.45959, 0.81723), 2: (0.20709, 0.494)}),
    # lead addition 11-18 (prior-art gate): two unstable points inside the paper's claimed band "1.55 <~ sigma0 <~ 2.07"
    'in-155': dict(sig0='31/20', mode='unstable', unstable=(0, complex(0.029367442, 0.978168536))),   # chk_1.55_0.json
    'in-200': dict(sig0='2', mode='unstable', unstable=(2, complex(0.035387296, 0.468617454))),       # sw_f2.json, 2.00
    'u150':  dict(sig0='3/2', mode='unstable', unstable=(0, complex(0.040312956, 0.939259160))),      # sw_f1.json, 1.50
    'u205':  dict(sig0='41/20', mode='unstable', unstable=(2, complex(0.073523517, 0.48414557))),
}
for _p in POINTS.values():
    _p.setdefault('R1', 26.0); _p.setdefault('r_m', 8.0); _p.setdefault('s', 1); _p.setdefault('n', 1)
PROBE_TAGS = ('p161', 'u150', 'u205')
SEALED_CANDIDATES = [t for t in POINTS if t not in PROBE_TAGS]
for _t in PROBE_TAGS:       # a calibration tag may never sit on a sealed-candidate point
    assert all(Fraction(POINTS[_t]['sig0']) != Fraction(POINTS[c]['sig0']) for c in SEALED_CANDIDATES), _t


def point(tag):
    p = dict(POINTS[tag])
    F = Fraction(p['sig0'])
    x = float(F)
    assert Fraction(repr(x)) == F, 'sigma0 %s has no short float label that reads back exactly' % p['sig0']
    p['sig0_label'] = x
    p['sig0_exact'] = str(F)
    p['tag'] = tag
    return p


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


def job_point_B(tag):
    """stable part 1: background, virial, brackets (CU, CL, D0, C-R) and C-W (= R1 target-B at sigma0 = p/q)."""
    t0 = time.time()
    c = point(tag)
    out = dict(job='B:' + tag, config=c)
    x = c['sig0_label']
    out['B'], info = bg_info(c['s'], c['n'], x, c['R1'])
    out['D1'] = S(3 * info['m'] / 4)
    out['brackets'] = br.run(c['s'], c['n'], x, c['R1'], [10.0, 14.0], 1e-3, [0, 1, 2, 3])
    out['CW'] = br.wneumann_test(c['s'], c['n'], x, c['R1'], 14.0)
    out['seconds'] = time.time() - t0
    return out


def separation(neg, pos, gneg, gpos, disc_r):
    """record (descriptive, outward floats) that the two certificates found two DIFFERENT modes near their guesses and
    that each Cauchy disc (a square of half-width disc_r about the Krawczyk centre) stays clear of the other mode."""
    gap = abs(gpos - gneg)
    r = dict(gap_guess=gap, disc_r=disc_r, disc_rule='min(0.002, gap/4)')
    if not (neg.get('ok') and pos.get('ok')):
        r['ok'] = False; r['why'] = 'a Krawczyk test did not contract'
        return r
    r['neg_capture'] = abs(neg['w_mid'] - gneg) < gap / 4
    r['pos_capture'] = abs(pos['w_mid'] - gpos) < gap / 4
    lo, hi = (neg, pos) if neg['w_hi'] < pos['w_lo'] else (pos, neg)
    r['disjoint'] = bool(lo['w_hi'] < hi['w_lo'])
    dist_lo = hi['w_lo'] - lo['w_hi']                  # lower bound on |w_neg* - w_pos*| from the certified boxes
    r['certified_separation_lower'] = dist_lo
    # centre-to-other-mode distance >= dist_lo; the square's farthest point is disc_r * sqrt(2) from its centre
    r['disc_excludes_other'] = bool(r['disjoint'] and disc_r * 1.4143 < dist_lo)
    r['ok'] = bool(r['neg_capture'] and r['pos_capture'] and r['disjoint'] and r['disc_excludes_other'])
    return r


def job_point_K(tag, L):
    """stable parts 2-4: Krein node I_L and its co-batched positive-Krein control PK_L (one run per L)."""
    t0 = time.time()
    c = point(tag)
    x = c['sig0_label']
    gneg, gpos = c['krein'][L]
    disc_r = min(DISC_MAX, abs(gpos - gneg) / 4)
    bj, info = kr.build(c['s'], c['n'], x, c['R1'])
    out = dict(job='K%d:%s' % (L, tag), config=c, L=L,
               neg=kr.krawczyk(bj, info, L, c['s'], x, gneg, c['r_m'], disc_r=disc_r),
               pos=kr.krawczyk(bj, info, L, c['s'], x, gpos, c['r_m'], disc_r=disc_r))
    out['separation'] = separation(out['neg'], out['pos'], gneg, gpos, disc_r)
    out['tube_sha256'] = info.get('tube_sha256'); out['tube_source'] = info.get('tube_source')
    out['seconds'] = time.time() - t0
    return out


def job_point_U(tag):
    """unstable point: background B and a Krawczyk-certified eigenvalue with Re lam > 0 in the named sector."""
    t0 = time.time()
    c = point(tag)
    x = c['sig0_label']
    L, lam0 = c['unstable']
    disc_r = min(DISC_MAX, abs(lam0.real) / 2)
    out = dict(job='U:' + tag, config=dict(c, unstable=[L, str(lam0)]), L=L)
    out['B'], info = bg_info(c['s'], c['n'], x, c['R1'])
    bj, info = ev.build(c['s'], c['n'], x, c['R1'])
    out['evans'] = ev.certify(bj, info, L, c['s'], x, lam0, c['r_m'], disc_r=disc_r)
    out['evans']['disc_rule'] = 'min(0.002, Re(guess)/2)'
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


def job_CALK(disc_r=DISC_MAX, name='CAL-K'):
    out = dict(job=name, config=dict(s=0, n=1, sig0=1.0, R1=48.0, L=1, disc_r=disc_r))
    bj, info = kr.build(0, 1, 1.0, 48.0)
    out['neg'] = kr.krawczyk(bj, info, 1, 0, 1.0, 0.1763, 10.0, disc_r=disc_r)
    out['pos'] = kr.krawczyk(bj, info, 1, 0, 1.0, 0.3646, 10.0, disc_r=disc_r)
    return out


def job_CALED():
    out = dict(job='CAL-ED', config=dict(s=0, n=1, sig0=1.0, R1=48.0, L=0, disc_r=0.0005))
    bj, info = ev.build(0, 1, 1.0, 48.0)
    out['evans'] = ev.certify(bj, info, 0, 0, 1.0, complex(0.0883, 0.5829), 10.0, disc_r=0.0005)
    return out


JOBS = {'C-B1': job_CB1, 'C-B2': job_CB2, 'C-P1': job_CP1,
        'C-P2': lambda: job_SP([0], 'C-P2'), 'C-P3': lambda: job_SP([2], 'C-P3'), 'NULL': job_NULL, 'CAL-K': job_CALK,
        'CAL-KD': lambda: job_CALK(0.0005, 'CAL-KD'), 'CAL-ED': job_CALED}
KINDS = {'B': job_point_B, 'K0': lambda t: job_point_K(t, 0), 'K1': lambda t: job_point_K(t, 1),
         'K2': lambda t: job_point_K(t, 2), 'U': job_point_U}


if __name__ == '__main__':
    name = sys.argv[1]
    if ':' in name:
        kind, tag = name.split(':', 1)
        if kind not in KINDS or tag not in POINTS:
            print('unknown job', name); sys.exit(2)
        if tag not in PROBE_TAGS and not os.path.exists(os.path.join(HERE, 'SEALED-%s.ok' % tag)):
            print('refusing: %s waits for the seal (create SEALED-%s.ok only after the lead seals BAR-R2-EDGES)' % (name, tag))
            sys.exit(2)
        bt.DISK_CACHE = False      # REFEREE-R1-FINAL item 5: every point tube is rebuilt inside its run, never cached
        t0 = time.time()
        res = KINDS[kind](tag)
        res['wall_seconds'] = time.time() - t0
        os.makedirs(os.path.join(OUT, tag), exist_ok=True)
        fn = os.path.join(OUT, tag, kind + '.json')
    else:
        if name not in JOBS:
            print('unknown job', name); sys.exit(2)
        t0 = time.time()
        res = JOBS[name]()
        res['wall_seconds'] = time.time() - t0
        os.makedirs(os.path.join(OUT, 'cal'), exist_ok=True)
        fn = os.path.join(OUT, 'cal', name + '.json')
    json.dump(res, open(fn, 'w'), indent=1, default=str)
    print('wrote', fn, 'wall %.0f s' % res['wall_seconds'])
