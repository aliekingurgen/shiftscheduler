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

# def getCurrentTime():
#     return asctime(localtime())

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

    netid = CASClient().authenticate().strip()
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
                    )
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------

@app.route('/coordinatorpage', methods=['GET'])
def coordinatorPage():
    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    html = render_template('coordinatorbootstrap.html',
                           netid=netid)
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------

@app.route('/profile', methods=['GET'])
def profile():
    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    html = render_template('profile.html',
                           netid=netid)
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------

@app.route('/team', methods=['GET'])
def team():
    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    html = render_template('team.html',
                           netid=netid)
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------

@app.route('/test', methods=['GET'])
def test():
    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    regShifts = database.regularShifts(netid)
    print()
    print('Regular shifts for yujl: ')
    for i in range(len(regShifts)):
        print(str(regShifts[i][0]) + ' ' + str(regShifts[i][1]))
    database.disconnect()

    html = render_template('test.html',
                           netid=netid)
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------

@app.route('/subIn', methods=['GET'])
def subIn():
    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

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

    successful = database.subIn(netid, date, task_id)
    database.disconnect()
    if successful:
        html = "<br>Sub-In successful!"
    else:
        html = "<br>Sub-In not successful. Please try again."
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------

@app.route('/subOut', methods=['GET'])
def subOut():
    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

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

    successful = database.subOut(netid, date, task_id)
    database.disconnect()
    if successful:
        html = "<p>Sub-Out successful!</p>"
    else:
        html = "<p>Sub-Out not successful. Please try again. </p>"
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------

@app.route('/myShifts', methods=['GET'])
def myShifts():
    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    shifts = database.regularShifts(netid)
    database.disconnect()
    for shift in shifts:
        print(shift)

    return shifts

#-----------------------------------------------------------------------

@app.route('/needSubShifts', methods=['GET'])
def needSubShifts():
    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''
    mon = request.args.get('mon')
    if mon is None:
        mon = ''
    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    subs = database.allSubsForWeek(mon)
    database.disconnect()

    return subs

# -----------------------------------------------------------------------

@app.route('/shiftdetails', methods=['GET'])
def shiftDetails():
    print("here")
    # date = "2020-03-23"
    # netid = request.cookies.get('netid')
    # if netid is None:
    #     netid = ''
    #
    # errorMsg = request.args.get('errorMsg')
    # if errorMsg is None:
    #     errorMsg = ''
    #
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
    html = '<strong>Date: </strong>' + str(shift.getDate()) + '<br>'
    html += '<strong>Meal: </strong>' + str(shift.getMeal()) + '<br>'
    html += '<strong>Task: </strong>' + str(shift.getTask()) + '<br>'
    html += '<strong>Start: </strong>' + str(shift.getStart()[0:5]) + '<br>'
    html += '<strong>End: </strong>' + str(shift.getEnd()[0:5]) + '<br>'

    response = make_response(html)
    return response

#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
