#!/bin/sh

if [ $# -lt 1 ]
then
	echo "uso: $0 [CONSULTA MDX]"
	exit
fi


cat << EOF | POST -c text/xml http://localhost:8180/mondrian/xmla
<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
<SOAP-ENV:Body>
  <Execute xmlns="urn:schemas-microsoft-com:xml-analysis">
   <Command>
    <Statement>$*</Statement>
   </Command>
   <Properties>
    <PropertyList>
    <DataSourceInfo>Provider=Mondrian;DataSource=MondrianFoodMart;</DataSourceInfo>
     <Catalog>FoodMart</Catalog>
     <Format>Tabular</Format>
     <AxisFormat>TupleFormat</AxisFormat>
    </PropertyList>
   </Properties>
  </Execute>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
EOF
