# -*- coding: utf-8 -*-
from django.contrib import admin
from cpu.bkz.models import *

class dvt21Admin(admin.ModelAdmin):
#    list_display = ('__unicode__','doc_date')
#    list_filter = ('solds__brick','agent')
#    ordering = ('-doc_date','agent')
    pass

class dvt22Admin(admin.ModelAdmin):
    pass

class termoadat22mAdmin(admin.ModelAdmin):
    pass


admin.site.register(dvt21, dvt21Admin)
admin.site.register(dvt22, dvt22Admin)
admin.site.register(termodat22m, termoadat22mAdmin)