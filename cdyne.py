#!/usr/bin/python
#
# cdyne (http://www.cdyne.com/api/phone/sms/) SMS sending service
#

# suds.client can't be used due to bug https://fedorahosted.org/suds/ticket/239#comment:22
#from suds.client import Client

import sys,os
import urllib
import ConfigParser

class sms_sender:
  def __init__(self,config):
    self.username=config.get("cdyne","username")
    self.password=config.get("cdyne","password")
    self.auth_code=config.get("cdyne","auth_code")
    self.url=config.get("cdyne","url")
    self.pause_before_check=config.get("cdyne","pause_before_check")
    #self.clickatell=clickatell_lib.Clickatell(self.username,self.password,self.auth_code)
    self.message_sent=False

  def send(self,text_str,recipient):
    get_args_raw = {"Message":text_str
                   ,"PhoneNumber":recipient
                   ,"LicenseKey":self.auth_code}
    get_args=urllib.urlencode(get_args_raw)
    
    url = self.url+"?"
    url+= get_args

#    print url
    handle=urllib.urlopen(url)
    body=" ".join(handle.readlines())
#    print body

#  def send(self,text_str,recipient):
#    recipient=recipient.replace("-","")
##    client = Client(url=self.url+"?wsdl",location=self.url)
#    wsdl_url=self.url+"?wsdl"
#    #wsdl_url="http://www.webservicex.net/stockquote.asmx?WSDL"
#    client = SOAPProxy(wsdl_url)
#    client.config.debug = 1
#    params = {"PhoneNumber":recipient
#             ,"LicenseKey" :self.auth_code
#             ,"Message"    :text_str
#             }
#
#    res = client.SimpleSMSsend(params)
#    return True
#    res = res->SimpleSMSsendResult

"""
TBD: analyse requests and get sent_status for each message

          $data = array(
                    'SendTime'        =>  date(DATE_FORMAT_DATA)
                  , 'CMTS_REQUEST_ID' =>  $GLOBALS['CMTS_REQUEST_ID']
                  , 'MessageID' =>  $res->MessageID
                );
        if (  true
            && $res->Queued
            && $res->SMSError == 'NoError'
           ) {
          $message_id = $res->MessageID;
          do_syslog(info,"SMS SENT VIA CDYNE recipient=[$recipient] MessageID=[$message_id]",SMS_LOGSOURCE);
        }

        if ($prov_data->PauseB4Check) {
          sleep($prov_data->PauseB4Check);

          $input = array(
                      'message_id'  =>  $message_id
                    , 'prov_data'   =>  $prov_data
                  );
          $res = $this->GetMessageStatus($input);
          $status = $res['data'];
          if (   false
              || $status['Sent'] == 'False'
              || $status['SMSError'] != 'NoError'
             ) {
            $level = error;
            do_syslog($level,"SMS NOT SENT VIA CDYNE recipient=[$recipient] \$status=".var_export($status,true), SMS_LOGSOURCE);
            $data = array_merge($data, array(
                            'Sent'      =>  $status['Sent']
                          , 'SMSError'  =>  $status['SMSError']
                        )
                      );
            throw new Exception(error_logtext(ERR_SMSFAIL) . " CDYNE recipient=[$recipient] message_id=[$message_id]", ERR_SMSFAIL);
          }
        }
        $result =  $this->makeOKResponse (__FUNCTION__, $status);
      }
      catch (Exception $ex) {
        $result = $this->makeErrorResponse (__FUNCTION__, $ex, false, get_defined_vars());
        $result['info'] = $data;
      }
"""

if __name__ == '__main__':
  text_str=sys.argv[1]
  recipient=sys.argv[2]

  config = ConfigParser.ConfigParser()
  #config.readfp(open('defaults.cfg'))
  config.read(['pysms.cfg', os.path.expanduser('~/.myapp.cfg')])

  sms=sms_sender(config)
  sms.send(text_str,recipient)
