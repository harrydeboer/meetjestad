import csv
import datetime


# Utrecht rectangle
lat_s = 52.03
lat_n = 52.14
long_w = 4.98
long_e = 5.19

step = 500
chart = []
with open("geocode_first.csv", newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
    for row in reader:
        items = []
        for item in row[0].split(','):
            items.append(int(item.replace('"', '')))
        chart.append(items)

last_sensor_id = 1100
for id_sensor in range(1, last_sensor_id + 1):
    latitudes = {}
    longitudes = {}
    utrecht = []
    particulate_matter = 0
    with open("ids/" + str(id_sensor) + "/out.csv", newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        count_latitude = 0
        count_longitude = 0
        for row in reader:
            date_object = datetime.datetime.strptime(row[0].replace('"', ''), "%Y-%m-%d %H:%M:%S")
            date = date_object.strftime('%Y-%m-%d')
            latitude = row[4].replace('"', '')
            if latitude == '':
                continue
            else:
                latitude = float(latitude)
            longitude = row[3].replace('"', '')
            if longitude == '':
                continue
            else:
                longitude = float(longitude)
            latitudes[date] = latitude
            if date in latitudes:
                count_latitude += 1
                latitudes[date] = (latitude + latitudes[date] * (count_latitude - 1)) / count_latitude
            else:
                latitudes[date] = latitude
                count_latitude = 1
            if date in longitudes:
                count_longitude += 1
                longitudes[date] = (longitude + longitudes[date] * (count_longitude - 1)) / count_longitude
            else:
                longitudes[date] = longitude
                count_longitude = 1
            if row[9] != '""' or row[10] != '""':
                particulate_matter = 1
    utrecht_city = False
    start_date_utrecht = ''
    end_date_utrecht = ''
    for key, latitude in latitudes.items():
        longitude = longitudes[key]
        utrecht_row = [key]
        if (long_e > longitude > long_w and lat_n > latitude > lat_s and
                chart[int((latitude - lat_s) * 500)][int((longitude - long_w) * 500)] == 1):
                utrecht_row.append(1)
                if not utrecht_city and start_date_utrecht == '':
                    start_date_utrecht = key
                utrecht_city = True
        else:
            if utrecht_city:
                end_date_utrecht = key
            utrecht_city = False
            utrecht_row.append(0)
        utrecht.append(utrecht_row)
    if utrecht_city:
        file = open("utrecht.csv", "a", newline='')
        csv.writer(file).writerow([id_sensor, next(iter(latitudes)), [*latitudes.keys()][-1],
                                   start_date_utrecht, end_date_utrecht, particulate_matter])
        file.close()
