# RUN: build-W instruments (R3-WINDOW): hashes, commands, projected time

Seat build-W, 2026-11-19. Folder: <LAB>/window/build-W/. build-1/2/3 untouched.
Every Python run goes through memcap:

    MC="python"

Environment: python-flint 0.9.0 (arb, arb_poly, arb_series; ctx.cap raised inside hw3.PolyFn), numpy, scipy,
sympy (only for the derivation in DESIGN-W3; the generated formulas are checked at run time by cell._sym_check).
Peak memory of every run so far: 0.99 GB. The environment variable WSU must be UNSET for sealed runs (green.SU = 3).

## Instruments (sha256; every final control output in CALIBRATION.md was produced by exactly these files)

| file | sha256 | origin |
|---|---|---|
| itaylor.py | c895713bb4f80fa96035cf27b2a6cc94e68aa2bafb5d7cb0404700304de3f1ca | build-3, identical |
| bg_tube.py | 46a104d245c3860b76910ab2353a4b60b92c82066d4dc4f09f7c9687a7528693 | build-3, identical |
| lincore.py | f9fa00ccd5931300c348e1448f6386088892c16f89137cd9779b784e6fd0f18c | build-3, identical |
| bracket.py | 4e48161bfd209205b03c8a033305f32fa18102867e2c693ba122eb53c467bf38 | build-3, identical |
| tail.py | 6c623c1c7a3dc353cbd809289d06dfb926f497318c5f32d7472585453b3ddf65 | build-3, identical (not on the window path) |
| match.py | 3dbce1e54283c9e61e994c50b03f068777723a01a65f48839c10996be84b3632 | build-3, identical (not on the window path) |
| kraw.py | b70ee710932a4cccd96991ddc739611ff4b21680df3a5db1b75f9a5d24c99b6b | build-3, identical (not on the window path) |
| krein.py | f85b62a41987c2fd173cc1871ed4602cad24e864aa0676d73c8b9980492f1069 | build-3, identical (not on the window path) |
| evans.py | 7dd008c628013c8f60caca7692c3df22528e8c4f74017b5e4c647389789c8d7f | build-3, identical (not on the window path) |
| assemble.py | 21b0df28ee44ae0a4fddb2beedce989bee185a395a8903a122d9b5ba7e4486d4 | build-3, identical (not on the window path) |
| verdict.py | f5f8e9bf0e86dfd8ce2534d8775c519d7c641bf2020d4135e3334384db70cae7 | build-3, identical (not on the window path) |
| hw3.py | a9e9b2c04830d79bcced98dfedcb9553d6f6f5426b57b2af129de922273c0eff | new (unchanged by the audit) |
| green.py | a01a44784b0237822e8459e34d839fbf99a64104856ec603f34d589d1ed04914 | new (audit G-1) |
| cell.py | d9b865e40b3bfb4fe1a5fac1fcf75108a639b3774724605f47360d61c40386bb | new (audit C-1..C-6, End assertion) |
| node.py | f558a038155c03e08a57859d294b3d1c30b0220682b641809169768879bfabfa | new (XU split; audit N-1) |
| assemble_w.py | ee5a1080631e9f1f5e6a116a4d89255f774b63a50f8204bdf377665a0f5ca9c1 | new (XU split; WSU assert) |
| verdict_w.py | cf79e09bd252a8f8bcb3c2cf34a480b2c0f92ea038df1b7b20f71dc4006820a3 | new (xu_merge: XU_TOP_MARGIN = 1e-3 and the re-count rule (lead, after seeing data); FAILED-by-brackets; XC set; reads JSON only) |
| recount.py | 9599b8a60c16878854f5e9f1cd3061d6affeb5144cd910dfa4bdee7b8d47d7af | new (XU single-point re-count; uses node.counts_at unchanged) |
| steer.py | 4deb7f861ecad3a58283c194ed794953a8e108aeb57b6c64c96203622301a5bb | new (float steering) |
| xc.py | 6fcc1da9b04ad35386e0b3d4144b8f85c82315e91320a4d85fce678871f74633 | new (float control) |
| guard_test.py | 52510a9a9d476fba1c481a4f73c42d888f7fb20e6b73ff6c4f172be30f13c189 | new (seal-guard test) |

Every control in CALIBRATION.md (final batch, 2026-11-19 after the audit) was produced by exactly these hashes. If any hash changes, rerun the controls.

## Seal guard
`assemble_w.py N:<tag>` and `C:<cid>` exit 2 unless SEALED-<tag>.ok / SEALED-<cid>.ok exists. Control jobs (XK, XU,
LOO, XI, R1REG) need no file and touch only the G9 nodes, 1595/1000, 1985/1000, 161/100, 31/20 and the cells
named in assemble_w.LOO_CELLS.

## Commands

Controls (already run pre-seal; rerun is required if a hash changes; about 50 min of compute):

    cd <LAB>/window/build-W
    for t in lo-s g165 g170 g175 r1 g185 g190 g195 hi-s; do $MC -u assemble_w.py XK:$t > logs/XK_$t.log 2>&1; done
    $MC -u assemble_w.py R1REG ; $MC -u assemble_w.py XU:lo-u
    for r in 1-130 131-156 157-182 183-208 209-234 235-246 247-252 253-258; do $MC -u assemble_w.py XU:hi-u:0.01:$r; done   # j-range parts up to w_max - 1e-3 (j = 258), at most two at once
    $MC -u recount.py hi-u 2.27 1e-6 1e-7                                  # the undecided point of the scan
    $MC -u assemble_w.py LOO:loo-161 --sectors ; $MC -u assemble_w.py LOO:loo-1595 ; $MC -u assemble_w.py XI
    : > out/controls/XC.jsonl        # fresh file: exactly the 5 sealed points
    for a in "1.597 1.6 1.5985 0 1.0153 1.0177" "1.75 1.8 1.775 0 1.14 1.182" "1.75 1.8 1.775 1 0.73 0.745" \
             "1.75 1.8 1.775 2 0.39 0.407" "1.95 1.983 1.98 2 0.47 0.4634"; do $MC xc.py $a >> out/controls/XC.jsonl; done
    $MC verdict_w.py controls          # must print "all_pass": true
    $MC guard_test.py                  # seal guard at non-window tags: GUARD TEST PASS

Window (only after the lead seals BAR-W1.md):

    for each node tag n1597 ... n1983:  echo sealed > SEALED-<tag>.ok ; $MC -u assemble_w.py N:<tag> > logs/N_<tag>.log 2>&1
    for each cell c01 ... c22:          echo sealed > SEALED-<cid>.ok ; $MC -u assemble_w.py C:<cid> > logs/C_<cid>.log 2>&1
    $MC verdict_w.py window

At most two jobs at once (nodes first; a cell needs both its node outputs). Every job is far below 30 min.

## Measured unit costs (CALIBRATION.md)
- Node: tube built in-run 75-120 s (XK runs: 90-135 s including 30-40 s of counts); brackets 25 s; GREEN 3-5 s
  (columns 2.7 s, kernel 0.3 s, apply 0.1 s). About 2.2 min per node.
- Cell: cross-grid Taylor models 7.6 s, BR' + CH 9 s, the 11 certificates at both ends with the float pre-pass about
  200 s: 221 s measured on the LOO-161 cell. About 3.7 min per cell.
- XK: 90-135 s per node; XU: one count pair about 5 s, scan step 0.01 (see CALIBRATION.md for the measured walls).

## Projection (full sealed run)
- Nodes: 23 x 2.2 min = 51 min. Cells: 22 x 3.7 min = 81 min. Total about 2.2 lane-hours, about 1.1 h of wall on two
  lanes; with bisections of up to 4 cells (contingency x 1.3) about 1.5 h of wall.
- SPEEDUP-W1 projected 31 min for the cells; the measured cost is 2.6 times higher (the 11 certificates per end, as
  referee-W2 re-projected: 22 to 88 min). The design's threshold (2 h wall) holds.
