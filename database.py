#!/usr/bin/env python

# -----------------------------------------------------------------------
# database.py
# Author: Bob Dondero
# -----------------------------------------------------------------------

from sqlite3 import connect
from sys import stderr
# from os import path, environ
import os
from shift import Shift
from employee import Employee

import psycopg2
import datetime
# from config import config
from configparser import ConfigParser


# -----------------------------------------------------------------------

class Database:

    def _init_(self):
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

        try:
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
        except (Exception, psycopg2.DatabaseError) as error:
            cur.close()
            print(error)

    def shiftFromID(self, shiftId):

        try:
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
        except (Exception, psycopg2.DatabaseError) as error:
            cur.close()
            print(error)

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

            QUERY_STRING = 'SELECT sub_requests.shift_id FROM sub_requests ' + \
                           'WHERE sub_requests.sub_in_netid = %s ' + \
                           'AND sub_requests.shift_id = %s'
            cur.execute(QUERY_STRING, (netid, shiftId))
            row = cur.fetchone()
            if row is not None:
                QUERY_STRING = 'UPDATE sub_requests SET sub_in_netid = %s WHERE ' + \
                               'sub_requests.sub_in_netid = %s AND sub_requests.shift_id = %s'
                cur.execute(QUERY_STRING, ('needed', netid, shiftId))
                self._conn.commit()
                print('Sub request is committed.')
                cur.close()
                return True

            else:
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

    def subIn(self, netid, dateIn, taskId):
        try:
            cur = self._conn.cursor()
            shiftDate = datetime.date.fromisoformat(dateIn)

            QUERY_STRING = 'SELECT shift_info.shift_id, sub_requests.sub_out_netid ' + \
                           'FROM shift_info, sub_requests ' + \
                           'WHERE shift_info.task_id = %s ' + \
                           'AND shift_info.date = %s ' + \
                           'AND shift_info.shift_id = sub_requests.shift_id AND sub_requests.sub_in_netid = %s'
            cur.execute(QUERY_STRING, (taskId, shiftDate, 'needed'))
            row = cur.fetchone()
            shiftId = row[0]
            otherNetid = row[1]

            if otherNetid == netid:
                QUERY_STRING = 'DELETE FROM sub_requests WHERE shift_id = %s AND sub_out_netid = %s'
                cur.execute(QUERY_STRING, (shiftId, netid))
                self._conn.commit()
                print('Sub pick-up is committed.')
                cur.close()
                return True

            else:
                # need to figure out a way to only apply this once
                QUERY_STRING = 'UPDATE sub_requests ' + \
                            'SET sub_in_netid = %s' + \
                            'WHERE sub_requests.shift_id = %s ' + \
                            'AND sub_requests.sub_out_netid = %s'
                cur.execute(QUERY_STRING, (netid, shiftId, otherNetid))
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

    # currently returns a list of shift objects
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

    def allSubsForWeek(self, date):
        subsList = self.allSubNeeded()

        if datetime.date.fromisoformat(date).weekday() != 0:
            print("Given date is not a Monday.")
            return -1

        monday = datetime.date.fromisoformat(date)
        tuesday = monday + datetime.timedelta(days=1)
        wednesday = tuesday + datetime.timedelta(days=1)
        thursday = wednesday + datetime.timedelta(days=1)
        friday = thursday + datetime.timedelta(days=1)
        saturday = friday + datetime.timedelta(days=1)
        sunday = saturday + datetime.timedelta(days=1)
        week = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]

        weekFormatted = []
        for day in week:
            dayFormatted = day.isoformat()
            weekFormatted.append(dayFormatted)

        retSubs = []
        for sub in subsList:
            if (sub.getDate() in weekFormatted):
                retSub = str(datetime.date.fromisoformat(sub.getDate()).weekday()) + '-' + sub.getTaskID()
                retSubs.append(retSub)

        return retSubs

    def regularShifts(self, netid):
        try:
            def convertDay(dayString):
                if (dayString == 'monday'): return '0'
                if (dayString == 'tuesday'): return '1'
                if (dayString == 'wednesday'): return '2'
                if (dayString == 'thursday'): return '3'
                if (dayString == 'friday'): return '4'
                if (dayString == 'saturday'): return '5'
                if (dayString == 'sunday'): return '6'

            cur = self._conn.cursor()

            # get netid's all regular shifts
            QUERY_STRING = 'SELECT regular_shifts.task_id, regular_shifts.dotw ' + \
                           'FROM regular_shifts ' + \
                           'WHERE regular_shifts.netid = %s'
            cur.execute(QUERY_STRING, (netid,))

            row = cur.fetchone()
            regShifts = []
            while row is not None:
                regShift = convertDay(row[1]) + '-' + str(row[0])
                if regShift not in regShifts:
                    regShifts.append(regShift)
                row = cur.fetchone()

            # get netid's all subbed in shifts
            QUERY_STRING = 'SELECT sub_requests.shift_id ' + \
                           'FROM sub_requests WHERE sub_in_netid = %s'
            cur.execute(QUERY_STRING, (netid,))
            row = cur.fetchone()
            while row is not None:
                subbedInShift = self.shiftFromID(row[0])
                regShift = str(datetime.date.fromisoformat(subbedInShift.getDate()).weekday()) + '-' + str(subbedInShift.getTaskID())
                if regShift not in regShifts:
                    regShifts.append(regShift)
                row = cur.fetchone()

            #remove netid's subbed out shifts
            QUERY_STRING = 'SELECT sub_requests.shift_id ' + \
                            'FROM sub_requests WHERE sub_out_netid = %s'
            cur.execute(QUERY_STRING, (netid,))
            rows = cur.fetchall()
            print(rows)
            if rows is not None:
                for row in rows:
                    subbedOutShift = self.shiftFromID(row[0])
                    outShift = str(datetime.date.fromisoformat(subbedOutShift.getDate()).weekday()) + '-' + str(subbedOutShift.getTaskID())
                    if outShift in regShifts:
                        regShifts.remove(outShift)
            cur.close()
            return regShifts

        except (Exception, psycopg2.DatabaseError) as error:
            print("there is an error")
            print(error)
            return False
    
    def regularShifts2(self, netid):
        try:
            def convertDay(dayString):
                if (dayString == 'monday'): return '0'
                if (dayString == 'tuesday'): return '1'
                if (dayString == 'wednesday'): return '2'
                if (dayString == 'thursday'): return '3'
                if (dayString == 'friday'): return '4'
                if (dayString == 'saturday'): return '5'
                if (dayString == 'sunday'): return '6'

            cur = self._conn.cursor()

            # get netid's all regular shifts
            QUERY_STRING = 'SELECT regular_shifts.task_id, regular_shifts.dotw ' + \
                           'FROM regular_shifts ' + \
                           'WHERE regular_shifts.netid = %s'
            cur.execute(QUERY_STRING, (netid,))

            row = cur.fetchone()
            regShifts = []
            while row is not None:
                regShift = convertDay(row[1]) + '-' + str(row[0])
                if regShift not in regShifts:
                    regShifts.append(regShift)
                row = cur.fetchone()

            cur.close()
            return regShifts

        except (Exception, psycopg2.DatabaseError) as error:
            print("there is an error")
            print(error)
            return False

    def populateShiftInfo(self, dateIn):

        try:
            if datetime.date.fromisoformat(dateIn).weekday() != 0:
                print("Given date is not a Monday.")
                return False

            date = datetime.date.fromisoformat(dateIn)
            cur = self._conn.cursor()

            def convertDayReverse(dayNumber):
                if (dayNumber == 0): return 'monday'
                if (dayNumber == 1): return 'tuesday'
                if (dayNumber == 2): return 'wednesday'
                if (dayNumber == 3): return 'thursday'
                if (dayNumber == 4): return 'friday'
                if (dayNumber == 5): return 'saturday'
                if (dayNumber == 6): return 'sunday'

            QUERY_STRING = 'SELECT * FROM max_shift_id'
            cur.execute(QUERY_STRING)
            row = cur.fetchone()

            shift_id = int(row[0])
            for i in range(7):
                for j in range(1, 7):
                    QUERY_STRING = 'SELECT regular_shifts.netid FROM regular_shifts WHERE task_id = %s AND dotw = %s'
                    cur.execute(QUERY_STRING, (j, convertDayReverse(i)))

                    numPeople = 0
                    rows = cur.fetchall()
                    for row in rows:
                        netid = row[0]
                        QUERY_STRING = 'INSERT INTO shift_assign(shift_id, netid) VALUES (%s, %s)'
                        cur.execute(QUERY_STRING, (shift_id, netid))
                        print('Added entry to shift_assign:' + str(shift_id) + ' ' + str(netid))
                        self._conn.commit()
                        numPeople += 1

                    QUERY_STRING = 'INSERT INTO shift_info(shift_id, date, task_id, cur_people) VALUES ' + \
                                   '(%s, %s, %s, %s);'
                    cur.execute(QUERY_STRING, (shift_id, date.isoformat(), j, numPeople))
                    self._conn.commit()
                    print('Added entry to shift_info:' + str(shift_id) + ' ' + str(date) + ' ' + str(j) + ' ' + str(
                        numPeople))
                    shift_id += 1

                if (i > 4):
                    for j in range(7, 13):
                        QUERY_STRING = 'SELECT regular_shifts.netid FROM regular_shifts WHERE task_id = %s AND dotw = %s'
                        cur.execute(QUERY_STRING, (j, convertDayReverse(i)))

                        numPeople = 0
                        rows = cur.fetchall()
                        for row in rows:
                            netid = row[0]
                            QUERY_STRING = 'INSERT INTO shift_assign(shift_id, netid) VALUES (%s, %s)'
                            cur.execute(QUERY_STRING, (shift_id, netid))
                            print('Added entry to shift_assign:' + str(shift_id) + ' ' + str(netid))
                            self._conn.commit()
                            numPeople += 1

                        QUERY_STRING = 'INSERT INTO shift_info(shift_id, date, task_id, cur_people) VALUES ' + \
                                       '(%s, %s, %s, %s);'
                        cur.execute(QUERY_STRING, (shift_id, date.isoformat(), j, numPeople))
                        self._conn.commit()
                        print('Added entry to shift_info:' + str(shift_id) + ' ' + str(date) + ' ' + str(j) + ' ' + str(
                            numPeople))
                        shift_id += 1

                if (i == 4):
                    QUERY_STRING = 'SELECT regular_shifts.netid FROM regular_shifts WHERE task_id = %s AND dotw = %s'
                    cur.execute(QUERY_STRING, (13, convertDayReverse(i)))

                    numPeople = 0
                    rows = cur.fetchall()
                    for row in rows:
                        netid = row[0]
                        QUERY_STRING = 'INSERT INTO shift_assign(shift_id, netid) VALUES (%s, %s)'
                        cur.execute(QUERY_STRING, (shift_id, netid))
                        print('Added entry to shift_assign:' + str(shift_id) + ' ' + str(netid))
                        self._conn.commit()
                        numPeople += 1

                    QUERY_STRING = 'INSERT INTO shift_info(shift_id, date, task_id, cur_people) VALUES ' + \
                                   '(%s, %s, %s, %s);'
                    cur.execute(QUERY_STRING, (shift_id, date.isoformat(), 13, numPeople))
                    self._conn.commit()
                    print('Added entry to shift_info:' + str(shift_id) + ' ' + str(date) + ' ' + str(13) + ' ' + str(
                        numPeople))
                    shift_id += 1

                date += datetime.timedelta(days=1)

            QUERY_STRING = 'UPDATE max_shift_id SET shift_id = %s, date = %s'
            cur.execute(QUERY_STRING, (shift_id, datetime.date.today().isoformat()))
            self._conn.commit()
            cur.close()
            return True

        except (Exception, psycopg2.DatabaseError) as error:
            self._conn.rollback()
            print('Could not populate shift_info table.')
            cur.close()
            print(error)
            return False
    
    def employeeDetails(self, netid):

        try:
            # create a cursor
            cur = self._conn.cursor()

            QUERY_STRING = 'SELECT netid FROM employees WHERE netid = %s'
            cur.execute(QUERY_STRING, (netid,))

            row = cur.fetchone()
            if row is None:
                print('Employee does not exist.')
                cur.close()
                return 'Employee does not exist.'

            QUERY_STRING = 'SELECT * FROM employees WHERE netid = %s'
            cur.execute(QUERY_STRING, (netid,))

            row = cur.fetchone()
            employee = Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            cur.close()
            return employee
        except (Exception, psycopg2.DatabaseError) as error:
            cur.close()
            print(error)
        
    def insertEmployee(self, netid, first_name, last_name, manager):

        try:
            if (not netid) or (not first_name) or (not last_name) or (not manager):
                print('Please enter all required information.')
                return False

            # create a cursor
            cur = self._conn.cursor()

            QUERY_STRING = 'SELECT netid FROM employees WHERE netid = %s'
            cur.execute(QUERY_STRING, (netid,))

            row = cur.fetchone()
            if row is not None:
                print('Employee already exists.')
                cur.close()
                return False
                
            email = netid + '@princeton.edu'
            QUERY_STRING = 'INSERT INTO employees (netid, first_name, last_name, hours, total_hours, email, manager) ' + \
                            'VALUES (%s, %s, %s, 0, 0, %s, %s)'
            cur.execute(QUERY_STRING, (netid, first_name, last_name, email, manager))
            self._conn.commit()
            print('Added employee: ' + netid + ' ' + first_name + ' ' + last_name + ' ' + manager)

            cur.close()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            self._conn.rollback()
            print('Could not add the employee.')
            cur.close()
            print(error)
            return False
    
    def removeEmployee(self, netid):

        try:

            if not netid:
                print('Please enter all required information.')
                return False

            # create a cursor
            cur = self._conn.cursor()

            QUERY_STRING = 'SELECT netid FROM employees WHERE netid = %s'
            cur.execute(QUERY_STRING, (netid,))

            row = cur.fetchone()
            if row is None:
                print('Employee does not exist.')
                cur.close()
                return False
                
            QUERY_STRING = 'DELETE FROM employees WHERE netid = %s'
            cur.execute(QUERY_STRING, (netid,))
            self._conn.commit()
            print('Removed employee: ' + netid)
            cur.close()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            self._conn.rollback()
            print('Could not remove the employee.')
            cur.close()
            print(error)
            return False

# -----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
    database = Database()
    database.connect()

    '''
    # Test shiftDetails ***** WORKS
    date = "2020-03-23"
    task_id = 1
    shift = database.shiftDetails(date, task_id)
    print(shift)

    # Test subOut ***** WORKS
    netid_out = 'trt2'
    sub_in_success = database.subOut(netid_out, date, task_id)
    print(sub_in_success)

    # Test subIn ***** WORKS
    netid_in = 'ortaoglu'
    netid_out = 'trt2'
    sub_out_success = database.subIn(netid_in, date, task_id, netid_out)
    print(sub_out_success)

    # Test allSubNeeded ***** WORKS
    subNeededShifts = database.allSubNeeded()
    print()
    print('All Sub Needed Shifts: ')
    for shift in subNeededShifts:
        print(shift)

    # Test allSubsForData ***** WORKS
    subNeededShiftsForDate = database.allSubsForDate(date)
    print()
    print('All Sub Needed Shifts for 2020-03-23: ')
    for shift in subNeededShiftsForDate:
        print(shift)

    # Test allSubsForWeek ***** WORKS
    date = "2020-03-23"
    print(database.allSubsForWeek(date))

    # Test regularShifts ***** WORKS
    netid = 'yujl'
    regShifts = database.regularShifts(netid)
    print()
    print('Regular shifts for yujl: ')
    for regShift in regShifts:
        print(regShift)

    # Test populateShiftInfo ***** WORKS
    date = "2020-04-13"
    boo = database.populateShiftInfo(date)
    '''

    # Test insertEmployee ***** WORKS
    database.insertEmployee('testguy', 'test', 'guy', 'N')

    # Test employeeDetails ***** WORKS
    employee = database.employeeDetails('testguy')
    print (employee.getFirstName() + ' ' + employee.getLastName() + ' ' + employee.getPosition()
            + ' ' + employee.getHours() + ' ' + employee.getTotalHours() + ' ' + employee.getEmail())

    # Test removeEmployee ***** WORKS
    database.removeEmployee('testguy')


    database.disconnect()