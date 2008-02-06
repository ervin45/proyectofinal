import models

from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def reportes(self, title):
    informe = models.Informe()
    
    table = informe.informe("movimientos", [["pieza", "codigo"], ["tiempo","anio"]], [["stock", "sum"]])
    
    print table
    t = get_template('reportes.html')
    codigos = list(table.values()).pop(0).keys()
    html = t.render(Context({'title': title, 'filas':table, 'codigos':codigos}))
    return HttpResponse(html)     
    
    #return dict(title=title, filas=table, link=(int(title) + 1))

    
    
   


