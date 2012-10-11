#!/usr/bin/python
#

import ConfigParser, os
import sys
import clickatell_lib
#import urllib

class sms_sender:
  def __init__(self,config):
    self.username=config.get("clickatell","username")
    self.password=config.get("clickatell","password")
    self.auth_code=config.get("clickatell","auth_code")
    self.url=config.get("clickatell","url")
    self.pause_before_check=config.get("clickatell","pause_before_check")
    self.clickatell=clickatell_lib.Clickatell(self.username,self.password,self.auth_code)

  def send(self,text_str,recipient):
    self.clickatell.auth()
    if not self.clickatell.ping():
      print "There was an error while connecting to the service"
      return False

    print "ping works"

    #  recipient='+972-52-2284657'
    recipient=recipient.replace("-","")

    # Due to SPAM complaints, Clickatell does not allow to specify arbitrate
    # sender without registering it first.
    # 'sender':'hobbit',

    # On linux incoming string is of utf-8 encoding
    text_utf8=text_str.decode('utf-8')

    message={'to':recipient,
             'text':text_utf8,
             'msg_type':'SMS_TEXT',
             'sender':'',
             'climsgid': 'random_md5_hash'}
    #print urllib.unquote(text_utf8).decode('utf8')
    if self.clickatell.sendmsg(message):
      print "Sent."
    else:
      print "There was an error while sending the message"

if __name__ == '__main__':
  text_str=sys.argv[1]
  recipient=sys.argv[2]

  config = ConfigParser.ConfigParser()
  #config.readfp(open('defaults.cfg'))
  config.read(['pysms.cfg', os.path.expanduser('~/.myapp.cfg')])

  sms=sms_sender(config)
  sms.send(recipient,text_str)
