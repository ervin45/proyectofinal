import psycopg2
import psycopg2.extras
import copy

import cubiculo
from pprint import pprint

class Cube:
    pass              
                         
class Informe:
    """
    Un informe realiza la conexion a la base de datos y
    genera un cubiculo para manipular

    # creando
    >>> i = Informe()
    # pasando parametros
    >>> cubo = i.informe("movimientos", [["pieza", "codigo"], ["tiempo","anio"]], [["stock", "sum"]]) 

    """
    def __init__(self):
        pass
                    
    def informe(self, ft, dimensions, measures, member_function):
        self.cubiculo = cubiculo.Cubiculo(ft, dimensions, measures)
        self.member_function = member_function
        return self.build_cube() 
    
    def pivot(self):       
        self.cubiculo.pivot()
        return self.build_cube() 
    
    def drill(self, axis):
        self.cubiculo.drill(axis)
        return self.build_cube()
    
    def roll(self, axis):
        self.cubiculo.roll(axis)
        return self.build_cube()
    
    def drill_replacing(self, axis, value):
        self.cubiculo.drill_replacing(axis, value)
        return self.build_cube()
    
    def drill_replacing2(self, value0, value1):
        self.cubiculo.drill_replacing2(value0, value1)
        return self.build_cube()    
       
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
        dicttable = dict(table[count])
        
        for h in first_axis:
            
            for s in second_axis:
                try:
                    #En caso que no haya clave para el elemento se crea
                    if not body.get(s, False):
                        body[s] = []  
                    #El elemento de la cabecera de table podria no coincidir con
                    #los indices recorridos porque table esta ordenado pero incompleto
                    if h == dicttable['columns'] and s == dicttable['rows']:
                        
                        measuresList = self.cubiculo.getMeasuresList()
                        
                        params = {}
                        for measure in measuresList:
                            params[measure] = dicttable[measure]                        
                        
                        value = self.member_function(**params)
                        
                        
                        body[s].append(value)
                        count = count + 1
                        dicttable = dict(table[count])
                    else:
                        body[s].append(-1) 
                except Exception, e:
                    print  e
                
        cube = Cube()
         
        cube.header = first_axis
        cube.body = body
        cube.body_order = second_axis
        
        return cube