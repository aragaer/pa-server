#!/usr/bin/env python3
"Send hardcoded message using LMTP"
import configparser
import os
import smtplib

message = "Привет".encode()

this_dir = os.path.dirname(__file__)
conf_path = os.path.join(this_dir, 'features', 'server.conf')

config = configparser.ConfigParser()
config.read(conf_path)

sender = config['client']['login']+'@human'
receiver = config['pa']['login']

srv = config['server']
try:
    smtpObj = smtplib.LMTP(srv['host'], port=srv['send'])
    #smtpObj.login(config['pa']['login'], config['pa']['pass'])
    smtpObj.sendmail(sender, receiver, b'\r\n'+message)
    print("Successfully sent email")
except smtplib.SMTPException as ex:
    print("Error: unable to send email", ex)
