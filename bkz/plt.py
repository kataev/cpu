# -*- coding: utf-8 -*-
from cpu.bkz.models import dvt21,dvt22
import matplotlib.pyplot as plt

def show():
    query=[dvt22]#,dvt22]
    re={'hmdt':[],'temp':[]}

    def g(obj,o):
        return getattr(obj,o)

    for c in query:
        t = c.objects.order_by('date').reverse().all()[:1000]
        for i in range(len(t)-1):
            for a in ['temp','hmdt']:
		items=re[a]
                if i == 0:
                    q=3 * g(t[i],a) + 2 * g(t[i+1],a) + g(t[i+2],a) - g(t[i+3],a)
                    q/=5
                    print '0: %s' % t[i].date
                if i == 1:
                    q=4 * g(t[i],a) + 3 * g(t[i+1],a) + 2 * g(t[i+2],a) + g(t[i+3],a)
                    q/=10
                if i >= 2 and i<=len(t)-3:
	#	    print items
                    q=items[i-2] + items[i-1] + g(t[i],a) + g(t[i+1],a) + g(t[i+2],a)
                    q/=5
                    q=round(q,2)
#		    if g(t[i],a)>70:
#			q=g(t[i-2],a)
                if i<=len(t)-2:
#                    continue
                    re[a].append(q)
                else:
                    print 'last %s' % t[i].date
#                re['id'][a].append(g(t[i],'date'))
#	        print re

        #.append(cur)
    return re

re = show()
w = []
for q in range(len(re['hmdt'][:-10])):
    w.append([re['hmdt'][q],re['temp'][q]])
#a = re['hmdt'][:-10]
#a = [[1,2],[2,3]]
a = w
#print a
plt.plot(range(len(a)),a)
plt.show()




