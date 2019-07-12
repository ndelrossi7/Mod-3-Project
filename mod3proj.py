import requests
from api import API
import time
from itertools import chain
import numpy as np

pages = list(range(1, 793))
all_2018 = []
for page in pages:
    response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key={}&language=en-US&sort_by=vote_average.desc&include_adult=false&include_video=false&page={}&primary_release_year=2018'.format(API, page))
    time.sleep(2)
    if response.status_code == 200:
        all_2018.append(response.json()['results'])
    else: 
        print('unauthorized')
        
all_2018_unlist = list(chain.from_iterable(all_2018))
df_2018 = pd.DataFrame.from_records(all_2018_unlist)
df = df_2018[['id', 'title', 'genre_ids', 'vote_average', 'vote_count', 'popularity']]
df.vote_count.replace(0, np.NaN, inplace = True)
df = df[df['vote_count'] >= 50]

mov_ids = list(df.id)
ids = []
budget = []
for mov_id in mov_ids:
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(mov_id, API))
    time.sleep(2)
    if response.status_code == 200:
        ids.append(response.json()['id'])
        budget.append(response.json()['budget'])
    else: 
        print('unauthorized')
        
budget_data = dictionary = dict(zip(ids, budget))
df1 = pd.DataFrame.from_dict(budget_data, orient = 'index')
df1.columns = ['budget']
df1 = df1[df1.budget != 0]

import sqlite3
conn = sqlite3.connect('tmdb.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS budgets
                 ([index] INTEGER PRIMARY KEY,
                 [id] integer,
                 [budget] integer)''')
for i in range(0, len(df1)):
    try:
        c.execute('''INSERT INTO budgets 
            (id, budget)
            VALUES(?,?)''', 
            (int(df1['id'][i]),
            df1['budget'][i]))
        conn.commit()
    except:
        print(df1['id'][i], df1['budget'][i])
        
c.execute('''CREATE TABLE IF NOT EXISTS top_rated
                 ([index] INTEGER PRIMARY KEY,
                 [id] integer,
                 [title] text,
                 [vote_average] integer, 
                 [vote_count] integer, 
                 [popularity] integer
                 )''')
for i in range(0, len(df)):
    try:
        c.execute('''INSERT INTO top_rated 
            (id, title, vote_average, vote_count, popularity)
            VALUES(?,?,?,?,?)''', 
            (int(df['id'][i]),
            df['title'][i], 
            df['vote_average'][i],
            df['vote_count'][i],
            df['popularity'][i]))
        conn.commit()
    except:
        print(df['id'][i], df['title'][i], df['vote_average'][i], df['vote_count'][i], df['popularity'][i])