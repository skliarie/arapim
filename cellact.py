#!/usr/bin/python
#

import ConfigParser, os,sys
import urllib

class sms_sender:
  def __init__(self,config):
    self.username=config.get("cellact","username")
    self.password=config.get("cellact","password")
    self.auth_code=config.get("cellact","auth_code")
    self.url=config.get("cellact","url")
    self.pause_before_check=config.get("cellact","pause_before_check")
    #self.clickatell=clickatell_lib.Clickatell(self.username,self.password,self.auth_code)
    self.message_sent=False

  def send(self,text_str,recipient):
    message = {"CONTENT":text_str}
    message_args=urllib.urlencode(message)
    
    # Cellact accepts phone numbers is local Israeli form
    #  '+972-52-2284657' -> '0522284657'
    recipient=recipient.replace("-","")
    assert(recipient[0:4]=="+972")
    recipient='0'+recipient[4:]

    # Message ID can be used for tracking delivery status
    message_id = 'CELLACT_12345';
    #      '&SENDER=6655'
    url = "%s?X=&FROM=%s&USER=%s&PASSWORD=%s&APP=LA&CMD=sendtextmt&"%(self.url,self.auth_code,self.username,self.password)
    url+= message_args
    url+= "&TO=%s"%recipient
    url+= "&SN=SMS&MSGID="+message_id

    handle=urllib.urlopen(url)
    body=" ".join(handle.readlines())

    # Success if body has <SESSION>...</SESSION>
    if '<SESSION>' in body:
      self.message_sent=True
    else:
      print "There was an error while retrieving URL [%s]"%url
      print "Result was [%s]"%body

if __name__ == '__main__':
  text_str=sys.argv[1]
  recipient=sys.argv[2]

  config = ConfigParser.ConfigParser()
  #config.readfp(open('defaults.cfg'))
  config.read(['pysms.cfg', os.path.expanduser('~/.myapp.cfg')])

  sms=sms_sender(config)
  sms.send(text_str,recipient)


"""
 FAILURE:
    0 => <PALO><RESULT>False</RESULT><DESCRIPTION>Xml Validation Error -- patt
ern constraint failed.
     1 => The element: \'TO\'  has an invalid value according to its data type.
     2 => '</DESCRIPTION></PALO>
 
  SUCCESS:
     0 => <PALO><RESULT>True</RESULT><SESSION>ad523373-0111-4154-b9b5-e328aadd4817</SESSION><OPTIONAL><MSG_ID>1348052170456220@d-n</MSG_ID><SERVICE_NAME>SMS</SERVICE_NAME></OPTIONAL></PALO>

"""

#        if (count($ret)>1) {
#          $data['Results']  = 'Failure';
#          $data['Reason']   = substr($ret[0],41);
#          $data['Description']  = $ret[1];
#          throw new Exception(error_logtext(ERR_SMSFAIL), ERR_SMSFAIL);
#        }
