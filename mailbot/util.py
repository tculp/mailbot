import datetime
import time
import mimetypes
import os

from getpass import getpass

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def buildErrorMessage():
    return "%s - Unable to send message..." % datetime.datetime.now()

def pause(delay):
    if delay <= 0:
        return
    start = datetime.datetime.now()
    current = datetime.datetime.now()
    while (current - start).seconds < delay:
        time.sleep(1)
        current = datetime.datetime.now()

def buildMessage(args):
    vals = {}
    vals['to'] = []
    vals['subject'] = ''
    vals['sender'] = ''
    vals['visible_sender'] = ''
    vals['password'] = ''
    vals['message'] = ''

    if args.to is not None:
        vals['to'] = args.to
    else:
        vals['to'] = input("To: ").replace(',', ' ').split(' ')

    if args.subject is not None:
        vals['subject'] = args.subject
    else:
        vals['subject'] = input("Subject: ")

    if args.email is not None:
        vals['sender'] = args.email
    else:
        vals['sender'] = input("Sender email: ")

    if args.spoof is not None:
        vals['visible_sender'] = args.spoof
    else:
        vals['visible_sender'] = vals['sender']

    if args.legacy and args.password is None:
        vals['password'] = getpass()


    for f in args.file:
        if os.path.isfile(f):
            args.message.append(open(f, 'r').read())
        else:
            raise Exception("Invalid file given: %s" % args.file)

    for m in args.message:
        vals['message'] += "%s\n" % m

    if len(vals['message']) == 0:
        message = input("Message: ")


    outer = MIMEMultipart()
    outer['Subject'] = vals['subject']
    outer['To'] = ','.join(vals['to'])
    outer['CC'] = ','.join(args.carbon)
    outer['From'] = vals['visible_sender']
    outer.attach(MIMEText(vals['message'], 'plain'))

    for attached_file in args.attach:

        if os.path.isfile(attached_file):
            ctype, encoding = mimetypes.guess_type(attached_file)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)

            if maintype == "text":
                fp = open(attached_file)
                # Note: we should handle calculating the charset
                attachment = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "image":
                fp = open(attached_file, "rb")
                attachment = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "audio":
                fp = open(attached_file, "rb")
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(attached_file, "rb")
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=attached_file)
            outer.attach(attachment)
        else:
            print(os.path.isfile(attached_file))
            raise Exception("Invalid file given: %s" % attached_file)

    return vals, outer.as_string()
