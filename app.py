import streamlit as st
import pickle
import pandas as pd
import requests

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# TMDb API Key
API_KEY = "acec2617cf9c5fe2bd1b0fce95c9688d"

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Recommend similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# Page configuration
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS for blank background and styling
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        font-family: 'Segoe UI', sans-serif;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .title {
        text-align: center;
        font-size: 48px;
        color: #333;
        margin-bottom: 20px;
    }
    .movie-title {
        font-size: 18px;
        text-align: center;
        margin-top: 10px;
        color: #444;
    }
    .poster {
        border-radius: 15px;
        transition: 0.3s;
    }
    .poster:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 15px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='title'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

# Dropdown for movie selection
selected_movie_name = st.selectbox(
    "Select a movie you like:",
    movies['title'].values,
    index=0
)

# Recommend button
if st.button('🔍 Recommend'):
    names, posters = recommend(selected_movie_name)

    st.subheader("🎥 You might also like:")
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown(f"<div class='movie-title'>{names[i]}</div>", unsafe_allow_html=True)
            st.image(posters[i], use_container_width=True, caption="", output_format="JPEG")


