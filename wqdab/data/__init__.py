"""
Data loading utilities for WQDAB (Water Quality Dataset Anomaly Benchmark).

This module provides functions to load single-year datasets (2017-2019)
and combined datasets for temporal/domain drift tasks.
"""

from .data import (
    load_single_dataset_2017,
    load_single_dataset_2018,
    load_single_dataset_2019,
    load_temporal_drift_task,
    load_domain_drift_task,
    load_all_datasets,
)

__all__ = [
    "load_single_dataset_2017",
    "load_single_dataset_2018",
    "load_single_dataset_2019",
    "load_temporal_drift_task",
    "load_domain_drift_task",
    "load_all_datasets",
]

