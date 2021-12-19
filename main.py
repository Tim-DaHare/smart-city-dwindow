import sqlite3
import time
import random
from sqlite3 import Error as SQLiteError
import db as db

measure_interval = 0.3

def measure_data():
    return 26.1, 30, 22

def shouldWindowOpen(celcius, eco2, tvoc):
    rand = random.random()
    return rand < 0.5

def main():
    conn = db.create_connection(r"sensor_dataset.db")

    if conn is None:
        raise Exception("connection could not be created")

    with conn:
        create_dr_q = """CREATE TABLE IF NOT EXISTS data_readings (id integer PRIMARY KEY, measured_at text, temprature real, eco2 integer, tvoc integer); """
        db.create_table(conn, create_dr_q)

    # Calibrate
    # ...
    
    while True:
        time.sleep(measure_interval)
        celcius, eco2, tvoc = measure_data()

        db.insertDataReading(conn, (celcius, eco2, tvoc))

        open_window = shouldWindowOpen(celcius, eco2, tvoc)





if __name__ == '__main__':
    main()