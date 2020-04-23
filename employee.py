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
        return ('NetID: ' + str(self._netid) + ' <br> ' + \
                'Name: ' + str(self._first_name) + ' ' + str(self._last_name) + ' <br> ' + \
                'Email: ' + str(self._email) + ' <br> ' + \
                'Manager: ' + str(self._manager) + ' <br> ' + \
                'Hours: ' + str(self._hours) + ' <br> ' + \
                'Total Hours: ' + str(self._total_hours) + ' <br> ' + \
                'Sub-Ins: ' + str(self._subins) + ' <br> ' + \
                'Sub-Outs: ' + str(self._subouts) + ' <br> ' + \
                'Walk-Ons: ' + str(self._walkons) + ' <br> ' + \
                'No-Shows: ' + str(self._noshows))

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
