#!/usr/bin/env python

#-----------------------------------------------------------------------
# sendemail.py
# Author: Shift Scheduler Team
#-----------------------------------------------------------------------

from flask import Flask
from flask_mail import Mail, Message
from sys import argv
import smtplib

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/testmail')
def mail_it(date, shiftStr, emailList):
    mail = Mail(app)

    # app.config.from_envvar('MINITWIT_SETTINGS', silent=True)
    app.config.update(
        DEBUG=True,
        # Flask-Mail Configuration
        MAIL_SERVER='smtp.outlook.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_USERNAME='shiftscheduler@princeton.edu',
        MAIL_PASSWORD='2020Shiftscheduler!',
        DEFAULT_MAIL_SENDER='shiftscheduler@princeton.edu',
    )

    # setup Mail
    mail = Mail(app)

    """handles our message notification"""
    # print("hello email")
    msg = Message("[ShiftScheduler] " + date + " Sub Request",
                  sender=("Shift Scheduler", "shiftscheduler@princeton.edu"),
                  recipients=emailList)
    # msg.body = "A sub was requested for" + shiftStr
    msg.html = "<h3> Sub Request: " + shiftStr + "</h3>"
    msg.html += "<div>Please visit your <a href=shiftscheduler.herokuapp.com/employee>calendar</a>"
    msg.html += " to fulfill this request.</div><br>"
    msg.html += "<div>Thanks!<br>The ShiftScheduler Team</div>"
    mail.send(msg)
    return "Email sent to all employees"

#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)
