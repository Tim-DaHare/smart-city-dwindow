import sqlite3
from sqlite3 import Error as SQLiteError
import db as db

def main():
    conn = db.create_connection(r"sensor_dataset.db")

    if conn is None:
        raise Exception("connection could not be created")

    with conn:
        create_dr_q = """CREATE TABLE IF NOT EXISTS data_readings (id integer PRIMARY KEY, measured_at text, temprature real, eco2 integer, tvoc integer); """

        db.create_table(conn, create_dr_q)

        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))
        db.insertDataReading(conn, (21.5, 37, 11))

if __name__ == '__main__':
    main()