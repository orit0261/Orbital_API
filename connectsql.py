import json

from config import connect
import csv
import datetime
import requests


def fill_json_to_tbl():
    with open('locations.json', 'r') as j:
        json_data = json.load(j)
        return [(get_response(item['name'], item['latitude'], item['longitude'], 50)) for item in
                json_data['locations']]


def get_response(p_city, p_lat, p_lon, p_n):
    db_connection, db_cursor = connect()
    params = {'lat': p_lat, 'lon': p_lon, 'n': p_n}
    response = requests.get("http://api.open-notify.org/iss-pass.json", params=params)
    try:
        response_json = response.json()['response']
        data = [(p_city, response_json['duration'], datetime.datetime.fromtimestamp(int(response_json["risetime"])))
                for response_json in response.json()['response']]
        db_cursor.executemany("INSERT INTO orbital_data_orit_naor(CITY,DURATION,RISETIME) VALUES (%s,%s,%s)", data)
        db_connection.commit()
    except Exception as e:
        print(e, flush=True)
        db_connection.rollback()
    finally:
        db_cursor.close()
        db_connection.close()


def sql_to_csv():
    db_connection, db_cursor = connect()
    try:
        db_cursor.callproc('city_status_orit_naor')
        for result in db_cursor.stored_results():
            res1=result.fetchall()
            column_names = [x[0] for x in result.description]

        response_jsons = res1
        fp = open('results.csv', 'w')
        myFile = csv.writer(fp, lineterminator='\n')
        myFile.writerow(column_names)
        myFile.writerows(response_jsons)
        fp.close()
    except Exception as e:
        print(e, flush=True)
    finally:
        db_cursor.close()
        db_connection.close()


sql_to_csv()