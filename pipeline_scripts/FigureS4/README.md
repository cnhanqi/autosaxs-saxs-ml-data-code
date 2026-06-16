# FigureS4 Code Index

This folder contains the dataset-specific code for rebuilding the crystalline peak mosaics from:

- `data/processed/intermediate/6/analysis/selected/analysis/crystalline_present_true/crystalline_present_true_mosaic_annot.png`
- `data/processed/intermediate/6/analysis/selected/analysis/crystalline_present_true/crystalline_present_true_mosaic_simple.png`

Original source in main pipeline:

- `pipelines/step2_crystal_features.py`
  - `build_crystalline_mosaics(...)`
  - `_build_mosaic_from_data(...)`

Figure S4 dedicated script:

- `figure_s4_crystalline_mosaic_highres.py`
  - fixed 5 columns per row
  - rows auto-expand to fit all crystalline samples
  - high-resolution output
  - clearer text and larger annotations
  - outputs new high-resolution annotated and simple mosaic figures
