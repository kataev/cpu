from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
#    (r'^mb/$', 'cpu.mb.views.index'),
#    (r'^mb/archive/(\d{1,4}-\d{1,2}-\d{1,2})/(\d{1,2}:\d{1,2}:\d{1,2})/$', 'cpu.mb.views.dt'),
#    (r'^mb/archive/(\d{1,})/$', 'cpu.mb.views.id'),
#    (r'^mb/archive/spark/$', 'cpu.mb.views.spark'),
    (r'^show/$','cpu.bkz.views.show'),
    (r'^store/(?P<model>\w+)/$','cpu.bkz.views.store'),
    (r'^store_avg/(?P<model>\w+)/(?P<time>\w+)/(?P<limit>\w+)/$','cpu.bkz.views.store_avg'),
    (r'^last/$','cpu.bkz.views.last'),
    (r'^show/(?P<model>\w+)/$','cpu.bkz.views.show'),
    (r'^$','cpu.bkz.views.main'),
    (r'^chart/$','cpu.bkz.views.show_chart'),
    (r'^chart/json/$','cpu.bkz.views.show_dvt_to_chart'),


    # Example:
    # (r'^cpu/', include('cpu.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
