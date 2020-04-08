#!/usr/bin/env python

#-----------------------------------------------------------------------
# shiftscheduler.py
# Author: Shift Scheduler Team
#-----------------------------------------------------------------------

from sys import argv
from database import Database
from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
from datetime import date, time
from CASClient import CASClient

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

app.secret_key = b'\xcdt\x8dn\xe1\xbdW\x9d[}yJ\xfc\xa3~/'
#-----------------------------------------------------------------------

def getAmPm():
    if strftime('%p') == "AM":
        return 'morning'
    return 'afternoon' 

#-----------------------------------------------------------------------

def getCurrentTime():
    return asctime(localtime())

#-----------------------------------------------------------------------

def getCalendarDate():
    return asctime(localtime())

#-----------------------------------------------------------------------

def getURL(date, taskid):
    return '/shiftdetails?date=' + date + '&taskid=' + taskid

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    netid = CASClient().authenticate()
    # html = render_template('index.html',
    #     name = username,
    #     ampm=getAmPm(),
    #     currentTime=getCurrentTime())
    html = render_template('indexbootstrap.html',
        name = netid)
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response
    
#-----------------------------------------------------------------------

@app.route('/employeepage', methods=['GET'])
def employeePage():

    NUM_DAYS = 7

    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    errorMsg = request.args.get('errorMsg')
    if errorMsg is None:
        errorMsg = ''

    currentTime = getCurrentTime()

    dates = []

    # year = localtime().tm_year
    # month = localtime().tm_mon
    # day = localtime().tm_mday
    # what if today is not monday
    # dotw = localtime().tm_wday
    #     # if dotw != 0:
    #     #     day -= dotw

    year = 2020
    month = 3
    day = 23

    for i in range(NUM_DAYS):
        dates.append(date(year, month, day))
        if day == 30:
            if month == 4 or month == 6 or month == 9 or month == 11:
                month += 1
                day = 1
            else:
                day += 1
        elif day == 31:
            if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10:
                month += 1
                day = 1
            elif month == 12:
                year += 1
                month = 1
                day = 1
        elif year % 4 == 0 and month == 2 and day == 29:
            month += 1
            day = 1
        elif year % 4 != 0 and month == 2 and day == 28:
            month += 1
            day = 1
        else:
            day += 1
    
    # html = render_template('employeepage.html',
    #     ampm=getAmPm(),
    #     currentTime=currentTime,
    #     errorMsg=errorMsg,
    #     monday=dates[0],
    #     tuesday=dates[1],
    #     wednesday=dates[2],
    #     thursday=dates[3],
    #     friday=dates[4],
    #     saturday=dates[5],
    #     sunday=dates[6]
    #                        )
    html = render_template('employeepagebootstrap.html',
        netid=netid,
        errorMsg=errorMsg,
        monday=dates[0],
        tuesday=dates[1],
        wednesday=dates[2],
        thursday=dates[3],
        friday=dates[4],
        saturday=dates[5],
        sunday=dates[6]
                    )
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

@app.route('/coordinatorpage', methods=['GET'])
def coordinatorPage():
    html = render_template('coordinatorbootstrap.html')
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

@app.route('/profile', methods=['GET'])
def profile():
    html = render_template('profile.html')
    response = make_response(html)
    return response

# -----------------------------------------------------------------------

@app.route('/shiftdetails', methods=['GET'])
def shiftDetails():
    errorMsg = request.args.get('errorMsg')
    if errorMsg is None:
        errorMsg = ''

    date = request.args.get('date')
    if date is None:
        date = ''

    task_id = request.args.get('taskid')
    if task_id is None:
        task_id = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e


    shift = database.shiftDetails(date, task_id)
    database.disconnect()

    # html = render_template('shiftdetails.html',
    #                        ampm=getAmPm(),
    #                        currentTime=getCurrentTime(),
    #                        errorMsg=errorMsg,
    #                        shift=shift
    #                        )
    html = render_template('shiftdetailsbootstrap.html',
                           errorMsg=errorMsg,
                           shift=shift
                           )
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
