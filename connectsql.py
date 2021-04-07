import csv
import datetime
import itertools
import json

import mysql.connector
import requests

db_connection = mysql.connector.connect(
    host="104.197.7.195",
    user="interview_user",
    passwd="zz!!@@202111558843",
    database="interview")

print(db_connection)
# creating database_cursor to perform SQL operation
db_cursor = db_connection.cursor()

# # Query for creating table
# ArtistTableSql = """CREATE TABLE orbital_data_orit_naor(
# ID INT(20) PRIMARY KEY AUTO_INCREMENT,
# CITY  CHAR(100) NOT NULL,
# DURATION INT,
# RISETIME datetime)"""
# db_cursor.execute(ArtistTableSql)
# db_connection.close()

# student_sql_query = "INSERT INTO orbital_data_orit_naor(city,duration) VALUES('ash',01)"
# db_cursor.execute(student_sql_query)

# student_sql_query = "INSERT INTO student(id,name) VALUES(01, 'John')"
# employee_sql_query = " INSERT INTO employee (id, name, salary) VALUES (01, 'John', 10000)"
# #Execute cursor and pass query as well as student data
# db_cursor.execute(student_sql_query)
# #Execute cursor and pass query of employee and data of employee
# 	db_cursor.execute(employee_sql_query)
# db_connection.commit()
# print(db_cursor.rowcount, "Record Inserted")


# queries for retrievint all rows
select_sql = "Select id,city,duration,CAST(risetime AS char) as risktime from orbital_data_orit_naor;"
db_cursor.execute(select_sql)

rows = db_cursor.fetchall()
column_names = [i[0] for i in db_cursor.description]
fp = open('test.csv', 'w')
myFile = csv.writer(fp, lineterminator='\n')
myFile.writerow(column_names)
myFile.writerows(rows)
fp.close()

# commiting the connection then closing it.
db_connection.commit()

params = {'lat': 32.8000, 'lon': 34.9833, 'n': 50}
response = requests.get("http://api.open-notify.org/iss-pass.json", params=params)
row = response.json()['response']
try:
    data = [('city',row['duration'],datetime.datetime.fromtimestamp(int(row["risetime"]))) for row in response.json()['response']]
    db_cursor.executemany("INSERT INTO orbital_data_orit_naor(CITY,DURATION,RISETIME) VALUES (%s,%s,%s)", data)
    db_connection.commit()
except Exception as e:
    print(e, flush=True)
    db_connection.rollback()
finally:
  db_connection.close()
# all = response.json()['response'] # No need to parse this, unless you want to check it's valid
# db_cursor.execute('insert into t select * from json_populate_recordset(null::t, %s)', [all])
