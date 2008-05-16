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

#from pyPgSQL import PgSQL
import psycopg2 as PgSQL
import MySQLdb
import etlutils

# Create a connection object and create a cursor
con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", db="b2")
cursor = con.cursor()
cursor2 = con.cursor()

## DWH
con_dwh = PgSQL.connect(host="192.168.61.100", port=5432, user="ncesar", password="a-notela", database="bieler_dw")
con_dwh.set_client_encoding('windows-1252')
cursor_dwh = con_dwh.cursor()


#info...
['Anio','Mes','Grupo_Constructivo1','Grupo_Constructivo2','Modelo','Modificacion','Pieza','Proovedor','Descripcion','Codigo','Stock','Egreso', 'Ingreso']



for anio in range(1998,2008):
  for mes in range(1,13):
    print "procesando ", anio, mes
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
 SUM( IF( M.ART_TIPMOV LIKE 'S%%', - M.ART_CANTID, M.ART_CANTID ) ) + AP.ART_SDOINI AS Stock,
 SUM( IF( M.ART_TIPMOV LIKE 'S%%' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 ) ) as Egresos,
 SUM( IF( M.ART_TIPMOV NOT LIKE 'S%%' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 ) ) as Ingresos,
 SUM( IF( CONCAT(M.ART_TIPMOV,'-',M.ART_CODSAL) = 'S1- 1' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 ) ) as ventas_por_taller,
 SUM( IF( CONCAT(M.ART_TIPMOV,'-',M.ART_CODSAL) = 'S3-' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 ) ) as ventas_por_mostrador,
 SUM( IF( CONCAT(M.ART_TIPMOV,'-',M.ART_CODSAL) = 'E1- 1' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 ) ) as compras1,
 SUM( IF( CONCAT(M.ART_TIPMOV,'-',M.ART_CODSAL) = 'E1- 2' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 ) ) as compras2,
 SUM( IF( CONCAT(M.ART_TIPMOV,'-',M.ART_CODSAL) = 'S1-22' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 ) ) as envios_a_rafaela,
 SUM( IF( CONCAT(M.ART_TIPMOV,'-',M.ART_CODSAL) = 'S1-23' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 ) ) as envios_a_reconquista,
 SUM( IF( CONCAT(M.ART_TIPMOV,'-',M.ART_CODSAL) = 'E1-22' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 ) ) as entrada_de_rafaela,
 SUM( IF( CONCAT(M.ART_TIPMOV,'-',M.ART_CODSAL) = 'E1-23' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 ) ) as entrada_de_reconquista,
 SUM( IF( CONCAT(M.ART_TIPMOV,'-',M.ART_CODSAL) = 'S1- 2' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 ) ) as ajuste_negativo,
 SUM( IF( CONCAT(M.ART_TIPMOV,'-',M.ART_CODSAL) = 'E1- 3' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 ) ) as ajuste_positivo,
 SUM( IF( CONCAT(M.ART_TIPMOV,'-',M.ART_CODSAL) = 'E3-91' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 )) as devolucion_salida1,
 SUM( IF( CONCAT(M.ART_TIPMOV,'-',M.ART_CODSAL) = 'E3-92' AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 )) as devolucion_salida2,
 SUM( IF( CONCAT(M.ART_TIPMOV,'-',M.ART_CODSAL) not in ('S1- 1','S3-','E1- 1','E1- 2','S1-22','S1-23','E1-22','E1-23','S1- 2','E1- 3','E3-91','E3-92') AND YEAR(M.ART_FECHA) = '%s' AND MONTH(M.ART_FECHA) = '%s', M.ART_CANTID, 0 ) ) as otro

FROM
 `STS_ARTIC0` A 
 Join `STS_MOVIM0` M on (A.ART_CODIGO = M.ART_CODIGO)
 Join `STS_APDEP0` AP on (A.ART_CODIGO = AP.ART_CODIGO)
WHERE
  A.`ART_DEFCOD` = 'A'
  and AP.ART_DEPOS = '1'
  and M.ART_FECHA < concat(period_add('%04d%02d',1), '01')
GROUP BY 
 A.ART_CODIGO
""" % ((anio,mes)*16)

## en caso de necesitar hacer pruebas chiquitas
#   and substring(A.ART_CODIGO, 4, 6)='376010'

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
         ingresos,
         ventas_por_taller,
         ventas_por_mostrador,
         compras1,
         compras2,
         envios_a_rafaela,
         envios_a_reconquista,
         entrada_de_rafaela,
         entrada_de_reconquista,
         ajuste_negativo,
         ajuste_positivo,
         devolucion_salida1,
         devolucion_salida2,
         otro) = row
        

        grupo_constructivo = grupoConstructivo1 + grupoConstructivo2
        
        tiempo_id = etlutils.get_id(cursor_dwh,'td_tiempo','id', {'anio':anio, 'mes':mes})
        

        pieza_id = etlutils.get_id(cursor_dwh,'td_pieza','id',{'grupo_constructivo': grupo_constructivo, 'modelo':modelo,'modificacion': modificacion, 'pieza': pieza, 'descripcion': descripcion, 'codigo': codigo})

        proveedor_id=etlutils.get_id(cursor_dwh,'td_proveedor','id',{'id_octosis':proovedor})

        sql = '''insert into ft_movimientos (fk_tiempo, fk_pieza,
         fk_proveedor, stock, egresos, ingresos, ventas_por_taller,
         ventas_por_mostrador, compras1, compras2, envios_a_rafaela,
         envios_a_reconquista, entrada_de_rafaela,
         entrada_de_reconquista, ajuste_negativo, ajuste_positivo,
         devolucion_salida1, devolucion_salida2, otro) values (%s, %s, %s,
         %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        cursor_dwh.execute (sql, (tiempo_id, pieza_id, proveedor_id,
         stock, egresos, ingresos, ventas_por_taller,
         ventas_por_mostrador, compras1, compras2, envios_a_rafaela,
         envios_a_reconquista, entrada_de_rafaela,
         entrada_de_reconquista, ajuste_negativo, ajuste_positivo,
         devolucion_salida1, devolucion_salida2, otro))
        
        con_dwh.commit()


con.close()
con_dwh.close()
