#############################################################################
#
#    Sistema de soporte de decisiones para Ricardo Bieler S.A.
#    Copyright (C) 2007-2008 Nicolas D. Cesar, Mariano N. Galan
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
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

    l = eval(s)
    rtn = []
    for restr in l:
        tabla = human_restriction(restr[2])
        rtn.append((restr[0],tabla))
    return "\n".join(["<li>%s: <b>%s</b></li>" % x for x in rtn])
#############################################################################
#
#    Sistema de soporte de decisiones para Ricardo Bieler S.A.
#    Copyright (C) 2007-2008 Nicolas D. Cesar, Mariano N. Galan
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
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

    l = eval(s)
    rtn = []
    for restr in l:
        tabla = human_restriction(restr[2])
        rtn.append((restr[0],tabla))
    return "\n".join(["<li>%s: <b>%s</b></li>" % x for x in rtn])
