import json
import os
import pandas as pd

data = pd.read_csv('/Users/linh/PycharmProjects/pythonProjects/movies.csv')

df = data[['genres', 'movie_title', 'imdb_score', 'movie_imdb_link']].copy()


genres_all_movies = [df.loc[i]['genres'].strip().split(', ') for i in df.index]
genres = sorted(list(set([item for sublist in genres_all_movies for item in sublist])))

print(genres)
full_data = []
movie_titles = []

df.to_csv('usefuldata.csv')
df.to_excel('usefuldata.xlsx')

for i in df.index:
    movie_titles.append((df.loc[i]['movie_title'].strip(), i, df.loc[i]['movie_imdb_link'].strip()))
    movie_data = [1 if genre in df.loc[i]['genres'].strip().split(', ') else 0 for genre in genres]
    movie_data.append(df.loc[i]['imdb_score'])
    full_data.append(movie_data)

print(movie_titles)
data_dump = '/Users/linh/PycharmProjects/pythonProjects/movie_data.json'
titles_dump = '/Users/linh/PycharmProjects/pythonProjects/movie_titles.json'
with open(data_dump, 'w+', encoding='utf-8') as f:
    json.dump(full_data, f)
with open(titles_dump, 'w+', encoding='utf-8') as f:
    json.dump(movie_titles, f)




