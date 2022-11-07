import pandas as pd
import numpy as np
import requests
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint

movie_title = []
years = []
cert = []
time = []
genres = []
imdb_score = []
movie_imdb_link = []
metascores = []
votes = []

headers = {'Accept-Language': 'en-US, en;q=0.5'}

pages = np.arange(1, 1001, 50)

for page in pages:
    page = requests.get('https://www.imdb.com/search/title/?groups=top_1000&start=' + str(page) + '&ref_=adv_nxt',
                        headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    movie_div = soup.find_all('div', class_='lister-item mode-advanced')
    sleep(randint(2, 10))

    for container in movie_div:
        name = container.h3.a.text
        movie_title.append(name)

        year = container.h3.find('span', class_='lister-item-year').text
        years.append(year)

        certificate = container.find('span', class_='certificate').text if container.p.find('span', class_='certificate') else 'Not Rated'
        cert.append(certificate)

        runtime = container.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else '-'
        time.append(runtime)

        movie_genre = container.find('span', class_='genre').text
        genres.append(movie_genre)

        imdb = float(container.strong.text)
        imdb_score.append(imdb)

        imdb_link = container.h3.a.get("href")
        for url in imdb_link:
            links = imdb_link
            if links[-1] == '/':
                link=str("https://www.imdb.com")+links[:-1]
            else:
                link=str("https://www.imdb.com")+imdb_link
        movie_imdb_link.append(link)

        m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
        metascores.append(m_score)

        nv = container.find_all('span', attrs={'name': 'nv'})
        vote = nv[0].text
        votes.append(vote)

movies = pd.DataFrame({'movie_title': movie_title,
                       'year': years,
                       'certificate': cert,
                       'time_minute': time,
                       'genres': genres,
                       'imdb_score': imdb_score,
                       'movie_imdb_link': movie_imdb_link,
                       'metascore': metascores,
                       'vote': votes})

movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
movies['time_minute'] = movies['time_minute'].str.extract('(\d+)').astype(int)
#movies['genres'] = movies['genres'].str.extract('(\d+)')
movies['metascore'] = movies['metascore'].str.extract('(\d+)')
#movies['metascore'] = pd.to_numeric(movies['metascore'], errors='coerce')
movies['vote'] = movies['vote'].str.replace(',', '').astype(int)

movies.to_csv('movies.csv')
movies.to_excel('movies.xlsx')
