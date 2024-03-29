from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import *
import olap.views as olap
import report_management.views as rm

import os

pwd = os.getcwd()
media_dir = '%s/media' % pwd
print 'media_dir', media_dir

urlpatterns = patterns('',
    (r'^$', olap.View.index),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),

    (r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    (r'^index/$', olap.View.index),
    (r'^initial/$', olap.View.initial),
    (r'^report/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-zA-Z0-9_]*)/params=(.*)/([a-zA-Z0-9_]*)/params=(.*)/$', olap.View.report),
    (r'^report2/([a-zA-Z0-9_]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_:]*)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]*)/xr=(.*)/yr=(.*)/ore=(.*)/([a-zA-Z0-9_]*)/params=(.*)/([a-zA-Z0-9_]*)/params=(.*)/$', olap.View.report2),
    (r'^pivot/$', olap.View.pivot),
    (r'^drill/(.*)/$', olap.View.drill),
    (r'^replace_to/(.*)/(.*)/$', olap.View.replace_to),
    (r'^replace_to_both_axis/(.*)/(.*)/$', olap.View.replace_to_both_axis),
    (r'^roll/(.*)/$', olap.View.roll),
    (r'^dice/(.*)/(.*)/$', olap.View.dice),

    (r'^navigation_tree/$', olap.View.navigation_tree),
    (r'^create_report/$', olap.View.create_report),
    (r'^adm_report/$', olap.View.adm_report),
    (r'^adm_categoria/$', olap.View.adm_categoria),

    (r'^report/formulario/$',olap.View.formulario),
    (r'^report/formulario2/$',olap.View.formulario2),


    (r'^save_report/$', olap.ViewAjax.save_report),
    (r'^delete_report/$', olap.ViewAjax.delete_report),

    (r'^save_categoria/$', olap.ViewAjax.save_categoria),
    (r'^delete_categoria/$', olap.ViewAjax.delete_categoria),

    (r'^report/get_dimensions/(.*)/$',olap.ViewAjax.get_dimensions),
    (r'^report/get_levels/(.*)/$',olap.ViewAjax.get_levels),
    (r'^report/get_levels_without_todo/(.*)/$',olap.ViewAjax.get_levels_without_todo),
    (r'^report/get_values/(.*)/(.*)/$',olap.ViewAjax.get_values),
    (r'^report/get_measures/(.*)/$',olap.ViewAjax.get_measures),
    (r'^report/get_cf/$',olap.ViewAjax.get_cf),

    (r'^admin/', include('django.contrib.admin.urls')),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_dir}),
)
