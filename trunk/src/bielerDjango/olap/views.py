import models
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from pprint import pprint

def costo_promedio(costo_pesos, cantidad):
    return float(costo_pesos) / float(cantidad)

def report(request,report, x, y, xl, yl, xr="", yr="", ore=""):
    #informe = models.Informe()
    
    report = models.Report()
    
    ##VIENE DE LA BD
    report.ft = "compras" #report
    report.measures = [["cantidad", "sum"],['costo_pesos', 'sum']]
    report.member_function = costo_promedio
    ##VIENE DE LA BD
    
    report.x = x
    report.xl = xl
    report.y = y
    report.yl = yl
    report.xr = xr
    report.yr = yr
    report.ore = ore
    
    cube = report.get_cube()
    
    request.session['informe'] = report
    print "body or"
    print cube.header
    print cube.body_order 
    print cube.body
    return render_to_response('reportes.html',{'cube':cube})

def pivot(request):
    a = request.session["informe"]
    url = a.pivot()
    return HttpResponseRedirect(url)
    
def roll(request, axis):
    a = request.session["informe"]
    url = a.roll(axis)
    return HttpResponseRedirect(url)

def drill(request, axis):
    a = request.session["informe"]
    url = a.drill(axis)
    return HttpResponseRedirect(url)

def drill_replacing(request, axis, value):
    a = request.session["informe"]
    url = a.drill_replacing(axis, value)
    return HttpResponseRedirect(url)

def drill_replacing2(request, value0, value1):
    a = request.session["informe"]
    url = a.drill_replacing2(value0, value1)
    return HttpResponseRedirect(url)