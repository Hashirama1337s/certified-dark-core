"""krein.py - nodes I0-I2: certified isolated imaginary eigenvalue i w of J L in sector L with the Krein sign of its
eigenvector, by Krawczyk on (w, v) for the real matching problem M(w) v = 0 (v = (alpha, beta) in R^6, v_k0 = 1).

  Krawczyk: K(X) = x~ - C F(x~) + (I - C J(X))(X - x~),  J = [dM/dw v | M e_j (j != k0)].
  K(X) in int(X)  =>  exactly one zero (w*, v*) in X, with J(w*, v*) invertible. (No algebraic-simplicity claim is
  made or needed: REFEREE-R1-FINAL item 6. The Krein reading uses only the certified eigenvector.)
  Eigenvector: (a, d) = Reg alpha on [0, r_m],  = -Dec beta on [r_m, inf).
  Krein form: <L xi, xi> = 2 w <a, d>,  <a, d> = alpha^T Greg alpha + beta^T Gdec beta + tail,
  |tail| <= (Ainv sum|beta|)^2 / ((1-theta)^2 2 mu)   (tail.py weighted norm).
  The real system needs w real: the Krawczyk box for w is a real interval, so w* is real and 0 < w* < |E|.
Cauchy bounds for d/dw of the tail error parts use the lemma on a complex disc of radius disc_r around w~.
"""
import sys, os, json, time, math
import numpy as np
from flint import arb, acb, ctx
import itaylor as it
import lincore as lc
import bg_tube as bt
import match as mt
import tail as tl
import kraw as kw


def mid(x):
    return float(x.mid())


def fmat(M):
    return np.array([[mid(x) for x in row] for row in M])


def build(s, n, sig0, R1, K=24, prec=200, log=print):
    steps, info, Yend = bt.get_tube(s, n, sig0, R1, log=log)
    it.set_prec(prec)
    bj = lc.BgJets(s, steps, Yend, K)
    return bj, info


def evalM(bj, info, L, s, sig0, w, r_m, deriv, gram, disc_r, box_r, K):
    par = arb(w)
    disc = acb(arb(w.mid()) if isinstance(w, arb) else arb(w), 0) + acb(arb(0, disc_r), arb(0, disc_r)) if deriv else None
    return mt.matrix(bj, info, 'krein', L, s, sig0, par, r_m, deriv=deriv, gram=gram, par_disc=disc, disc_r=disc_r,
                     box_r=box_r, K=K)


def krawczyk(bj, info, L, s, sig0, w0, r_m, K=24, disc_r=0.002, log=print):
    t0 = time.time()
    evalpt = lambda w, deriv: evalM(bj, info, L, s, sig0, w, r_m, deriv, False, disc_r, 0.0, K)
    evalbox = lambda W, rho: evalM(bj, info, L, s, sig0, W, r_m, True, True, disc_r, rho, K)
    C = kw.certify(evalpt, evalbox, float(w0), 'real', log=log)
    if not C['ok']:
        return dict(ok=False, L=L, w_guess=C.get('par_guess'), why='Krawczyk did not contract', seconds=time.time() - t0)
    wv = C['par']; v = C['v']; Rb = C['Rb']
    al = v[:3]; be = v[3:]
    Gr = Rb['Greg']; Gd = Rb['Gdec']
    q1 = sum((al[i] * Gr[i][j] * al[j] for i in range(3) for j in range(3)), arb(0))
    q2 = sum((be[i] * Gd[i][j] * be[j] for i in range(3) for j in range(3)), arb(0))
    Tb = Rb['Td'] or Rb['T']
    sb = sum((abs(x) for x in be), arb(0))
    tailb = (Tb['Ainv'] * sb) ** 2 / ((1 - Tb['theta']) ** 2 * 2 * Tb['mu'])
    ad = q1 + q2 + tailb * arb(0, 1)
    nrm = abs(q1).upper() + abs(q2).upper()
    sign = '-' if ad < 0 else ('+' if ad > 0 else '?')
    Eabs = -info['E']
    inband = bool(wv > 0 and wv < Eabs)
    S = lambda x: '%s +/- %.2e' % (x.mid().str(10, radius=False), float(x.rad()))
    # build-3: outward float ends of the certified w (for the separation check of two close opposite-Krein modes)
    return dict(ok=True, L=L, w=S(wv), w_mid=mid(wv), w_rad=float(wv.rad()), w_lo=it.flo(wv), w_hi=it.fup(wv),
                disc_r=disc_r, krein_ad=S(ad), krein_sign=sign,
                ad_over_parts=S(ad / nrm), in_gap=inband, int_inner=S(q1), int_outer=S(q2), tail_bound='%.2e' % float(tailb.upper()),
                rel=C['rel'], r_m=r_m, k0=C['k0'], theta='%.2e' % float(Tb['theta'].upper()), mu='%.5f' % float(Tb['mu'].mid()),
                frob_e1='%.2e' % float(Rb['frob']['e1'].upper()), Tt='%.2e' % float(Rb['Tt'].upper()), seconds=time.time() - t0)


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('s', type=int); ap.add_argument('n', type=int); ap.add_argument('sig0', type=float)
    ap.add_argument('R1', type=float); ap.add_argument('out')
    ap.add_argument('--L', type=int, required=True); ap.add_argument('--w', required=True, help='comma list of float guesses')
    ap.add_argument('--rm', type=float, default=8.0); ap.add_argument('--K', type=int, default=24)
    a = ap.parse_args()
    bj, info = build(a.s, a.n, a.sig0, a.R1, K=a.K)
    out = []
    for w0 in [float(x) for x in a.w.split(',')]:
        print('L=%d guess w=%g' % (a.L, w0), flush=True)
        r = krawczyk(bj, info, a.L, a.s, a.sig0, w0, a.rm, K=a.K)
        print(' ->', {k: v for k, v in r.items() if k in ('ok', 'w', 'krein_sign', 'krein_ad', 'in_gap', 'tail_bound', 'seconds', 'why')}, flush=True)
        out.append(r)
    json.dump(out, open(a.out, 'w'), indent=1, default=str)
