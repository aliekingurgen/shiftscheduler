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
import json
from datetime import date, time
from CASClient import CASClient

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

app.secret_key = b'\xcdt\x8dn\xe1\xbdW\x9d[}yJ\xfc\xa3~/'

#-----------------------------------------------------------------------
@app.route('/', methods=['GET'])
@app.route('/landing', methods=['GET'])
def landing():

    html = render_template('landing.html')
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

@app.route('/login', methods=['GET'])
def login():

    netid = CASClient().authenticate().strip()
    print("netid: " + netid)
    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    if database.isCoordinator(netid):
        return redirect(url_for('index'))
    elif database.isEmployee(netid):
        return redirect(url_for('employee'))
    else:
        return redirect(url_for('noPermissions'))

    database.disconnect()

    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------

@app.route('/logout', methods=['GET'])
def logout():
    CASClient().logout()

#-----------------------------------------------------------------------

@app.route('/nopermissions', methods=['GET'])
def noPermissions():
    html = render_template('nopermissions.html')
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

@app.route('/index', methods=['GET'])
def index():

    # netid = request.cookies.get('netid')
    netid = CASClient().authenticate().strip()
    print("netid2: " + netid)
    if netid is None:
        netid = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    if not database.isCoordinator(netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

    database.disconnect()

    html = render_template('index.html',
        netid = netid)
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------

@app.route('/employee', methods=['GET'])
def employee():

    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    errorMsg = request.args.get('errorMsg')
    if errorMsg is None:
        errorMsg = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    if not database.isCoordinator(netid) and not database.isEmployee(netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

    database.disconnect()

    monday = request.args.get('monday')
    if monday is None:
        monday = 'today'

    html = render_template('employee.html',
        netid=netid,
        errorMsg=errorMsg,
        monday=monday)

    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

# #-----------------------------------------------------------------------
#
# @app.route('/calendar', methods=['GET'])
# def calendar():
#
#     netid = request.cookies.get('netid')
#     if netid is None:
#         netid = ''
#
#     errorMsg = request.args.get('errorMsg')
#     if errorMsg is None:
#         errorMsg = ''
#
#     monday = request.args.get('monday')
#     if monday is None:
#         monday = 'today'
#
#     # print('monday: ' + monday)
#
#     html = render_template('calendar.html',
#         netid=netid,
#         errorMsg=errorMsg,
#         monday=monday)
#
#     response = make_response(html)
#     response.set_cookie('netid', netid)
#     return response

#-----------------------------------------------------------------------

@app.route('/manageemployees', methods=['GET'])
def manageEmployees():

    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    if not database.isCoordinator(netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

    # allSubsNeeded = database.allSubNeeded()
    # for shift in allSubsNeeded:
    #     print(shift)

    employees = database.getAllEmployees()

    database.disconnect()

    html = render_template('manageemployees.html',
                           netid=netid,
                           employees=employees)
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------
@app.route('/coordinatorschedule', methods=['GET'])
def coordinatorSchedule():

    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    monday = request.args.get('monday')
    if monday is None:
        monday = 'today'

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    if not database.isCoordinator(netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

    allSubsNeeded = database.allSubNeeded()
    for shift in allSubsNeeded:
        print(shift)
    database.disconnect()

    html = render_template('coordinatorschedule.html',
                           netid=netid,
                           monday=monday)
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------

@app.route('/manageshifts', methods=['GET'])
def manageShifts():

    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    employee = request.args.get('employee')
    if employee is None:
        employee = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    if not database.isCoordinator(netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

    # allSubsNeeded = database.allSubNeeded()
    # for shift in allSubsNeeded:
    #     print(shift)

    employees = database.getAllEmployees()

    database.disconnect()

    html = render_template('manageshifts.html',
                           netid=netid,
                           employees=employees,
                           employee = employee)
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

    if not database.isCoordinator(netid) and not database.isEmployee(netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

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

    if not database.isCoordinator(netid) and not database.isEmployee(netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

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

    if not database.isCoordinator(netid) and not database.isEmployee(netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

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

    if not database.isCoordinator(netid) and not database.isEmployee(netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

    shifts = database.myShifts(netid)
    # for shift in shifts:
    #     print(shift)
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

    if not database.isCoordinator(netid) and not database.isEmployee(netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

    shifts = database.regularShifts(netid)
    for shift in shifts:
        print(shift)
    database.disconnect()
    return jsonify(shifts)

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

    if not database.isCoordinator(netid) and not database.isEmployee(netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

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

    if not database.isCoordinator(netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

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

    if not database.isCoordinator(netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

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
    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

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

    if not database.isCoordinator(netid) and not database.isEmployee(netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

    shift = database.shiftDetails(date, task_id)


    if shift is None:
        html = '<strong> Error: No data to display</strong>'
    else:
        shift_id = shift.getShiftID()
        employees = database.employeesInShift(shift_id)
        numEmployees = database.numberOfEmployeesInShift(shift_id)
        html = '<strong>Date: </strong>' + str(shift.getDate()) + '<br>'
        html += '<strong>Meal: </strong>' + str(shift.getMeal()) + '<br>'
        html += '<strong>Task: </strong>' + str(shift.getTask()) + '<br>'
        html += '<strong>Start: </strong>' + str(shift.getStart()[0:5]) + '<br>'
        html += '<strong>End: </strong>' + str(shift.getEnd()[0:5]) + '<br>'
        # can get rid of the second condition once numEmployees fixed?
        if numEmployees != 0 and numEmployees == len(employees):
            html += '<strong>Working: </strong>'
            for i in range(numEmployees):
                html += employees[i]
                if i != numEmployees - 1:
                    html += ", "
            html += '<br><strong>Current Number Working: </strong>' + str(numEmployees) + '<br>'

    database.disconnect()
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

# -----------------------------------------------------------------------
def idToDay(shiftStr):
    day = int(shiftStr[0])
    str = ''
    if (day == 0):
        str = 'monday'
    elif (day == 1):
        str = 'tuesday'
    elif (day == 2):
        str = 'wednesday'
    elif (day == 3):
        str = 'thursday'
    elif (day == 4):
        str = 'friday'
    elif (day == 5):
        str = 'saturday'
    elif (day == 6):
        str = 'sunday'
    return str
# -----------------------------------------------------------------------
def idToStr(shiftStr):
    day = int(shiftStr[0])
    str = ''
    if (day == 0): str = 'Monday '
    elif (day == 1): str = 'Tuesday '
    elif (day == 2): str = 'Wednesday '
    elif (day == 3): str = 'Thursday '
    elif (day == 4): str = 'Friday '
    elif (day == 5): str = 'Saturday '
    elif (day == 6): str = 'Sunday '
    taskid = int(shiftStr[2])
    if (taskid == 1): str += 'Dinner Manager'
    elif (taskid == 2): str +=  'Dinner First Shift'
    elif (taskid == 3): str +=  'Dinner Second Shift'
    elif (taskid == 4): str +=  'Dinner Dish Manager'
    elif (taskid == 5): str +=  'Dinner First Dish'
    elif (taskid == 6): str +=  'Dinner Second Dish'
    elif (taskid == 7): str +=  'Brunch Manager'
    elif (taskid == 8): str +=  'Brunch First Shift'
    elif (taskid == 9): str +=  'Brunch Second Shift'
    elif (taskid == 10): str +=  'Brunch Dish Manager'
    elif (taskid == 11): str +=  'Brunch First Dish'
    elif (taskid == 12): str += 'Brunch Second Dish'
    elif (taskid == 13): str +=  'CJL Swipe'
    return str

#-----------------------------------------------------------------------
@app.route('/employeeShiftDetails', methods=['GET'])
def employeeShiftDetails():
    # date = "2020-03-23"
    my_netid = request.cookies.get('netid')
    if my_netid is None:
        my_netid = ''

    # errorMsg = request.args.get('errorMsg')
    # if errorMsg is None:
    #     errorMsg = ''
    #
    netid = request.args.get('netid')
    if netid is None or netid == '':
        response = make_response('')
        response.set_cookie('netid', my_netid)
        return response

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    if not database.isCoordinator(my_netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))
    employee = database.employeeDetails(netid)

    regularShifts = database.regularShifts(netid)
    database.disconnect()
    if employee is None:
        employee = '<strong> Error: No data to display</strong>'
    else:
        html = str(employee) + "<br>"

        html += "<ul class = \" list-group list-group-flush \" style=\"overflow-y:scroll;height:200px;font-size:13px;\" >"
        for shift in regularShifts:
            day = idToDay(str(shift))
            taskid = shift[2]
            html += "<li class=\"list-group-item\">" + idToStr(str(shift)) + "&nbsp&nbsp&nbsp&nbsp"
            html += "<a class = \"btn  btn-info btn-sm \" href = \"/unassign?day=" + day
            html += "&taskid="+taskid+"&netid=" + employee.getNetID()+  "\""
            html += "style=\"font-size:13px\"> unassign </a> </li>"
            # print(html)
        html += "</ul>"

    response = make_response(html)
    response.set_cookie('netid', my_netid)
    return response

#-----------------------------------------------------------------------
@app.route('/employeeDetails', methods=['GET'])
def employeeDetails():
    # date = "2020-03-23"
    my_netid = request.cookies.get('netid')
    if my_netid is None:
        my_netid = ''

    # errorMsg = request.args.get('errorMsg')
    # if errorMsg is None:
    #     errorMsg = ''
    #
    netid = request.args.get('netid')
    if netid is None:
        netid = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    if not database.isCoordinator(my_netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

    employee = database.employeeDetails(netid)
    database.disconnect()
    if employee is None:
        employee = '<strong> Error: No data to display</strong>'
    else:
        # html = "<h3>Employee Details:</h3>" + str(employee) + "<br>"
        html = str(employee) + "<br>"

    response = make_response(html)
    response.set_cookie('netid', my_netid)
    return response

#-----------------------------------------------------------------------
@app.route('/unassign', methods=['GET'])
def unassignShift():
    print("HERE")
    netid = request.args.get('netid')
    taskid = request.args.get("taskid")
    dow = request.args.get("day")
    print("netid" + netid)
    print("taskid" + taskid)
    print("dow" + dow )
    try:
        database = Database()
        database.connect()
        database.removeRegularShift(netid, taskid, dow)
        database.disconnect()
    except Exception as e:
        errorMsg = e

    # response = make_response(html)
    return redirect("/manageshifts?employee=" + netid)

#-----------------------------------------------------------------------
@app.route('/assign', methods=['GET'])
def assignShift():
    print("HERE")
    netid = request.args.get('netid')
    data = request.args.get("shifts")
    shifts = data.split('_')
    try:
        database = Database()
        database.connect()
        for shift in shifts:
            if shift is not '':
                info = shift.split("-")
                day = info[0]
                taskid = info[1]
                print(day)
                print(taskid)
                database.addRegularShift(netid, int(taskid), day)

        database.disconnect()
    except Exception as e:
        errorMsg = e

    response = make_response('')
    return location.reload()

#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
