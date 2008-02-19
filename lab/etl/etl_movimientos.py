#!/usr/bin/env python

#from pyPgSQL import PgSQL
import psycopg2 as PgSQL
import MySQLdb
import etlutils

# Create a connection object and create a cursor
con = MySQLdb.Connect(host="192.168.61.3", port=3306, user="b2", passwd="b2", db="b2")
cursor = con.cursor()
cursor2 = con.cursor()

## DWH

con_dwh = PgSQL.connect(host="192.168.61.102", port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
con_dwh.set_client_encoding('windows-1252')

cursor_dwh = con_dwh.cursor()


#info...
['Anio','Mes','Grupo_Constructivo1','Grupo_Constructivo2','Modelo','Modificacion','Pieza','Proovedor','Descripcion','Codigo','Stock','Egreso', 'Ingreso']



for anio in range(1998,2008):
  for mes in range(1,13):
    # Make SQL string and execute it
    sql = """
SELECT 
 substring(A.ART_CODIGO, 7, 2)  as Grupo_Constructivo1,
 substring(A.ART_CODIGO, 9, 1)  as Grupo_Constructivo2,
 substring(A.ART_CODIGO, 4, 3)  as Modelo,
 substring(A.ART_CODIGO, 10, 2) as Modificacion,
 substring(A.ART_CODIGO, 12, 2) as Pieza,
 substring(A.ART_CODIGO, 20, 3) as Proovedor,
 A.ART_DESCRI as Descripcion,
 A.ART_CODIGO as Codigo,
 SUM( IF( M.ART_TIPMOV LIKE 'S%%', - M.ART_CANTID, M.ART_CANTID ) ) + AP.ART_SDOINI AS Stock
 SUM( IF( M.ART_TIPMOV LIKE 'S%%' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 ) ) as Egresos,
 SUM( IF( M.ART_TIPMOV NOT LIKE 'S%%' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 ) ) as Ingresos
FROM
 `STS_ARTIC0` A 
 Join `STS_MOVIM0` M on (A.ART_CODIGO = M.ART_CODIGO)
 Join `STS_APDEP0` AP on (A.ART_CODIGO = AP.ART_CODIGO)
WHERE
  A.`ART_DEFCOD` = 'A'
  and AP.ART_DEPOS = '1'
  and substring(A.ART_CODIGO, 4, 6)='376010'
  and M.ART_FECHA < '%s-%s-01'
GROUP BY 
 A.ART_CODIGO
""" % (anio,mes,anio,mes,anio,mes)
    cursor.execute(sql)

    # Fetch all results from the cursor into a sequence and close the connection
    results = cursor.fetchall()
    for row in results:

    	(grupoConstructivo1, 
         grupoConstructivo2,
         modelo,
         modificacion,
         pieza,
         proovedor,
         descripcion,
         codigo,
         stock,
         egresos,
         ingresos) = row[0:11]

        grupo_constructivo = grupoConstructivo1 + grupoConstructivo2
        
        tiempo_id = etlutils.get_id(cursor_dwh,'td_tiempo','id', {'anio':anio, 'mes':mes})
        

        pieza_id = etlutils.get_id(cursor_dwh,'td_pieza','id',{'grupo_constructivo': grupo_constructivo, 'modelo':modelo,'modificacion': modificacion, 'pieza': pieza, 'descripcion': descripcion, 'codigo': codigo})

        proveedor_id=etlutils.get_id(cursor_dwh,'td_proveedor','id',{'id_octosis':proovedor})

        sql = 'insert into ft_movimientos (fk_tiempo, fk_pieza, fk_proveedor, stock, egresos, ingresos) values (%s, %s, %s, %s, %s, %s)'
        cursor_dwh.execute (sql, (tiempo_id, pieza_id, proveedor_id, stock, egresos, ingresos))
        con_dwh.commit()


con.close()
con_dwh.close()
