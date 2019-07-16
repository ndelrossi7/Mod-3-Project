import requests
from api import API
import time
from itertools import chain
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import seaborn as sns
from matplotlib import pyplot as plt
from statsmodels.stats.power import TTestIndPower, TTestPower

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
# Merging to access budget info
genre_merged = pd.merge(genres, genre_merged, left_on = 'id', right_on = 'genre_id')
# Merging to have the genre names for better visualization
genre_merged = genre_merged.groupby('genre_id').filter(lambda x : len(x)>= 10)
# Selected genres that had 10 or more movies associated with it
genre_merged.drop(['index', 'id_x'], axis = 1, inplace = True)

remakes = pd.read_csv('remakes.csv')
# The data from this CSV came from webscraping by Greg of this article: https://www.usatoday.com/picture-gallery/life/entertainthis/2018/05/05/best-and-worst-movie-remakes-of-all-time/34498459/
                              
remakes.drop('Unnamed: 0', axis = 1, inplace = True)
remakes.drop_duplicates(inplace = True)

# Making API calls based on the titles to get movie info                              
remake_search = []
for remake in remake_list:
    response = requests.get('https://api.themoviedb.org/3/search/movie?api_key={}&language=en-US&query={}&page=1&include_adult=false'.format(API, remake))
    time.sleep(2)
    if response.status_code == 200:
        remake_search.append(response.json()['results'])
    else: 
        print('unauthorized')
# Cleaning the returned data for easier work
remake_unlist = list(chain.from_iterable(remake_search))
remake_df = pd.DataFrame.from_records(remake_unlist)
remake_df = remake_df[['id', 'title', 'release_date', 'vote_average', 'vote_count']]
remake_df = remake_df[remake_df['vote_count'] >= 50]
remake_df.reset_index(inplace = True)
remake_df.drop('index', axis = 1, inplace = True)
remake_df.drop_duplicates(inplace = True)
rm_df = pd.DataFrame(remake_list)
rm_df.columns = ['title']
# merging on the original list of titles to pare down the results
merged_remake = pd.merge(remake_df, rm_df, on = 'title')

# The following is a list of IDs for movies that either did not make the cut when it came to enough votes or did not have a pair
                              
to_drop = [42884, 10772, 2020, 8198, 13188, 17979, 16716, 13189, 428081, 197796, 648, 1553, 16559, 43828, 6844, 63, 11673, 5528, 17809, 38985, 3111, 19610, 10445, 11113, 6404, 60935, 10714, 13528, 949, 58857, 34148, 1422, 4481, 8970, 36355, 13972, 25137, 97434, 87567, 5689, 10067, 13184, 46717, 14347, 24070, 263472, 929, 10484, 11045, 18681, 28696]
 
merged_remake = merged_remake[~merged_remake.id.isin(to_drop)]
# Removing any movies that are in the drop list

identifiers = []
for num in list(range(1, 56)):
    identifiers.append([num]*2)

identifiers = list(chain.from_iterable(identifiers))
                              
# Because our remakes are not all the same name and they are not all ordered based on release date, I am assigning them identifiers so that we can group by the identifier and then release date for easier subsetting. 
merged_remake['identifiers'] = identifiers
                              
merged_remake = merged_remake.sort_values(by=['identifiers', 'release_date'])
merged_remake.reset_index(inplace = True)
merged_remake.drop('index', axis = 1, inplace = True)
                              
original = merged_remake.loc[::2]
new_remake = merged_remake.loc[1::2]
# Our 2 new dataframes for our paired sample t-test                          
                              
                              ##############################STATS BELOW###########################
                              
# Running the Shapiro Wilkes test to assess normality - sample size is large enough that we do not have to worry too much about this
stats.shapiro(genre_merged['vote_average'])
# ANOVA table (one-way)
formula = 'vote_average ~ C(genre)'
lm = ols(formula, genre_merged).fit()
table = sm.stats.anova_lm(lm, typ=2)
# print(table)
m_comp = pairwise_tukeyhsd(endog=genre_merged['vote_average'], groups=genre_merged['genre'], alpha=0.05)
tukey = pd.DataFrame(data=m_comp._results_table.data[1:], columns=m_comp._results_table.data[0])
tukey[tukey['reject'] == 1]
# Running tukey tests and visualizing the ones that reject the null hypothesis