# -*- coding: utf-8 -*-
from django.db import models
import dojango.forms as forms
from dojango.data.modelstore import  *


class relsib(models.Model):
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    hmdt = models.FloatField(verbose_name="Влажность", null=True)
    temp = models.FloatField(verbose_name="Температура", null=True)

    def get_hmdt(self):
        return {'x': self.position, 'y': self.hmdt}

    def get_temp(self):
        return {'x': self.position, 'y': self.temp}

    def show(self):
        return {'date': str(self.date), 'hmdt': self.hmdt, 'temp': self.temp, 'position': self.position}

    def get_full_info(self):
        return {'date': self.date, 'hmdt': self.hmdt, 'temp': self.temp}

    def get_position(self):
        return self.position

    class Meta:
        abstract = True

    def __unicode__(self):
        return self._meta.verbose_name


class dvt21(relsib):
    position = u'Камера 2 Позиция 9'
    class Meta:
        verbose_name = u'dvt21'


class dvt22(relsib):
    position = u'Камера 1 Позиция 9'
    class Meta:
        verbose_name = u'dvt22'


class termodat22m(models.Model):
    position = 'Термодат'

    date = models.DateTimeField(verbose_name="Дата", auto_now=True)
    t1 = models.FloatField(verbose_name=u"гор 703", null=True)
    t2 = models.FloatField(verbose_name=u"гор 704", null=True)
    t3 = models.FloatField(verbose_name=u"гор 306", null=True)
    t4 = models.FloatField(verbose_name=u"гор 606", null=True)
    t5 = models.FloatField(verbose_name=u"гор 206", null=True)
    t6 = models.FloatField(verbose_name=u"гор 506", null=True)
    t7 = models.FloatField(verbose_name=u"давл 401", null=True)
    t8 = models.FloatField(verbose_name=u"разр 502", null=True)
    t9 = models.FloatField(verbose_name=u"разр 602", null=True)

    t10 = models.FloatField(verbose_name=u"", null=True)
    t11 = models.FloatField(verbose_name=u"", null=True)
    t12 = models.FloatField(verbose_name=u"", null=True)

    t13 = models.FloatField(verbose_name=u"", null=True)
    t14 = models.FloatField(verbose_name=u"", null=True)
    t15 = models.FloatField(verbose_name=u"", null=True)
    t16 = models.FloatField(verbose_name=u"", null=True)
    t17 = models.FloatField(verbose_name=u"", null=True)
    t18 = models.FloatField(verbose_name=u"", null=True)
    t19 = models.FloatField(verbose_name=u"", null=True)
    t20 = models.FloatField(verbose_name=u"", null=True)
    t21 = models.FloatField(verbose_name=u"", null=True)
    t22 = models.FloatField(verbose_name=u"", null=True)
    t23 = models.FloatField(verbose_name=u"", null=True)
    t24 = models.FloatField(verbose_name=u"", null=True)
    class Meta:
        verbose_name = 'termodat22m'

    def __unicode__(self):
        return self._meta.verbose_name


class chartform(forms.Form):
    model_c = (('dvt21', dvt21.position), ('dvt22', dvt22.position),
               ('termodat22m',u'Термодат'))
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
    ('t9',u"разр 602"),)
    avg_c =(
        ('minute','Минутам'),
        ('second','Секундам'),
        ('hour','Часам'),
        ('day','Дням'),
    )



    model = forms.ChoiceField(label=u'Датчик', choices=model_c,)
    value = forms.ChoiceField(choices=value_c,label=u'Значения, и горелки для термодата')
    avg = forms.ChoiceField(choices=avg_c,label=u'Усреднять по')
    limit = forms.IntegerField(initial=10,widget=forms.NumberSpinnerInput(attrs={'style': 'width:80px;', 'constraints': {'min': 1}}),label=u'Кол-во точек')
    date = forms.DateField(required=False, label=u'Начало отсчета(не обязательнo)')


class dvt21Store(Store):
    id=StoreField()
    date = StoreField(get_value=ValueMethod('strftime', '%Y-%m-%d %H:%M'))
    temp = StoreField()
    hmdt = StoreField()
#    position = StoreField(get_value=ObjectMethod('get_position'))

    class Meta(object):
        objects = [dvt21.objects.latest('id')]
#        objects = dvt21.objects.order_by('date').reverse().all()[:50]
        label = None

class dvt22Store(Store):
    id=StoreField()
    date = StoreField(get_value=ValueMethod('strftime', '%Y-%m-%d %H:%M'))
    temp = StoreField()
    hmdt = StoreField()
#    position = StoreField(get_value=ObjectMethod('get_position'))

    class Meta(object):
        objects = [dvt22.objects.latest('id')]
#        objects = dvt22.objects.order_by('date').reverse().all()[:50]
        label = None
class termodat22mStore(Store):
    id=StoreField()
    date = StoreField(get_value=ValueMethod('strftime', '%Y-%m-%d %H:%M'))
    t1=StoreField()
    t2=StoreField()
    t3=StoreField()
    t4=StoreField()
    t5=StoreField()
    t6=StoreField()
    t7=StoreField()
    t8=StoreField()
    t9=StoreField()
    t10=StoreField()
    t11=StoreField()
    t12=StoreField()
    t13=StoreField()
    t14=StoreField()
    t15=StoreField()
    t16=StoreField()
    t17=StoreField()
    t18=StoreField()
    t19=StoreField()
    t20=StoreField()
    t21=StoreField()
    t22=StoreField()
    t23=StoreField()
    t24=StoreField()

#    hmdt = StoreField()
#    position = StoreField(get_value=ObjectMethod('get_position'))

    class Meta(object):
        objects = [termodat22m.objects.latest('id')]
#        objects = termodat22m.objects.order_by('date').reverse().all()[:50]
        label=None
#        label = termodat22m._meta.verbose_name
