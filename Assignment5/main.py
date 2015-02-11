import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import plotBarChart

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print "input artists are ", artist_names
    artist_info_list = []
    album_info_list = []
    for artist_name in artist_names: 	
    	artist_id = fetchArtistId(artist_name)
    	artist_info = fetchArtistInfo(artist_id)
        artist_info_list.append(artist_info)
        albums_id = fetchAlbumIds(artist_id)
        for album_id in albums_id:
        	album_info = fetchAlbumInfo(album_id)
        	album_info_list.append(album_info)

    writeArtistsTable(artist_info_list)
    writeAlbumsTable(album_info_list)
    plotBarChart()



    

