# -*- coding: utf-8 -*-
from django.db import models
import dojango.forms as forms
from dojango.data.modelstore import  *
from django.db.models.loading import get_models

class relsib(models.Model):
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True)
    hmdt = models.FloatField(verbose_name="Влажность", null=True)
    temp = models.FloatField(verbose_name="Температура", null=True)

    def __unicode__(self):
        return self._meta.module_name

    def show(self):
        return {'date':self.date.isoformat(),'hmdt':self.hmdt,'temp':self.temp,'model':self._meta.module_name}

    class Meta:
        abstract = True
        ordering = ('-date')

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

    t10 = models.FloatField(verbose_name=u"M201", null=True)
    t11 = models.FloatField(verbose_name=u"M202", null=True)
    t12 = models.FloatField(verbose_name=u"M203", null=True)

    t13 = models.FloatField(verbose_name=u"M204", null=True)
    t14 = models.FloatField(verbose_name=u"M205", null=True)
    t15 = models.FloatField(verbose_name=u"M206", null=True)
    t16 = models.FloatField(verbose_name=u"M207", null=True)
    t17 = models.FloatField(verbose_name=u"M208", null=True)
    t18 = models.FloatField(verbose_name=u"", null=True)
    t19 = models.FloatField(verbose_name=u"", null=True)
    t20 = models.FloatField(verbose_name=u"", null=True)
    t21 = models.FloatField(verbose_name=u"", null=True)
    t22 = models.FloatField(verbose_name=u"", null=True)
    t23 = models.FloatField(verbose_name=u"", null=True)
    t24 = models.FloatField(verbose_name=u"", null=True)

    def __unicode__(self):
        return self._meta.module_name

    def show(self):
        d = {}
        for t in range(1,24):
            d['t%d' % t] = getattr(self,'t%d' % t)
        d['date'] = self.date.isoformat()
        d['model'] = self._meta.module_name
        return d

places = (
    (u'firing',u'Обжиг'),
    (u'drying_1',u'Сушка 1'),
    (u'drying_2',u'Сушка 2'),
)


devices = map(lambda m: (m._meta.module_name,m._meta.verbose_name,),filter(lambda m: m._meta.app_label in 'bkz',get_models()))

class Positions(models.Model):
    name = models.CharField(u'Имя устойства',max_length=100,choices=devices,)
    field = models.CharField(u'Канал устойства',max_length=100,null=True,blank=True)
    place = models.CharField(u'Раположение',max_length=50,choices=places,null=True,blank=True)
    position = models.CharField(u'Позиция',max_length=100)

    def show(self):
        return dict(field=self.field,place=self.get_place_display(),position=self.position)

    class Meta:
        verbose_name=u'позиция точек и датчиков'
        verbose_name_plural=u'позиции точек и датчиков'

    def __unicode__(self):
        if self.field:
            name = u'%s %s' % (self.get_name_display(),self.field)
        else:
            name = self.get_name_display()
        if self.place:
            return u'%s в %s %s' % (name,self.get_place_display(),self.position)
        else:
            return u'%s %s' % (name,self.position)
