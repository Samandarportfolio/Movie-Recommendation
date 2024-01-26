import streamlit as st 
import pickle
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=ce3d02d3bcdfc7837c5f5031adda2750&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500" + poster_path
    return full_path


movies = pickle.load(open('movies.list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = movies['title'].values

indices = dict(zip(movies['title'].str.lower(), range(len(movies))))

st.header("Movie Recommender System")

selected_movie = st.selectbox("Select a movie:", movie_list)

import streamlit.components.v1 as components

def get_recommendations(title):
    # Convert the input title to lowercase
    title_lower = title.lower()

    # Check if the lowercase title exists in the indices dictionary
    if title_lower not in indices:
        # If not found, check for a partial match
        matches = [movie_title for movie_title in indices.keys() if title_lower in movie_title.lower()]

        if not matches:
            return "Movie not found. Please check your input."

        # Use the first partial match found
        title_lower = matches[0]

    # Get the index for the lowercase title
    idx = indices[title_lower]

    # Retrieve similarity scores for the lowercase title
    sim_scores = list(enumerate(similarity[idx]))

    # Sort the similarity scores in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    recommend_movies = []
    recommend_poster = []
    # movie_indices = [i[0] for i in sim_scores]
    for i in sim_scores[0:5]:
        movies_id = movies.iloc[i[0]].id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))
   # Return the movie titles corresponding to the indices
    return recommend_movies, recommend_poster

if st.button("Search Movies : "):
    movie_name, movie_poster = get_recommendations(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
    