import requests
from dotenv import load_dotenv
import os
import csv
from research.utrecht_rectangle import UtrechtRectangle


rectangle = UtrechtRectangle()
load_dotenv()
maps_api_key = os.getenv('MAPS_API_KEY')
for latitude in reversed(range(int(rectangle.lat_s * rectangle.step_inverse),
                               int(rectangle.lat_n * rectangle.step_inverse) + 1)):
    results = [0] * (int(rectangle.long_e * rectangle.step_inverse) -
                     int(rectangle.long_w * rectangle.step_inverse) + 1)
    for longitude in range(int(rectangle.long_w * rectangle.step_inverse),
                           int(rectangle.long_e * rectangle.step_inverse) + 1):
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng=' +
                                     str(latitude / rectangle.step_inverse) + ',' +
                                str(longitude / rectangle.step_inverse) + '&key=' + maps_api_key)
        if response.status_code != 200 or 'error_message' in response.json():
             raise Exception(response.reason)
        maps = response.json()['plus_code']['compound_code']
        if maps.split(',')[0].split(' ')[1] == 'Utrecht':
           results[longitude - int(rectangle.long_e * rectangle.step_inverse)] = 1
    file = open(os.getcwd() + "/geocode.csv", "a", newline='')
    csv.writer(file).writerow(results)
    file.close()

