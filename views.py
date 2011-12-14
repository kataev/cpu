# -*- coding: utf-8 -*-
from cpu.bkz.models import *
from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import render
from bkz.forms import ChartForm
import qsstats
from django.db.models import Avg
import datetime
from django.db.models.loading import get_models,get_model

def data(request):
    form = ChartForm(request.GET)
    if form.is_valid():
        model = get_model('bkz',form.cleaned_data['model'])
        queryset = model.objects.all()
        qss = qsstats.QuerySetStats(queryset,'date')
        start = form.cleaned_data['start'] or datetime.date.today()
        end = form.cleaned_data['end'] or datetime.datetime.now()
        interval = form.cleaned_data['interval'] or 'hours'
        aggregate = form.cleaned_data['aggregate']

        s = map(lambda x: dict(date=x[0].strftime('%s'),value=x[1]),qss.time_series(start,end,aggregate=Avg(aggregate),interval=interval))

        return HttpResponse(simplejson.dumps(s))
    else:
        return HttpResponse(simplejson.dumps(form.errors))

def last(request):
    data = []
    for m in (dvt21.objects.latest('pk'),dvt22.objects.latest('pk'),termodat22m.objects.latest('pk')):
        for f in m._meta.fields:
            if f.name in ('date','id'): continue
            if getattr(m,f.name):
                data.append(dict(value=getattr(m,f.name),id='%s_%s' % (m._meta.module_name,f.name)))

    return HttpResponse(simplejson.dumps(data), mimetype='application/json')


def main(request):
    pos = {}
    for p in Positions.objects.all():
        d = pos.get(p.name,{})
        d[p.field] = dict(place = p.get_place_display(), pos = p.position,p=p.place)
        pos[p.name]=d
    models = map(lambda m: m,filter(lambda m: m._meta.app_label in 'bkz' and m._meta.module_name != 'positions',get_models()))

    data = []

    start = datetime.datetime.now() - datetime.timedelta(0,0,0,0,10)
    end = datetime.datetime.now() - datetime.timedelta(0,0,0,0,1)
    s = """where date >= '%s' and date <= '%s' """ % (start.isoformat(),end.isoformat())

    q = dict(termodat22m=termodat22m.objects.raw("SELECT min(id) as id,min(date) as date,avg(t1) as t1,avg(t2) as t2,avg(t3) as t3,avg(t4) as t4,avg(t5) as t5,avg(t6) as t6,avg(t7) as t7,avg(t8) as t8,avg(t9) as t9,avg(t10) as t10,avg(t11) as t11,avg(t12) as t12,avg(t13) as t13,avg(t14) as t14,avg(t15) as t15,avg(t16) as t16,avg(t17) as t17,avg(t18) as t18,avg(t19) as t19,avg(t20) as t02,avg(t21) as t21,avg(t22) as t22,avg(t23) as t23,avg(t24) as t24 from bkz_%s %s group by date_trunc('%s',date) ORDER BY id DESC limit %s;" % ('termodat22m',s,'minutes',10)))

    for mo in (dvt21,dvt22):
        q[mo._meta.module_name] = mo.objects.raw("SELECT min(id) as id,min(date) as date,avg(hmdt) as hmdt,avg(temp) as temp from bkz_%s %s group by date_trunc('minutes',date) ORDER BY id DESC limit 10;" % (mo._meta.module_name,s))

    for m in models:
        obj = m.objects.latest('pk')
        for f in m._meta.fields:
            if f.name in ('date','id'): continue
            query = map(lambda m: getattr(m,f.name),q[m._meta.module_name])
            if getattr(obj,f.name):
                data.append(dict(value=getattr(obj,f.name),id='%s_%s' % (m._meta.module_name,f.name),query=query))

    return render(request,'main.html',{'pos':simplejson.dumps(pos),'data':simplejson.dumps(data),'form':ChartForm()})

def chart(request):
    return render(request, 'chart.html',{'form':ChartForm()})
