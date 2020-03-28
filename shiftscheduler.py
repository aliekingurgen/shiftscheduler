#!/usr/bin/env python

#-----------------------------------------------------------------------
# shiftscheduler.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

from sys import argv
from database import Database
from time import localtime, asctime, strftime
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

def getAmPm():
    if strftime('%p') == "AM":
        return 'morning'
    return 'afternoon' 
    
def getCurrentTime():
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
    
    prevAuthor = request.cookies.get('prevAuthor')
    if prevAuthor is None:
        prevAuthor = '(None)'
    
    html = render_template('employeepage.html',
        ampm=getAmPm(),
        currentTime=getCurrentTime(),
        errorMsg=errorMsg,
        prevAuthor=prevAuthor)
    response = make_response(html)
    return response    
    
#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
