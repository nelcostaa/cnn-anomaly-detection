## WQDAB - Water Quality Dataset Anomaly Benchmark

**Multi-year water quality anomaly detection research project** with support for temporal and domain drift analysis. Focuses on the GECCO 2018 industrial challenge dataset plus 2017 and 2019 data for drift studies.

### Datasets

#### Primary Dataset (GECCO 2018)
- Source: `resources_research_geccco_challenge/1_gecco2018_water_quality.csv`
- Copy to `data/raw/` for local experimentation

#### Multi-Year Datasets (2017-2019)
- **2017**: Train/Test splits (baseline year)
- **2018**: Train/Test splits (GECCO challenge year)
- **2019**: Train/Val/Test splits (target year for drift)
- Loaded via `wqdab.data` module (automatic download from cloud)

### Package Structure

```
wqdab/                    # Main Python package (pip installable)
├── data/                 # Dataset loaders
│   ├── load_single_dataset_2017/2018/2019()
│   ├── load_temporal_drift_task()  # 2017→2018
│   └── load_domain_drift_task()    # 2017+2018→2019
├── features/             # Feature engineering
├── models/               # Baseline models (IsolationForest, LOF)
├── utils/                # Preprocessing and metrics
│   ├── preprocess_data()
│   └── compute_metrics() # Time-series aware metrics
├── visualization/        # Plotting utilities
└── metrics.py           # Re-export of metrics module

notebooks/                # Jupyter notebooks
├── 01-03_*.ipynb        # Original GECCO2018 EDA/viz
├── 04a-c_*.ipynb        # Single-year baselines (2017/2018/2019)
└── temporal_drift_*.ipynb # Drift analysis notebooks

tests/                    # Pytest test suite
data/                     # Data directory (gitignored)
reports/figures/          # Generated plots (gitignored)
```

### Installation

#### Standard Installation
```bash
# Clone repository
git clone <repo-url>
cd "IA - Detecção Falhas"

# Install package in editable mode
pip install -e .

# Or install from requirements.txt (includes dev tools)
pip install -r requirements.txt
```

#### Dependencies
Core ML packages: `numpy`, `pandas`, `scikit-learn`, `scipy`, `matplotlib`, `seaborn`, `plotly`

Additional: `tensorflow` (deep models), `imbalanced-learn` (sampling), `optuna` (tuning), `prts` (time-series metrics)

### Quick Start

```python
# Load single-year datasets
from wqdab.data import load_single_dataset_2017, load_single_dataset_2018
df_train_2017, df_test_2017 = load_single_dataset_2017()
df_train_2018, df_test_2018 = load_single_dataset_2018()

# Preprocess data
from wqdab.utils import preprocess_data
X_train, X_orig, y_train, means, stds = preprocess_data(df_train_2017)
X_test, _, y_test, _, _ = preprocess_data(df_test_2017, means=means, stds=stds)

# Evaluate with time-series metrics
from wqdab.metrics import compute_metrics
predictions = model.predict(X_test)  # Your model
compute_metrics(y_test, predictions)
```

### Drift Analysis Tasks

```python
# Temporal drift: 2017 (source) → 2018 (target)
from wqdab.data import load_temporal_drift_task
df_source, df_target_train, df_target_test = load_temporal_drift_task()

# Domain drift: 2017+2018 (source) → 2019 (target)
from wqdab.data import load_domain_drift_task
df_source, df_target_train, df_target_test = load_domain_drift_task()
```

### Running Tests

```bash
pytest tests/ -v
```

### Development Notes
- **Package Name**: `wqdab` (Water Quality Dataset Anomaly Benchmark)
- **Import Convention**: Use `from wqdab.*` throughout (old `src.*` imports have been migrated)
- Keep `data/` directories gitignored to prevent large file commits
- Use `pytest` for testing, `ruff` for linting

