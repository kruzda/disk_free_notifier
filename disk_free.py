#!/usr/bin/env python3
import shutil
import smtplib

alert_state_file = '/home/k/disk_space_notification_status'

def notify(dfr):
    fr = "eth-node <eth-node@kuk.ac>"
    to = "crs666@gmail.com"
    msg = "From: {}\r\nTo: {}\r\n".format(fr, to)
    msg += "Subject: Disk space alert\r\n\r\n"
    msg += "Free disk space is {}%".format(int(dfr * 100))
    smtp_session = smtplib.SMTP('localhost')
    smtp_session.sendmail(fr, to, msg)
    smtp_session.close()
    with open(alert_state_file, "w") as f:
        f.write('sent')

def check():
    disk_usage = shutil.disk_usage('/')
    disk_free_ratio = disk_usage.free / disk_usage.total
    if disk_free_ratio < 0.10:
        print("free disk space is low: {}%".format(
              int(disk_free_ratio * 100)))
        with open(alert_state_file) as f:
            if "sent" not in f.readlines():
                print('notification not yet sent, trying to send now')
                notify(disk_free_ratio)
            else:
                print("already sent notification")
    else:
        print('disk space usage nominal')

if __name__ == "__main__":
    check()
