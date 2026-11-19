import sys, time
sys.path.insert(0, 'code/blind')
import numpy as np
from bg import count_nodes
t = time.time()
for u0 in np.linspace(3.3, 12, 30):
    k, sol = count_nodes(1.8, u0, +1, 80.0, 1e-8)
    print(f"u0={u0:.3f} k={k} rend={sol.t[-1]:.2f} nsteps={len(sol.t)} t={time.time()-t:.2f}", flush=True)
