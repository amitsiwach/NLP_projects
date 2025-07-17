import streamlit as st
import pickle
import pandas as pd
import requests

movies_df = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies_df['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

def fetch_posters(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c6d016072f76d6e8edcc61fed0e25af9&language=en-US'.format(movie_id))
    data = response.json()
    poster_path = data['poster_path']
    full_path = "http://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies_df[movies_df['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id

        recommended_movies.append(movies_df.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_posters(movie_id))
    return recommended_movies, recommended_movies_posters

selected_movie_name =  st.selectbox('Type or select a movie from the dropdown',
     movies_list)

if st.button('Show Recommendations'):
     recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
     col1, col2, col3, col4, col5 = st.columns(5)
     with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
     with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

     with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
     with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
     with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])


#st.write('You selected:', selected_movie_name)