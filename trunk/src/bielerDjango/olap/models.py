import psycopg2
import psycopg2.extras
import copy

import cubiculo
from pprint import pprint


def isFloat(s):
    try:
        return float(s) or True
    except:
        return False

def compare(a,b):
    primero = a.split(' - ')
    segundo = b.split(' - ')
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

class Cube:
    '''
    >>> c = Cube()
    >>> c.add(1,1,{"c":1})
    >>> c.add(1,2,{"c":3})
    >>> c.add(2,1,{"c":2})
    >>> c.add(2,2,{"c":7})
    >>> c.add(1,1,{"a":10})
    >>> c.add(1,2,{"a":10})
    >>> c.add(2,1,{"a":40})
    >>> c.add(2,2,{"a":42})
    >>> c.add(3,2,{"a":78})
    >>> c.add(4,3,{"a":79})
    >>> for a in c.columns(y=3, measure="a"):
    ...   print a
    ...
    None
    None
    None
    79
    >>> for a in c.columns(y=2, measure="a"):
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
    
    def set_default(self, value):
        ''' 
        >>> c = Cube()
        >>> c.add(1,1,{"c":1})
        >>> c.add(1,2,{"c":3})
        >>> c.add(2,1,{"c":2})
        >>> c.add(2,2,{"c":7})
        >>> c.add(1,1,{"a":10})
        >>> c.add(1,2,{"a":10})
        >>> c.add(2,1,{"a":40})
        >>> c.add(2,2,{"a":42})
        >>> c.add(3,2,{"a":78})
        >>> c.add(4,3,{"a":79})
        >>> for a in c.columns(y=3, measure="a"):
        ...   print a
        ...
        None
        None
        None
        79
        >>> c.set_default(-1)
        >>> for a in c.columns(y=3, measure="a"):
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
        >>> c.add('uno',1,{"c":1})
        >>> c.add('uno',2,{"c":3})
        >>> c.add('dos',1,{"c":2})
        >>> c.add('dos',2,{"c":7})
        >>> pprint(c.data)
        {('dos', 1, 'c'): 2,
         ('dos', 2, 'c'): 7,
         ('uno', 1, 'c'): 1,
         ('uno', 2, 'c'): 3}
        >>> c.add('uno',1,{"a":8})
        >>> c.add('uno',2,{"a":2})
        >>> c.add('dos',1,{"a":1})
        >>> c.add('dos',2,{"a":5})
        >>> pprint(c.data)
        {('dos', 1, 'a'): 1,
         ('dos', 1, 'c'): 2,
         ('dos', 2, 'a'): 5,
         ('dos', 2, 'c'): 7,
         ('uno', 1, 'a'): 8,
         ('uno', 1, 'c'): 1,
         ('uno', 2, 'a'): 2,
         ('uno', 2, 'c'): 3}
        >>> c.dim_x
        ['dos', 'uno']
        >>> c.dim_y
        [1, 2]
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
        >>> c.add(1,1,{"c":1})
        >>> c.add(1,2,{"c":3})
        >>> c.add(2,1,{"c":2})
        >>> c.add(2,2,{"c":7})
        >>> c.add(1,1,{"a":10})
        >>> c.add(1,2,{"a":10})
        >>> c.add(2,1,{"a":40})
        >>> c.add(2,2,{"a":42})
        >>> pprint(c.get(2, 1))
        {'a': 40, 'c': 2}
        >>> 
        >>> c = Cube()
        >>> c.add(1,1,{"c":1})
        >>> c.add(1,2,{"c":3})
        >>> c.add(1,3,{"c":2})
        >>> c.add(1,4,{"c":7})
        >>> c.add_y_value(5)
        >>> c.get(1,5)
        {'c': None}
        '''
        
        t = {}
        for m in self.measures:
            t[m] = self.data.get((x, y, m), self.default)
            
        return t
        
            
    def columns(self, y, measure):   
        '''
        >>> c = Cube()
        >>> i = c.columns(y=2, measure="c")
        >>> for a in i: print a
        >>> c.add(1,1,{"c":1})
        >>> c.add(1,2,{"c":3})
        >>> c.add(2,1,{"c":2})
        >>> c.add(2,2,{"c":7})
        >>> for a in c.columns(y=2, measure="c"):
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
        >>> i = c.rows(x=2, measure="c")
        >>> for a in i: print a
        >>> c.add(1,1,{"c":1})
        >>> c.add(1,2,{"c":3})
        >>> c.add(2,1,{"c":2})
        >>> c.add(2,2,{"c":7})
        >>> for a in c.rows(x=2, measure="c"):
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
        >>> i = c.get_measures(x=2, y=2)
        >>> for a in i: print a
        >>> c.add(1,1,{"c":1})
        >>> c.add(1,2,{"c":3})
        >>> c.add(2,1,{"c":2})
        >>> c.add(2,2,{"c":7})
        >>> i = c.get_measures(x=2, y=2)
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
        >>> c = Cube()
        >>> c.add_x_value('1998-7', 7)
        >>> c.add_x_value('2000-11', )
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
        >>> c.add(1,1,{"c":1})
        >>> c.add(2,1,{"c":2})
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
        >>> c.add('uno',1,{"c":1})
        >>> c.add('uno',2,{"c":3})
        >>> c.add('uno',3,{"c":2})
        >>> c.add('uno',4,{"c":7})
        >>> pprint(c.data)
        {('uno', 1, 'c'): 1,
         ('uno', 2, 'c'): 3,
         ('uno', 3, 'c'): 2,
         ('uno', 4, 'c'): 7}
        >>> for a in c.columns(y=2, measure="c"):
        ...   print a
        ...
        3
        >>> c.fit(4,4)
        >>> for a in c.columns(y=2, measure="c"):
        ...   print a
        ...
        3
        3
        3
        3
        >>> c.dim_x
        ['uno', 'uno', 'uno', 'uno']
        >>> c.dim_y
        [1, 2, 3, 4]
        >>> c = Cube()
        >>> c.add('uno',1,{"c":1})
        >>> c.add('uno',2,{"c":3})
        >>> c.add('dos',1,{"c":2})
        >>> c.add('dos',2,{"c":7})
        >>> c.fit(4,4)
        >>> pprint(c.dim_x)
        ['dos', 'dos', 'uno', 'uno']
        >>> c.dim_y
        [1, 1, 2, 2]
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


class Report:
    def __init__(self,report_name, x, y, xl, yl, xr, yr, ore, member_function):
        ##VIENE DE LA BD en base a report
        self.fts = ["compras", "ventas"]
        self.measures = {'compras': [["cantidad", "sum"], ['costo_dolar', 'sum']], 'ventas': [["precio_venta_dolares", "sum"], ["margen_dolares", "sum"]]}
        self.member_function = member_function
        ##VIENE DE LA BD
        self.x = x
        self.xl = xl
        self.y = y
        self.yl = yl
        self.xr = xr
        self.yr = yr
        self.ore = ore        
         
        self.cubiculos = {}
        for ft in self.fts:
            #dimensions = [[self.x,self.xl,eval(self.xr)],[self.y,self.yl,eval(self.yr)]]
            dimensions = [[self.x,self.xl,{}],[self.y,self.yl,{}]]
            cub=cubiculo.Cubiculo(ft,dimensions,self.measures[ft], eval(self.ore))
            self.cubiculos[ft] = cub 

    def pivot(self, request):
        for cubiculo in self.cubiculos.values():       
            cubiculo.pivot()
        
        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.absolute_url(request)

    def drill(self,request, axis):
        for cubiculo in self.cubiculos.values():       
            cubiculo.drill(axis)
        
        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.absolute_url(request)    

    def roll(self, request, axis):
        for cubiculo in self.cubiculos.values():       
            cubiculo.roll(axis)
        
        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.absolute_url(request)        

    def drill_replacing(self, request, axis, value):
        for cubiculo in self.cubiculos.values():       
            cubiculo.drill_replacing(axis, value)
        
        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.absolute_url(request)        

    def drill_replacing2(self, request, value0, value1):
        for cubiculo in self.cubiculos.values():       
            cubiculo.drill_replacing(0, value0)
            cubiculo.drill_replacing(1, value1)

        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.absolute_url(request)
        
    def dice(self, request, main_axis, other_axis):
        for cubiculo in self.cubiculos.values():       
            cubiculo.dice(main_axis, other_axis)

        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.absolute_url(request)
       
    def dimension_values(self, axis):
        con_dwh = psycopg2.connect(host="127.0.0.1", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
        cursor_dwh = con_dwh.cursor()        

        first_cubiculo = self.cubiculos[self.fts[0]]
        sql_dimension_values = first_cubiculo.dimension_values(int(axis))
        cursor_dwh.execute(sql_dimension_values)
        axis_values = cursor_dwh.fetchall()        
        axis_values = [x[0]  for x in axis_values]
        
        return axis_values

    def getMainAxisList(self):
        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.getMainAxisList()
    
    def getOtherAxisList(self):
        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.getOtherAxisList()
    
    def build_cube(self):
        tables = {}
        count = {}
        dicttable = {}
        
        con_dwh = psycopg2.connect(host="127.0.0.1", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")        
       
       
        for ft in self.fts:
            cursor_dwh = con_dwh.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            sql = self.cubiculos[ft].sql()
            cursor_dwh.execute(sql)
           
            tables[ft] = cursor_dwh.fetchall()
            count[ft] = 0
   
            try:
                dicttable[ft] = dict(tables[ft][count[ft]])
            except:
                dicttable[ft] = {}            
       
        x_axis = self.dimension_values(0)
        y_axis = self.dimension_values(1)
       
        body = {}
       
        for x in x_axis:
            for y in y_axis:
   
                #En caso que no haya clave para el elemento se crea
                if not body.get(y, False):
                    body[y] = []
               
                params = {}
                for ft in self.fts:
                    print "dicttable"
                    pprint(dicttable[ft])                       
                    #El elemento de la cabecera de table podria no coincidir con
                    #los indices recorridos porque table esta ordenado pero incompleto
                    if x == dicttable[ft].get('columns', False) and y == dicttable[ft].get('rows', False):
                        measuresList = self.cubiculos[ft].getMeasuresList()
                        print "measuresList"
                        pprint(measuresList)
                       
                        for measure in measuresList:
                            params[measure] = dicttable[ft][measure] 
                                                  
                        count[ft] += 1
                       
                        try:
                            dicttable[ft] = dict(tables[ft][count[ft]])
                        except:
                            dicttable[ft] = {}
                            
                       
                value = self.member_function(**params)
                body[y].append(value)
               
        cube = Cube()
        cube.header = x_axis
        cube.body = body
        cube.body_order = y_axis
        return cube 
    


class Report2:
    def __init__(self,ft1, x1, y1, xl1, yl1, xr1, yr1, ore1,ft2, x2, y2, xl2, yl2, xr2, yr2, ore2, member_function=None):
        ##VIENE DE LA BD en base a report
        self.fts = [ft1, ft2]
        self.measures = {'movimientos': [["stock", "avg"]], 'ventas': [["cantidad", "sum"], ["margen_dolares", "sum"]]}
        self.member_function = member_function
        ##VIENE DE LA BD
        exr1        = eval(xr1)
        d11         = [x1, xl1, exr1]
        eyr1        = eval(yr1)
        d12         = [y1, yl1, eyr1]
        dimensions1 = [d11, d12]
        eore1       = eval(ore1)
        cubiculo1   = cubiculo.Cubiculo(ft1,dimensions1, self.measures[ft1], eore1)

        exr2 = eval(xr2)
        d21 = [x2, xl2,exr2]
        eyr2 = eval(yr2)
        d22 = [y2, yl2, eyr2]
        dimensions2 = [d21, d22]
        eore2 = eval(ore2)
        cubiculo2   = cubiculo.Cubiculo(ft2, dimensions2, self.measures[ft2], eore2)


        self.cubiculos = {}
        self.cubiculos[ft1] = cubiculo1
        self.cubiculos[ft2] = cubiculo2

    def pivot(self, request):
        for cubiculo in self.cubiculos.values():       
            cubiculo.pivot()
        
        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.absolute_url(request)

    def drill(self,request, axis):
        for cubiculo in self.cubiculos.values():       
            cubiculo.drill(axis)
        
        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.absolute_url(request)    

    def roll(self, request, axis):
        for cubiculo in self.cubiculos.values():       
            cubiculo.roll(axis)
        
        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.absolute_url(request)        

    def drill_replacing(self, request, axis, value):
        for cubiculo in self.cubiculos.values():       
            cubiculo.drill_replacing(axis, value)
        
        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.absolute_url(request)        

    def drill_replacing2(self, request, value0, value1):
        for cubiculo in self.cubiculos.values():       
            cubiculo.drill_replacing(0, value0)
            cubiculo.drill_replacing(1, value1)

        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.absolute_url(request)
        
    def dice(self, request, main_axis, other_axis):
        for cubiculo in self.cubiculos.values():       
            cubiculo.dice(main_axis, other_axis)

        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.absolute_url(request)
       
    def dimension_values(self, axis, cubiculo):
        con_dwh = psycopg2.connect(host="127.0.0.1", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
        cursor_dwh = con_dwh.cursor()        

        sql_dimension_values = cubiculo.dimension_values(int(axis))
        cursor_dwh.execute(sql_dimension_values)
        axis_values = cursor_dwh.fetchall()        
        axis_values = [x[0]  for x in axis_values]
        
        return axis_values

    def getMainAxisList(self):
        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.getMainAxisList()
    
    def getOtherAxisList(self):
        first_cubiculo = self.cubiculos[self.fts[0]]
        return first_cubiculo.getOtherAxisList()
    
    def get_sql(self, ft):
        cubiculo = self.cubiculos[ft]
        return cubiculo.sql()
    
    def exec_sql(self, sql):
        con_dwh = psycopg2.connect(host="127.0.0.1", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
        cursor_dwh = con_dwh.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        cursor_dwh.execute(sql)  
         
        return cursor_dwh.fetchall()

    def fill_table(self, cube, incomplete_table):
        for row in incomplete_table:
            dict_row = dict(row)
            cube.add(dict_row.pop('rows'),dict_row.pop('columns'),dict_row) 
            
    
    def complete_dimensions(self, cube, cubiculo):
        x_axis = self.dimension_values(1, cubiculo)
        y_axis = self.dimension_values(0, cubiculo)
        
        for x in x_axis:
            cube.add_x_value(x)

        for y in y_axis:
            cube.add_y_value(y)
            
    def fit(self, complete_cubes):
        max_dimensions = (0, 0)
        for cube in complete_cubes:
            pprint(cube.dimensions())
            max_dimensions = max(max_dimensions, cube.dimensions())

        print "max dimensions"
        pprint(max_dimensions)

        for cube in complete_cubes:
            cube.fit(max_dimensions[0], max_dimensions[1])
            
        pprint(complete_cubes[0].dimensions())
        pprint(complete_cubes[1].dimensions())


    def merge(self, cubes):
        first  = cubes[0]
        second = cubes[1]
        
        temp_cube = Cube()
        
        print "values"
        for x1, x2 in zip(first.dim_x, second.dim_x):           
            for y1, y2 in zip(first.dim_y, second.dim_y):                
                first_cube_values  = first.get(x1, y1)
                second_cube_values = second.get(x2, y2)
                
                temp = self.member_function(first = first_cube_values, second = second_cube_values)
                
                
                temp_cube.add(x1, y1, {'result': temp})
        
        return temp_cube
        

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

        
        pprint(final_cube.data)
        
        return final_cube
    
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
