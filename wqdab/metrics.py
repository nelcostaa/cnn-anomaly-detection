"""
Metrics module for WQDAB.

This module re-exports metrics functions from wqdab.utils.metrics
for convenient notebook imports (from wqdab.metrics import ...).
"""

from .utils.metrics import compute_metrics

__all__ = ["compute_metrics"]

