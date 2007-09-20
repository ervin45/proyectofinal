import urllib
import urllib2



def query_mondrian(stm):
    url = 'http://localhost:8180/mondrian/xmla'
    headers = { 'Content-Type' : 'text/xml' } 
    data = """<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Body>
      <Execute xmlns="urn:schemas-microsoft-com:xml-analysis">
       <Command>
        <Statement>%s</Statement>
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
    """ % stm
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page


print query_mondrian("SELECT Measures.MEMBERS ON COLUMNS FROM Sales")

