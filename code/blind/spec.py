"""Linear spectrum of J L, L = diag(L+, L-), for one GPP stationary state, B-spline Galerkin."""
import sys, json, time
import numpy as np
import scipy.linalg as sla
sys.path.insert(0, 'code/blind')
from fem import Basis, RadialProblem


def analyse(bgobj, R, N, p, beta, Ls=(0, 1, 2, 3), s=+1, alpha=1.0, ktol=1e-6, verbose=True):
    E = bgobj.E
    basis = Basis(R, N, p, beta)
    pr = RadialProblem(bgobj.eval, basis, s=s, alpha=alpha)
    r = basis.rq
    sig = pr.sig
    # expected kernel vectors (reduced): L=0 L-: r sigma ; L=1 L+: r sigma'
    out = {}
    for L in Ls:
        Hp, Hm = pr.ops(L)
        Ap, Li = pr.sym(Hp)
        Am, _ = pr.sym(Hm)
        ep, vp = np.linalg.eigh(Ap)
        em, vm = np.linalg.eigh(Am)
        res = dict(L=L)
        # kernels: eigenvalues with |mu| < ktol
        res['Lplus_lowest'] = ep[:6].tolist()
        res['Lminus_lowest'] = em[:6].tolist()
        kp = np.where(np.abs(ep) < ktol)[0]
        km = np.where(np.abs(em) < ktol)[0]
        res['n_Lplus'] = int(np.sum(ep < -ktol))
        res['n_Lminus'] = int(np.sum(em < -ktol))
        res['kernel_Lplus'] = [float(ep[i]) for i in kp]
        res['kernel_Lminus'] = [float(em[i]) for i in km]
        # J L in symmetric coordinates: lambda a = Am d ; lambda d = -Ap a
        n = len(Ap)
        Z = np.zeros((n, n))
        JL = np.block([[Z, Am], [-Ap, Z]])
        lam, X = np.linalg.eig(JL)
        res['max_re_lambda'] = float(np.max(lam.real))
        big = np.abs(lam) > 1e-5
        res['max_re_lambda_excl_kernel'] = float(np.max(lam.real[big]))
        res['n_small_lambda'] = int(np.sum(~big))
        res['max_abs_small_lambda'] = float(np.max(np.abs(lam[~big]))) if (~big).any() else 0.0
        # list modes lambda = i w with 0 < w < |E|
        modes = []
        for j in np.argsort(lam.imag):
            l = lam[j]
            if l.imag > 1e-7 and l.imag < abs(E) and abs(l.real) < 1e-6 * max(1, abs(l.imag)) * 1e3:
                x = X[:, j]
                a, c = x[:n], x[n:]
                q = np.vdot(a, Ap @ a) + np.vdot(c, Am @ c)
                # real form: for lambda = i w take a real (rotate phase), d = Ap a / w
                ph = a[np.argmax(np.abs(a))]
                ar = (a / ph).real
                w = l.imag
                d = Ap @ ar / w
                resid = np.linalg.norm(Am @ d - w * ar) / np.linalg.norm(w * ar)
                modes.append(dict(w=float(w), re=float(l.real), krein_LxiXi=float(np.sign(q.real)),
                                  Lxixi=float(q.real / np.vdot(x, x).real), a_dot_d=float(ar @ d / (ar @ ar)),
                                  realform_resid=float(resid)))
        res['modes'] = modes
        # nonzero real / complex eigenvalues
        res['unstable'] = [complex(l) for l in lam if l.real > 1e-7]
        res['unstable'] = [[x.real, x.imag] for x in res['unstable']]
        # kernel checks
        if L == 0:
            cvec = pr.coeffs_of(r * sig)
            y = Li @ (pr.M @ cvec)  # transformed coords: y = L^T c ; use M c = L L^T c -> L^T c = L^{-1} M c
            res['kernel_check_Lminus_rsigma'] = float(np.linalg.norm(Am @ y) / np.linalg.norm(y))
        if L == 1:
            # sigma' via ODE dense output inside, numerical outside
            dsig = np.gradient(sig, r)
            inn = r <= bgobj.rc
            dsig[inn] = bgobj.bgin(r[inn])[1]
            cvec = pr.coeffs_of(r * dsig)
            y = Li @ (pr.M @ cvec)
            res['kernel_check_Lplus_rdsigma'] = float(np.linalg.norm(Ap @ y) / np.linalg.norm(y))
            # boost: L- (r^2 sigma) = -2 r sigma'
            c2 = pr.coeffs_of(r**2 * sig)
            y2 = Li @ (pr.M @ c2)
            res['boost_check'] = float(np.linalg.norm(Am @ y2 + 2 * y) / np.linalg.norm(2 * y))
        if L == 0:
            # Vakhitov-Kolokolov quantity <L+^{-1} a0, a0>, a0 = r sigma
            cvec = pr.coeffs_of(r * sig)
            y = Li @ (pr.M @ cvec)
            res['VK_Lplus_inv'] = float(y @ np.linalg.solve(Ap, y))
        out[L] = res
        if verbose:
            print(f"  L={L}: n(L+)={res['n_Lplus']} n(L-)={res['n_Lminus']} kerP={res['kernel_Lplus']} "
                  f"kerM={res['kernel_Lminus']} maxRe={res['max_re_lambda']:.3e}", flush=True)
            print(f"     L+ low: {np.array(res['Lplus_lowest'][:4])}", flush=True)
            print(f"     L- low: {np.array(res['Lminus_lowest'][:4])}", flush=True)
            for md in modes:
                print(f"     w={md['w']:.12f} re={md['re']:.1e} krein={md['krein_LxiXi']:+.0f} a.d={md['a_dot_d']:+.4e} resid={md['realform_resid']:.1e}", flush=True)
            if res['unstable']:
                print(f"     unstable: {res['unstable']}", flush=True)
            for k in ('kernel_check_Lminus_rsigma', 'kernel_check_Lplus_rdsigma', 'boost_check', 'VK_Lplus_inv'):
                if k in res:
                    print(f"     {k} = {res[k]:.6e}", flush=True)
    return out
