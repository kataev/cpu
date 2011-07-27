# -*- coding: utf-8 -*-
from cpu.bkz.models import *
from cpu.bkz import models
from cjson import encode as json
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template.loader import render_to_string
from django.core import serializers
from django.db.models.loading import get_models, get_app

def store(request,model):
    try:
        store = getattr(models,model+'Store')()
#    print store
        store._meta.objects = getattr(models,model).objects.order_by('date').reverse().all()[:50]
        return HttpResponse(store.to_json(), mimetype='application/json; charset=utf-8;')
    except :
        return HttpResponse(json({'status':False}), mimetype='application/json; charset=utf-8;')


def show(request,model):
    try:
        store = getattr(models,model+'Store')()
#    store._meta.objects = [getattr(models,model).objects.latest('date')]
        store.set_option('label1', 'custom_label_field')
        return HttpResponse(store.to_json(), mimetype='application/json; charset=utf-8;')
    except :
        return HttpResponse(json({'status':False}), mimetype='application/json; charset=utf-8;')

def store_avg(request,model,time,limit):
    if model in ['dvt21','dvt22']:
        try:
            store = getattr(models,model+'Store')()
            store._meta.objects = getattr(models,model).objects.raw("SELECT min(id) as id,min(date) as date,avg(hmdt) as hmdt,avg(temp) as temp from bkz_%s group by date_trunc('%s',date) ORDER BY id DESC limit %s;" % (model,time,limit))
            return HttpResponse(store.to_json(), mimetype='application/json; charset=utf-8;')
        except :
            return HttpResponse(json({'status':False}), mimetype='application/json; charset=utf-8;')
    else:
        try:
            store = getattr(models,model+'Store')()
            store._meta.objects = getattr(models,model).objects.raw("SELECT min(id) as id,min(date) as date,avg(t1) as t1,avg(t2) as t2,avg(t3) as t3,avg(t4) as t4,avg(t5) as t5,avg(t6) as t6,avg(t7) as t7,avg(t8) as t8,avg(t9) as t9,avg(t10) as t10,avg(t11) as t11,avg(t12) as t12,avg(t13) as t13,avg(t14) as t14,avg(t15) as t15,avg(t16) as t16,avg(t17) as t17,avg(t18) as t18,avg(t19) as t19,avg(t20) as t02,avg(t21) as t21,avg(t22) as t22,avg(t23) as t23,avg(t24) as t24 from bkz_%s group by date_trunc('%s',date) ORDER BY id DESC limit %s;" % (model,time,limit))
            return HttpResponse(store.to_json(), mimetype='application/json; charset=utf-8;')
        except :
            return HttpResponse(json({'status':False}), mimetype='application/json; charset=utf-8;')


def last(request):
    list = [dvt21,dvt22,termodat22m]

    j = []
    try:
        for a in list:
            print len(j),a,a.objects.latest('date')
            j.append(a.objects.latest('date'))
    except :
        pass

    return HttpResponse(serializers.serialize('json',j), mimetype='application/json')


def main(request):
    a= {'termodat':[{'model':termodat22m,'fields':termodat22m._meta.fields[2:]}],'dvt':[dvt22,dvt21,]}
    re=render_to_string('main.html',a)
    return HttpResponse(re,mimetype="text/html; charset=utf-8;")

def show_chart(request):
    j = [{'value':'temp','label':'Температура'},{'value':'hmdt','label':'Влажность'}]

    for a in termodat22m._meta.fields:
        if a.name in ['id','date']:
            continue
        if len(a.verbose_name)==0:
            continue
        j.append({'value':a.name,'label':a.verbose_name})

    print j
    re=render_to_string('chart.html',{'models':get_models(get_app('bkz')),'options':j})
    return HttpResponse(re,mimetype="text/html; charset=utf-8;")

def show_dvt_to_chart(request):

    query=[dvt21,dvt22]
    response=[]

    def g(obj,o):
        return getattr(obj,o)



    for c in query:
        cur={'identifier':'id','items':[],'fields':[],'name':c._meta.verbose_name,'position':c.position}
        for a in c._meta.fields:
            cur['fields'].append({'field':a.name,'name':a.verbose_name,'width':'10px'})

        t = c.objects.order_by('date').reverse().all()[:2000]
        delta=  (t[0].date - t[1999].date)
        items=[]
        for i in range(len(t)-1):
            q={}
            q['date']=str(t[i].date)
            q['id']=i+1

            for a in ['temp','hmdt']:
                if i == 0:
                    q[a]=3 * g(t[i],a) + 2 * g(t[i+1],a) + g(t[i+2],a) - g(t[i+3],a)
                    q[a]/=5

                if i == 1:
                    q[a]=4 * g(t[i],a) + 3 * g(t[i+1],a) + 2 * g(t[i+2],a) + g(t[i+3],a)
                    q[a]/=10

                if i >= 2 and i<=len(t)-3:
                    q[a]=items[i-2][a] + items[i-1][a] + g(t[i],a) + g(t[i+1],a) + g(t[i+2],a)
                    q[a]/=5
                if i<=len(t)-2:
                    continue
            items.append(q)


        cur['items']=items
        response.append(cur)
        response.append(str(delta))
        
    return HttpResponse(json(response),mimetype="application/json; charset=utf-8;")
