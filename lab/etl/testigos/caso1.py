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
import pprint
import re
import MySQLdb

filename = 'A000.180.20.09.txt'
articulo = '000001802009000000000'

n='6111800009000000000'
filename = '%s.txt' % n
articulo = '00%s' % n 

octosis_file = file(filename,'r').readlines()
octosis_file = octosis_file[7:]

con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="", db="b2")
cursor = con.cursor(MySQLdb.cursors.DictCursor)
sql = """SELECT
 CONCAT(ART_TIPMOV,'-',ART_CODSAL) as TIPO,
 ART_CANTID as CANTIDAD,
 ART_FECHA as FECHA,
 ART_PRECIO as PRECIO,
 ART_PREDOL as D,
 ART_PREVT as PREVT
FROM
 `STS_MOVIM0`
WHERE
 ART_CODIGO = ' %s'
order by
 ART_FECHA, ART_HORA
""" % articulo
cursor.execute(sql)
results = cursor.fetchall()


#Just comparing...
nice_tuples = zip(octosis_file, results)

def check(p):
    return check_date(p) and check_precio(p) and check_cnt(p) and check_tipo(p)

def check_date(p):
    o = p[0][3:11].split('/')
    m = p[1]

    #check year
    if str(m['FECHA'].year)[2:4] == o[2]:
        #check month
        if m['FECHA'].month == int(o[1]):
            #check day
            if m['FECHA'].day == int(o[0]):
                return True                
    return False

def check_precio(p):
    o = p[0][42:52]
    m = p[1]
    
    return float(o) == m['PRECIO']

def check_cnt(p):
    o = p[0][50:68]
    m = p[1]

    return float(o) == m['CANTIDAD']


def check_tipo(p):
    o = p[0][12:40]
    m = p[1]['TIPO'].strip()

    ## Salida por Consumo
    ## CUANDO SE REALIZO UNA VENTA POR TALLER QUE LUEGO SE
    ## HACE LA DEVOLUCIoN APARECE ESTA LEYENDA
    
    if (re.match('SAL  1-Salida por Consumo',o) and m == 'S1- 1'):          
        #print p[0], p[1]
        return True

    ## venta por taller
    ## S.Ap.XX ES SUB APERTURA EJEMPLO 00->CLIENTE     02->GARANTIA
    if (re.match('SAL +OR: +[0-9]+ +S\.Ap\.[0-9]+',o) and m == 'S1- 1'):
        return True

    ## venta mostrador
    if (re.match('SAL x Venta \(Pv\. +[0-9\.]+\)',o) and m == 'S3-'):
        return True

    ## compra
    if (o[0:14] == 'ENT  1-Remito:' and m == 'E1- 1'):
        return True

    ## compra (a otros que no sean mercedes benz / preguntarle a Gustavo)
    if (o[0:14] == 'ENT  2-Remito:' and m == 'E1- 2'):
        return True

    if (re.match('SAL 23-SUCURSAL RECONQUISTA',o)    and m == 'S1-23'):
        return True

    if (re.match('SAL 22-SUCURSAL RAFAELA',o)        and m == 'S1-22'):
        return True

    if (re.match('ENT 23-Ent.de RECONQUISTA',o)      and m == 'E1-23'):
        return True

    if (re.match('ENT 22-Ent.de RAFAELA',o)          and m == 'E1-22'):
        return True


    if (re.match('SAL  2-Ajuste Inventario -',o)     and m == 'S1- 2'):
        return True

    if (re.match('ENT  3-Ajuste Inventario \+',o)    and m == 'E1- 3'):
        return True

    # hay 2 "ENT Devoluci\xa2n de Salida" internas?
    if (re.match('ENT Devoluci\xa2n de Salida',o)    and m == 'E3-91'):
       return True
    
    if (re.match('ENT Devoluci\xa2n de Salida',o)    and m == 'E3-92'):
        return True

## encontre un 'S2-91' en los siguientes dias:
##    * 1999-12-21 en el codigo ' 003760107420000000000'
##    * 1999-09-17 en el codigo ' 003760100113000000000'
## Y parece que estaria asociado a un 'E1- 1' ese mismo dia
    #print o.__repr__(), m

errors=0
for p in nice_tuples:
    if check(p):
        #print "OK"
        pass
    else:
        print "-----ERROR-------"
        pprint.pprint(p)
        print "-----------------"
        errors += 1
        pass

print "\nErrors: %d" %errors


