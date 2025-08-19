import requests
from typing import Literal
import datetime


class MeetJeStadService:

    def get_data(self,
                 begin: str,
                 end: str,
                 type: Literal['sensors', 'flora', 'stories'],
                 format: Literal['csv', 'json'],
                 ids: str = 'Utrecht',
                 is_particulate_matter_only: bool = False,
                 limit: int = 100) -> list:

        date_begin = datetime.datetime.strptime(begin, "%Y-%m-%d,%H:%M")
        date_end = datetime.datetime.strptime(end, "%Y-%m-%d,%H:%M")
        if date_end  < date_begin:
            raise Exception('t1 must be later than t0.')

        if type not in ['sensors', 'flora', 'stories']:
            raise Exception('type must be sensors, flora or stories.')

        if format not in ['csv', 'json']:
            raise Exception('Format must be csv or json.')

        if ids == 'Utrecht':
            ids = '1'

        for id in ids.split(','):
            if len(id.split('-')) > 1:
                for id_underscore in id.split('-'):
                    if not id_underscore.isdigit():
                        raise Exception('Invalid IDs')
            else:
                if not id.isdigit():
                    raise Exception('Invalid IDs')

        uri = 'https://meetjestad.net/data/?type='
        uri += type + '&ids=' + ids + '&begin=' + date_begin.strftime('%Y-%m-%d,%H:%M') + '&end=' + date_end.strftime('%Y-%m-%d,%H:%M') + '&format=' + format + '&limit=' + str(limit)

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
        for row in response.json():
            dates.append(row['timestamp'])
            ids.append(row['id'])
            temps.append(row['temperature'])
            longitude.append(row['longitude'])
            latitude.append(row['latitude'])
            humidity.append(row['humidity'])
            supply.append(row['supply'])
            battery.append(row['battery'])

        # bind lists and transpose
        date_ids_temp = list(zip(*(dates, ids, temps, longitude, latitude, humidity, supply, battery)))

        return date_ids_temp
