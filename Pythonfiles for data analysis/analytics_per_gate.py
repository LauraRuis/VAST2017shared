"""
Produces a csv file per gate-name from sensor data.
File contains number of unique vehicles per day (also number of vehicles per car type per day).
"""

import json
import csv


def write_to_csv(data, outfile_name):
    """
    Takes dict and writes number of vehicles per day to csv file.
    :param data: dict with data per day, hour and car-id
    :param outfile_name: unique string for writing data to csv
    """

    data_count = {}
    count = []
    days = data.keys()

    # loop over days
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

    # write data to csv
    with open(outfile_name, 'w', newline='') as outfile:
        spamwriter = csv.writer(outfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Day", "Total", "1", "2", "3", "4", "5", "6", "2P"])
        for key, value in data_count.items():
            print("key: ", key)
            print("value: ", value)
            data_list = []
            data_list.append(key)
            data_list.append(value['total'])
            [data_list.append(value) for key, value in value['car-types'].items()]
            spamwriter.writerow(data_list)

if __name__ == "__main__":

    # get unique gates in list
    with open("Data/route_per_ID.json", 'r') as infile:
        temp_data = json.load(infile)
    gates = []
    for key, value in temp_data.items():
        for item in value:
            if item['gate'] not in gates:
                gates.append(item['gate'])

    # loop over gates and write data to csv per gate
    for gate in gates:
        file_string = "Data/data per gate/sensor_data_" + gate + ".json"
        with open(file_string, "r") as infile:
            data = json.load(infile)
        outfile_name = "Data/data per gate/sensor_data_" + gate + ".csv"
        print("Current gate: ", gate)
        write_to_csv(data, outfile_name)
