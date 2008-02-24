#!/usr/bin/env python
#-*- coding: utf-8 -*-

from pprint import pprint

class InvalidLevel:
    pass

class InvalidDimension:
    pass

class InvalidData:
    pass

class InvalidAxis:
    pass

class InvalidMeasure:
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
                            
        self.fact_table_meta = {'ventas':      ['tiempo',
                                                'pieza',
                                                'proveedor',
                                                'tipo_venta'],
                                'compras':     ['tiempo',
                                                'pieza',
                                                'proveedor'],
                                'movimientos': ['tiempo',
                                                'pieza',
                                                'proveedor']}

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
        self.dimensions_fixed = {}
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
        dim_name = a[0]
        
        try:
            self.dimensions_order[0]
        except:
            self.dimensions_order = []
        
        if len(a) == 2:
            a.append({})
            
        if dim_name.startswith(":"):
            dim_name = dim_name[1:]
            a[0]     = dim_name
            self.dimensions_fixed[dim_name] = True
        else:
            self.dimensions_fixed[dim_name] = False
            
        self.dimensions_order.append(dim_name)
        self.dimensions[dim_name] = a

    def _add_measure(self, m):
        '''
        Agrega un measure. 
        
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[])
        >>> c.measures
        [['cantidad', 'sum']]
        >>> c._add_measure(['margen_dolares', 'sum'])
        >>> c.measures
        [['cantidad', 'sum'], ['margen_dolares', 'sum']]
        >>> try:
        ...    c._add_measure('margen_pesos')
        ... except InvalidMeasure:
        ...    print "OK"
        ...
        OK
        >>> try:
        ...    c._add_measure(['margen_pesos'])
        ... except InvalidMeasure:
        ...    print "OK"
        ...
        OK
        >>> try:
        ...    c._add_measure(['margen_pesos','sum','cualquiera'])
        ... except InvalidMeasure:
        ...    print "OK"
        ...
        OK
        >>> 
        '''
        
        if len(m) != 2:
            raise InvalidMeasure
        
        self.measures.append(m)
        
    def _add_restriction(self, dimension, level, value):
        '''
        Agrega una restriccion a una dimension en un determinado nivel.
        value debe ser una lista de elementos a los cuales ser incluido

        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[])
        >>> c.dimensions
        {'tiempo': ['tiempo', 'mes', {}], 'pieza': ['pieza', 'grupo_constructivo', {}]}
        >>> c._add_restriction('pieza', 'grupo_constructivo', '184')
        >>> c.dimensions
        {'tiempo': ['tiempo', 'mes', {}], 'pieza': ['pieza', 'grupo_constructivo', {'grupo_constructivo': ['184']}]}
        >>> c._add_restriction('pieza', 'grupo_constructivo', '185')
        >>> c.dimensions
        {'tiempo': ['tiempo', 'mes', {}], 'pieza': ['pieza', 'grupo_constructivo', {'grupo_constructivo': ['184', '185']}]}
        >>>
        '''
        
        if not self.dimensions[dimension][2].has_key(level):
            self.dimensions[dimension][2][level] = [value] 
        else:
            self.dimensions[dimension][2][level].append(value)

    def _del_restriccion(self, dimension):
        '''
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[])
        >>> c._del_restriccion('pieza')
        >>> c.dimensions
        {'tiempo': ['tiempo', 'mes', {}], 'pieza': ['pieza', 'grupo_constructivo', {}]}

        '''
        
        self.dimensions[dimension][2] = {}


    def drill(self, axis):
        '''
        Ejecuta una operación de drill en el cubo

        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'anio', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['stock','avg'], ['compras','sum']], ore=[])
        >>> c.drill(0)
        >>> c.dimensions['tiempo']
        ['tiempo', 'mes', {}]
        >>> c.drill(1)
        >>> c.dimensions['pieza']
        ['pieza', 'modelo', {}]
        >>> try:
        ...    c.drill(2)
        ... except InvalidAxis:
        ...    print "OK"
        ...
        OK
        >>> c = Cubiculo(ft='movimientos', dimensions=[[':tiempo', 'anio', {}], ['pieza', 'modelo', {}]], measures=[['stock','avg'], ['compras','sum']], ore=[])
        >>> c.roll(0)
        False
        >>> c.dimensions['tiempo']
        ['tiempo', 'anio', {}]
        '''
        
        if int(axis) not in (0, 1):
            raise InvalidAxis
        
        
        dimension = self.dimensions_order[int(axis)]
        
        if self.dimensions_fixed[dimension]:
            return False 
        
        level = self.dimensions[dimension][1]
        new_level = self.meta.previous(dimension, level)
        self.dimensions[dimension][1] = new_level

    def roll(self, axis):
        '''
        Realiza una operación de roll al cubo

        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], ['pieza', 'modelo', {}]], measures=[['stock','avg'], ['compras','sum']], ore=[])
        >>> c.roll(0)
        >>> c.dimensions['tiempo']
        ['tiempo', 'anio', {}]
        >>> c.roll(0)
        >>> c.dimensions['tiempo']
        ['tiempo', 'TODO', {}]
        >>> c.roll(1)
        >>> c.dimensions['pieza']
        ['pieza', 'grupo_constructivo', {}]
        >>> c.roll(1)
        >>> c.dimensions['pieza']
        ['pieza', 'TODO', {}]
        >>> try:
        ...    c.roll(2)
        ... except InvalidAxis:
        ...    print "OK"
        ...
        OK
        >>> c = Cubiculo(ft='movimientos', dimensions=[[':tiempo', 'mes', {}], ['pieza', 'modelo', {}]], measures=[['stock','avg'], ['compras','sum']], ore=[])
        >>> c.roll(0)
        False
        >>> c.dimensions['tiempo']
        ['tiempo', 'mes', {}]
        
        '''
        
        if int(axis) not in (0, 1):
            raise InvalidAxis        
        
        dimension = self.dimensions_order[int(axis)]
        
        if self.dimensions_fixed[dimension]:
            return False
        
        level = self.dimensions[dimension][1]
        new_level = self.meta.next(dimension, level)
        self._del_restriccion(dimension)
        self.dimensions[dimension][1] = new_level

    def pivot(self):
        '''realiza la operacion de pivot (intercambio de dimensiones principales)
        del cubo

        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], ['pieza', 'modelo', {}]], measures=[['stock','avg'], ['compras','sum']], ore=[])
        >>> c.pivot()        
        >>> c.dimensions
        {'tiempo': ['tiempo', 'mes', {}], 'pieza': ['pieza', 'modelo', {}]}
        >>> 
        '''
        
        (self.dimensions_order[0], self.dimensions_order[1]) = (self.dimensions_order[1], self.dimensions_order[0])
        

    def get_measures_list(self):
        '''
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'anio', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['stock','avg'], ['compras','sum']], ore=[])
        >>> c.get_measures_list()
        ['stock', 'compras']
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[])
        >>> c.get_measures_list()
        ['cantidad']
        '''
        return [x[0] for x in self.measures]


    def drill_replacing(self, axis, value):
        '''
        Realiza una operación de drill en un eje determinado

        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'anio', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['stock']], ore=[])
        >>> c.dimensions
        {'tiempo': ['tiempo', 'anio', {}], 'pieza': ['pieza', 'grupo_constructivo', {}]}
        >>> c.drill_replacing(0, '2007')
        >>> c.dimensions
        {'tiempo': ['tiempo', 'mes', {'anio': ['2007']}], 'pieza': ['pieza', 'grupo_constructivo', {}]}
        >>> c.drill_replacing(0, '2007 - 6')
        >>> c.dimensions
        {'tiempo': ['tiempo', 'mes', {'anio': ['2007'], 'mes': ['6']}], 'pieza': ['pieza', 'grupo_constructivo', {}]}
        >>> try:
        ...     c.drill_replacing(3, '1999')
        ... except InvalidAxis:
        ...     print "OK"
        ...
        OK
        >>> try:
        ...     c.drill_replacing('1', '1999')
        ...     print "OK"
        ... except InvalidAxis:
        ...     print "WRONG"
        ...
        OK
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'TODO', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['stock']], ore=[])
        >>> c.drill_replacing('0', 'TODO')
        >>> c.dimensions
        {'tiempo': ['tiempo', 'anio', {}], 'pieza': ['pieza', 'grupo_constructivo', {}]}
        '''
        
        if int(axis) not in (0, 1):
            raise InvalidAxis
        
        if value == "TODO":
            self.drill(axis)
            return
        
        
        level = self.dimensions[self.dimensions_order[int(axis)]][1]
        dimension = self.dimensions[self.dimensions_order[int(axis)]]
        self._del_restriccion(dimension[0])
        
        values = value.split(" - ")
        levels = self.meta.parent_list_without_dimension(dimension[0], level)
        
        for level, value in zip(levels, values):
            self._add_restriction(dimension[0], level, value)
        self.drill(axis)

    def drill_replacing2(self, value0, value1):
        '''
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['stock']], ore=[])
        >>> c.dimensions
        {'tiempo': ['tiempo', 'mes', {}], 'pieza': ['pieza', 'grupo_constructivo', {}]}
        >>> c.drill_replacing2('2007 - 6', '184')
        >>> c.dimensions
        {'tiempo': ['tiempo', 'mes', {'anio': ['2007'], 'mes': ['6']}], 'pieza': ['pieza', 'modelo', {'grupo_constructivo': ['184']}]}
        >>>
        '''
        self.drill_replacing(0, value0)
        self.drill_replacing(1, value1)
        
    def dice(self, main_axis, other_axis):
        '''
        Realiza una operacion de dice (rotacion de ejes del cubo)
        
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['stock']], ore=[])
        >>> c.get_main_axis_list()
        ['tiempo', 'pieza']
        >>> c.dice('pieza', 'proveedor')
        >>> c.get_main_axis_list()
        ['tiempo', 'proveedor']
        >>> c.get_other_axis_list()
        ['pieza']
        >>> try:
        ...    c.dice('pieza', 'proveedor')
        ... except InvalidDimension:
        ...    print "OK"
        ...
        OK
        >>>
        '''
        
        if not main_axis in self.dimensions.keys():
            raise InvalidDimension
        
        
        other_dimensions = [x for x in self.meta.fact_table_meta[self.ft] if x not in self.dimensions.keys()]
        if not other_axis in other_dimensions:
            raise InvalidDimension


        main_dimension = self.dimensions.pop(main_axis)
        
        #other_axis puede estar o no en self.ore
        try:
            #si esta
            index = [self.ore.index(x) for x in self.ore if x[0] == other_axis][0]
            other_dimension = self.ore[index]
            self.ore[index] = main_dimension
        except IndexError:
            #si no esta
            other_dimension = [other_axis, "TODO", {}]
            self.ore.append(main_dimension)
            
        main_axis_order = self.dimensions_order.index(main_axis)
        self.dimensions_order[main_axis_order] = other_axis
        
        self.dimensions[other_axis] = other_dimension
        
    def dimension_values(self, axis):
        '''
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'anio', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['stock']], ore=[])
        >>> c.dimension_values(0)
        'select distinct(td_tiempo.anio), td_tiempo.anio from td_tiempo  order by td_tiempo.anio'
        >>> c.dimension_values(1)
        'select distinct(td_pieza.grupo_constructivo), td_pieza.grupo_constructivo from td_pieza  order by td_pieza.grupo_constructivo'
        >>> try:
        ...    c.dimension_values(3)
        ... except InvalidAxis:
        ...    print "OK"
        ...
        OK
        >>>
        '''
        
        if axis not in (0, 1):
            raise InvalidAxis
        
        
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
            if where:
                where = "where %s" % where
            sql = "select distinct(%s), %s from td_%s %s order by %s" % (select, campos, first_dimension[0], where, campos)
            
            return sql                  

    def get_main_axis_list(self):
        '''
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['stock']], ore=[])
        >>> c.get_main_axis_list()
        ['tiempo', 'pieza']
        >>>
        '''
        return self.dimensions.keys()
    
    def get_other_axis_list(self):
        '''
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['stock']], ore=[])
        >>> c.get_other_axis_list()
        ['proveedor']
        >>> c = Cubiculo(ft='compras', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['stock']], ore=[])
        >>> c.get_other_axis_list()
        ['proveedor']
        '''
        
        total_dimensions = self.meta.fact_table_meta[self.ft]
        return [x for x in total_dimensions if x not in (self.dimensions.keys())]
    
    def _select(self):
        '''
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[])
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
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[])
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
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[])
        >>> c._where()
        ''
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {'anio': ['2005', '1999']}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[])
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
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[])
        >>> c._group_by()
        'GROUP BY td_tiempo.anio, td_tiempo.mes, td_pieza.grupo_constructivo '
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'TODO', {}]], measures=[['cantidad', 'sum']], ore=[])
        >>> c._group_by()
        'GROUP BY td_tiempo.anio, td_tiempo.mes '
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'TODO', {}], ['pieza', 'TODO', {}]], measures=[['cantidad', 'sum']], ore=[])
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
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[])
        >>> c._order_by()
        'ORDER BY td_tiempo.anio, td_tiempo.mes, td_pieza.grupo_constructivo '
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'TODO', {}]], measures=[['cantidad', 'sum']], ore=[])
        >>> c._order_by()
        'ORDER BY td_tiempo.anio, td_tiempo.mes '
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'TODO', {}], ['pieza', 'TODO', {}]], measures=[['cantidad', 'sum']], ore=[])
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
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[])
        >>> c.sql()
        "SELECT td_tiempo.anio|| ' - ' ||td_tiempo.mes as columns, td_pieza.grupo_constructivo as rows, sum(ft_ventas.cantidad) as cantidad\\nFROM ft_ventas JOIN td_tiempo on (ft_ventas.fk_tiempo = td_tiempo.id) JOIN td_pieza on (ft_ventas.fk_pieza = td_pieza.id) \\n\\nGROUP BY td_tiempo.anio, td_tiempo.mes, td_pieza.grupo_constructivo \\nORDER BY td_tiempo.anio, td_tiempo.mes, td_pieza.grupo_constructivo \\n"
        >>>
        '''   

        sql = "%s\n" * 5 % (self._select(),self._from(), self._where(), self._group_by(), self._order_by() )

        return sql
    
    
    def parcial_url(self):
        '''
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[])
        >>> print c.parcial_url()
        ventas/tiempo/pieza/mes/grupo_constructivo/xr={}/yr={}/ore=[]/
        >>> c = Cubiculo(ft='compras', dimensions=[['tiempo', 'mes', {'anio': ['1998']}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[])
        >>> print c.parcial_url()
        compras/tiempo/pieza/mes/grupo_constructivo/xr={'anio': ['1998']}/yr={}/ore=[]/
        >>> c = Cubiculo(ft='compras', dimensions=[[':tiempo', 'mes', {'anio': ['1998']}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[])
        >>> print c.parcial_url()
        compras/:tiempo/pieza/mes/grupo_constructivo/xr={'anio': ['1998']}/yr={}/ore=[]/
        '''
        url = self.ft + "/"
        
        dimensions = []
        for dim in self.dimensions_order:
            if self.dimensions_fixed[dim]:
                dimensions.append(":" + dim)
            else:
                dimensions.append(dim)
        dimension_url = "/".join(dimensions)
        url = url + dimension_url + "/"
        
        level_url = "/".join([self.dimensions[x][1] for x in self.dimensions_order])
        url = url + level_url + "/"
        
        xr_url = "xr=" + str(self.dimensions[self.dimensions_order[0]][2]) + "/"
        yr_url = "yr=" + str(self.dimensions[self.dimensions_order[1]][2]) + "/"
        ore_url = "ore=" + str(self.ore) + "/"
        
        url = url + xr_url + yr_url + ore_url
        
        return url
    
    def can_roll_x(self):
        '''
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], ['pieza', 'pieza', {}]], measures=[['stock']], ore=[])
        >>> c.can_roll_x()
        True
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'TODO', {}], ['pieza', 'pieza', {}]], measures=[['stock']], ore=[])
        >>> c.can_roll_x()
        False
        '''
        
        x_dimension = self.dimensions_order[0]
        x_levels    = self.meta.dimension_meta[x_dimension]
        
        highest_level = x_levels[-1] 
        actual_level = self.dimensions[x_dimension][1]
        
        if highest_level == actual_level:
            return False
        
        return True
    
    def can_drill_x(self):
        '''
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], ['pieza', 'pieza', {}]], measures=[['stock']], ore=[])
        >>> c.can_drill_x()
        False
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'anio', {}], ['pieza', 'pieza', {}]], measures=[['stock']], ore=[])
        >>> c.can_drill_x()
        True
        '''
        
        x_dimension = self.dimensions_order[0]
        x_levels    = self.meta.dimension_meta[x_dimension]
        
        lowest_level = x_levels[0] 
        actual_level = self.dimensions[x_dimension][1]
        
        if lowest_level == actual_level:
            return False
        
        return True


    def can_roll_y(self):
        '''
        >>> c = Cubiculo(ft='movimientos', dimensions=[['pieza', 'pieza', {}], ['tiempo', 'mes', {}]], measures=[['stock']], ore=[])
        >>> c.can_roll_y()
        True
        >>> c = Cubiculo(ft='movimientos', dimensions=[['pieza', 'pieza', {}], ['tiempo', 'TODO', {}]], measures=[['stock']], ore=[])
        >>> c.can_roll_y()
        False
        '''
        
        y_dimension = self.dimensions_order[1]
        y_levels    = self.meta.dimension_meta[y_dimension]
        
        highest_level = y_levels[-1] 
        actual_level = self.dimensions[y_dimension][1]
        
        if highest_level == actual_level:
            return False
        
        return True
    
    def can_drill_y(self):
        '''
        >>> c = Cubiculo(ft='movimientos', dimensions=[['pieza', 'pieza', {}], ['tiempo', 'anio', {}]], measures=[['stock']], ore=[])
        >>> c.can_drill_y()
        True
        >>> c = Cubiculo(ft='movimientos', dimensions=[['pieza', 'pieza', {}], ['tiempo', 'mes', {}]], measures=[['stock']], ore=[])
        >>> c.can_drill_y()
        False
        '''
        
        y_dimension = self.dimensions_order[1]
        y_levels    = self.meta.dimension_meta[y_dimension]
        
        lowest_level = y_levels[0] 
        actual_level = self.dimensions[y_dimension][1]
        
        if lowest_level == actual_level:
            return False
        
        return True    



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
