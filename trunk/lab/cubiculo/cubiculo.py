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

class Cubiculo:
	def __init__(self,ft, dimensions, measures):
		self.ft = ft
		self.dimensions = {}
		for a in dimensions:
			self.add_dimension(a)
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

                t = ['%s(%s)' % (x[1],x[0]) for x in self.measures]

		select = "select " + ','.join(levels) + ',' + ','.join(t) 

		sql = """
%s
%s
%s
%s
%s""" % (select,sfrom, joins,where,group_by)

		return sql


#c = cubiculo.Cubiculo('vendido',
#	[['Tiempo','anio'],
#	 ['Sucursal','sucursal',"sucursal = 'rafaela'"]],
#	['Cantidad'])
#print c.sql()
#c.drill('Tiempo','mes','anio=2007')
#print c.sql()



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

class Cubiculo:
	def __init__(self,ft, dimensions, measures):
		self.ft = ft
		self.dimensions = {}
		for a in dimensions:
			self.add_dimension(a)
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

                t = ['%s(%s)' % (x[1],x[0]) for x in self.measures]

		select = "select " + ','.join(levels) + ',' + ','.join(t) 

		sql = """
%s
%s
%s
%s
%s""" % (select,sfrom, joins,where,group_by)

		return sql


#c = cubiculo.Cubiculo('vendido',
#	[['Tiempo','anio'],
#	 ['Sucursal','sucursal',"sucursal = 'rafaela'"]],
#	['Cantidad'])
#print c.sql()
#c.drill('Tiempo','mes','anio=2007')
#print c.sql()



