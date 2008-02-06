from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import *
from olap.views import *

urlpatterns = patterns('',
    (r'^reportes/(\d)/$', reportes),
    (r'^setSession/(.+)/$', setSession),
    (r'^printSession/$', printSession),
    (r'^admin/', include('django.contrib.admin.urls')),
)
