#!/usr/bin/env python

import argparse
import sys
import base64

from mailbot import oauthCredentialHandler, oauthSend, legacySend, util

time_between_attempts = 60
max_attempts = 10

def getSender(args):
    if args.email is not None:
        sender = args.email
    else:
        sender = input("Sender email: ")
    return sender

def parseArgs(args):

    parser = argparse.ArgumentParser(description="Send email from the command line")
    parser.add_argument("-t", "--to", action='append')
    parser.add_argument("-c", "--carbon", action='append', default=[])
    parser.add_argument("-b", "--blind", action='append', default=[])

    parser.add_argument("-s", "--subject", action='store')
    parser.add_argument("-a", "--attach", action='append', default=[])

    parser.add_argument("-e", "--email", action='store')
    parser.add_argument("-p", "--password", action='store')
    parser.add_argument("--spoof", action='store')

#    parser.add_argument("--phone", action='append', default = [])
#    parser.add_argument("--provider", action='store')

    parser.add_argument("-d", "--delete-file", action='store_true', default=False)

    parser.add_argument("--retry-pause", type=int, action='store', default=time_between_attempts)
    parser.add_argument("--max-attempts", type=int, action='store', default=max_attempts)
    parser.add_argument("--delay", type=int, action='store', default=-1)
    parser.add_argument("--print-raw", action='store_true')

    parser.add_argument("--legacy", action='store_true', default=False)
    parser.add_argument("--auth-only", action='store_true', default=False)

    parser.add_argument("-m", "--message", action='append', default=[])
    parser.add_argument("-f", "--file", action='append', default=[])

    return parser.parse_args(args)

def main(args=sys.argv[1:]):
    args = parseArgs(args)
    if args.auth_only:
        authenticate(args)
    else:
        send_mail(args)

def authenticate(args):
    sender = getSender(args)
    if args.legacy:
        pass
    else:
        sender = getSender(args)
        oauthCredentialHandler.getCredentials(sender)
        print("Done")

def send_mail(args):
    vals, message = util.buildMessage(args)
    if args.legacy:
        legacySend.sendMessageLoop(args, vals['sender'], vals['visible_sender'], vals['password'], vals['to'], message)
    else:
        credentials = oauthCredentialHandler.getCredentials(vals['sender'])
        build = oauthCredentialHandler.getServiceInstance(credentials)
        util.pause(args.delay)
        if args.print_raw:
            print(message)
        oauthSend.sendMessageLoop(args, build, vals['sender'], {'raw': base64.urlsafe_b64encode(message.encode()).decode()})

if __name__ == '__main__':
    main(sys.argv[1:])
