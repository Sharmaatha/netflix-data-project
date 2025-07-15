import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# App Layout
st.set_page_config(page_title="Netflix Dashboard", layout="wide")
st.markdown(
    "<h1 style='color:#E50914;'>🍿 Netflix Dashboard</h1>",
    unsafe_allow_html=True
)

# Load dataset 
df = pd.read_csv("netflix_titles.csv")

# Genre Clustering Function
def assign_genre_cluster(genre_str):
    genre_str = str(genre_str).lower()
    if 'kids' in genre_str or 'children' in genre_str:
        return 'Kids'
    elif 'documentary' in genre_str or 'reality' in genre_str or 'informational' in genre_str:
        return 'Informational'
    elif 'series' in genre_str or 'tv show' in genre_str:
        return 'Series'
    elif 'drama' in genre_str or 'romance' in genre_str or 'story' in genre_str:
        return 'Story-Driven'
    elif 'action' in genre_str or 'comedy' in genre_str or 'thriller' in genre_str or 'movie' in genre_str:
        return 'Global'
    else:
        return 'Other'

df['genre_cluster'] = df['listed_in'].apply(assign_genre_cluster)

# Expander 1: Netflix Table (default open)
with st.expander("📄 View Netflix Titles Table", expanded=True):
    st.markdown("### 🗂️ All Netflix Titles")
    st.dataframe(df[["title", "type", "release_year", "country", "listed_in"]], use_container_width=True)

# Expander 2: Genre Cluster Bar Chart (default collapsed)
    st.markdown("### 📊 Genre Distribution Bar Chart")

    genre_order = ['Global', 'Informational', 'Series', 'Kids', 'Story-Driven', 'Other']
    genre_counts = df['genre_cluster'].value_counts().reindex(genre_order, fill_value=0)

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.barh(genre_counts.index, genre_counts.values, color='crimson')

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height()/2, str(width),
                va='center', color='white', fontsize=9)

    ax.set_facecolor('#1c1c1e')
    fig.patch.set_facecolor('#1c1c1e')
    ax.tick_params(colors='white')
    ax.set_xlabel(" Number of movies/shows", color='white')
    ax.set_title(" Titles by Genre ", color='white')

    st.pyplot(fig)
    
    st.markdown("""
    <style>
    .streamlit-expanderHeader {
        font-size: 18px;
        color: #E50914;
        font-weight: bold;
    }
    .stDataFrame {
        border: 2px solid white;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

