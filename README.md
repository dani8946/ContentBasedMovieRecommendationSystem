
# 🎬 Content Based Movie Recommendation System

Welcome to the **Content Movie Recommendation System** — a smart, content-based recommender that helps you discover movies similar to your favorites!

---

## 🚀 Project Overview

This project provides personalized movie recommendations based on the content and metadata of films. By analyzing genres, keywords, cast, crew, and overviews, it suggests movies that share similar themes and characteristics.

---

## 🧠 Recommendation Type & Algorithm

### Content-Based Filtering

- The system recommends movies **similar in content** to a movie you like.
- It focuses on **movie metadata and descriptions** instead of user ratings or interactions.

### How It Works:

- Extracts features from:
  - Movie **genres** 🎭
  - **Keywords** 🏷️
  - **Cast** 👩‍🎤
  - **Crew/Director** 🎬
  - Movie **overview** 📖
- Text data is **preprocessed and combined into a single 'tags' column**.
- Uses **Count Vectorizer** to transform text tags into numeric feature vectors.
- Calculates **cosine similarity** between movie vectors to find the closest matches.
- Returns the top 5 most similar movies with posters fetched from TMDb API.

---

## 🛠️ Tech Stack

| Technology          | Description                           | Icon      |
|---------------------|-------------------------------------|-----------|
| **Python**          | Core programming language            | 🐍        |
| **Flask**           | Web framework for backend API        | 🌐        |
| **Pandas & NumPy**  | Data manipulation & numerical ops    | 📊        |
| **scikit-learn**    | Machine learning (CountVectorizer, Cosine Similarity) | 🤖        |
| **TMDb API**        | Movie metadata & poster images       | 🎥        |
| **Requests**        | HTTP requests for API calls          | 🔗        |
| **Flask-CORS**      | Handling cross-origin requests       | 🔐        |
| **HTML/CSS/JS**     | Frontend for user interaction        | 🎨        |

---

## ⚙️ Features

- 🔍 Search for your favorite movie.
- 🎯 Get top 5 recommendations based on content similarity.
- 🖼️ View movie posters dynamically fetched from TMDb.
- 📈 Powered by cosine similarity of movie metadata vectors.
- 🚀 Fast and lightweight Flask backend with REST API.

---

## 💡 How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/dani8946/ContentBasedMovieRecommendationSystem
   cd ContentBasedMovieRecommendationSystem
   ```

2. Add your TMDb API key in `app.py`:
   ```python
   TMDB_API_KEY = 'your_tmdb_api_key_here'

3. Run the Flask app:
   ```bash
   python app.py
   ```

4. Open your browser and enjoy!


---

## ⚠️ Notes

- Ensure **credits.csv** and **movies.csv** are in the project directory.
- TMDb API key is required to fetch movie posters.
- Data preprocessing handles missing and malformed entries gracefully.
- Logs are saved in `app.log` for troubleshooting.

---

## 🙌 Contributions

Feel free to **fork**, **star ⭐**, and submit **pull requests** to improve the project!

---

⭐ **Enjoy discovering your next favorite movie!** 🎬🍿
