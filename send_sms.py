#!/usr/bin/python

import ConfigParser, os, sys

config = ConfigParser.ConfigParser()
#config.readfp(open('defaults.cfg'))
config.read(['arapim.cfg', os.path.expanduser('~/.myapp.cfg')])

if len(sys.argv)==1:
  print "Usage: send_sms [message text] [phone number]"
  sys.exit(1)
  
text_str=sys.argv[1]
recipient=sys.argv[2]

# TBD: Detect best SMS provider to send SMS through
# For now just hardcode the whole thing
assert(recipient[0]=="+")
recipient=recipient.replace("-","")

# TBD: Verify that a given provider is configured in the configuration file before using it
if recipient[:4]=="+972":
  print "Debug: using provider cellact"
  import cellact
  sms=cellact.sms_sender(config)
elif recipient[:2]=="+1":
  print "Debug: using provider cdyne"
  import cdyne
  sms=cdyne.sms_sender(config)
else:
  print "Debug: using provider clickatell"
  import clickatell

  sms=clickatell.sms_sender(config)

result=sms.send(text_str,recipient)
