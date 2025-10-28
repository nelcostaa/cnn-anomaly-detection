"""
Water Quality Dataset Anomaly Benchmark (WQDAB)
================================================

A Python package for water quality anomaly detection research,
focused on multi-year datasets and temporal/domain drift analysis.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="wqdab",
    version="0.1.0",
    author="Research Team",
    description="Water Quality Dataset Anomaly Benchmark - Multi-year anomaly detection research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["wqdab", "wqdab.*"]),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24",
        "pandas>=2.2",
        "scikit-learn>=1.4",
        "scipy>=1.13",
        "matplotlib>=3.8",
        "seaborn>=0.13",
        "jupyterlab>=4.2",
        "ipywidgets>=8.1",
        "pyyaml>=6.0",
        "plotly>=5.24",
        "prts>=0.2.0",  # Time-series precision/recall metrics
        "imbalanced-learn>=0.12",  # imblearn for RUSBoost
        "optuna>=3.0",  # Hyperparameter optimization
        "tensorflow>=2.15",  # Deep learning models
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "ruff>=0.6",
            "black>=24.8",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

