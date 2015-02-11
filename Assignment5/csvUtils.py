from io import open

def writeArtistsTable(artist_info_list):
    """Given a list of dictionries, each as returned from 
    fetchArtistInfo(), write a csv file 'artists.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY
    """
    outfile = open('artists.csv', 'w', encoding = 'utf-8')
    outfile.write(u'ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY\n')
    for artist_info in artist_info_list:
        line = artist_info['id']+ u',"' + artist_info['name'] + u'",' + str(artist_info['followers']) + u',' + str(artist_info['popularity']) + u'\n'
        outfile.write(line) 
    outfile.close()   

def writeAlbumsTable(album_info_list):
    """
    Given list of dictionaries, each as returned
    from the function fetchAlbumInfo(), write a csv file
    'albums.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY
    """
    outfile = open('albums.csv', 'w', encoding = 'utf-8')
    outfile.write(u'ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY\n')
    for album_info in album_info_list:
        line = album_info['artist_id']+ u',' + album_info['album_id'] + u',"' + album_info['name'] + u'",' + album_info['year'] + u',' + str(album_info['popularity']) + u'\n'
        outfile.write(line) 
    outfile.close() 
