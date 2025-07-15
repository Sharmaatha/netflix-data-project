import streamlit as st
import pandas as pd

# 🧠 Basic Setup
st.set_page_config(page_title="Netflix Explorer", layout="wide")

# 🎨 Custom CSS
st.markdown("""
    <style>
        body {
            background-color: #111;
            color: white;
        }
        .stDataFrame {
            border: 2px solid white;
            border-radius: 5px;
        }
        .dataframe {
            font-size: 16px;
        }
        .block-container {
            padding-top: 2rem;
        }
        h1, h2, h3 {
            color: #E50914;
        }
    </style>
""", unsafe_allow_html=True)

# 📌 Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/7/75/Netflix_icon.svg", width=80)
st.sidebar.title("🎛️ Filter Options")

# 📂 Load and prepare dataset
df = pd.read_csv("netflix_titles.csv")
df.dropna(subset=["type", "release_year", "country", "listed_in"], inplace=True)
df["genre_list"] = df["listed_in"].str.split(", ").apply(lambda genres: [g.strip() for g in genres])

df_exploded = df.explode("genre_list")

# 🎯 Genre Clustering
genre_map = {
    'Action': 'Entertainment',
    'Adventure': 'Entertainment',
    'Animation': 'Entertainment',
    'Children & Family Movies': 'Kids',
    'Family': 'Kids',
    'Kids': 'Kids',
    'Comedy': 'Entertainment',
    'Dramas': 'Story-Driven',
    'Drama': 'Story-Driven',
    'Romantic': 'Story-Driven',
    'Romantic Movies': 'Story-Driven',
    'Horror': 'Dark',
    'Thriller': 'Dark',
    'Crime': 'Dark',
    'Documentaries': 'Informational',
    'Documentary': 'Informational',
    'Reality': 'Informational',
    'International Movies': 'Global',
    'International TV Shows': 'Global',
    'TV Shows': 'Series',
    'TV Dramas': 'Series',
    'TV Comedies': 'Series'
}

df_exploded["genre_cluster"] = df_exploded["genre_list"].map(lambda x: genre_map.get(x, 'Other'))

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

# Apply the function to assign genre clusters
df['genre_cluster'] = df['listed_in'].apply(assign_genre_cluster)


# 🧮 Sidebar Filters
selected_cluster = st.sidebar.selectbox("Select Genre Cluster", sorted(df_exploded["genre_cluster"].unique()))
selected_type = st.sidebar.multiselect("Select Content Type", df_exploded["type"].unique(), default=df_exploded["type"].unique())

# Add back release year filter
min_year = int(df_exploded["release_year"].min())
max_year = int(df_exploded["release_year"].max())
year_range = st.sidebar.slider("Select Release Year Range", min_value=min_year, max_value=max_year, value=(2010, 2020))

# 📊 Filter data
filtered = df_exploded[
    (df_exploded["genre_cluster"] == selected_cluster) &
    (df_exploded["type"].isin(selected_type)) &
    (df_exploded["release_year"].between(year_range[0], year_range[1]))
]

# ==========================
# 🔴 Section 1: Data Table
# ==========================
st.markdown(f"## 🎞️ Netflix Shows")
st.dataframe(
    filtered[["title", "type", "release_year", "country", "genre_list"]],
    use_container_width=True
)

st.success(f"Total titles shown: {filtered.shape[0]}")

# ==========================
# 🔴 Section 2: Bar Chart
# ==========================
# Genre Cluster Distribution - Bar Chart
st.markdown("---")
st.header("📊 Genre Cluster Distribution")

import matplotlib.pyplot as plt

# Predefined genre categories
expected_genres = ['Global', 'Informational', 'Series', 'Kids', 'Story-Driven', 'Other']

# Calculate genre counts safely
genre_counts = df['genre_cluster'].value_counts().reindex(expected_genres, fill_value=0)

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 4))  # Adjusted for smaller width

# Plot horizontal bars
bars = ax.barh(genre_counts.index, genre_counts.values, color='crimson', height=0.5)

# Add value labels
for bar in bars:
    width = bar.get_width()
    ax.text(width + 1, bar.get_y() + bar.get_height()/2, str(width),
            va='center', color='white', fontsize=9)

# Customize appearance
ax.set_xlabel("Number of Movies/ Shows ", color='white')
ax.set_facecolor('#1c1c1e')
fig.patch.set_facecolor('#1c1c1e')
ax.tick_params(colors='white')
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.set_title("Titles by Genre ", fontsize=12, weight='bold', color='white')

# Display chart in Streamlit
st.pyplot(fig)


