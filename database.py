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
    
    def connect(self):      
        """ Connect to the PostgreSQL database server """
        self._conn = None
        try:    
            print('Connecting to the PostgreSQL database...')

            # DATABASE_URL = os.environ['DATABASE_URL']
            DATABASE_URL = "postgres://qxcsbcdzxdftyo:6034a3745c758509ba1c815e3507925ae54fbef58258edea409b7d0958fe0002@ec2-34-204-22-76.compute-1.amazonaws.com:5432/d6c9olgrm57o3s"
            self._conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        except (Exception, psycopg2.DatabaseError) as error:
            print('Error: ' + str(error))
                
    def disconnect(self):
        self._conn.close()
        print('Database connection closed.')

    def shiftDetails(self, dateIn, task_id):

        # create a cursor
        cur = self._conn.cursor()

        shiftDate = datetime.date.fromisoformat(dateIn)
        QUERY_STRING = 'SELECT shift_info.shift_id, shift_info.date,' + \
            'shift_info.task_id, task_info.meal, task_info.task,' + \
            'task_info.start_time, task_info.end_time, shift_info.cur_people FROM shift_info,' + \
            'task_info WHERE shift_info.task_id = task_info.task_id AND ' + \
            'shift_info.date = %s AND task_info.task_id = %s'
        cur.execute(QUERY_STRING, (shiftDate, task_id))
        
        row = cur.fetchone()
        shift = Shift(row[0], str(row[1]), row[2], row[3], row[4], row[5], row[6], row[7])
        cur.close()
        return shift

    def shiftFromID(self, shiftId):

        # create a cursor
        cur = self._conn.cursor()

        QUERY_STRING = 'SELECT shift_info.shift_id, shift_info.date,' + \
            'shift_info.task_id, task_info.meal, task_info.task,' + \
            'task_info.start_time, task_info.end_time, shift_info.cur_people FROM shift_info,' + \
            'task_info WHERE shift_info.task_id = task_info.task_id AND ' + \
            'shift_info.shift_id = %s'
        cur.execute(QUERY_STRING, (shiftId,))
        
        row = cur.fetchone()
        shift = Shift(row[0], str(row[1]), row[2], row[3], row[4], row[5], row[6], row[7])
        cur.close()
        return shift

    def subOut(self, netid, dateIn, taskId):
        try:
            cur = self._conn.cursor()
            shiftDate = datetime.date.fromisoformat(dateIn)

            QUERY_STRING = 'SELECT shift_info.shift_id FROM shift_info ' + \
                           'WHERE shift_info.task_id = %s ' + \
                           'AND shift_info.date = %s'
            cur.execute(QUERY_STRING, (taskId, shiftDate))
            row = cur.fetchone()
            shiftId = row[0]
            
            QUERY_STRING = 'INSERT INTO sub_requests (shift_id, sub_out_netid, sub_in_netid) VALUES ' + \
                           '(%s, %s, %s);'
            cur.execute(QUERY_STRING, (shiftId, netid, 'needed'))
            self._conn.commit()
            print('Sub request is committed.')
            cur.close()
            return True

        except (Exception, psycopg2.DatabaseError) as error:
            self._conn.rollback()
            print('Sub request rolled back.')
            cur.close()
            print(error)
            return False

    def subIn(self, netid, dateIn, taskId, subOutId):
        try:
            cur = self._conn.cursor()
            shiftDate = datetime.date.fromisoformat(dateIn)

            QUERY_STRING = 'SELECT shift_info.shift_id, sub_requests.sub_out_netid ' + \
                            'FROM shift_info, sub_requests ' + \
                           'WHERE shift_info.task_id = %s ' + \
                           'AND shift_info.date = %s ' + \
                            'AND sub_requests.sub_out_netid = %s ' + \
                           'AND sub_requests.sub_in_netid = %s'
            cur.execute(QUERY_STRING, (taskId, shiftDate, subOutId, 'needed'))
            row = cur.fetchone()
            shiftId = row[0]

            #need to figure out a way to only apply this once
            QUERY_STRING = 'UPDATE sub_requests ' + \
                           'SET sub_in_netid = %s' + \
                           'WHERE sub_requests.shift_id = %s ' + \
                           'AND sub_requests.sub_out_netid = %s'
            cur.execute(QUERY_STRING, (netid, shiftId, subOutId))
            self._conn.commit()
            print('Sub pick-up is committed.')
            cur.close()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            self._conn.rollback()
            print('Sub pick-up rolled back.')
            cur.close()
            print(error)
            return False

    #currently returns a list of shift objects
    def allSubNeeded(self):
        try:
            cur = self._conn.cursor()

            QUERY_STRING = 'SELECT sub_requests.shift_id FROM sub_requests ' + \
                           'WHERE sub_requests.sub_in_netid = %s'
            cur.execute(QUERY_STRING, ('needed',))

            row = cur.fetchone()
            shiftsNeeded = []
            while row is not None:
                shiftsNeeded.append(row[0])
                row = cur.fetchone()
            cur.close()

            shiftObjects = []
            for shift in shiftsNeeded:
                shiftObject = self.shiftFromID(shift)
                shiftObjects.append(shiftObject)
            return shiftObjects
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return []

    def allSubsForDate(self, date):
        subsList = self.allSubNeeded()

        dateSubs = []
        for sub in subsList:
            if (sub.getDate() == date):
                dateSubs.append(sub)
        return dateSubs

    def regularShifts(self, netid):
        try:
            cur = self._conn.cursor()
            QUERY_STRING = 'SELECT regular_shifts.task_id, regular_shifts.dotw ' + \
                            'FROM regular_shifts ' + \
                           'WHERE regular_shifts.netid = %s'
            cur.execute(QUERY_STRING, (netid, ))

            row = cur.fetchone()
            regShiftInfo = []
            while row is not None:
                regShiftInfo.append([row[0], row[1]])
                row = cur.fetchone()
            cur.close()

            return regShiftInfo
            # Code below is not going to work because dotw is not same as date
            '''
            regShiftObjects = []
            for info in regShiftInfo:
                regShiftObject = self.shiftDetails(info[0], info[1])
                regShiftObjects.append(regShiftObject)
            return regShiftObjects
            '''
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
        

#-----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
    database = Database()
    database.connect()
    
    # Test shiftDetails *********** WORKS
    date = "2020-03-23"
    task_id = 1
    shift = database.shiftDetails(date, task_id)
    print(shift)
    
    # Test subOut ************* WORKS
    netid_out = 'trt2'
    sub_in_success = database.subOut(netid_out, date, task_id)
    print(sub_in_success)

    # Test subIn ************* WORKS
    netid_in = 'ortaoglu'
    netid_out = 'trt2'
    sub_out_success = database.subIn(netid_in, date, task_id, netid_out)
    print(sub_out_success)
    
    # Test allSubNeeded *********** WORKS
    subNeededShifts = database.allSubNeeded()
    print()
    print('All Sub Needed Shifts: ')
    for shift in subNeededShifts:
        print(shift)

    # Test allSubsForData *********** WORKS
    subNeededShiftsForDate = database.allSubsForDate(date)
    print()
    print('All Sub Needed Shifts for 2020-03-23: ')
    for shift in subNeededShiftsForDate:
        print(shift)

    # Test regularShifts *********** WORKS
    netid = 'yujl'
    regShifts = database.regularShifts(netid)
    print()
    print('Regular shifts for yujl: ')
    for i in range(len(regShifts)):
        print(str(regShifts[i][0]) + ' ' + str(regShifts[i][1]))

    database.disconnect()

    

