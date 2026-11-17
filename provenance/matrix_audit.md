# Independent arithmetic audit of the complete 2D matrix study

17 November 2026. Internal empirics-referee audit after the separately
authorized native946201 and uncertainty946202 stages completed. All543
named checks passed. This audit used ONLY recorded states, rows, indices,
coefficients and receipts. No PRNG constructor, replay, scientific draw,
trajectory, parameter fit or change to a scientific source/result occurred.

## Artifacts and reproducibility

| Artifact | SHA-256 |
|---|---|
| Complete analyzed summary | `93bfb6d29724b8a73bae260eb1627258313f14c744bce7897a2aee4843e33148` |
| Independent audit source | `a86b4e184b8b06ae58a73287d4a8af70c758131f95d2255c83e6387311637c80` |
| Independent full audit JSON | `cf69141afc24c9d651ca5e60d6507fb2f93ff4c52b066c10b1e2b59f386c6b90` |

The analysis summary is
`results/q2_matrix_analysis_20261117/run/summary.json`. The source and full
audit JSON are under the UNIQUE directory
`results/q2_matrix_empirics_independent_audit_20261117/`. The audit source
requires an explicit absolute consumer path and expected SHA, refuses an
existing output, and checks a literal count-based resampling example before
reading the scientific inputs. It imports no scientific producer/consumer.

## What was independently verified

- The consumer's complete native input artifacts and its own source hashes
  match their immutable receipts; every observed vector state/counter is present.
- All10000×648 saved primary/coordinate bootstrap estimates are reproduced
  **exactly**, with maximum absolute discrepancy zero. An independently
  built add-at frequency matrix applies the recorded shared replica indices.
- All10000×27 saved AdamW ratio estimates are reconstructed exactly, as are
  every27 reported point ratio and percentile interval.
- All432 primary point estimates, replica SEs, pointwise percentile95%
  intervals, the max-deviation critical value and simultaneous intervals
  are reproduced exactly. Each primary row is separately reconstructed
  from its declared risk/paired/control/start/window/rate meaning.
- All216 coordinate rows, means, SEs and descriptive percentile intervals
  are reproduced exactly from the original vector snapshots.
- An independent full-matrix contraction(u^T Hbar u)/2 checks the risk
  cross term and coordinate axes. Its maximum discrepancy from the
  producer's expanded expression is1.3877787807814457e-16, consistent with
  ordinary floating-point reduction differences.
- The three exact rational nominal SGD covariances satisfy every entry of
  the stationary Lyapunov equation with ZERO residual. Their risks and
  neighboring-float enclosures agree with those exact covariances.
- Exact enumeration of both atomic oracle laws confirms identical complete
  Hessian and vector-noise marginals, Hbar=[[2,1.25],[1.25,2]], noise
  covariance I/2, and zero for every mixed E[H_ij e_k]. Both sample Hessians
  are positive definite and their commutator has offdiagonal entry-5.
- All40 saved uncertainty index-chunk SHA values and recorded full-state
  transitions match. The native three-role packed352-byte ledger also has
  continuous recorded state chains, complete physical prefixes and counts.
  This checks recorded-chain consistency, NOT independently advanced PRNG
  states; replay was deliberately excluded.

## Results, including the finite-window limitations

The fixed zero-start final-window display is:

| eta | Independent AdamW risk | Coupled AdamW risk | Coupled/independent ratio |
|---:|---:|---:|---:|
| .001 | .0001169172 | .2079983 |1779.02|
| .0002 | .00002082282 | .21146665 |10155.53|
| .00004 | .000003975007 | .21209878 |53358.09|

All27 AdamW coupled-minus-independent contrasts have strictly positive
lower endpoints in the complete approximate432-family simultaneous band.
None of the54 SGD-minus-exact controls excludes zero in that band.
These are correlated features of256 shared histories, not27 independent
confirmations. Bootstrap coverage remains approximate.

The complete family also flags **4/72 start contrasts,2/72 window contrasts
and22/72 rate contrasts** as excluding zero. Every flag label and interval
is retained in the full audit JSON. These finite start/window/rate effects
must not be described as universal empirical stationarity or exact scaling.
In particular, risk agreement cannot rule out different occupancy of
symmetry-related wells; coordinate means are descriptive diagnostics of
that issue and do not certify full-chain mixing.

The large observed separation is compatible with the separately proved
fixed-memory stability switch and stationary risk-order theorem. Three
finite step sizes, however, do not themselves prove an asymptotic exponent
or a finite mixing time. The empirically tested law is the explicit atomic
fixture; the smooth-joint-law theorem is a separate mathematical extension
and has no claimed numerical smoothing threshold in this experiment.
