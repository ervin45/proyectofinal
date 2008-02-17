import models
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from pprint import pprint

def costo_promedio(costo_pesos, cantidad):
    return float(costo_pesos) / float(cantidad)

def report(request,report_name, x, y, xl, yl, xr="", yr="", ore=""):
    report = models.Report(report_name, x, y, xl, yl, xr, yr, ore, costo_promedio)
    
    cube = report.build_cube()
    main_axis = report.getMainAxisList()
    other_axis = report.getOtherAxisList()
    
    request.session['data'] = cube
    
    return render_to_response('reportes.html',locals())

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

def graph_data(request):
    import OpenFlashChart as ofc
    import itertools as it
    
    cube = request.session['data']
    
    graph = ofc.graph()
    
    bar_colours = ['#000000', '#550000', '#AA0000', '#FF0000']
    
    colour_iter = it.cycle(bar_colours)
    max_y = 0
    for i, valor in enumerate(cube.body_order):
        graph.bar(alpha=50, colour=colour_iter.next(), text=valor, size=10)
        graph.set_data(cube.body[valor])
        
        max_y = max(max_y, max(cube.body[valor]))
        
    
    graph.set_x_labels([str(x) for x in cube.header])
    
    graph.set_y_max(round(float(max_y) * 1.1, -2))
    
    html = graph.render()
    
    return HttpResponse(html)    

def parse_url(request):
    import re
    import urllib
    
    referer = urllib.unquote_plus(request.META['HTTP_REFERER'])
    url_patter = '^http://%s:%s/report/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/xr=(.*)/yr=(.*)/ore=(.*)/$' % (request.META['SERVER_NAME'], request.META['SERVER_PORT'])
    p = re.compile(url_patter)    
    result = p.findall(referer)
    
    return result[0]
