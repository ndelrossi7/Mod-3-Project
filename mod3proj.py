import requests
from api import API
import time
from itertools import chain
import numpy as np

# Importing necessary packages

pages = list(range(1, 793))
# number of pages of data on the website

all_2018 = []
for page in pages:
    response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key={}&language=en-US&sort_by=vote_average.desc&include_adult=false&include_video=false&page={}&primary_release_year=2018'.format(API, page))
    time.sleep(2)
    if response.status_code == 200:
        all_2018.append(response.json()['results'])
    else: 
        print('unauthorized')
# Created a list to put all of the responses from each page into        
        
all_2018_unlist = list(chain.from_iterable(all_2018))
# Unlist the original list to put into a dataframe for inspection and cleaning
df_2018 = pd.DataFrame.from_records(all_2018_unlist)
df = df_2018[['id', 'title', 'genre_ids', 'vote_average', 'vote_count', 'popularity']]
df.vote_count.replace(0, np.NaN, inplace = True)
df = df[df['vote_count'] >= 50]
# We set the vote_count greater than or equal to 50 because there were many movies with a very high score but with only 1-2 ratings

mov_ids = list(df.id)
# Made a list of ids from our top_rated table to iterate through the different ids when retrieving movie budget details
ids = []
budget = []
# putting each id and corresponding budget into separate lists
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
# Creating a cleaning dataframe

import sqlite3
conn = sqlite3.connect('tmdb.db')
# Instantiating a database
c = conn.cursor()
# connecting to the database

c.execute('''CREATE TABLE IF NOT EXISTS budgets
                 ([index] INTEGER PRIMARY KEY,
                 [id] integer,
                 [budget] integer)''')

# creating a table

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

# inserting data into table 
        
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
        
        
budgets_df = pd.read_sql('SELECT * FROM budgets', conn)
# moving from SQL to pandas for easier analysis
budgets_df['budget_c'] = budgets_df.budget.transform(lambda x: int.from_bytes(x, 'little'))
# converting budget data stored as bytes into numbers
budgets_df.drop(['budget'], axis = 1, inplace = True)
top_rated_df = pd.read_sql('SELECT * FROM top_rated', conn)
top_rated_df.drop(['index'], axis = 1, inplace = True)
df_merged = pd.merge(top_rated_df, budgets_df, on = 'id')
# merging our rating and popularity data with budget data


genre_response = requests.get(https://api.themoviedb.org/3/genre/movie/list?api_key={}&language=en-US'.format(API))
genres = response.json()['genres']
genres_df = pd.DataFrame.from_records(genres)
c.execute("""CREATE TABLE IF NOT EXISTS genres
            ([index] INTEGER PRIMARY KEY,
            [id] integer,
            [genre] text)""")
for i in range(0, len(genres_df)):
    try:
        c.execute('''INSERT INTO genres 
            (id, genre)
            VALUES(?,?)''', 
            (int(genres_df['id'][i]),
            genres_df['name'][i]))
        conn.commit()
    except:
        print(genres_df['id'][i], genres_df['name'][i])
        
                              
updated_pages = list(range(1, 795))
extra_info = []
for page in updated_pages:
    response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key={}&language=en-US&sort_by=vote_average.desc&include_adult=false&include_video=false&page={}&primary_release_year=2018'.format(API, page))
    time.sleep(3)
    if response.status_code == 200:
        extra_info.append(response.json()['results'])
    else: 
        print('unauthorized')
                              
                              
forgenre_unlist = list(chain.from_iterable(extra_info))
df_genre = pd.DataFrame.from_records(forgenre_unlist)
df_genre.vote_count.replace(0, np.NaN, inplace = True)
df_genre = df_genre[df_genre['vote_count'] >= 50]
df_genre = df_genre[['id', 'genre_ids', 'title']]
df_genre.reset_index(inplace = True)
df_genre.drop(['index'], axis = 1, inplace = True)
df_genre = df_genre[df_genre.genre_ids.map(lambda x: len(x) > 0)]
df_genre['theme'] = df_genre.genre_ids.apply(lambda x: x[0])
df_genre.drop('genre_ids', axis = 1, inplace = True)
df_genre.reset_index(inplace = True)
df_genre.drop(['index'], axis = 1, inplace = True)
                              
c.execute("""CREATE TABLE IF NOT EXISTS genre_info
            ([index] INTEGER PRIMARY KEY,
            [id] integer,
            [genre_id] integer)""")
for i in range(0, len(df_genre)):
    try:
        c.execute('''INSERT INTO genre_info 
            (id, genre_id)
            VALUES(?,?)''', 
            (int(df_genre['id'][i]),
            int(df_genre['theme'][i])))
        conn.commit()
    except:
        print(df_genre['id'][i], df_genre['theme'][i])

genre_info = pd.read_sql('SELECT * FROM genre_info', conn)
genre_info.drop(['index'], axis = 1, inplace = True)

genre_merged = pd.merge(top_rated_df, genre_info, on = 'id')