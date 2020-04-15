#!/usr/bin/env python

#-----------------------------------------------------------------------
# employee.py
# Author: shiftscheduler team
#-----------------------------------------------------------------------

class Employee:

    def __init__(self, netid, first_name, last_name, hours, total_hours, email, manager,):
        self._netid = netid
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._manager = manager
        self._hours = hours
        self._total_hours = total_hours
        
    def __str__(self):
        return str(self._shiftID)

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



    
    
