import requests
import pandas as pd

def getRelatedArtists(artist_id):
    """Using the Spotify API, takes a string representing the id and 
    returns a list of related artists.
    """
    url = 'https://api.spotify.com/v1/artists/' + artist_id +'/related-artists'
    req = requests.get(url)
    data = req.json()
    related_artists = []
    for item in data['artists']:
        related_artists.append(item['id'])
    return related_artists

def getDepthEdges(artistID, depth):
    artists_list = [artistID]
    starting_indexs = [0]
    edges = []
    for i in range(depth):
        starting_indexs.append(len(artists_list))
        for artist in artists_list[starting_indexs[i]:]:
            related_artists = getRelatedArtists(artist) 
            for related_artist in related_artists:
                if related_artist in artists_list:
                    pass
                else:
                    artists_list.append(related_artist)
                if (related_artist, artist) in edges:
                    pass
                else:
                    edges.append((artist, related_artist))
            
    return edges

def getEdgeList(artistID, depth):
    edges = getDepthEdges(artistID, depth)
    edgelist = pd.DataFrame(edges)
    return edgelist

def writeEdgeList(artistID, depth, filename):
    getEdgeList(artistID, depth).to_csv(filename, index = False)
    print filename + " is saved."