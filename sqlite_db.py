import sqlite3
import datetime
import time


def get_time_str(a_time):
    return datetime.datetime.fromtimestamp(a_time).strftime('%yy_%mm_%dd_%H_%M_%S')


sqlite_file = 'data.sqlite'  # database for all sensors, contains 6 tables


def init_db():
    # Get a cursor object
    db = sqlite3.connect(sqlite_file)
    cursor = db.cursor()
    # cursor.execute('''
    # CREATE TABLE sensors_values(id INTEGER PRIMARY KEY AUTOINCREMENT , timestamp TEXT,
    # CH4 TEXT, LPG TEXT , CO2 TEXT, Dust TEXT, Temperature TEXT, Humidity TEXT, Lat TEXT, Long TEXT)
    # ''')

    cursor.execute('''
        CREATE TABLE sensor(id INTEGER PRIMARY KEY AUTOINCREMENT , timestamp TEXT, event TEXT, value TEXT, prio_class TEXT, prio_value TEXT,
        lat TEXT, alt TEXT, long TEXT)
    	''')

    db.commit()


def insert(ts, event, value, prio_class, prio_val, lat, alt, lng):
    '''

    :param ts:
    :param event:
    :param value:
    :param prio_class:
    :param prio_val:
    :param lat:
    :param alt:
    :param lng:
    :return:
    '''
    db = sqlite3.connect(sqlite_file)
    c = db.cursor()
    c.execute('''INSERT INTO sensor(timestamp, event, value, prio_class, prio_value, lat, alt, long)
    VALUES(?,?,?,?,?,?,?,?)''', (ts, event, value, prio_class, prio_val, lat, alt, lng))
    db.commit()


#init_db()
