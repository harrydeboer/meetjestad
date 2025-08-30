import csv
import datetime


# Utrecht rectangle
lat_s = 52.03
lat_n = 52.14
long_w = 4.98
long_e= 5.19

chart = []
with open("geocode_first.csv", newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
    for row in reader:
        chart.append(row)

last_sensor_id = 1100
for id_sensor in range(1, last_sensor_id + 1):
    with open("ids/" + str(id_sensor) + "/out.csv", newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        for row in reader:
            date_object = datetime.datetime.strptime(row[0].replace('"', ''), "%Y-%m-%d %H:%M:%S")
            date = date_object.strftime('%Y-%m-%d %H:%M:%S')