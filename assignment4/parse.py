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


def zip_code_barchart(arg):
    import matplotlib.pyplot as plt
    zipcodes = []
    for i in range(15): #There are at most 15 contractors in the data.
        column = 28 + 7*i
        for permit in arg:
            if permit[column] != '':
                zipcodes.append(permit[column][0:5])

    zipcode_count = {}
    for zipcode in zipcodes:
        if zipcode in zipcode_count:
            zipcode_count[zipcode] = zipcode_count[zipcode] + 1
        else:
            zipcode_count[zipcode] = 1
    
    width = 1
    plt.figure(figsize = (20,6))
    plt.bar(range(len(zipcode_count)), zipcode_count.values(), width, color = 'red')
    plt.xticks(range(len(zipcode_count)), zipcode_count.keys(), rotation=45, fontsize =7)
    plt.ylabel('Frequency')
    plt.title('Frequency by zipcode')
    plt.savefig('barchart.jpg')

if len(sys.argv) == 1:
	print get_avg_latlng(data)
	zip_code_barchart(data)
elif sys.argv[1] == 'latlong':
	print get_avg_latlng(data)
elif sys.argv[1] == 'hist':
	zip_code_barchart(data)
