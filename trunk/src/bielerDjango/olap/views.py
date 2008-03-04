import models
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from pprint import pprint
import math

def header_list_top(header):
    if header == ['TODO']:
        return [[['TODO', 1]]]
    
    levels_count = len(header[0].split("-"))
    
    result = []
    caminos = []
    
    for i in range(levels_count):
        result.append([])
        caminos.append([])
    
    
    
    for x in header:
        temp = x.split("-")
        for i in range(levels_count):
    
            if not temp[:i + 1] in caminos[i]:
                result[i].append([temp[i], 1])
                caminos[i].append(temp[:i + 1])
            else:
                result[i][len(result[i]) - 1][1] += 1

    return result, len(result)
        
def _slide_col(t, start, end):
    result = []
    sum = 0
    for tl in t:
        sum += tl[1]
        
        if sum in range(start + 1, end + 1):
            result.append(tl)
            
        if sum > end:
            break

    return result

def header_list_left(header):
    if header[0] == ['TODO']:
        return [[['TODO', 1]]]

    re = header_list_top(header)[0]

    temp = []
    for x in range(len(re) - 1):
        temp.append([])

    last_level = re[len(re) - 1]
    last_level = [x + ["LAST"] for x in last_level]

    temp.append(last_level)

    for x in range(len(re) - 2, -1, -1):
        count = 0
        for l in re[x]:
            temp[x].append(l)
            temp[x].extend(_slide_col(temp[x+1], count, count + l[1] * (len(re) - 1 -x)))

            count = count + l[1]

    rows = []
    col = []
    for x in temp[0]:
        col.append(x)
        try:
            if x[2] == "LAST":
                rows.append(col)
                col = []
        except:
            pass
        
    return rows, len(re)


def report(request,ft, x, y, xl, yl, xr, yr, ore, mf, params, cf, cf_params):
    report = models.Report1(ft, x, y, xl, yl, xr, yr, ore, mf, params, cf, cf_params)

    
    try:
        cube = report.build_cube()   
        
        header     = cube.dim_y
        
        header_top, header_top_size = header_list_top(cube.dim_y)
        pprint(header_top)
        
        header_left, header_left_size = header_list_left(cube.dim_x)
        pprint(header_left)
        
        body       = get_body(cube)
        body_order = cube.dim_x     
        
        can_roll_x   = cube.can_roll_x()
        can_roll_y   = cube.can_roll_y()
        can_drill_x  = cube.can_drill_x()
        can_drill_y  = cube.can_drill_y()
         
        cube_info    = cube.get_info()
        ft           = cube_info[0][0]
        dimensions   = cube_info[0][1]
        measures     = cube_info[0][2]
        ore          = cube_info[0][3] 
        
        dim_x = x
        dim_y = y
        
        from django.conf import settings
        server_ip = settings.IP        
            
        main_axis = report.get_main_axis_list()
        
        other_axis = ['Seleccionar..']
        other_axis.extend(report.get_other_axis_list())
        
        #ofc_params = graph_data(header, body, body_order, x, xl)
        return render_to_response('reportes2.html',locals())
    
    except models.CubeTooBig:
        return render_to_response('tooBig.html',locals())
    

def report2(request,ft1, x1, y1, xl1, yl1, xr1, yr1, ore1
    ,ft2, x2, y2, xl2, yl2, xr2, yr2, ore2, mf, params, cf, cf_params):
    report2 = models.Report2(ft1, x1, y1, xl1, yl1, xr1, yr1, ore1
    ,ft2, x2, y2, xl2, yl2, xr2, yr2, ore2, mf, params, cf, cf_params)
    
    try:
        cube = report2.build_cube()
        
        header     = cube.dim_y
        body       = get_body(cube)
        body_order = cube.dim_x
        
        can_roll_x   = cube.can_roll_x()
        can_roll_y   = cube.can_roll_y()
        can_drill_x  = cube.can_drill_x()
        can_drill_y  = cube.can_drill_y()
        
        cube_info    = cube.get_info()
        ft           = cube_info[0][0]
        dimensions   = cube_info[0][1]
        measures     = cube_info[0][2]
        ore          = cube_info[0][3]         
        
        ft2           = cube_info[1][0]
        dimensions2   = cube_info[1][1]
        measures2     = cube_info[1][2]
        ore2          = cube_info[1][3]        
        
        main_axis = report2.get_main_axis_list()
        other_axis = report2.get_other_axis_list()
        
        #ofc_params = graph_data(header, body, body_order)
        
        return render_to_response('reportes2.html',locals())
    
    except models.CubeTooBig, e:
        cells = e.cells
        rows  = e.rows
        
        return render_to_response('tooBig.html',locals())

def pivot(request):
    report = get_report(request)
    url = report.pivot(request)
    return HttpResponseRedirect(url)
    
def roll(request, axis):
    report = get_report(request)
    url = report.roll(request, axis)
    return HttpResponseRedirect(url)

def drill(request, axis):
    report = get_report(request)
    url = report.drill(request, axis)
    return HttpResponseRedirect(url)

def drill_replacing(request, axis, value):
    report = get_report(request)
    url = report.drill_replacing(request, axis, value)
    return HttpResponseRedirect(url)

def drill_replacing2(request, value0, value1):
    report = get_report(request)
    url = report.drill_replacing2(request, value0, value1)
    return HttpResponseRedirect(url)

def dice(request, main_axis, other_axis):
    report = get_report(request)
    url = report.dice(request, main_axis, other_axis)
    return HttpResponseRedirect(url)



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

def get_report(request):
    from django.conf import settings
    
    http_referer = request.META['HTTP_REFERER']
    server_ip  = settings.IP
    server_port  = request.META['SERVER_PORT']
    
    if referer_type(http_referer, server_ip, server_port) == "Report1":
        parsed_url = parse_url(http_referer, server_ip, server_port)
        (report, x, y, xl, yl, xr, yr, ore, mf, params, cf, cf_params) = parsed_url
        
        report = models.Report1(report, x, y, xl, yl, xr, yr, ore, mf, params, cf, cf_params)
    else:
        parsed_url = parse_url2(http_referer, server_ip, server_port)
        (ft1, x1, y1, xl1, yl1, xr1, yr1, ore1, ft2, x2, y2, xl2, yl2, xr2, yr2, ore2, mf, params, cf, cf_params) = parsed_url
        report = models.Report2(ft1, x1, y1, xl1, yl1, xr1, yr1, ore1, ft2, x2, y2, xl2, yl2, xr2, yr2, ore2, mf, params, cf, cf_params)
        
    return report

    
def referer_type(http_referer, server_ip, server_port):
    if parse_url(http_referer, server_ip, server_port):
        return "Report1"
    else:
        return "Report2"

def parse_url(http_referer, server_ip, server_port):
    import re
    import urllib
    
    referer = urllib.unquote_plus(http_referer)
    url_patter = '^http://%s:%s/report/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-zA-Z0-9_]*)/params=(.*)/([a-zA-Z0-9_]*)/params=(.*)/$' % (server_ip, server_port)
    p = re.compile(url_patter)
    result = p.findall(referer)
    
    if result == []:
        return False
    
    return result[0]

def parse_url2(http_referer, server_ip, server_port):
    import re
    import urllib
    
    referer = urllib.unquote_plus(http_referer)
    
    url_patter = '^http://%s:%s/report2/([a-zA-Z0-9_]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-zA-Z0-9_]*)/params=(.*)/([a-zA-Z0-9_]*)/params=(.*)/$' % (server_ip, server_port)
    p = re.compile(url_patter)
    result = p.findall(referer)
    
    if result == []:
        return False
    
    return result[0]



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


def graph_data(header, body, body_order, x_label_dim, x_label_level):
    import OpenFlashChart as ofc
    import itertools as it
    
    graph = ofc.graph()
    graph.x_label_style = "11,#9933CC,2"
    graph.y_label_style= "11,#9933CC,2"
    
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
        
        graph.bar(alpha=50, colour=colour_iter.next(), text=valor, size=8)
        graph.set_data(row_values_str)
        
        max_y = max([max_y] + row_values)
        
    
    graph.set_x_labels([str(x) for x in header])
    graph.x_legend= '%s[%s],20,#736AFF' % (x_label_dim, x_label_level)
    #graph.y_legend= 'ves in Feburary,20,#736AFF'

    graph.set_y_max(get_tope(max_y))
    
    return graph.render_js()
    
    
        
        
def formulario(request):
    from django.conf import settings
    server_ip = settings.IP
    
    return render_to_response('formulario.html',locals())
            
def formulario2(request):
    from django.conf import settings
    server_ip = settings.IP
        
    return render_to_response('formulario2.html',locals())
            
            
####AJAX####
from cubiculo import Meta

def get_dimensions(request, ft):
    response = models.Ajax_responser.get_dimensions(ft)
    return HttpResponse("|".join(response))

def get_measures(request, ft):
    response = models.Ajax_responser.get_measures(ft)
    response = ["ft_%s.%s" % (ft, x) for x in response]
    return HttpResponse("|".join(response))

def get_levels(request, dimension):
    response = models.Ajax_responser.get_levels(dimension)
    return HttpResponse("|".join(response))

def get_levels_without_todo(request, dimension):
    response = models.Ajax_responser.get_levels(dimension)
    response.remove('TODO')
    print "get_levels_without_todo"
    pprint(response)
    return HttpResponse("|".join(response))

def get_values(request, dimension, level):
    response = models.Ajax_responser.get_values(dimension, level)
    print response
    return HttpResponse("|".join(response))

def get_mf(request):
    return HttpResponse('')

def get_cf(request):
    response = models.Ajax_responser.get_cf()
    print str(response)
    return HttpResponse(str(response))


