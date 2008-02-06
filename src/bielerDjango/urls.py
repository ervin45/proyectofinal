from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import *
from olap.views import *

urlpatterns = patterns('',
    (r'^reportes/$', reportes),
    (r'^pivot/$', pivot),
    (r'^setSession/(.+)/$', setSession),
    (r'^printSession/$', printSession),
    (r'^admin/', include('django.contrib.admin.urls')),
)
