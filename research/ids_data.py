import meet_je_stad_api_service
import csv
import os
import datetime
from dotenv import load_dotenv


load_dotenv()
last_sensor_id = int(os.getenv('LAST_SENSOR_ID'))
start_date = datetime.datetime.strptime((os.getenv('START_DATE')),"%Y-%m-%d,%H:%M").year
end_year = datetime.datetime.strptime((os.getenv('END_DATE')),"%Y-%m-%d,%H:%M").year
quarter = os.getenv('QUARTER')
for id_sensor in range(1, last_sensor_id + 1):
    results = []
    for year in range(2022, end_year + 1):
        # Including summer
        if year == end_year:
            if quarter == '1':
                if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                    end_date = str(year) + '-02-29,22:59'
                else:
                    end_date = str(year) + '-02-28,22:59'
            elif quarter == '2':
                end_date = str(year) + '-05-31,21:59'
            elif quarter == '3':
                end_date = str(year) + '-08-31,21:59'
            elif quarter == '4':
                end_date = str(year) + '-11-30,22:59'
            else:
                end_date = os.getenv('END_DATE')
        else:
            end_date = str(year) + '-12-31,23:59'
        result = meet_je_stad_api_service.MeetJeStadAPIService().get_data(
            str(year) + '-01-01,00:00',
            end_date,
            'sensors',
            'json',
            str(id_sensor),
            False,
            40000)

        if result != list():
            for row in result:
                results.append(list(row))

    os.makedirs(os.getcwd() + '/ids/' + str(id_sensor), exist_ok=True)
    file = open(os.getcwd() + '/ids/' + str(id_sensor) + "/out.csv", "w", newline='')
    csv.writer(file,).writerows(results)
    file.close()
