"""band/map: lightweight spectrum summary per (sigma0, L) using the blind seat's Galerkin engine (copied fem.py, bg.py).
NOT SEALED, float."""
import sys, time
import numpy as np
sys.path.insert(0, 'code/band-map')
from fem import Basis, RadialProblem
from bg import Background

S, NN, ALPHA = +1, 1, 1.0
THR = 1e-8      # Re lambda above this counts as unstable candidate (rounding is ~1e-11)
KSMALL = 1e-5   # |lambda| below this = generalised-kernel pair, excluded


def disc_auto(E, level=0):
    k = np.sqrt(-E)
    R = max(40.0, 70.0 / k)
    N = int(round(150 + 1.5 * (R - 40)))
    p, beta = 7, (2.0 if R <= 50 else 2.5)
    if level == 1:
        R, N, p = 1.5 * R, int(round(N * 1.67)), 9
    if level == 2:
        R, N, p = 1.25 * R, int(round(N * 1.35)), 8
    return R, N, p, beta


def background(sig0, u0guess=None, rtol=1e-10):
    return Background(sig0, S, NN, rtol=rtol, method='DOP853', u0guess=u0guess)


def summarize(b, R, N, p, beta, Ls, want_vk=True, nlow=8):
    E = b.E
    basis = Basis(R, N, p, beta)
    pr = RadialProblem(b.eval, basis, s=S, alpha=ALPHA)
    out = {}
    for L in Ls:
        Hp, Hm = pr.ops(L)
        Ap, Li = pr.sym(Hp)
        Am, _ = pr.sym(Hm)
        ep = np.linalg.eigvalsh(Ap)
        em = np.linalg.eigvalsh(Am)
        n = len(Ap)
        Z = np.zeros((n, n))
        lam, X = np.linalg.eig(np.block([[Z, Am], [-Ap, Z]]))
        big = np.abs(lam) > KSMALL
        res = dict(nLp=int(np.sum(ep < -1e-6)), nLm=int(np.sum(em < -1e-6)),
                   maxre=float(np.max(lam.real[big])))
        uns = [(float(l.real), float(abs(l.imag))) for l in lam[big] if l.real > THR and l.imag >= -1e-9]
        uns.sort(reverse=True)
        res['unst'] = uns
        res['n_unst'] = len(uns)
        # imaginary-axis modes with Krein sign (lowest nlow + all negative-Krein ones)
        modes = []
        for j in np.argsort(lam.imag):
            l = lam[j]
            if l.imag > KSMALL and abs(l.real) < 1e-6:
                x = X[:, j]
                q = (np.vdot(x[:n], Ap @ x[:n]) + np.vdot(x[n:], Am @ x[n:])).real
                modes.append((float(l.imag), int(np.sign(q))))
        res['negK'] = [w for w, k in modes if k < 0]
        res['low'] = modes[:nlow]
        res['n_im_below_E'] = int(sum(1 for w, k in modes if w < abs(E)))
        # Krein sign of unstable modes is zero by theory; also record L+ L- lowest
        res['Lp_low'] = ep[:3].tolist()
        res['Lm_low'] = em[:3].tolist()
        if L == 0 and want_vk:
            r = basis.rq
            cvec = pr.coeffs_of(r * pr.sig)
            y = Li @ (pr.M @ cvec)
            res['VK'] = float(y @ np.linalg.solve(Ap, y))
        out[L] = res
    return out


def point(sig0, Ls, u0guess=None, level=0, rtol=1e-10, disc=None):
    t = time.time()
    b = background(sig0, u0guess, rtol)
    # sanity: the n=1 repulsive branch has E < -0.2 and m > 4 on [0.3, 5] (coarse sweep); a stray bracket gives a
    # different object (seen once at 1.43: E = -0.034). Fall back to the full upward bracket search.
    if u0guess is not None and (b.E > -0.25 or abs(b.info['u0'] - u0guess) > 0.1 * (1 + abs(u0guess))):
        print(f"  [bg fallback at {sig0}: E={b.E} u0={b.info['u0']} guess={u0guess}]", flush=True)
        b = background(sig0, None, rtol)
    # cause found: tail start r_c taken at a grid sample sitting on the node (fixed in bg.py); guard anyway
    assert abs(b.info['logder_mismatch']) < 1e-2 and b.E < -0.25, f"bad background at {sig0}: {b.info}"
    tb = time.time() - t
    R, N, p, beta = disc if disc is not None else disc_auto(b.E, level)
    sp = summarize(b, R, N, p, beta, Ls)
    return dict(sig0=sig0, E=float(b.E), m=float(b.m), u0=float(b.info['u0']), rc=float(b.rc),
                disc=[R, N, p, beta], t_bg=tb, t=time.time() - t, L={str(k): v for k, v in sp.items()}), b.info['u0']
