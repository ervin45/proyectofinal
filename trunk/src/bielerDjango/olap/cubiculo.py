from pprint import pprint

class Meta:
	def __init__(self):
		self.dimension_meta = {'pieza':['grupo_constructivo', 
										'modelo', 
										'modificacion'],
							   'tiempo':['mes', 'anio']}
							
	def previous(self, dimension, nivel):
		prev = ''
		for next in self.dimension_meta[dimension]:
			if next == nivel:
				result = prev
			prev = next
			
		if result == '':
			result = nivel
				
		return result
	
	def next(self, dimension, nivel):
		from copy import copy
		prev = ''
		lista = copy(self.dimension_meta[dimension])
		lista.reverse()
		for next in lista:
			if next == nivel:
				result = prev
			prev = next
			
		if result == '':
			result = nivel
				
		return result
	
	def parent_list(self, dimension, nivel):
		niveles = self.dimension_meta[dimension]
		result = niveles[niveles.index(nivel):]
		result.reverse()
		return result
			

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
			a.append(None)
		self.dimensions[a[0]] = a

	def add_measure(self, m):
		self.measures.append(m)

	def drill(self, axis):
		dimension = self.dimensions_order[int(axis)]
		nivel = self.dimensions[dimension][1]
		nuevo_nivel = self.meta.previous(dimension, nivel)
		self.dimensions[dimension][1] = nuevo_nivel

	def roll(self, axis):
		dimension = self.dimensions_order[int(axis)]
		nivel = self.dimensions[dimension][1]
		nuevo_nivel = self.meta.next(dimension, nivel)
		self.dimensions[dimension][1] = nuevo_nivel
		
	def pivot(self):
		pprint(self.dimensions_order)
		(self.dimensions_order[0], self.dimensions_order[1]) = (self.dimensions_order[1], self.dimensions_order[0])
		pprint(self.dimensions_order)
		
	def second_dimension_values(self):
		second_dimension = self.dimensions[self.dimensions_order[1]]
		levels_parent = self.meta.parent_list(second_dimension[0], second_dimension[1])
		select = "|| ' - ' ||".join(levels_parent)
		sql = "select distinct(%s) from td_%s" % (select, second_dimension[0])
		return sql

	def sql(self):
		""" devuelve el SQL """
		ft = "ft_%s" % self.ft
		sfrom = "from %s" % ft

		joins = ''
		levels_with_parent = []
		levels = []
		where = []
		
		for dimension in self.dimensions_order:
			(name, level, restriction) = self.dimensions[dimension]
		
			joins += "join td_%s on (%s.fk_%s = td_%s.id) " % (name, ft, name, name)
			levels_with_parent.append(self.meta.parent_list(name, level)) 
			levels.append("td_%s.%s" % (name,level))
			if restriction:
				where.append(restriction)

		group_by = 'group by ' + ', '.join([", ".join(x) for x in levels_with_parent])
		if where:
			where = "where " + ' and '.join(where)
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



