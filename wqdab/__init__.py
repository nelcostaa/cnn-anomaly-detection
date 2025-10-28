"""
WQDAB - Water Quality Dataset Anomaly Benchmark
================================================

A Python package for water quality anomaly detection research,
focused on multi-year datasets and temporal/domain drift analysis.

Main Modules:
-------------
- data: Dataset loading functions for 2017-2019 water quality data
- utils: Preprocessing and evaluation utilities
- features: Feature engineering tools
- models: Baseline and deep learning models
- visualization: Plotting utilities
"""

__version__ = "0.1.0"

# Expose key functions at package level for convenience
from .data import (
    load_single_dataset_2017,
    load_single_dataset_2018,
    load_single_dataset_2019,
    load_temporal_drift_task,
    load_domain_drift_task,
    load_all_datasets,
)

from .utils import (
    preprocess_data,
    compute_metrics,
)

__all__ = [
    # Data loading
    "load_single_dataset_2017",
    "load_single_dataset_2018",
    "load_single_dataset_2019",
    "load_temporal_drift_task",
    "load_domain_drift_task",
    "load_all_datasets",
    # Utils
    "preprocess_data",
    "compute_metrics",
]

