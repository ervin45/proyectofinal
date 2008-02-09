import models
from django.shortcuts import render_to_response

def reportes(request):
    informe = models.Informe()
    #cubo = informe.informe("movimientos", [["pieza", "modelo"], ["tiempo","anio"]], [["stock", "avg"]]) 
    cubo = informe.informe("compras", [["pieza", "grupo_constructivo"], ["tiempo","anio"]], [["cantidad", "sum"],['costo_pesos', 'sum'], ['costo_dolar', 'sum']]) 
    print "generando informe"
    request.session["informe"] = informe  
    return render_to_response('reportes.html',{'cubo':cubo})

def pivot(request):
    a = request.session["informe"]
    cubo = a.pivot()
    request.session["informe"] = a
    return render_to_response('reportes.html',{'cubo':cubo})
    
def roll(request, axis):
    a = request.session["informe"]
    cubo = a.roll(axis)
    request.session["informe"] = a
    return render_to_response('reportes.html',{'cubo':cubo})

def drill(request, axis):
    a = request.session["informe"]
    cubo = a.drill(axis)
    request.session["informe"] = a
    return render_to_response('reportes.html',{'cubo':cubo})

def drill_replacing(request, axis, value):
    a = request.session["informe"]
    cubo = a.drill_replacing(axis, value)
    request.session["informe"] = a
    return render_to_response('reportes.html',{'cubo':cubo})    

def drill_replacing2(request, value0, value1):
    a = request.session["informe"]
    cubo = a.drill_replacing2(value0, value1)
    request.session["informe"] = a
    return render_to_response('reportes.html',{'cubo':cubo})    
