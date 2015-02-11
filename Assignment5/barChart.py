import unicodecsv as csv
import matplotlib.pyplot as plt

def getBarChartData(): #Define a function.
    f_artists = open('artists.csv') #Open or create a 'artists.csv'.
    f_albums = open('albums.csv') #Open or create a 'albums.csv'.

    artists_rows = csv.reader(f_artists) #Use csv.reader to read the file.
    albums_rows = csv.reader(f_albums) #Use csv.reader to read the file.

    artists_header = artists_rows.next() #Read the first line of the artists file. 
    albums_header = albums_rows.next() #Read the first line of the albums file.

    artist_names = [] #Create an empty list called artist_names.
    
    decades = range(1900,2020, 10) #Create a list of decades that range from 1900 to 2020.
    decade_dict = {} #Create an empty dictionary.
    for decade in decades: #Loop over decades in the decades list. 
        decade_dict[decade] = 0 #Set the value of each decade in the dictionary to 0.
    
    for artist_row in artists_rows: #Loop over rows in artists file.
        if not artist_row: #If a row is empty, then skip.
            continue
        artist_id,name,followers, popularity = artist_row #Create 4 variables and let them equal to the 4 elements in the row respevtively.
        artist_names.append(name) #Append the value of the name variable to the artist_names list. 

    for album_row  in albums_rows: #Loop over rows in albums file.
        if not album_row: #If a row is empty, then skip.
            continue
        artist_id, album_id, album_name, year, popularity = album_row #Create 5 variables and let them equal to the 5 elements in the row respectively.
        for decade in decades: #Loop over decades in the decades list. 
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)): #If the release year is with the decade, let the value corresponding to the decade in the decade_dict dictionary equal increase by 1 and end the loop.
                decade_dict[decade] += 1
                break

    x_values = decades #Create a list called x_values and let it equal to decades.
    y_values = [decade_dict[d] for d in decades] #Create a list called y_values and let it equalt to the list of values correponding to all decades in the dictionary.
    return x_values, y_values, artist_names #Let the output be x_values, y_values and artist_names

def plotBarChart(): #Define a function.
    x_vals, y_vals, artist_names = getBarChartData()  #Let x_vals, y_vals, and artist_names equal to the output of the getBarChartData().
    
    fig , ax = plt.subplots(1,1) # Set the figure size to be 1 x 1.
    ax.bar(x_vals, y_vals, width=10) #Create a bar plot, let the horizontal axis equal to x_vals, and let the vertical axis equal to y_vals. Also set the width of bins to 10.
    ax.set_xlabel('decades') #Label the horizontal axis as 'decades'.
    ax.set_ylabel('number of albums') #Label the vertial axis as 'number of albums'.
    ax.set_title('Totals for ' + ', '.join(artist_names)) #Let the title of the graph be "Totals for the artist's name". 
    plt.show() #Show the plot.


    
