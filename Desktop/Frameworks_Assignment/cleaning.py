# cleaning.py
import pandas as pd
import re

def clean_basic(df):
    df = df.copy()
    # convert publish_time to datetime
    df['publish_time'] = pd.to_datetime(df.get('publish_time'), errors='coerce')
    # create year column
    df['year'] = df['publish_time'].dt.year
    # fill missing short text fields
    if 'abstract' in df.columns:
        df['abstract'] = df['abstract'].fillna('')
    if 'title' in df.columns:
        df['title'] = df['title'].fillna('')

    # abstract word count
    if 'abstract' in df.columns:
        df['abstract_word_count'] = df['abstract'].apply(lambda x: len(re.findall(r'\w+', str(x))))
    # drop rows without title or year
    if 'title' in df.columns and 'year' in df.columns:
        df = df[df['title'].str.strip().astype(bool) & df['year'].notna()].copy()
        df['year'] = df['year'].astype(int)
    return df
