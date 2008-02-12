import models
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from pprint import pprint

def costo_promedio(costo_pesos, cantidad):
    return float(costo_pesos) / float(cantidad)

def report(request,report, x, y, xl, yl, xr="", yr="", ore=""):
    report = models.Report(x, y, xl, yl, xr, yr, ore, costo_promedio)
    cube = report.build_cube()
    return render_to_response('reportes.html',{'cube':cube})

def pivot(request):
    (report, x, y, xl, yl, xr, yr, ore) = parse_url(request.META['HTTP_REFERER'])
    report = models.Report(x, y, xl, yl, xr, yr, ore, costo_promedio)
    url = report.pivot()
    return HttpResponseRedirect(url)
    
def roll(request, axis):
    (report, x, y, xl, yl, xr, yr, ore) = parse_url(request.META['HTTP_REFERER'])
    report = models.Report(x, y, xl, yl, xr, yr, ore, costo_promedio)
    url = report.roll(axis)
    return HttpResponseRedirect(url)

def drill(request, axis):
    (report, x, y, xl, yl, xr, yr, ore) = parse_url(request.META['HTTP_REFERER'])
    report = models.Report(x, y, xl, yl, xr, yr, ore, costo_promedio)
    url = report.drill(axis)
    return HttpResponseRedirect(url)

def drill_replacing(request, axis, value):
    (report, x, y, xl, yl, xr, yr, ore) = parse_url(request.META['HTTP_REFERER'])
    report = models.Report(x, y, xl, yl, xr, yr, ore, costo_promedio)
    url = report.drill_replacing(axis, value)
    return HttpResponseRedirect(url)

def drill_replacing2(request, value0, value1):
    (report, x, y, xl, yl, xr, yr, ore) = parse_url(request.META['HTTP_REFERER'])
    report = models.Report(x, y, xl, yl, xr, yr, ore, costo_promedio)
    url = report.drill_replacing2(value0, value1)
    return HttpResponseRedirect(url)

def parse_url(referer):
    import re
    
    referer = referer.replace("%7B", "{")
    referer = referer.replace("%7D", "}")
    referer = referer.replace("%5B", "[")
    referer = referer.replace("%5D", "]")
    referer = referer.replace("%20", " ")    

    p = re.compile('^http://localhost:8000/report/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/xr=(.*)/yr=(.*)/ore=(.*)/$')    
    result = p.findall(referer)
    
    return result[0]
