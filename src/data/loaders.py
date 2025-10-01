from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

from src.utils.paths import RAW_DATA_DIR


def load_gecco2018_csv(path: Optional[Path] = None) -> pd.DataFrame:
    csv_path = Path(path) if path is not None else RAW_DATA_DIR / "1_gecco2018_water_quality.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"GECCO2018 CSV not found at {csv_path}. Copy it into data/raw/")
    df = pd.read_csv(csv_path)
    return df


