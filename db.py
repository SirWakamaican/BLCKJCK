# this file contains the functions to read and write balance info to the accompany save txt file money.txt
import sqlite3
from contextlib import closing

conn = None

def connect():
    global conn
    conn = sqlite3.connect("session_db.sqlite")
    conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

def create_session():
    c = conn.cursor()
    query = """
            CREATE TABLE IF NOT EXISTS "Session" (
                "sessionID" INTEGER, 
	            "startTime"	TEXT,
	            "startMoney"	REAL,
	            "stopTime"	TEXT,
	            "stopMoney"	REAL,
                PRIMARY KEY ("sessionID" AUTOINCREMENT)
            );
            """

    c.execute(query)
    conn.commit()
    try:
        session = get_last_session()
        if len(session) <= 1:
            pass

    except:
        query = """INSERT INTO Session (sessionID, startTime, startMoney, stopTime, stopMoney) VALUES (0, 'x', 199, 'y', 199);"""
        c.execute(query)
        conn.commit()


def get_last_session():
    query = '''SELECT * FROM Session ORDER BY sessionID DESC;'''
    c = conn.cursor()
    c.execute(query)
    return c.fetchone()

def add_session(s):
    query = '''
        INSERT INTO Session (startTime,startMoney,stopTime,stopMoney) VALUES (?, ?, ?, ?)
        '''
    c = conn.cursor()
    c.execute(query, (s.startTime, s.startMoney, s.stopTime, s.stopMoney))
    conn.commit()
