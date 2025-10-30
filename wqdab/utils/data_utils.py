"""
Data preparation utilities for anomaly visualization.

This module provides helper functions to prepare time-series dataframes
for visualization across multiple years and datasets.
"""

from __future__ import annotations

from typing import Literal

import pandas as pd


def prepare_time_series(
    df: pd.DataFrame,
    time_col: str = 'Time',
    event_col: str = 'EVENT',
    numeric_cols: list[str] | None = None
) -> pd.DataFrame:
    """
    Prepare a dataframe for time-series anomaly visualization.
    
    Performs standard cleaning operations:
    - Parse time column
    - Ensure EVENT column is boolean
    - Coerce numeric columns
    - Drop rows with missing time or sensor data
    - Set datetime index
    - Sort by time
    
    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe with time, sensor, and event columns
    time_col : str
        Name of the time column (default: 'Time')
    event_col : str
        Name of the event/anomaly column (default: 'EVENT')
    numeric_cols : list[str], optional
        List of numeric sensor columns. If None, inferred from data
        
    Returns
    -------
    pd.DataFrame
        Cleaned dataframe with datetime index
        
    Examples
    --------
    >>> df_ts = prepare_time_series(df)
    >>> df_ts.head()
    """
    df = df.copy()
    
    # Parse time column
    if time_col in df.columns:
        df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
    
    # Infer numeric columns if not provided
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        # Remove event column if present
        if event_col in numeric_cols:
            numeric_cols.remove(event_col)
    
    # Coerce numeric columns
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Ensure EVENT is boolean
    if event_col in df.columns:
        if df[event_col].dtype != bool:
            df[event_col] = df[event_col].astype(str).str.lower().isin(
                ["true", "1", "t", "yes", "yes"]
            )
    
    # Drop rows with nulls in time or numeric sensors
    subset_cols = [time_col] + numeric_cols
    df_clean = df.dropna(subset=subset_cols)
    
    # Sort by time and set index
    df_clean = df_clean.sort_values(time_col).reset_index(drop=True)
    df_ts = df_clean.set_index(time_col).sort_index()
    
    return df_ts


def get_standard_sensors(df: pd.DataFrame) -> list[str]:
    """
    Get the standard sensor column names for water quality data.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to extract sensor names from
        
    Returns
    -------
    list[str]
        List of standard sensor column names
        
    Examples
    --------
    >>> sensors = get_standard_sensors(df)
    >>> sensors
    ['Tp', 'Cl', 'pH', 'Redox', 'Leit', 'Trueb', 'Cl_2', 'Fm', 'Fm_2']
    """
    standard_sensors = ['Tp', 'Cl', 'pH', 'Redox', 'Leit', 'Trueb', 'Cl_2', 'Fm', 'Fm_2']
    
    # Return only sensors that exist in the dataframe
    return [s for s in standard_sensors if s in df.columns]


def load_and_prepare_dataset(
    load_func: callable,
    year: int | str,
    **kwargs
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame | None]:
    """
    Load and prepare dataset for visualization.
    
    Loads a dataset using the provided function and prepares both train and test sets.
    
    Parameters
    ----------
    load_func : callable
        Function that loads the dataset (returns train, test or train, val, test)
    year : int or str
        Year identifier for the dataset (for display purposes)
    **kwargs
        Additional arguments to pass to prepare_time_series()
        
    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame | None]
        Prepared train and test dataframes, and optionally validation dataframe
    """
    print(f"📥 Loading dataset for year {year}...")
    
    # Load dataset
    if hasattr(load_func, '__call__'):
        data = load_func()
    else:
        data = load_func
    
    # Handle different return formats
    if len(data) == 2:
        train_df, test_df = data
        val_df = None
    elif len(data) == 3:
        train_df, val_df, test_df = data
    else:
        raise ValueError(f"Unexpected number of datasets returned: {len(data)}")
    
    print(f"  Train: {train_df.shape}, Test: {test_df.shape}")
    if val_df is not None:
        print(f"  Val: {val_df.shape}")
    
    # Prepare data
    df_train_ts = prepare_time_series(train_df, **kwargs)
    df_test_ts = prepare_time_series(test_df, **kwargs)
    
    if val_df is not None:
        df_val_ts = prepare_time_series(val_df, **kwargs)
        return df_train_ts, df_test_ts, df_val_ts
    
    return df_train_ts, df_test_ts, None

