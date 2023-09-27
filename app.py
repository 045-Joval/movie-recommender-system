import streamlit as st
import pickle as pk
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    response = requests.get(url)
    data = response.json()
    full_path = "https://image.tmdb.org/t/p/w500" + data["poster_path"]
    return full_path


def recommend(movie, i):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    id = distances[i]

    movie_id = movies.iloc[id[0]].movie_id
    recommended_movies = movies.iloc[id[0]].title
    try:
        recommended_movies_poster = fetch_poster(movie_id)
    except KeyError:
        recommended_movies_poster = "https://siteimages.textbooks.com/img/global/img-not-avail-154.gif"
    return recommended_movies, recommended_movies_poster


movies_dict = pk.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pk.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select a movie', movies['title'].values)
i = 0
if st.button('Recommend'):
    for col in st.columns(5):
        with col:
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name, i + 1)
            st.image(recommended_movie_posters, caption=recommended_movie_names, width=140)
            i += 1






