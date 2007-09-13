#!/bin/sh
##
## un test rápido para ver los requerimientos SOAP que inconvenientes tienen...
##

cat << EOF | POST -c text/xml http://localhost:8180/mondrian/xmla
<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
<SOAP-ENV:Body>
<Discover xmlns="urn:schemas-microsoft-com:xml-analysis" SOAP-ENC:root="1">
<RequestType>DBSCHEMA_CATALOGS</RequestType>
<Restrictions />
<Properties>
<PropertyList>
 <DataSourceInfo>Provider=Mondrian;DataSource=MondrianFoodMart;</DataSourceInfo>
 <Format>Tabular</Format>
</PropertyList>
</Properties>
</Discover>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
EOF
