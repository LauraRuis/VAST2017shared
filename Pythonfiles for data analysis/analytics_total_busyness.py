"""
Produces a csv file from sensor data.
File contains number of unique vehicles per day (also number of vehicles per car type per day).
"""

import json
import csv

# get data per day
with open("Data/sensor_data_per_timeslot.json", 'r') as infile:
    data = json.load(infile)

# initialize dict for keeping track of counts
data_count = {}

# initialize list for keeping track of unique car-id's per day
count = []

# loop over days
days = data.keys()
for day in days:

    # initialize dict for keeping track of amount of vehicles per car-type
    temp_dict = {"1": 0,
                 "2": 0,
                 "3": 0,
                 "4": 0,
                 "5": 0,
                 "6": 0,
                 "2P": 0}

    # loop over timeslots in day
    for key, value in data[day].items():

        # loop over car-id's in per timeslot
        for key, value in data[day][key].items():

            # if car-id not already counted for this day, append to total count
            if key not in count:
                count.append(key)

                # also count vehicle per type
                temp_dict[value['car-type']] += 1

    data_count[day] = {}
    data_count[day]["total"] = len(count)
    data_count[day]["car-types"] = temp_dict

    # re-initialize count list for next day
    count = []

# write to csv file
with open("Data/busyness_per_day.csv", 'w') as outfile:
    spamwriter = csv.writer(outfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for key, value in data_count.items():
        print("key: ", key)
        print("value: ", value)
        data_list = []
        data_list.append(key)
        data_list.append(value['total'])
        types = [data_list.append(value) for key, value in value['car-types'].items()]
        spamwriter.writerow(data_list)
