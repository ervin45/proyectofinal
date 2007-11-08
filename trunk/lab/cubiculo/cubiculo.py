
class Cubiculo:
	def __init__(self,ft, dimensions, measures):
		self.ft = ft
		self.dimensions = dimensions
		self.measures = measures

	def drill(self, dimension, nivel, restriccion):
		rtn = []
		for a in self.dimensions:
			if a[0] == dimension:
				rtn.append([a[0],nivel,restriccion])
			else:
				rtn.append(a)
		self.dimensions = rtn

	def sql(self):

		ft = "ft_%s" % self.ft
		sfrom = "from %s" % ft

		joins = ''
		levels = []
		where = []
		for dim in self.dimensions:
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



