import streamlit as st
import pickle
import pandas as pd
import requests

# Enable wide mode in Streamlit
st.set_page_config(layout="wide")

# Load movie data and similarity matrix
movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


# Function to fetch movie poster
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# Function to recommend movies
def recommend(movie):
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


# Custom CSS styling
st.markdown("""
    <style>
        /* Style the title */
        .title {
            font-size: 3em;
            color: #ffffff; /* Change title color to white */
            text-align: center;
            font-weight: bold;
            padding: 10px 0;
            margin-bottom: 20px;
        }
        /* Background gradient */
        .stApp {
            background: linear-gradient(to right, #2c3e50, #bdc3c7);
            color: #f2f2f2;
            padding: 20px;
        }
        /* Center the select box and button */
        .stButton>button, .stSelectbox {
            display: block;
            margin: 0 auto; /* Center align */
            color: white;
            font-size: 1.2em;
            font-weight: bold;
            border-radius: 12px;
            padding: 10px 20px;
        }
        /* Center-align movie titles in recommendations */
        .movie-title {
            font-size: 1.4em;
            font-weight: bold;
            color: #ffffff;
            max-width: 300px;  /* Increased max width for wider titles */
            white-space: nowrap; /* Prevent wrapping */
            overflow: hidden;    /* Hide overflow */
            text-overflow: ellipsis; /* Show ellipsis for overflow */
            text-align: center;
            margin: auto;
        }
        /* Column layout for movie posters */
        .css-1inhw8n {
            justify-content: space-around;
            text-align: center;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Title and selection box
st.markdown('<div class="title">Movie Recommender System</div>', unsafe_allow_html=True)
selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

# Recommend button and results display
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Set expanded column widths
    cols = st.columns([2, 2, 2, 2, 2])

    # Display each recommendation in a column
    for i, col in enumerate(cols):
        with col:
            # Use st.markdown with inline HTML and the .movie-title class for styling
            col.markdown(f'<div class="movie-title">{names[i]}</div>', unsafe_allow_html=True)
            col.image(posters[i], use_column_width=True)
