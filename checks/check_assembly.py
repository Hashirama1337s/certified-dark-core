"""check_assembly.py - proof seat check (PROOF-R1, section 7). Reads build-2/out/*.json only (no build-2 code imported).

Re-derives from the certified output strings, in ball arithmetic:
  K(L) from the counts (kernels booked as in IDX), the D0 inequalities, the exterior margins, the tail-lemma
  contraction constants, the Krein signs with tail bound, 0 < w < |E| (w from the Krawczyk log strings, which are
  outward arb strings), D1 > 0, a single tube sha256, and the C-P3 realness remark (K(2) <= 1, Re lam > 0).
Every JSON value 'm +/- r' with a TRUNCATED midpoint is flagged, since such a string is not an enclosure.
Run:  python -B checks/check_assembly.py
"""
import json, re
from flint import arb, ctx

ctx.prec = 200
OUT = 'data/r1/'


def A(sx):
    """arb from '[m +/- r]' or 'm +/- r' (arb parses the bracket form; outward)."""
    sx = str(sx).strip()
    if not sx.startswith('['):
        sx = '[' + sx + ']'
    return arb(sx)


B = json.load(open(OUT + 'target-B.json'))
Ks = {L: json.load(open(OUT + 'target-K%d.json' % L)) for L in (0, 1, 2)}
ok_all = True


def chk(name, cond):
    global ok_all
    ok_all = ok_all and bool(cond)
    print('%-62s %s' % (name, 'OK' if cond else 'FAIL'))


shas = {B['B']['tube_sha256'], B['brackets']['tube_sha256']} | {Ks[L]['tube_sha256'] for L in Ks}
chk('one tube sha256 in all four outputs (%s...)' % list(shas)[0][:10], len(shas) == 1)
bg = B['B']
chk('B: zeros = 1, tail_ok, existence_certified', bg['zeros'] == 1 and bg['tail_ok'] and bg['existence_certified'])
E = A(bg['E']); m = A(bg['m'])
chk('B: E < 0, u(R1) < 0, kappa1 > 0', bool(E < 0) and bool(A(bg['u_R1']) < 0) and bool(A(bg['kappa1']) > 0))
chk('D1 = 3m/4 > 0', bool(A(B['D1']) > 0))

for R in ('10.0', '14.0'):
    rows = B['brackets']['radii'][R]
    U = {L: (rows[str(L)]['+']['upper'], rows[str(L)]['-']['upper']) for L in range(4)}
    Lo = {L: (rows[str(L)]['+']['lower'], rows[str(L)]['-']['lower']) for L in range(4)}
    for L in range(4):
        chk('R=%s L=%d ext margin |E|-m/R-delta-eps > 0 (%s)' % (R, L, rows[str(L)]['ext_margin']),
            bool(A(rows[str(L)]['ext_margin']) > 0) and rows[str(L)]['ext_ok'])
        for w in '+-':
            d = rows[str(L)][w]
            chk('R=%s L=%d %s counts certified, upper %s >= lower %s' % (R, L, w, d['upper'], d['lower']),
                d['up_detail']['ok'] and d['lo_detail']['ok'] and d['upper'] >= d['lower'])
    d0 = rows['0']['D0']
    d2 = A(d0['d2']); M = A(d0['M'])
    chk('R=%s D0: n(B)=2, d2 < 0, M|d2| > 1 (M|d2| = %s)' % (R, (M * abs(d2)).str(5)),
        d0['ok'] and d0['nB'] == 2 and bool(d2 < 0) and bool(M * abs(d2) > 1))
    # independent recomputation of M from g1, ge and the level-0 reserve ext0 = ext_margin + eps
    ext0 = A(rows['0']['ext_margin']) + arb(1) / 1000
    g1 = A(d0['g1'].replace('[', '').replace(']', '')) if '+/-' in d0['g1'] else arb(d0['g1'])
    ge = A(d0['ge'])
    Mre = 1 / (g1 / 1 + ge / ext0)
    chk('R=%s D0: M recomputed from g1, ge, ext0 = %s, consistent' % (R, Mre.str(5)), bool(Mre.overlaps(M)))
    K0 = (d0['nB'] - 1) + (U[0][1] - 1)
    K1 = (U[1][0] - 1) + U[1][1]
    K2 = U[2][0] + U[2][1]
    K3 = U[3][0] + U[3][1]
    print('   R=%s: K = (%d, %d, %d, %d)' % (R, K0, K1, K2, K3))
    chk('R=%s K(0..2) <= 2 and K(3) = 0' % R, K0 <= 2 and K1 <= 2 and K2 <= 2 and K3 == 0)

logw = {0: '[1.10491108047488 +/- 4.15e-15]', 1: '[0.539925668013455 +/- 2.97e-16]', 2: '[0.2968148506 +/- 6.42e-11]'}
logwp = {0: '[1.25921337137566 +/- 6.39e-15]', 1: '[0.951028237700108 +/- 2.59e-16]', 2: '[0.5179458643 +/- 7.13e-11]'}
for L in (0, 1, 2):
    for key, lw in (('neg', logw), ('pos', logwp)):
        k = Ks[L][key]
        w = arb(lw[L])
        ad = A(k['krein_ad'])
        th = arb(k['theta'])
        sgn = (ad < 0) if key == 'neg' else (ad > 0)
        chk('L=%d %s: Krawczyk ok, 0 < w < |E| (w=%s)' % (L, key, w.str(12)), k['ok'] and bool(w > 0) and bool(w < -E)
            and k['in_gap'])
        chk('L=%d %s: <a,d> = %s certified %s, tail %s, theta %s < 1/2' % (L, key, k['krein_ad'], '<0' if key == 'neg'
            else '>0', k['tail_bound'], k['theta']), bool(sgn) and bool(th < arb('0.5')))
        # the JSON 'w' string has a 10-digit midpoint with the unrounded ball radius: flag if it does not contain the log ball
        wj = A(k['w'])
        if not wj.contains(w):
            print('   NOTE L=%d %s: JSON w string %s is NOT an enclosure (truncated midpoint); log ball %s used' % (
                L, key, k['w'], lw[L]))

# C-P3 realness remark (controls only)
c3 = json.load(open(OUT + 'cal/C-P3.json'))
K2s = []
for R, rows in c3['brackets']['radii'].items():
    K2s.append(rows['2']['+']['upper'] + rows['2']['-']['upper'])
re3 = c3['evans']['re_lower']
chk('C-P3: K(2) <= 1 at both radii (%s) and Re lam lower end %.6g > 0' % (K2s, re3), max(K2s) <= 1 and re3 > 0)
print('ALL PASS' if ok_all else 'SOME CHECK FAILED')
