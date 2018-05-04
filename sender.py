#!/usr/bin/env python3
import smtplib

sender = 'malena@brain'
receivers = ['aragaer']

message = "Приветик".encode()

try:
    smtpObj = smtplib.SMTP('127.0.0.1', port=8006)
    smtpObj.sendmail(sender, receivers, message)         
    print("Successfully sent email")
except smtplib.SMTPException as ex:
    print("Error: unable to send email", ex)
