#!/usr/bin/env python

import math

def get_posible_maxs(digitos):
    posible = [(x+1)*(10**(digitos-1)) for x in range(10)]
    return posible


def get_tope(max_y):
    big_max_y = max_y * 1.05
    digitos = math.ceil(math.log10(big_max_y))
    pos = get_posible_maxs(digitos)

    tope = [x for x in pos if x > big_max_y][0]
    return tope

pruebas = (0.22, 3.20, 5, 10.20, 12, 17.22, 19.9999, 378, 23787, 12918277218)

for p in pruebas:
    print "max_y:", p ,"tope:", get_tope(p)
