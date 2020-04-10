#!/usr/bin/env python

#-----------------------------------------------------------------------
# shift.py
# Author: shiftscheduler team
#-----------------------------------------------------------------------

class Shift:

    def __init__(self, shiftID, date, taskID, meal, task, startTime, endTime, curPeople):
        self._shiftID = shiftID
        self._date = date
        self._taskID = taskID
        self._meal = meal
        self._task = task
        self._startTime = startTime
        self._endTime = endTime
        self._curPeople = curPeople

    def __str__(self):
        return str(self._shiftID)

    def getShiftID(self):
        return str(self._shiftID)

    def getDate(self):
        return str(self._date)
    
    def getTaskID(self):
        return str(self._taskID)
    
    def getMeal(self):
        return self._meal
    
    def getTask(self):
        return self._task
    
    def getStart(self):
        return str(self._startTime)

    def getEnd(self):
        return str(self._endTime)
    
    def getCurPeople(self):
        return str(self._curPeople)
    
    
