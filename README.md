# AutoSAXS Curated Minimal Public Release

This repository contains a reduced public package for the SAXS descriptor-extraction and machine-learning workflow used to analyse lysozyme/EAN crystallization behaviour.

The release is intentionally minimal. It contains the curated descriptor table, a small representative subset of SAXS profiles, lightweight Bragg/CI/OLIGOMER helper code, model-metrics tables, and protocol notes needed for summary-level reproducibility review. It does not contain full raw working directories, figure-generation code, large OLIGOMER basis files, bulk figure outputs, legacy scripts, or one-command end-to-end reproduction pipelines.

## Included Content

- `data/curated_descriptor_dataset_n96.csv`
  The primary curated descriptor dataset used for the manuscript analyses.
- `selected_for_ML/`
  Ten representative SAXS `.dat` profiles spanning buffer and EAN conditions.
- `src/saxs_crystal/io/read_dat.py`
  Minimal SAXS `.dat` reader helper.
- `src/saxs_crystal/physics/bragg.py`
  Lightweight Bragg-peak summary helper.
- `src/saxs_crystal/physics/crystallinity.py`
  Lightweight crystallinity-index helper.
- `src/saxs_crystal/physics/oligomer.py`
  Deterministic OLIGOMER command-wrapper helper without bundled ATSAS assets.
- `outputs/model_evaluation/*/metrics.csv`
  Task-level ML evaluation metrics.
- `outputs/publication_metrics/*.csv`
  Summary manuscript-facing performance tables.
- `configs/ml.default.yaml`
  Compact ML settings summary.
- `ML_PROTOCOL.md`
  Train/test split, random-seed, cross-validation, and metrics description.
- `REPRESENTATIVE_SAXS_PROFILES.md`
  List of the retained SAXS profiles.
- `hyperparameter_tuning_description.md`
  Hyperparameter-grid description.
- `CITATION.cff`, `.zenodo.json`, `LICENSE`, `NOTICE.md`
  Citation, DOI metadata, and reuse terms.

## Not Included

- figure-generation scripts or plotting modules
- bulk PNG outputs and heatmap-rendering assets
- full raw SAXS working directories
- complete legacy scripts
- OLIGOMER basis PDB/form-factor files
- complete OLIGOMER example-output bundles
- one-click full reproduction pipelines
- Word, PowerPoint, Origin, Illustrator, and response-document files

## Representative Profiles

The retained SAXS profiles are:

- `Buf_2.5mg.dat`
- `Buf_50mg.dat`
- `Buf_100mg.dat`
- `EAN1.5_50mg.dat`
- `EAN5.7_5mg.dat`
- `EAN12_50mg.dat`
- `EAN30_75mg.dat`
- `EAN54.6_25mgb.dat`
- `EAN75_2.5mg.dat`
- `EAN99_70mg.dat`

## Reproducibility Scope

This curated minimal package is intended for method inspection and summary-level result checking. It is not a full rerun package for regenerating every intermediate table or figure from the original local workflow.

ATSAS/OLIGOMER is third-party software and is not redistributed in this repository.

## Citation

Citation metadata are provided in `CITATION.cff`. The currently archived Zenodo DOI associated with this repository is `https://doi.org/10.5281/zenodo.20716687`.
