import models
from django.shortcuts import render_to_response

def costo_promedio(costo_pesos, cantidad):
    return float(costo_pesos) / float(cantidad)

def reportes(request):
    informe = models.Informe()
    #cube = informe.informe("movimientos", [["pieza", "modelo"], ["tiempo","anio"]], [["stock", "avg"]]) 
    cube = informe.informe("compras", 
                         [["pieza", "grupo_constructivo"], ["tiempo","anio"]], 
                         [["cantidad", "sum"],['costo_pesos', 'sum']], 
                           costo_promedio) 
    request.session["informe"] = informe  
    return render_to_response('reportes.html',{'cube':cube})

def pivot(request):
    a = request.session["informe"]
    cube = a.pivot()
    request.session["informe"] = a
    return render_to_response('reportes.html',{'cube':cube})
    
def roll(request, axis):
    a = request.session["informe"]
    cube = a.roll(axis)
    request.session["informe"] = a
    return render_to_response('reportes.html',{'cube':cube})

def drill(request, axis):
    a = request.session["informe"]
    cube = a.drill(axis)
    request.session["informe"] = a
    return render_to_response('reportes.html',{'cube':cube})

def drill_replacing(request, axis, value):
    a = request.session["informe"]
    cube = a.drill_replacing(axis, value)
    request.session["informe"] = a
    return render_to_response('reportes.html',{'cube':cube})    

def drill_replacing2(request, value0, value1):
    a = request.session["informe"]
    cube = a.drill_replacing2(value0, value1)
    request.session["informe"] = a
    return render_to_response('reportes.html',{'cube':cube})    
