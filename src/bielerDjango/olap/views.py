import models
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from pprint import pprint

def costo_promedio(costo_pesos, cantidad):
    return float(costo_pesos) / float(cantidad)

def report(request,report_name, x, y, xl, yl, xr="", yr="", ore=""):
    report = models.Report(report_name, x, y, xl, yl, xr, yr, ore, costo_promedio)
    cube = report.build_cube()
    return render_to_response('reportes.html',{'cube':cube})

def pivot(request):
    (report, x, y, xl, yl, xr, yr, ore) = parse_url(request)
    report = models.Report(report, x, y, xl, yl, xr, yr, ore, costo_promedio)
    url = report.pivot(request)
    return HttpResponseRedirect(url)
    
def roll(request, axis):
    (report, x, y, xl, yl, xr, yr, ore) = parse_url(request)
    report = models.Report(report, x, y, xl, yl, xr, yr, ore, costo_promedio)
    url = report.roll(request, axis)
    return HttpResponseRedirect(url)

def drill(request, axis):
    (report, x, y, xl, yl, xr, yr, ore) = parse_url(request)
    report = models.Report(report, x, y, xl, yl, xr, yr, ore, costo_promedio)
    url = report.drill(request, axis)
    return HttpResponseRedirect(url)

def drill_replacing(request, axis, value):
    (report, x, y, xl, yl, xr, yr, ore) = parse_url(request)
    report = models.Report(report, x, y, xl, yl, xr, yr, ore, costo_promedio)
    url = report.drill_replacing(request, axis, value)
    return HttpResponseRedirect(url)

def drill_replacing2(request, value0, value1):
    (report, x, y, xl, yl, xr, yr, ore) = parse_url(request)
    report = models.Report(report, x, y, xl, yl, xr, yr, ore, costo_promedio)
    url = report.drill_replacing2(request, value0, value1)
    return HttpResponseRedirect(url)

def dice(request, main_axix, other_axis):
    (report, x, y, xl, yl, xr, yr, ore) = parse_url(request)
    report = models.Report(report, x, y, xl, yl, xr, yr, ore, costo_promedio)
    url = report.dice(request, main_axix, other_axis)
    return HttpResponseRedirect(url)    

def parse_url(request):
    import re
    import urllib
    
    referer = urllib.unquote_plus(request.META['HTTP_REFERER'])
    url_patter = '^http://%s:%s/report/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/xr=(.*)/yr=(.*)/ore=(.*)/$' % (request.META['SERVER_NAME'], request.META['SERVER_PORT'])
    p = re.compile(url_patter)    
    result = p.findall(referer)
    
    return result[0]
