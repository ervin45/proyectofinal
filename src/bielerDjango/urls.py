from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import *
from olap.views import *

urlpatterns = patterns('',
    (r'^reportes/$', reportes),
    (r'^pivot/$', pivot),
    (r'^drill/(.*)/$', drill),
    (r'^drill_replacing/(.*)/(.*)/$', drill_replacing),
    (r'^roll/(.*)/$', roll),
    
    (r'^admin/', include('django.contrib.admin.urls')),
)
