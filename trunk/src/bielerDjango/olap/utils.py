def isFloat(s):
    try:
        return float(s) or True
    except:
        return False

def compare(a,b):
    primero = str(a).split('-')
    segundo = str(b).split('-')
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


def sumar(a,b):
    if a == None:
        a = 0
        
    if b == None:
        b = 0
        
    return a + b 