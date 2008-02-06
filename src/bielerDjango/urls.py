from django.conf.urls.defaults import patterns
from olap.views import current_datetime
from olap.views import reportes

urlpatterns = patterns('',
    (r'^time/$', current_datetime),
    (r'^reportes/(\d)/$', reportes),
)
