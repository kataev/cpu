# -*- coding: utf-8 -*-
from cpu.bkz.models import *
from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import render
from bkz.forms import ChartForm
import qsstats
from django.db.models import Avg
import datetime

def positions(request):
    dvt = Positions.objects.filter(name__startswith='dvt')
    pos = {}
    pos['dvt'] = map(lambda p: {'name':p.name,'place':p.get_place_display(),'pos':p.position},dvt)
    ter = Positions.objects.filter(name__startswith='termodat')
    pos['termodat22m'] = map(lambda p: {'field':p.field,'place':p.get_place_display(),'pos':p.position},ter)
    pos['termodat22m'].sort(key=lambda x:int(x['field'].split('t')[1]))
    return HttpResponse(simplejson.dumps(pos))

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
    dvt = Positions.objects.filter(name__startswith='dvt').order_by('place')
    pos = {}
    pos['dvt'] = map(lambda p: {'name':p.name,'place':p.get_place_display(),'pos':p.position},dvt)
    ter = Positions.objects.filter(name__startswith='termodat')
    pos['termodat22m'] = map(lambda p: {'field':p.field,'place':p.get_place_display(),'pos':p.position},ter)
    pos['termodat22m'].sort(key=lambda x:int(x['field'].split('t')[1]))
    return render(request,'main.html',{'pos':pos})

def chart(request):
    return render(request, 'chart.html',{'form':ChartForm()})
