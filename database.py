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

    def shiftFromID(self, shiftId):

        # create a cursor
        cur = self._conn.cursor()

        shiftDate = datetime.date.fromisoformat(dateIn)
        QUERY_STRING = 'SELECT shift_info.shift_id, shift_info.date,' + \
            'shift_info.task_id, task_info.meal, task_info.task,' + \
            'task_info.start_time, task_info.end_time FROM shift_info,' + \
            'task_info WHERE shift_info.task_id = task_info.task_id AND ' + \
            'shift_info.shift_id = %s'
        cur.execute(QUERY_STRING, (shiftDate, task_id))
        
        row = cur.fetchone()
        shift = Shift(row[0], str(row[1]), row[2], row[3], row[4], row[5], row[6])
        cur.close()
        return shift

    def subOut(self, netid, dateIn, taskId):
        try:
            cur = self._conn.cursor()
            shiftDate = datetime.date.fromisoformat(dateIn)

            QUERY_STRING = 'SELECT shift_info.shift_id ' + \
                           'WHERE shift_info.task_id = %s ' + \
                           'AND shift_info.date = %s'
            cur.execute(QUERY_STRING, (taskId, shiftDate))
            row = cur.fetchone()
            shiftId = row[0]


            #maybe use -1 instead of NULL to indicate a sub needs to be filled?
            
            QUERY_STRING = 'INSERT INTO sub_requests(shift_id, sub_out_netid, sub_in_netid): ' + \
                           '(%s, %s, NULL)'
            cur.execute(QUERY_STRING, (shiftId, netid))
            cur.close()
            return true
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return false

    def subIn(self, netid, dateIn, taskId):
        try:
            cur = self._conn.cursor()
            shiftDate = datetime.date.fromisoformat(dateIn)

            QUERY_STRING = 'SELECT shift_info.shift_id, sub_requests_sub_out_netid ' + \
                           'WHERE shift_info.task_id = %s ' + \
                           'AND shift_info.date = %s ' + \
                           'AND sub_requests.sub_in_netid = NULL'
            cur.execute(QUERY_STRING, (taskId, shiftDate))
            row = cur.fetchone()
            shiftId = row[0]
            otherSubId = row[1]

            #need to figure out a way to only apply this once
            QUERY_STRING = 'UPDATE sub_requests ' + \
                           'SET sub_in_netid = %s' + \
                           'WHERE sub_requests.shift_id = %s ' + \
                           'AND sub_requests.sub_out_netid = %s'
            cur.execute(QUERY_STRING, (netid, shiftid, otherSubId))
            cur.close()
            return true
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return false

    #currently returns a list of shift objects
    def allSubNeeded(self):
        try:
            cur = self._conn.cursor()
            shiftDate = datetime.date.fromisoformat(dateIn)
            QUERY_STRING = 'SELECT sub_requests.shift_id' + \
                           'WHERE sub_requests.sub_out_netid = NULL'
            cur.execute(QUERY_STRING, (netid, shiftid, otherSubId))
            row = cur.fetchone()
            shiftsNeeded = []
            while row is not None:
                shiftsNeeded.append(row[0])

            cur.close()

            shiftObjects = []
            for shift in shiftsNeeded:
                shiftObject = shiftFromId(self, shift)
                shiftObjects.append(shiftObject)
            return shiftObjects
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return false

    def allSubsForDate(self, date):
        subsList = allSubNeeded(self)
        dateSubs = []
        for sub in subsList:
            if sub.getDate(sub) is date:
                dateSubs.append(sub)
        return dateSubs

    def regShifts(self, netid):
        try:
            cur = self._conn.cursor()
            QUERY_STRING = 'SELECT regular_shifts.task_id, regular_shifts.dotw ' + \
                           'WHERE regular_shifts.netid = %s'
            cur.execute(QUERY_STRING, (netid, shiftid, otherSubId))
            row = cur.fetchone()
            regShiftInfo = []
            while row is not None:
                regShiftInfo.append([row[0], row[1]])
            cur.close()

            regShiftObjects = []
            for info in regShiftInfo:
                regShiftObject = shiftDetails(self, info[0], info[1])
                regShiftObjects.append(regShiftObject)
            return regShiftObjects
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return false
        

#-----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
    database = Database()
    database.connect()
    date = "2020-03-23"
    task_id = 1
    database.shiftDetails(date, task_id)
    database.disconnect()
