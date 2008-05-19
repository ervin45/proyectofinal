from django import template
register = template.Library()

@register.filter
def hash(h, key):
    return h[key]

@register.filter
def sub(h, index):
    return h[index]

@register.filter
def size(h):
    return len(h)


def con_articulo(algo):
    return "el "+algo

@register.filter
def human_restriction(h):

    if h == {}:
        return "sin restricciones"

    rtn = []
    for k in h.keys():
        if len(h[k]) == 1:
            rtn.append('<tr><td>%s</td><td>%s</td></tr>' % (k, h[k][0]))

    return "<table>"+"".join(rtn)+"</table>"

def human_agg(valor):
    if valor == 'sum':
        return ""
    if valor == 'avg':
        return " (promedio)"

    return " " + valor

@register.filter
def human_measures(l):

    if l == []:
        return "no se visualizan medidas"

    rtn = []
    for value in l:
        if len(value) == 3:
            rtn.append('<li>%s%s</li>' % (value[1], human_agg(value[2])))

    return "\n".join(rtn)


@register.filter
def human_ore(s):
    ''' input example : [['pieza', 'pieza', {'grupo_constructivo': ['92'], 'modelo': ['376'], 'modificacion': ['73']}]] '''
    print "HUMAN_ORE", s

    try:
        l = eval(s)
    except:
        l = s

    rtn = []
    for restr in l:
        tabla = human_restriction(restr[2])
        rtn.append((restr[0],tabla))
    return "\n".join(["<li>%s: <b>%s</b></li>" % x for x in rtn])