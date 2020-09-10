import time
import os

from mailbot import util

def sendMessage(build, sender, message):
    message = (build.users().messages().send(userId=sender, body=message)
            .execute())
    return message

def sendMessageLoop(args, build, sender, message):
    result = sendMessage(build, sender, message)

    attempt_count = 1

    while result == False and attempt_count < args.max_attempts:
        print("Not connected to the internet, trying again in %i seconds..." % args.retry_pause)
        time.sleep(args.retry_pause)
        result = sendMessage(build, sender, message)
        attempt_count += 1

    if result != False:
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
