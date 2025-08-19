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

        if format == 'csv':
            file = open("output/out.csv", "wb")
            file.write(response.content)
            file.close()

            return []

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
        dates_list = list(zip(*(dates, ids, temps, longitude, latitude, humidity, supply, battery, firmware_version, pm25, pm10)))

        return dates_list
