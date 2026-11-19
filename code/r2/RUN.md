# RUN: build-3 instruments (R2-BAND): hashes, commands per point, timings

Seat build-3, 2026-11-18. Folder: <LAB>/build-3/. build-1/ and build-2/ were not touched.
Every Python run goes through memcap:

    MC="python"

Environment: python-flint 0.9.0, numpy and scipy (as in build-2). Peak memory of every run was 0.79 GB. At most two
jobs ran at once. Changes: PATCHES.md. Controls and regression: CALIBRATION.md. Bar draft: BAR-R2-EDGES.md.
Helpers (not instruments, not on any proof path): aux/b3guess.py (float Newton guesses from the float map),
aux/b3compare.py (leaf-by-leaf JSON comparison), aux/b3patch.py and aux/b3patch2.py (the scripted patches),
aux/run_pair.sh and aux/run_chain.sh (runners), aux/b3peek.py and aux/b3pts.py (read the float-map files).

## Instruments (sha256; every build-3 output in CALIBRATION.md was produced by exactly these files)

| file | sha256 | vs build-2 |
|---|---|---|
| itaylor.py | c895713bb4f80fa96035cf27b2a6cc94e68aa2bafb5d7cb0404700304de3f1ca | changed (A3) |
| bg_tube.py | 46a104d245c3860b76910ab2353a4b60b92c82066d4dc4f09f7c9687a7528693 | changed (A4) |
| lincore.py | f9fa00ccd5931300c348e1448f6386088892c16f89137cd9779b784e6fd0f18c | changed (A2) |
| bracket.py | 4e48161bfd209205b03c8a033305f32fa18102867e2c693ba122eb53c467bf38 | changed (A3 caller, B1) |
| tail.py | 6c623c1c7a3dc353cbd809289d06dfb926f497318c5f32d7472585453b3ddf65 | changed (A1) |
| match.py | 3dbce1e54283c9e61e994c50b03f068777723a01a65f48839c10996be84b3632 | identical |
| kraw.py | b70ee710932a4cccd96991ddc739611ff4b21680df3a5db1b75f9a5d24c99b6b | identical |
| krein.py | f85b62a41987c2fd173cc1871ed4602cad24e864aa0676d73c8b9980492f1069 | changed (output keys, C2) |
| evans.py | 7dd008c628013c8f60caca7692c3df22528e8c4f74017b5e4c647389789c8d7f | changed (output keys, C3) |
| assemble.py | 21b0df28ee44ae0a4fddb2beedce989bee185a395a8903a122d9b5ba7e4486d4 | rewritten (C1) |
| verdict.py | f5f8e9bf0e86dfd8ce2534d8775c519d7c641bf2020d4135e3334384db70cae7 | extended (C4) |

See CALIBRATION.md "Provenance note": the eight R1 control jobs and B:p161 ran before a table-only edit of
assemble.py/verdict.py at 20:57:52; every later job ran with exactly these hashes.

## Seal guard
`assemble.py <KIND>:<tag>` exits 2 unless SEALED-<tag>.ok exists. I checked B:lo-s, K0:g170 and U:hi-u: each exits 2.
The calibration tags p161, u150 and u205 need no file. assemble.py asserts that none of them equals a
sealed-candidate sigma0. SEALED-r1.ok exists only for the 9/5 regression; it cites seal 07faff6621 +
AMENDMENT-R1-1. Every point tube is rebuilt in-run, and the disk cache is neither read nor written.

## Commands per point (only after the lead seals BAR-R2-EDGES.md)

    cd <LAB>/build-3
    # controls first (already run pre-seal; rerun is cheap and required if any instrument hash changed):
    $MC verdict.py controls ; $MC verdict.py controls-r2
    # for each sealed tag, after the lead creates its seal file:
    echo sealed > SEALED-<tag>.ok

Stable tags: lo-s (1597/1000), hi-s (1983/1000), g165 (33/20), g170 (17/10), g175 (7/4), g185 (37/20), g190 (19/10),
g195 (39/20).

    $MC -u assemble.py B:<tag>  > logs/B_<tag>.log  2>&1
    $MC -u assemble.py K0:<tag> > logs/K0_<tag>.log 2>&1
    $MC -u assemble.py K1:<tag> > logs/K1_<tag>.log 2>&1
    $MC -u assemble.py K2:<tag> > logs/K2_<tag>.log 2>&1
    $MC verdict.py point <tag>                      # -> out/<tag>/verdict.json

Unstable tags: lo-u (1595/1000, L = 0), hi-u (1985/1000, L = 2), in-155 (31/20, L = 0) and in-200 (2, L = 2).

    $MC -u assemble.py U:<tag>  > logs/U_<tag>.log  2>&1
    $MC verdict.py point <tag>

Rules for the runs:
- Run at most two jobs at once, e.g. `sh aux/run_pair.sh K0:lo-s K1:lo-s`.
- A stable verdict reads out/<tag>/{B,K0,K1,K2}.json and requires one tube_sha256 across them.
- If a stable point is INCONCLUSIVE, the refutation search is a separate run. Use the evans.py CLI at the float
  eigenvalue of the failing sector, written to out/<tag>/refute.json; verdict.py reads a dict or a list.
- Suggested order: the four edge points first (lo-u, lo-s, hi-s, hi-u), then the grid.

## Calibration commands run by this seat (pre-seal; logs in logs/)

| job | wall (two jobs at once) | result |
|---|---|---|
| B:p161 (probe, 161/100) | 107 s | counts = 9/5 counts; see CALIBRATION.md |
| C-B2 | 157 s | identical to build-2 |
| C-B1 | 217 s | identical |
| C-P1 | 105 s | identical |
| C-P2 | 425 s | identical |
| C-P3 | 338 s | identical |
| NULL | 542 s | identical |
| CAL-K | 465 s | identical |
| B:r1 | 120 s | identical to build-2 target-B (labels only differ) |
| K0:r1 | 502 s | identical to target-K0 |
| K1:r1 | 681 s | identical to target-K1 |
| K2:r1 | 676 s | identical to target-K2 |
| U:u150 (3/2, L=0) | 459 s | certified Re lambda > 0 |
| U:u205 (41/20, L=2) | 474 s | certified Re lambda > 0 |
| CAL-KD | 475 s | identical digits to CAL-K |
| CAL-ED | 481 s | identical digits to C-P2 evans |
| K0:p161 | 408 s (alone) | separation ok, signs -,+ |
| verdict controls / controls-r2 / point r1 | 1 s each | all PASS; r1 HOLDS |

Runner: `sh aux/run_chain.sh` (pairs via aux/run_pair.sh). Peak memory 0.80 GB.

## Projected time per point
- B job: 107-120 s (tube built in-run, about 90 s of it).
- K job: 408-681 s (K0 at 161/100 alone took 408 s; the K jobs at 9/5 took 502-681 s with two jobs at once).
- U job: 459-474 s (tube plus one complex Krawczyk).
- **Stable point (B + K0 + K1 + K2): about 33 min of compute, or about 20 min of wall with two jobs at once.**
- **Unstable point (U): about 8 min.**
- The full sealed set is 8 stable points (lo-s, hi-s, g165-g195) and 4 unstable points (lo-u, hi-u, in-155,
  in-200). That is about 4.4 h + 0.5 h = about 5 h of compute, or about 2.6 h of wall at two jobs at a time.
- The four edge points plus in-155 and in-200 alone take about 1.5 h of compute, or about 50 min of wall.
- Every single run stays under 12 min (limit 30).
- The near-edge Krawczyk steps (gap 7.5e-3 at lo-s, L = 0) are untested and may take one more epsilon-inflation;
  this does not change the order of magnitude.
