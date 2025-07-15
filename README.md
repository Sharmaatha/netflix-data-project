# 🎬 Netflix Data Explorer (Streamlit App)

A data engineering + visualization project to explore Netflix Movies & TV Shows using Python, Pandas, and Streamlit.

## 🔍 Features

- Load and clean a Netflix dataset (CSV)
- Group by Genre Clusters (Global, Story-Driven, Kids, Informational, Series, Others)
- Interactive filters:
  - Genre Cluster
  - Content Type (Movie / TV Show)
  - Year Range
- Display:
  - Filtered Data Table with 3000+ titles
  - Bar Chart for Genre Cluster Distribution
- Modern UI inspired by Netflix branding

## 🛠️ Tools Used

- **Python**
- **Pandas**
- **Streamlit**
- **Matplotlib**
- **VS Code**

## 📁 Project Structure
├── netflix_titles.csv
├── netflix_pipeline.py # Data cleaning (optional)
├── netflix_dashboard.py # Streamlit web dashboard
└── README.md
git clone https://github.com/yourusername/netflix-data-project.git
cd netflix_data_project
pip install -r requirements.txt
streamlit run netflix_dashboard.py


📦 Dataset Source
Kaggle Netflix Dataset
