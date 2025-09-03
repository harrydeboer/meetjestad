import requests
from dotenv import load_dotenv
import os
import csv


# Utrecht rectangle
lat_s = 52.03
lat_n = 52.14
long_w = 4.98
long_e = 5.19

step = 500
load_dotenv()
maps_api_key = os.getenv('MAPS_API_KEY')
for latitude in reversed(range(int(lat_s * step), int(lat_n * step) + 1)):
    results = [0] * (int(long_e * step) - int(long_w * step) + 1)
    for longitude in range(int(long_w * step), int(long_e * step) + 1):
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng=' +
                                     str(latitude / step) + ',' + str(longitude / step) + '&key=' + maps_api_key)
        if response.status_code != 200 or 'error_message' in response.json():
             raise Exception(response.reason)
        maps = response.json()['plus_code']['compound_code']
        if maps.split(',')[0].split(' ')[1] == 'Utrecht':
           results[longitude - int(long_e * step)] = 1
    file = open(os.getcwd() + "/geocode.csv", "a", newline='')
    csv.writer(file).writerow(results)
    file.close()

