# ML Protocol Summary

This note records the compact machine-learning settings retained in the curated minimal public package.

## Primary data table

- `data/curated_descriptor_dataset_n96.csv`

## Random seed and split logic

- Default configuration file: `configs/ml.default.yaml`
- Default `random_state`: `42`
- Default cross-validation folds in the config: `5`
- The original public analysis script used repeated random hold-out evaluation with:
  - `80/20` train/test split
  - `5` random seeds
  - seed values `0` to `4`
  - `5`-fold cross-validation on the training split

## Metrics retained in this package

- Regression:
  - `R2`
  - `RMSE`
- Classification:
  - `ROC-AUC`
  - `F1`
  - `accuracy`

## Metrics files

- `outputs/model_evaluation/CI_classification/metrics.csv`
- `outputs/model_evaluation/CI_regression/metrics.csv`
- `outputs/model_evaluation/Rg_regression/metrics.csv`
- `outputs/publication_metrics/model_performance_summary.csv`
- `outputs/publication_metrics/ci_metrics.csv`
- `outputs/publication_metrics/ci_reg_metrics.csv`
- `outputs/publication_metrics/rg_metrics.csv`

## Scope note

This repository version does not include the full training or plotting pipeline. It retains the evaluation settings and summary metrics needed to document the reported workflow without exposing the complete local automation stack.
