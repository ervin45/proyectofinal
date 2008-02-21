from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import *
import olap.views as olap
import report_management.views as rm

urlpatterns = patterns('',
    (r'^report/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/xr=(.*)/yr=(.*)/ore=(.*)/$', olap.report),
    (r'^report2/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/xr=(.*)/yr=(.*)/ore=(.*)$', olap.report2),
    (r'^pivot/$', olap.pivot),
    (r'^drill/(.*)/$', olap.drill),
    (r'^drill_replacing/(.*)/(.*)/$', olap.drill_replacing),
    (r'^drill_replacing2/(.*)/(.*)/$', olap.drill_replacing2),
    (r'^roll/(.*)/$', olap.roll),
    (r'^dice/(.*)/(.*)/$', olap.dice),
    (r'^graph_data/$', olap.graph_data),
    
    (r'^report/report_list/$', rm.report_list),
    (r'^report/delete/(\d{1,4})/$', rm.delete),
    
    (r'^admin/', include('django.contrib.admin.urls')),
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/proyecto/proyectofinal/src/bielerDjango/media'}),
    
)
