import models
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from pprint import pprint
import math


def costo_promedio(first):
    return first.get("costo_dolar", 0)

def ratio_ventas_compras(**kw):
    return kw.get("cantidad", 0)
    try:
            return str(float(kw.get("precio_venta_dolares", 0)) / float(kw.get("costo_dolar", 0)))
    except ZeroDivisionError:
            return None

def rotacion(first, second):

    if not first['cantidad'] or not second['stock']:
        return None

    return first['cantidad'] / second['stock']


def report(request,report_name, x, y, xl, yl, xr="", yr="", ore=""):
    report = models.Report(report_name, x, y, xl, yl, xr, yr, ore, costo_promedio)
    
    print "parameter"
    print report_name, x, y, xl, yl, xr, yr, ore

    
    try:
        cube = report.build_cube()   
        
        header     = cube.dim_y
        body       = get_body(cube)
        body_order = cube.dim_x     
            
        main_axis = report.get_main_axis_list()
        other_axis = report.get_other_axis_list()
    
        #ofc_params = graph_data(header, body, body_order)
        return render_to_response('reportes2.html',locals())
    
    except models.CubeTooBig:
        return render_to_response('tooBig.html',locals())
    

def report2(request,ft1, x1, y1, xl1, yl1, xr1, yr1, ore1
    ,ft2, x2, y2, xl2, yl2, xr2, yr2, ore2):
    report2 = models.Report2(ft1, x1, y1, xl1, yl1, xr1, yr1, ore1
    ,ft2, x2, y2, xl2, yl2, xr2, yr2, ore2, rotacion)
    
    
    cube = report2.build_cube()
    
    header     = cube.dim_y
    body       = get_body(cube)
    body_order = cube.dim_x
    
    
    #main_axis = report2.getMainAxisList()
    #other_axis = report2.getOtherAxisList()
    
    #ofc_params = graph_data(header, body, body_order)
    
    return render_to_response('reportes2.html',locals())

        
def get_body(cube):
    '''
    >>> from pprint import pprint
    >>> c = Cube()
    >>> c.add('uno',1,{"result":1})
    >>> c.add('uno',2,{"result":3})
    >>> c.add('dos',1,{"result":2})
    >>> c.add('dos',2,{"result":7})
    >>> pprint(c.body())
    {'dos': [2, 7], 'uno': [1, 3]}
    '''
        
    result = {}
    
    for x in cube.dim_x:
        result[x] = list(cube.rows(x, 'result'))
        
    return result

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


def get_tope(max_y):
    '''
    Toma max_y y devuelve un numero de tope de la tabla
    '''
    big_max_y = max_y * 1.05
    if max_y <= 1:
        digitos = 1
    else:    
        digitos = math.ceil(math.log10(big_max_y))
    pos = [(x+1)*(10**(digitos-1)) for x in range(10)]
    tope = [x for x in pos if x > big_max_y][0]
    
    return tope


def graph_data(header, body, body_order):
    import OpenFlashChart as ofc
    import itertools as it
    
    graph = ofc.graph()
    graph.x_label_style="13,#9933CC,2"
    
    graph.set_tool_tip('#key# <br> #val#')
    
    palette = ['#0066BB', '#BB0066', '#BB6600',
               '#66BB00', '#6600BB', '#6666BB', '#00ff55',
               '#0055ff', '#ff0055', '#ff5500', '#55ff00',
               '#5500ff', '#5555ff', '#00AA33', '#0033AA',
               '#AA0033', '#AA3300', '#33AA00', '#3300AA',
               '#3333AA', '#00EE88', '#0088EE', '#EE0088',
               '#EE8800', '#88EE00', '#8800EE', '#8888AA']
    bar_colours = palette[0:len(body_order)]
    
    colour_iter = it.cycle(bar_colours)
    max_y = 0
    for i, valor in enumerate(body_order):
        row_values_str = body[valor]
        row_values     = [float(x) for x in row_values_str if x]
        
        graph.bar(alpha=50, colour=colour_iter.next(), text=valor, size=10)
        graph.set_data(row_values_str)
        
        max_y = max([max_y] + row_values)
        
    
    graph.set_x_labels([str(x) for x in header])
    

    graph.set_y_max(get_tope(max_y))
    
    return graph.render_js()

def parse_url(request):
    import re
    import urllib
    
    referer = urllib.unquote_plus(request.META['HTTP_REFERER'])
    url_patter = '^http://%s:%s/report/([a-zA-Z_]*)/([a-zA-Z_]*)/([a-zA-Z_]*)/([a-zA-Z_]*)/([a-zA-Z_]*)/xr=(.*)/yr=(.*)/ore=(.*)/$' % (request.META['SERVER_NAME'], request.META['SERVER_PORT'])
    p = re.compile(url_patter)    
    result = p.findall(referer)
    
    return result[0]

def test(request):
    return HttpResponse('hola')


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
