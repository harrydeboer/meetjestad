import meet_je_stad_api_service
import csv
import requests
from dotenv import load_dotenv
import os
import datetime


# Utrecht rectangle
lat_s = 52.05
lat_n = 52.13
long_w = 5.03
long_e= 5.19

last_sensor_id = 1100
start_year = 2022
current_year = datetime.datetime.now().year
load_dotenv()
maps_api_key = os.getenv('MAPS_API_KEY')
for id_sensor in range(1, last_sensor_id + 1):
    results = []
    for year in range(2022, current_year + 1):
        result = meet_je_stad_api_service.MeetJeStadAPIService().get_data(
            str(year) + '-01-01,00:00',
            str(year) + '-12-31,23:59',
    'sensors',
'json',
            str(id_sensor),
        False,
        40000)

        if result != []:
            for row in result:
                longitude = row[3]
                latitude = row[4]
                date = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d')
                if longitude is not None  and latitude is not None:
                    # sensor_utrecht[(year - start_year)] = 1
                    # if long_w < longitude < long_e and lat_s < latitude < lat_n:
                    #     response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng=' +
                    #                             str(latitude) + ',' + str(longitude) + '&key=' + maps_api_key)
                    #     if response.status_code != 200 or 'error_message' in response.json():
                    #         raise Exception(response.reason)
                    #     maps = response.json()['plus_code']['compound_code']
                    #     if maps.split(',')[0].split(' ')[1] == 'Utrecht':
                    #         sensor_utrecht[(year - start_year)] = 2
                    # break
                    test = 1
                results.append(list(row))

    os.makedirs('ids/' + str(id_sensor), exist_ok=True)
    file = open('ids/' + str(id_sensor) + "/out.csv", "w", newline='')
    csv.writer(file, quoting=csv.QUOTE_ALL).writerows(results)
    file.close()
