import psycopg2
import psycopg2.extras
import copy

import cubiculo
from pprint import pprint

class Cube:
    pass              
    
class Report:
    def __init__(self,report_name, x, y, xl, yl, xr, yr, ore, member_function):
        ##VIENE DE LA BD en base a report
        self.ft = "compras" #report
        self.measures = [["cantidad", "sum"],['costo_pesos', 'sum']]
        self.member_function = member_function
        ##VIENE DE LA BD
        self.x = x
        self.xl = xl
        self.y = y
        self.yl = yl
        self.xr = xr
        self.yr = yr
        self.ore = ore        
        
        
        self.cubiculo = cubiculo.Cubiculo("compras", 
                                         [[self.x, self.xl, eval(self.xr)], [self.y, self.yl, eval(self.yr)]], 
                                         [["cantidad", "sum"],['costo_pesos', 'sum']], eval(self.ore))        

    def pivot(self, request):       
        self.cubiculo.pivot()
        return self.cubiculo.absolute_url(request)

    def drill(self,request, axis):
        self.cubiculo.drill(axis)
        return self.cubiculo.absolute_url(request)

    def roll(self, request, axis):
        self.cubiculo.roll(axis)
        return self.cubiculo.absolute_url(request)

    def drill_replacing(self, request, axis, value):
        self.cubiculo.drill_replacing(axis, value)
        return self.cubiculo.absolute_url(request)

    def drill_replacing2(self, request, value0, value1):
        self.cubiculo.drill_replacing(0, value0)
        self.cubiculo.drill_replacing(1, value1)
        return self.cubiculo.absolute_url(request)    
    
    def dice(self, request, main_axis, other_axis):
        self.cubiculo.dice(main_axis, other_axis)
        return self.cubiculo.absolute_url(request)    
       
    def dimension_values(self, axis):
        con_dwh = psycopg2.connect(host="127.0.0.1", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
        cursor_dwh = con_dwh.cursor()        

        sql_dimension_values = self.cubiculo.dimension_values(int(axis))
        cursor_dwh.execute(sql_dimension_values)
        axis_values = cursor_dwh.fetchall()        
        axis_values = [x[0]  for x in axis_values]
        
        return axis_values

    
    def build_cube(self):
        con_dwh = psycopg2.connect(host="127.0.0.1", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
        
        cursor_dwh = con_dwh.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = self.cubiculo.sql()
        cursor_dwh.execute(sql)
        
        table = cursor_dwh.fetchall()
        
        x_axis = self.dimension_values(0)
        y_axis = self.dimension_values(1)
        
        count = 0
        body = {}
        try:
            dicttable = dict(table[count])
        except:
            dicttable = {}
        
        for x in x_axis:
            for y in y_axis:
                #En caso que no haya clave para el elemento se crea
                if not body.get(y, False):
                    body[y] = []
                    
                #El elemento de la cabecera de table podria no coincidir con
                #los indices recorridos porque table esta ordenado pero incompleto
                if x == dicttable.get('columns', False) and y == dicttable.get('rows', False):
                    measuresList = self.cubiculo.getMeasuresList()
                    
                    params = {}
                    for measure in measuresList:
                        params[measure] = dicttable[measure]                        
                    value = self.member_function(**params)
                    body[y].append(str(value))
                    
                    count = count + 1
                    
                    try:
                        dicttable = dict(table[count])
                    except:
                        dicttable = {}
                        
                else:
                    body[y].append('') 


                
        cube = Cube()
        cube.header = x_axis
        cube.body = body
        cube.body_order = y_axis
        return cube    
        
    
    
    