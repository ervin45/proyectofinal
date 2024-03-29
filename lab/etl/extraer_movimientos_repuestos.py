#!/usr/bin/env python
#############################################################################
#
#    Sistema de soporte de decisiones para Ricardo Bieler S.A.
#    Copyright (C) 2007-2008 Nicolas D. Cesar, Mariano N. Galan
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

import MySQLdb
import csv

# Create a connection object and create a cursor
con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="", db="b2")
cursor = con.cursor()
cursor2 = con.cursor()

writer = csv.writer(open("stock.csv", "wb"),delimiter = ';', quoting = csv.QUOTE_ALL)
writer.writerows((['Anio','Mes','Grupo_Constructivo1','Grupo_Constructivo2','Modelo','Modificacion','Pieza','Proovedor','Descripcion','Codigo','Stock','Costo_pesos','Precio_Vta', 'Compras', 'Devoluciones', 'Ventas', 'VentaPorTaller'],))

def get_costo_precio_etc(row,cursor):
  anio=row[0]
  mes=row[1]
  codigo=row[9]


  ###
  ### E1-1 | Compra | "1-Remito"
  ###
  sql=""" 
SELECT
 M.ART_PRECIO * M.ART_CANTID as Costo_Pesos
FROM
 `STS_ARTIC0` A
  Join `STS_MOVIM0` M on (A.ART_CODIGO = M.ART_CODIGO)
WHERE
  A.`ART_DEFCOD`   = 'A'
  and A.ART_CODIGO ='%s'
  and M.ART_FECHA < '%s-%s-01'
  and M.ART_TIPMOV = 'E1'
  and M.ART_CODSAL = '1'
  and (M.ART_PRECIO + M.ART_PREDOL) > 0
ORDER BY
  M.ART_FECHA DESC LIMIT 1
""" % (codigo,anio,mes)
  cursor2.execute(sql)
  costos = cursor2.fetchone()  

  if not costos:
    sql=""" 
SELECT
 M.ART_PRECIO as Costo_Pesos
FROM
 `STS_ARTIC0` A
  Join `STS_MOVIM0` M on (A.ART_CODIGO = M.ART_CODIGO)
WHERE
  A.`ART_DEFCOD`   = 'A'
  and A.ART_CODIGO ='%s'
  and M.ART_FECHA < '%s-%s-01'
  and (M.ART_PRECIO + M.ART_PREDOL) > 0
ORDER BY
  M.ART_FECHA DESC LIMIT 1
""" % (codigo,anio,mes)
    cursor2.execute(sql)
    costos = cursor2.fetchone()  

  sql="""
SELECT
 M.ART_PREVT as Precio_Vta
FROM
 `STS_ARTIC0` A
  Join `STS_MOVIM0` M on (A.ART_CODIGO = M.ART_CODIGO)
WHERE
  A.`ART_DEFCOD`   = 'A'
  and A.ART_CODIGO ='%s'
  and M.ART_FECHA < '%s-%s-01'
  and

  (M.ART_TIPMOV = 'S3' or
   (M.ART_TIPMOV = 'S3' and  and M.ART_CODSAL = '1')
  )
  and (M.ART_PRECIO + M.ART_PREDOL) > 0
ORDER BY
  M.ART_FECHA DESC LIMIT 1
""" % (codigo,anio,mes)
  cursor2.execute(sql)
  venta = cursor2.fetchone()

  #pudo Solo haber existido ingreso
  if not venta:
    sql="""
SELECT
 M.ART_PREVT as Precio_Vta
FROM
 `STS_ARTIC0` A
  Join `STS_MOVIM0` M on (A.ART_CODIGO = M.ART_CODIGO)
WHERE
  A.`ART_DEFCOD`   = 'A'
  and A.ART_CODIGO ='%s'
  and M.ART_FECHA < '%s-%s-01'
  and (M.ART_PRECIO + M.ART_PREDOL) > 0
ORDER BY
  M.ART_FECHA DESC LIMIT 1
""" % (codigo,anio,mes)
    cursor2.execute(sql)
    venta = cursor2.fetchone()
 
  sql="""
SELECT
 SUM(M.ART_CANTID) as Compras
FROM
 `STS_ARTIC0` A
  Join `STS_MOVIM0` M on (A.ART_CODIGO = M.ART_CODIGO)
WHERE
  A.`ART_DEFCOD`   = 'A'
  and A.ART_CODIGO ='%s'
  and YEAR(M.ART_FECHA) = '%s'
  AND MONTH(M.ART_FECHA) = '%s'
  and M.ART_TIPMOV = 'E1'
ORDER BY
  M.ART_FECHA DESC LIMIT 1
""" % (codigo,anio,mes)
  cursor2.execute(sql)
  cantidad_compras = cursor2.fetchone()
  if cantidad_compras == (None,):
    cantidad_compras = (0.0, )

  sql="""
SELECT
 SUM(M.ART_CANTID) as Ventas
FROM
 `STS_ARTIC0` A
  Join `STS_MOVIM0` M on (A.ART_CODIGO = M.ART_CODIGO)
WHERE
  A.`ART_DEFCOD`   = 'A'
  and A.ART_CODIGO ='%s'
  and YEAR(M.ART_FECHA) = '%s'
  AND MONTH(M.ART_FECHA) = '%s'
  and M.ART_TIPMOV = 'S3'
ORDER BY
  M.ART_FECHA DESC LIMIT 1
""" % (codigo,anio,mes)
  cursor2.execute(sql)
  cantidad_ventas = cursor2.fetchone()
  if cantidad_ventas == (None,):
    cantidad_ventas = (0.0, )

  sql="""
SELECT
 SUM(M.ART_CANTID) as OtroEgreso 
FROM
 `STS_ARTIC0` A
  Join `STS_MOVIM0` M on (A.ART_CODIGO = M.ART_CODIGO)
WHERE
  A.`ART_DEFCOD`   = 'A'
  and A.ART_CODIGO ='%s'
  and YEAR(M.ART_FECHA) = '%s'
  AND MONTH(M.ART_FECHA) = '%s'
  and M.ART_TIPMOV = 'S1'
ORDER BY
  M.ART_FECHA DESC LIMIT 1
""" % (codigo,anio,mes)
  cursor2.execute(sql)
  cantidad_otroegreso = cursor2.fetchone()
  if cantidad_otroegreso == (None,):
    cantidad_otroegreso = (0.0, )

  sql="""
SELECT
 SUM(M.ART_CANTID) as Devoluciones
FROM
 `STS_ARTIC0` A
  Join `STS_MOVIM0` M on (A.ART_CODIGO = M.ART_CODIGO)
WHERE
  A.`ART_DEFCOD`   = 'A'
  and A.ART_CODIGO ='%s'
  and YEAR(M.ART_FECHA) = '%s'
  AND MONTH(M.ART_FECHA) = '%s'
  and M.ART_TIPMOV = 'E3'
ORDER BY
  M.ART_FECHA DESC LIMIT 1
""" % (codigo,anio,mes)
  cursor2.execute(sql)
  cantidad_devoluciones = cursor2.fetchone()
  if cantidad_devoluciones == (None,):
    cantidad_devoluciones = (0.0, )

  rtn=[]
  try:
    rtn.extend(costos)
    rtn.extend(venta)
    rtn.extend(cantidad_compras)
    rtn.extend(cantidad_devoluciones)
    rtn.extend(cantidad_ventas)
    rtn.extend(cantidad_otroegreso)
  except:
    print codigo
    print costos
    raise

  print rtn
  return rtn

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
""" % (anio,mes)
    cursor.execute(sql)

    # Fetch all results from the cursor into a sequence and close the connection
    results = cursor.fetchall()
    for row in results:
	someiterable = [anio, mes]
   	someiterable.extend(row)
   	someiterable.extend(get_costo_precio_etc(someiterable,cursor2))

    	writer.writerows((someiterable,))
con.close()
