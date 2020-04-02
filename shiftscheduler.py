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

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

def getAmPm():
    if strftime('%p') == "AM":
        return 'morning'
    return 'afternoon' 
    
def getCurrentTime():
    return asctime(localtime())

def getCalendarDate():
    return asctime(localtime())

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
 
    html = render_template('index.html',
        ampm=getAmPm(),
        currentTime=getCurrentTime())
    response = make_response(html)
    return response
    
#-----------------------------------------------------------------------

@app.route('/employeepage', methods=['GET'])
def employeePage():

    errorMsg = request.args.get('errorMsg')
    if errorMsg is None:
        errorMsg = ''

    currentTime = getCurrentTime()

    # year = currentTime.
    
    html = render_template('employeepage.html',
        ampm=getAmPm(),
        currentTime=currentTime,
        errorMsg=errorMsg,
        monday="2020-03-23",
        tuesday="2020-03-24",
        wednesday="2020-03-25",
        thursday="2020-03-26",
        friday="2020-03-27",
        saturday="2020-03-28",
        sunday="2020-03-29"
                           )
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
    shift = shift[0]
    database.disconnect()

    html = render_template('shiftdetails.html',
                           ampm=getAmPm(),
                           currentTime=getCurrentTime(),
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
