from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import *
from olap.views import *

urlpatterns = patterns('',
    (r'^reportes/$', reportes),
    (r'^report/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/([a-z_]*)/xr=(.*)/yr=(.*)/ore=(.*)/$', report),
    (r'^pivot/$', pivot),
    (r'^drill/(.*)/$', drill),
    (r'^drill_replacing/(.*)/(.*)/$', drill_replacing),
    (r'^drill_replacing2/(.*)/(.*)/$', drill_replacing2),
    (r'^roll/(.*)/$', roll),
    
    (r'^admin/', include('django.contrib.admin.urls')),
)
