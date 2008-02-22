#!/usr/bin/env python

def isFloat(s):
    try:
        return float(s) or True
    except:
        return False

def compare(a,b):
    primero = a.split(' - ')
    segundo = b.split(' - ')
    for x,y in zip(primero, segundo):
        if isFloat(x) and isFloat(y):                                   
            if float(x) > float(y):
                return 1
            elif float(x) < float(y):
                return -1
        else:
            if x > y:
                return 1
            elif x < y:
                return -1
    print "returning 0"
    return 0

a_ordenar = ['2003 - 3.11', '2006 - 10', '1999 - 12', '1999 - 1', '1999 - 10', '1999 - 2', '2003 - 3.1']

a_ordenar.sort(compare)

print a_ordenar
