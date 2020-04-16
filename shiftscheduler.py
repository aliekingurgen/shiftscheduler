#!/usr/bin/env python

#-----------------------------------------------------------------------
# shiftscheduler.py
# Author: Shift Scheduler Team
#-----------------------------------------------------------------------

from sys import argv
from database import Database
from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, jsonify
from datetime import date, time
from CASClient import CASClient

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

app.secret_key = b'\xcdt\x8dn\xe1\xbdW\x9d[}yJ\xfc\xa3~/'
#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    netid = CASClient().authenticate().strip()

    html = render_template('indexbootstrap.html',
        name = netid)
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------

@app.route('/logout', methods=['GET'])
def logout():
    CASClient().logout()

#-----------------------------------------------------------------------

@app.route('/employeepage', methods=['GET'])
def employeePage():

    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    errorMsg = request.args.get('errorMsg')
    if errorMsg is None:
        errorMsg = ''

    html = render_template('employeepagebootstrap.html',
        netid=netid,
        errorMsg=errorMsg)
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------

@app.route('/coordinatorpage', methods=['GET'])
def coordinatorPage():

    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    allSubsNeeded = database.allSubNeeded()
    for shift in allSubsNeeded:
        print(shift)
    database.disconnect()

    html = render_template('coordinatorbootstrap.html',
                           netid=netid)
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------
@app.route('/coordinatorschedule', methods=['GET'])
def coordinatorSchedule():

    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    allSubsNeeded = database.allSubNeeded()
    for shift in allSubsNeeded:
        print(shift)
    database.disconnect()

    html = render_template('coordinatorschedule.html',
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

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    employee = database.employeeDetails(netid)
    database.disconnect()

    name = employee.getFirstName() + ' ' + employee.getLastName()
    position = employee.getPosition()

    html = render_template('profile.html',
                           netid=netid,
                           name=name,
                           position=position)
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
        html = "Sub-In successful!"
    else:
        html = "Sub-In not successful. Please try again."
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
        html = "Sub-Out successful!"
    else:
        html = "Sub-Out not successful. Please try again."
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

    shifts = database.myShifts(netid)
    for shift in shifts:
        print(shift)
    database.disconnect()
    return jsonify(shifts)

#-----------------------------------------------------------------------

@app.route('/regularShifts', methods=['GET'])
def regularShifts():

    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    shifts = database.regularShifts(netid)
    for shift in shifts:
        print(shift)
    database.disconnect()
    return jsonify(shifts)

#-----------------------------------------------------------------------

@app.route('/needSubShifts', methods=['GET'])
def needSubShifts():

    mon = request.args.get('mon')
    if mon is None:
        mon = ''
    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    print(mon);
    subs = database.allSubsForWeek(mon)
    database.disconnect()

    return jsonify(subs)

#-----------------------------------------------------------------------

@app.route('/insertEmployee', methods=['GET'])
def insertEmployee():

    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    employeenetid = request.args.get('employeenetid')
    if employeenetid is None:
        employeenetid = ''

    firstname = request.args.get('firstname')
    if firstname is None:
        firstname = ''

    lastname = request.args.get('lastname')
    if lastname is None:
        lastname = ''

    manager = request.args.get('manager')
    if manager is None:
        manager = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    successful = database.insertEmployee(employeenetid, firstname, lastname, manager)
    database.disconnect()

    if successful:
        html = employeenetid + ' was successfully added!'
    else:
        html = employeenetid + ' was not added. Please try again.'
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------

@app.route('/removeEmployee', methods=['GET'])
def removeEmployee():

    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    employeenetid = request.args.get('employeenetid')
    if employeenetid is None:
        employeenetid = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    successful = database.removeEmployee(employeenetid)
    database.disconnect()

    if successful:
        html = employeenetid + ' was successfully removed!'
    else:
        html = employeenetid + ' was not removed. Please try again.'
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

# -----------------------------------------------------------------------

@app.route('/shiftdetails', methods=['GET'])
def shiftDetails():
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
    if shift is None:
        html = '<strong> Error: No data to display</strong>'
    else:
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
