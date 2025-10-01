## IA - Detecção de Falhas (GECCO2018 Water Quality)

Anomaly detection research project focused on the GECCO 2018 industrial challenge (water quality dataset). This repository is data-science oriented: understand the problem, explore the data, and develop baselines and deep models. No MLOps stack.

### Dataset
- Primary dataset: `resources_research_geccco_challenge/1_gecco2018_water_quality.csv`
- We are not participating in the original competition; ignore competition rules.
- Copy the CSV into `data/raw/` for local experimentation (not tracked by Git).

### Structure
```
data/
  raw/          # original data (ignored)
  external/     # external sources (ignored)
  interim/      # intermediate artifacts (ignored)
  processed/    # model-ready outputs (ignored)
notebooks/      # EDA and experiments in notebooks
src/
  data/         # loading and I/O utils
  features/     # preprocessing and feature engineering
  models/       # baselines and model definitions
  visualization/# plotting utilities
  utils/        # shared utilities
reports/
  figures/      # generated plots (ignored)
experiments/    # experiment configs, logs
configs/        # YAML/JSON configs for experiments
scripts/        # CLI scripts for common tasks
```

### Getting Started
1. Create a virtual environment (optional):
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place dataset:
   ```bash
   cp resources_research_geccco_challenge/1_gecco2018_water_quality.csv data/raw/
   ```
4. Open the starter EDA notebook in `notebooks/`.

### Notes
- Keep `data/` directories ignored to prevent large files in Git.
- Prefer reproducible notebooks and scripts with fixed seeds when relevant.

