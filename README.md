# AutoSAXS SAXS Descriptor and ML Workflow

Curated public release package for the SAXS descriptor-extraction and machine-learning workflow used to analyse lysozyme/EAN crystallization behaviour.

This package is intentionally selective. It contains the processed descriptor tables, representative SAXS profiles, executable analysis code, model-evaluation outputs, and source data for the ML phase maps. It does not include the full local working directory, manuscript drafts, reviewer correspondence, PowerPoint files, or unrelated exploratory files.

## Contents

- `data/`: curated descriptor and target tables. The primary table is `curated_descriptor_dataset_n96.csv`.
- `selected_for_ML/`: representative SAXS `.dat` profiles used for the descriptor and ML workflow.
- `src/saxs_crystal/physics/`: Bragg-peak detection, crystallinity-index, Guinier, and OLIGOMER command helpers.
- `src/` and `scripts/`: data cleaning, model training/evaluation, heatmap generation, and publication-plot scripts.
- `configs/`: default analysis and ML configuration files.
- `outputs/model_evaluation/`: model metrics and representative evaluation plots.
- `outputs/heatmap_source_data/`: source CSV files for CI/Rg phase-map and transition-region outputs.
- `outputs/publication_metrics/`: model-performance summary CSV files.
- `oligomer_basis/`: PDB/form-factor basis files used for the representative OLIGOMER workflow.
- `example_oligomer_outputs/`: small example output set from the OLIGOMER fitting workflow.
- `legacy_reference_scripts/`: non-executable text copies of selected legacy step scripts retained for provenance only. These are not the recommended runnable code path.

## Primary Dataset

The primary curated descriptor table is:

`data/curated_descriptor_dataset_n96.csv`

It contains 96 curated samples after filtering/cleaning from the larger descriptor tables. Supporting source/provenance tables are provided as:

- `data/source_descriptor_table_v3_n99.csv`
- `data/source_descriptor_table_v2_n100.csv`
- `data/curated_descriptor_dataset_rg_n99.csv`
- `data/curated_descriptor_dataset_ci_n96.csv`

## Reproducibility Notes

The formal reusable implementation is in `src/` and `scripts/`. The Bragg and crystallinity-index logic is in `src/saxs_crystal/physics/bragg.py` and `src/saxs_crystal/physics/crystallinity.py`; the OLIGOMER command wrapper is in `src/saxs_crystal/physics/oligomer.py`.

ATSAS is required only for workflows that call FFMAKER/OLIGOMER. Install ATSAS separately and set the `ATSAS_BIN` environment variable if needed.

## Suggested Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

## Citation

Please cite the associated manuscript and the archived release DOI once available. Citation metadata are provided in `CITATION.cff`.

## License

See `LICENSE` and `NOTICE.md`. The package is shared for peer-review, reproducibility, and non-commercial academic research use with attribution.
