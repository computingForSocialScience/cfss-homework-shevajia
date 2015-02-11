import sys
import requests
import csv

def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    url = 'https://api.spotify.com/v1/search?q=' + name +'&offset=0&limit=20&type=artist'
    req = requests.get(url)
    data = req.json() 
    artist_id = data['artists']['items'][0]['id']
    return artist_id.encode('utf8')
    
    

def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
`   returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
    url = 'https://api.spotify.com/v1/artists/' + artist_id
    req = requests.get(url)
    data = req.json()
    artist_info = {}
    artist_info['followers'] = str(data['followers']['total'])
    artist_info['genres'] = data['genres']
    artist_info['id'] = data['id']
    artist_info['name'] = data['name']
    artist_info['popularity'] = str(data['popularity'])
    return artist_info

