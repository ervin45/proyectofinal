#!/usr/bin/env python
## corrige STS_MOVIM0.M_PRECIOVTA y pone en reemplazo el "costo" basandose
## en la ultima venta, caso contrario los deja tal cual.
## si encuentra cotizacion para ese dia se calcula el 


import datetime
import MySQLdb
import time

# Create a connection object and create a cursor
con = MySQLdb.Connect(host="localhost", port=3306, user="root", passwd="", db="b2")
cursor = con.cursor()
cursor2 = con.cursor()
cursor3 = con.cursor()

debug = False
debug_level = 5

def dbg(s, level = 10):
    if debug and (debug_level > level):
        print s

sql = '''SELECT
  M.ART_FECHA as Fecha,
  M.ART_HORA as Hora,
  M.ART_CODIGO as Codigo,
  M.ART_PREDOL as Predol,
  M.ART_PRECIO as Precio
FROM
  `STS_MOVIM0` M
WHERE
  M.`ART_DEFCOD` = 'A'
  and M.ART_TIPMOV = 'S3'

'''
  #and M.ART_TIPMOV = 'S1'
  #and M.ART_CODSAL = ' 1'
  ## Y 'S3'???
  ## select X_PRECIO_PESOS from STS_MOVIM0 where art_codigo = ' 009060380171000000000' and ART_TIPMOV = 'S3';
  ## me esta devolviendo todo NULL!
cursor.execute(sql)

dbg("Cantidad de registros a procesar: %d" % cursor.rowcount, 3)
for row in cursor.fetchall():
    start = time.time()
    (fecha, hora, codigo, predol, precio) = row
    #print "procesing...", row
    dbg("01 - %f" % (time.time() - start ))
    sql_costo = '''SELECT
 M.ART_CODIGO as Codigo,
 M.ART_FECHA as Fecha,
 M.ART_PRECIO as Costo_Pesos,
 IF(M.ART_PREDOL > 0, M.ART_PREDOL, M.ART_PRECIO) as Costo_Dolar
FROM
 `STS_MOVIM0` M
WHERE
  M.`ART_DEFCOD` = 'A'
  and M.ART_CODIGO = '%s'
  and M.ART_FECHA <= '%s'
  and M.ART_TIPMOV = 'E1'
  and (M.ART_CODSAL = ' 1' or M.ART_CODSAL = ' 2')

ORDER BY
  M.ART_FECHA DESC
LIMIT 0,1
''' % (codigo, fecha)
  
    dbg("02 - %f" % (time.time() - start ))
    cursor2.execute(sql_costo)
    dbg("03 - %f" % (time.time() - start ))       
    costos = cursor2.fetchall()  
    dbg("04 - %f" % (time.time() - start ))       
  
    if len(costos) == 1:
        precio_historico_pesos = costos[0][2]
    else:
        precio_historico_pesos = precio

    if predol > 0 :
        precio_historico_dolares = predol
    else:
        sql_cotizacion = "select  C.CAM_VENDED as cotizacion from `PVD4_CAMBI` C where (C.FECHA = '%s')" % fecha
        dbg("04.01 - %f" % (time.time() - start ))       
        cursor3.execute(sql_cotizacion)
        dbg("04.02 - %f" % (time.time() - start ))       
        cotizacion = cursor3.fetchall()
        dbg("04.03 - %f" % (time.time() - start ))       
        if not cotizacion:
            dbg( "warning: no existe cotizacion para fecha %s" % fecha, 2)
            precio_historico_dolares = precio
            dbg( "setting precio_historico_dolares = %s" % precio_historico_dolares,12)
        else:
            precio_historico_dolares = precio / cotizacion[0][0]
            
            dbg( "setting precio_historico_dolares = %s, precio = %s and cotizacion[0][0] = %s" % (precio_historico_dolares,precio, cotizacion[0][0]) ,12)

    print """UPDATE `STS_MOVIM0` set X_PRECIO_PESOS='%s', X_PRECIO_DOLARES='%s' WHERE ART_DEFCOD = 'A' AND ART_CODIGO = '%s' and ART_FECHA = '%s' and ART_HORA = '%s';""" % (precio_historico_pesos, precio_historico_dolares, codigo, fecha, hora)
    dbg("** - %f" % (time.time() - start ), 3)

