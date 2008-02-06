import models
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.core.context_processors import debug

from django.template import loader, Context

def custom_proc(request):
    "A context processor that provides 'app', 'user' and 'ip_address'."
    return {
        'app': 'My app',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR']
    }

def reportes(request, title):
    informe = models.Informe()
    
    table = informe.informe("movimientos", [["pieza", "codigo"], ["tiempo","anio"]], [["stock", "sum"]])

    print table
    codigos = list(table.values()).pop(0).keys()
    return render_to_response('reportes.html',{'title': title, 'filas':table, 'codigos':codigos},context_instance=RequestContext(request, processors=[custom_proc]))


def setSession(request, valor):
    request.session['valor'] = valor


def printSession(request):
    print request.session['valor']

