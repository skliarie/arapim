#!/usr/bin/python
#
# SMS compacter and remailer daemon
#
# Author: Arie Skliarouk
#
# * SMS Compacter
#   Some failures cause several short messages to be sent at once.
#   Frequently the messages might be combined into single 159 chars SMS.
#
# * SMS Remailer
#   SMSes are often needs to be sent to group of people. This
#   script gets all numbers from db lookup and sends SMS to each recepient.
#
# Usage:
#  To send a message to given group, create a new file in the watchdir/group/
#  or move new file into the directory
#

import pyinotify  # apt-get install python-pyinotify
import time
import os
#from subprocess import call
import subprocess

# Monitor the /var/tmp/xymon_sms directory using inotify
watchdir = "/var/tmp/xymon_sms"

fp_contacts = "/usr/local/bin/contacts.txt"
if not os.path.exists(fp_contacts):
    fp_contacts = "contacts.txt"

#in seconds
TIME_TO_WAIT_FOR_MSGS = 3


class WatchList():
    last_rcvd = dict()
    messages = dict()
    groups_numbers = dict()

    def __init__(self, watchdir):
        # on start scan the watched directories and add files in it to the
        # watchlist
        for root, subFolders, files in os.walk(watchdir):
            for file in files:
                self.add_file(os.path.join(root, file))

    def add_file(self, fpFile):
        if os.path.isdir(fpFile) is True:
            return
        message = open(fpFile, "r").read(8192).rstrip()
        os.unlink(fpFile)
        # Group is name of the last directory in fpFile
        group = fpFile.split("/")[-2]
        self.messages.setdefault(group, []).append(message)
        self.last_rcvd[group] = time.time()
        print "got file[%s] group[%s] message [%s]" % (fpFile, group, message)

    def send_sms(self, group, message):
        for phone in self.groups_numbers[group]:
            return_code = subprocess.check_call(['/usr/local/bin/sendsms.sh',
                                                message,
                                                phone],
                                                stderr=subprocess.STDOUT)
            if return_code > 0:
                # Signal to wrapper to send email
                os.exit(1)

    def compact_send_smses(self, group):
        self.update_group_numbers()
        print "Sending msg to group [%s]" % group
        if group in self.groups_numbers:
            print "Send msg to phones[%s]" % self.groups_numbers[group]
            print "message [%s]" % str(self.messages[group])
            big_msg = ""
            separator = ""
            for msg in self.messages[group]:
                if len(big_msg) + 1 + len(msg) > 159:
                    self.send_sms(group, big_msg)
                    big_msg = ""
                else:
                    big_msg += separator + msg
                    separator = "\n"

            if len(big_msg) > 0:
                self.send_sms(group, big_msg)

        self.last_rcvd.pop(group)
        self.messages.pop(group)
#    > /dev/null || echo There wa
#    s an error while sending sms [$(cat file)] to phone [$phone]

    def send_collected_smses(self):
        time_now = time.time()
        # send SMS for messages collected so far
        for group, s_last_seen in self.last_rcvd.items():
            if time_now > (s_last_seen + TIME_TO_WAIT_FOR_MSGS):
                self.compact_send_smses(group)

    def update_group_numbers(self):
        self.groups_numbers = dict()
        with open(fp_contacts) as f:
            for line in f:
                if not "|" in line:
                    continue
                (name, email, phone, groups) = line.split("|")
                groups = groups.rstrip()
                if len(groups) > 0:
                    for group in groups.split(","):
                        self.groups_numbers.setdefault(group, []).append(phone)
        #print self.groups_numbers

    def quick_check(self, notifier):
        assert notifier._timeout is not None, 'Bad timeout of Notifier'
        print ".",
        self.send_collected_smses()
        notifier.process_events()
        #loop in case more events appear while we are processing
        while notifier.check_events():
            notifier.read_events()
            notifier.process_events()


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, watchlist):
        pyinotify.ProcessEvent.__init__(self)
        self.watchlist = watchlist

    # Invoked on file creation
    def process_IN_CREATE(self, event):
        print "Creating:", event.pathname
        self.watchlist.add_file(event.pathname)

    # moved_to
    def process_IN_MOVED_TO(self, event):
        print "Moved to:", event.pathname
        self.watchlist.add_file(event.pathname)

if not os.path.exists(watchdir):
    os.mkdir(watchdir)
    print "Warning: Created directory [%s]" % watchdir

watchlist = WatchList(watchdir)
wm = pyinotify.WatchManager()
handler = EventHandler(watchlist)
notifier = pyinotify.Notifier(wm, default_proc_fun=handler, timeout=1000)
wm.add_watch(watchdir, pyinotify.IN_CREATE|pyinotify.IN_MOVED_TO, rec=True)
# Loop forever and handle events.
notifier.loop(callback=watchlist.quick_check)
