# Same Loss and Gradient Covariance, Different Stationary Errors in Adaptive Optimization

Research code, mathematical proofs and recorded numerical evidence accompanying the manuscript by **Ihor Kendiukhov**.

**Status:** unpublished research manuscript, prepared for the *Journal of Optimization Theory and Applications*. This repository does not claim journal acceptance or external human proof review. Substantial AI assistance is described in the manuscript.

## What the Result Says

Two stochastic quadratic problems can have the same average loss, the same complete separate distributions of Hessians and noise at the minimum, and the same gradient covariance at every pair of parameter values, yet give very different AdamW errors.

Only the pairing of curvature and noise changes. With the same fixed AdamW settings, stationary excess loss decreases in proportion to the learning rate in one problem and stays bounded away from zero in the other. Plain SGD has exactly equal stationary covariance and quadratic risk on the two problems. “Stationary” means the distribution of the parameters and moment estimates is unchanged by further updates; it does not describe a proven burn-in time for a finite run.

The construction has two interacting coordinates, uniformly positive-definite sample Hessians and an extension to smooth sampling densities. An exact curvature-response formula identifies dependence that loss and covariance summaries miss.

The theorem proves the smooth-distribution result. The recorded simulations use the separately specified **atomic** example. They illustrate the mechanism and do not prove the theorem or establish a language-model training benefit.

## Start with the Exact Checks

Python **3.10 or newer** is required. The core package uses only the standard library.

```bash
git clone https://github.com/Biodyn-AI/loss-gradient-covariance.git
cd loss-gradient-covariance
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m loss_gradient_covariance check
```

On Windows, activate the environment with `.venv\Scripts\activate`.

The core checks establish exact identities for the finite example and verify saved certificate bytes. They do not constitute automated verification of the paper's proofs.

The same tools can be used directly in Python:

```python
from loss_gradient_covariance import fixture_law, matching_report, sgd_stationary_covariance

independent = fixture_law("independent")
coupled = fixture_law("coupled")
assert matching_report(independent, coupled)["all_matched"]
assert sgd_stationary_covariance(independent, "0.001") == sgd_stationary_covariance(coupled, "0.001")
```

## Reproduce the Recorded Results

The full frozen scientific record is a release download, keeping large data out of Git. It contains **721 files**, including original code, raw records, analysis receipts, proof notes and earlier discrepancies. The current journal-format paper lives separately in `paper/`. Use Python **3.11 or 3.12** for the pinned numerical environment below; the core's broader Python requirement does not imply compatibility with every pinned numerical dependency.

```bash
python -m pip install -r requirements-reproduce.txt
python -m loss_gradient_covariance download-data --output data/scientific-record-v1.0.0.zip
python -m loss_gradient_covariance verify-data data/scientific-record-v1.0.0.zip
python -m loss_gradient_covariance extract-data data/scientific-record-v1.0.0.zip --output data/workspace
python -m loss_gradient_covariance reproduce-tables --data-root data/workspace --output outputs/tables.json
python scripts/reproduce_figures.py --scientific-root data/workspace --output outputs/figures
```

See [the reproduction guide](docs/reproduction.md) for the archive identity, environment, interpretation and distinction between reanalysis and fresh simulation.

## Read and Build the Paper

The main paper includes the essential proofs in Appendices A–E. Online Resource 1 contains the scalar, matched-speed and memory extensions and supporting numerical studies.

Read the [main manuscript](paper/manuscript.pdf) and [Online Resource 1](paper/ESM_1.pdf), or compile them locally:

```bash
python paper/build.py --output outputs/paper
```

Building requires `pdflatex`, `bibtex` and the LaTeX packages used in `paper/preamble.tex`. The build downloads and verifies the official Springer template when the publisher class files are absent. See the reproduction guide for offline use and license details.

## Evidence and Limits

The prespecified two-dimensional study retained both optimizers, both pairings, three learning rates, three starts and three observation windows. All **27 AdamW coupled-minus-independent contrasts** are positive in the approximate simultaneous band covering the complete 432 primary quantities. These are correlated comparisons, not 27 independent confirmations.

The same analysis flags **4/72 start**, **2/72 window** and **22/72 rate** contrasts. Those diagnostics and the earlier unsuccessful absolute predictions remain in the record. They leave finite-window and finite-rate effects unresolved. Three learning rates do not prove an asymptotic exponent, full-chain mixing or convergence to stationarity.

The mathematical results concern the specified fixed-memory quadratic setting. They provide neither a demonstrated intervention for trained language models nor a generalization benefit. Internal agent reviews are recorded as such; they are not external human peer review or formal proof-assistant verification.

## Repository Layout

| Path | Contents |
|---|---|
| `src/loss_gradient_covariance/` | Exact finite-law tools, certificate loading and a floating-point toy simulator |
| `tests/` | Exact identities, literal update checks and input-validation tests |
| `certificates/` | Preserved deterministic bounds with linked SHA-256 identities |
| `data/release.json` | Versioned archive URL, byte count and digest |
| `provenance/` | Scientific inventory, reference validation and arithmetic audits |
| `paper/` | Current manuscript, supplement, figures and build sources |
| `scripts/` | Reproduction entry points using saved scientific records |
| `examples/` | Fresh finite-horizon toy demonstrations |
| `docs/` | Reproduction instructions |

## Citation and Reuse

Use [CITATION.cff](CITATION.cff) for the repository and unpublished manuscript citation. Cite a specific release or commit when using recorded results. No paper DOI or publication venue is asserted.

Original code is **MIT** licensed. Original manuscript, documentation, figures and synthetic data are **CC BY 4.0** licensed. Third-party materials retain their own terms; see the repository's license notices. Publishing this archive does not turn the internal checks into an independent validation of every scientific claim.

