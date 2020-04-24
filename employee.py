#!/usr/bin/env python

#-----------------------------------------------------------------------
# employee.py
# Author: shiftscheduler team
#-----------------------------------------------------------------------

class Employee:

    def __init__(self, netid, first_name, last_name, hours, total_hours, email, manager, subins, subouts, walkons, noshows):
        self._netid = netid
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._manager = manager
        self._hours = hours
        self._total_hours = total_hours
        self._subins = subins
        self._subouts = subouts
        self._walkons = walkons
        self._noshows = noshows

    def __str__(self):
        return ('<strong>NetID:</strong> ' + str(self._netid) + ' <br> ' + \
                '<strong>Name:</strong> ' + str(self._first_name) + ' ' + str(self._last_name) + ' <br> ' + \
                '<strong>Email:</strong> ' + str(self._email) + ' <br> ' + \
                '<strong>Manager:</strong> ' + str(self._manager) + ' <br> ' + \
                '<strong>Hours:</strong> ' + str(self._hours) + ' <br> ' + \
                '<strong>Total Hours:</strong> ' + str(self._total_hours) + ' <br> ' + \
                '<strong>Sub-Ins:</strong> ' + str(self._subins) + ' <br> ' + \
                '<strong>Sub-Outs:</strong> ' + str(self._subouts) + ' <br> ' + \
                '<strong>Walk-Ons:</strong> ' + str(self._walkons) + ' <br> ' + \
                '<strong>No-Shows:</strong> ' + str(self._noshows))

    def getNetID(self):
        return str(self._netid)

    def getFirstName(self):
        return str(self._first_name)

    def getLastName(self):
        return str(self._last_name)

    def getEmail(self):
        return str(self._email)

    def getPosition(self):
        if self._manager == "Y":
            return "Manager"
        else:
            return "Regular"

    def getHours(self):
        return str(self._hours)

    def getTotalHours(self):
        return str(self._total_hours)

    def getSubIns(self):
        return str(self._subins)

    def getSubOuts(self):
        return str(self._subouts)

    def getWalkOns(self):
        return str(self._walkons)

    def getNoShows(self):
        return str(self._noshows)

    def addHours(self, amount):
        hours = hours + amount
        total_hours = total_hours + amount

    def resetPayPeriod(self):
        hours = 0
