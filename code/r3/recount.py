"""recount.py - XU single-point re-count (lead rule, 2026-11-19, set after seeing XU-1985 data): an undecided count of the
XU scan is re-counted at the SAME w with finer levels (1e-6, then 1e-7) using the unchanged node.counts_at (hw3.count:
re-based march, same R = 20). Any level > 0 is rigorous: #(H <= 0) <= #(H < +lev) and #(H < 0) >= #(H < -lev).
Output: out/controls/XU_<tag>_recount.json; verdict_w.xu_merge replaces an undecided scan point by a re-count only if
BOTH re-counted counts are decided. Usage: recount.py <tag> <w> [levels...]"""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import node as nd
import hw3

tag = sys.argv[1]; w = float(sys.argv[2])
levels = [float(x) for x in sys.argv[3:]] or [1e-6, 1e-7]
t0 = time.time()
s0, L = nd.UNSTABLE[tag]; x = nd.label(s0)
steps, info, Yend = nd.tube(s0, False, log=lambda *a: None)
bj = hw3.setup(steps, Yend, 24)
rows = []
for lev in [1e-5] + levels:
    c = nd.counts_at(bj, steps, info, x, L, w, lev, 20.0)
    rows.append(dict(w=w, lev=lev, upper=c['upper'], lower=c['lower'], why=c['why'], ext=c['ext']))
    print('w %g lev %g: upper %s lower %s why %s' % (w, lev, c['upper'], c['lower'], c['why']), flush=True)
dec = [r for r in rows if r['upper'] is not None and r['lower'] is not None and r['lev'] != 1e-5]
rec = dict(job='RECOUNT:%s:%g' % (tag, w), sig0=s0, L=L, tube_sha256=info['tube_sha256'], rows=rows,
           decided=dec[0] if dec else None, seconds=time.time() - t0)
fn = os.path.join(HERE, 'out', 'controls', 'XU_%s_recount.json' % tag)
old = json.load(open(fn)) if os.path.exists(fn) else []
old = [o for o in old if o['rows'][0]['w'] != w]
json.dump(old + [rec], open(fn, 'w'), indent=1, default=str)
print('done in %.0f s; decided: %s' % (rec['seconds'], rec['decided']))
