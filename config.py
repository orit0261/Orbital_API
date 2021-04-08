import configparser
from configparser import ConfigParser

import mysql
from mysql.connector import MySQLConnection, Error


def read_db_config(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db

def connect():
    """ Connect to MySQL database """
    db_config = read_db_config()
    db_connection = None
    try:
        db_connection = MySQLConnection(**db_config)
        if db_connection.is_connected():
            db_connection.connect()
            print('Connected to MySQL database')

    except Error as e:
        print(e)

    finally:
        # if db_connection is not None and db_connection.is_connected():
        #     db_connection.close()
        return db_connection, db_connection.cursor()

