# Recorded Scientific Data

This directory tracks the release metadata, not the large archive. The frozen scientific record is distributed as a versioned GitHub release asset so that ordinary source checkouts stay small.

## Exact Archive Identity

| Field | Value |
|---|---|
| Version | `1.0.0` |
| Filename | `scientific-record-v1.0.0.zip` |
| Compressed bytes | `253677113` |
| SHA-256 | `ff6c87277d6d25ec43872e366d0d4ca373487bba2295771e18b32447547767ff` |
| Recorded scientific members | `721` |
| Uncompressed scientific bytes | `375077016` |

[Download the versioned asset](https://github.com/Biodyn-AI/loss-gradient-covariance/releases/download/v1.0.0/scientific-record-v1.0.0.zip). The same identity is recorded in [release.json](release.json), and the scientific file inventory is in [the provenance manifest](../provenance/scientific_manifest.json). The archive also contains its embedded `MANIFEST.json`; byte counts above describe the recorded scientific members, excluding manifest/filesystem overhead.

This is the raw scientific record, **not** the journal submission's `ESM_2.zip` wrapper. Different wrappers must not be substituted under this digest.

## Download, Check and Extract

From the repository root after installing the package:

```bash
python -m loss_gradient_covariance download-data --output data/scientific-record-v1.0.0.zip
python -m loss_gradient_covariance verify-data data/scientific-record-v1.0.0.zip
python -m loss_gradient_covariance extract-data data/scientific-record-v1.0.0.zip --output data/workspace
```

Verification checks the outer digest, safe member names, declared sizes and every scientific member's digest. Extraction uses the same verified open archive and requires a new destination, sufficient free space and no overwriting of an existing workspace. An `.incomplete` marker remains if extraction fails; do not analyze that partial workspace. The download/extraction commands do not execute archived research code.

Downloaded ZIPs and `data/workspace/` are ignored by Git. Keep them unchanged; write reanalysis products into a separate output directory. See [the reproduction guide](../docs/reproduction.md) for table/figure commands and numerical dependencies.

## Scope and Provenance

The record preserves source code, observations, uncertainty inputs, receipts, proof notes, validation reports and earlier discrepancies. Historical manifests and receipts describe the state at their original freeze time; an `external_publication: false` field is not a statement that the later GitHub repository is private. A zero-draw packaging or reanalysis record does not imply the original simulations used no randomness.

The current JOTA-format manuscript and presentation changes are separately maintained in `paper/`. Reproducing saved numbers does not independently establish a mathematical proof, confidence coverage, mixing time or benefit in language models.

Original software and original scientific content have different license scopes: see [LICENSE_SCOPE.md](../LICENSE_SCOPE.md) and [third-party notices](../THIRD_PARTY_NOTICES.md). The complete CC BY 4.0 text is in [LICENSES/CC-BY-4.0.txt](../LICENSES/CC-BY-4.0.txt), copied from the [official SPDX license-list-data text](https://raw.githubusercontent.com/spdx/license-list-data/main/text/CC-BY-4.0.txt), with SHA-256 `d557539df68e771cc1eedcc91d13f70fca930e508d11eedcafa4b15db49e3744`.

