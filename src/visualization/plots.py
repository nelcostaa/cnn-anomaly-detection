from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def plot_pairwise_histograms(df: pd.DataFrame, max_cols: int = 10) -> None:
    cols = df.select_dtypes(include="number").columns[:max_cols]
    df[cols].hist(bins=30, figsize=(14, 10))
    plt.tight_layout()
    plt.show()


