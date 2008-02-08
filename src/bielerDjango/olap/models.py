import psycopg2
import cubiculo
from pprint import pprint

class Cubo:
    pass              
                         
class Informe:
                             
    def __init__(self):
        pass
                    
    def informe(self, ft, dimensions, measures):
        self.cubiculo = cubiculo.Cubiculo(ft, dimensions, measures)
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
        
    def build_cube(self):
        con_dwh = psycopg2.connect(host="127.0.0.1", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
        cursor_dwh = con_dwh.cursor()        
        
        sql = self.cubiculo.sql()
        cursor_dwh.execute(sql)
        table = cursor_dwh.fetchall()
        
        rtn = {}    
        
        for row in table:
            if not rtn.has_key(row[0]):
                rtn[row[0]] = {}
            rtn[row[0]][row[1]] = row[2]            
        
        sql_second_dimension_values = self.cubiculo.second_dimension_values()
        cursor_dwh.execute(sql_second_dimension_values)
        
        codigos = cursor_dwh.fetchall()        
        codigos = [x[0] for x in codigos]
        
        valores = {}
        
        for anio in rtn.values():
            for codigo in codigos:
                if not valores.get(codigo, False):
                    valores[codigo] = []
                valores[codigo].append(anio.get(codigo, 0))            
               
        cubo = Cubo()
        cubo.header = rtn.keys()
        cubo.body = valores
        
        return cubo  
        
