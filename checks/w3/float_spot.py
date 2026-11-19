"""referee-W3 FLOAT spot recompute (own discretisation; nothing imported from build-W).

Background: shooting on u(0) for the one-node decaying solution of
    sigma'' + 2 sigma'/r = sigma^3 - u sigma,   u'' + 2 u'/r = -sigma^2,   sigma(0) = sigma0
(F(sigma,u) = (-Lap sigma + sigma^3 - u sigma, -Lap u - sigma^2), s = 1). Beyond the divergence radius sigma := 0,
u := E + m/r.
Operators in reduced variables a = r d on r_i = i h (Dirichlet at 0 and Rb), second-order FD, Richardson (h, h/2):
    L+ = -D2 + l(l+1)/r^2 + 3 sigma^2 - u - K_l,  K_l(r,s) = 2 sigma(r) sigma(s) r s r_<^l / ((2l+1) r_>^(l+1)),
    L- = -D2 + l(l+1)/r^2 + sigma^2 - u,          H(w) = [[L+, -w], [-w, L-]].
Outputs per spot cell: E at both ends (vs certified), sanity kernels, end margins (lambda_{k+1}), counts N(w1), N(w2)
at ends and at theta = 1/2, chord loss at theta = 1/2 on a COMMON subspace, versus eta2(1/2), eta2'(1/2) of the cell.
"""
import json, sys, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import eigh
from fractions import Fraction as Fr

BW = 'data/r3'
KUP = {0: 3, 1: 2, 2: 1}
UPM = {0: 4, 1: 3, 2: 2, 3: 0}


def rhs(r, y):
    s, sp, u, up = y
    return [sp, -2 * sp / r + s ** 3 - u * s, up, -2 * up / r - s * s]


def shoot(s0, u0, rmax=40.0):
    r0 = 1e-4
    # series start: s = s0 + c r^2, c = (s0^3 - u0 s0)/6 ; u = u0 - s0^2 r^2 / 6
    c = (s0 ** 3 - u0 * s0) / 6
    y0 = [s0 + c * r0 ** 2, 2 * c * r0, u0 - s0 ** 2 * r0 ** 2 / 6, -s0 ** 2 * r0 / 3]
    ev = lambda r, y: abs(y[0]) - 2.5 * s0
    ev.terminal = True
    sol = solve_ivp(rhs, (r0, rmax), y0, method='DOP853', rtol=1e-13, atol=1e-16, events=ev, dense_output=True)
    s = sol.y[0]
    z = int(np.sum(np.sign(s[1:]) != np.sign(s[:-1])))
    return sol, z


def find_state(s0):
    us = np.arange(-4.0, 12.0, 0.05)
    prev = None
    for u0 in us:
        _, z = shoot(s0, u0)
        if prev is not None and prev[1] <= 1 and z >= 2:
            lo, hi = prev[0], u0
            break
        prev = (u0, z)
    else:
        raise RuntimeError('no 1->2 node transition')
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        _, z = shoot(s0, mid)
        if z >= 2:
            hi = mid
        else:
            lo = mid
    sol, z = shoot(s0, lo)
    # cut radius: where |sigma| reaches its minimum magnitude before diverging
    rr = np.linspace(sol.t[0], sol.t[-1], 20001)
    Y = sol.sol(rr)
    sg = np.sign(Y[0]); iz = int(np.nonzero(sg[1:] != sg[:-1])[0][0]) + 1
    k = iz + int(np.argmin(np.abs(Y[0][iz:])))
    rc = rr[k]
    uc, upc = Y[2][k], Y[3][k]
    m = -rc * rc * upc
    E = uc - m / rc
    return dict(s0=s0, u0=lo, sol=sol, rc=rc, E=E, m=m, zeros=1)


def bg_on(st, r):
    s = np.zeros_like(r); u = np.empty_like(r)
    inn = r <= st['rc']
    Y = st['sol'].sol(np.maximum(r[inn], st['sol'].t[0]))
    s[inn] = Y[0]; u[inn] = Y[2]
    u[~inn] = st['E'] + st['m'] / r[~inn]
    return s, u


class Ops:
    def __init__(self, st, N, Rb):
        self.h = Rb / (N + 1); self.r = self.h * np.arange(1, N + 1); self.N = N
        self.s, self.u = bg_on(st, self.r)

    def blocks(self, l):
        N, h, r, s, u = self.N, self.h, self.r, self.s, self.u
        D = (np.diag(np.full(N, 2.0)) - np.diag(np.ones(N - 1), 1) - np.diag(np.ones(N - 1), -1)) / h ** 2
        cen = l * (l + 1) / r ** 2
        rl, rg = np.minimum.outer(r, r), np.maximum.outer(r, r)
        K = 2 * np.outer(s * r, s * r) * rl ** l / ((2 * l + 1) * rg ** (l + 1)) * h
        Lp = D + np.diag(cen + 3 * s * s - u) - K
        Lm = D + np.diag(cen + s * s - u)
        return Lp, Lm

    def H(self, l, w):
        Lp, Lm = self.blocks(l)
        I = np.eye(self.N)
        return np.block([[Lp, -w * I], [-w * I, Lm]])


def comp_min(H, P):
    Q, _ = np.linalg.qr(P, mode='complete')
    C = Q[:, P.shape[1]:]
    return float(eigh(C.T @ H @ C, eigvals_only=True, subset_by_index=[0, 0])[0])


def comp_max(H, V):
    Q, _ = np.linalg.qr(V)
    return float(np.linalg.eigvalsh(Q.T @ H @ Q)[-1])


def lam(H, i):
    return float(eigh(H, eigvals_only=True, subset_by_index=[i, i])[0])


def nneg(H):
    return int(np.sum(np.linalg.eigvalsh(H) < 0))


def ivlo(s):
    s = s.strip('[]').split('+/-'); return float(s[0]) - float(s[1])


def ivhi(s):
    s = s.strip('[]').split('+/-'); return float(s[0]) + float(s[1])


def main(cid, N=1000, Rb=24.0):
    t0 = time.time()
    c = json.load(open('%s/cells/%s.json' % (BW, cid)))
    a, b = (float(Fr(x)) for x in c['cell'])
    tags = ['n%d' % int(Fr(x) * 1000) for x in c['cell']]
    Ecert = [json.load(open('%s/%s/N.json' % (BW, t)))['E'] for t in tags]
    sts = {0.0: find_state(a), 1.0: find_state(b), 0.5: find_state(0.5 * (a + b))}
    print('== %s [%s, %s]  (N = %d, %d; Rb = %g)' % (cid, c['cell'][0], c['cell'][1], N, 2 * N, Rb))
    for t, k in ((0.0, 0), (1.0, 1)):
        Ec = Ecert[k]
        print('  E float %.10f  certified %s  inside: %s' % (sts[t]['E'], Ec, ivlo(Ec) - 1e-8 <= sts[t]['E'] <= ivhi(Ec) + 1e-8))
    print('  E float at mid %.8f ; |E| lower bound of the cell %s' % (sts[0.5]['E'], c['absE_lower']))
    ops = {t: (Ops(st, N, Rb), Ops(st, 2 * N, Rb)) for t, st in sts.items()}
    rich = lambda f: (4 * f(1) - f(0)) / 3          # f(j): value on grid j (0 = N, 1 = 2N)
    # sanity: L-(0) sigma = 0 and L+(1) sigma' = 0 (tests the nonlocal factor 2 and the background)
    o = ops[0.0]
    k0 = rich(lambda j: min(abs(np.linalg.eigvalsh(o[j].blocks(0)[1]))))
    k1 = rich(lambda j: min(abs(np.linalg.eigvalsh(o[j].blocks(1)[0]))))
    print('  sanity: |lowest-|eig| of L-(0)| %.2e, of L+(1) %.2e (both should be ~0)' % (k0, k1))
    CH = c['CH']
    out = dict(cell=cid, rows=[])
    for l in (0, 1, 2):
        h = c['certs']['H(w2) L%d' % l]; rz = c['certs']['RITZ L%d' % l]
        k = KUP[l]
        w2 = {0.0: h['wa'], 1.0: h['wb']}; w2[0.5] = 0.5 * (h['wa'] + h['wb'])
        w1 = {0.0: rz['w1a'], 1.0: rz['w1b']}; w1[0.5] = 0.5 * (rz['w1a'] + rz['w1b'])
        # end margins lambda_{k+1}(H(w2)) (Richardson) vs certified ma, mb
        em = {t: rich(lambda j: lam(ops[t][j].H(l, w2[t]), k)) for t in (0.0, 1.0)}
        er = {t: rich(lambda j: lam(ops[t][j].H(l, w1[t]), k)) for t in (0.0, 1.0)}   # top of the k+1 lowest (Ritz top)
        cnt = {t: (nneg(ops[t][1].H(l, w1[t])), nneg(ops[t][1].H(l, w2[t]))) for t in (0.0, 0.5, 1.0)}
        # chord loss at theta = 1/2 on the common subspace from end a (grid 2N; also grid N to show stability)
        loss_u = []; loss_l = []
        for j in (0, 1):
            Ha = ops[0.0][j].H(l, w2[0.0]); _, V = np.linalg.eigh(Ha); P = V[:, :k]
            vals = {t: comp_min(ops[t][j].H(l, w2[t]), P) for t in (0.0, 0.5, 1.0)}
            loss_u.append(0.5 * (vals[0.0] + vals[1.0]) - vals[0.5])
            H1 = ops[0.0][j].H(l, w1[0.0]); _, V1 = np.linalg.eigh(H1); S = V1[:, :k + 1]
            tops = {t: comp_max(ops[t][j].H(l, w1[t]), S) for t in (0.0, 0.5, 1.0)}
            loss_l.append(tops[0.5] - 0.5 * (tops[0.0] + tops[1.0]))
        eta2 = ivhi(CH[str(l)]['C0']) + ivhi(CH[str(l)]['C1']) / 4
        eta2p = ivhi(CH[str(l)]['C0p']) + ivhi(CH[str(l)]['C1p']) / 4
        print('  L%d H(w2): float margin a %.4e b %.4e | certified ma %s mb %s | ma<=float: %s' % (
            l, em[0.0], em[1.0], h['ma'], h['mb'], ivhi(h['ma']) <= em[0.0] and ivhi(h['mb']) <= em[1.0]))
        print('      RITZ: float top a %.4e b %.4e | certified -ma %s -mb %s | top<=-m: %s' % (
            er[0.0], er[1.0], rz['ma'], rz['mb'], er[0.0] <= -ivhi(rz['ma']) and er[1.0] <= -ivhi(rz['mb'])))
        print('      counts (N(w1), N(w2)) at t=0, 1/2, 1: %s %s %s  (need (%d, %d))' % (cnt[0.0], cnt[0.5], cnt[1.0], k + 1, k))
        print('      chord loss at 1/2, upper: %s vs eta2(1/2) %.3e ; lower: %s vs eta2p(1/2) %.3e ; within: %s' % (
            ['%.3e' % x for x in loss_u], eta2, ['%.3e' % x for x in loss_l], eta2p,
            loss_u[1] <= eta2 and loss_l[1] <= eta2p))
        out['rows'].append(dict(L=l, em=em, er=er, cnt=cnt, loss_u=loss_u, loss_l=loss_l, eta2=eta2, eta2p=eta2p))
    for l in (0, 1, 2, 3):
        k = UPM[l]; hc = c['certs']['H(0) L%d' % l]
        em = {t: rich(lambda j: lam(ops[t][j].H(l, 0.0), k)) for t in (0.0, 1.0)}
        j = 1
        Ha = ops[0.0][j].H(l, 0.0); _, V = np.linalg.eigh(Ha); P = V[:, :k]
        if k:
            vals = {t: comp_min(ops[t][j].H(l, 0.0), P) for t in (0.0, 0.5, 1.0)}
        else:
            vals = {t: lam(ops[t][j].H(l, 0.0), 0) for t in (0.0, 0.5, 1.0)}
        loss = 0.5 * (vals[0.0] + vals[1.0]) - vals[0.5]
        eta2 = ivhi(CH[str(l)]['C0']) + ivhi(CH[str(l)]['C1']) / 4
        # block purity of the k lowest eigenvectors of H(0) at both ends (needed for the K-row split)
        pur = []
        for t in (0.0, 1.0):
            _, V = np.linalg.eigh(ops[t][j].H(l, 0.0)); M = ops[t][j].N
            pur.append(max(min(np.linalg.norm(V[:M, i]), np.linalg.norm(V[M:, i])) for i in range(k)) if k else 0.0)
            ev = np.linalg.eigvalsh(ops[t][j].H(l, 0.0))[:k + 2]
        print('  H(0) L%d: float margin a %.4e b %.4e | certified ma %s mb %s | ma<=float: %s | loss %.3e vs eta2 %.3e | max mixing %.1e' % (
            l, em[0.0], em[1.0], hc['ma'], hc['mb'], ivhi(hc['ma']) <= em[0.0] and ivhi(hc['mb']) <= em[1.0], loss, eta2, max(pur)))
    print('  seconds %.0f' % (time.time() - t0))


if __name__ == '__main__':
    main(sys.argv[1], N=int(sys.argv[2]) if len(sys.argv) > 2 else 1000)
