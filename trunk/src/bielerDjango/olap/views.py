from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User

import models
import cubiculo
import reports

from pprint import pprint
import math

# patron espacios de mas \s{1,}$

def header_list_top(header):
    if header == ['TODO']:
        return [[['TODO', 1,'TODO']]], 1

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
                branch = "-".join(temp[:i + 1])
                result[i].append([temp[i], 1, branch])
                caminos[i].append(temp[:i + 1])
            else:
                result[i][len(result[i]) - 1][1] += 1

    return result, len(result)

#toma un nivel un corta una tajada cuya suma incremental del COLSPAN este entre start y end
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
    if header == ['TODO']:
        return [[['TODO', 1,'TODO']]], 1

    re = header_list_top(header)[0]

    temp = []
    for x in range(len(re) - 1):
        temp.append([])

    last_level = re[len(re) - 1]
    last_level = [x + ["LAST"] for x in last_level]

    temp.append(last_level)


    #La estructura jerarquica de la funcion header_list_top debe aplanarse (RAIZ, IZQUIERDO, DERECHO)
    for x in range(len(re) - 2, -1, -1):
        count = 0
        for l in re[x]:
            temp[x].append(l)
            temp[x].extend(_slide_col(temp[x+1], count, count + l[1] * (len(re) - 1 - x)))

            #count = count + l[1]
            count = count + l[1] * (len(re) - 1 - x)

    rows = []
    col = []
    for x in temp[0]:
        col.append(x)
        try:
            if x[3] == "LAST":
                rows.append(col)
                col = []
        except:
            pass

    return rows, len(re)

@login_required(redirect_field_name='/login/')
def index(request):
    return render_to_response('index.html',locals())

@login_required(redirect_field_name='/login/')
def initial(request):
    return render_to_response('initial.html',locals())

def restriction_human_redeable(h):
    return "test:" + str(h)

@login_required(redirect_field_name='/login/')
def report(request,ft, x, y, xl, yl, xr, yr, ore, mf, params, cf, cf_params):
    report = reports.Report1(ft, x, y, xl, yl, xr, yr, ore, mf, params, cf, cf_params)

    logged_user_name = User.objects.get(id=request.user.id).username

    try:
        cube = report.build_cube()
    except reports.CubeTooBig:
        return render_to_response('tooBig.html',locals())
    except reports.CubeEmpty, e:
        cell = -50
        rows = -50
        return render_to_response('empty.html', locals())

    total_x = cube.total_x()
    total_y = cube.total_y()

    header     = cube.dim_y
    header_top, header_top_size = header_list_top(cube.dim_y)

    #pprint(cube.dim_y)

    header_left, header_left_size = header_list_left(cube.dim_x)

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

    #pprint(body)

    main_axis = report.get_main_axis_list()

    other_axis = ['Seleccionar..']
    other_axis.extend(report.get_other_axis_list())

    if len(cube.dim_x) > 20 or len(cube.dim_y) > 20:
        ofc_params = ""
        mostrar_grafico = False
    else:
        ofc_params = graph_data(header, body, body_order, x, xl)
        mostrar_grafico = True

    categorias = models.Categoria.objects.filter(user_id=request.user.id)

    exp_t = [cubiculo.Meta.measure_as_string(x) for x in measures]
    ##FIXME: " y " deberia ser reemplzado por la operacion entre measures
    join_exp_t = " y ".join(exp_t)
    
    explanation = "Ud. esta viendo " + join_exp_t

    return render_to_response('reportes2.html',locals())

@login_required(redirect_field_name='/login/')
def report2(request,ft1, x1, y1, xl1, yl1, xr1, yr1, ore1
    ,ft2, x2, y2, xl2, yl2, xr2, yr2, ore2, mf, params, cf, cf_params):

    report2 = reports.Report2(ft1, x1, y1, xl1, yl1, xr1, yr1, ore1
    ,ft2, x2, y2, xl2, yl2, xr2, yr2, ore2, mf, params, cf, cf_params)

    logged_user_name = User.objects.get(id=request.user.id).username

    try:
        cube = report2.build_cube()
    except reports.CubeTooBig, e:
        cells = e.cells
        rows  = e.rows
        return render_to_response('tooBig.html',locals())
    except reports.CubeEmpty, e:
        cell = -50
        rows = -50
        return render_to_response('tooBig.html', locals())



    total_x = cube.total_x()
    total_y = cube.total_y()

    header     = cube.dim_y
    pprint(header)

    header_top, header_top_size = header_list_top(cube.dim_y)
    header_left, header_left_size = header_list_left(cube.dim_x)

    body       = get_body(cube)
    pprint(body)
    body_order = cube.dim_x
    pprint(body_order)

    pprint(header_top)
    pprint(header_left)

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

    dim_x = x1
    dim_y = y1

    main_axis = report2.get_main_axis_list()
    other_axis = report2.get_other_axis_list()

    if len(cube.dim_x) > 20 or len(cube.dim_y) > 20:
        ofc_params = ""
        mostrar_grafico = False
    else:
        ofc_params = graph_data(header, body, body_order, x1, xl1)
        mostrar_grafico = True

    categorias = models.Categoria.objects.filter(user_id=request.user.id)

    tmp = []
    tmp.extend(measures)
    tmp.extend(measures2)
    exp_t = [cubiculo.Meta.measure_as_string(x) for x in tmp]
    ##FIXME: llevar esto al META para que no pase lo siguiente:
    ## '''Ud. esta viendo el margen de ventas expresado
    ## en pesos multiplicar el stock promedio expresado en piezas'''
    
    join_exp_t = (" %s " % str(mf)).join(exp_t)
    
    explanation = "Ud. esta viendo " + join_exp_t

    two_cubes = True
    return render_to_response('reportes2.html',locals())

@login_required(redirect_field_name='/login/')
def pivot(request):
    report = get_report(request)
    url = report.pivot(request)
    return HttpResponseRedirect(url)

@login_required(redirect_field_name='/login/')
def roll(request, axis):
    report = get_report(request)
    url = report.roll(request, axis)

    return HttpResponseRedirect(url)

@login_required(redirect_field_name='/login/')
def drill(request, axis):
    report = get_report(request)
    url = report.drill(request, axis)
    return HttpResponseRedirect(url)

@login_required(redirect_field_name='/login/')
def replace_to(request, axis, values):
    report = get_report(request)
    url = report.replace_to(request, axis, values)
    return HttpResponseRedirect(url)

@login_required(redirect_field_name='/login/')
def replace_to_both_axis(request, value0, value1):
    report = get_report(request)
    url = report.replace_to_both_axis(request, value0, value1)
    return HttpResponseRedirect(url)

@login_required(redirect_field_name='/login/')
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

    if referer_type(http_referer) == "Report1":
        parsed_url = parse_url(http_referer)
        (report, x, y, xl, yl, xr, yr, ore, mf, params, cf, cf_params) = parsed_url

        report = reports.Report1(report, x, y, xl, yl, xr, yr, ore, mf, params, cf, cf_params)
    else:
        parsed_url = parse_url2(http_referer)
        (ft1, x1, y1, xl1, yl1, xr1, yr1, ore1, ft2, x2, y2, xl2, yl2, xr2, yr2, ore2, mf, params, cf, cf_params) = parsed_url
        report = reports.Report2(ft1, x1, y1, xl1, yl1, xr1, yr1, ore1, ft2, x2, y2, xl2, yl2, xr2, yr2, ore2, mf, params, cf, cf_params)

    return report


def referer_type(http_referer):
    if parse_url(http_referer):
        return "Report1"
    else:
        return "Report2"

def parse_url(http_referer):
    import re
    import urllib

    referer = urllib.unquote_plus(http_referer)
    url_patter = '^.*report/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-zA-Z0-9_]*)/params=(.*)/([a-zA-Z0-9_]*)/params=(.*)/$'
    p = re.compile(url_patter)
    result = p.findall(referer)

    if result == []:
        return False

    return result[0]

def parse_url2(http_referer):
    import re
    import urllib

    referer = urllib.unquote_plus(http_referer)

    url_patter = '^.*/report2/([a-zA-Z0-9_]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-zA-Z0-9_]*)/params=(.*)/([a-zA-Z0-9_]*)/params=(.*)/$'
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
    return render_to_response('formulario.html',locals())

def formulario2(request):
    return render_to_response('formulario2.html',locals())

def navigation_tree(request):
    categorias_admin   = models.Categoria.objects.filter(user_id=1)

    admin = True
    if str(request.user.id) != "1":
        admin = False
        categorias_usuario = models.Categoria.objects.filter(user_id=request.user.id)

    logged_user_id = request.user.id
    return render_to_response('navigation_tree.html',locals())

def adm_categoria(request):
    categorias = models.Categoria.objects.filter(user_id=request.user.id)
    return render_to_response('adm_categoria.html',locals())

def create_report(request):
    return render_to_response('create_report.html',locals())

def adm_report(request):
    return render_to_response('adm_report.html',locals())


####AJAX####

@login_required(redirect_field_name='/login/')
def get_dimensions(request, ft):
    response = reports.Ajax_responser.get_dimensions(ft)
    return HttpResponse("|".join(response))

@login_required(redirect_field_name='/login/')
def get_measures(request, ft):
    response = reports.Ajax_responser.get_measures(ft)
    response = ["ft_%s.%s" % (ft, x) for x in response]
    return HttpResponse("|".join(response))

@login_required(redirect_field_name='/login/')
def get_levels(request, dimension):
    response = reports.Ajax_responser.get_levels(dimension)
    response.reverse()
    return HttpResponse("|".join(response))

@login_required(redirect_field_name='/login/')
def get_levels_without_todo(request, dimension):
    response = reports.Ajax_responser.get_levels(dimension)
    response.reverse()
    response.remove('TODO')
    return HttpResponse("|".join(response))

@login_required(redirect_field_name='/login/')
def get_values(request, dimension, level):
    response = reports.Ajax_responser.get_values(dimension, level)
    return HttpResponse("|".join(response))

@login_required(redirect_field_name='/login/')
def get_mf(request):
    return HttpResponse('')

@login_required(redirect_field_name='/login/')
def get_cf(request):
    response = reports.Ajax_responser.get_cf()
    return HttpResponse(str(response))

@login_required(redirect_field_name='/login/')
def save_report(request):
    nombre         = request.POST.get('nombre')
    dwp  = request.POST.get('dwp')
    categoria_id = request.POST.get('categoria_id')

    categoria = models.Categoria.objects.get(id=categoria_id)

    if models.Reporte.objects.filter(nombre=nombre).extra(where=['categoria_id=%s' % categoria_id]):
        return HttpResponse("repeat_name")

    reporte  = models.Reporte(nombre=nombre, dwp=dwp, categoria=categoria, user_id=request.user.id)
    reporte.save()
    return HttpResponse("")

@login_required(redirect_field_name='/login/')
def delete_report(request):
    id        = request.POST.get('id')
    models.Reporte.objects.get(id=id).delete()

    return HttpResponse("")

@login_required(redirect_field_name='/login/')
def save_categoria(request):
    nombre         = request.POST.get('nombre', False)
    if models.Categoria.objects.filter(user_id=request.user.id).filter(nombre=nombre):
        return HttpResponse("repeat_name")

    categoria  = models.Categoria(nombre=nombre, user_id=request.user.id)
    categoria.save()

    return HttpResponse('')

@login_required(redirect_field_name='/login/')
def delete_categoria(request):
    id = request.POST.get('id')
    models.Categoria.objects.get(id=id).delete()

    return HttpResponse('')
