import psycopg2
import cubiculo
              
                         
class Informe:
                             
    def __init__(self):
        pass
                    
    def informe(self, ft, dimensions, measures):
        con_dwh = psycopg2.connect(host="127.0.0.1", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
        cursor_dwh = con_dwh.cursor()
        c = cubiculo.Cubiculo(ft, dimensions, measures)
        sql = c.sql()
        cursor_dwh.execute (sql)
        table = cursor_dwh.fetchall()
        
        rtn = {}
        
        for row in table:
            if not rtn.has_key(row[0]):
                rtn[row[0]] = {}
            rtn[row[0]][row[1]] = row[2]
 
        return rtn                 
                         