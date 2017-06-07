"""
Write csv file of sensor data to json per gate.
"""

import csv
import json

INFILE = "Data/sensor_data.csv"
INFILE2 = "Data/route_per_ID.json"


def convert2json(extern, gate, outfile):
    # takes data, gate name and string for outfile name
    # outputs json file in current directory
    csvfile = open(INFILE, 'r')
    reader = csv.DictReader(csvfile)

    # initialize dict
    dict = {}

    # loop over rows in csv and make key per day
    for row in reader:
        if row['gate-name'] == gate:
            day = row['timestamp'].split()[0]
            dict[day] = {}

    # re-open reader
    csvfile = open(INFILE, 'r')
    reader = csv.DictReader(csvfile)

    # per day add key per hour
    for row in reader:
        if row['gate-name'] == gate:
            day = row['timestamp'].split()[0]
            time = row['timestamp'].split()[1]
            hour = time.split(":")[0] + ":00"
            dict[day][hour] = {}

    csvfile = open(INFILE, 'r')
    reader = csv.DictReader(csvfile)

    # per hour add dict for each car id
    for row in reader:
        if row['gate-name'] == gate:
            day = row['timestamp'].split()[0]
            time = row['timestamp'].split()[1]
            hour = time.split(":")[0] + ":00"
            dict[day][hour][row['car-id']] = {}
            dict[day][hour][row['car-id']]['car-type'] = row['car-type']
            dict[day][hour][row['car-id']]['time'] = time
            dict[day][hour][row['car-id']]['previous'] = {}
            dict[day][hour][row['car-id']]['next'] = {}

    csvfile = open(INFILE, 'r')
    reader = csv.DictReader(csvfile)

    # fill dict per car-id with data
    for row in reader:
        if row['gate-name'] == gate:
            day = row['timestamp'].split()[0]
            time = row['timestamp'].split()[1]
            hour = time.split(":")[0] + ":00"
            route = []
            times = []
            for item in extern[row['car-id']]:
                route.append(item['gate'])
                times.append(item['timestamp'])
            index = times.index(row['timestamp'])
            if index - 1 > -1:
                dict[day][hour][row['car-id']]['previous']['gate'] = route[index - 1]
                dict[day][hour][row['car-id']]['previous']['timestamp'] = times[index - 1]
            else:
                dict[day][hour][row['car-id']]['previous']['gate'] = None
                dict[day][hour][row['car-id']]['previous']['timestamp'] = None
            try:
                dict[day][hour][row['car-id']]['next']['gate'] = route[index + 1]
                dict[day][hour][row['car-id']]['next']['timestamp'] = times[index + 1]
            except IndexError:
                dict[day][hour][row['car-id']]['next']['gate'] = None
                dict[day][hour][row['car-id']]['next']['timestamp'] = None

    json.dump(dict, outfile, indent=4, separators=(',', ': '))
    outfile.write('\n')


if __name__ == '__main__':

    # get unique gates
    with open(INFILE2, 'r') as infile:
        data = json.load(infile)
    gates = []
    for key, value in data.items():
        for item in value:
            if item['gate'] not in gates:
                gates.append(item['gate'])

    # loop over gates and convert to json per gate
    for gate in gates:
        file_string = "Data/sensor_data_" + gate + ".json"
        outfile = open(file_string, "w")
        convert2json(data, gate, outfile)
