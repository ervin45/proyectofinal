import models
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from pprint import pprint

def costo_promedio(**kw):
    return kw.get("margen_dolares", 0)

def ratio_ventas_compras(**kw):
    return kw.get("cantidad", 0)
    try:
            return str(float(kw.get("precio_venta_dolares", 0)) / float(kw.get("costo_dolar", 0)))
    except ZeroDivisionError:
            return None
    

def report(request,report_name, x, y, xl, yl, xr="", yr="", ore=""):
    report = models.Report(report_name, x, y, xl, yl, xr, yr, ore, costo_promedio)
    
    cube = report.build_cube()
    main_axis = report.getMainAxisList()
    other_axis = report.getOtherAxisList()
    
    ofc_params = graph_data(cube)
    
    return render_to_response('reportes.html',locals())

def report2(request,ft1, x1, y1, xl1, yl1, xr1="", yr1="", ore1=""
    ,ft2, x2, y2, xl2, yl2, xr2="", yr2="", ore2=""):
    report = models.Report2(ft1, x1, y1, xl1, yl1, xr1="", yr1="", ore1=""
    ,ft2, x2, y2, xl2, yl2, xr2="", yr2="", ore2="", costo_promedio)
    
    cube = report2.build_cube()
    #main_axis = report2.getMainAxisList()
    #other_axis = report2.getOtherAxisList()
    
    ofc_params = graph_data(cube)
    
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

def graph_data(cube):
    import OpenFlashChart as ofc
    import itertools as it
    
    graph = ofc.graph()
    graph.x_label_style="13,#9933CC,2"
    
    bar_colours = ['#000000', '#550000', '#AA0000', '#FF0000']
    
    colour_iter = it.cycle(bar_colours)
    max_y = 0
    for i, valor in enumerate(cube.body_order):
        row_values_str = cube.body[valor]
        row_values     = [float(x) for x in row_values_str if x]
        
        graph.bar(alpha=50, colour=colour_iter.next(), text=valor, size=10)
        graph.set_data(row_values_str)
        
        max_y = max([max_y] + row_values)
        
    
    graph.set_x_labels([str(x) for x in cube.header])
    
    if max_y < 50: 
        max_y2 = 50 
    else: 
        max_y2 = round(float(max_y) * 1.1 + 50, -2)
        
    graph.set_y_max(max_y2)
    
    return graph.render_js()

def parse_url(request):
    import re
    import urllib
    
    referer = urllib.unquote_plus(request.META['HTTP_REFERER'])
    url_patter = '^http://%s:%s/report/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/xr=(.*)/yr=(.*)/ore=(.*)/$' % (request.META['SERVER_NAME'], request.META['SERVER_PORT'])
    p = re.compile(url_patter)    
    result = p.findall(referer)
    
    return result[0]
