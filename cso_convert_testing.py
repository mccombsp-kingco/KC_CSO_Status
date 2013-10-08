import sys
import csv
import urllib2
import pprint
import json

"""
Things you need to do next:
- Convert data types to their proper formats.
e.g coordinates to floats, values to ints.
- Convert to GeoJSON format.
- Add in timestamp

Given remote rows from cso_status_data. Data when downloaded from url 
11TH.CSOSTATUS_N,3
30TH.CSOSTATUS_N,3
3RD.CSOSTATUS_N,3

And local cords in the form of
[{'CSO_TagName': 'ALKI', 'X_COORD': '-122.4225', 'Y_COORD': '47.57024'},
 {'CSO_TagName': 'ALSK', 'X_COORD': '-122.40695', 'Y_COORD': '47.55944'},
 {'CSO_TagName': 'MURR', 'X_COORD': '-122.4', 'Y_COORD': '47.54028'},...]

Create a data structure like
{'Timestamp': '09-25-2013 6:50'
  'Stations' : {
                 'ALKI': { 'x_cord': '-122.3222',
                           'y_cord': '47.57000',
                           'value': 3 }
               }
}


"""
# cso_cord is analagous to handle
cso_cord = open('cso_coord.csv', 'r')
# MK NOTE: Uncomment below, and comment out above to
# get your command line input back.
# cso_cord = open(sys.argv[1])

#instead of reading CSV file, it needs to read over CSV from urllib2 method
print("the real file")

# Downloading csv status values from the web.
cso_status_data = urllib2.urlopen("http://your.kingcounty.gov/dnrp/library/wastewater/cso/img/CSO.CSV")

# Read CSV into a list data type
text = cso_status_data.readlines()
cso_status_csv = csv.reader(text)
reader = csv.DictReader(cso_cord)
location = list (reader)
cso_cord.close()

# Setup our ending data format
formatted_data_dict = {'timestamp': '',
                    'stations': {}}

# Populate with station names and coordinates.
for row in location:
    formatted_data_dict['stations'][row['CSO_TagName']] = {'X_COORD': float(row['X_COORD']),
                                                       'Y_COORD': float(row['Y_COORD'])}

# Populate with station values, based on station names.
for line in cso_status_csv:
    cso_name = line[0][0:len(line[0])-12]
    cso_value = line[1]
    # If CSO exists, add to it.
    if cso_name in formatted_data_dict['stations']:
        formatted_data_dict['stations'][cso_name]['value'] = cso_value

result = json.dumps(formatted_data_dict)

#print (formatted_data_dict)
pprint.pprint(formatted_data_dict)