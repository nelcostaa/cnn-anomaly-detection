import pandas as pd

def load_single_dataset_2017():
  df_2017_train = pd.read_parquet('https://drive.google.com/uc?export=download&id=1-EYCMAdgUODc_i37E8pPkQ_37COsEJp-')
  df_2017_test = pd.read_parquet('https://drive.google.com/uc?export=download&id=1-Md7j1sksTUpJUKJJCWXI058gGsuHqTT')
  return df_2017_train, df_2017_test
    
def load_single_dataset_2018():
  df_2018_train = pd.read_parquet('https://drive.google.com/uc?export=download&id=1-XfmTdzm16Zx4fvtu4Uz5mV8Xjeo2c2L')
  df_2018_test = pd.read_parquet('https://drive.google.com/uc?export=download&id=1-VX8DicXctHvhv3RZ3rCB3qHRLCsri74')
  return df_2018_train, df_2018_test
    
def load_single_dataset_2019():
  df_2019_train = pd.read_parquet('https://drive.google.com/uc?export=download&id=1-pZ8zr4_5dsbGf55H6gzKPo2hgsvPo5n')
  df_2019_val = pd.read_parquet('https://drive.google.com/uc?export=download&id=1-qTsRzdxDj0V-kGE_7K1MjnILKm3BwlT')
  df_2019_test = pd.read_parquet('https://drive.google.com/uc?export=download&id=1-blk4tBL1OLafR6Pkaer5zmt2kJwk6uK')
  return df_2019_train, df_2019_val, df_2019_test

def load_temporal_drift_task():
  df_source_train, df_source_test = load_single_dataset_2017()
  df_target_train, df_target_test = load_single_dataset_2018()
  df_source = pd.concat([df_source_train, df_source_test])
  return df_source, df_target_train, df_target_test

def load_domain_drift_task():
  df_source1_train, df_source1_test = load_single_dataset_2017()
  df_source2_train, df_source2_test = load_single_dataset_2018()
  df_target_train, df_target_val, df_target_test = load_single_dataset_2019()
  df_source = pd.concat([df_source1_train, df_source1_test, df_source2_train, df_source2_test])
  df_source = df_source.reset_index(drop=True)
  df_target_train = pd.concat([df_target_train, df_target_val])
  return df_source, df_target_train, df_target_test

def load_all_datasets():
  df_2017_train, df_2017_test = load_single_dataset_2017()
  df_2018_train, df_2018_test = load_single_dataset_2018()
  df_2019_train, df_2019_val, df_2019_test = load_single_dataset_2019()
  return df_2017_train, df_2017_test, df_2018_train, df_2018_test, df_2019_train, df_2019_val, df_2019_test
