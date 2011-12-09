# -*- coding: utf-8 -*-
from django.contrib import admin
from cpu.bkz.models import *

class PositionAdmin(admin.ModelAdmin):
    list_display = ('name','place','field','position')


admin.site.register(Positions,PositionAdmin)