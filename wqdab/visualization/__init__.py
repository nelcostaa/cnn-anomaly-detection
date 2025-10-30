"""
Visualization utilities for WQDAB.

This module provides plotting functions for exploratory data analysis,
anomaly visualization, and multi-year comparisons.
"""

from .anomaly_plots import (
    get_anomaly_windows,
    plot_anomaly_zoom,
    plot_all_anomaly_windows,
)
from .plots import plot_pairwise_histograms

__all__ = [
    "get_anomaly_windows",
    "plot_anomaly_zoom",
    "plot_all_anomaly_windows",
    "plot_pairwise_histograms",
]

