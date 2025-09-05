import csv
import datetime
import math
import os
from dotenv import load_dotenv
from research.utrecht_rectangle import UtrechtRectangle


rectangle = UtrechtRectangle()
load_dotenv()
chart = []
with open(os.getcwd() + "/geocode.csv", newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
    for row in reader:
        items = []
        for item in row[0].split(','):
            items.append(int(item))
        chart.append(items)
    chart.reverse()

last_sensor_id = int(os.getenv('LAST_SENSOR_ID'))
last_date = datetime.datetime.strptime((os.getenv('END_DATE')),"%Y-%m-%d,%H:%M:%S").strftime('%Y-%m-%d')
for id_sensor in range(1, last_sensor_id + 1):
    results = []
for id_sensor in range(1, last_sensor_id + 1):
    latitudes = {}
    longitudes = {}
    utrecht = []
    particulate_matter = 0
    start_date = ''
    end_date = ''
    with open(os.getcwd() + "/ids/" + str(id_sensor) + "/out.csv", newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        count_latitude = 0
        count_longitude = 0
        for key, row in enumerate(reader):
            date_object = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            date = date_object.strftime('%Y-%m-%d')
            end_date = date
            if key == 0:
                start_date = date
            latitude = row[4]
            if latitude == '':
                continue
            else:
                latitude = float(latitude)
            longitude = row[3]
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
            if row[9] != '' or row[10] != '':
                particulate_matter = 1
    utrecht_city = False
    start_date_utrecht = ''
    end_date_utrecht = ''
    for key, latitude in latitudes.items():
        longitude = longitudes[key]
        utrecht_row = [key]
        end_date_utrecht = key
        if rectangle.long_e > longitude > rectangle.long_w and rectangle.lat_n > latitude > rectangle.lat_s:
            north = math.ceil((latitude - rectangle.lat_s) * rectangle.step_inverse)
            south = math.floor((latitude - rectangle.lat_s) * rectangle.step_inverse)
            east = math.ceil((longitude - rectangle.long_w) * rectangle.step_inverse)
            west = math.floor((longitude - rectangle.long_w) * rectangle.step_inverse)
            chart_sw = chart[south][west]
            chart_se = chart[south][east]
            chart_nw = chart[north][west]
            chart_ne = chart[north][east]
            if chart_sw == 1 or chart_se == 1 or chart_nw == 1 or chart_ne == 1:
                utrecht_row.append(1)
                if not utrecht_city and start_date_utrecht == '':
                    start_date_utrecht = key
                utrecht_city = True
            else:
                utrecht_row.append(0)
                utrecht_city = False
        else:
            utrecht_city = False
            utrecht_row.append(0)
        utrecht.append(utrecht_row)
    if utrecht_city:
        if end_date == last_date:
            end_date = ''
        if end_date_utrecht == last_date:
            end_date_utrecht = ''
        file = open(os.path.dirname(os.getcwd()) + "/utrecht.csv", "a", newline='')
        csv.writer(file).writerow([id_sensor, start_date, end_date,
                                   start_date_utrecht, end_date_utrecht, particulate_matter])
        file.close()
