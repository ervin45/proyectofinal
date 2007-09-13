#!/bin/sh

## este script reproduce el error:
##
## The Mondrian XML: Mondrian Error:Internal error: no data source is configured with name &#39;null&#39;

cat << EOF | POST -c text/xml http://localhost:8180/mondrian/xmla
<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
<SOAP-ENV:Body>
<Discover xmlns="urn:schemas-microsoft-com:xml-analysis">
<RequestType>DBSCHEMA_CATALOGS</RequestType>
<Restrictions />
<Properties />
</Discover>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
EOF
