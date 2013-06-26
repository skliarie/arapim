#!/bin/bash
#
# Wrapper to run sms_cr.py, to be launched from cron, hourly
#
# Author: Arie Skliarouk
#
# This way if something happens with sms_cr, someone will get email
# on that.

pids=$(pidof -x sms_cr.py)

if [ -n "$pids" ];
then
  exit 0
fi

while [ 1 ];
do
    /opt/arapim/sms_cr.py &> /tmp/sms_cr.stdboth
    if [ $? -gt 0 ];
    then
        cat /tmp/sms_cr.stdboth
    fi
    sleep 10
done

