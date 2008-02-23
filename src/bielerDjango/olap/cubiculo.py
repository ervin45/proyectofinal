#!/usr/bin/env python
#-*- coding: <encoding name> -*-

from pprint import pprint

class InvalidLevel:
    pass

class InvalidDimension:
    pass


class Meta:
    def __init__(self):
        self.dimension_meta = {'pieza':['codigo',
                                        'pieza',
                                        'modificacion',
                                        'modelo', 
                                        'grupo_constructivo',
                                        'TODO'
                                        ],
                               'tiempo':['mes', 'anio', 'TODO'],
                               'proveedor':['proveedor', 'TODO']
                            }

    def previous(self, dimension, level):
        """
        >>> c = Meta()
        >>> c.previous('tiempo', 'anio')
        'mes'
        >>> c.previous('tiempo', 'TODO')
        'anio'
        >>>
        >>> try:
        ...    c.previous('tiempo', '')
        ... except InvalidLevel:
        ...    print "OK"
        ... 
        OK
        >>> try:
        ...    c.previous('tiempo', 'cualquiera')
        ... except InvalidLevel:
        ...    print "OK"
        ... 
        OK
        >>> try:
        ...    c.previous('', 'anio')
        ... except InvalidDimension:
        ...    print "OK"
        ... 
        OK
        """
        if not dimension in self.dimension_meta.keys():
            raise InvalidDimension
        
        if not level in self.dimension_meta[dimension]:
            raise InvalidLevel
        
        index = self.dimension_meta[dimension].index(level)
        result = self.dimension_meta[dimension][index - 1:index]
        if result == []:
            result = level
        else:
            result = result[0]
        return result

    def next(self, dimension, level=""):
        """
        >>> c = Meta()
        >>> c.next('tiempo', 'anio')
        'TODO'
        >>> c.next('tiempo', 'TODO')
        'TODO'
        >>>
        >>> c.next('tiempo', 'mes')
        'anio'
        >>> try:
        ...    c.next('tiempo', '')
        ... except InvalidLevel:
        ...    print "OK"
        ... 
        OK
        >>> try:
        ...    c.next('tiempo', 'cualquiera')
        ... except InvalidLevel:
        ...    print "OK"
        ... 
        OK
        >>> try:
        ...    c.next('', 'anio')
        ... except InvalidDimension:
        ...    print "OK"
        ...
        OK
        """
        if not dimension in self.dimension_meta.keys():
            raise InvalidDimension
        
        if not level in self.dimension_meta[dimension]:
            raise InvalidLevel
        
        index = self.dimension_meta[dimension].index(level)
        result = self.dimension_meta[dimension][index + 1:index + 2]
        if result == []:
            result = level
        else:
            result = result[0]
        return result

    def parent_list(self, dimension, level):
        '''
        >>> c = Meta()
        >>> c.parent_list('tiempo', 'mes')
        ['td_tiempo.anio', 'td_tiempo.mes']
        >>> c.parent_list('tiempo', 'anio')
        ['td_tiempo.anio']
        >>> c.parent_list('tiempo', 'TODO')
        ['TODO']
        >>> try:
        ...    c.parent_list('tiempo', 'cualquiera')
        ... except InvalidLevel:
        ...    print "OK"
        ... 
        OK
        >>> try:
        ...    c.parent_list('', 'anio')
        ... except InvalidDimension:
        ...    print "OK"
        ... 
        OK
        '''
        if not dimension in self.dimension_meta.keys():
            raise InvalidDimension

        if not level in self.dimension_meta[dimension]:
            raise InvalidLevel


        if level == 'TODO':
            return ['TODO']
        else:
            result = []
        
            levels = self.dimension_meta[dimension]
            niveles_superiores = levels[levels.index(level):]
        
            result = ["td_%s.%s" % (dimension, x)  for x in niveles_superiores if x != 'TODO']
            result.reverse()
            return result
        
    def parent_list_without_dimension(self, dimension, level):
        '''
        >>> c = Meta()
        >>> c.parent_list_without_dimension('tiempo', 'mes')
        ['anio', 'mes']
        >>> c.parent_list_without_dimension('tiempo', 'anio')
        ['anio']
        >>> c.parent_list_without_dimension('tiempo', 'TODO')
        ['TODO']
        >>>
        '''
        
        if level == 'TODO':
            return ['TODO']
        else:
            result = []
        
            levels = self.dimension_meta[dimension]
            niveles_superiores = levels[levels.index(level):]
        
            result = [x for x in niveles_superiores if x != 'TODO']
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
    def __init__(self,ft, dimensions, measures, ore):
        self.ft = ft
        self.dimensions = {}
        for a in dimensions:
            self._add_dimension(a)
        self.measures = measures
        self.ore = ore
        self.meta = Meta()

    def _add_dimension(self, a):
        '''
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore={})
        >>> c._add_dimension(['proveedor', 'proveedor', {'proveedor': ['Mercedez']}])
        >>> pprint(c.dimensions)
        {'pieza': ['pieza', 'grupo_constructivo', {}],
         'proveedor': ['proveedor', 'proveedor', {'proveedor': ['Mercedez']}],
         'tiempo': ['tiempo', 'mes', {}]}
        ''' 
        try:
            self.dimensions_order[0]
        except:
            self.dimensions_order = []
        
        if len(a) == 2:
            a.append({})
        self.dimensions_order.append(a[0])
        self.dimensions[a[0]] = a

    def add_measure(self, m):
        self.measures.append(m)
        
    def add_restriction(self, dimension, level, value):
        if not self.dimensions[dimension][2].has_key(level):
            self.dimensions[dimension][2][level] = [value] 
        else:
            self.dimensions[dimension][2][level].append(value)

    def del_restriccion(self, dimension):
        self.dimensions[dimension][2] = {}


    def drill(self, axis):
        dimension = self.dimensions_order[int(axis)]
        level = self.dimensions[dimension][1]
        new_level = self.meta.previous(dimension, level)
        self.dimensions[dimension][1] = new_level

    def roll(self, axis):
        dimension = self.dimensions_order[int(axis)]
        level = self.dimensions[dimension][1]
        new_level = self.meta.next(dimension, level)
        self.del_restriccion(dimension)
        self.dimensions[dimension][1] = new_level

    def pivot(self):
        (self.dimensions_order[0], self.dimensions_order[1]) = (self.dimensions_order[1], self.dimensions_order[0])
        

    def getMeasuresList(self):
        return [x[0] for x in self.measures]

    def dimension_values(self, axis):
        first_dimension = self.dimensions[self.dimensions_order[int(axis)]]
        levels_parent = self.meta.parent_list(first_dimension[0], first_dimension[1])
        
        if levels_parent == ['TODO']:
            return "select 'TODO' as TODO"
        else: 
            select = "|| ' - ' ||".join(levels_parent)
            campos = ", ".join([x for x in levels_parent])
            
            where = []
            where_aux = []
            for level, val in first_dimension[2].items():
                valores = ", ".join([str(v) for v in val])
                rest = "td_%s.%s in('%s')" % ( first_dimension[0], level, valores)
                where_aux.append(rest)
            where = "%s" % " and ".join(where_aux)
            #where = "%s" % " and ".join(["td_%s.%s in(%s)" % ( first_dimension[0], level, ", ".join(val)) for level, val in first_dimension[2].items()])
            if where:
                where = "where %s" % where
            sql = "select distinct(%s), %s from td_%s %s order by %s" % (select, campos, first_dimension[0], where, campos)
            print sql
            return sql          

    def drill_replacing(self, axis, value):
        level = self.dimensions[self.dimensions_order[int(axis)]][1]
        dimension = self.dimensions[self.dimensions_order[int(axis)]]
        self.del_restriccion(dimension[0])
        
        values = value.split(" - ")
        levels = self.meta.parent_list_without_dimension(dimension[0], level)
        
        for level, value in zip(levels, values):
            self.add_restriction(dimension[0], level, value)
        self.drill(axis)

    def drill_replacing2(self, value0, value1):
        '''
        Realiza una operación de drill_replacing en ambos ejes
        para 2 valores (uno por eje)
        
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['stock']], ore={})
        >>> c.dimensions2
        {'tiempo': ['tiempo', 'mes', {}], 'pieza': ['pieza', 'grupo_constructivo', {}]}
        >>> c.drill_replacing2('2007 - 6', '184')
        >>> c.dimensions
        {'tiempo': ['tiempo', 'mes', {'anio': ['2007'], 'mes': ['6']}], 'pieza': ['pieza', 'modelo', {'grupo_constructivo': ['184']}]}
        >>> try:
        ...    c.drill_replacing2('cualquiera', '184')
        ... except InvalidLevel:
        ...    print "OK"
        OK
        >>>
        '''
        self.drill_replacing(0, value0)
        self.drill_replacing(1, value1)
        
    def dice(self, main_axis, other_axis):
        '''
        Realiza una operación de dice (rotación de ejes del cubo)
        
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['stock']], ore={})
        >>> c.getMainAxisList()
        ['tiempo', 'pieza']
        >>> c.dice('pieza', 'proveedor')
        >>> c.getMainAxisList()
        ['tiempo', 'povedoor']
        >>> try:
        ...    c.dice('pieza', 'proveedor')
        ... except InvalidDimension:
        ...    print "OK"
        ...
        OK
        >>>
        '''
        ma = self.dimensions.pop(main_axis)
        
        index = [self.ore.index(x) for x in self.ore if x[0] == other_axis][0]
        oa = self.ore[index]
        
        self.dimensions_order[self.dimensions_order.index(main_axis)] = other_axis
        self.ore[index] = ma
        self.dimensions[other_axis] = oa
        
    def getMainAxisList(self):
        '''
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['stock']], ore={})
        >>> c.getMainAxisList()
        ['tiempo', 'pieza']
        >>>
        '''
        return self.dimensions.keys()
    
    def getOtherAxisList(self):
        '''
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['stock']], ore={})
        >>> c.getOtherAxisList()
        ['proveedor']
        >>>
        '''
        return [x[0] for x in self.ore]
    
    def _select(self):
        '''
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore={})
        >>> c._select()
        "SELECT td_tiempo.anio|| ' - ' ||td_tiempo.mes as columns, td_pieza.grupo_constructivo as rows, sum(ft_ventas.cantidad) as cantidad"
        >>>
        '''
        levels_with_parent = []

        for dimension in self.dimensions_order:
            (name, level, restriction) = self.dimensions[dimension]
            levels_with_parent.append(self.meta.parent_list(name, level)) 
        
        measures = ['%s(ft_%s.%s) as %s' % (x[1], self.ft ,x[0], x[0]) for x in self.measures]
        
        if levels_with_parent[0] == ["TODO"]:
            columns_string = "'TODO' as columns"
        else:
            columns_string = "|| ' - ' ||".join(levels_with_parent[0]) + " as columns"

        if levels_with_parent[1] == ["TODO"]:
            rows_string = "'TODO' as rows"
        else:
            rows_string   = "|| ' - ' ||".join(levels_with_parent[1]) + " as rows"
        
        select = "SELECT %s, %s, %s"  % (columns_string, rows_string,','.join(measures)) 
        
        return select
    
    def _from(self):
        '''
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore={})
        >>> c._from()
        'FROM ft_ventas JOIN td_tiempo on (ft_ventas.fk_tiempo = td_tiempo.id) JOIN td_pieza on (ft_ventas.fk_pieza = td_pieza.id) '
        >>>
        '''
        sfrom = "FROM ft_%s" % self.ft
        
        joins = ""
        for dimension in self.dimensions_order:
            (name, level, restriction) = self.dimensions[dimension]

            joins += "JOIN td_%s on (ft_%s.fk_%s = td_%s.id) " % (name, self.ft, name, name)
            
        for other_dim in self.ore:
            (name, level, restriction) = other_dim
            joins += "JOIN td_%s on (ft_%s.fk_%s = td_%s.id) " % (name, self.ft, name, name)
            
        return "%s %s" % (sfrom, joins)
    
    def _where(self):
        '''
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore={})
        >>> c._where()
        ''
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {'anio': ['2005', '1999']}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore={})
        >>> c._where()
        "WHERE td_tiempo.anio in('2005', '1999') "
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {'anio': ['2005', '1999']}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[['proveedor', 'proveedor', {'proveedor': ['Mercedez Benz']}]])
        >>> c._where()
        "WHERE td_tiempo.anio in('2005', '1999') AND td_proveedor.proveedor in('Mercedez Benz') "
        '''
        
        levels_with_parent = []
        where = []

        for dimension in self.dimensions_order:
            (name, level, restriction) = self.dimensions[dimension]
            levels_with_parent.append(self.meta.parent_list(name, level)) 
            if restriction:
                for level, val in restriction.items():
                    valores = ", ".join(["'%s'" % v for v in val])
                    where.append("td_%s.%s in(%s)" % ( name, level, valores))
        
        for other_dim in self.ore:
            (name, level, restriction) = other_dim
            if restriction:
                for level, val in restriction.items():
                    valores = ", ".join(["'%s'" % v for v in val])
                    where.append("td_%s.%s in(%s)" % ( name, level, valores))

        if where:
            where = "WHERE %s " % ' AND '.join(where)
        else:
            where = ""
        
        return where
        
    def _group_by(self):
        '''
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore={})
        >>> c._group_by()
        'GROUP BY td_tiempo.anio, td_tiempo.mes, td_pieza.grupo_constructivo '
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'TODO', {}]], measures=[['cantidad', 'sum']], ore={})
        >>> c._group_by()
        'GROUP BY td_tiempo.anio, td_tiempo.mes '
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'TODO', {}], ['pieza', 'TODO', {}]], measures=[['cantidad', 'sum']], ore={})
        >>> c._group_by()
        ''
        >>>
        '''
        levels_with_parent = []

        for dimension in self.dimensions_order:
            (name, level, restriction) = self.dimensions[dimension]
            if level != 'TODO':
                levels_with_parent.append(self.meta.parent_list(name, level)) 
        
        if levels_with_parent == []:
            return ''
        else:
            values = ', '.join([", ".join(x) for x in levels_with_parent])
            group_by = 'GROUP BY %s ' % values
            return group_by

    
    def _order_by(self):
        '''
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore={})
        >>> c._order_by()
        'ORDER BY td_tiempo.anio, td_tiempo.mes, td_pieza.grupo_constructivo '
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'TODO', {}]], measures=[['cantidad', 'sum']], ore={})
        >>> c._order_by()
        'ORDER BY td_tiempo.anio, td_tiempo.mes '
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'TODO', {}], ['pieza', 'TODO', {}]], measures=[['cantidad', 'sum']], ore={})
        >>> c._order_by()
        ''
        >>>
        '''        

        levels_with_parent = []

        for dimension in self.dimensions_order:
            (name, level, restriction) = self.dimensions[dimension]
            if level != 'TODO':
                levels_with_parent.append(self.meta.parent_list(name, level)) 

        if levels_with_parent == []:
            return ''
        else:
            values = ', '.join([", ".join(x) for x in levels_with_parent])
            order_by = "ORDER BY %s " % values
            return order_by

    def sql(self):
        '''
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore={})
        >>> c.sql()
        "SELECT td_tiempo.anio|| ' - ' ||td_tiempo.mes as columns, td_pieza.grupo_constructivo as rows, sum(ft_ventas.cantidad) as cantidad\\nFROM ft_ventas JOIN td_tiempo on (ft_ventas.fk_tiempo = td_tiempo.id) JOIN td_pieza on (ft_ventas.fk_pieza = td_pieza.id) \\n\\nGROUP BY td_tiempo.anio, td_tiempo.mes, td_pieza.grupo_constructivo \\nORDER BY td_tiempo.anio, td_tiempo.mes, td_pieza.grupo_constructivo \\n"
        >>>
        '''   

        sql = "%s\n" * 5 % (self._select(),self._from(), self._where(), self._group_by(), self._order_by() )

        return sql
    
    
    def absolute_url(self, request):
        url = "http://%s:%s/report/compras/" % (request.META['SERVER_NAME'], request.META['SERVER_PORT'])
        dimension_url = "/".join(self.dimensions_order)
        url = url + dimension_url + "/"
        
        level_url = "/".join([self.dimensions[x][1] for x in self.dimensions_order])
        url = url + level_url + "/"
        
        xr_url = "xr=" + str(self.dimensions[self.dimensions_order[0]][2]) + "/"
        yr_url = "yr=" + str(self.dimensions[self.dimensions_order[1]][2]) + "/"
        ore_url = "ore=" + str(self.ore) + "/"
        
        url = url + xr_url + yr_url + ore_url
        
        return url


#c = cubiculo.Cubiculo('vendido',
#   [['Tiempo','anio'],
#    ['Sucursal','sucursal',"sucursal = 'rafaela'"]],
#   ['Cantidad'])
#print c.sql()
#c.drill('Tiempo','mes','anio=2007')
#print c.sql()




def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
