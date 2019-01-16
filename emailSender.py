#!/usr/bin/env python
'''

@author: Jayakumar M
'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import glob
import os
import time
import shutil, pdb


# me == my email address
# you == recipient's email address

def send_mail(fromaddr, toaddr, mailpassword, subject, filetoAttach, smtpserver="smtp.office365.com"):
    me = fromaddr
    you = toaddr

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ",".join(you)

    # Create the body of the message (a plain-text and an HTML version).
    text = "<text>Hi! <br/><br/>Please find the Validation Test Report which is attached in this mail.</text><br/>"

    sign = "<text>Regards,<br/> Automation Team</text>"

    # reportfile = fetch_file_to_attach()


    body = text + sign
    print "=" * 60

    part2 = MIMEText(body, 'html')
    msg.attach(part2)


    filePath = filetoAttach + "Report.html"
    fi = open(filePath)
    attachment = MIMEText(fi.read())
    attachment.add_header('Content-Disposition', 'attachment', filename="Report.html")
    msg.attach(attachment)
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.



    # Send the message via local SMTP server.
    s = smtplib.SMTP(smtpserver, 587)
    s.ehlo()
    s.starttls()
    s.login(fromaddr, mailpassword)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()
    time.sleep(20)
    print "Mail Sent Successfully"


# scandirs()


def fetch_file_to_attach():
    pathTo = os.getcwd()
    pathList = pathTo.split('/')

    #     del pathList[-1]
    #     pathTo = '/'.join(pathList) + '/Reports/'
    path = '/'.join(pathList) + '/Reports/'
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)

    newest = files[-1]

    print '*' * 40

    #     b = max(a,key = os.path.getctime)
    print "Latest Report File: ", newest
    print '*' * 40
    filesize = os.path.getsize(newest)
    if filesize != 0:
        return newest
    else:
        return False


def scandirs():
    pathTo = os.getcwd()
    pathList = pathTo.split('/')

    del pathList[-1]
    pathTo = '/'.join(pathList) + '/libraries'
    for root, dirs, files in os.walk(pathTo):
        for currentFile in files:

            exts = ('.html')
            if any(currentFile.lower().endswith(ext) for ext in exts):
                print "Deleting the Report file: " + currentFile
                os.remove(os.path.join(root, currentFile))


toAddress = ['jayakumar.muniswamy@lnttechservices.com', 'vaibhavx.agarwal@intel.com']
send_mail('austonio.ihealth@gmail.com', toAddress, 'Intel@123', "Test", 'smtp.gmail.com')