# Reproduction Guide

This guide separates **exact finite-example checks**, **reanalysis of recorded evidence**, **paper compilation** and **fresh toy simulation**. Reanalysis should use the preserved observations and analysis inputs. Fresh output is a new experiment and should be identified separately from the preserved record.

## 1. Environment

The core supports Python **3.10 or newer**. For the pinned numerical reproduction stack, use Python **3.10–3.12**, preferably **3.11 or 3.12**: NumPy 1.26.4 supports Python 3.9–3.12 ([official release notes](https://numpy.org/doc/stable/release/1.26.4-notes.html)). Use a virtual environment with the intended interpreter:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Windows activation: `.venv\Scripts\activate`.

The core package has no third-party runtime dependencies. Table/figure reproduction uses `requirements-reproduce.txt`, which pins:

| Package | Version |
|---|---:|
| NumPy | 1.26.4 |
| Matplotlib | 3.10.8 |
| SciPy | 1.15.2 |

```bash
python -m pip install -r requirements-reproduce.txt
```

The archive occupies 253,677,113 bytes compressed and 375,077,016 bytes before filesystem overhead when extracted. Allow additional space for the environment, generated outputs and paper build. Document the Python version, operating system and dependency versions for any reproduction report.

## 2. Exact Checks Without the Large Archive

```bash
python -m loss_gradient_covariance check
python -m unittest discover -s tests -v
```

The public core provides:

| Function | Scope |
|---|---|
| `fixture_law` | Exact independent eight-atom or coupled four-atom law |
| `gradient_moments` | Exact means and same-sample cross covariance at two parameter values |
| `matching_report` | Complete marginal and all-parameter mean/covariance matching |
| `sgd_stationary_covariance` | Exact stationary covariance and excess quadratic risk under checked contraction assumptions |
| `load_fixture_certificate` | Byte verification of the saved fixture certificate and optional kernel link |
| `simulate` | Floating-point finite-horizon updates driven by a supplied atom-index tape |

Exact interfaces accept integers, `fractions.Fraction` values and strings; they reject floating-point arguments. Use `"0.1"` for the exact decimal rational or `Fraction.from_float(0.1)` for the exact binary64 value, according to the quantity intended.

The stored kernel certificate uses its documented binary64 dyadic constants. Its enclosure must not silently be relabeled as a certificate for nearby exact decimal constants. The exact SGD helper's nominal rational controls are also distinct from floating-point simulation identities.

The all-parameter matching check is an algebraic identity: each covariance entry is affine in each of its two parameter arguments, so a complete affine-basis grid determines its coefficients. It is not a random parameter search. A saved certificate's checksum verifies identity with the recorded artifact; reading it alone does not recompute its proof or numerical enclosure.

## 3. Download and Verify the Frozen Scientific Record

```bash
python -m loss_gradient_covariance download-data --output data/scientific-record-v1.0.0.zip
python -m loss_gradient_covariance verify-data data/scientific-record-v1.0.0.zip
```

The versioned asset is:

`https://github.com/Biodyn-AI/loss-gradient-covariance/releases/download/v1.0.0/scientific-record-v1.0.0.zip`

| Field | Expected value |
|---|---|
| Bytes | `253677113` |
| SHA-256 | `ff6c87277d6d25ec43872e366d0d4ca373487bba2295771e18b32447547767ff` |
| Files | `721` |
| Uncompressed bytes | `375077016` |

These values are also recorded in `data/release.json`; file identities are recorded in `provenance/scientific_manifest.json`. This is the **raw scientific archive**, not the differently packaged journal `ESM_2.zip` wrapper. Do not substitute one archive for the other under the same checksum.

Verify the archive before extraction or execution. If the size or digest differs, stop and resolve the mismatch instead of weakening the check. For a source-only checkout without network access, transfer an exact copy of the asset and run the same verification command.

## 4. Extract and Reproduce Tables

```bash
python -m loss_gradient_covariance extract-data data/scientific-record-v1.0.0.zip --output data/workspace
python -m loss_gradient_covariance reproduce-tables --data-root data/workspace --output outputs/tables.json
```

The data root is the extracted scientific workspace containing `experiments/`, `research/` and `results/`. Keep the extracted record unchanged and write new products under `outputs/`. The archive preserves its earlier paths so that recorded source/receipt references remain interpretable.

Some historical scripts and receipts contain machine-specific paths. Use the public entry points documented here for portable reanalysis; the historical sources are preserved as provenance, rather than advertised as turnkey runners.

The table command is the public entry point for the recorded numerical summaries. Inspect its output together with the preserved raw results, receipts and audit reports. Reproducing a summary or saved resampling calculation does not establish exact confidence coverage, equilibration or a mathematical limit theorem.

## 5. Reproduce Figures

```bash
python scripts/reproduce_figures.py --scientific-root data/workspace --output outputs/figures
```

The displays come from saved numerical results or deterministic certified calculations. They must retain the difference between empirical intervals and independent theoretical/oracle enclosures, along with the stated finite-rate limitations. Cosmetic differences across rendering libraries or fonts do not justify changing scientific values. Compare underlying numbers and caption meaning as well as image appearance.

The current JOTA-format paper includes later typography and layout work in `paper/`; that presentation is separate from the unchanged historical scientific archive.

## 6. Build the Manuscript and Supplement

Install a TeX distribution providing `pdflatex`, `bibtex` and the packages listed in `paper/preamble.tex`, then run:

```bash
python paper/build.py --output outputs/paper
```

The build resolves cross-references between the main manuscript and `ESM_1` and applies the recorded bibliography ordering. Expected outputs are `outputs/paper/manuscript.pdf` and `outputs/paper/ESM_1.pdf`.

The Springer class files are third-party materials and are not covered by this project's MIT/CC BY license. The build downloads the official template and verifies its pinned size and SHA-256 before copying only its two class files. Already verified local files are reused. For offline use, transfer the exact `svjour3.cls` and `svglov3.clo` files from that template into `paper/`; the build checks their hashes. The official template source is:

`https://media.springer.com/full/springer-instructions-for-authors-assets/zip/1705114_LaTeX%20JOTA.zip`

Use the current posted journal instructions where its old example conflicts with them. The repository preserves the documented local bibliography-style patch; it must not be mistaken for an unmodified publisher file.

Compilation runs no experiment. Successful compilation and resolved references do not independently validate a proof.

## 7. Fresh Toy Simulations

The public `simulate` function and `examples/` are for new finite-horizon demonstrations. The core requires centered noise and positive-definite sample Hessians so its reported risk is excess average quadratic loss. It applies the stated AdamW update without initial bias correction and with the denominator offset outside the square root.

```bash
python examples/simulate.py --steps 5000 --seed 7 --output outputs/fresh_demo.json
```

The core consumes a caller-supplied atom-index tape and creates no random generator. If generating a tape, record the generator, seed, law, parameter settings, start, horizon and output location. A supplied tape is not automatically an independent sample from its law.

Fresh trajectories are not replacements for the frozen study and are not certified stationary samples. Keep them outside the preserved archive and label them as new output.

## 8. Interpret a Reproduction Honestly

The matrix study has 27 positive AdamW pairing contrasts in the approximate simultaneous band for 432 primary quantities. It also retains 4/72 start, 2/72 window and 22/72 rate flags. These comparisons share histories; their counts are not independent replications.

The smooth-law stationary theorem is separate from the atomic simulations. Neither matching the plotted curves nor passing the software tests proves a mixing time, a scaling exponent from three learning rates, or a benefit in trained language models. The archive retains earlier unsuccessful predictions and diagnostic limitations. Human responsibility for assessing the mathematics and evidence remains; internal AI-assisted checks are not external human peer review.

