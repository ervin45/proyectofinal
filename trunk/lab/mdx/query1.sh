#!/bin/sh
##
## ejecuta la query:
## SELECT Measures.MEMBERS ON COLUMNS FROM Sales
##
## la salida está en salida1

cat << EOF | POST -c text/xml http://localhost:8180/mondrian/xmla
<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
<SOAP-ENV:Body>
  <Execute xmlns="urn:schemas-microsoft-com:xml-analysis">
   <Command>
    <Statement>SELECT Measures.MEMBERS ON COLUMNS FROM Sales</Statement>
   </Command>
   <Properties>
    <PropertyList>
    <DataSourceInfo>Provider=Mondrian;DataSource=MondrianFoodMart;</DataSourceInfo>
     <Catalog>FoodMart</Catalog>
     <Format>Multidimensional</Format>
     <AxisFormat>TupleFormat</AxisFormat>
    </PropertyList>
   </Properties>
  </Execute>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
EOF
