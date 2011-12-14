from django.conf.urls.defaults import *
from bkz.models import termodat22m
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^data/$','cpu.views.data'),
    (r'^last/$', 'cpu.views.last'),
    (r'^$', 'cpu.views.main'),

    (r'^chart/$', 'cpu.views.chart'),

    (r'^admin/', include(admin.site.urls)),
    (r'^dojango/', include('dojango.urls')),
)
