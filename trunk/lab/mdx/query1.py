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


print query_mondrian("SELECT Gender.MEMBERS ON COLUMNS FROM Sales")

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


print query_mondrian("SELECT Gender.MEMBERS ON COLUMNS FROM Sales")

