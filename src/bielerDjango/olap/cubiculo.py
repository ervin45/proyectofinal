from pprint import pprint

class Meta:
	def __init__(self):
		self.dimension_meta = {'pieza':['codigo',
										'modificacion',
										'modelo', 
										'grupo_constructivo'],
							   'tiempo':['mes', 'anio']}

	def previous(self, dimension, nivel):
		index = self.dimension_meta[dimension].index(nivel)
		result = self.dimension_meta[dimension][index - 1:index]
		if result == []:
			result = nivel
		else:
			result = result[0]
		return result

	def next(self, dimension, nivel):
		index = self.dimension_meta[dimension].index(nivel)
		result = self.dimension_meta[dimension][index + 1:index + 2]
		if result == []:
			result = nivel
		else:
			result = result[0]
		return result

	def parent_list(self, dimension, nivel):
		niveles = self.dimension_meta[dimension]
		result = niveles[niveles.index(nivel):]
		result.reverse()
		return result


'''
Las restricciones dentro de las dimensiones seran un hash. Una key
por cada elemento de la dimension y como value un lista de valores 
permitidos

anio: [2000, 2002, 2007], mes: [12, 11]

where anio in (2000, 2002, 2007) and mes in (12,11)
'''
class Cubiculo:
	def __init__(self,ft, dimensions, measures):
		self.ft = ft
		self.dimensions = {}
		for a in dimensions:
			self.add_dimension(a)
		self.dimensions_order = self.dimensions.keys()
		self.measures = measures
		self.meta = Meta()

	def add_dimension(self, a):
		if len(a) == 2:
			a.append({})
		self.dimensions[a[0]] = a

	def add_measure(self, m):
		self.measures.append(m)
		
	def add_restriction(self, dimension, nivel, value):
		if not self.dimensions[dimension][2].has_key(nivel):
			self.dimensions[dimension][2][nivel] = [value] 
		else:
			self.dimensions[dimension][2][nivel].append(value)

	def del_restriccion(self, dimension):
		self.dimensions[dimension][2] = {}


	def drill(self, axis):
		dimension = self.dimensions_order[int(axis)]
		nivel = self.dimensions[dimension][1]
		nuevo_nivel = self.meta.previous(dimension, nivel)
		self.dimensions[dimension][1] = nuevo_nivel

	def roll(self, axis):
		dimension = self.dimensions_order[int(axis)]
		nivel = self.dimensions[dimension][1]
		nuevo_nivel = self.meta.next(dimension, nivel)
		self.del_restriccion(dimension)
		self.dimensions[dimension][1] = nuevo_nivel

	def pivot(self):
		(self.dimensions_order[0], self.dimensions_order[1]) = (self.dimensions_order[1], self.dimensions_order[0])

	def dimension_values(self, axis):
		first_dimension = self.dimensions[self.dimensions_order[int(axis)]]
		levels_parent = self.meta.parent_list(first_dimension[0], first_dimension[1])
		select = "|| ' - ' ||".join(levels_parent)
		campos = ", ".join([x for x in levels_parent])
		
		pprint(first_dimension)
		where = "%s" % " and ".join(["td_%s.%s in(%s)" % ( first_dimension[0], nivel, ", ".join(val)) for nivel, val in first_dimension[2].items()])
		if where:
			where = "where %s" % where
		sql = "select distinct(%s), %s from td_%s %s order by %s" % (select, campos, first_dimension[0], where, campos)
		print sql
		return sql			

	def drill_replacing(self, axis, value):
		nivel = self.dimensions[self.dimensions_order[int(axis)]][1]
		dimension = self.dimensions[self.dimensions_order[int(axis)]]
		self.del_restriccion(dimension[0])
		
		values = value.split(" - ")
		niveles = self.meta.parent_list(dimension[0], nivel)
		
		for nivel, value in zip(niveles, values):
			self.add_restriction(dimension[0], nivel, value)
		self.drill(axis)

	def drill_replacing2(self, value0, value1):
		self.drill_replacing(0, value0)
		self.drill_replacing(1, value1)

	def sql(self):
		""" devuelve el SQL """
		ft = "ft_%s" % self.ft
		sfrom = "from %s" % ft

		joins = ''
		levels_with_parent = []
		where = []

		for dimension in self.dimensions_order:
			(name, level, restriction) = self.dimensions[dimension]

			joins += "join td_%s on (%s.fk_%s = td_%s.id) " % (name, ft, name, name)
			levels_with_parent.append(self.meta.parent_list(name, level)) 
			if restriction:
				where.extend(["td_%s.%s in(%s)" % ( name, nivel, ", ".join(val)) for nivel, val in restriction.items()])

		group_by = 'group by ' + ', '.join([", ".join(x) for x in levels_with_parent])
		order_by = "order by %s " % ', '.join([", ".join(x) for x in levels_with_parent])
		if where:
			where = "where %s " % ' and '.join(where)
			#where = "where %s " % ' and '.join(where)
		else:
			where = ""

                t = ['%s(%s)' % (x[1],x[0]) for x in self.measures]


		select = "select %s, %s"  % (','.join(["|| ' - ' ||".join(x) for x in levels_with_parent])
									,  ','.join(t)) 

		
		sql = """
%s
%s
%s
%s
%s
%s
""" % (select,sfrom, joins,where,group_by, order_by)
		print sql

		return sql


#c = cubiculo.Cubiculo('vendido',
#	[['Tiempo','anio'],
#	 ['Sucursal','sucursal',"sucursal = 'rafaela'"]],
#	['Cantidad'])
#print c.sql()
#c.drill('Tiempo','mes','anio=2007')
#print c.sql()



