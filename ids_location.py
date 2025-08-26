import meet_je_stad_api_service
from datetime import datetime
import csv
import requests
from dotenv import load_dotenv
import os


# Utrecht rectangle
lat_s = 52.05
lat_n = 52.13
long_w = 5.03
long_e= 5.19

last_sensor_id = 1100
current_year = datetime.now().year
load_dotenv()
maps_api_key = os.getenv('MAPS_API_KEY')
for id_sensor in range(1, last_sensor_id):
    sensor_utrecht = [0] * (current_year - 2016 + 1)
    for year in range(2016, current_year + 1):
        result = meet_je_stad_api_service.MeetJeStadAPIService().get_data(
            str(year) + '-01-01,00:00',
            str(year) + '-12-31,23:59',
    'sensors',
'json',
            str(id_sensor))

        if result != []:
            for row in result:
                longitude = row[3]
                latitude = row[4]
                if longitude is not None  and latitude is not None:
                    sensor_utrecht[(year - 2016)] = 1
                    if long_w < longitude < long_e and lat_s < latitude < lat_n:
                        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng=' +
                                                str(latitude) + ',' + str(longitude) + '&key=' + maps_api_key)
                        if response.status_code != 200 or 'error_message' in response.json():
                            raise Exception(response.reason)
                        maps = response.json()['plus_code']['compound_code']
                        if maps.split(',')[0].split(' ')[1] == 'Utrecht':
                            sensor_utrecht[(year - 2016)] = 2
                    break

    sensor_utrecht = [id_sensor] + sensor_utrecht
    file = open("out.csv", "a", newline='')
    csv.writer(file, quoting=csv.QUOTE_ALL).writerow(sensor_utrecht)
    file.close()
