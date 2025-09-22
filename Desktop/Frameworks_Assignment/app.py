# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

st.set_page_config(page_title="CORD-19 Data Explorer", layout="wide")
st.title("CORD-19 Data Explorer — Beginner version")
st.write("Simple exploration of the `metadata.csv` file. Put metadata.csv in the same folder as this app.")

@st.cache_data
def load_data(path="metadata.csv", nrows=None):
    return pd.read_csv(path, nrows=nrows, dtype=str)

# try to load dataset
try:
    df = load_data("metadata.csv", nrows=None)  # change nrows for faster testing
except FileNotFoundError:
    st.error("metadata.csv not found. Put the file in the same folder as app.py and refresh.")
    st.stop()

# basic cleaning inline (keeps app simple)
df['publish_time'] = pd.to_datetime(df.get('publish_time'), errors='coerce')
df['year'] = df['publish_time'].dt.year
df['title'] = df.get('title').fillna('')
df['abstract'] = df.get('abstract').fillna('')
# drop rows without title or year
df = df[df['title'].str.strip().astype(bool) & df['year'].notna()].copy()
df['year'] = df['year'].astype(int)

# sidebar controls
min_year = int(df['year'].min())
max_year = int(df['year'].max())
year_range = st.sidebar.slider("Select year range", min_year, max_year, (min_year, max_year))
nrows_sample = st.sidebar.number_input("Sample rows to show", min_value=5, max_value=100, value=10)

# filter
dff = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Publications by year
st.header("Publications over time")
year_counts = dff['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index.astype(int), year_counts.values)
ax.set_xlabel("Year")
ax.set_ylabel("Number of papers")
ax.set_title("Publications by Year")
st.pyplot(fig)

# Top journals
if 'journal' in df.columns:
    st.header("Top journals")
    top_journals = dff['journal'].fillna('Unknown').value_counts().head(10)
    fig2, ax2 = plt.subplots()
    ax2.barh(top_journals.index[::-1], top_journals.values[::-1])
    ax2.set_title("Top 10 journals")
    st.pyplot(fig2)

# Top words in titles (simple frequency)
st.header("Common words in titles")
titles = dff['title'].dropna().str.lower()
stopwords = set([
    'the','and','of','in','to','a','for','on','with','by','from','an','is','study','analysis',
    'covid','covid19','sars','coronavirus','new'
])
counter = Counter()
for t in titles:
    tokens = re.findall(r'\w+', t)
    counter.update([w for w in tokens if w not in stopwords])
top_words = counter.most_common(20)
if top_words:
    words, counts = zip(*top_words)
    fig3, ax3 = plt.subplots(figsize=(8,4))
    ax3.bar(words, counts)
    ax3.set_xticklabels(words, rotation=45, ha='right')
    ax3.set_title("Top title words (filtered)")
    st.pyplot(fig3)
else:
    st.write("No title words found in selection.")

# sample table
st.header("Sample records")
st.dataframe(dff[['publish_time','title','journal']].head(nrows_sample))
