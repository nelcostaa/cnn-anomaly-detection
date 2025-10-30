"""
Anomaly visualization functions for time-series datasets.

This module provides functions to extract anomaly windows and create
visualizations for anomaly detection analysis across multiple sensors and years.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd


def get_anomaly_windows(
    df_ts: pd.DataFrame, 
    event_col: str = 'EVENT', 
    margin_minutes: int = 60
) -> list[tuple[pd.Timestamp, pd.Timestamp, pd.Timestamp, pd.Timestamp]]:
    """
    Extract time windows around anomalies with margin.
    
    This function identifies contiguous anomaly regions and creates windows
    around them with configurable margin for context visualization.
    
    Parameters
    ----------
    df_ts : pd.DataFrame
        DataFrame with datetime index and boolean event column
    event_col : str
        Name of the boolean event/anomaly column
    margin_minutes : int
        Minutes to add as margin around each anomaly region
        
    Returns
    -------
    list[tuple]
        List of (start_time, end_time, anomaly_start, anomaly_end) tuples
        representing the windows with anomaly start/end markers
        
    Examples
    --------
    >>> windows = get_anomaly_windows(df_ts, margin_minutes=120)
    >>> len(windows)
    25
    >>> start, end, anom_start, anom_end = windows[0]
    """
    # Find contiguous anomaly regions
    events = df_ts[event_col].copy()
    
    # Identify transitions (False -> True and True -> False)
    event_starts = events & ~events.shift(1, fill_value=False)
    event_ends = events & ~events.shift(-1, fill_value=False)
    
    start_times = df_ts.index[event_starts].tolist()
    end_times = df_ts.index[event_ends].tolist()
    
    if len(start_times) == 0:
        return []
    
    windows = []
    margin = pd.Timedelta(minutes=margin_minutes)
    
    for anom_start, anom_end in zip(start_times, end_times):
        # Add margin around anomaly
        win_start = max(df_ts.index.min(), anom_start - margin)
        win_end = min(df_ts.index.max(), anom_end + margin)
        windows.append((win_start, win_end, anom_start, anom_end))
    
    return windows


def plot_anomaly_zoom(
    df_ts: pd.DataFrame,
    start_time: pd.Timestamp | str,
    end_time: pd.Timestamp | str,
    sensors: list[str] | None = None,
    figsize: tuple[int, int] = (14, 4),
    save_path: Path | str | None = None,
    show: bool = True
) -> None:
    """
    Visualize a specific time window with anomaly highlighting.
    
    Creates a multi-sensor time-series plot with anomaly regions highlighted.
    Each sensor gets its own subplot, with anomalies marked in red.
    
    Parameters
    ----------
    df_ts : pd.DataFrame
        DataFrame with datetime index and sensor columns
    start_time : pd.Timestamp or str
        Start of the time window
    end_time : pd.Timestamp or str
        End of the time window
    sensors : list[str], optional
        List of sensor columns to plot (defaults to all numeric columns)
    figsize : tuple[int, int]
        Figure size (width, height) in inches
    save_path : Path or str, optional
        If provided, saves the figure to this path
    show : bool
        Whether to display the figure (default: True)
        
    Examples
    --------
    >>> windows = get_anomaly_windows(df_ts, margin_minutes=120)
    >>> plot_anomaly_zoom(df_ts, windows[0][0], windows[0][1], 
    ...                   sensors=['Tp', 'pH', 'Cl'])
    """
    # Convert strings to datetime if necessary
    if isinstance(start_time, str):
        start_time = pd.to_datetime(start_time)
    if isinstance(end_time, str):
        end_time = pd.to_datetime(end_time)
    
    # Filter data for the time window
    mask = (df_ts.index >= start_time) & (df_ts.index <= end_time)
    df_window = df_ts.loc[mask]
    
    if len(df_window) == 0:
        print(f"⚠️ Nenhum dado encontrado entre {start_time} e {end_time}")
        return
    
    # Default to all numeric columns if no sensors specified
    if sensors is None:
        sensors = df_window.select_dtypes(include=['number']).columns.tolist()
        # Remove EVENT column if present
        if 'EVENT' in sensors:
            sensors.remove('EVENT')
    
    # Create figure and subplots
    n_sensors = len(sensors)
    fig, axes = plt.subplots(n_sensors, 1, figsize=figsize, sharex=True)
    
    # Handle single sensor case
    if n_sensors == 1:
        axes = [axes]
    
    # Plot each sensor
    for i, sensor in enumerate(sensors):
        ax = axes[i]
        
        # Plot sensor data
        ax.plot(df_window.index, df_window[sensor], 
                color='steelblue', linewidth=1.5, label='Leitura')
        
        # Highlight anomalies if EVENT column exists
        if 'EVENT' in df_window.columns:
            anomaly_mask = df_window['EVENT']
            
            if anomaly_mask.any():
                # Mark anomalous points
                ax.scatter(df_window.index[anomaly_mask], 
                          df_window.loc[anomaly_mask, sensor],
                          color='crimson', s=30, marker='o', 
                          alpha=0.8, label='Anomalia', zorder=5)
                
                # Shade anomaly regions
                ymin, ymax = ax.get_ylim()
                anomaly_times = df_window.index[anomaly_mask]
                for anom_time in anomaly_times:
                    ax.axvspan(anom_time, anom_time + pd.Timedelta(minutes=1), 
                              color='crimson', alpha=0.15, zorder=1)
        
        # Configure labels and style
        ax.set_ylabel(sensor, fontsize=12, fontweight='bold')
        ax.grid(alpha=0.3, linestyle='--', linewidth=0.5)
        ax.legend(loc='upper right', fontsize=9)
    
    # Set global title and x-axis label
    axes[0].set_title(f'Janela: {start_time.strftime("%Y-%m-%d %H:%M")} até '
                     f'{end_time.strftime("%Y-%m-%d %H:%M")}', 
                     fontsize=13, fontweight='bold', pad=10)
    
    axes[-1].set_xlabel('Tempo', fontsize=11)
    plt.setp(axes[-1].xaxis.get_majorticklabels(), rotation=30, ha='right')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figure if path provided
    if save_path:
        if isinstance(save_path, str):
            save_path = Path(save_path)
        # Ensure parent directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✅ Figura salva: {save_path}")
    
    # Show or close
    if show:
        plt.show()
    else:
        plt.close(fig)


def plot_all_anomaly_windows(
    df_ts: pd.DataFrame,
    anomaly_windows: list[tuple[pd.Timestamp, pd.Timestamp, pd.Timestamp, pd.Timestamp]],
    sensors: list[str] | None = None,
    figsize: tuple[int, int] = (14, 10),
    save_dir: Path | str | None = None,
    prefix: str = "anomaly_zoom"
) -> None:
    """
    Plot all anomaly windows found in the dataset.
    
    Convenience function to generate visualizations for all detected anomaly
    windows, optionally saving them to disk.
    
    Parameters
    ----------
    df_ts : pd.DataFrame
        DataFrame with datetime index and sensor columns
    anomaly_windows : list[tuple]
        List of anomaly windows from get_anomaly_windows()
    sensors : list[str], optional
        Sensor columns to plot
    figsize : tuple[int, int]
        Figure size
    save_dir : Path or str, optional
        Directory to save figures (created if needed)
    prefix : str
        Filename prefix for saved figures
        
    Examples
    --------
    >>> windows = get_anomaly_windows(df_ts, margin_minutes=120)
    >>> plot_all_anomaly_windows(df_ts, windows, save_dir='figures/')
    """
    for i, (start, end, anom_start, anom_end) in enumerate(anomaly_windows):
        save_path = None
        if save_dir:
            save_dir = Path(save_dir)
            save_dir.mkdir(parents=True, exist_ok=True)
            save_path = save_dir / f'{prefix}_{i}.png'
        
        plot_anomaly_zoom(
            df_ts, start, end, 
            sensors=sensors, 
            figsize=figsize, 
            save_path=save_path,
            show=False
        )

