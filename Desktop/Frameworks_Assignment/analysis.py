# analysis.py
from data_load import load_data
from cleaning import clean_basic
import pandas as pd

if __name__ == "__main__":
    df = load_data(nrows=5000)   # use a small sample first (remove nrows for full file)
    print("Raw shape:", df.shape)
    print(df.dtypes)
    print("Missing values (top):")
    print(df.isnull().sum().sort_values(ascending=False).head(10))

    df = clean_basic(df)
    print("Cleaned shape:", df.shape)
    print("Years present:", sorted(df['year'].unique())[:10])
    # quick counts
    print(df['year'].value_counts().sort_index().head())
    # top journals
    if 'journal' in df.columns:
        print(df['journal'].fillna('Unknown').value_counts().head(10))
