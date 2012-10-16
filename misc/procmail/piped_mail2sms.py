#!/usr/bin/python
#
# Get subject from stdin email and send it as SMS
#
# Author: Arie Skliarouk <skliarie@gmail.com>
#
# The script is to be launched from .forward-sms file (or similar)
# it relies on arapim project to be located in /opt/arapim directory

import sys,os
import subprocess

phone_number=sys.argv[1];

def get_subject():
  for line in sys.stdin.readlines():
    if line.startswith("Subject: "):
      return line[9:].rstrip()

  sys.exit(1)

message=get_subject()

os.chdir("/opt/arapim")
code = subprocess.Popen(["/opt/arapim/send_sms.py", message, phone_number], stdout=subprocess.PIPE)
for line in code.stdout:
  print line
code.stdout.close()

