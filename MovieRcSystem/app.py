import streamlit as st
import pickle
import pandas as pd
import requests

# Enable wide mode in Streamlit
st.set_page_config(layout="wide", page_title="Movie Recommender System")

# Load movie data and similarity matrix
movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

# Function to recommend movies
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters
    except IndexError:
        return [], []

# Custom CSS styling
st.markdown("""
    <style>
        .title {
            font-size: 3em;
            color: #ffffff;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .stApp {
            background: linear-gradient(to right, #1f4037, #99f2c8);
            color: #f8f8f8;
        }
        .recommend-button > button {
            font-size: 1.2em;
            font-weight: bold;
            background-color: #16a085;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .movie-title {
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
            text-align: center;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Page title
st.markdown('<div class="title">🎥 Movie Recommender System</div>', unsafe_allow_html=True)

# Search box with dynamic dropdown suggestions
search_query = st.text_input("Type a movie name", placeholder="Search for a movie...")

filtered_movies = movies[movies['title'].str.contains(search_query, case=False, na=False)].sort_values('title')
if not filtered_movies.empty:
    selected_movie_name = st.selectbox("Select a movie", filtered_movies['title'].values)
else:
    selected_movie_name = None
    st.warning("No movies found. Please try a different search.")

# Recommend button and results display
if st.button('Recommend', key="recommend-button") and selected_movie_name:
    names, posters = recommend(selected_movie_name)

    if names:
        st.markdown(f"### Recommendations for **{selected_movie_name}**:")
        cols = st.columns(5)  # Adjust column width for responsiveness

        for i, col in enumerate(cols):
            with col:
                col.image(posters[i], use_column_width=True)
                col.markdown(f'<div class="movie-title">{names[i]}</div>', unsafe_allow_html=True)
    else:
        st.warning("No recommendations found for this movie!")
