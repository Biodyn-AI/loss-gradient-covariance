# Independent saved-result audit of the prospective paired-decay contrast

17 November 2026. Read-only deterministic audit, independently reconstructing
the stored sampling units and arithmetic. All62 checks passed. No scientific
RNG constructor, PRNG advancement replay, native trajectory, model run or
source modification occurred. All original study/consumer/prediction bytes
remain unchanged.

| Artifact | SHA-256 |
|---|---|
| Complete analyzed consumer summary | `db1802a09c53214dc21e62f53829b7a1b9afb140ca717de83a04149aba3e201a` |
| Independent successful audit source | `544a033fb046084366b45dfea0fc3e9afeeea5a261946c9674385baf8296546b` |
| Successful full audit receipt | `ae623973bdd4127e37b891d2567769215e2327723ea2c3639f398a91bf85c794` |

The source and receipt are respectively
`results/q2_decay_contrast_independent_audit_20261117/audit_v2.py` and
`audit_v2.json`. The script refuses to overwrite its output. Three test-first
literal unit checks cover independently counted paired resamples, every
primary/descriptive flat index, and math.fsum mean/SE references.

The first audit completed its calculations but failed while serializing a
NumPy boolean in its prediction-inclusion display. Its source `audit.py`
and incomplete `audit.json` remain preserved. The successful v2 changes only
that boolean-to-Python-bool conversion and the fresh destination name. This
was an audit output bug, not a failed scientific run or reason to redraw data.

## Reconstruction checks

The audit binds the complete consumer summary and every reported source,
prediction, native sample and ledger hash. It checks that the native run
used the same prediction frozen before its histories; every declared native
state, mask and horizon count completed without a failed trajectory.

It recomputes all36 raw moment rows from every original snapshot, by
square-before-time-average of u/r. It reconstructs all18 high-minus-low
paired rows by literal flat cell/start/window indices, and all84 descriptive
rows including the48 start/window diagnostics. All rows and labels match
exactly. Every complete replica column remains the sampling unit.

All40 saved bootstrap index chunks match their raw SHA-256 values; the full
recorded before/after state chain, returned flags and10000-resample counts
are continuous and complete. This is a recorded-chain consistency check;
no PRNG advancement is claimed to have been independently replayed.

All10000-by102 bootstrap estimates were reconstructed **exactly** using
independent indexed-addition count matrices, rather than the consumer's
bincount implementation. All102 reported means, replica SEs and pointwise
percentiles match exactly. The18-coordinate simultaneous band and its
max-deviation critical value also match, using only the primary family.
The descriptive84 coordinates do not acquire simultaneous coverage.

Independent math.fsum reductions differ from the stated NumPy reduction
by at most1.3877787807814457e-17 in means and4.336808689942018e-19 in SEs.
These are floating-point consistency checks, not formal arithmetic proofs.

## Results and material diagnostic boundary

All18 primary point estimates, pointwise upper endpoints and planned
simultaneous upper endpoints are below zero. The predeclared zero-start
final-window display is:

| n | High-minus-low moment contrast | Approx. primary simultaneous95% interval | Contrast/delta |
|---|---:|---|---:|
|384|-0.0246630825|[-0.0265867196,-0.0227394454]|-1.10898458|
|448|-0.0136807803|[-0.0148430170,-0.0125185436]|-1.15907218|

Both point estimates lie inside the independently frozen first-response
functional intervals. These intervals exclude the unknown finite-rate
asymptotic remainder and equilibration error. The leading decay contrast is
zero; the observed negative paired effect supports the response mechanism,
without proving a finite-rate stationary formula.

Six of the48 descriptive start/window pointwise intervals exclude zero:
at n448, late-minus-middle second moments are positive for both decay arms,
repeated across the three paired starts. Their values are0.0046894447 for
low decay and0.0035635993 for high decay, with pointwise intervals respectively
[0.0006959486,0.0086857281] and[0.0005350577,0.0066004899] rounded outward.
These are correlated, unadjusted descriptive flags, not six independent
rejections or a primary-family test. They preserve a possible finite-clock
drift concern; a statement that all observation windows agree is unsupported.
No start contrast has such a pointwise flag.

The planned paired contrasts retain the same negative direction in every
window. This audit confirms numerical/provenance consistency and the stated
diagnostics; it does not certify mixing, stationarity, asymptotic remainder,
external novelty or a neural-model benefit.
