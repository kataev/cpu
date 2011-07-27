# -*- coding: utf-8 -*-
from cpu.bkz.models import dvt21,dvt22
import matplotlib.pyplot as plt

a = dvt21.objects.order_by('date').values_list('temp').reverse().all()[:1000]

#a = a[:-10]

plt.plot(range(len(a)),a)
plt.show()




