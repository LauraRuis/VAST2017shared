"""
Write csv file of sensor data to json per car timeslot.
"""

import csv
import json

INFILE = "Data/sensor_data.csv"
OUTFILE = open("Data/sensor_data_per_timeslot.json", "w")


def convert2json():
    # outputs json file in current directory
    csvfile = open(INFILE, 'r')
    reader = csv.DictReader(csvfile)

    dict = {}
    # loop over rows and add key per day
    for row in reader:
        day = row['timestamp'].split()[0]
        dict[day] = {}

    csvfile = open(INFILE, 'r')
    reader = csv.DictReader(csvfile)

    # loop over rows and add hour key per hour to days
    for row in reader:
        day = row['timestamp'].split()[0]
        time = row['timestamp'].split()[1]
        hour = time.split(":")[0] + ":00"
        dict[day][hour] = {}

    csvfile = open(INFILE, 'r')
    reader = csv.DictReader(csvfile)

    # loop over rows and add dicts with car-id's to hours and the route the car has taken
    for row in reader:
        day = row['timestamp'].split()[0]
        time = row['timestamp'].split()[1]
        hour = time.split(":")[0] + ":00"
        dict[day][hour][row['car-id']] = {}
        dict[day][hour][row['car-id']]['car-type'] = row['car-type']
        dict[day][hour][row['car-id']]['entrance'] = []
        dict[day][hour][row['car-id']]['route'] = {}

    csvfile = open(INFILE, 'r')
    reader = csv.DictReader(csvfile)

    # loop over rows and add gate name per time slot
    for row in reader:
        day = row['timestamp'].split()[0]
        time = row['timestamp'].split()[1]
        hour = time.split(":")[0] + ":00"
        dict[day][hour][row['car-id']]['route'][time] = row['gate-name']

    json.dump(dict, OUTFILE, indent=4, separators=(',', ': '))
    OUTFILE.write('\n')

if __name__ == '__main__':
    convert2json()
