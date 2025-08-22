# Read data from KNMI dataplatform
import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse
from typing import Literal
import datetime
import csv


class KNMIDataplatformService:

    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv('API_KEY')

    # Request collection data (validated data, one value per day) from KNMI data platform
    # sample curl
    # in case of collection there's both the collection (Tg1/Tn1/Tx1/Rd1/EV24/wins50) and the parameter (temperature,station-temperature,station-number)
    # curl -X 'GET' \
    # 'https://api.dataplatform.knmi.nl/edr/v1/collections/Tg1/cube?f=CoverageJSON&bbox=5.17%2C52.09%2C5.18%2C52.1&z=0&datetime=2024-07-22T04%3A10%3A00Z%2F2024-07-23T04%3A10%3A00Z&parameter-name=station-temperature' \
    # -H 'accept: application/prs.coverage+json' \
    # -H 'Authorization: .env'
    def get_coll(self, t0: str, t1: str, coll: Literal['Tg1', 'Tn1', 'Tx1', 'Rd1', 'EV24', 'wins50'], format: Literal['csv', 'json']) -> list:
        # data validation
        # coll in c('Tx1','Tg1','Tn1')?
        # Tx1 max
        # Tg1 mean
        # Tn1 min
        # Rd1 precipitation
        # EV24 evaporation
        # wins50 wind

        if format not in ['csv', 'json']:
            raise Exception('Format must be csv or json.')

        if coll not in ['Tg1', 'Tn1', 'Tx1', 'Rd1', 'EV24', 'wins50']:
            raise ValueError('Coll must be Tg1, Tn1, Tx1, Rd1, EV24 or wins50.')

        if datetime.datetime.strptime(t1, "%Y-%m-%d") < datetime.datetime.strptime(t0, "%Y-%m-%d"):
            raise Exception('t1 must be later than t0.')

        # split URL in its parts
        uri_segments = urlparse('https://api.dataplatform.knmi.nl/edr/v1/collections/Tg1/cube?f=CoverageJSON&bbox=5.17%2C52.09%2C5.18%2C52.1&z=0&datetime=2024-07-22T04%3A10%3A00Z%2F2024-07-23T04%3A10%3A00Z&parameter-name=station-temperature')

        # merge collection into path
        uri_path = uri_segments.path.split('/')  # split path into list
        uri_path[4] = coll
        uri_path = '/'.join(uri_path)

        uri_segments = uri_segments._replace(path=uri_path)

        # set datetime in query string to start & end
        queries = uri_segments.query.split("&")
        query = ''
        for query_string in queries:
            if query_string.startswith('datetime='):
                query_string = 'datetime=' + self._to_interval(t0, t1)
            query += query_string + '&'
        uri_segments = uri_segments._replace(query=query[:-1])

        # Use urlunparse() to build URL
        uri = urlunparse(uri_segments)

        response = requests.get(uri, headers={"Authorization": self.api_key})

        if response.status_code != 200:
            raise Exception(response.reason)

        # read dates and temperatures from JSON
        dates = response.json()['domain']['axes']['t']['values']
        temps = response.json()['ranges']['station-temperature']['values']  # $station-temperature throws error 'temperature' not found

        # bind lists and transpose
        date_temp = list(zip(*(dates, temps)))

        if format == 'csv':
            with open('output/knmi/out.csv', 'w') as my_file:
                wr = csv.writer(my_file, quoting=csv.QUOTE_ALL)
                for row in date_temp:
                    wr.writerow(row)

            return []
        else:

            return date_temp

    # Request observation data (non-validated, one value every 10') from KNMI data platform
    # sample URL
    # https://api.dataplatform.knmi.nl/edr/v1/collections/observations/cube?f=CoverageJSON&bbox=5.17%2C52.09%2C5.18%2C52.1&z=0&datetime=2025-01-22T04%3A10%3A00Z%2F..&parameter-name=sq_10
    # def knmi_obs(self,t0: str,t1: str, param, daily: bool = False) -> list:
    #     # validate data
    #
    #     # split URL in its parts
    #     uri_segments = urlparse('https://api.dataplatform.knmi.nl/edr/v1/collections/observations/cube?f=CoverageJSON&bbox=5.17%2C52.09%2C5.18%2C52.1&z=0&datetime=2025-01-22T04%3A10%3A00Z%2F..&parameter-name=sq_10')
    #
    #     # set datetime in query string to start & end
    #     queries = uri_segments.query.split("&")
    #     query = ''
    #     for query_string in queries:
    #         if query_string.startswith('datetime='):
    #             query_string = 'datetime=' + self._to_interval(t0, t1)
    #         if query_string.startswith('parameter-name='):
    #             query_string = 'parameter-name=' + param
    #         query += query_string + '&'
    #     uri_segments = uri_segments._replace(query=query[:-1])
    #
    #     uri = urlunparse(uri_segments)
    #
    #     response = requests.get(uri, headers={"Authorization": self.api_key})
    #
    #     if response.status_code != 200:
    #         raise Exception(response.reason)

        # # read dates and temperatures from JSON
        # dates = response.json()['coverages'][0]['domain']['axes']['t']['values']
        # temps = response.json()['coverages'][0]['ranges']['station-temperature']['values']  # $station-temperature throws error 'temperature' not found
        #
        # # bind into list
        # date_temp = list(zip(*(dates, temps)))
        #
        # date_temp = list()
        #
        # return date_temp

    @staticmethod
    def _to_interval(t0: str, t1: str):
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
