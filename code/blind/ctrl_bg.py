import sys, time, json
sys.path.insert(0, 'code/blind')
from bg import Background

out = {}
cases = [(0.19, -1, 0), (1.0, -1, 0), (1.03, -1, 0), (1.05, -1, 0), (1.89, -1, 0), (1.8, +1, 1), (0.5, +1, 1)]
for rtol in (1e-10, 1e-12):
    for sig0, s, n in cases:
        t = time.time()
        b = Background(sig0, s, n, rtol=rtol)
        I = b.integrals()
        vir = I['D'] - (2 * I['T'] + 3 * s * I['F'])    # eq. 26
        # E*N relation: E N = 2T + 4 s F - 4 D, N = 4 pi m
        EN = b.E * I['M4pi'] - (2 * I['T'] + 4 * s * I['F'] - 4 * I['D'])
        print(f"rtol={rtol:g} sig0={sig0} s={s} n={n}: u0={b.info['u0']:.15f} E={b.E:.15f} E33={I['E_eq33']:.15f} "
              f"m={I['m']:.13f} T={I['T']:.6f} F={I['F']:.6f} D={I['D']:.6f} vir={vir:.2e} EN={EN:.2e} "
              f"rc={b.rc:.2f} mism={b.info['logder_mismatch']:.1e} t={time.time()-t:.1f}s", flush=True)
