#!/usr/bin/python
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

import inspect,re
from olap import cubiculo
from olap import reports

def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).

    NO USAR ESTA FUNCION EN LINEAS LARGAS!!!
    mejor leer:
    http://docs.python.org/lib/module-textwrap.html
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line)-line.rfind('\n')-1
                         + len(word.split('\n',1)[0]) >= width)],
                   word),
                  text.split(' ')
                 )

classes = [cubiculo.Cubiculo, 
           cubiculo.Meta,     
           reports.Cube,      
           reports.Report1,   
           reports.Report2,   
           reports.Ajax_responser]

for clase in classes:

    print
    titulo = "Clase: %s.%s"  % (clase.__module__,clase.__name__)
    print titulo
    print "-" * len(titulo)
    print ""

    metodos = [(t[0],t[1].__doc__) for t in inspect.getmembers(clase,lambda x: inspect.ismethod(x) or inspect.isfunction(x))]

    metodos_con_docstring = [x for x in metodos if x[1]]

    for (metodo, docstring) in metodos_con_docstring:

        print 'Metodo: %s' % metodo
        print
        lineas = wrap(docstring, 70).split("\n")
        lineas_sin_lineas_blancas = [x for x in lineas if not re.match(' +$',x)]
        lineas_identadas = ["  %s" % x.strip() for x in lineas_sin_lineas_blancas]
        print "\n".join(lineas_identadas)
        print
