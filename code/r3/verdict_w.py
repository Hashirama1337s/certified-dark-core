"""verdict_w.py - per-cell and whole-window verdict (R3-WINDOW, BAR-W1 outcome rules). Reads JSON only.

  controls             -> out/controls_verdict.json : XK (9 nodes), XU (2), LOO (2 cells), XI, XC (5), R1REG; all must PASS
  window               -> out/window_verdict.json   : per cell HOLDS / FAILED / INCONCLUSIVE / VOID; the window verdict;
                          if not every cell HOLDS, the largest closed union of consecutive HOLDS cells (all components
                          listed, the longest reported).
Rules (BAR-W1):
  VOID          a must-pass control is missing or failed; or a cell's tube sha differs from its node record; or a
                cell job was REJECTED (bad node data).
  FAILED        an end node is not certified (existence, one node, tail) or its brackets contradict R1 (K != (2,2,2,0)),
                i.e. the certified inputs contradict the design.
  INCONCLUSIVE  the cell record's outcome is INCONCLUSIVE (the failing step is copied).
  HOLDS         the cell record's outcome is HOLDS.
"""
import sys, os, json
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import assemble_w as aw

OUT = os.path.join(HERE, 'out')
G9TAGS = ['lo-s', 'g165', 'g170', 'g175', 'r1', 'g185', 'g190', 'g195', 'hi-s']


def load(p):
    try:
        return json.load(open(p))
    except Exception:
        return None


# XU rule (lead decision 2026-11-19, SET AFTER SEEING XU-1985 DATA, pre-seal; BAR-W1 control 2):
#  - the scan stops at w < w_max - XU_TOP_MARGIN; the cells never count above w2 <= max w+ = 1.4641 (G9) while
#    |E| >= 1.9 (certified BR bound), so the smallest gap the cells rely on is far above 1e-3; delta = 1e-3.
#  - an undecided scan point is replaced by a single-point re-count at the SAME w (recount.py, finer level, same
#    tube sha) only if BOTH re-counted counts are decided; no neighbour-based exclusion.
XU_TOP_MARGIN = 1e-3


def _jtop(wmax, step):
    """number of grid points w_j = step j with w_j < w_max - XU_TOP_MARGIN (exact rational step)."""
    from fractions import Fraction as F
    st = F(step); j = 0
    while float(st * (j + 1)) < wmax - XU_TOP_MARGIN:
        j += 1
    return j


def _pairs(scan):
    return sum(1 for i, (w1, u1, l1) in enumerate(scan) for (w2, u2, l2) in scan[i + 1:]
               if l1 is not None and u2 is not None and l1 - u2 >= 1)


def xu_merge(c, t):
    """XU result for tag t: the single-job file, or the merge of part files that tile j = 1 .. jtop exactly (same tube
    sha, same grid). jtop excludes grid points within XU_TOP_MARGIN of w_max. The pair rule (no w1 < w2 with
    lower(w1) - upper(w2) >= 1, no undecided count) is applied to the scan j = 1 .. jtop; the other sectors come from
    the part with jlo = 1."""
    import glob
    d = load(os.path.join(c, 'XU_%s.json' % t))
    if d is not None:
        jt = _jtop(d['wmax'], d['grid_step'])
        scan = d['scan'][:jt]
        und = [s_ for s_ in scan if s_[1] is None or s_[2] is None]
        oth = d.get('other_sectors') or {}
        ok = bool(len(scan) == jt and not und and _pairs(scan) == 0 and oth and all(o.get('drop') for o in oth.values()))
        return dict(PASS=ok, source='single job', n=len(scan), jmax=d['jmax'], jtop=jt, undecided=len(und),
                    drop_pairs=_pairs(scan), excluded=d['jmax'] - jt)
    parts = [load(p) for p in sorted(glob.glob(os.path.join(c, 'XU_%s_part*.json' % t)))]
    parts = [p for p in parts if p]
    if not parts:
        return dict(PASS=False, source='missing')
    parts.sort(key=lambda p: p['jlo'])
    jmax = parts[0]['jmax']
    jt = _jtop(parts[0]['wmax'], parts[0]['grid_step'])
    ok = all(p['jmax'] == jmax and p['tube_sha256'] == parts[0]['tube_sha256'] and p['grid_step'] == parts[0]['grid_step']
             for p in parts)
    nxt = 1
    for p in parts:
        ok = ok and p['jlo'] == nxt
        nxt = p['jhi'] + 1
    ok = ok and nxt == jt + 1
    scan = [s_ for p in parts for s_ in p['scan']]
    ok = ok and len(scan) == jt
    rc = load(os.path.join(c, 'XU_%s_recount.json' % t)) or []
    used = []
    for k_, s_ in enumerate(scan):
        if s_[1] is None or s_[2] is None:
            for rr in rc:
                d_ = rr.get('decided')
                if (d_ and rr['tube_sha256'] == parts[0]['tube_sha256'] and abs(d_['w'] - s_[0]) < 1e-12
                        and d_['upper'] is not None and d_['lower'] is not None):
                    scan[k_] = [s_[0], d_['upper'], d_['lower']]; used.append(dict(w=s_[0], lev=d_['lev'], upper=d_['upper'], lower=d_['lower']))
                    break
    und = [s_ for s_ in scan if s_[1] is None or s_[2] is None]
    pairs = _pairs(scan)
    oth = parts[0].get('other_sectors') or {}
    oth_ok = bool(oth) and all(o.get('drop') for o in oth.values())
    return dict(PASS=bool(ok and not und and pairs == 0 and oth_ok), source='%d parts' % len(parts), n=len(scan),
                jmax=jmax, jtop=jt, excluded=jmax - jt, undecided=len(und), drop_pairs=pairs, other_sectors=oth,
                tiling_ok=bool(ok), recounts_used=used)


def controls():
    c = os.path.join(OUT, 'controls')
    res = {}; xud = {}
    for t in G9TAGS:
        d = load(os.path.join(c, 'XK_%s.json' % t)); res['XK:' + t] = bool(d and d.get('PASS'))
    for t in ('lo-u', 'hi-u'):
        m = xu_merge(c, t); res['XU:' + t] = m['PASS']; xud[t] = {k: v for k, v in m.items() if k != 'other_sectors'}
    for n in aw.LOO_GATES:
        d = load(os.path.join(c, 'LOO_%s.json' % n))
        res['LOO:' + n] = bool(d and d.get('LOO', {}).get('inside') and d.get('tube_below_r_u') and
                               all(b.get('ok') for b in d.get('BR', [])))
    d = load(os.path.join(c, 'XI.json')); res['XI'] = bool(d and d.get('outcome') == 'REJECTED')
    xc = []
    try:
        xc = [json.loads(l) for l in open(os.path.join(c, 'XC.jsonl')) if l.strip()]
    except Exception:
        pass
    # audit-W: exactly the 5 sealed XC points, each once (no stale appended lines)
    sealed_xc = [((1.597, 1.6), 1.5985, 0), ((1.75, 1.8), 1.775, 0), ((1.75, 1.8), 1.775, 1), ((1.75, 1.8), 1.775, 2),
                 ((1.95, 1.983), 1.98, 2)]
    got = [((x['cell'][0], x['cell'][1]), x['point'], x['L']) for x in xc]
    res['XC'] = bool(sorted(got) == sorted(sealed_xc) and all(x.get('PASS') for x in xc))
    d = load(os.path.join(c, 'R1REG.json')); res['R1REG'] = bool(d and d.get('PASS'))
    out = dict(controls=res, all_pass=all(res.values()), xu_detail=xud)
    json.dump(out, open(os.path.join(OUT, 'controls_verdict.json'), 'w'), indent=1)
    return out


def cell_verdict(i, cv):
    a, b = aw.CELLS[i]
    tag = aw.ctag(i)
    if not cv['all_pass']:
        return dict(cell=tag, interval=[a, b], verdict='VOID', why='controls not all PASS')
    Na = load(os.path.join(OUT, aw.ntag(a), 'N.json')); Nb = load(os.path.join(OUT, aw.ntag(b), 'N.json'))
    C = load(os.path.join(OUT, 'cells', tag + '.json'))
    if Na is None or Nb is None or C is None:
        return dict(cell=tag, interval=[a, b], verdict='INCONCLUSIVE', why='missing output')
    for N in (Na, Nb):
        if N.get('brackets_ok') is not True:                     # audit-W: FAILED-by-brackets (K != (2,2,2,0))
            return dict(cell=tag, interval=[a, b], verdict='FAILED',
                        why='end node %s: brackets contradict R1 (K14 = %s)' % (N['sig0'], N.get('K14')))
        if not N.get('ok'):
            return dict(cell=tag, interval=[a, b], verdict='FAILED', why='end node %s not certified' % N['sig0'])
    if C.get('tube_sha') != [Na['tube_sha256'], Nb['tube_sha256']]:
        return dict(cell=tag, interval=[a, b], verdict='VOID', why='tube sha mismatch')
    if C.get('outcome') == 'REJECTED':
        return dict(cell=tag, interval=[a, b], verdict='VOID', why=C.get('why'))
    if C.get('outcome') == 'HOLDS':
        return dict(cell=tag, interval=[a, b], verdict='HOLDS', seconds=C.get('seconds'))
    return dict(cell=tag, interval=[a, b], verdict='INCONCLUSIVE', failing_steps=C.get('failing_steps') or C.get('failing_step'),
                fails=C.get('fails'))


def window():
    cv = controls()
    rows = [cell_verdict(i, cv) for i in range(len(aw.CELLS))]
    comps = []; cur = None
    for i, r in enumerate(rows):
        if r['verdict'] == 'HOLDS':
            cur = [aw.CELLS[i][0], aw.CELLS[i][1]] if cur is None else [cur[0], aw.CELLS[i][1]]
        else:
            if cur:
                comps.append(cur)
            cur = None
    if cur:
        comps.append(cur)
    allh = all(r['verdict'] == 'HOLDS' for r in rows)
    longest = max(comps, key=lambda c: Fraction(c[1]) - Fraction(c[0])) if comps else None
    out = dict(controls=cv, cells=rows, window='HOLDS on [1597/1000, 1983/1000]' if allh else
               ('VOID' if any(r['verdict'] == 'VOID' for r in rows) else 'NOT ALL CELLS HOLD'),
               closed_components=comps, largest_closed_union=longest)
    json.dump(out, open(os.path.join(OUT, 'window_verdict.json'), 'w'), indent=1, default=str)
    return out


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'controls'
    r = controls() if what == 'controls' else window()
    print(json.dumps(r if what == 'controls' else {k: v for k, v in r.items() if k != 'cells'}, indent=1, default=str))
