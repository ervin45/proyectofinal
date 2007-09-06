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

server.namespace='ns1'
server.Discover(RequestType=Types.untypedType('MDSCHEMA_CUBES'))


###
### Genera la peticion
# <?xml version="1.0" encoding="UTF-8"?>
# <SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
# <SOAP-ENV:Body>
# <ns1:Discover xmlns:ns1="ns1" SOAP-ENC:root="1">
# <RequestType>MDSCHEMA_CUBES</RequestType>
# </ns1:Discover>
# </SOAP-ENV:Body>
# </SOAP-ENV:Envelope>
