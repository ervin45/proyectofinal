import models
from django.shortcuts import render_to_response

def reportes(request):
    informe = models.Informe()
    cubo = informe.informe("movimientos", [["pieza", "modelo"], ["tiempo","anio"]], [["stock", "sum"]]) 
    print "generando informe"
    request.session["informe"] = informe  
    return render_to_response('reportes.html',{'header':cubo.header, 'body':cubo.body})

def pivot(request):
    a = request.session["informe"]
    cubo = a.pivot()
    request.session["informe"] = a
    return render_to_response('reportes.html',{'header':cubo.header, 'body':cubo.body})
    
def roll(request, axis):
    a = request.session["informe"]
    cubo = a.roll(axis)
    request.session["informe"] = a
    return render_to_response('reportes.html',{'header':cubo.header, 'body':cubo.body})

def drill(request, axis):
    a = request.session["informe"]
    cubo = a.drill(axis)
    request.session["informe"] = a
    return render_to_response('reportes.html',{'header':cubo.header, 'body':cubo.body})

