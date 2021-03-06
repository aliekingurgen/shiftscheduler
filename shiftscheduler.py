#!/usr/bin/env python

#-----------------------------------------------------------------------
# shiftscheduler.py
# Author: Shift Scheduler Team
#-----------------------------------------------------------------------

from sys import argv
from database import Database
from sendemail import mail_it
from time import strftime
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
    print("net id: " + netid)
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
    if netid is None:
        netid = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    if not database.isCoordinator(netid):
        if not database.isEmployee(netid):
            database.disconnect()
            return redirect(url_for('noPermissions'))
        else:
            database.disconnect()
            return redirect(url_for('employee'))

    database.disconnect()

    html = render_template('index.html',
        netid = netid)
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------

@app.route('/employee', methods=['GET'])
def employee():

    netid = CASClient().authenticate().strip()
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

    if (database.hoursForEmployee(netid)):
        employee = database.employeeDetails(netid)
        hours = employee.getHours()

    database.disconnect()

    name = employee.getFirstName() + ' ' + employee.getLastName()
    position = employee.getPosition()

    html = render_template('profile.html',
                           netid=netid,
                           name=name,
                           position=position,
                           hours=hours)
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

#-----------------------------------------------------------------------

@app.route('/managehours', methods=['GET'])
def manageHours():

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

    database.disconnect()

    html = render_template('managehours.html',
        netid = netid)
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

@app.route('/reset', methods=['GET'])
def reset():

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

    database.disconnect()

    html = render_template('reset.html',
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
    if successful == "conflict":
        html = "Sub-In not successful. You already have a shift at this time."
    elif successful == "already_assigned":
        html += "Sub-In not successful. You are already assigned to this shift."
    elif successful == "old":
        html = "You cannot sub-in to a past shift."
    elif successful:
        html = "Sub-In successful!"
    else:
        html = "Sub-In not successful. Please try again."
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

# -----------------------------------------------------------------------

def taskidToStr(taskid):
    str = ''
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
    return str

#-----------------------------------------------------------------------

@app.route('/subOut', methods=['GET'])
def subOut():

    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    shiftDate = request.args.get('date')
    if shiftDate is None:
        shiftDate = ''

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

    successful = database.subOut(netid, shiftDate, task_id)
    emailList = database.getAllEmails()
    # emailList = ["ortaoglu@princeton.edu","agurgen@princeton.edu", "cz10@princeton.edu", "trt2@princeton.edu"]
    database.disconnect()

    if successful == "old":
        html = "You cannot sub-out of a past shift."
    elif successful:
        html = "Sub-Out successful!"
        print("email being sent")
        # print(taskidToStr(int(task_id)))
        dateObject = date.fromisoformat(shiftDate)
        print(shiftDate)
        dateFormatted = dateConvert(dateObject.strftime("%m/%d"))
        print(dateFormatted)
        shiftStr = dateFormatted + ' ' + taskidToStr(int(task_id))
        # print(shiftStr)
        print(mail_it(dateFormatted, shiftStr, emailList))
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
    shifts = database.myShifts(netid, mon)

    # for shift in shifts:
    #    print("shift: " + shift)

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

    # print(mon)
    subs = database.allSubsForWeek(mon)
    database.disconnect()

    return jsonify(subs)

#-----------------------------------------------------------------------
@app.route('/needSubShiftsEmployee', methods=['GET'])
def needSubShiftsEmployee():

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

    # print(mon)
    subs = database.allSubsForEmployee(mon, netid)
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
    else:
        firstNameSplit = firstname.split("-")

        if len(firstNameSplit) > 1:
            firstname = ""
            for name in firstNameSplit:
                firstname += name + " "


    lastname = request.args.get('lastname')
    print(lastname)
    if lastname is None:
        lastname = ''
    else:
        lastNameSplit = lastname.split("-")
        if len(lastNameSplit) > 1:
            lastname = ""
            for name in lastNameSplit:
                print(name)
                lastname += name + " "

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

    print(employeenetid + " " + firstname + " " + lastname + " " + manager)
    successful = database.insertEmployee(employeenetid, firstname, lastname, manager)
    database.disconnect()

    print(successful)
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

    if successful == "not_employee":
        html = employeenetid + ' is not an employee.'
    elif successful:
        html = employeenetid + ' was successfully removed!'
    else:
        html = employeenetid + ' was not removed. Please try again.'
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

# -----------------------------------------------------------------------

def timeConvert(time):
    separated = time.split(':')
    try:
        hour = int(separated[0])
        if hour > 12:
            hour -= 12
        # print(hour)
            return str(hour) + ':' + separated[1] + ' PM'
        else:
            return str(hour) + ':' + separated[1] + ' AM'
    except:
        print('error converting to 12-hour time')
        pass

# -----------------------------------------------------------------------

def dateConvert(date):
    separated = date.split('/')
    try:
        month = int(separated[0])
        day = int(separated[1])
        return str(month) + '/' + str(day)
    except:
        print('error getting rid of 0s from date')
        pass

# -----------------------------------------------------------------------

@app.route('/shiftdetails', methods=['GET'])
def shiftDetails():
    netid = request.cookies.get('netid')
    if netid is None:
        netid = ''

    shiftDate = request.args.get('date')
    if shiftDate is None:
        shiftDate = ''

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

    shift = database.shiftDetails(shiftDate, task_id)

    if shift is None:
        html = '<strong> Error: No data to display</strong>'

    else:
        shift_id = shift.getShiftID()
        employees = database.employeesInShift(shift_id)
        numEmployees = database.numberOfEmployeesInShift(shift_id)
        dateObject = date.fromisoformat(shiftDate)
        dateFormatted = dateObject.strftime("%m/%d")
        html = '<strong>Date: </strong>' + dateConvert(dateFormatted) + '<br>'
        # html += '<strong>Shift ID: </strong>' + str(shift.getShiftID()) + '<br>'
        html += '<strong>Meal: </strong>' + str(shift.getMeal()) + '<br>'
        html += '<strong>Task: </strong>' + str(shift.getTask()) + '<br>'
        html += '<strong>Start: </strong>' + timeConvert(shift.getStart()[0:5]) + '<br>'
        html += '<strong>End: </strong>' + timeConvert(shift.getEnd()[0:5]) + '<br>'
        # can get rid of the second condition once numEmployees fixed?
        print(employees)
        print(numEmployees)
        if len(employees) != 0:
            html += '<strong>Working: </strong><br>'
            for i in range(len(employees)):
                html += employees[i]
                html += "<br>"
            # html += '<br><strong>Current Number Working: </strong>' + str(numEmployees) + '<br>'
        walkOns = database.walkOnsInShift(shift_id)

        workingNo = len(employees) + len(walkOns)
        # html += '<br><strong>Current Number Working: </strong>' + str(workingNo) + '<br>'

        if len(walkOns) != 0:
            html += "<strong> Walk-Ons: </strong>"
            for walkOn in walkOns:
                html += "<br>"
                html += walkOn.getFirstName() + " " + walkOn.getLastName()

    database.disconnect()
    response = make_response(html)
    response.set_cookie('netid', netid)
    return response

# -----------------------------------------------------------------------

@app.route('/shiftdetailsco', methods=['GET'])
def shiftDetailsCoordinator():
    my_netid = request.cookies.get('netid')
    if my_netid is None:
        my_netid = ''

    dateArg = request.args.get('date')
    if dateArg is None:
        dateArg = ''

    task_id = request.args.get('taskid')
    if task_id is None:
        task_id = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    if not database.isCoordinator(my_netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

    shift = database.shiftDetails(dateArg, task_id)


    if shift is None:
        html = '<strong> Error: No data to display</strong>'
    else:
        shift_id = shift.getShiftID()
        employees = database.employeeObjectsInShift(shift_id)

        for employee in employees:
            print(employee.getNetID())

        numEmployees = database.numberOfEmployeesInShift(shift_id)
        dateObject = date.fromisoformat(shift.getDate())
        dateFormatted = dateObject.strftime("%m/%d")
        html = '<strong>Date: </strong>' + dateConvert(dateFormatted) + '<br>'
        html += '<strong>Shift ID: </strong>' + str(shift.getShiftID()) + '<br>'
        html += '<strong>Meal: </strong>' + str(shift.getMeal()) + '<br>'
        html += '<strong>Task: </strong>' + str(shift.getTask()) + '<br>'
        html += '<strong>Start: </strong>' + timeConvert(shift.getStart()[0:5]) + '<br>'
        html += '<strong>End: </strong>' + timeConvert(shift.getEnd()[0:5]) + '<br>'
        # can get rid of the second condition once numEmployees fixed?
        print(employees)
        print(numEmployees)
        # if numEmployees != 0 and numEmployees == len(employees):
        if len(employees) != 0:
            html += '<strong>Working: </strong><br>'
            for i in range(len(employees)):
                print('working:' + employees[i].getNetID())
                html += "<br>"
                html += employees[i].getFirstName() + " " + employees[i].getLastName()
                html += "&nbsp&nbsp&nbsp"
                html += "<span id = \"noshow"  + employees[i].getNetID() + "\" >"
                html += "<button class=\"btn btn-secondary btn-sm noShow\" netid = \"" + employees[i].getNetID() + "\" "
                html += "href = \"/noShow?netid=" + employees[i].getNetID() + "&shiftid=" + shift_id
                print(date.today())
                print(dateObject)
                if date.today() < dateObject:
                    html += "\" id = \"" + employees[i].getNetID() + "button\" disabled>mark no show</button> "
                else:
                    html += "\" id = \"" + employees[i].getNetID() + "button\">mark no show</button> "
                html += " </span><br>"
        noShows = database.noShowsInShift(shift_id)
        if (len(employees) == 0) and (len(noShows) != 0):
                html += '<strong>Working: </strong><br>'
        for noShow in noShows:
            print('no show: ' + noShow.getNetID())
            html += "<br>"
            html += noShow.getFirstName() + " " + noShow.getLastName()
            html += "&nbsp&nbsp&nbsp"
            html += "<span id = \"noshow" + noShow.getNetID() + "\" >"
            html += "<button class=\"btn btn-danger btn-sm undoNoShow\" netid = \"" + noShow.getNetID() + "\" "
            html += " href=\"/undoNoShow?netid=" + noShow.getNetID() + "&shiftid=" + shift_id
            html += "\" id = \"" + noShow.getNetID() + "button\">no show</button> "
            html += " </span><br>"
            print(html)

        walkOns = database.walkOnsInShift(shift_id)

        workingNo = len(employees) + len(walkOns)
        # html += '<br><strong>Current Number Working: </strong>' + str(workingNo) + '<br>'

        if len(walkOns) != 0:
            html += "<strong> Walk-Ons: </strong>"
            for walkOn in walkOns:
                html += "<br>"
                html += walkOn.getFirstName() + " " + walkOn.getLastName()


    database.disconnect()
    response = make_response(html)
    response.set_cookie('netid', my_netid)
    return response

# -----------------------------------------------------------------------
@app.route('/noShow', methods=['GET'])
def noShow():
    my_netid = request.cookies.get('netid')
    if my_netid is None:
        my_netid = ''

    netid = request.args.get('netid')
    if netid is None:
        netid = ''

    shift_id = request.args.get('shiftid')
    if shift_id is None:
        shift_id = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    if not database.isCoordinator(my_netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

    print("shiftid: " + shift_id)
    print("netid" + netid)
    successful = database.addNoShow(shift_id, netid)
    database.disconnect()
    html = ""
    if successful == 'future':
        print(successful)
        html += "<span id = \"noshow" + netid + "\" >"
        html += "<button class=\"btn btn-secondary btn-sm noShow\" netid = \"" + netid + "\" "
        html += "href = \"/noShow?netid=" + netid + "&shiftid=" + shift_id
        html += "\" id = \"" + netid + "button\">not possible for a future shift</button> "
        html += " </span>"
        # html += '<span class="text-danger">You cannot mark a no-show to a future shift.</span>'
    else:
        print(successful)
        html += "<span id = \"noshow" + netid + "\" >"
        html += "<button class=\"btn btn-danger btn-sm undoNoShow\" netid = \"" + netid + "\" "
        html += " href=\"/undoNoShow?netid=" + netid + "&shiftid=" + shift_id
        html += "\" id = \"" + netid + "button\">no show</button> "
        html += " </span>"

    response = make_response(html)
    response.set_cookie('netid', my_netid)
    return response

# -----------------------------------------------------------------------
@app.route('/undoNoShow', methods=['GET'])
def undoNoShow():
    my_netid = request.cookies.get('netid')
    if my_netid is None:
        my_netid = ''

    netid = request.args.get('netid')
    if netid is None:
        netid = ''

    shift_id = request.args.get('shiftid')
    if shift_id is None:
        shift_id = ''

    try:
        database = Database()
        database.connect()
    except Exception as e:
        errorMsg = e

    if not database.isCoordinator(my_netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

    print("shiftid: " + shift_id)
    print("netid" + netid)
    successful = database.undoNoShow(shift_id, netid)
    database.disconnect()
    html = ""
    if successful == 'future':
        print(successful)
        html += '<span class="text-danger">You cannot undo a no-show to a future shift.</span>'
    elif successful:
        html += "<span id = \"noshow" + netid + "\" >"
        html += "<button class=\"btn btn-secondary btn-sm noShow\" netid = \"" + netid + "\" "
        html += "href = \"/noShow?netid=" + netid + "&shiftid=" + shift_id
        html += "\" id = \"" + netid + "button\">mark no show</button> "
        html += " </span>"
    else:
        # keep the red button
        html += "<span id = \"noshow" + netid + "\" >"
        html += "<button class=\"btn btn-danger btn-sm undoNoShow\" netid = \"" + netid + "\" "
        html += " href=\"/undoNoShow?netid=" + netid + "&shiftid=" + shift_id
        html += "\" id = \"" + netid + "button\">no show</button> "
        html += " </span>"
        print(html)

    response = make_response(html)
    response.set_cookie('netid', my_netid)
    return response

#-----------------------------------------------------------------------
@app.route('/walkOn', methods=['POST'])
def walkOn():
    my_netid = request.cookies.get('netid')
    if my_netid is None:
        my_netid = ''

    netid = request.args.get('netid').strip()
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

    if not database.isCoordinator(my_netid):
        database.disconnect()
        return redirect(url_for('noPermissions'))

    shift = database.shiftDetails(date, task_id)
    shift_id = shift.getShiftID()

    successful = database.addWalkOn(shift_id, netid)

    html = ''
    if successful == 'future':
        html += 'future'
    elif successful == 'already_assigned':
        html += 'already_assigned'
    elif successful == 'not_employee':
        html += 'not_employee'
    elif successful:
        walkOns = database.walkOnsInShift(shift_id)
        if len(walkOns) == 1:
            html += "<strong> Walk-Ons: </strong>"
        employeeObj = database.getEmployeeObject(netid)
        html += "<br>" + employeeObj.getFirstName() + " " + employeeObj.getLastName()
    else:
        html = "failed"
    database.disconnect()
    response = make_response(html)
    response.set_cookie('netid', my_netid)
    return response

#-----------------------------------------------------------------------

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
    return str

#-----------------------------------------------------------------------
@app.route('/employeeShiftDetails', methods=['GET'])
def employeeShiftDetails():
    my_netid = request.cookies.get('netid')
    if my_netid is None:
        my_netid = ''

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
    # print('employee: ' + employee)

    regularShifts = database.regularShifts(netid)
    database.disconnect()
    if employee is None:
        html = '<strong> Error: No data to display</strong>'
    elif employee == 'Employee does not exist.':
        html = '<strong> Error: Employee does not exist</strong>'
    else:
        html = '<strong>Net ID:</strong> ' + employee.getNetID() + ' <br> ' + \
                '<strong>Name:</strong> ' + employee.getFirstName() + ' ' + employee.getLastName() + ' <br> ' + \
                '<strong>Email:</strong> ' + employee.getEmail()+ ' <br> ' + \
                '<strong>Position:</strong> ' + employee.getPosition() + ' <br> ' + \
                '<strong>Sub-Ins:</strong> ' + employee.getSubIns() + ' <br> ' + \
                '<strong>Sub-Outs:</strong> ' + employee.getSubOuts() + ' <br> ' + \
                '<strong>Walk-Ons:</strong> ' + employee.getWalkOns() + ' <br> ' + \
                '<strong>No-Shows:</strong> ' + employee.getNoShows() + ' <br> '

        html += "<ul class = \" list-group list-group-flush \" style=\"overflow-y:scroll;height:200px;font-size:13px;\" >"
        for shift in regularShifts:
            day = idToDay(str(shift))
            taskid = shift[2]
            html += "<li class=\"list-group-item\">" + idToStr(str(shift)) + "&nbsp&nbsp&nbsp&nbsp"
            html += "<a class = \"btn  btn-info btn-sm unassign\" href = \"/unassign?day=" + day
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
    my_netid = request.cookies.get('netid')
    if my_netid is None:
        my_netid = ''

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
        html = '<strong>Net ID:</strong> ' + employee.getNetID() + ' <br> ' + \
                '<strong>Name:</strong> ' + employee.getFirstName() + ' ' + employee.getLastName() + ' <br> ' + \
                '<strong>Email:</strong> ' + employee.getEmail()+ ' <br> ' + \
                '<strong>Position:</strong> ' + employee.getPosition() + ' <br> ' + \
                '<strong>Sub-Ins:</strong> ' + employee.getSubIns() + ' <br> ' + \
                '<strong>Sub-Outs:</strong> ' + employee.getSubOuts() + ' <br> ' + \
                '<strong>Walk-Ons:</strong> ' + employee.getWalkOns() + ' <br> ' + \
                '<strong>No-Shows:</strong> ' + employee.getNoShows() + ' <br> '

    response = make_response(html)
    response.set_cookie('netid', my_netid)
    return response

#-----------------------------------------------------------------------
@app.route('/unassign', methods=['GET'])
def unassignShift():

    my_netid = request.cookies.get('netid')
    if my_netid is None:
        my_netid = ''

    netid = request.args.get('netid')
    taskid = request.args.get("taskid")
    dow = request.args.get("day")
    print("netid" + netid)
    print("taskid" + taskid)
    print("dow" + dow )
    try:
        database = Database()
        database.connect()
        if not database.isCoordinator(my_netid):
            database.disconnect()
            return redirect(url_for('noPermissions'))
        database.removeRegularShift(netid, taskid, dow)
        database.disconnect()
    except Exception as e:
        errorMsg = e

    # response = make_response(html)
    return redirect("/manageshifts?employee=" + netid)

#-----------------------------------------------------------------------
@app.route('/assign', methods=['GET'])
def assignShift():

    my_netid = request.cookies.get('netid')
    if my_netid is None:
        my_netid = ''

    netid = request.args.get('netid')
    shift = request.args.get("shift")
    result = False
    try:
        database = Database()
        database.connect()
        if not database.isCoordinator(my_netid):
            database.disconnect()
            return redirect(url_for('noPermissions'))
        info = shift.split("-")
        day = info[0]
        taskid = info[1]
        result = database.addRegularShift(netid, int(taskid), day)
        database.disconnect()
    except Exception as e:
        errorMsg = e

    response = make_response('')
    if result == 'already_assigned':
        return 'Shift is already assigned.'
    elif result == 'conflict':
        return 'Request conflicts with another assigned shift.'
    elif result == 'not_valid':
        return 'Not a valid shift.'
    elif result == True:
        return 'Shift was successfully added!'
    else:
        return 'Request failed. Please try again.'

#-----------------------------------------------------------------------
@app.route('/allhours', methods=['GET'])
def allHours():

    startDate = request.args.get("startDate")
    endDate = request.args.get("endDate")

    try:
        database = Database()
        database.connect()
        employees = database.hoursForAllEmployees(startDate, endDate)
        if not employees:
            database.disconnect()
            return '<strong>Error. Please try again.</strong>'
        database.disconnect()
    except Exception as e:
        errorMsg = e

    html = "<table class = \" table table-striped \" style=\"overflow-y:scroll;height:300px;\"  >"
    html += "<tr>"
    html += "<th> First Name </th>"
    html += "<th> Last Name </th>"
    html += "<th> Hours </th>"
    html += "<th> Total Sub-Ins </th>"
    html += "<th> Total Sub-Outs </th>"
    html += "<th> Total Walk-Ons </th>"
    html += "<th> Total No-Shows </th>"
    html  += "</tr>"
    for employee in  employees:
        html += "<tr>"
        html += "<td>" + employee.getFirstName() + "</td>"+ "<td>" + employee.getLastName() + "</td>"
        html += "<td>" + employee.getHours() + "</td>"
        html += "<td>" + employee.getSubIns() + "</td>" + "<td>" + employee.getSubOuts() + "</td>"
        html += "<td>" + employee.getWalkOns() + "</td>" + "<td>" + employee.getNoShows() + "</td>"
        html += "</tr>"
        # print(html)
    html += "</table>"
    return html

#-----------------------------------------------------------------------
@app.route('/resetStatsLink', methods=['GET'])
def resetStats():

    my_netid = request.cookies.get('netid')
    if my_netid is None:
        my_netid = ''

    try:
        database = Database()
        database.connect()
        if not database.isCoordinator(my_netid):
            database.disconnect()
            return redirect(url_for('noPermissions'))
        if database.resetStatsForEmployees():
            html = 'success'
        else:
            html = 'failed'
        database.disconnect()
    except Exception as e:
        errorMsg = e
        html = 'failed'

    html = 'success'
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
