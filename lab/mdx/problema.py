#!/usr/bin/env python

from SOAPpy import SOAPProxy
from SOAPpy import Types

url = 'http://localhost:8180/mondrian/xmla'
n= 'urn:schemas-microsoft-com:xml-analysis'
server = SOAPProxy(url,n)

# if you want to see the SOAP message exchanged
# uncomment the two following lines

server.config.dumpSOAPOut = 1
#server.config.dumpSOAPIn = 1

server.Discover(RequestType=Types.untypedType('MDSCHEMA_CUBES'))
