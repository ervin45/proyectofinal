import psycopg2
import psycopg2.extras
import copy

import cubiculo

import copy
from pprint import pprint

from odict import odict

from member_functions import *

too_many_rows = 2000
too_many_cells = 20000

def isFloat(s):
    try:
        return float(s) or True
    except:
        return False

def compare(a,b):
    primero = str(a).split(' - ')
    segundo = str(b).split(' - ')
    for x,y in zip(primero, segundo):
        if isFloat(x) and isFloat(y):
            if float(x) > float(y):
                return 1
            elif float(x) < float(y):
                return -1
        else:
            if x > y:
                return 1
            elif x < y:
                return -1
    print "returning 0"
    return 0

def compare_dicts_asc(a, b):
    if a[1] > b[1]:
        return 1
    elif a[1] < b[1]:
        return -1
    return 0

def compare_dicts_desc(a, b):
    if a[1] > b[1]:
        return -1
    elif a[1] < b[1]:
        return 1
    return 0

def top_ordered(d, total_elements = 10, order = "desc"):
    temp = d.items()
    if order=="desc":
        order_func = compare_dicts_desc
    else:
        order_func = compare_dicts_asc

    temp.sort(order_func)
    rtn = temp[:total_elements]
    return rtn



class Cube:
    '''
    >>> c = Cube()
    >>> c.add('1','1',{"c":1})
    >>> c.add('1','2',{"c":3})
    >>> c.add('2','1',{"c":2})
    >>> c.add('2','2',{"c":7})
    >>> c.add('1','1',{"a":10})
    >>> c.add('1','2',{"a":10})
    >>> c.add('2','1',{"a":40})
    >>> c.add('2','2',{"a":42})
    >>> c.add('3','2',{"a":78})
    >>> c.add('4','3',{"a":79})
    >>> for a in c.columns(y='3', measure="a"):
    ...   print a
    ...
    None
    None
    None
    79
    >>> for a in c.columns(y='2', measure="a"):
    ...   print a
    ...
    10
    42
    78
    None
    >>>  
    '''

    def __init__(self):
        self.dim_x = []
        self.dim_y = []
        self.measures = []
        self.data = {}
        self.default = None
        self._can_roll_x = True
        self._can_roll_y = True
        self._can_drill_x = True
        self._can_drill_y = True
        self.info = []
    
    def set_default(self, value):
        ''' 
        >>> c = Cube()
        >>> c.add('1','1',{"c":1})
        >>> c.add('1','2',{"c":3})
        >>> c.add('2','1',{"c":2})
        >>> c.add('2','2',{"c":7})
        >>> c.add('1','1',{"a":10})
        >>> c.add('1','2',{"a":10})
        >>> c.add('2','1',{"a":40})
        >>> c.add('2','2',{"a":42})
        >>> c.add('3','2',{"a":78})
        >>> c.add('4','3',{"a":79})
        >>> for a in c.columns(y='3', measure="a"):
        ...   print a
        ...
        None
        None
        None
        79
        >>> c.set_default(-1)
        >>> for a in c.columns(y='3', measure="a"):
        ...   print a
        ...
        -1
        -1
        -1
        79
        >>>
        '''
        self.default = value
    
    def add(self, x, y, measures_values):
        ''' 
        >>> c = Cube()
        >>> c.add('uno','1',{"c":1})
        >>> c.add('uno','2',{"c":3})
        >>> c.add('dos','1',{"c":2})
        >>> c.add('dos','2',{"c":7})
        >>> pprint(c.data)
        {('dos', '1', 'c'): 2,
         ('dos', '2', 'c'): 7,
         ('uno', '1', 'c'): 1,
         ('uno', '2', 'c'): 3}
        >>> c.add('uno','1',{"a":8})
        >>> c.add('uno','2',{"a":2})
        >>> c.add('dos','1',{"a":1})
        >>> c.add('dos','2',{"a":5})
        >>> pprint(c.data)
        {('dos', '1', 'a'): 1,
         ('dos', '1', 'c'): 2,
         ('dos', '2', 'a'): 5,
         ('dos', '2', 'c'): 7,
         ('uno', '1', 'a'): 8,
         ('uno', '1', 'c'): 1,
         ('uno', '2', 'a'): 2,
         ('uno', '2', 'c'): 3}
        >>> c.dim_x
        ['dos', 'uno']
        >>> c.dim_y
        ['1', '2']
        >>> 
        '''
        self.add_x_value(x)
        self.add_y_value(y)
        for k, v in measures_values.items():
            self.data[(x,y,k)] =  v
            self.add_measure_value(k)
            
    def get(self, x, y):
        ''' 
        >>> c = Cube()
        >>> from pprint import pprint
        >>> c.add('1','1',{"c":1})
        >>> c.add('1','2',{"c":3})
        >>> c.add('2','1',{"c":2})
        >>> c.add('2','2',{"c":7})
        >>> c.add('1','1',{"a":10})
        >>> c.add('1','2',{"a":10})
        >>> c.add('2','1',{"a":40})
        >>> c.add('2','2',{"a":42})
        >>> pprint(c.get('2', '1'))
        {'a': 40, 'c': 2}
        >>> 
        >>> c = Cube()
        >>> c.add('1','1',{"c":1})
        >>> c.add('1','2',{"c":3})
        >>> c.add('1','3',{"c":2})
        >>> c.add('1','4',{"c":7})
        >>> c.add_y_value('5')
        >>> c.get('1','5')
        {'c': None}
        '''
        
        t = {}
        for m in self.measures:
            t[m] = self.data.get((x, y, m), self.default)
            
        return t
        
            
    def columns(self, y, measure):   
        '''
        >>> c = Cube()
        >>> i = c.columns(y='2', measure="c")
        >>> for a in i: print a
        >>> c.add('1','1',{"c":1})
        >>> c.add('1','2',{"c":3})
        >>> c.add('2','1',{"c":2})
        >>> c.add('2','2',{"c":7})
        >>> for a in c.columns(y='2', measure="c"):
        ...   print a
        ...
        3
        7
        >>>
        '''
        
        for x in self.dim_x:
            yield self.data.get((x,y,measure), self.default)
                
    def rows(self, x, measure):
        '''
        >>> c = Cube()
        >>> i = c.rows(x='2', measure="c")
        >>> for a in i: print a
        >>> c.add('1','1',{"c":1})
        >>> c.add('1','2',{"c":3})
        >>> c.add('2','1',{"c":2})
        >>> c.add('2','2',{"c":7})
        >>> for a in c.rows(x='2', measure="c"):
        ...   print a
        ...
        2
        7
        >>>
        '''
        
        for y in self.dim_y:
            yield self.data.get((x,y,measure), self.default)        
            
    def get_measures(self, x, y):
        '''
        >>> c = Cube()
        >>> i = c.get_measures(x='2', y='2')
        >>> for a in i: print a
        >>> c.add('1','1',{"c":1})
        >>> c.add('1','2',{"c":3})
        >>> c.add('2','1',{"c":2})
        >>> c.add('2','2',{"c":7})
        >>> i = c.get_measures(x='2', y='2')
        >>> for a in i: print a
        ...
        7
        >>>
        '''
        for measure in self.measures:
            yield self.data.get((x,y,measure), self.default)

    def add_x_value(self, x):
        '''
        >>> c = Cube()
        >>> c.dim_x
        []
        >>> c.add_x_value('2007')
        >>> c.dim_x
        ['2007']
        >>> c.add_y_value('Producto_1')
        >>> i = c.get_measures(x='2007', y='Producto_1')
        >>> for a in i: print a
        ...
        >>>
        '''
        if x not in self.dim_x:
            self.dim_x.append(x)
            self.dim_x.sort(compare)

    def add_y_value(self, y):
        '''
        >>> c = Cube()
        >>> c.dim_y
        []
        >>> c.add_y_value('2007')
        >>> c.dim_y
        ['2007']
        >>> c.add_x_value('Producto_1')
        >>> i = c.get_measures(y='2007', x='Producto_1')
        >>> for a in i: print a
        ...
        >>>
        '''
        if y not in self.dim_y:
            self.dim_y.append(y)
            self.dim_y.sort(compare)

    def add_measure_value(self, measure):
        '''
        >>> c = Cube()
        >>> c.measures
        []
        >>> c.add_measure_value('cantidad')
        >>> c.measures
        ['cantidad']
        >>>
        '''
        if measure not in self.measures:
            self.measures.append(measure)
            self.measures.sort(compare)

    def dimensions(self):
        '''
        >>> c = Cube()
        >>> c.add('1','1',{"c":1})
        >>> c.add('2','1',{"c":2})
        >>> c.dimensions()
        (2, 1)
        >>> c.fit(2,24)
        >>> c.dimensions()
        (2, 24)
        >>>
        '''

        return (len(self.dim_x), len(self.dim_y))
        
    def fit(self, x, y):
        '''
        >>> from pprint import pprint
        >>> c = Cube()
        >>> c.add('uno','1',{"c":1})
        >>> c.add('uno','2',{"c":3})
        >>> c.add('uno','3',{"c":2})
        >>> c.add('uno','4',{"c":7})
        >>> pprint(c.data)
        {('uno', '1', 'c'): 1,
         ('uno', '2', 'c'): 3,
         ('uno', '3', 'c'): 2,
         ('uno', '4', 'c'): 7}
        >>> for a in c.columns(y='2', measure="c"):
        ...   print a
        ...
        3
        >>> c.fit(4,4)
        >>> for a in c.columns(y='2', measure="c"):
        ...   print a
        ...
        3
        3
        3
        3
        >>> c.dim_x
        ['uno', 'uno', 'uno', 'uno']
        >>> c.dim_y
        ['1', '2', '3', '4']
        >>> c = Cube()
        >>> c.add('uno','1',{"c":1})
        >>> c.add('uno','2',{"c":3})
        >>> c.add('dos','1',{"c":2})
        >>> c.add('dos','2',{"c":7})
        >>> c.fit(4,4)
        >>> pprint(c.dim_x)
        ['dos', 'dos', 'uno', 'uno']
        >>> c.dim_y
        ['1', '1', '2', '2']
        >>> 
        '''     
        
        
        if x % len(self.dim_x) == 0:
            factor_x = x / len(self.dim_x)
            temp = []
            for i in self.dim_x:
                temp.extend([i] * factor_x)
            self.dim_x = temp
        
        if y % len(self.dim_y) == 0:
            factor_y = y / len(self.dim_y)
            temp = []
            for j in self.dim_y:
                temp.extend([j] * factor_y)
            self.dim_y = temp
            
    def can_roll_x(self):
        return self._can_roll_x
    
    def can_roll_y(self):
        return self._can_roll_y
    
    def can_drill_x(self):
        return self._can_drill_x
    
    def can_drill_y(self):
        return self._can_drill_y
    
    def add_info(self, ft, dimensions, measures, ore):
        self.info.append([ft, dimensions, measures, ore])
        
    def get_info(self):
        return self.info

class CubeTooBig:
    def __init__(self, cells, rows):
        self.cells = cells
        self.rows  = rows


class Report1:
    def __init__(self,ft, x, y, xl, yl, xr, yr, ore, mf, param):
        ##VIENE DE LA BD en base a report
        self.ft = ft
        self.measures = eval(param)
        self.member_function = globals()[mf]
        ##VIENE DE LA BD
        self.x = x
        self.xl = xl
        self.y = y
        self.yl = yl
        self.xr = xr
        self.yr = yr
        self.ore = ore
         
        dimensions = [[self.x,self.xl,eval(self.xr)],[self.y,self.yl,eval(self.yr)]]
        self.cubiculo = cubiculo.Cubiculo(self.ft,dimensions,self.measures, eval(self.ore))
        
    def pivot(self, request):
        self.cubiculo.pivot()
        
        parcial_url = self.cubiculo.parcial_url()
        return self.absolute_url(request, parcial_url)

    def drill(self,request, axis):
        self.cubiculo.drill(axis)
        
        parcial_url = self.cubiculo.parcial_url()
        return self.absolute_url(request, parcial_url)

    def roll(self, request, axis):
        self.cubiculo.roll(axis)
        
        parcial_url = self.cubiculo.parcial_url()
        return self.absolute_url(request, parcial_url)

    def drill_replacing(self, request, axis, value):
        self.cubiculo.drill_replacing(axis, value)
        
        parcial_url = self.cubiculo.parcial_url()
        return self.absolute_url(request, parcial_url)

    def drill_replacing2(self, request, value0, value1):
        self.cubiculo.drill_replacing(0, value0)
        self.cubiculo.drill_replacing(1, value1)

        parcial_url = self.cubiculo.parcial_url()
        return self.absolute_url(request, parcial_url)
        
    def dice(self, request, main_axis, other_axis):
        self.cubiculo.dice(main_axis, other_axis)
        
        parcial_url = self.cubiculo.parcial_url()
        return self.absolute_url(request, parcial_url)
       
    def dimension_values(self, axis):
        con_dwh = psycopg2.connect(host="127.0.0.1", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
        cursor_dwh = con_dwh.cursor()

        sql_dimension_values = self.cubiculo.dimension_values(int(axis))
        cursor_dwh.execute(sql_dimension_values)
        axis_values = cursor_dwh.fetchall()
        axis_values = [x[0]  for x in axis_values]

        return axis_values

    def get_main_axis_list(self):
        return self.cubiculo.get_main_axis_list()

    def get_other_axis_list(self):
        return self.cubiculo.get_other_axis_list()
 
    def get_sql(self, ft):
        return self.cubiculo.sql()

    def exec_sql(self, sql):
        con_dwh = psycopg2.connect(host="127.0.0.1", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
        cursor_dwh = con_dwh.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        cursor_dwh.execute(sql)
        
        if cursor_dwh.rowcount > too_many_rows:
            rows = cursor_dwh.rowcount
            raise CubeTooBig(0, rows)

        return cursor_dwh.fetchall()

    def fill_table(self, cube, incomplete_table):
        for row in incomplete_table:
            dict_row = dict(row)
            cube.add(str(dict_row.pop('rows')),str(dict_row.pop('columns')),dict_row) 


    def complete_dimensions(self, cube, cubiculo):
        x_axis = self.dimension_values(1)
        y_axis = self.dimension_values(0)
        
        if len(x_axis) * len(y_axis) > too_many_cells:
            cells = len(x_axis) * len(y_axis)
            raise CubeTooBig(cells, 0)

        for x in x_axis:
            cube.add_x_value(str(x))

        for y in y_axis:
            cube.add_y_value(str(y))
            
    def _member_function_params(self, x1, y1, cube):
        params = []
        
        measures_values = cube.get(x1, y1)
        for ft, measure, agregation in self.measures:
            params.append(measures_values["%s__%s" % (ft, measure)])
            
        return params
            
    def exec_member_function(self, cube):
        temp_cube = Cube()
        
        pprint(cube)

        for x1 in cube.dim_x:
            for y1 in cube.dim_y:
                
                params = self._member_function_params(x1, y1, cube)
                #cube_values = cube.get(x1, y1)

                temp = self.member_function(*params)

                temp_cube.add(x1, y1, {'result': temp})

        return temp_cube
            
    def set_can_flags(self, cube):
        cube._can_roll_x = self.cubiculo.can_roll_x()
        cube._can_roll_y = self.cubiculo.can_roll_y()
        cube._can_drill_x = self.cubiculo.can_drill_x()
        cube._can_drill_y = self.cubiculo.can_drill_y()
        
    def set_meta_info(self, cube):
        ft = self.cubiculo.ft
        dimensions = self.cubiculo.dimensions
        measures   = self.cubiculo.measures
        ore        = self.ore
        cube.add_info(ft=ft, dimensions=dimensions, measures=measures, ore=ore)

    def build_cube(self):
        cube = Cube()

        sql = self.get_sql(self.ft)
        incomplete_table = self.exec_sql(sql)

        self.fill_table(cube, incomplete_table)
        self.complete_dimensions(cube, self.cubiculo)
        final_cube = self.exec_member_function(cube)
        
        self.set_can_flags(final_cube)
        self.set_meta_info(final_cube)

        return final_cube

    def absolute_url(self, request, parcial_url):
        from django.conf import settings
        
        
        server_ip  = settings.IP        
        mf = self.member_function.__name__
        param = str(self.measures)
        
        url = "http://%s:%s/report/%s%s/param=%s" % (server_ip, request.META['SERVER_PORT'], parcial_url, mf, param)
        print "URL", url
        return url


class Report2:
    def __init__(self,ft1, x1, y1, xl1, yl1, xr1, yr1, ore1,ft2, x2, y2, xl2, yl2, xr2, yr2, ore2, mf, param):
        ##VIENE DE LA BD en base a report
        self.fts = [ft1, ft2]
        self.measures = eval(param)
        self.member_function = globals()[mf]
        ##VIENE DE LA BD
        exr1        = eval(xr1)
        d11         = [x1, xl1, exr1]
        eyr1        = eval(yr1)
        d12         = [y1, yl1, eyr1]
        dimensions1 = [d11, d12]
        eore1       = eval(ore1)

        cubiculo1   = cubiculo.Cubiculo(ft1,dimensions1, self._split_measures(ft1), eore1)

        exr2 = eval(xr2)
        d21 = [x2, xl2,exr2]
        eyr2 = eval(yr2)
        d22 = [y2, yl2, eyr2]
        dimensions2 = [d21, d22]
        eore2 = eval(ore2)
        cubiculo2   = cubiculo.Cubiculo(ft2, dimensions2, self._split_measures(ft2), eore2)


        self.cubiculos = odict()
        self.cubiculos[ft1] = cubiculo1
        self.cubiculos[ft2] = cubiculo2
        
    def _split_measures(self, ft):
        '''
        >>> r = Report2("ventas", "tiempo", "pieza", "anio", "pieza", "{}", "{}", "{}", "movimiento", "tiempo", "pieza", "anio", "pieza", "{}", "{}", "{}", "sumar", '[["ft_movimientos", "stock", "avg"], ["ft_ventas", "cantidad", "sum"], ["ft_ventas", "margen_dolares", "sum"]]')
        >>> r._split_measures("movimientos")
        [['ft_movimientos', 'stock', 'avg']]
        >>> r._split_measures("ventas")
        [['ft_ventas', 'cantidad', 'sum'], ['ft_ventas', 'margen_dolares', 'sum']]
        '''
        result = []
        for measure in self.measures:
            if ft == measure[0][3:]:
                result.append(measure)
        return result

    def pivot(self, request):
        parcial_url = ""
        
        for cubiculo in self.cubiculos.values():       
            cubiculo.pivot()
            parcial_url += cubiculo.parcial_url()
            
        return self.absolute_url(request, parcial_url)

    def drill(self,request, axis):
        parcial_url = ""
        
        for cubiculo in self.cubiculos.values():       
            cubiculo.drill(axis)
            parcial_url += cubiculo.parcial_url()
            
        return self.absolute_url(request, parcial_url)

    def roll(self, request, axis):
        parcial_url = ""
        
        for cubiculo in self.cubiculos.values():       
            cubiculo.roll(axis)
            parcial_url += cubiculo.parcial_url()
            
        return self.absolute_url(request, parcial_url)

    def drill_replacing(self, request, axis, value):
        parcial_url = ""
        
        for cubiculo in self.cubiculos.values():       
            cubiculo.drill_replacing(axis, value)
            parcial_url += cubiculo.parcial_url()
            
        return self.absolute_url(request, parcial_url)

    def drill_replacing2(self, request, value0, value1):
        parcial_url = ""
        
        for cubiculo in self.cubiculos.values():       
            cubiculo.drill_replacing(0, value0)
            cubiculo.drill_replacing(1, value1)
            
            parcial_url += cubiculo.parcial_url()
            
        return self.absolute_url(request, parcial_url)

    def dice(self, request, main_axis, other_axis):
        parcial_url = ""
        
        for cubiculo in self.cubiculos.values():       
            cubiculo.dice(main_axis, other_axis)
            parcial_url += cubiculo.parcial_url()
            
        return self.absolute_url(request, parcial_url)

    def dimension_values(self, axis, cubiculo):
        con_dwh = psycopg2.connect(host="127.0.0.1", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
        cursor_dwh = con_dwh.cursor()        

        sql_dimension_values = cubiculo.dimension_values(int(axis))
        cursor_dwh.execute(sql_dimension_values)
        axis_values = cursor_dwh.fetchall()        
        axis_values = [x[0]  for x in axis_values]

        return axis_values

    def get_main_axis_list(self):
        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.get_main_axis_list()

    def get_other_axis_list(self):
        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.get_other_axis_list()

    def get_sql(self, ft):
        cubiculo = self.cubiculos[ft]
        return cubiculo.sql()

    def exec_sql(self, sql):
        con_dwh = psycopg2.connect(host="127.0.0.1", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
        cursor_dwh = con_dwh.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        cursor_dwh.execute(sql)
        
        if cursor_dwh.rowcount > too_many_rows:
            rows = cursor_dwh.rowcount
            raise CubeTooBig(0, rows)

        return cursor_dwh.fetchall()

    def fill_table(self, cube, incomplete_table):
        for row in incomplete_table:
            dict_row = dict(row)
            cube.add(str(dict_row.pop('rows')),str(dict_row.pop('columns')),dict_row) 


    def complete_dimensions(self, cube, cubiculo):
        x_axis = self.dimension_values(1, cubiculo)
        y_axis = self.dimension_values(0, cubiculo)
        
        if len(x_axis) * len(y_axis) > too_many_cells:
            cells = len(x_axis) * len(y_axis)
            raise CubeTooBig(cells, 0)

        for x in x_axis:
            cube.add_x_value(str(x))

        for y in y_axis:
            cube.add_y_value(str(y))

    def fit(self, complete_cubes):
        max_dimensions = (0, 0)
        for cube in complete_cubes:
            pprint(cube.dimensions())
            max_dimensions = max(max_dimensions, cube.dimensions())

        print "max dimensions"
        pprint(max_dimensions)

        for cube in complete_cubes:
            cube.fit(max_dimensions[0], max_dimensions[1])

    def _member_function_params(self, x1, y1, x2, y2, cube1, cube2):
        params = []
        
        measures_values = {}
        measures_values.update(cube1.get(x1, y1))
        measures_values.update(cube2.get(x2, y2))
            
        for ft, measure, agregation in self.measures:
            params.append(measures_values["%s__%s" % (ft, measure)])

        return params


    def merge(self, cubes):
        first  = cubes[0]
        second = cubes[1]

        temp_cube = Cube()

        for x1, x2 in zip(first.dim_x, second.dim_x):
            for y1, y2 in zip(first.dim_y, second.dim_y):

                params = self._member_function_params(x1, y1, x2, y2, first, second)

                temp = self.member_function(*params)

                temp_cube.add(x1, y1, {'result': temp})

        return temp_cube

    def set_can_flags(self, cube):
        cube._can_roll_x  = any(x.can_roll_x()  for x in self.cubiculos.values())
        cube._can_roll_y  = any(x.can_roll_y()  for x in self.cubiculos.values())
        cube._can_drill_x = any(x.can_drill_x() for x in self.cubiculos.values())
        cube._can_drill_y = any(x.can_drill_y() for x in self.cubiculos.values())
        

    def order_and_slice_the_cube(self, cube, total_elements=2, order="desc"):
        cube.data = dict(top_ordered(cube.data, total_elements, order))
        return cube

    def set_meta_info(self, cube):
        ft = [x for x in self.fts]
        dimensions = self.cubiculos[self.fts[0]].dimensions
        measures   = [x.measures for x in self.cubiculos.values()]
        ore        = [x.ore for x in self.cubiculos.values()]
        cube.add_info(ft=ft, dimensions=dimensions, measures=measures, ore=ore)
        
    def set_meta_info(self, cube):
        for ft in self.fts:
            ft = self.cubiculos[ft].ft
            dimensions = self.cubiculos[ft].dimensions
            measures   = self.cubiculos[ft].measures
            ore        = self.cubiculos[ft].ore
            cube.add_info(ft=ft, dimensions=dimensions, measures=measures, ore=ore)        



    def build_cube(self):
        complete_cubes = []
        for ft in self.fts:
            sql = self.get_sql(ft)
            incomplete_table = self.exec_sql(sql)

            cube = Cube()
            self.fill_table(cube, incomplete_table)
            self.complete_dimensions(cube, self.cubiculos[ft])
            complete_cubes.append(cube)

        self.fit(complete_cubes)
        final_cube = self.merge(complete_cubes)
        ## if has_cube_function.... blah blah
        final_cube = self.order_and_slice_the_cube(final_cube)
        self.set_can_flags(final_cube)
        self.set_meta_info(final_cube)

        return final_cube
        
    def absolute_url(self, request, parcial_url):
        from django.conf import settings
        server_ip  = settings.IP
        mf = self.member_function.__name__
        param = str(self.measures)
        
        url = "http://%s:%s/report2/%s%s/param=%s" % (server_ip, request.META['SERVER_PORT'], parcial_url, mf, param)
        return url
    
class Ajax_responser:
        @staticmethod
        def get_dimensions(ft):
            return cubiculo.Meta.get_dimensions(ft)

        @staticmethod
        def get_levels(dimension):
            return copy.copy(cubiculo.Meta.get_levels(dimension))
        
        @staticmethod
        def get_values(dimension, level):
            con_dwh = psycopg2.connect(host="127.0.0.1", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
            cursor_dwh = con_dwh.cursor()

            sql = "SELECT distinct(%s) FROM td_%s" % (level, dimension)
            cursor_dwh.execute(sql)
            
            
            return [str(x[0]) for x in cursor_dwh.fetchall()]
        
        @staticmethod
        def get_measures(ft):
            return cubiculo.Meta.get_measures(ft)        

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
