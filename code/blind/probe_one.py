import sys, time
sys.path.insert(0, 'code/blind')
import numpy as np
import mpmath as mp
from bg import Background
sig0, s, n = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
t = time.time()
import os
b = Background(sig0, s, n, rtol=float(os.environ.get("BG_RTOL","1e-12")), method=os.environ.get("BG_METHOD","DOP853"))
print("shoot+profile", time.time() - t, b.info, flush=True)
# tail check: asymptotic series vs mpmath whittaker
for f in (1.0, 1.5, 3.0):
    r = b.rc * f
    ex = float(b.W(r) / b.Wc)
    print(f"tail ratio r={r:.2f}: asym={b.Wasym(np.array([r]))[0]:.15e} mpmath={ex:.15e}", flush=True)
t = time.time()
I = b.integrals()
print("integrals", time.time() - t, I, flush=True)
vir = I['D'] - (2 * I['T'] + 3 * s * I['F'])
EN = b.E * I['M4pi'] - (2 * I['T'] + 4 * s * I['F'] - 4 * I['D'])
print("virial resid", vir, "EN resid", EN, "E", b.E, "E33", I['E_eq33'], flush=True)
rr = np.linspace(1e-3, b.rc, 200001)
sg = b.eval(rr)[0]
idx = np.where(sg[1:] * sg[:-1] < 0)[0]
print("nodes:", len(idx), "at r ~", rr[idx], flush=True)
import scipy.optimize as so
for i in idx:
    rz = so.brentq(lambda x: b.eval(np.array([x]))[0][0], rr[i], rr[i + 1], xtol=1e-15)
    print("node r =", repr(rz), flush=True)
