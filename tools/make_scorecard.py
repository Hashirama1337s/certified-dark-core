#!/usr/bin/env python
"""make_scorecard.py -- build scorecard.svg and SCORECARD.md: every sealed test of this work, failures and voids
included, with the R2 points shown as PENDING until their certified verdicts are in data/r2/, and the R3 window test
(version 2.0).

Every R1 outcome is checked against the shipped verdict files before anything is written:
  data/r1/target_verdict.json      verdict of the amended target run (AMENDMENT-R1-1, seal 6ad54f5713)
  data/blind/verdict_blind.out     scores of the blind replication (BAR-R1-BLIND, seal f47da860b7)
For R2 (BAR-R2-EDGES, seal 3ad051728e) the script reads data/r2/<tag>/verdict.json when it exists and shows
PENDING otherwise. For R3 (BAR-W1, seal 5e6d7bfed0) it reads data/r3/window_verdict.json and
data/r3/controls_verdict.json. The script stops if a shipped verdict disagrees with the table below.
Run from anywhere:  python tools/make_scorecard.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H, F, V, P = 'HOLD', 'FAILED', 'VOID', 'PENDING'

# (test, seal, what, outcome, source, [(item, outcome, what as scored)])
BARS = [
    ('R1', '07faff6621', 'Spectral stability at sigma0 = 1.80 (first run, sigma0 entered as the double nearest 1.8)', H,
     'seals/BAR-R1-FINAL.md', [
         ('P1', H, 'counts: upper (2,2,1,0)/(2,1,1,0), lower (2,1,1,0)/(1,1,1,0) at R = 10, 14'),
         ('P2', H, 'D0: n(B) = 2, d2 < 0, M|d2| > 1; D1 = 3m/4 > 0'),
         ('P3', H, 'K = (2, 2, 2, 0)'),
         ('P4', H, 'three negative-Krein eigenvalues certified, <a,d> < 0'),
         ('T', H, 'HOLDS; superseded by the amended run at exactly 9/5 (referee-3 fixes)')]),
    ('R1-dup', 'dbcc9f9278', 'Duplicate seal of the identical BAR-R1-FINAL file', V, 'seals/BAR-R1-FINAL.md', []),
    ('R1-amend', '6ad54f5713', 'Amended instruments, re-run at sigma0 = 9/5 exactly (the result of this work)', H,
     'seals/AMENDMENT-R1-1.md', [
         ('controls', H, 'C-B1, C-B2, C-P1, C-P2, C-P3, NULL all PASS'),
         ('K', H, 'K = (2, 2, 2, 0)'),
         ('Krein', H, 'negative-Krein certified at L = 0, 1, 2'),
         ('T', H, 'HOLDS: no eigenvalue with Re lambda > 0 in any sector')]),
    ('R1-blind', 'f47da860b7', 'Blind float replication from the paper alone', H, 'seals/BAR-R1-BLIND.md', [
        ('PB1', H, 'background E and m'), ('PB2', H, 'counts n(L+), n(L-)'),
        ('PB3', H, 'negative-Krein w to 1e-4 (agree to all 10 printed digits)'), ('PB4', H, 'positive-Krein w'),
        ('PB5', H, 'max Re lambda <= 1.6e-11'), ('PC', H, 'growing quartet at sigma0 = 1/2')]),
]
R2_SEAL = '3ad051728e'
R2_POINTS = [('lo-u', '1595/1000', 'unstable L = 0'), ('lo-s', '1597/1000', 'stable'),
             ('hi-s', '1983/1000', 'stable'), ('hi-u', '1985/1000', 'unstable L = 2'),
             ('in-155', '31/20', 'unstable L = 0 (paper band)'), ('in-200', '2', 'unstable L = 2 (paper band)'),
             ('g165', '33/20', 'stable'), ('g170', '17/10', 'stable'), ('g175', '7/4', 'stable'),
             ('g185', '37/20', 'stable'), ('g190', '19/10', 'stable'), ('g195', '39/20', 'stable')]

FONT = 'Segoe UI, Helvetica, Arial, sans-serif'
INK, MUTED, ACCENT, BAND, LINE, BORDER = '#e8edf2', '#9aa4ae', '#39ff14', '#262b31', '#22272e', '#2f353d'
CHIP = {'HOLD': ('#12301c', '#39ff14'), 'FAILED': ('#3a1a1a', '#ff6b6b'), 'VOID': ('#33290f', '#ffc94d'),
        'PENDING': ('#1f2a3a', '#7fb2ff'), 'INCONCLUSIVE': ('#2a2a2a', '#c8ccd0')}


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def check():
    tv = json.load(open(os.path.join(ROOT, 'data', 'r1', 'target_verdict.json'), encoding='utf-8'))
    if tv.get('verdict') != 'HOLDS' or any(v != 'PASS' for v in tv['controls'].values()):
        sys.exit('data/r1/target_verdict.json disagrees with the R1-amend row')
    if tv['K'] != {'0': 2, '1': 2, '2': 2, '3': 0} or not all(tv['negative_krein_certified'].values()):
        sys.exit('data/r1/target_verdict.json K or Krein disagrees')
    txt = open(os.path.join(ROOT, 'data', 'blind', 'verdict_blind.out'), encoding='utf-8').read()
    sc = json.loads(txt[:txt.index('\nPC raw:')])['scores']
    for k in ('PB1', 'PB2', 'PB3', 'PB4', 'PB5'):
        if sc[k] != 'HOLD':
            sys.exit('data/blind/verdict_blind.out disagrees for %s' % k)


def r2_outcomes():
    out = []
    for tag, s0, what in R2_POINTS:
        fn = os.path.join(ROOT, 'data', 'r2', tag, 'verdict.json')
        o = P
        if os.path.exists(fn):
            v = json.load(open(fn, encoding='utf-8'))
            t = str(v.get('verdict', v.get('T', ''))).upper()
            o = {'HOLDS': H, 'HOLD': H, 'FAILED': F, 'VOID': V, 'INCONCLUSIVE': 'INCONCLUSIVE'}.get(t, P)
        out.append((tag, o, 'sigma0 = %s, %s' % (s0, what)))
    return out


R3_SEAL = '5e6d7bfed0'
R3_NODES = 23


def r3_items():
    wv = json.load(open(os.path.join(ROOT, 'data', 'r3', 'window_verdict.json'), encoding='utf-8'))
    cv = json.load(open(os.path.join(ROOT, 'data', 'r3', 'controls_verdict.json'), encoding='utf-8'))
    cells = wv['cells']
    n_hold = sum(1 for c in cells if c['verdict'] == 'HOLDS')
    ctrl = cv['controls']
    n_nodes = sum(1 for d in os.listdir(os.path.join(ROOT, 'data', 'r3')) if d.startswith('n')
                  and json.load(open(os.path.join(ROOT, 'data', 'r3', d, 'N.json'), encoding='utf-8')).get('ok') is True)
    if wv['window'] != 'HOLDS on [1597/1000, 1983/1000]' or n_hold != 22 or len(cells) != 22:
        sys.exit('data/r3/window_verdict.json disagrees with the R3 row')
    if not cv['all_pass'] or not all(ctrl.values()) or len(ctrl) != 16 or n_nodes != R3_NODES:
        sys.exit('data/r3 controls or nodes disagree with the R3 row')
    return H, [('cells', H, '%d of %d cells HOLD (c01 ... c22)' % (n_hold, len(cells))),
               ('nodes', H, '%d of %d nodes certified, K = (2, 2, 2, 0)' % (n_nodes, R3_NODES)),
               ('controls', H, '%d of %d controls PASS (XK x9, XU x2, LOO x2, XI, XC, R1REG); XU-1985 rule set after '
                               'seeing its data, disclosed' % (sum(ctrl.values()), len(ctrl))),
               ('T', H, 'HOLDS on [1597/1000, 1983/1000]: spectral stability for every sigma0 in the interval, along the certified branch')]


def chip(x, y, outcome, small=False):
    fill, fg = CHIP[outcome]
    w = (len(outcome) * (6.6 if small else 7.4)) + (14 if small else 20)
    h = 16 if small else 20
    fs = 10 if small else 11.5
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2:.0f}" fill="{fill}"/>'
            f'<text x="{x + (7 if small else 10)}" y="{y + h - (4 if small else 6)}" font-size="{fs}" font-weight="600" '
            f'fill="{fg}">{outcome}</text>'), w


def build():
    check()
    r2 = r2_outcomes()
    r2_bar = P if any(o == P for _, o, _ in r2) else (H if all(o == H for _, o, _ in r2) else F)
    bars = BARS + [('R2', R2_SEAL, 'Certified edges and interior grid of the stability band (12 points)', r2_bar,
                    'seals/BAR-R2-EDGES.md', r2)]
    r3_out, r3 = r3_items()
    bars.append(('R3', R3_SEAL, 'Stability for every sigma0 in [1597/1000, 1983/1000] (version 2.0)', r3_out,
                 'seals/BAR-W1.md', r3))
    n_p = sum(1 for _, o, _ in r2 if o == P)
    title = 'Scorecard: %d sealed bars (R1: HOLD; blind: HOLD; one duplicate VOID; R2: %s; R3: %s)' % (
        len(bars), 'PENDING, %d of 12 points open' % n_p if n_p else r2_bar, r3_out)
    sub = 'Sealed = predictions and pass bars hashed before the run. Failures and voids are shown. Details: SCORECARD.md.'
    W, y, body = 1000, 66, []
    body.append(f'<rect x="10" y="{y}" width="{W - 20}" height="22" fill="{BAND}"/>')
    body.append(f'<text x="20" y="{y + 16}" font-size="11.5" font-weight="600" fill="{ACCENT}" letter-spacing="0.5">'
                f'THIS WORK: ONE POINT PROVED (R1), THE BAND EDGES (R2) AND THE WHOLE WINDOW (R3)</text>')
    y += 22
    for tid, seal, what, out, _, its in bars:
        body.append(f'<text x="20" y="{y + 22}" font-size="12.5" font-family="Consolas, Menlo, monospace" fill="{INK}">'
                    f'{esc(tid + " " + seal)}</text>')
        body.append(f'<text x="210" y="{y + 22}" font-size="12.5" fill="{INK}">{esc(what)}</text>')
        c, _ = chip(W - 120, y + 8, out)
        body.append(c)
        y += 30
        x = 210
        for it, o, _ in its:
            if x + len(it) * 6.6 + 100 > W - 20:
                x, y = 210, y + 22
            body.append(f'<text x="{x}" y="{y + 12}" font-size="10.5" font-family="Consolas, Menlo, monospace" '
                        f'fill="{MUTED}">{esc(it)}</text>')
            c, w = chip(x + len(it) * 6.6 + 6, y, o, small=True)
            body.append(c)
            x += len(it) * 6.6 + 6 + w + 14
        y += 24 if its else 0
        body.append(f'<line x1="10" y1="{y + 1}" x2="{W - 10}" y2="{y + 1}" stroke="{LINE}"/>')
    Ht = y + 14
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Ht}" viewBox="0 0 {W} {Ht}" font-family="{FONT}" '
           f'role="img" aria-label="{esc(title)}">\n<title>{esc(title)}</title>\n'
           f'<rect width="{W}" height="{Ht}" rx="10" fill="#1c2026" stroke="{BORDER}"/>\n'
           f'<text x="20" y="34" font-size="17" font-weight="600" fill="{INK}">{esc(title)}</text>\n'
           f'<text x="20" y="54" font-size="12" fill="{MUTED}">{esc(sub)}</text>\n' + '\n'.join(body) + '\n</svg>\n')
    with open(os.path.join(ROOT, 'scorecard.svg'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(svg)
    ch = {k: '![%s](brand/chips/%s.svg)' % (k, k.lower()) for k in CHIP}
    md = ['# Scorecard', '',
          '**In plain words.** Before each test ran, we wrote down what it had to show and hashed that text, so it could not',
          'be changed afterwards. Each test is scored exactly as written. This page lists every such test of this work and',
          'every item in it. A duplicate seal is listed as VOID. The R2 rows are read from `data/r2/<tag>/verdict.json`,',
          'the R3 rows from `data/r3/window_verdict.json`, `data/r3/controls_verdict.json` and the node files.',
          '',
          title + '.', '',
          'Generated by `tools/make_scorecard.py`, which first checks the R1 rows against `data/r1/target_verdict.json` and',
          '`data/blind/verdict_blind.out`.', '',
          '| Test | Seal | What was predicted | Verdict | Source |', '|---|---|---|---|---|']
    for tid, seal, what, out, src, _ in bars:
        md.append(f'| {tid} | `{seal}` | {what} | {ch[out]} | [{src}]({src}) |')
    md += ['', '## Every sealed item', '', '| Test | Item | Verdict | As scored |', '|---|---|---|---|']
    for tid, _, _, _, _, its in bars:
        for it, o, d in its:
            md.append(f'| {tid} | {it} | {ch[o]} | {d} |')
    md += ['', 'Notes:',
           '- R1 (07faff6621) was first run with sigma0 entered as the binary double nearest 1.8. The internal referee',
           '  (referee-3) asked for sigma0 = 9/5 exactly and four other code fixes; AMENDMENT-R1-1 (6ad54f5713) re-ran the',
           '  same bar with the fixed code. The amended run is the result of this work. It has the same certified',
           '  midpoints as the first run to every printed digit; radii differ in the last digits.',
           '- R1 items P1-P4 were sealed as MATCH/MISS predictions (BAR-R1-FINAL); they scored MATCH and are shown with',
           '  the HOLD chip.',
           '- dbcc9f9278 sealed the same file (identical sha256) a second time; it is VOID and scored under 07faff6621.',
           '- The blind replication is double precision with no enclosure: a replication, not a certificate.',
           '- R2 per point: HOLDS, FAILED (stable points only), INCONCLUSIVE or VOID, read from data/r2/<tag>/verdict.json.',
           '- R3 (BAR-W1): the XU control at 1985/1000 FAILED under the rule as first written and passed under a rule the',
           '  lab lead set after seeing its data, before the seal (disclosed in the bar; PAPER.md, Section 12.11). It',
           '  concerns frequencies near the upper limit of the counter (w ~ 2.59), far above those the proof uses.']
    with open(os.path.join(ROOT, 'SCORECARD.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(md) + '\n')
    print(title)


if __name__ == '__main__':
    build()
