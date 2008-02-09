import models
from django.shortcuts import render_to_response

'''fffffffffff'''
def reportes(request):
    informe = models.Informe()
    cubo = informe.informe("movimientos", [["pieza", "modelo"], ["tiempo","anio"]], [["stock", "avg"]]) 
    print "generando informe"
    request.session["informe"] = informe  
    return render_to_response('reportes.html',{'header':cubo.header, 'body':cubo.body, 'body_order':cubo.body_order})

def pivot(request):
    a = request.session["informe"]
    cubo = a.pivot()
    request.session["informe"] = a
    return render_to_response('reportes.html',{'header':cubo.header, 'body':cubo.body, 'body_order':cubo.body_order})
    
def roll(request, axis):
    a = request.session["informe"]
    cubo = a.roll(axis)
    request.session["informe"] = a
    return render_to_response('reportes.html',{'header':cubo.header, 'body':cubo.body, 'body_order':cubo.body_order})

def drill(request, axis):
    a = request.session["informe"]
    cubo = a.drill(axis)
    request.session["informe"] = a
    return render_to_response('reportes.html',{'header':cubo.header, 'body':cubo.body, 'body_order':cubo.body_order})

def drill_replacing(request, axis, value):
    a = request.session["informe"]
    cubo = a.drill_replacing(axis, value)
    request.session["informe"] = a
    return render_to_response('reportes.html',{'header':cubo.header, 'body':cubo.body, 'body_order':cubo.body_order})    

def drill_replacing2(request, value0, value1):
    a = request.session["informe"]
    cubo = a.drill_replacing2(value0, value1)
    request.session["informe"] = a
    return render_to_response('reportes.html',{'header':cubo.header, 'body':cubo.body, 'body_order':cubo.body_order})    
