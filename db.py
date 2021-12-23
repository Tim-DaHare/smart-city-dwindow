import sqlite3
from sqlite3 import Error as SQLiteError

def getLastReadings(conn, num):
    cur = conn.cursor()
    cur.execute("SELECT * FROM data_readings ORDER BY datetime(measured_at) ASC LIMIT " + str(num))

    rows = cur.fetchall()

    return rows

def insertDataReading(conn, data):
    # temprature real, eco2 integer, tvoc integer, precipitation_chance integer, window_open tinyint
    sql = '''INSERT INTO data_readings (measured_at, temprature, eco2, tvoc, precipitation_chance, window_open)
              VALUES(datetime('now'), ?, ?, ?, ?, ?)'''

    cur = conn.cursor()
    cur.execute(sql, data)
    
    conn.commit()

    return cur.lastrowid

def setUserConfig(conn, data):
    cur = conn.cursor()

    cur.execute("UPDATE user_config SET eco2_threshold = ?, temp_threshold = ?", data)
    conn.commit()


def getUserConfig(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_config")

    return cur.fetchone()

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