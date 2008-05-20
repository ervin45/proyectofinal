from decimal import Decimal

def dividir(arg0, arg1):

    if not arg0:
        arg0 = Decimal("0.0")

    if not arg1:
        return 0

    return float(arg0) / float(arg1)

def multiplicar(arg0, arg1):

    if not arg0:
        arg0 = Decimal("0.0")

    if not arg1:
        return 0

    return arg0 * arg1

def sumar(arg0, arg1):
    if not arg0:
        arg0 = 0

    if not arg1:
        arg1 = 0

    return arg0 + arg1

def restar(arg0, arg1):
    if not arg0:
        arg0 = 0

    if not arg1:
        arg1 = 0

    return arg0 - arg1

def mismo_valor(arg):
    return arg
