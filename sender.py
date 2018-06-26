#!/usr/bin/env python3
import configparser
import os
import smtplib

sender = 'malena@brain'
receivers = ['aragaer']

message = "Приветик".encode()

this_dir = os.path.dirname(__file__)
conf_path = os.path.join(this_dir, 'features', 'server.conf')

config = configparser.ConfigParser()
config.read(conf_path)

srv = config['server']
try:
    smtpObj = smtplib.SMTP(srv['host'], port=srv['send'])
    smtpObj.sendmail(sender, receivers, message)         
    print("Successfully sent email")
except smtplib.SMTPException as ex:
    print("Error: unable to send email", ex)
