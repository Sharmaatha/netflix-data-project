import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("netflix_titles.csv")

# Drop nulls from relevant columns
df.dropna(subset=['type', 'listed_in'], inplace=True)

# Split genres and explode them into rows
df['genre_list'] = df['listed_in'].str.split(', ')
df_exploded = df.explode('genre_list')

# Preview genre clusters
print(df_exploded[['title', 'type', 'genre_list']].head())

# Count genre occurrences
genre_counts = df_exploded['genre_list'].value_counts().head(15)

# Plot
plt.figure(figsize=(10, 5))
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='coolwarm')
plt.title("Top 15 Genres on Netflix")
plt.xlabel("Number of Titles")
plt.ylabel("Genre")
plt.tight_layout()
plt.savefig("top_genres.png")
plt.show()

# Group by genre and content type
genre_type_counts = df_exploded.groupby(['genre_list', 'type']).size().unstack().fillna(0)

# Show top 10 genres
top10_genres = genre_counts.head(10).index
genre_type_counts = genre_type_counts.loc[top10_genres]

# Plot stacked bar chart
genre_type_counts.plot(kind='barh', stacked=True, figsize=(10, 6), colormap='Set2')
plt.title("Top Genres Grouped by Content Type")
plt.xlabel("Number of Titles")
plt.ylabel("Genre")
plt.tight_layout()
plt.savefig("top_genres_by_type.png")
plt.show()
