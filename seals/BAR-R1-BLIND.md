# BAR-R1-BLIND: blind float replication of the R1 counts and Krein frequencies (doctrine #31)

Written 2026-11-18 by the lead, after referee-5 (core/seats/referee-5/REFEREE-R1-PROOF.md) asked for one blind seat. The owner
said "Yes, finish it". The blind seat gets only the paper and an object definition. It never sees this bar, build-1,
build-2, proof/, seats/ or any earlier output.

## Disclosed before sealing
- The certified values (build-2/out, AMENDMENT-R1-1 6ad54f5713) are known to the lead and are the predictions below.
- Three non-blind float checks (referee-3 FD, referee-4 Chebyshev, referee-5 FD) already agree with them.
- So this bar tests whether a seat that never saw the numbers reproduces them from the paper alone. Its main risk is a
  convention mismatch (units, sign of the nonlocal term, factor 2 in time), which is exactly what it is meant to catch.

## Object (as given to the blind seat)
The one-node (n = 1) repulsive Gross-Pitaevskii-Poisson stationary state of arXiv 2402.07998, alpha = 1, sigma0 = 9/5.
Its linearisation J L per angular sector L (eqs. 35-37, 43). The seat chooses its own method.

## Predictions (scored by the lead with a verdict script; POST HOC labels forbidden)
- **PB1 (background).** E in [-3.1055, -3.1054] and mass m in [19.158, 19.159]. This is a convention check. If it fails, the
  bar is VOID (a convention mismatch, not a refutation), and the reason is reported.
- **PB2 (counts).** n(L+) = (2, 1, 1, 0) and n(L-) = (1, 1, 1, 0) for L = 0, 1, 2, 3, after the seat removes the
  symmetry kernels (phase at L = 0, translation at L = 1). The seat must report the kernels it removed.
- **PB3 (negative-Krein frequencies).** For L = 0, 1, 2 the seat reports exactly one frequency w in (0, |E|) whose
  Krein sign <a, d> is negative. It lies within relative 1e-4 of 1.1049110805, 0.5399256680 and 0.2968148506
  respectively.
- **PB4 (positive-Krein neighbours).** A positive-Krein frequency is reported within relative 1e-4 of 1.2592133714,
  0.9510282377 and 0.5179458643 (L = 0, 1, 2).
- **PB5 (no growth).** The max of Re lambda over L = 0..3 is below 1e-3, with any residual attributed to discretised
  kernel modes that shrink under refinement (the seat must show two resolutions).

## Controls
- **Positive control PC.** At sigma0 = 1/2 (same n, sign and alpha) the seat must find a growing L = 0 mode with
  Re lambda > 0. Its value lies within relative 1e-3 of 0.0241322927 + 0.2832272004 i. If no growing mode is found:
  VOID (the method cannot see instability).
- **Null.** The PC itself is the null of PB5: same pipeline, a background outside the stable band.

## Verdict
- HOLD if PB1-PB5 and PC all pass.
- FAILED if PB1 and PC pass but any of PB2-PB5 misses. The lead then checks for a convention mismatch before reporting;
  any such finding is logged, not used to rescore.
- VOID if PB1 or PC fails.

## Not claimed
- This is a float replication. It certifies nothing by itself; the certificate is 07faff6621 / 6ad54f5713.

## Seal fields
- formula_ref: <LAB-ROOT>/seats/frontier/dl/2402.07998.txt:822-861
- calibrated_on: none - the predicted values are the certified outputs of 6ad54f5713, disclosed above; tolerances set before the blind seat runs
- depends_on: 07faff6621
- null_not_symmetry: sigma0 = 1/2 is a different background with a known growing mode; it tests that the blind method can see instability
- target_form: integer counts per L; float frequencies with Krein signs; max Re lambda; one complex eigenvalue at sigma0 = 1/2
- parameters: sigma0 = 9/5, 1/2; L = 0, 1, 2, 3; resolution = at least two, chosen by the seat
- tolerances: relative 1e-4 on frequencies, because float discretisation at modest resolution reaches 1e-7 to 1e-12 in the three non-blind checks; 1e-3 on the PC eigenvalue; counts exact
- ceiling: an independent blind reproduction of every decisive number of the R1 certificate
- positive control: PC at sigma0 = 1/2
- toy_model: PB1 background energy and mass
- baseline: the three non-blind float checks (referee-3, referee-4, referee-5)
- files: BAR-R1-BLIND.md
- command: the blind seat's own (core/blind/seat/RUN.md), under memcap 8
