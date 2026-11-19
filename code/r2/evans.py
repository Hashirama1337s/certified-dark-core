"""evans.py - certified enclosure of an off-axis eigenvalue lam of J L in sector L (controls C-P2, C-P3, null N1; the
refutation route of the target), by complex Krawczyk on (lam, v) for M(lam) v = 0 (match.py, EVANS channels).

  K(X) in int(X) for an acb box X  =>  exactly one zero (lam*, v*) of M(lam) v = 0, v_k0 = 1, in X (no
  algebraic-simplicity claim is made; REFEREE-R1-FINAL item 6 wording, applied here too).
  'growing' is certified when Re(lam-disc) > 0.  For a disc centred on the real axis, uniqueness plus the conjugate
  symmetry of the real operator J L (lam eigenvalue => conj(lam) eigenvalue) gives lam* real.
"""
import sys, json, time
import numpy as np
from flint import arb, acb
import itaylor as it
import lincore as lc
import bg_tube as bt
import match as mt
import kraw as kw


def build(s, n, sig0, R1, K=24, prec=200, log=print):
    steps, info, Yend = bt.get_tube(s, n, sig0, R1, log=log)
    it.set_prec(prec)
    bj = lc.BgJets(s, steps, Yend, K)
    return bj, info


def certify(bj, info, L, s, sig0, lam0, r_m, K=24, disc_r=0.002, log=print):
    t0 = time.time()
    def evalpt(lam, deriv):
        disc = acb(lam) + acb(arb(0, disc_r), arb(0, disc_r)) if deriv else None
        return mt.matrix(bj, info, 'evans', L, s, sig0, acb(lam), r_m, deriv=deriv, par_disc=disc, disc_r=disc_r,
                         box_r=0.0, K=K)
    def evalbox(Lb, rho):
        c = acb(Lb.real.mid(), Lb.imag.mid())
        disc = c + acb(arb(0, disc_r), arb(0, disc_r))
        return mt.matrix(bj, info, 'evans', L, s, sig0, Lb, r_m, deriv=True, par_disc=disc, disc_r=disc_r,
                         box_r=rho * 1.5, K=K)
    C = kw.certify(evalpt, evalbox, complex(lam0), 'complex', log=log)
    if not C['ok']:
        return dict(ok=False, L=L, guess=str(C.get('par_guess')), why='Krawczyk did not contract', seconds=time.time() - t0)
    lam = C['par']
    re = lam.real; im = lam.imag
    S = lambda x: '%s +/- %.2e' % (x.mid().str(10, radius=False), float(x.rad()))
    Eabs = -info['E']
    out = dict(ok=True, L=L, lam_re=S(re), lam_im=S(im), growing=bool(re > 0), re_lower=it.flo(re),
               lam_over_2absE_re=S(re / (2 * Eabs)), lam_over_2absE_im=S(abs(im) / (2 * Eabs)),
               lam_over_absE_re=S(re / Eabs), seconds=time.time() - t0, rel=C['rel'], r_m=r_m,
               re_upper=it.fup(re), im_lower=it.flo(im), im_upper=it.fup(im), disc_r=disc_r)   # build-3: outward ends
    # real-axis case: the box is a disc centred on the real axis
    out['center_on_real_axis'] = bool(abs(float(lam.imag.mid())) < float(lam.imag.rad()))
    return out


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('s', type=int); ap.add_argument('n', type=int); ap.add_argument('sig0', type=float)
    ap.add_argument('R1', type=float); ap.add_argument('out')
    ap.add_argument('--L', type=int, required=True); ap.add_argument('--lam', required=True, help='complex guess, e.g. 0.088+0.58j')
    ap.add_argument('--rm', type=float, default=10.0); ap.add_argument('--K', type=int, default=24)
    a = ap.parse_args()
    bj, info = build(a.s, a.n, a.sig0, a.R1, K=a.K)
    res = certify(bj, info, a.L, a.s, a.sig0, complex(a.lam), a.rm, K=a.K)
    res['E'] = info['E'].str(12, radius=True)
    print(res)
    json.dump(res, open(a.out, 'w'), indent=1, default=str)
