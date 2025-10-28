import pytest
from unittest.mock import patch
import pandas as pd
from wqdab.data import (
    load_single_dataset_2017,
    load_single_dataset_2018,
    load_single_dataset_2019,
    load_temporal_drift_task,
    load_domain_drift_task,
    load_all_datasets,
)

# Mock dataset for testing
@pytest.fixture
def mock_dataframe():
    return pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

@patch('wqdab.data.pd.read_parquet')
def test_load_single_dataset_2017(mock_read_parquet, mock_dataframe):
    mock_read_parquet.return_value = mock_dataframe
    train, test = load_single_dataset_2017()
    assert train.equals(mock_dataframe)
    assert test.equals(mock_dataframe)
    assert mock_read_parquet.call_count == 2

@patch('wqdab.data.pd.read_parquet')
def test_load_single_dataset_2018(mock_read_parquet, mock_dataframe):
    mock_read_parquet.return_value = mock_dataframe
    train, test = load_single_dataset_2018()
    assert train.equals(mock_dataframe)
    assert test.equals(mock_dataframe)
    assert mock_read_parquet.call_count == 2

@patch('wqdab.data.pd.read_parquet')
def test_load_single_dataset_2019(mock_read_parquet, mock_dataframe):
    mock_read_parquet.return_value = mock_dataframe
    train, val, test = load_single_dataset_2019()
    assert train.equals(mock_dataframe)
    assert val.equals(mock_dataframe)
    assert test.equals(mock_dataframe)
    assert mock_read_parquet.call_count == 3

@patch('wqdab.data.pd.read_parquet')
def test_load_temporal_drift_task(mock_read_parquet, mock_dataframe):
    mock_read_parquet.return_value = mock_dataframe
    source, target_train, target_test = load_temporal_drift_task()
    assert source.equals(pd.concat([mock_dataframe, mock_dataframe]))
    assert target_train.equals(mock_dataframe)
    assert target_test.equals(mock_dataframe)
    assert mock_read_parquet.call_count == 4

@patch('wqdab.data.pd.read_parquet')
def test_load_domain_drift_task(mock_read_parquet, mock_dataframe):
    mock_read_parquet.return_value = mock_dataframe
    source, target_train, target_test = load_domain_drift_task()
    assert source.equals(pd.concat([mock_dataframe] * 4).reset_index(drop=True))
    assert target_train.equals(pd.concat([mock_dataframe, mock_dataframe]))
    assert target_test.equals(mock_dataframe)
    assert mock_read_parquet.call_count == 7

@patch('wqdab.data.pd.read_parquet')
def test_load_all_datasets(mock_read_parquet, mock_dataframe):
    mock_read_parquet.return_value = mock_dataframe
    results = load_all_datasets()
    assert all([result.equals(mock_dataframe) for result in results])
    assert mock_read_parquet.call_count == 7
