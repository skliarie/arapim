#!/usr/bin/python

import ConfigParser
import xmpp # apt-get install python-xmpp
import sys,os

if __name__ == '__main__':

  if len(sys.argv)==1:
    print "Usage: jabber_send.py [message] [recipient]"
    sys.exit(1)
  message=sys.argv[1]
  recipient=sys.argv[2]

  config = ConfigParser.ConfigParser()
  config.read(['arapim.cfg', os.path.expanduser('~/.myapp.cfg')])

  login=config.get("jabber","login")
  password=config.get("jabber","password")
  client=config.get("jabber","client")
  server=config.get("jabber","server")
  port=config.get("jabber","port")

  cnx = xmpp.Client(client,debug=[])
  cnx.connect( server=(server,int(port)) )
  cnx.auth(login,password, 'botty')

  cnx.send( xmpp.Message( recipient, message ) )
