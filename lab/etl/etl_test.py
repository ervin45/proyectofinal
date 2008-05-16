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

import random
import etlutils
import psycopg2 as PgSQL


## DWH
con_dwh = PgSQL.connect(host="192.168.61.100", port=5432, user="ncesar", password="noteladigo", database="bieler_dw")
con_dwh.set_client_encoding('windows-1252')
cursor_dwh = con_dwh.cursor()

anios       = range(1999,2008)
meses       = range(1,13)
tipo_piezas = ['Original', 'Alternativo']
"""select CONCAT('[\'',
 substring(ART_CODIGO, 7, 3) , '\',\'',
 substring(ART_CODIGO, 4, 3) , '\',\'',
 substring(ART_CODIGO, 10, 2) , '\',\'',
 substring(ART_CODIGO, 12, 2) , '\',\'',
 ART_DESCRI, '\',\'',
 ART_CODIGO, '\']') as rest
from
 STS_ARTIC0
where substring(ART_CODIGO,  7, 3) = '184' """
piezas = [
    ['184','003','33','01','FILTRO DE ACEITE MB1620-UNID.SELLADA',' 000031843301000000000'],
    ['184','102','01','01','FILTRO DE ACEITE',' 001021840101000000555'],
    ['184','314','03','08','CABEZAL FILTRO DE ACEITE-MOTOR IND.',' 003141840308000000000'],
    ['184','000','67','25','FILTRO DE ACEITE',' 000001846725000000555'],
    ['184','000','84','25','FILTRO DE ACEITE',' 000001848425000000000'],
    ['184','001','58','25','FILTRO RADIADOR DE ACEITE MB1620',' 000011845825000000000'],
    ['184','345','00','25','FILTRO DE ACEITE MB1521/1526',' 003451840025000000000'],
    ['184','366','01','25','FILTRO DE ACEITE MB1215/1620M/V-CARTUCHO',' 003661840125000000000'],
    ['184','366','02','25','FILTRO DE ACEITE MB710/913',' 003661840225000000000'],
    ['184','352','03','29','CAJA VALV. PRES.',' 003521840329000000000'],
    ['184','355','00','32','VALVULA DE FILTRO',' 003551840032000000000'],
    ['184','601','01','32','VALVULA',' 006011840132000000000'],
    ['184','322','00','56','TAPON FILTRO ACEITE',' 003221840056000000000'],
    ['184','000','14','71','TORNILLO FILTRO ACEITE',' 000001841471000000000'],
    ['184','352','01','71','TORNILLO FILTRO A',' 003521840171000000000'],
    ['184','312','10','79','JUNTA CABEZAL ACEITE',' 003121841079000000555'],
    ['184','314','03','79','JUNTA FILTRO ACEITE',' 003141840379000000000'],
    ['184','000','63','80','JUNTA FILTRO ACEITE',' 000001846380000000000'],
    ['184','000','65','80','JUNTA FILTRO ACEITE',' 000001846580000000000'],
    ['184','000','93','80','JUNTA FILTRO RAD.ACEITE',' 000001849380000000000'],
    ['184','000','97','80','T1 JUNTA BASE FILTRO DE ACEITE',' 000001849780000000000'],
    ['184','327','02','80','JUNTA FILTRO ACEITE',' 003271840280000000555'],
    ['184','355','04','80','JUNTA FILTRO DE ACEITE',' 003551840480000000000'],
    ['184','364','02','80','JUNTA FILTRO ACEITE',' 003641840280000000000'],
    ['184','616','12','80','MB JUNTA FILTRO DE A',' 006161841280000000000'],
    ['184','001','39','25','FILTRO DE ACEITE MB1114/1518',' 000011843925000000001'],
    ['184','003','33','01','FILTRO DE ACEITE MB1620-UNID.SELLADA',' 000031843301000000001'],
    ['184','352','09','08','CABEZA DE FILTRO',' 003521840908000000000'],
    ['184','001','35','25','FILTRO DE ACEITE',' 000011843525000000000'],
    ['184','102','01','01','FILTRO DE ACEITE',' 001021840101000067000'],
    ['184','616','15','80','MB JUNTA TAPA DE FIL',' 006161841580000000000'],
    ['184','616','16','80','MB JUNTA TAPA DE FIL',' 006161841680000000000'],
    ['184','352','03','29','VALVULA SOBREPRESION DE ACEITE MB1620',' 003521840329100000002'],
    ['184','343','00','25','FILTRO DE ACEITE MB608',' 003431840025000000000'],
    ['184','003','33','01','FILTRO DE ACEITE MB1620-UNID.SELLADA',' 000031843301000000099'],
    ['184','343','00','25','FILTRO DE ACEITE MB608',' 003431840025000000001'],
    ['184','457','00','08','CUERPO/TAPA DE FILTRO',' 004571840008000000000'],
    ['184','601','05','80','JUNTA',' 006011840580000000000'],
    ['184','343','72','25','FILTRO DE ACEITE MB608',' 003431847225000000000'],
    ['184','364','03','80','JUNTA RADIADOR DE ACEITE MB1526',' 003641840380000000000'],
    ['184','001','39','25','FILTRO DE ACEITE MB1114/1518',' 000011843925000000000'],
    ['184','102','01','01','FILTRO DE ACEITE',' 001021840101000000000'],
    ['184','003','33','01','FILTRO DE ACEITE MB1620-UNID.SELLADA',' 000031843301000000045'],
    ['184','001','39','25','FILTRO DE ACEITE MB1114/1518',' 000011843925000000077'],
    ['184','403','01','32','VALVULA DE REFRIG.DE ACEITE MB1938',' 004031840132000000000'],
    ['184','102','05','01','FILTRO DE ACEITE',' 001021840501000000000'],
    ['184','601','05','80','JUNTA',' 006011840580000000081'],
    ['184','611','02','80','VM JUNTA',' 006111840280000000000'],
    ['184','166','02','80','AM JUNTA',' 001661840280000000000'],
    ['184','112','02','61','MM JUNTA ANULAR',' 001121840261000000000'],
    ['184','112','03','61','MM JUNTA ANULAR',' 001121840361000000000'],
    ['184','112','00','61','MM JUNTA ANULAR',' 001121840061000000000'],
    ['184','112','02','80','S JUNTA',' 001121840280000000000'],
    ['184','345','00','25','FILTRO DE ACEITE MB1521/1526',' 003451840025000000001'],
    ['184','266','03','80','CLB JUNTA RADIADOR DE ACEITE',' 002661840380000000000']
]





for anio in anios:
    for mes in meses:
        for tipo in tipo_piezas:
            for pieza in piezas:
                print anio, mes, tipo, pieza[5]
                cantidad = random.randint(1,15)
                costo = "%.2f" % (random.random() * 100)
        
                tiempo_id = etlutils.get_id(cursor_dwh,'td_tiempo','id', {'anio':anio, 'mes':mes})

                pieza_id = etlutils.get_id(cursor_dwh,'td_pieza','id',{'grupo_constructivo': pieza[0], 'modelo':pieza[1],'modificacion': pieza[2], 'pieza': pieza[3], 'descripcion': pieza[4], 'codigo': pieza[5]})

                tipo_pieza_id=etlutils.get_id(cursor_dwh,'td_tipo_pieza','id',{'tipo_pieza':tipo})

                sql = 'insert into ft_test (fk_tiempo, fk_pieza, fk_tipo_pieza, cantidad, costo) values (%s, %s, %s, %s, %s)'
                #print sql, (tiempo_id, pieza_id, tipo_pieza_id, cantidad, costo)
                cursor_dwh.execute (sql, (tiempo_id, pieza_id, tipo_pieza_id, cantidad, costo))
                con_dwh.commit()
con_dwh.close()
