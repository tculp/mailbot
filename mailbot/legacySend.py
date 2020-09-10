import time
import os
import smtplib
import socket

from mailbot import util

def sendMessage(sender, visible_sender, password, receiver, message):
    socket.setdefaulttimeout(None)
    if sender.split('@')[1] == 'gmail.com':
        HOST = "smtp.gmail.com"
        PORT = "587"
    elif sender.split('@')[1] == 'yahoo.com':
        HOST = "smtp.mail.yahoo.com"
        PORT = "587"
    else:
        raise Exception("Unknown @ field")

    try:
        server = smtplib.SMTP()
        server.connect(HOST, PORT)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
        server.close()
        return True
    except socket.gaierror:
        return False

def sendMessageLoop(args, sender, visible_sender, password, receiver, message):
    success = sendMessage(sender, visible_sender, password, receiver, message)

    attempt_count = 1

    while not success and attempt_count < args.max_attempts:
        print("Not connected to the internet, trying again in %i seconds..." % args.retry_pause)
        time.sleep(args.retry_pause)
        success = sendMessage(sender, visible_sender, password, receiver, message)
        attempt_count += 1

    if success:
        print("Message Sent!")
        if args.delete_file:
            for f in args.file:
                if os.path.isfile(f):
                        os.remove(f)
    else:
        print(util.buildErrorMessage())
        file = open(os.path.join(os.path.expanduser('~'), 'mailbot.error'), 'a')
        file.write(util.buildErrorMessage())
        file.close()
