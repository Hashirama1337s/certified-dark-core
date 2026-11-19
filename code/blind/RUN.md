# RUN.md - commands (cwd code/blind)

Prefix for every run: `python -u`  (peak memory under 1 GB, every run under 1 min except ctrl_bg ~2 min)

1. `probe_bg.py`  - 2-minute probe: node-count classification speed at sigma0 = 1.8.
2. `probe_one.py 1.0 -1 0`, `probe_one.py 0.19 -1 0`, `probe_one.py 1.89 -1 0`  - attractive n=0 controls (paper Fig. 5 T, F).
3. `probe_one.py 1.8 1 1`, `probe_one.py 0.5 1 1`, each with BG_METHOD=DOP853 and BG_METHOD=LSODA  - targets: background, node radius, second integrator.
4. `ctrl_bg.py > ctrl_bg.log`  - background controls at rtol 1e-10 and 1e-12 (adds sigma0 = 1.03, 1.05 attractive).
5. `ctrl_spec.py > ctrl_spec.log`  - spectral controls (repulsive n=0; attractive n=0 at 0.19 and 1.89; VK identity vs finite differences).
6. `run_main.py 9 5 3 s95 40 150 7 2 60 250 7 2 80 400 9 2.5 > main_s95.log`
   `BG_RTOL=1e-10 run_main.py 9 5 3 s95_rtol10 60 250 7 2 > main_s95_rtol10.log`
7. `run_main.py 1 2 0 s12 80 200 7 2.5 120 300 7 2.5 160 450 9 3 > main_s12.log`
   `BG_RTOL=1e-10 run_main.py 1 2 0 s12_rtol10 120 300 7 2.5 > main_s12_rtol10.log`
   (arguments: sigma0 numerator, denominator, Lmax, tag, then quadruples R N p beta = box radius, number of
   B-spline intervals, spline degree, sinh-grading parameter)
8. `compare.py raw_s95_rtol10.json raw_s95.json` (mode-by-mode changes), `assemble.py > assemble.log` -> RESULT.json

Note: one early run of ctrl_bg.py (old slow mpmath tail) was killed by its own `timeout 600`; superseded by item 4.
raw_probe.json is the first probe of the spectrum (R=40, N=150), superseded by raw_s95.json.
