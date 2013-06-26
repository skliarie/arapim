#!/usr/bin/python
#
# Send SMS from CLI using most appropriate SMS sending provider
#
# Author: Arie Skliarouk <skliarie@gmail.com>

import ConfigParser
import os
import sys

config = ConfigParser.ConfigParser()
#config.readfp(open('defaults.cfg'))
config.read(['arapim.cfg', os.path.expanduser('~/.myapp.cfg')])

if len(sys.argv) == 1:
    print "Usage: send_sms [message text] [phone number]"
    sys.exit(1)

text_str = sys.argv[1]
recipient = sys.argv[2]

# TBD: Detect best SMS provider to send SMS through
# For now just hardcode the whole thing
assert(recipient[0] == "+")
recipient = recipient.replace("-", "")

# TBD: Verify that a given provider is configured in the
# configuration file before using it
if recipient[:4] == "+972":
    provider="cellact"
    import cellact
    sms = cellact.sms_sender(config)
elif recipient[:2] == "+1":
    provider="cdyne"
    import cdyne
    sms = cdyne.sms_sender(config)
else:
    provider="clickatell"
    import clickatell

    sms = clickatell.sms_sender(config)

print "Debug: got number [%s], using provider [%s]" % (recipient, provider)

result = sms.send(text_str, recipient)
