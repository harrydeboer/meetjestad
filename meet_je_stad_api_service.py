import os
import requests
from typing import Literal
import datetime
import csv


class MeetJeStadAPIService:

    def __init__(self):
        self.row_keys = [
            'timestamp',
            'id',
            'row',
            'temperature',
            'longitude',
            'latitude',
            'humidity',
            'supply',
            'battery',
            'firmware_version',
            'pm2.5',
            'pm10',
            'lux',
            'extra'
        ]

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
        results = []
        for row in response.json():
            result = []
            for key in row:
                if key not in self.row_keys:
                    raise Exception('Invalid key ' + key + ' in row.')
            for key in self.row_keys:
                if key == 'row':
                    continue
                if key in row:
                    result.append(row[key])
                else:
                    result.append(None)
            results.append(result)

        results.reverse()
        results.sort(key=lambda x: x[1])

        results = self._sanitize(results)

        if format_output == 'csv':
            file = open(os.path.dirname(os.path.abspath(__file__)) + "/output/meetjestad/out.csv", "w", newline='')
            csv.writer(file).writerows(results)
            file.close()

            return []
        else:
            return results

    def _sanitize(self, results: list) -> list:

        result = []
        for row in results:
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
            result += [row_return]

        return result
