# Launch with
#
# gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc

from flask import Flask, render_template
import sys,os
import pandas as pd
import numpy as np


app = Flask(__name__)


@app.route("/")
def Users():
    """Show a list of article titles"""
    
    return render_template('Home.html', fav_songs_genre = user_list)


@app.route("/users/<user_id>")
def article(user_id):
    """
    Show an article with relative path filename. Assumes the BBC structure of
    topic/filename.txt so our URLs follow that.
    """
    return render_template('Songs.html', customized = customized_songs[user_id], lyrics = list(lyrics_songs[user_id]))


page1_data = pd.read_csv('page1_users.csv').sort_values('avg_play_count', ascending=False)
unique_users = list(page1_data.user_id.unique())
user_dct = {user_id:[] for user_id in unique_users}
user_genre = {user_id:'' for user_id in unique_users}

for i in range(page1_data.shape[0]):
    user_dct[page1_data.loc[i,'user_id']].append(page1_data.loc[i,'title'])
    user_genre[page1_data.loc[i,'user_id']] = page1_data.loc[i,'genre']

user_list = []
for i in user_dct:
    user_dct[i] = user_dct[i][:5]
    #user_dct[i].append(user_genre[i])
    user_list.append([i,user_dct[i],user_genre[i]])

page2_data = pd.read_csv('page2.csv')
customized_songs = {i:[] for i in user_dct}

for i in range(page2_data.shape[0]):
    customized_songs[page2_data.loc[i,'user_id']].append([page2_data.loc[i,'title'],
                                                          page2_data.loc[i,'artist_name'],
                                                          page2_data.loc[i,'prediction']])

page2_lyrics = pd.read_csv('page2_lyrics.csv')

lyrics_songs = {i:set() for i in user_dct}

for i in range(page2_lyrics.shape[0]):
    lyrics_songs[page2_lyrics.loc[i,'user_id']].add((page2_lyrics.loc[i,'title'],
                                                          page2_lyrics.loc[i,'artist_name'],
                                                          page2_lyrics.loc[i,'popularity_prediction']))

for i in lyrics_songs:
    if len(lyrics_songs[i])<10:
        n_random = 10 - len(lyrics_songs[i])
        np.random.seed(10)
        list_ind = np.random.randint(low = 1 , high = 3160, size = n_random)
        for j in list_ind:
            lyrics_songs[i].add((page2_lyrics.loc[j,'title'],
                                                          page2_lyrics.loc[j,'artist_name'],
                                                          page2_lyrics.loc[j,'popularity_prediction']))

app.run(debug = True)