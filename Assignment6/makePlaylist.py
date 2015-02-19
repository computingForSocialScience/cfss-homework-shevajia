import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from artistNetworks import writeEdgeList
from analyzeNetworks import readEdgeList, combineEdgeLists, pandasToNetworkX, randomCentralNode
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
import numpy as np
import requests
from io import open


artist_names = sys.argv[1:]
print "input artists are ", artist_names
artistID_list = [fetchArtistId(artist_name) for artist_name in artist_names]
for artistID in artistID_list:
	writeEdgeList(artistID, 2, artistID + '.csv')

combinedEdgeList = readEdgeList(artistID_list[0] + '.csv')

for artistID in artistID_list[1:]:
    edgeList = readEdgeList(artistID + '.csv')
    combinedEdgeList = combineEdgeLists(combinedEdgeList, edgeList)

g = pandasToNetworkX(combinedEdgeList)

sample = []
for i in range(30):
	sample.append(randomCentralNode(g))

outfile = open('playlist.csv', 'w', encoding = 'utf-8')
outfile.write(u'artist_name,album_name,track_name\n')

def fetchARandomTrack(album_id):
	url = 'https://api.spotify.com/v1/albums/'+ album_id +'/tracks' 
	req = requests.get(url)
	data = req.json()
	items = data['items']
	row = np.random.choice(items)
	track_id = row['id']
	track_name = row['name']
	return (track_id, track_name)


for artist in sample:
	artist_name = fetchArtistInfo(artist)['name']
	album_ids = fetchAlbumIds(artist)
	random_album = np.random.choice(album_ids)
	random_album_name = fetchAlbumInfo(random_album)['name']
	random_track_name = fetchARandomTrack(random_album)[1]
	line = '"' + artist_name + '","' + random_album_name + '","' + random_track_name +'"\n'
	outfile.write(line)

outfile.close()
print "playlist.csv is saved."  