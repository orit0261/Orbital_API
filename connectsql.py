import json
from config import connect
import csv
import datetime
import requests


# class for all tasks needs
class iss_path:
    URL_ADDRESS = "http://api.open-notify.org/iss-pass.json"

    def __init__(self):
        print('Create Connection...')
        self.db_connection, self.db_cursor = connect()

    def __del__(self):
        print('Del Connection...')
        self.db_cursor.close()
        self.db_connection.close()
        print('Finished Del Connection...')


    # orbitals details are send to api request and get response back
    def fill_json_to_tbl(self):

        with open('locations.json', 'r') as j:
            json_data = json.load(j)
            return [(self.get_response(item['name'], item['latitude'], item['longitude'], 50))
                    for item in json_data['locations']]

    # insert all data from locations.json to orbital_data_orit_naor table
    def get_response(self, p_city, p_lat, p_lon, p_n):

        params = {'lat': p_lat, 'lon': p_lon, 'n': p_n}
        response = requests.get(self.URL_ADDRESS, params=params)
        try:
            response_json = response.json()['response']
            data = [(p_city, response_json['duration'], datetime.datetime.fromtimestamp(int(response_json["risetime"])))
                    for response_json in response.json()['response']]
            self.db_cursor.executemany("INSERT INTO orbital_data_orit_naor(CITY,DURATION,RISETIME) VALUES (%s,%s,%s)",
                                       data)
            self.db_connection.commit()
        except Exception as e:
            print(e, flush=True)
            self.db_connection.rollback()
            self.db_cursor.close()
            self.db_connection.close()

    # convert stored procedure results to csv file
    def sql_to_csv(self):
        try:
            self.db_cursor.callproc('city_status_orit_naor')
            for result in self.db_cursor.stored_results():
                res1 = result.fetchall()
                column_names = [x[0] for x in result.description]

            response_jsons = res1
            fp = open('results.csv', 'w')
            myFile = csv.writer(fp, lineterminator='\n')
            myFile.writerow(column_names)
            myFile.writerows(response_jsons)
            fp.close()
        except Exception as e:
            print(e, flush=True)
            self.db_cursor.close()
            self.db_connection.close()

    def execute(self):
        print("Start fill table..")
        self.fill_json_to_tbl()
        print("Finished fill table..")

        print("Start create csv file..")
        self.sql_to_csv()
        print("csv file created")
