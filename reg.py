#!/usr/bin/env python

#-----------------------------------------------------------------------
# reg.py
# Author: Ekin Gurgen and Nicole Meister
#-----------------------------------------------------------------------

from sys import argv, exit
from common import getHeader, getFooter
from regdatabase import Database
from flask import Flask, request, make_response, redirect, url_for
from course import Course
from classdetails import Class_Details

#-----------------------------------------------------------------------

app = Flask(__name__)
   
#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    if "dept" in request.cookies:
        prev_dept = request.cookies.get('dept')
    else:
        prev_dept = ""
    if "number" in request.cookies:
        prev_number = request.cookies.get('number')
    else:
        prev_number = ""
    if "area" in request.cookies:
        prev_area = request.cookies.get('area')
    else:
        prev_area = ""
    if "title" in request.cookies:
        prev_title = request.cookies.get('title')
    else:
        prev_title = ""

    dept = request.args.get('dept')
    number = request.args.get('number')
    area = request.args.get('area')
    title = request.args.get('title')

    if (dept is None):
        dept = prev_dept
    if (number is None):
        number = prev_number
    if (area is None):
        area = prev_area
    if (title is None):
        title = prev_title

    html = ''
    html += '<!DOCTYPE html>'
    html += '<html>'
    html += '<head>'
    html += "<title>Registrar's Office Class Search</title>"
    html += '</head>'
    html += '<body style = "font-family:courier;font-size:16px;">'
    html += getHeader()
    html += "<h2>Class Search</h2>"
    html += '<hr>'
    html += '<br>'
    html += '<form action="index" method="get">'
    html += ('{0:<6}'.format('Dept:')).replace(" ", "&nbsp&nbsp;")
    html += '<input type="text" name="dept" value=' + dept + '>'
    html += '<br>'
    html += ('{0:<7}'.format('Number:')).replace(" ", "&nbsp&nbsp;")
    html += '<input type="text" name="number" value=' + number + '>'
    html += '<br>'
    html += ('{0:<6}'.format('Area:')).replace(" ", "&nbsp&nbsp;")
    html += '<input type="text" name="area" value=' + area + '>'
    html += '<br>'
    html += ('{0:<6.5}'.format('Title:')).replace(" ", "&nbsp&nbsp;")
    html += '<input type="text" name="title" value=' + title + '>'
    html += '<br>'
    html += '<input type="submit" value="Submit Query">'
    html += '</form>'
    html += '<hr>'

    
    #Display courses here
    database = Database()
    database.connect()
    command_dic = {"-dept": dept, "-coursenum": number, "-area": area, "-title": title}
    courses = database.searchCourses(command_dic)
    database.disconnect()
    html += '<b>ClassId Dept Num Area Title</b>'
    html += '<br>'
    for course in courses:
        myClassId = '{0:>5}'.format(course.getClassId()).replace(" ", '&nbsp;')
        html += '<a href="searchresults?classId=' + course.getClassId() + '">' + myClassId
        html += '</a>&nbsp&nbsp;'
        myDept = "{0:>3}".format(course.getDept())
        html += myDept + '</a>&nbsp&nbsp;'
        myCourseNum = "{0:<4}".format(course.getCourseNum()).replace(" ", "&nbsp;")
        html += myCourseNum + '</a>&nbsp&nbsp;'
        myArea = "{0:<3}".format(course.getArea()).replace(" ", "&nbsp;")
        html += myArea + '</a>&nbsp&nbsp;'
        html += course.getTitle()
        html += '<br>'
    html += getFooter()
    html += '</body>'
    html += '</html>'
    
    response = make_response(html)
    response.set_cookie('dept', dept)
    response.set_cookie('number', number)
    response.set_cookie('area', area)
    response.set_cookie('title', title)
    return response
    
#-----------------------------------------------------------------------

@app.route('/searchresults', methods=['GET'])
def searchResults():
    
    classId = request.args.get("classId")
    dept = request.args.get("dept")

    if (classId is None) or (classId.strip() == ''):
        errorMsg = 'Please click on a class ID.'
        return redirect(url_for('index', errorMsg=errorMsg))
  
    database = Database()
    database.connect()
    myClass = database.searchClass(classId)
    database.disconnect()
    
    html = ''
    html += '<!DOCTYPE html>'
    html += '<html>'
    html += '<head>'
    html += "<title>Registrar's Office Class Details</title>"
    html += '</head>'
    html += '<body style = "font-family:courier;font-size:16px;">'
    html += getHeader()
    html += '<hr>'
    html += '<h2>Class Details (class id ' + classId + ')</h2>'
    html += '<b>Course Id: </b>' + str(myClass.courseId)
    html += '<br>'
    html += '<b>Days: </b>' + str(myClass.days)
    html += '<br>'
    html += '<b>Start time: </b>' + str(myClass.start_time)
    html += '<br>'
    html += '<b>End time: </b>' + str(myClass.end_time)
    html += '<br>'
    html += '<b>Building: </b>' + str(myClass.building)
    html += '<br>'
    html += '<b>Room: </b>' + str(myClass.room)
    html += '<br>'
    html += '<hr>'
    html += '<h2>Course Details (course id ' + myClass.courseId + ')</h2>'
    for i in range(len(myClass.depts)):
        html += '<b>Dept and Number: </b>'
        html += myClass.depts[i] + " " + myClass.nums[i]  + '<br>'
    html += '<b>Area: </b>' + str(myClass.area) + '<br>'
    html += '<b>Title: </b>' + str(myClass.title) + '<br>'
    html += '<b>Description: </b>' + str(myClass.descrip)  + '<br>'
    html += '<b>Prerequisites: </b>' + str(myClass.prereq)  + '<br>'
    for professor in range(len(myClass.profs)):
        html += '<b>Professor: </b>' + str(myClass.profs[professor])  + '<br>'
    html += '<hr>'
    html += 'Click here to do '
    html += '<a href="index">another class search</a>.'
    html += getFooter()
    html += '</body>'
    html += '</html>' 

    response = make_response(html)
    return response
     
#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='localhost', port=int(argv[1]), debug=True)