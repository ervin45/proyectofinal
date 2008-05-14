#!/usr/bin/env python
#-*- coding: utf-8 -*-

from pprint import pprint

class InvalidLevel:
    def __init__(self, level):
        self.level = level

    def __repr__(self):
        return "INVALID LEVEL %s" % self.level

class InvalidDimension:
    def __init__(self, dimension):
        self.dimension = dimension

    def __repr__(self):
        return "INVALID DIMENSION %s" % self.dimension

class InvalidData:
    pass

class InvalidAxis:
    pass

class InvalidMeasure:
    pass


class Meta:
    dimension_meta = {'pieza':[     'descripcion',
                                    'codigo',
                                    'pieza',
                                    'modificacion',
                                    'modelo',
                                    'grupo_constructivo',
                                    'TODO'
                                    ],
                            'tiempo':['mes', 'anio', 'TODO'],
                            'proveedor':['proveedor', 'TODO'],
                            'tipo_pieza':['tipo_pieza', 'TODO'],
                            'tipo_venta':['tipo_venta', 'TODO']
                        }

    fact_table_dimensions_meta = {'ventas':['tiempo',
                                            'pieza',
                                            'proveedor',
                                            'tipo_venta',
                                            'tipo_pieza'],

                            'compras':     ['tiempo',
                                            'pieza',
                                            'proveedor',
                                            'tipo_pieza'],

                            'movimientos': ['tiempo',
                                            'pieza',
                                            'proveedor'],

                            'test':        ['tiempo',
                                            'pieza',
                                            'tipo_pieza']                                            }

    fact_table_measures_meta   = {'ventas': ['cantidad',
                                             'precio_venta_pesos',
                                             'margen_pesos',
                                             'precio_venta_dolares',
                                             'margen_dolares'],
                                   'compras': ['cantidad',
                                               'costo_pesos',
                                               'costo_dolar'],
                                   'movimientos': ['stock',
                                        	    'egresos',
                                                    'ingresos',
                                                    'ventas_por_taller',
                                                    'ventas_por_mostrador',
                                                    'compras1',
                                                    'compras2',
                                                    'envios_a_rafaela',
                                                    'envios_a_reconquista',
                                                    'entrada_de_rafaela',
                                                    'entrada_de_reconquista',
                                                    'ajuste_negativo',
                                                    'ajuste_positivo',
                                                    'devolucion_salida1',
                                                    'devolucion_salida2',
                                                    'otro'],

                                   'test': ['cantidad',
                                               'costo']
                                             }

    @staticmethod
    def measure_as_string(lista):
        """
        >>> Meta.measure_as_string([['ft_compras', 'costo_dolar', 'sum']])
        'el costo de compras expresado en dolares'
        >>> Meta.measure_as_string([['ft_compras', 'costo_dolar', 'avg']])
        'el costo promedio de compras expresado en dolares'
        >>> Meta.measure_as_string([['ft_compras', 'costo_pesos', 'sum']])
        'el costo de compras expresado en pesos'
        >>> Meta.measure_as_string([['ft_compras', 'costo_pesos', 'avg']])
        'el costo promedio de compras expresado en pesos'
        >>> Meta.measure_as_string([['ft_compras', 'cantidad', 'sum']])
        'la cantidad de compras expresada en unidades'
        >>> Meta.measure_as_string([['ft_compras', 'cantidad', 'avg']])
        'la cantidad promedio de compras expresada en unidades'
        >>> Meta.measure_as_string([['ft_ventas', 'cantidad', 'sum']])
        'la cantidad de ventas expresada en unidades'
        >>> Meta.measure_as_string([['ft_ventas', 'cantidad', 'avg']])
        'la cantidad promedio de ventas expresada en unidades'
        >>> Meta.measure_as_string([['ft_ventas', 'margen_pesos', 'sum']])
        'el margen de ventas expresado en pesos'
        >>> Meta.measure_as_string([['ft_ventas', 'margen_pesos', 'avg']])
        'el margen promedio de ventas expresado en pesos'
        >>> Meta.measure_as_string([['ft_ventas', 'margen_dolares', 'sum']])
        'el margen de ventas expresado en dolares'
        >>> Meta.measure_as_string([['ft_ventas', 'margen_dolares', 'avg']])
        'el margen promedio de ventas expresado en dolares'
        >>> Meta.measure_as_string([['ft_ventas', 'precio_venta_pesos', 'sum']])
        'el precio de ventas expresado en pesos'
        >>> Meta.measure_as_string([['ft_ventas', 'precio_venta_pesos', 'avg']])
        'el precio promedio de ventas expresado en pesos'
        >>> Meta.measure_as_string([['ft_ventas', 'precio_venta_dolares', 'sum']])
        'el precio de ventas expresado en dolares'
        >>> Meta.measure_as_string([['ft_ventas', 'precio_venta_dolares', 'avg']])
        'el precio promedio de ventas expresado en dolares'
        >>> Meta.measure_as_string([['ft_movimientos', 'devolucion_salida1', 'sum']])
        'las devoluciones fuera de la garantia expresadas en piezas'
        >>> Meta.measure_as_string([['ft_movimientos', 'devolucion_salida1', 'avg']])
        'las devoluciones fuera de la garantia promedio expresadas en piezas'
        >>> Meta.measure_as_string([['ft_movimientos', 'devolucion_salida2', 'sum']])
        'las devoluciones en garantia expresadas en piezas'
        >>> Meta.measure_as_string([['ft_movimientos', 'devolucion_salida2', 'avg']])
        'las devoluciones en garantia promedio expresadas en piezas'
        """

        t = lista[0]

        expresa = 'expresado'
        if t[2] == 'avg':
            promedio = 'promedio '
        else:
            promedio= ''

        ft_name = t[0][3:]

        elem = t[1].split('_')

        if len(elem) == 1:
            ## ejemplo: cantidad
            que, unidades = elem[0], 'unidades'
        elif len(elem) == 2:
            ## ejemplo: margen_dolares
            que, unidades = elem[0], elem[1]
        elif len(elem) == 3:
            ## ejemplo: precio_venta_dolares
            que = '_'.join(elem[:-1])
            unidades = elem[-1]

        if unidades == 'dolar':
            unidades = 'dolares'


        ## manejo de que y su genero
        if que == 'precio_venta':
            que = 'el precio'
        elif que == 'margen':
            que = 'el margen'
        elif que == 'costo':
            que = 'el costo'
        elif que == 'cantidad':
            que = 'la cantidad'
            expresa = 'expresada'


        rtn = '%s %sde %s %s en %s' % (que, promedio, ft_name, expresa, unidades)
        
        return rtn

    @staticmethod
    def previous(dimension, level):
        """
        >>> Meta.previous('tiempo', 'anio')
        'mes'
        >>> Meta.previous('tiempo', 'TODO')
        'anio'
        >>> Meta.previous('tiempo', 'mes')
        'mes'
        >>> try:
        ...    Meta.previous('tiempo', '')
        ... except InvalidLevel:
        ...    print "OK"
        ...
        OK
        >>> try:
        ...    Meta.previous('tiempo', 'cualquiera')
        ... except InvalidLevel:
        ...    print "OK"
        ...
        OK
        >>> try:
        ...    Meta.previous('', 'anio')
        ... except InvalidDimension:
        ...    print "OK"
        ...
        OK
        """
        if not dimension in Meta.dimension_meta.keys():
            raise InvalidDimension(dimension)

        if not level in Meta.dimension_meta[dimension]:
            raise InvalidLevel(level)

        index = Meta.dimension_meta[dimension].index(level)
        result = Meta.dimension_meta[dimension][index - 1:index]
        if result == []:
            result = level
        else:
            result = result[0]
        return result

    @staticmethod
    def next(dimension, level=""):
        """
        >>> Meta.next('tiempo', 'anio')
        'TODO'
        >>> Meta.next('tiempo', 'TODO')
        'TODO'
        >>>
        >>> Meta.next('tiempo', 'mes')
        'anio'
        >>> try:
        ...    Meta.next('tiempo', '')
        ... except InvalidLevel:
        ...    print "OK"
        ...
        OK
        >>> try:
        ...    Meta.next('tiempo', 'cualquiera')
        ... except InvalidLevel:
        ...    print "OK"
        ...
        OK
        >>> try:
        ...    Meta.next('', 'anio')
        ... except InvalidDimension:
        ...    print "OK"
        ...
        OK
        """
        if not dimension in Meta.dimension_meta.keys():
            raise InvalidDimension(dimension)

        if not level in Meta.dimension_meta[dimension]:
            raise InvalidLevel(level)

        index = Meta.dimension_meta[dimension].index(level)
        result = Meta.dimension_meta[dimension][index + 1:index + 2]
        if result == []:
            result = level
        else:
            result = result[0]
        return result

    @staticmethod
    def parent_list(dimension, level):
        '''
        >>> Meta.parent_list('tiempo', 'mes')
        ['td_tiempo.anio', 'td_tiempo.mes']
        >>> Meta.parent_list('tiempo', 'anio')
        ['td_tiempo.anio']
        >>> Meta.parent_list('tiempo', 'TODO')
        ['TODO']
        >>> try:
        ...    Meta.parent_list('tiempo', 'cualquiera')
        ... except InvalidLevel:
        ...    print "OK"
        ...
        OK
        >>> try:
        ...    Meta.parent_list('', 'anio')
        ... except InvalidDimension:
        ...    print "OK"
        ...
        OK
        '''
        if not dimension in Meta.dimension_meta.keys():
            raise InvalidDimension(dimension)

        if not level in Meta.dimension_meta[dimension]:
            raise InvalidLevel(level)


        if level == 'TODO':
            return ['TODO']
        else:
            result = []

            levels = Meta.dimension_meta[dimension]
            niveles_superiores = levels[levels.index(level):]

            result = ["td_%s.%s" % (dimension, x)  for x in niveles_superiores if x != 'TODO']
            result.reverse()
            return result

    @staticmethod
    def parent_list_without_dimension(dimension, level):
        '''
        >>> Meta.parent_list_without_dimension('tiempo', 'mes')
        ['anio', 'mes']
        >>> Meta.parent_list_without_dimension('tiempo', 'anio')
        ['anio']
        >>> Meta.parent_list_without_dimension('tiempo', 'TODO')
        ['TODO']
        >>>
        '''

        if level == 'TODO':
            return ['TODO']
        else:
            result = []

            levels = Meta.dimension_meta[dimension]
            niveles_superiores = levels[levels.index(level):]

            result = [x for x in niveles_superiores if x != 'TODO']
            result.reverse()
            return result

    @staticmethod
    def children_list_without_dimension(dimension, level):
        '''
        >>> Meta.children_list_without_dimension('tiempo', 'mes')
        ['mes']
        >>> Meta.children_list_without_dimension('tiempo', 'anio')
        ['anio', 'mes']
        >>> Meta.children_list_without_dimension('tiempo', 'TODO')
        ['TODO']
        >>>
        '''

        if level == 'TODO':
            return ['TODO']
        else:

            levels = Meta.dimension_meta[dimension]
            niveles_inferiores = levels[:levels.index(level) + 1]

            niveles_inferiores.reverse()

            return niveles_inferiores

    @staticmethod
    def get_dimensions(ft):
        '''
        >>> Meta.get_dimensions('ventas')
        ['tiempo', 'pieza', 'proveedor', 'tipo_venta', 'tipo_pieza']
        >>>
        '''

        return Meta.fact_table_dimensions_meta[ft]

    @staticmethod
    def get_levels(dimension):
        '''
        >>> Meta.get_levels('tiempo')
        ['mes', 'anio', 'TODO']
        >>>
        '''

        return Meta.dimension_meta[dimension]

    @staticmethod
    def get_measures(ft):
        '''
        >>> Meta.get_measures('compras')
        ['cantidad', 'costo_pesos', 'costo_dolar']
        >>>
        '''

        return Meta.fact_table_measures_meta[ft]



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
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {'anio': ['2007', '2006'], 'mes': ['1', '2', '5']}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[])
        >>> c._del_restriccion('tiempo')
        >>> c.dimensions
        {'tiempo': ['tiempo', 'mes', {}], 'pieza': ['pieza', 'grupo_constructivo', {}]}

        '''

        self.dimensions[dimension][2] = {}

    def _del_restriccion_from_level(self, dimension, level):
        '''
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {'anio': ['2007', '2006'], 'mes': ['1', '2', '5']}], ['pieza', 'grupo_constructivo', {'grupo_constructivo': ['184'], 'modificacion' :['121']}]], measures=[['cantidad', 'sum']], ore=[])
        >>> c._del_restriccion_from_level('tiempo', 'mes')
        >>> c.dimensions['tiempo']
        ['tiempo', 'mes', {'anio': ['2007', '2006']}]
        >>> c._del_restriccion_from_level('pieza', 'modelo')
        >>> c.dimensions['pieza']
        ['pieza', 'grupo_constructivo', {'grupo_constructivo': ['184']}]
        '''

        children_levels = Meta.children_list_without_dimension(dimension, level)
        for level in children_levels:
            if self.dimensions[dimension][2].has_key(level):
                del(self.dimensions[dimension][2][level])

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
        new_level = Meta.previous(dimension, level)
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
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {'anio': ['2007'], 'mes': ['1','11']}], ['pieza', 'modelo', {}]], measures=[['stock','avg'], ['compras','sum']], ore=[])
        >>> c.roll(0)
        >>> c.dimensions['tiempo']
        ['tiempo', 'anio', {'anio': ['2007']}]

        '''

        if int(axis) not in (0, 1):
            raise InvalidAxis

        dimension = self.dimensions_order[int(axis)]
        level = self.dimensions[dimension][1]

        self._del_restriccion_from_level(dimension, level)

        if self.dimensions_fixed[dimension]:
            return False

        new_level = Meta.next(dimension, level)
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

    def replace_to(self, axis, values):
        '''Estable el nivel y las restricciones previas al nivel seguel el valor de values

        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], ['pieza', 'modificacion', {'grupo_constructivo': ['184']}]], measures=[['stock','avg'], ['compras','sum']], ore=[])
        >>> c.replace_to(1, '184-1')
        >>> c.dimensions['pieza']
        ['pieza', 'modificacion', {'grupo_constructivo': ['184'], 'modelo': ['1']}]
        >>> c.replace_to(1, '184-1-60')
        >>> c.dimensions['pieza']
        ['pieza', 'pieza', {'grupo_constructivo': ['184'], 'modelo': ['1'], 'modificacion': ['60']}]
        >>> try:
        ...     c.replace_to('3', '1999')
        ...     print "OK"
        ... except InvalidAxis:
        ...     print "WRONG"
        ...
        WRONG
        '''

        if int(axis) not in (0, 1):
            raise InvalidAxis

        if values == "TODO":
            self.drill(axis)
            return

        dim = self.dimensions_order[int(axis)]

        self.dimensions[dim][2] = {}
        rest_values = str(values).split("-")
        values_size = len(rest_values)

        rest_levels = Meta.dimension_meta[dim][(values_size + 1) * -1: -1]
        rest_levels.reverse()

        for level, value in zip(rest_levels, rest_values):
            self.dimensions[dim][2][level] = [value]

        self.dimensions[dim][1] = Meta.previous(dim, rest_levels[-1])

    def replace_to_both_axis(self, value0, value1):
        '''
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['stock']], ore=[])
        >>> c.dimensions
        {'tiempo': ['tiempo', 'mes', {}], 'pieza': ['pieza', 'grupo_constructivo', {}]}
        >>> c.replace_to_both_axis('2007-6', '184')
        >>> c.dimensions
        {'tiempo': ['tiempo', 'mes', {'anio': ['2007'], 'mes': ['6']}], 'pieza': ['pieza', 'modelo', {'grupo_constructivo': ['184']}]}
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], [':pieza', 'grupo_constructivo', {}]], measures=[['stock']], ore=[])
        >>> c.dimensions
        {'tiempo': ['tiempo', 'mes', {}], 'pieza': ['pieza', 'grupo_constructivo', {}]}
        >>> c.replace_to_both_axis('2007-6', '184')
        >>> c.dimensions
        {'tiempo': ['tiempo', 'mes', {'anio': ['2007'], 'mes': ['6']}], 'pieza': ['pieza', 'modelo', {'grupo_constructivo': ['184']}]}
        >>>
        '''
        self.replace_to(0, value0)
        self.replace_to(1, value1)

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
            raise InvalidDimension(main_axis)


        other_dimensions = [x for x in Meta.fact_table_dimensions_meta[self.ft] if x not in self.dimensions.keys()]
        if not other_axis in other_dimensions:
            raise InvalidDimension(dimension)


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
        levels_parent = Meta.parent_list(first_dimension[0], first_dimension[1])

        if levels_parent == ['TODO']:
            return "select 'TODO' as TODO"
        else:
            select = "|| '-' ||".join(levels_parent)
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
        ['proveedor', 'tipo_pieza']
        '''

        total_dimensions = Meta.fact_table_dimensions_meta[self.ft]
        return [x for x in total_dimensions if x not in (self.dimensions.keys())]

    def _select(self):
        '''
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['ft_ventas', 'cantidad', 'sum']], ore=[])
        >>> c._select()
        "SELECT td_tiempo.anio|| '-' ||td_tiempo.mes as columns, td_pieza.grupo_constructivo as rows, sum(ft_ventas.cantidad) as ft_ventas__cantidad"
        >>>
        '''
        levels_with_parent = []

        for dimension in self.dimensions_order:
            (name, level, restriction) = self.dimensions[dimension]
            levels_with_parent.append(Meta.parent_list(name, level))
        measures = ['%s(%s.%s) as %s__%s' % (x[2], x[0], x[1], x[0], x[1]) for x in self.measures]

        if levels_with_parent[0] == ["TODO"]:
            columns_string = "'TODO' as columns"
        else:
            columns_string = "|| '-' ||".join(levels_with_parent[0]) + " as columns"

        if levels_with_parent[1] == ["TODO"]:
            rows_string = "'TODO' as rows"
        else:
            rows_string   = "|| '-' ||".join(levels_with_parent[1]) + " as rows"

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
        "WHERE trim(td_tiempo.anio) in(trim('2005'), trim('1999')) "
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {'anio': ['2005', '1999']}], ['pieza', 'grupo_constructivo', {}]], measures=[['cantidad', 'sum']], ore=[['proveedor', 'proveedor', {'proveedor': ['Mercedez Benz']}]])
        >>> c._where()
        "WHERE trim(td_tiempo.anio) in(trim('2005'), trim('1999')) AND trim(td_proveedor.proveedor) in(trim('Mercedez Benz')) "
        '''

        levels_with_parent = []
        where = []

        for dimension in self.dimensions_order:
            (name, level, restriction) = self.dimensions[dimension]
            levels_with_parent.append(Meta.parent_list(name, level))
            if restriction:
                for level, val in restriction.items():
                    valores = ", ".join(["trim('%s')" % v for v in val])
                    where.append("trim(td_%s.%s) in(%s)" % ( name, level, valores))

        for other_dim in self.ore:
            (name, level, restriction) = other_dim
            if restriction:
                for level, val in restriction.items():
                    valores = ", ".join(["trim('%s')" % v for v in val])
                    where.append("trim(td_%s.%s) in(%s)" % ( name, level, valores))

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
                levels_with_parent.append(Meta.parent_list(name, level))

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
                levels_with_parent.append(Meta.parent_list(name, level))

        if levels_with_parent == []:
            return ''
        else:
            values = ', '.join([", ".join(x) for x in levels_with_parent])
            order_by = "ORDER BY %s " % values
            return order_by

    def sql(self):
        '''
        >>> c = Cubiculo(ft='ventas', dimensions=[['tiempo', 'mes', {}], ['pieza', 'grupo_constructivo', {}]], measures=[['ft_ventas', 'cantidad', 'sum']], ore=[])
        >>> c.sql()
        "SELECT td_tiempo.anio|| '-' ||td_tiempo.mes as columns, td_pieza.grupo_constructivo as rows, sum(ft_ventas.cantidad) as ft_ventas__cantidad\\nFROM ft_ventas JOIN td_tiempo on (ft_ventas.fk_tiempo = td_tiempo.id) JOIN td_pieza on (ft_ventas.fk_pieza = td_pieza.id) \\n\\nGROUP BY td_tiempo.anio, td_tiempo.mes, td_pieza.grupo_constructivo \\nORDER BY td_tiempo.anio, td_tiempo.mes, td_pieza.grupo_constructivo \\n"
        >>>
        '''

        sql = "%s\n" * 5 % (self._select(),self._from(), self._where(), self._group_by(), self._order_by() )

        f = file("/tmp/cubiculo-debug","a")
        f.write(sql+"\n")
        f.close()
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
            if self.dimensions_fixed.get(dim, False):
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
        x_levels    = Meta.dimension_meta[x_dimension]

        highest_level = x_levels[-1]
        actual_level = self.dimensions[x_dimension][1]

        if highest_level == actual_level:
            return False

        return True

    def can_drill_x(self):
        '''
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'mes', {}], ['pieza', 'pieza', {}]], measures=[['stock']], ore=[])
        >>> c.can_drill_x()
        True
        >>> c = Cubiculo(ft='movimientos', dimensions=[['tiempo', 'anio', {}], ['pieza', 'pieza', {}]], measures=[['stock']], ore=[])
        >>> c.can_drill_x()
        True
        '''

        x_dimension = self.dimensions_order[0]
        x_levels    = Meta.dimension_meta[x_dimension]

        lowest_level = x_levels[0]
        actual_level = self.dimensions[x_dimension][1]

        #if lowest_level == actual_level:
            #return False

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
        y_levels    = Meta.dimension_meta[y_dimension]

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
        True
        '''

        y_dimension = self.dimensions_order[1]
        y_levels    = Meta.dimension_meta[y_dimension]

        lowest_level = y_levels[0]
        actual_level = self.dimensions[y_dimension][1]

        #if lowest_level == actual_level:
            #return False

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
