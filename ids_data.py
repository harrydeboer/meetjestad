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
        result = meet_je_stad_api_service.MeetJeStadAPIService().get_data(
            str(year) + '-01-01,00:00',
            str(year) + '-12-31,23:59',
    'sensors',
'json',
            str(id_sensor),
        False,
        40000)

        if result != []:
            result.reverse()
            for row in result:
                results.append(list(row))

    os.makedirs('ids/' + str(id_sensor), exist_ok=True)
    file = open('ids/' + str(id_sensor) + "/out.csv", "w", newline='')
    csv.writer(file, quoting=csv.QUOTE_ALL).writerows(results)
    file.close()
