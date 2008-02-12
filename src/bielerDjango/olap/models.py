import psycopg2
import psycopg2.extras
import copy

import cubiculo
from pprint import pprint

class Cube:
    pass              
    
class Report:
    pass

    def get_cube(self):
        self.cubiculo = cubiculo.Cubiculo("compras", 
                                 [[self.x, self.xl, eval(self.xr)], [self.y, self.yl, eval(self.yr)]], 
                                 [["cantidad", "sum"],['costo_pesos', 'sum']])
                                
        return self.build_cube()

    def pivot(self):       
        self.cubiculo.pivot()
        return self.cubiculo.absolute_url()
        #return "http://localhost:8000/reporte2/compras/tiempo/pieza/mes/grupo_constructivo/rx={'anio':[2002]}/ry={}/ro={}/"

    def drill(self, axis):
        self.cubiculo.drill(axis)
        return self.cubiculo.absolute_url()

    def roll(self, axis):
        self.cubiculo.roll(axis)
        return self.cubiculo.absolute_url()

    def drill_replacing(self, axis, value):
        self.cubiculo.drill_replacing(axis, value)
        return self.cubiculo.absolute_url()

    def drill_replacing2(self, value0, value1):
        self.cubiculo.drill_replacing(0, value0)
        self.cubiculo.drill_replacing(1, value1)
        return self.cubiculo.absolute_url()    
       
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
        
        first_axis = self.dimension_values(0)
        second_axis = self.dimension_values(1)
        
        count = 0
        body = {}
        try:
            dicttable = dict(table[count])
        except:
            dicttable = {}
        
        for h in first_axis:
            
            for s in second_axis:
                #En caso que no haya clave para el elemento se crea
                if not body.get(s, False):
                    body[s] = []  
                #El elemento de la cabecera de table podria no coincidir con
                #los indices recorridos porque table esta ordenado pero incompleto
                if h == dicttable.get('columns', False) and s == dicttable.get('rows', False):
                    measuresList = self.cubiculo.getMeasuresList()
                    
                    params = {}
                    for measure in measuresList:
                        params[measure] = dicttable[measure]                        
                    value = self.member_function(**params)
                    
                    body[s].append(value)
                    count = count + 1
                    
                    try:
                        dicttable = dict(table[count])
                    except:
                        dicttable = {}
                        
                else:
                    body[s].append(-1) 


                
        cube = Cube()
         
        cube.header = first_axis
        cube.body = body
        cube.body_order = second_axis
        print cube.body_order
        return cube    
        
    
    
    