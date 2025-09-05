# Read data from KNMI dataplatform
import os
import requests
from dotenv import load_dotenv
from typing import Literal
import datetime
import csv


class KNMIDataplatformAPIService:

    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv('KNMI_API_KEY')

    # Request collection data (validated data, one value per day) from KNMI data platform
    # sample curl
    # in case of collection there's both the collection (Tg1/Tn1/Tx1/Rd1/EV24/wins50) and the
    # parameter (temperature,station-temperature,station-number)
    # curl -X 'GET' \
    # 'https://api.dataplatform.knmi.nl/edr/v1/collections/Tg1/cube?
    # -H 'accept: application/prs.coverage+json' \
    # -H 'Authorization: .env'
    def get_coll(self, t0: str, t1: str, coll: Literal['Tg1', 'Tn1', 'Tx1', 'Rd1', 'EV24', 'wins50'],
                 format_output: Literal['csv', 'json']) -> list:
        # data validation
        # coll in c('Tx1','Tg1','Tn1')?
        # Tx1 max
        # Tg1 mean
        # Tn1 min
        # Rd1 precipitation
        # EV24 evaporation
        # wins50 wind

        if format_output not in ['csv', 'json']:
            raise Exception('Format must be csv or json.')

        if coll not in ['Tg1', 'Tn1', 'Tx1', 'Rd1', 'EV24', 'wins50']:
            raise ValueError('Coll must be Tg1, Tn1, Tx1, Rd1, EV24 or wins50.')

        if datetime.datetime.strptime(t1, "%Y-%m-%d") < datetime.datetime.strptime(t0, "%Y-%m-%d"):
            raise Exception('t1 must be later than t0.')

        # split URL in its parts
        uri = 'https://api.dataplatform.knmi.nl/edr/v1/collections/' + coll + '/cube?f=CoverageJSON'
        uri += '&bbox=5.17%2C52.09%2C5.18%2C52.1&z=0'
        uri += '&datetime=' + self._to_interval(t0, t1) + '&parameter-name=station-temperature'

        response = requests.get(uri, headers={"Authorization": self.api_key})

        if response.status_code != 200:
            raise Exception(response.reason)

        # read dates and temperatures from JSON
        dates = response.json()['domain']['axes']['t']['values']
        temps = response.json()['ranges']['station-temperature']['values']

        # bind lists and transpose
        date_temp = list(zip(*(dates, temps)))

        if format_output == 'csv':
            path = os.path.dirname(os.path.abspath(__file__))
            path.replace('\\vendor\\meetjestad', '')
            with open(path + '/output/knmi/' + coll + '-' + t0 + '-' + t1  +
                      '.csv', 'w', newline='') as my_file:
                wr = csv.writer(my_file)
                for row in date_temp:
                    wr.writerow(list(row))

            return []
        else:

            return date_temp

    def _to_interval(self, t0: str, t1: str):
        # t0 or t1 empty - replace with '..'
        # both empty - return error
        # (%2F)

        time_string = 'T00:00:00Z'
        slash = '/'

        if t0 == '' and t1 == '':
            raise Exception('Provide at least one date.')

        if t0 == '':
            t0 = '..'
            t1 = datetime.datetime.strptime(t1, "%Y-%m-%d").date()

            return t0 + t1.strftime('%Y-%m-%d') + time_string

        elif t1 == '':
            t1 = '..'
            t0 = datetime.datetime.strptime(t0, "%Y-%m-%d").date()

            return t0.strftime('%Y-%m-%d') + time_string + slash +  t1
        else:
            t0 = datetime.datetime.strptime(t0, "%Y-%m-%d").date()
            t1 = datetime.datetime.strptime(t1, "%Y-%m-%d").date()

        return t0.strftime('%Y-%m-%d') + time_string + slash + t1.strftime('%Y-%m-%d') + time_string
