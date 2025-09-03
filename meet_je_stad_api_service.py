import os

import requests
from typing import Literal
import datetime
import csv


class MeetJeStadAPIService:

    def get_data(self,
                 begin: str,
                 end: str,
                 type_api: Literal['sensors', 'flora', 'stories'],
                 format_output: Literal['csv', 'json'],
                 ids: str = 'Utrecht',
                 is_particulate_matter_only: bool = False,
                 limit: int = 100,
                 is_active_only: bool = True) -> list:

        date_begin = datetime.datetime.strptime(begin, "%Y-%m-%d,%H:%M")
        date_end = datetime.datetime.strptime(end, "%Y-%m-%d,%H:%M")
        if date_end < date_begin:
            raise Exception('t1 must be later than t0.')

        if type_api not in ['sensors', 'flora', 'stories']:
            raise Exception('type must be sensors, flora or stories.')

        if format_output not in ['csv', 'json']:
            raise Exception('Format must be csv or json.')

        if ids == 'Utrecht':
            ids = ''
            with open(os.path.dirname(os.path.abspath(__file__)) + '/utrecht.csv') as csvfile:
                reader = csv.reader(csvfile)
                for index, row in enumerate(reader):
                    if index == 0:
                        continue
                    if is_active_only and row[2] != '':
                        continue
                    if is_particulate_matter_only and row[5] == '0':
                        continue
                    ids += row[0] + ','
                ids = ids[:-1]
        else:
            for id_sensor in ids.split(','):
                if len(id_sensor.split('-')) > 1:
                    for id_underscore in id_sensor.split('-'):
                        if not id_underscore.isdigit():
                            raise Exception('Invalid IDs')
                else:
                    if not id_sensor.isdigit():
                        raise Exception('Invalid IDs')

        uri = 'https://meetjestad.net/data/?type='
        uri += (type_api + '&ids=' + ids + '&begin=' + date_begin.strftime('%Y-%m-%d,%H:%M') + '&end=' +
                date_end.strftime('%Y-%m-%d,%H:%M') + '&format=json&limit=' + str(limit))

        response = requests.get(uri)

        if response.status_code != 200:
            raise Exception(response.reason)

        # read from JSON
        dates = []
        ids = []
        temps = []
        longitude = []
        latitude = []
        humidity = []
        supply = []
        battery = []
        firmware_version = []
        pm25 = []
        pm10 = []
        for row in response.json():
            dates.append(row['timestamp'])
            ids.append(row['id'])
            if 'temps' in row:
                temps.append(row['temps'])
            else:
                temps.append(None)
            if 'longitude' in row:
                longitude.append(row['longitude'])
            else:
                longitude.append(None)
            if 'latitude' in row:
                latitude.append(row['latitude'])
            else:
                latitude.append(None)
            if 'humidity' in row:
                humidity.append(row['humidity'])
            else:
                humidity.append(None)
            if 'supply' in row:
                supply.append(row['supply'])
            else:
                supply.append(None)
            if 'battery' in row:
                battery.append(row['battery'])
            else:
                battery.append(None)
            if 'firmware_version' in row:
                firmware_version.append(row['firmware_version'])
            else:
                firmware_version.append(None)
            if 'pm2.5' in row:
                pm25.append(row['pm2.5'])
            else:
                pm25.append(None)
            if 'pm10' in row:
                pm10.append(row['pm10'])
            else:
                pm10.append(None)

        # bind lists and transpose
        dates_list = list(zip(*(dates, ids, temps, longitude, latitude, humidity,
                                supply, battery, firmware_version, pm25, pm10)))

        dates_list.reverse()
        dates_list.sort(key=lambda x: x[1])

        dates_list = self._sanitize(dates_list)

        if format_output == 'csv':
            file = open(os.path.dirname(os.path.abspath(__file__)) + "/output/meetjestad/out.csv", "w", newline='')
            csv.writer(file).writerows(dates_list)
            file.close()

            return []
        else:
            return dates_list

    def _sanitize(self, dates_list: list) -> list:

        result = []
        for row in dates_list:
            row_return = list(row)
            if row[2] is not None:
                if row[2] < -25 or row[2] > 70:
                    row_return[2] = None
            if row[9] is not None:
                if row[9] < 0 or row[9] > 250:
                    row_return[9] = None
            if row[10] is not None:
                if row[10] < 0 or row[10] > 250:
                    row_return[10] = None
            result += [row]

        return result
