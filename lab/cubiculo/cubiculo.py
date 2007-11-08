
class Cubiculo:
	def __init__(self,ft, dimensions, measures):
		self.ft = ft
		self.dimensions = {}
		for a in dimensions:
			self.dimensions[a[0]] = a
		self.measures = measures

	def drill(self, dimension, nivel, restriccion):
		""" operacion primitiva para hacer el drilldown, drillup y slice"""
		self.dimensions[dimension] = [dimension, nivel, restriccion]

	def sql(self):
		""" devuelve el SQL """
		ft = "ft_%s" % self.ft
		sfrom = "from %s" % ft

		joins = ''
		levels = []
		where = []
		for dim in self.dimensions.values():
			(name, level, restriction) = dim
		
			joins += "join td_%s on (%s.fk_%s = td_%s.id) " % (name, ft, name, name)
			levels.append("td_%s.%s" % (name,level))
			if restriction:
				where.append(restriction)

		group_by = 'group by ' + ', '.join(levels)
		if where:
			where = "where " + ' and '.join(where)
		else:
			where = ""

		select = "select " + ','.join(levels) + ',' + ','.join(self.measures) 

		sql = """
%s
%s
%s
%s
%s""" % (select,sfrom, joins,where,group_by)

		return sql



