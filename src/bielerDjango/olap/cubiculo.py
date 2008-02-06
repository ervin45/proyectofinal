from pprint import pprint

class Cubiculo:
	def __init__(self,ft, dimensions, measures):
		self.ft = ft
		self.dimensions = {}
		for a in dimensions:
			self.add_dimension(a)
		self.dimensions_order = self.dimensions.keys()
		self.measures = measures
		
	def add_dimension(self, a):
		if len(a) == 2:
			a.append(None)
		self.dimensions[a[0]] = a

	def add_measure(self, m):
		self.measures.append(m)

	def drill(self, dimension, nivel, restriccion):
		""" operacion primitiva para hacer el drilldown, drillup y slice"""
		self.dimensions[dimension] = [dimension, nivel, restriccion]
		
	def pivot(self):
		pprint(self.dimensions_order)
		(self.dimensions_order[0], self.dimensions_order[1]) = (self.dimensions_order[1], self.dimensions_order[0])
		pprint(self.dimensions_order)
		
	def second_dimension_values(self):
		second_dimension = self.dimensions[self.dimensions_order[1]]
		sql = "select distinct(%s) from td_%s" % (second_dimension[1], second_dimension[0])
		return sql


	def sql(self):
		""" devuelve el SQL """
		ft = "ft_%s" % self.ft
		sfrom = "from %s" % ft

		joins = ''
		levels = []
		where = []
		
		for dimension in self.dimensions_order:
			(name, level, restriction) = self.dimensions[dimension]
		
			joins += "join td_%s on (%s.fk_%s = td_%s.id) " % (name, ft, name, name)
			levels.append("td_%s.%s" % (name,level))
			if restriction:
				where.append(restriction)

		group_by = 'group by ' + ', '.join(levels)
		if where:
			where = "where " + ' and '.join(where)
		else:
			where = ""

                t = ['%s(%s)' % (x[1],x[0]) for x in self.measures]

		select = "select " + ','.join(levels) + ',' + ','.join(t) 

		sql = """
%s
%s
%s
%s
%s""" % (select,sfrom, joins,where,group_by)
		print sql
		return sql


#c = cubiculo.Cubiculo('vendido',
#	[['Tiempo','anio'],
#	 ['Sucursal','sucursal',"sucursal = 'rafaela'"]],
#	['Cantidad'])
#print c.sql()
#c.drill('Tiempo','mes','anio=2007')
#print c.sql()



