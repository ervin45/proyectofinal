#!/usr/bin/env python

import psycopg2 as PgSQL
import MySQLdb
import etlutils

# Create a connection object and create a cursor
con = MySQLdb.Connect(host="localhost", port=3306, user="root", passwd="", db="b2")
cursor = con.cursor()
#cursor2 = con.cursor()

## DWH
con_dwh = PgSQL.connect(host="192.168.61.100", port=5432, user="ncesar", password="noteladigo", database="bieler_dw")
con_dwh.set_client_encoding('windows-1252')
cursor_dwh = con_dwh.cursor()


#info...
['Anio','Mes','Grupo_Constructivo1','Grupo_Constructivo2','Modelo','Modificacion','Pieza','Proovedor','Descripcion','Codigo','Cantidad','Costo_pesos']


for anio in range(1998,2008):
  for mes in range(1,13):
    print "procesando: ", anio, mes
    # Make SQL string and execute it
  ###
  ### E1-1 | Compra | "1-Remito"
  ### E1-2 | Compra (aparentemente a proveedores distintos de MBenz) | 2-Remito
  ###
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
 SUM(M.ART_CANTID) as Cantidad,
 SUM(M.ART_PRECIO * M.ART_CANTID) as Costo_Pesos,
 SUM(IF(M.ART_PREDOL > 0, M.ART_PREDOL, M.ART_PRECIO) * M.ART_CANTID) as Costo_Dolar
FROM
 `STS_ARTIC0` A 
 Join `STS_MOVIM0` M on (A.ART_CODIGO = M.ART_CODIGO)
WHERE
  A.`ART_DEFCOD` = 'A'
  and YEAR(M.ART_FECHA) =  '%s'
  and MONTH(M.ART_FECHA) = '%s'
  and M.ART_TIPMOV = 'E1'
  and (M.ART_CODSAL = ' 1' or M.ART_CODSAL = ' 2')

GROUP BY 
 A.ART_CODIGO
""" % (anio,mes)
    #print sql
    cursor.execute(sql)

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
         cantidad,
         costo_pesos,
         costo_dolar) = row[0:11]

        print anio, mes, codigo

        grupo_constructivo = grupoConstructivo1 + grupoConstructivo2

        tiempo_id = etlutils.get_id(cursor_dwh,'td_tiempo','id', {'anio':anio, 'mes':mes})


        pieza_id = etlutils.get_id(cursor_dwh,'td_pieza','id',{'grupo_constructivo': grupo_constructivo, 'modelo':modelo,'modificacion': modificacion, 'pieza': pieza, 'descripcion': descripcion, 'codigo': codigo})

        proveedor_id=etlutils.get_id(cursor_dwh,'td_proveedor','id',{'id_octosis':proovedor})

        sql = 'insert into ft_compras (fk_tiempo, fk_pieza, fk_proveedor, cantidad, costo_pesos, costo_dolar) values (%s, %s, %s, %s, %s, %s)'
        cursor_dwh.execute (sql, (tiempo_id, pieza_id, proveedor_id, cantidad, costo_pesos, costo_dolar))
        con_dwh.commit()


con.close()
con_dwh.close()
