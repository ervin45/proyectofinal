from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import *
import olap.views as olap
import report_management.views as rm

import os

pwd = os.getcwd()
media_dir = '%s/media' % pwd
print 'media_dir', media_dir

urlpatterns = patterns('',
    (r'^$', olap.index),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),

    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^index/$', olap.index),
    (r'^initial/$', olap.initial),
    (r'^report/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-zA-Z0-9_]*)/params=(.*)/([a-zA-Z0-9_]*)/params=(.*)/$', olap.report),
    (r'^report2/([a-zA-Z0-9_]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-zA-Z0-9_]*)/params=(.*)/([a-zA-Z0-9_]*)/params=(.*)/$', olap.report2),
    (r'^pivot/$', olap.pivot),
    (r'^drill/(.*)/$', olap.drill),
    (r'^replace_to/(.*)/(.*)/$', olap.replace_to),
    (r'^replace_to_both_axis/(.*)/(.*)/$', olap.replace_to_both_axis),
    (r'^roll/(.*)/$', olap.roll),
    (r'^dice/(.*)/(.*)/$', olap.dice),
    (r'^graph_data/$', olap.graph_data),

    (r'^navigation_tree/$', olap.navigation_tree),
    (r'^create_report/$', olap.create_report),
    (r'^adm_report/$', olap.adm_report),
    (r'^adm_categoria/$', olap.adm_categoria),

    (r'^save_report/$', olap.save_report),
    (r'^delete_report/$', olap.delete_report),

    (r'^save_categoria/$', olap.save_categoria),
    (r'^delete_categoria/$', olap.delete_categoria),

    (r'^report/formulario/$',olap.formulario),
    (r'^report/formulario2/$',olap.formulario2),
    (r'^report/get_dimensions/(.*)/$',olap.get_dimensions),
    (r'^report/get_levels/(.*)/$',olap.get_levels),
    (r'^report/get_levels_without_todo/(.*)/$',olap.get_levels_without_todo),
    (r'^report/get_values/(.*)/(.*)/$',olap.get_values),
    (r'^report/get_measures/(.*)/$',olap.get_measures),
    (r'^report/get_cf/$',olap.get_cf),

    (r'^admin/', include('django.contrib.admin.urls')),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_dir}),
)
