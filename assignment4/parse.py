import csv
import sys

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)


### enter your code below
data = readCSV('permits_hydepark.csv')
def get_avg_latlng(arg):
    '''computes the average latitude and longitude of construction permits in Hyde Park and prints it to the console'''
    lattitudes = []
    longtitudes = []
    for i in range(len(arg)):
        lattitudes.append(arg[i][-3])
        longtitudes.append(arg[i][-2])
    lattitudes_total  = sum([float(n) if n else 0 for n in lattitudes])
    lattitudes_average = lattitudes_total/len(lattitudes)
    longtitudes_total = sum([float(m) if m else 0 for m in longtitudes])
    longtitudes_average = longtitudes_total/len(longtitudes)
    return "The average lattitude is " + str(lattitudes_average) + ", and the average longtitude is " + str(longtitudes_average) +"."


print get_avg_latlng(data)