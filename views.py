# -*- coding: utf-8 -*-
from cpu.bkz.models import *
from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import render
from bkz.forms import ChartForm
import qsstats
from django.db.models import Avg
import datetime

def data(request,model):
    form = ChartForm(request.GET)
    if form.is_valid():
        queryset = model.objects.all()
        print form.cleaned_data
        qss = qsstats.QuerySetStats(queryset,'date')
        start = form.cleaned_data['start'] or datetime.date.today()
        end = form.cleaned_data['end'] or datetime.datetime.now()
        interval = form.cleaned_data['interval'] or 'hours'
        aggregate = form.cleaned_data['aggregate']

        s = map(lambda x: [x[0].isoformat(),x[1]],qss.time_series(start,end,aggregate=Avg(aggregate),interval=interval))

        return HttpResponse(simplejson.dumps(s))
    else:
        return HttpResponse(simplejson.dumps(form.errors))

def last(request):
    data = (dvt21.objects.latest('pk'),dvt22.objects.latest('pk'),termodat22m.objects.latest('pk'))
    data = map(lambda x: x.show(),data)
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')


def main(request):
    pos = {}
    for p in Positions.objects.all():
        d = pos.get(p.name,{})
        d[p.field] = dict(place = p.get_place_display(), pos = p.position)
        pos[p.name]=d

    data = (dvt21.objects.latest('pk'),dvt22.objects.latest('pk'),termodat22m.objects.latest('pk'))
    data = map(lambda x: x.show(),data)
    return render(request,'main.html',{'pos':simplejson.dumps(pos),'data':simplejson.dumps(data)})

def chart(request):
    return render(request, 'chart.html',{'form':ChartForm()})
