import streamlit as st 
import pickle
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ce3d02d3bcdfc7837c5f5031adda2750&language=en-US".format(movie_id)
    try:
        data = requests.get(url)
        data.raise_for_status()  # Raise an exception for bad responses
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500" + poster_path
        return full_path
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching movie details: {e}")
        return None

movies = pickle.load(open('movies.list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = movies['title'].values

indices = dict(zip(movies['title'].str.lower(), range(len(movies))))

st.header("Movie Recommender System")

selected_movie = st.selectbox("Select a movie", movie_list)

import streamlit.components.v1 as components

def get_recommendations(title):
    title_lower = title.lower()

    if title_lower not in indices:
        matches = [movie_title for movie_title in indices.keys() if title_lower in movie_title.lower()]

        if not matches:
            return "Movie not found. Please check your input."

        title_lower = matches[0]

    idx = indices[title_lower]
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    recommend_movies = []
    recommend_poster = []

    for i in sim_scores[1:16]:
        movies_id = movies.iloc[i[0]].id
        recommend_movies.append(movies.iloc[i[0]].title)
        poster = fetch_poster(movies_id)
        if poster:
            recommend_poster.append(poster)

    return recommend_movies, recommend_poster

if st.button("Search Movies"):
    movie_name, movie_poster = get_recommendations(selected_movie)

    if movie_name:
        rows = 3
        cols = 5

    for row in range(rows):
        col1, col2, col3, col4, col5 = st.columns(cols)

        for col_index, col in enumerate([col1, col2, col3, col4, col5]):
            index = row * cols + col_index

            if index < len(movie_name):
                with col:
                    st.text(movie_name[index])
                    st.image(movie_poster[index])
else:
    st.warning("No recommendations found.")



