import pandas as pd

def preprocess_data(data, means=None, stds=None):
    window_trend = 24 * 60 # 1 day (24 hours x 60 minutes)
    X = data.iloc[:,1:-1]
    missing_data = 1.0 * (X.isna().sum(axis=1) > 0)
    X_fill = X.bfill()
    y = data['EVENT'] * 1.0
    X_trend = X_fill.rolling(window_trend, min_periods=1).mean()
    X_detrended = X_fill - X_trend
    if means is None:
        means = X_detrended.mean()
    if stds is None:
        stds = X_detrended.std()
    X_detrended = (X_detrended - means)/stds
    X_detrended['missing'] = missing_data
    X['missing'] = missing_data
    return X_detrended.values, X.values, y.values, means, stds
