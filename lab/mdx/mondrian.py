#!/usr/bin/env python

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

