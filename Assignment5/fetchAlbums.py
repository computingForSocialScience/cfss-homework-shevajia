import requests
from datetime import datetime

def fetchAlbumIds(artist_id):
    """Using the Spotify API, take an artist ID and 
    returns a list of album IDs in a list
    """
    url = 'https://api.spotify.com/v1/artists/'+ artist_id + '/albums?market=US&album_type=album'
    req = requests.get(url)
    data = req.json()
    items = data['items']
    album_id = [] 
    for row in items:
        album_id.append(row['id'])
    return album_id

def fetchAlbumInfo(album_id):
    """Using the Spotify API, take an album ID 
    and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
    """
    album_info = {}
    url = 'https://api.spotify.com/v1/albums/' + album_id
    req = requests.get(url)
    data = req.json()
    album_info['artist_id'] = data['artists'][0]['id']
    album_info['album_id'] =  data['id']
    album_info['name'] = data['name'] 
    album_info['year'] = data['release_date'][0:4]
    album_info['popularity'] = str(data['popularity'])
    
    return album_info

