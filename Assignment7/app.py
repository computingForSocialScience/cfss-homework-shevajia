from flask import Flask, render_template, request, redirect, url_for
import pymysql
import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from artistNetworks import getEdgeList
from analyzeNetworks import pandasToNetworkX, randomCentralNode
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
import numpy as np
import requests
from io import open

dbname="playlists"
host="localhost"
user="root"
passwd="Thome1987"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

app = Flask(__name__)


@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))


@app.route('/playlists/')
def make_playlists_resp():
    cur = db.cursor()
    sql = '''SELECT * FROM playlist'''
    cur.execute(sql)
    playlists = cur.fetchall()
    return render_template('playlists.html',playlists=playlists)


@app.route('/playlist/<playlistId>')
def make_playlist_resp(playlistId):
    cur = db.cursor()
    sql = '''SELECT songOrder,artistName,albumName,trackName FROM songs
             WHERE playlistId=('%s')''' % (playlistId)
    cur.execute(sql)
    songs = cur.fetchall()
    return render_template('playlist.html',songs=songs)


@app.route('/addPlaylist/',methods=['GET','POST'])
def add_playlist():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('addPlaylist.html'))
    elif request.method == 'POST':
        #this code executes when someone fills out the form
        artistName = request.form['artistName']
        createNewPlaylist(artistName)
        return(redirect("/playlists/"))


def fetchARandomTrack(album_id):
    url = 'https://api.spotify.com/v1/albums/'+ album_id +'/tracks' 
    req = requests.get(url)
    data = req.json()
    items = data['items']
    row = np.random.choice(items)
    track_id = row['id']
    track_name = row['name']
    return (track_id, track_name)

def createNewPlaylist(artist_name):
    cur = db.cursor()
    sql_create_playlists ='''CREATE TABLE IF NOT EXISTS playlist (id INTEGER PRIMARY KEY AUTO_INCREMENT,rootArtist VARCHAR(128));'''
    sql_create_songs ='''CREATE TABLE IF NOT EXISTS songs (playlistId INTEGER, songOrder INTEGER,artistName VARCHAR(128), albumName VARCHAR(256), trackName VARCHAR(256));'''
    cur.execute(sql_create_playlists)
    cur.execute(sql_create_songs)

    sql_insert_artist_name = '''INSERT INTO playlist (rootArtist) VALUES ('%s');''' % (artist_name)
    cur.execute(sql_insert_artist_name)
    playlistId = cur.lastrowid
  
    root_artist_id = fetchArtistId(artist_name)
    edgelist = getEdgeList(root_artist_id, 2)
    g = pandasToNetworkX(edgelist)
    songs = []
    for i in range(30):
        artist_id = (randomCentralNode(g))
        songOrder = i + 1
        artist_name = fetchArtistInfo(artist_id)['name']
        album_ids = fetchAlbumIds(artist_id)
        random_album = np.random.choice(album_ids)
        random_album_name = fetchAlbumInfo(random_album)['name']
        random_track_name = fetchARandomTrack(random_album)[1]
        songs.append((playlistId, songOrder, artist_name, random_album_name, random_track_name))

    insertSongs = '''INSERT INTO songs 
                     (playlistId, songOrder, artistName, albumName, trackName)
                     VALUES
                     (%s, %s, %s, %s, %s)'''
    cur.executemany(insertSongs, songs)
    db.commit()
   
    print "playlists updated"

if __name__ == '__main__':
    app.debug=True
    app.run()
    #createNewPlaylist("Taylor Swift")