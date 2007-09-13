#!/bin/sh

##esta es la consulta tal cual la hace openi para descubrir datasources

cat << EOF | POST -c text/xml http://localhost:8180/mondrian/xmla
<?xml version="1.0" encoding="UTF-8"?> 
<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/"> 
<soap-env:Header/> 
<soap-env:Body> 
<Discover  xmlns="urn:schemas-microsoft-com:xml-analysis"> 
<RequestType>DISCOVER_DATASOURCES</RequestType> 
 <Restrictions> 
 <RestrictionList/> 
 </Restrictions> 
 <Properties> 
 <PropertyList> 
 <Content>Data</Content> 
 </PropertyList> 
 </Properties> 
 </Discover> 
 </soap-env:Body> 
</soap-env:Envelope> 
EOF
