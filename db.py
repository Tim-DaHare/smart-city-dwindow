import sqlite3
from sqlite3 import Error as SQLiteError

def getLastReadings(conn, num):
    cur = conn.cursor()
    cur.execute("SELECT * FROM data_readings ORDER BY datetime(measured_at) ASC LIMIT " + num)

    rows = cur.fetchall()

    return rows

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
    sql = '''INSERT INTO data_readings (measured_at, temprature, eco2, tvoc)
              VALUES(datetime('now'), ?, ?, ?)'''

    cur = conn.cursor()
    cur.execute(sql, data)
    
    conn.commit()

    return cur.lastrowid