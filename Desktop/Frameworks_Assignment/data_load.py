# data_load.py
import pandas as pd

def load_data(path="metadata.csv", nrows=None):
    """
    Loads metadata.csv. Use nrows for a faster small sample during development.
    """
    return pd.read_csv(path, nrows=nrows, dtype=str)
