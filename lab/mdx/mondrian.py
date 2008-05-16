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

## intento usar SOAPpy para hacer la consultas
## pero no logro hacer que funcione correctamente


from SOAPpy import SOAPProxy
from SOAPpy import Types


url = 'http://localhost:8180/mondrian/xmla'
n= 'urn:schemas-microsoft-com:xml-analysis'
server = SOAPProxy(url,n)

# if you want to see the SOAP message exchanged
# uncomment the two following lines
server.config.dumpSOAPOut = 1
#server.config.dumpSOAPIn = 1


cmd = {'Statement': Types.untypedType('SELECT [Measures].MEMBERS ON COLUMNS FROM [Sales]')}

prts={
    'PropertyList': {
    'DataSourceInfo':Types.untypedType('Provider=Mondrian;DataSource=MondrianFoodMart;'),
    'Catalog':Types.untypedType('FoodMart'),
    'Format':Types.untypedType('Multidimensional'),
    'AxisFormat':Types.untypedType('ClusterFormat')
    }
    }

#server.Execute(Command=cmd, Properties=prts)
#server._callWithBody({'Excecute':{'Command':cmd, 'Properties':prts}})

restr={
    'ns1:RestrictionList': {
    'CATALOG_NAME':Types.untypedType('FoodMart')
    }
    }

prts2={
    'ns1:PropertyList': {
    'ns1:Catalog':Types.untypedType('FoodMart'),
    'ns1:Format':Types.untypedType('Tabular'),
    }
    }


#server.namespace='urn:schemas-microsoft-com:xml-analysis'
#server.Discover(RequestType=Types.untypedType('DBSCHEMA_CATALOGS'), Restrictions=None, Properties=None)




import pprint
pprint.pprint(dir(server))

