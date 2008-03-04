from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import *
import olap.views as olap
import report_management.views as rm

urlpatterns = patterns('',
    (r'^report/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-zA-Z0-9_]*)/params=(.*)/([a-zA-Z0-9_]*)/params=(.*)/$', olap.report),
    (r'^report2/([a-zA-Z0-9_]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-zA-Z0-9_]*)/params=(.*)/([a-zA-Z0-9_]*)/params=(.*)/$', olap.report2),
    (r'^pivot/$', olap.pivot),
    (r'^drill/(.*)/$', olap.drill),
    (r'^drill_replacing/(.*)/(.*)/$', olap.drill_replacing),
    (r'^drill_replacing2/(.*)/(.*)/$', olap.drill_replacing2),
    (r'^roll/(.*)/$', olap.roll),
    (r'^dice/(.*)/(.*)/$', olap.dice),
    (r'^graph_data/$', olap.graph_data),

    (r'^report/formulario/$',olap.formulario),
    (r'^report/formulario2/$',olap.formulario2),
    (r'^report/get_dimensions/(.*)/$',olap.get_dimensions),
    (r'^report/get_levels/(.*)/$',olap.get_levels),
    (r'^report/get_levels_without_todo/(.*)/$',olap.get_levels_without_todo),
    (r'^report/get_values/(.*)/(.*)/$',olap.get_values),
    (r'^report/get_measures/(.*)/$',olap.get_measures),
    (r'^report/get_cf/$',olap.get_cf),

    (r'^report/report_list/$', rm.report_list),
    (r'^report/delete/(\d{1,4})/$', rm.delete),



    (r'^admin/', include('django.contrib.admin.urls')),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/proyecto/proyectofinal/src/bielerDjango/media'}),
)