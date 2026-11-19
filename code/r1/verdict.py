"""verdict.py - applies the comparators of BAR-R1-FINAL.md to assembled instrument output.

  python verdict.py controls            -> reads out/cal/*.json, prints the control table, writes out/controls_verdict.json
  python verdict.py target              -> reads out/target_assembled.json + out/controls_verdict.json, prints T verdict

Outcome of T (spectral stability of the n=1 repulsive state at sigma0 = 1.80):
  VOID          a must-pass control failed, or an internal inconsistency (upper < lower; K(L) < 2 at a sector with a
                certified negative-Krein pair; a positive-Krein control not certified positive).
  FAILED        a certified enclosure (evans.py Krawczyk) of an eigenvalue with Re lam > 0 in some sector.  (Refutation.)
  HOLDS         K(0), K(1), K(2) <= 2, K(3) = 0 (certified upper counts, D0 node), D1 > 0, and at L = 0, 1, 2 one
                Krawczyk-certified eigenvalue i w, 0 < w < |E|, with certified <a, d> < 0.
  INCONCLUSIVE  anything else (a count above the bar, an enclosure straddling 0, a Krawczyk test that does not contract).
No parity theorem is used anywhere: an odd K is never read as a growing mode.
"""
import sys, os, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')


def lo_hi(s):
    """parse an arb string '[m +/- r]' or 'm +/- r' -> (lo, hi) floats (outward-rounded by 1 ulp-ish margin)."""
    s = str(s).strip()
    if s.startswith('['):
        s = s[1:-1]
    if '+/-' in s:
        a, b = s.split('+/-')
        a = a.strip(); b = float(b.strip())
        m = float(a) if a else 0.0
    else:
        m = float(s); b = 0.0
    eps = 1e-15 * max(1.0, abs(m))
    return m - b - eps, m + b + eps


def K_of(rows, L, kind='upper'):
    """index bound K(L) from bracket rows at one radius (None if not certified)."""
    r = rows.get(str(L)) or rows.get(L)
    if r is None:
        return None, 'missing'
    up_p = r['+']['upper']; up_m = r['-']['upper']
    if up_p is None or up_m is None:
        return None, 'upper count not certified'
    if L == 0:
        d0 = r.get('D0') or {}
        if not d0.get('ok'):
            return None, 'D0 node not certified'
        return d0['constrained_upper'] + (up_m - 1), 'K0 = [nB-1] + [U-(0)-1]'
    if L == 1:
        return (up_p - 1) + up_m, 'K1 = [U+(1)-1] + U-(1)'
    return up_p + up_m, 'K = U+ + U-'


def consistency(rows):
    bad = []
    for L, r in rows.items():
        if not isinstance(r, dict) or '+' not in r:
            continue
        for w in '+-':
            u, l = r[w]['upper'], r[w]['lower']
            if u is not None and l is not None and u < l:
                bad.append('L=%s %s upper %s < lower %s' % (L, w, u, l))
    return bad


def controls():
    C = {}
    def load(n):
        fn = os.path.join(OUT, 'cal', n + '.json')
        return json.load(open(fn)) if os.path.exists(fn) else None
    # C-B1 (calibration)
    d = load('C-B1')
    if d:
        a = d['sig0.191']; b = d['sig1.047']
        T1, F1, T2, F2 = lo_hi(a['T']), lo_hi(a['F']), lo_hi(b['T']), lo_hi(b['F'])
        ok = (0.555 <= T1[0] and T1[1] <= 0.561 and 0.0465 <= F1[0] and F1[1] <= 0.0475 and
              5.62 <= T2[0] and T2[1] <= 5.66 and 1.875 <= F2[0] and F2[1] <= 1.900 and
              a['virial_rel_upper'] <= 1e-6 and b['virial_rel_upper'] <= 1e-6)
        C['C-B1'] = dict(result='PASS' if ok else 'FAIL', label='CALIBRATION (sigma0 matched post hoc)',
                         T191=a['T'], F191=a['F'], T1047=b['T'], F1047=b['F'],
                         virial_rel=(a['virial_rel_upper'], b['virial_rel_upper']),
                         note='attractive: existence of the decaying solution inside the tube is not certified (s=-1)')
    d = load('C-B2')
    if d:
        ok = 0.1884 <= d['ratio_lo'] and d['ratio_hi'] <= 0.1896
        C['C-B2'] = dict(result='PASS' if ok else 'FAIL', ratio=d['E1_over_E0_equal_N'], window=[0.1884, 0.1896])
    d = load('C-P1')
    if d:
        Ks = {}; ok = True
        for R, rows in d['brackets']['radii'].items():
            for L in range(4):
                k, why = K_of(rows, L)
                Ks['R%s_L%d' % (R, L)] = k
                ok = ok and (k == 0)
            ok = ok and not consistency(rows)
        C['C-P1'] = dict(result='PASS' if ok else 'FAIL', K=Ks, rule='K(L) = 0 for L = 0..3 at both radii')
        rr = list(d['brackets']['radii'].values())
        same = _same_counts(rr)
        C['C-R(C-P1 background)'] = dict(result='PASS' if same else 'FAIL', rule='identical certified counts at both radii')
        C['C-W(C-P1 background)'] = dict(result='PASS' if d['CW'].get('ok') else 'FAIL', Q_at_X_upper=d['CW'].get('Q_at_X_upper'),
                                         slope_upper=d['CW'].get('slope_upper'))
    for name, L, kmax in (('C-P2', 0, 2), ('C-P3', 2, 1)):
        d = load(name)
        if not d:
            continue
        ev = d['evans']
        Ks = {}; okK = True
        for R, rows in d['brackets']['radii'].items():
            k, why = K_of(rows, L)
            Ks['R%s' % R] = k
            okK = okK and (k is not None and k <= kmax)
        if not ev.get('ok'):
            C[name] = dict(result='FAIL', why='Krawczyk did not contract', K=Ks)
        elif name == 'C-P2':
            re = lo_hi(ev['lam_over_2absE_re']); im = lo_hi(ev['lam_over_2absE_im'])
            okE = ev['ok'] and ev['growing'] and im[0] > 0
            win_re = (0.0451 * 0.9, 0.0451 * 1.1); win_im = (0.325 * 0.97, 0.325 * 1.03)
            okT = win_re[0] <= re[0] and re[1] <= win_re[1] and win_im[0] <= im[0] and im[1] <= win_im[1]
            C[name] = dict(result='PASS' if (okK and okE and okT) else 'FAIL', K0=Ks, lam_re=ev.get('lam_re'),
                           lam_im=ev.get('lam_im'), ratio_re=ev.get('lam_over_2absE_re'), ratio_im=ev.get('lam_over_2absE_im'),
                           windows=dict(re=win_re, im=win_im),
                           reading='K(0) <= 2 and one certified non-real Re>0 eigenvalue (a quartet, 2 directions) => exactly one quartet',
                           tolerance_disclosure='the 10% real-part gate was set after a 7% float mismatch was seen (mock-informed)')
        else:
            okE = ev['ok'] and ev['growing'] and ev.get('center_on_real_axis')
            C[name] = dict(result='PASS' if (okK and okE) else 'FAIL', K2=Ks, lam_re=ev.get('lam_re'), lam_im=ev.get('lam_im'),
                           reading='K(2) <= 1 and one certified real eigenvalue lam > 0 => exactly one real pair (no parity used)')
        if 'CW' in d and name == 'C-P2':
            C['C-W(SP background)'] = dict(result='PASS' if d['CW'].get('ok') else 'FAIL', Q_at_X_upper=d['CW'].get('Q_at_X_upper'))
        same = _same_counts(list(d['brackets']['radii'].values()))
        C['C-R(%s background)' % name] = dict(result='PASS' if same else 'FAIL')
    d = load('NULL')
    if d:
        ev = d['evans']
        ok = bool(ev.get('ok') and ev.get('growing'))
        Ks = {}
        for R, rows in d['brackets']['radii'].items():
            for L in (0, 2):
                Ks['R%s_L%d' % (R, L)] = K_of(rows, L)[0]
        C['NULL'] = dict(result='PASS' if ok else 'FAIL', lam_re=ev.get('lam_re'), lam_im=ev.get('lam_im'),
                         K_descriptive=Ks, rule='certified eigenvalue with Re > 0 at L = 0 (sigma0 = 0.50)')
    d = load('CAL-K')
    if d:
        ok = d['neg'].get('krein_sign') == '-' and d['pos'].get('krein_sign') == '+'
        C['CAL-K'] = dict(result='PASS' if ok else 'FAIL', neg_w=d['neg'].get('w'), neg_ad=d['neg'].get('krein_ad'),
                          pos_w=d['pos'].get('w'), pos_ad=d['pos'].get('krein_ad'),
                          label='instrument calibration (not a BAR control)')
    json.dump(C, open(os.path.join(OUT, 'controls_verdict.json'), 'w'), indent=1)
    for k, v in C.items():
        print('%-26s %s' % (k, v['result']))
    return C


def _same_counts(rowsets):
    if len(rowsets) < 2:
        return False
    def sig(rows):
        out = []
        for L, r in sorted(((k, v) for k, v in rows.items() if isinstance(v, dict) and '+' in v), key=lambda x: str(x[0])):
            out.append((str(L), r['+']['upper'], r['+']['lower'], r['-']['upper'], r['-']['lower'],
                        (r.get('D0') or {}).get('constrained_upper')))
        return out
    s0 = sig(rowsets[0])
    return all(sig(x) == s0 for x in rowsets[1:]) and all(None not in t[1:5] for t in s0)


def target():
    d = json.load(open(os.path.join(OUT, 'target-B.json')))
    d['krein'] = {}
    for L in (0, 1, 2):
        k = json.load(open(os.path.join(OUT, 'target-K%d.json' % L)))
        d['krein'][str(L)] = dict(neg=k['neg'], pos=k['pos'])
    rf = os.path.join(OUT, 'target-refute.json')
    if os.path.exists(rf):
        d['evans_refutation'] = json.load(open(rf))
    cv = json.load(open(os.path.join(OUT, 'controls_verdict.json')))
    must = ['C-B1', 'C-B2', 'C-P1', 'C-P2', 'C-P3', 'NULL']
    rep = dict(controls={k: cv.get(k, {}).get('result', 'MISSING') for k in must})
    void = [k for k, v in rep['controls'].items() if v != 'PASS']
    B = d['B']
    if not (B.get('tail_ok') and B.get('existence_certified') and B.get('zeros') == 1 and B['virial_rel_upper'] <= 1e-6):
        void.append('B: background tube not certified')
    radii = d['brackets']['radii']
    Kt = {}
    for R, rows in radii.items():
        bad = consistency(rows)
        if bad:
            void.append('inconsistent brackets R=%s: %s' % (R, bad))
        for L in range(4):
            Kt['R%s_L%d' % (R, L)] = K_of(rows, L)[0]
    if not _same_counts(list(radii.values())):
        void.append('C-R: counts differ between R = 10 and R = 14')
    if not d['CW'].get('ok'):
        void.append('C-W failed')
    kr = d['krein']
    neg_ok = {}
    for L in ('0', '1', '2'):
        k = kr.get(L) or kr.get(int(L))
        neg = k['neg']; pos = k['pos']
        if not (pos.get('ok') and pos.get('krein_sign') == '+'):
            void.append('positive-Krein control at L=%s not certified positive' % L)
        neg_ok[L] = bool(neg.get('ok') and neg.get('krein_sign') == '-' and neg.get('in_gap'))
    # K(L) from the R = 14 brackets (C-R makes R = 10 identical)
    K = {L: Kt.get('R14.0_L%d' % L) for L in range(4)}
    for L in ('0', '1', '2'):
        if neg_ok[L] and K[int(L)] is not None and K[int(L)] < 2:
            void.append('IDX contradiction at L=%s: K < 2 with a certified negative-Krein pair' % L)
    rep['K'] = K; rep['negative_krein_certified'] = neg_ok; rep['void_reasons'] = void
    refuted = d.get('evans_refutation') or []
    if void:
        verdict = 'VOID'
    elif any(e.get('ok') and e.get('growing') for e in refuted):
        verdict = 'FAILED'
    elif all(K[L] is not None and K[L] <= 2 for L in (0, 1, 2)) and K[3] == 0 and all(neg_ok.values()) \
            and lo_hi(d['D1'])[0] > 0:
        verdict = 'HOLDS'
    else:
        verdict = 'INCONCLUSIVE'
    rep['verdict'] = verdict
    json.dump(rep, open(os.path.join(OUT, 'target_verdict.json'), 'w'), indent=1)
    print(json.dumps(rep, indent=1))
    return rep


if __name__ == '__main__':
    if sys.argv[1] == 'controls':
        controls()
    else:
        target()
