from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


def impute_and_scale(df: pd.DataFrame) -> Tuple[pd.DataFrame, StandardScaler]:
    numeric_df = df.select_dtypes(include=[np.number])
    imputer = SimpleImputer(strategy="median")
    imputed = imputer.fit_transform(numeric_df)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(imputed)
    scaled_df = pd.DataFrame(scaled, columns=numeric_df.columns, index=df.index)
    return scaled_df, scaler


