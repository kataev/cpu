# -*- coding: utf-8 -*-
__author__ = 'bteam'
from dojango import forms
import datetime

class ChartForm(forms.Form):
    value_c = (
    ('hmdt', u'Влажность'),
    ('temp', u'Температура'),
    ('t1',u"гор 703"),
    ('t2',u"гор 704"),
    ('t3',u"гор 306"),
    ('t4',u"гор 606"),
    ('t5',u"гор 206"),
    ('t6',u"гор 506"),
    ('t7',u"давление 401"),
    ('t8',u"разр 502"),
    ('t9',u"разр 602"),
    ('t10',u"M201"),
    ('t11',u"M202"),
    ('t12',u"M203"),
    ('t13',u"M304"),
    ('t14',u"M205"),
    ('t15',u"M206"),
    ('t16',u"M207"),
    ('t17',u"M208"),
        )

    avg_c =(
        ('minutes','Минутам'),
        ('hours','Часам'),
        ('days','Дням'),
    )
    
    aggregate = forms.ChoiceField(choices=value_c,label=u'Значения')
    interval = forms.ChoiceField(choices=avg_c,label=u'Усреднять',required=False)
    start = forms.DateTimeField(required=False, label=u'Начало отсчета')
    end = forms.DateTimeField(required=False, label=u'Конец отсчета')
    