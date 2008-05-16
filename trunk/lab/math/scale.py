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

import math

def get_posible_maxs(digitos):
    posible = [(x+1)*(10**(digitos-1)) for x in range(10)]
    return posible


def get_tope(max_y):
    big_max_y = max_y * 1.05
    if max_y <= 1:
        digitos = 1
    else:
        digitos = math.ceil(math.log10(big_max_y))
    pos = get_posible_maxs(digitos)

    tope = [x for x in pos if x > big_max_y][0]
    return tope

pruebas = (-1, 0, 0.22, 3.20, 5, 10.20, 12, 17.22, 19.9999, 378, 23787, 12918277218)

for p in pruebas:
    print "max_y:", p ,"tope:", get_tope(p)
