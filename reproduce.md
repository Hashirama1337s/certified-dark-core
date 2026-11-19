# Reproduce

**In plain words.** These are the exact commands to check this release yourself, from quick checks that take
seconds to the full certified run that takes about half an hour on one core. Version 2.0 adds Tier 6, the
window: a check of all its outputs in seconds, one cell rerun in about 6 minutes, and the full run (81 minutes on two
lanes in the lab). Every command is run from the repository
root unless a step says `cd`. Paths are relative.

## Environment

- Python 3.11; python-flint 0.9.0 (Arb ball arithmetic); numpy, scipy, mpmath; matplotlib 3.11 for the figures.
- `pip install python-flint==0.9.0 numpy scipy mpmath matplotlib`
- Peak memory of every lab run was under 1.1 GB. No job reads a pickle; the background tube is stored as JSON strings.

## Tier 0: integrity (seconds)

```
sha256sum -c MANIFEST.sha256          # every shipped file against the manifest
python tools/check_numbers.py         # every number printed in the text against the file it names
python tools/canon.py --selftest      # the comparison tool ignores run times and catches real changes
python tools/make_scorecard.py        # rebuilds scorecard.svg / SCORECARD.md, checking the R1 verdict files first
```

The manifest is written by `python tools/make_manifest.py`.

## Tier 1: proof checks on the shipped certified outputs (about 3 minutes, plus about 15 minutes for check_u0_r2)

```
python -B checks/check_assembly.py      # K = (2, 2, 2, 0), D0, the six Krein signs, one tube sha (< 1 s)
python -B checks/check_frob_slack.py    # the Frobenius remainder constants bound the true ones (< 1 s)
python -B checks/check_U0.py            # rebuilds the tube from scratch; U0' lies inside the computed U0 (about 2 min)
python checks/verdict_blind.py data/blind/RESULT.json   # scores the blind replication exactly as sealed
python -B checks/check_frob_slack_r2.py   # the Frobenius check at the eight R2 stable points (< 1 s)
python -B checks/check_u0_r2.py lo-s g165 g170 g175   # U0'_p at four R2 points (tube rebuilds, about 6-8 min)
python -B checks/check_u0_r2.py g185 g190 g195 hi-s   # the other four
```

Expected last lines: `ALL PASS` for the three proof checks (shipped logs: `checks/*.log`); the blind verdict prints the
same scores as `data/blind/verdict_blind.out` (it prints the scores; there is no ALL PASS line).

## Tier 2: the certified R1 run (about 30 minutes on one core)

The instruments refuse the target jobs until a file `SEALED.ok` exists (the lab created it only after sealing).

```
cd code/r1
mkdir -p out/cal
echo sealed > SEALED.ok
python -u assemble.py target-B  > out/target-B.log  2>&1
python -u assemble.py target-K0 > out/target-K0.log 2>&1
python -u assemble.py target-K1 > out/target-K1.log 2>&1
python -u assemble.py target-K2 > out/target-K2.log 2>&1
for j in C-B1 C-B2 C-P1 C-P2 C-P3 NULL CAL-K; do python -u assemble.py $j > out/cal/$j.log 2>&1; done
python verdict.py controls
python verdict.py target                 # -> out/target_verdict.json: "verdict": "HOLDS"
cd ../..
```

Logged wall times in the lab (one job per core): target-B 78 s, target-K0 655 s, target-K1 621 s, target-K2 417 s;
the seven control jobs add about 35 minutes (field `wall_seconds` of each `data/r1/cal/*.json`; NULL is the longest at
531 s). At most two jobs were run at once.

**Compare with the shipped outputs.** `tools/canon.py` prints a canonical form that drops run times:

```
python tools/canon.py code/r1/out/target-K0.json > a.txt
python tools/canon.py data/r1/target-K0.json   > b.txt
diff a.txt b.txt
```

canon.py treats the free-text field `tube_source` ("built in this run (N s)") as a run-time key, so for every job type (R1 and R2)
the canonical comparison must print no difference: every enclosure, count, sign and the `tube_sha256` agree.

## Tier 3: the blind replication (minutes)

`code/blind/RUN.md` lists the seat's commands. Run them from the repository root, e.g.

```
python -u code/blind/run_main.py 9 5 3 s95 40 150 7 2 60 250 7 2 80 400 9 2.5
python -u code/blind/assemble.py
```

They write into `data/blind/` (overwriting the shipped copies; compare with `git diff` or the manifest).

## Tier 4: the float band map (about 25 minutes)

`data/band-map/MAP.md` ("Commands") lists every sweep. `analyze.py` reads every sweep file (sw_cA0, sw_cA, sw_cB,
sw_f1, sw_f2), the four edge files and the refinement checks chk_1.43_*, chk_1.79_*, chk_4_0 and chk_4.5_0 (all
shipped in `data/band-map/`), so run every command in MAP.md "Commands" first if you regenerate them. From the
repository root, e.g.

```
python -u code/band-map/sweep.py f1 1.30 1.85 0.01 14
python -u code/band-map/edge.py lo1 1.5962 1.5964 0 1 1e-7
python -u code/band-map/analyze.py
python figures/make_figures.py
```

These are float computations; they certify nothing.

## Tier 5: the certified R2 points (BAR-R2-EDGES)

The R2 instruments are `code/r2/` (changes from R1: PATCHES.md, part B). Per sealed point `<tag>`:

```
cd code/r2
mkdir -p logs
echo sealed > SEALED-<tag>.ok          # one guard file per tag you run
python -u assemble.py B:<tag>  > logs/B_<tag>.log 2>&1      # stable points: B, K0, K1, K2
python -u assemble.py K0:<tag> > logs/K0_<tag>.log 2>&1
python -u assemble.py K1:<tag> > logs/K1_<tag>.log 2>&1
python -u assemble.py K2:<tag> > logs/K2_<tag>.log 2>&1
python -u assemble.py U:<tag>  > logs/U_<tag>.log 2>&1      # unstable points: U only
python verdict.py controls ; python verdict.py controls-r2
python verdict.py point <tag>                                 # -> out/<tag>/verdict.json
```

Stable tags: lo-s, hi-s, g165, g170, g175, g185, g190, g195. Unstable tags: lo-u, hi-u, in-155, in-200. The lab's
projected cost was about 33 minutes of compute per stable point and about 8 minutes per unstable point
(`seals/BAR-R2-EDGES.md`, "Projected time"). The control jobs (C-B1 ... CAL-ED, u150, u205) are run first, as for R1.

## Tier 6: the window (version 2.0, BAR-W1)

**6a. Verify the shipped window outputs (seconds to minutes).** The referee-W3 checker imports nothing from the
instruments. It reads `data/r3/cells/*.json` and `data/r3/<node>/N.json` (plus each `tube.json`, whose sha256 it
recomputes) and re-applies the sealed per-cell rule in exact rational arithmetic to the printed enclosures.

```
python -B checks/w3/check_w3.py          # about 5 s; last lines: TOTAL PROBLEMS: 0 and ALL 22 CELLS HOLD, ALL 23 NODES OK, TILING EXACT
python -B checks/w3/nulls_w3.py          # 14 mutation tests; last line: NULLS: 14/14 behave as required
python -B checks/w3/float_spot.py c05 600   # FLOAT spot recompute of one cell, about 1-2 minutes (also c01, c11, c22)
```

Shipped logs: `checks/w3/logs/` (fresh runs from the repository root; identical to the referee's own logs except the
wall-time line of the float runs and the memory-cap line). `check_w3.py` also rewrites `checks/w3/logs/check_w3.json`; since version 2.0 it writes it with LF line endings on
every system (PATCHES.md, S22), so the rerun output is byte-identical to the shipped file and a later
`sha256sum -c MANIFEST.sha256` still passes. To be safe, run the manifest check before Tier 6a.

**6b. Rerun one cell from scratch (about 6 minutes).** The instruments are `code/r3/` (sha256 in `code/r3/RUN.md`).
Each node job and cell job refuses to run until its guard file `SEALED-<tag>.ok` exists, and the environment variable
`WSU` must be unset. A cell job reads both node outputs from `code/r3/out/`. The shortest cell is c22:

```
cd code/r3
unset WSU
mkdir -p logs
echo sealed > SEALED-n1980.ok ; echo sealed > SEALED-n1983.ok ; echo sealed > SEALED-c22.ok
python -u assemble_w.py N:n1980 > logs/N_n1980.log 2>&1     # logged 127 s
python -u assemble_w.py N:n1983 > logs/N_n1983.log 2>&1     # logged 86 s
python -u assemble_w.py C:c22  > logs/C_c22.log  2>&1       # logged 143 s
cd ../..
python tools/canon.py code/r3/out/cells/c22.json > a.txt
python tools/canon.py data/r3/cells/c22.json     > b.txt
diff a.txt b.txt
sha256sum code/r3/out/n1983/tube.json data/r3/n1983/tube.json
```

The node tags are `n` followed by 1000 σ0 (n1597 ... n1983); cells c01 ... c22 are the consecutive pairs
(`code/r3/assemble_w.py`). The canonical comparison drops run times; every enclosure, count and sha256 should agree.
This tier was repeated in a clean room for c22 and c11 (with their nodes): IDENTICAL-CANONICAL, tube hashes equal.
The commands are POSIX shell (`unset WSU`, `;`); on Windows, Git Bash works. If you run Python through a wrapper
that prints its own status lines (for example a memory-cap launcher), strip those lines from `a.txt` and `b.txt`
before the `diff`.

**6c. The full window run (81 minutes of wall time on two lanes in the lab).** `code/r3/run_w1.sh` is the lab's
driver (folders replaced, PATCHES.md part A): 23 node jobs, then 22 cell jobs, at most two at once, then
`python verdict_w.py window`, which writes `out/window_verdict.json` ("HOLDS on [1597/1000, 1983/1000]"). Logged walls:
86-127 s per node and 143-514 s per cell (`data/r3/logs/N_*.log`, `C_*.log`, the "done in" lines).

**6d. The controls (about 50 minutes of compute in the lab).** `code/r3/RUN.md`, "Commands", lists them. Two controls
(XK and R1REG) read the R2 outputs from `../../build-3/out` relative to `code/r3/` (the lab's folder layout). In this
repository those outputs are `data/r2/`, with the same sub-folder names, so first run, from the repository root:

```
mkdir -p build-3 && cp -r data/r2 build-3/out
```

Then `python verdict_w.py controls` in `code/r3/` must print `"all_pass": true`. The XU control at 1985/1000 uses the
re-count rule that was set after seeing its data (PAPER.md, Section 12.11). One control cannot be rerun from this
repository: XC (a float control) imports the lab's float probe helpers (`design/probe/fbg.py` and its float
background solver), which are design probes, not instruments, and are not shipped; its output is shipped
(`data/r3/controls/XC.jsonl`); copy it to `code/r3/out/controls/` before `verdict_w.py controls`, which reads it
from there.
