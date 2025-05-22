import numpy as np
import pandas as pd
import ast
import logging
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[
    logging.FileHandler("app.log"),
    logging.StreamHandler()
])

# TMDb API Key
TMDB_API_KEY = ''

app = Flask(__name__)
CORS(app)

# Load Data
try:
    print("Loading datasets...")
    credits_df = pd.read_csv("credits.csv")
    movies_df = pd.read_csv("movies.csv")
    print("Datasets loaded successfully!")
except Exception as e:
    logging.error("Error loading datasets: %s", e)

# Merge Data
try:
    print("Merging datasets...")
    movies_df = movies_df.merge(credits_df, on="title")
    print("Merge completed!")
except Exception as e:
    logging.error("Error merging datasets: %s", e)

# Select and clean columns
movies_df = movies_df[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies_df.dropna(inplace=True)

def convert(obj):
    try:
        return [i['name'] for i in ast.literal_eval(obj)]
    except:
        return []

def convert3(obj):
    try:
        return [i['name'] for i in ast.literal_eval(obj)[:3]]
    except:
        return []

def fetch_director(obj):
    try:
        return [i['name'] for i in ast.literal_eval(obj) if i['job'] == "Director"]
    except:
        return []

# Apply conversion
movies_df['genres'] = movies_df['genres'].apply(convert)
movies_df['keywords'] = movies_df['keywords'].apply(convert)
movies_df['cast'] = movies_df['cast'].apply(convert3)
movies_df['crew'] = movies_df['crew'].apply(fetch_director)

# Preprocess text
movies_df['overview'] = movies_df['overview'].apply(lambda x: x.split())
for col in ['genres', 'keywords', 'cast', 'crew']:
    movies_df[col] = movies_df[col].apply(lambda x: [i.replace(" ", "") for i in x])

movies_df['tags'] = movies_df['overview'] + movies_df['genres'] + movies_df['keywords'] + movies_df['cast'] + movies_df['crew']
new_df = movies_df[['movie_id', 'title', 'tags']]
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())

# Vectorize
cv = CountVectorizer(max_features=5000, stop_words="english")
vectorized_tags = cv.fit_transform(new_df['tags']).toarray()

# Cosine similarity
similarity = cosine_similarity(vectorized_tags)

# Fetch poster from TMDb
def fetch_poster(movie_name):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
        response = requests.get(url)
        data = response.json()
        if data['results']:
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path
        return "https://via.placeholder.com/500x750?text=No+Image"
    except Exception as e:
        logging.error("Error fetching poster for '%s': %s", movie_name, e)
        return "https://via.placeholder.com/500x750?text=No+Image"

# Recommendation logic
def recommend(movie):
    try:
        movie_index = new_df[new_df['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommendations = []
        for i in movies_list:
            title = new_df.iloc[i[0]].title
            poster = fetch_poster(title)
            recommendations.append({"title": title, "poster": poster})
        return recommendations
    except Exception as e:
        logging.error("Error in recommend(): %s", e)
        return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend_movie():
    try:
        data = request.get_json()
        movie_name = data.get('movie', '')
        logging.info("Received recommendation request for: %s", movie_name)
        recommendations = recommend(movie_name)
        return jsonify({'recommended_movies': recommendations})
    except Exception as e:
        logging.error("Error in /recommend: %s", e)
        return jsonify({'error': 'Something went wrong'}), 500

if __name__ == '__main__':
    print("Started the server...")
    app.run(debug=True)
