from django.conf.urls.defaults import *
from bkz.models import termodat22m
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^termodat/$','cpu.views.data',{'model':termodat22m}),
    (r'^last/$', 'cpu.views.last'),
    (r'^$', 'cpu.views.main'),

    (r'^chart/$', 'cpu.views.chart'),

    (r'^pos/$', 'cpu.views.positions'),

    (r'^admin/', include(admin.site.urls)),
    (r'^dojango/', include('dojango.urls')),
)
