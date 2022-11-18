import os
import sys
import argparse
import mysql.connector as db
from dotenv import load_dotenv

load_dotenv()
username = os.getenv('DB_USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
db_name = os.getenv('DATABASE')

def get_db(autocommit=False, dict_cursor=False):
    try:
        conn = db.connect(
            host=host,
            db=db_name,
            user=username,
            password=password
        )
        conn.autocommit = autocommit

        cur = conn.cursor(dictionary=dict_cursor)

        return conn, cur

    except db.Error as e:
        print("###\t ", e)
        return None