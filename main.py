import sqlite3
from sqlite3 import Error as SQLiteError

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except SQLiteError as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except SQLiteError as e:
        print(e)

def insertDataReading(conn, data):
    sql = '''INSERT INTO data_readings (measured_at, temprature, air_quality)
              VALUES(datetime('now'), ?, ?)'''

    cur = conn.cursor()
    cur.execute(sql, data)
    
    conn.commit()

    return cur.lastrowid

def main():
    conn = create_connection("sensor_dataset.db")

    if conn is None:
        raise Exception("connection could not be created")

    with conn:
        create_dr_q = """CREATE TABLE IF NOT EXISTS data_readings (id integer PRIMARY KEY, measured_at text, temprature real, air_quality real); """

        create_table(conn, create_dr_q)

        insertDataReading(conn, (20, 37.36))

if __name__ == '__main__':
    main()