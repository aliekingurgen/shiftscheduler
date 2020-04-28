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
def mail_it():
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
    print("hello email")
    msg = Message("Hello",
                  sender=("Shift Scheduler", "shiftscheduler@princeton.edu"),recipients=["ortaoglu@princeton.edu","agurgen@princeton.edu"])
    msg.body = "A shift has been subbed out of!"
    mail.send(msg)
    return "I sent an email!"

#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)

# import smtplib, ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
#
# sender_email = "shiftschedulerprinceton@gmail.com"
# receiver_email = "ortaoglu@princeton.edu"
# # password = input("Type your password and press enter: ")
# password = 'Dondero22'
#
# message = MIMEMultipart("alternative")
# message["Subject"] = "multipart test"
# message["From"] = sender_email
# message["To"] = receiver_email
#
# # Create the plain-text and HTML version of your message
# text = """\
# Hi,
# How are you?
# Real Python has many great tutorials:
# www.realpython.com"""
# html = """\
# <html>
#   <body>
#     <p>Hi,<br>
#        How are you?<br>
#        <a href="http://www.realpython.com">Real Python</a>
#        has many great tutorials.
#     </p>
#   </body>
# </html>
# """
#
# # Turn these into plain/html MIMEText objects
# part1 = MIMEText(text, "plain")
# part2 = MIMEText(html, "html")
#
# # Add HTML/plain-text parts to MIMEMultipart message
# # The email client will try to render the last part first
# message.attach(part1)
# message.attach(part2)
#
# # Create secure connection with server and send email
# context = ssl.create_default_context()
# with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#     server.login(sender_email, password)
#     server.sendmail(
#         sender_email, receiver_email, message.as_string()
#     )
#
# import sendgrid
# import os
# from sendgrid.helpers.mail import *
#
# sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
# from_email = Email("shiftschedulerprinceton@gmail.com")
# subject = "Hello World from the SendGrid Python Library!"
# to_email = Email("ortaoglu@princeton.edu")
# content = Content("text/plain", "Hello, Email!")
# mail = Mail(from_email, subject, to_email, content)
# response = sg.client.mail.send.post(request_body=mail.get())
# print(response.status_code)
# print(response.body)
# print(response.headers)
