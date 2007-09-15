#!/usr/bin/env python
import pprint
import re

octosis_file = file('A000.180.20.09.txt','r').readlines()
mysql_file = file('A000.180.20.09-mysql.txt','r').readlines()
#octosis_file = file('A000.180.16.09.txt','r').readlines()
#mysql_file = file('A000.180.16.09-mysql.txt','r').readlines()


octosis_file = octosis_file[6:]
mysql_file = mysql_file[5:]

nice_tuples = zip(octosis_file, mysql_file)

def check(p):
    return check_date(p) and check_precio(p) and check_cnt(p) and check_tipo(p)

def check_date(p):
    o = p[0][3:11].split('/')
    m = p[1].split('|')[3].split('-')

    #print m[0][3:5],   o[2]

    #check year
    if m[0][3:5] == o[2]:
        #check month
        if int(m[1]) == int(o[1]):
            #check day
            if int(m[2]) == int(o[0]):
                return True                
    return False

def check_precio(p):
    o = p[0][42:52]
    m = p[1].split('|')[4]
    
    return float(o) == float(m)

def check_cnt(p):
    o = p[0][50:68]
    m = p[1].split('|')[2]

    return float(o) == float(m)


def check_tipo(p):
    o = p[0][12:40]
    m = p[1].split('|')[1].strip()

    if (o[0:14] == 'ENT  1-Remito:' and m == 'E1- 1'):
        return True

    if (re.match('SAL +OR: +[0-9]+ +S\.Ap\.[0-9]+',o) and m == 'S1- 1'):
        return True

    if (re.match('SAL x Venta \(Pv\. +[0-9\.]+\)',o) and m == 'S3-'):
        return True

    if (re.match('SAL 23-SUCURSAL RECONQUISTA',o) and m == 'S1-23'):
        return True

    if (re.match('SAL 22-SUCURSAL RAFAELA',o) and m == 'S1-22'):
        return True

    if (re.match('ENT 23-Ent.de RECONQUISTA',o) and m == 'E1-23'):
        return True

    if (re.match('ENT 22-Ent.de RAFAELA',o) and m == 'E1-22'):
        return True

    if (re.match('SAL  1-Salida por Consumo',o) and m == 'S1- 1'):          
        return True

    if (re.match('SAL  2-Ajuste Inventario -',o) and m == 'S1- 2'):
        return True

    if (re.match('ENT  3-Ajuste Inventario \+',o) and m == 'E1- 3'):
        return True

    #if (re.match('ENT Devoluci\xa2n de Salida',o) and m == 'E3-91'):
    #   return True
    
    if (re.match('ENT Devoluci\xa2n de Salida',o) and m == 'E3-92'):
        return True
    
    print o.__repr__(), m

for p in nice_tuples:
    if check(p):
        pass
    else:
        #print "ERROR"
        pass


