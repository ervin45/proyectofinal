#!/usr/bin/env python
#############################################################################
#
#    Sistema de soporte de decisiones para Ricardo Bieler S.A.
#    Copyright (C) 2007-2008 Nicolas D. Cesar, Mariano N. Galan
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

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

#####
### Genera la peticion
# <?xml version="1.0" encoding="UTF-8"?>
# <SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
# <SOAP-ENV:Body>
# <ns1:Discover xmlns:ns1="urn:schemas-microsoft-com:xml-analysis" SOAP-ENC:root="1">
# <RequestType>MDSCHEMA_CUBES</RequestType>
# </ns1:Discover>
# </SOAP-ENV:Body>
# </SOAP-ENV:Envelope>
