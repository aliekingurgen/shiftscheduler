#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sqlite3 import connect
from sys import stderr
# from os import path, environ
import os
from shift import Shift

import psycopg2
import datetime
# from config import config
from configparser import ConfigParser

#-----------------------------------------------------------------------

class Database:
    
    def __init__(self):
        self._conn = None

    def config(self, filename='database.ini', section='postgresql'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)
    
        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    
        return db

    def connect(self):      
        """ Connect to the PostgreSQL database server """
        self._conn = None
        try:
            # read connection parameters
            # params = self.config()
    
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            DATABASE_URL = os.environ['DATABASE_URL']

            self._conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            # self._conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
                
                    
    def disconnect(self):
        self._conn.close()
        print('Database connection closed.')

    def shiftDetails(self, dateIn, task_id):

        # create a cursor
        cur = self._conn.cursor()

        shiftDate = datetime.date.fromisoformat(dateIn)
        QUERY_STRING = 'SELECT shift_info.shift_id, shift_info.date,' + \
            'shift_info.task_id, task_info.meal, task_info.task,' + \
            'task_info.start_time, task_info.end_time FROM shift_info,' + \
            'task_info WHERE shift_info.task_id = task_info.task_id AND ' + \
            'shift_info.date = %s AND task_info.task_id = %s'
        cur.execute(QUERY_STRING, (shiftDate, task_id))
        
        row = cur.fetchone()
        shift = Shift(row[0], str(row[1]), row[2], row[3], row[4], row[5], row[6])
        cur.close()
        return shift

#-----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
    database = Database()
    database.connect()
    date = "2020-03-23"
    task_id = 1
    database.shiftDetails(date, task_id)
    database.disconnect()
