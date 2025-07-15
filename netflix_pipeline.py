import pandas as pd
import sqlite3

# Load CSV
df = pd.read_csv("netflix_titles.csv")
df = pd.read_csv(r"C:\Users\sharm\OneDrive\Desktop\netflix_data_project\netflix_titles.csv")

# Clean data
df = df.dropna(subset=['title', 'type', 'release_year'])
df.fillna({'director': 'Unknown', 'cast': 'Unknown', 'country': 'Unknown'}, inplace=True)
df.drop_duplicates(inplace=True)

# Save cleaned version
df.to_csv("cleaned_netflix.csv", index=False)

# Store into SQLite DB
conn = sqlite3.connect("netflix.db")
cursor = conn.cursor()
df.to_sql("netflix_titles", conn, if_exists="replace", index=False)

# Run sample queries
print("\n🎬 Top 5 Movies Released After 2015:")
query1 = cursor.execute("SELECT title, release_year FROM netflix_titles WHERE release_year > 2015 AND type = 'Movie' LIMIT 5;")
for row in query1:
    print(row)

print("\n🌍 Total Shows by Country:")
query2 = cursor.execute("SELECT country, COUNT(*) FROM netflix_titles GROUP BY country ORDER BY COUNT(*) DESC LIMIT 5;")
for row in query2:
    print(row)

conn.close()
