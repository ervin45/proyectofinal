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
