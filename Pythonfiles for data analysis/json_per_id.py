"""
Write csv file of sensor data to json per car ID.
"""

import csv
import json

INFILE = "Data/sensor_data.csv"
OUTFILE = open("Data/sensor_data_per_ID.json", "w")


def convert2json():
    # outputs json file in current directory
    csvfile = open(INFILE, 'r')
    reader = csv.DictReader(csvfile)

    dict = {}
    # loop over rows in csv and add dict per car id, add car type to this dict
    for row in reader:
        dict[row['car-id']] = {}
        dict[row['car-id']]['car-type'] = row['car-type']
        dict[row['car-id']]['entrance'] = []
        dict[row['car-id']]['route'] = {}

    csvfile = open(INFILE, 'r')
    reader = csv.DictReader(csvfile)

    # again loop over rows and add key of day to dict with route
    for row in reader:
        day = row['timestamp'].split()[0]
        dict[row['car-id']]['route'][day] = []

    csvfile = open(INFILE, 'r')
    reader = csv.DictReader(csvfile)

    # add time and gate-name to route
    for row in reader:
        day = row['timestamp'].split()[0]
        time = row['timestamp'].split()[1]
        dict[row['car-id']]['route'][day].append({time: row['gate-name']})

    csvfile = open(INFILE, 'r')
    reader = csv.DictReader(csvfile)

    # add time of entrance and exit
    for row in reader:
        if 'entrance' in row['gate-name']:
            dict[row['car-id']]['entrance'].append(row['timestamp'])

    json.dump(dict, OUTFILE, indent=4, separators=(',', ': '))
    OUTFILE.write('\n')

if __name__ == '__main__':
    convert2json()
