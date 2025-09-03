import meet_je_stad_api_service
import csv
import os
import datetime


last_sensor_id = 1100
start_year = 2022
current_year = datetime.datetime.now().year
for id_sensor in range(1, last_sensor_id + 1):
    results = []
    for year in range(2022, current_year + 1):
        # Including summer
        if year == current_year:
            end_date = str(year) + '-08-31,23:59'
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

        if result != []:
            for row in result:
                results.append(list(row))

    os.makedirs(os.getcwd() + '/ids/' + str(id_sensor), exist_ok=True)
    file = open(os.getcwd() + '/ids/' + str(id_sensor) + "/out.csv", "w", newline='')
    csv.writer(file,).writerows(results)
    file.close()
