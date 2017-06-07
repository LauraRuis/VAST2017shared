"""
Write csv file of sensor data to json per car ID with route traveled per car-id.
"""

import csv
import json

INFILE = "Data/sensor_data.csv"
OUTFILE = open("Data/route_per_ID.json", "w")


def convert2json():
    # outputs json file in current directory
    csvfile = open(INFILE, 'r')
    reader = csv.DictReader(csvfile)

    dict = {}
    # initialize list per car-id
    for row in reader:
        dict[row['car-id']] = []

    csvfile = open(INFILE, 'r')
    reader = csv.DictReader(csvfile)

    # add route per car-id
    for row in reader:
        dict[row['car-id']].append({'timestamp': row['timestamp'], 'gate': row['gate-name']})

    json.dump(dict, OUTFILE, indent=4, separators=(',', ': '))
    OUTFILE.write('\n')

if __name__ == '__main__':
    convert2json()
