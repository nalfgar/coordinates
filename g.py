 #!pythona
# -*- coding: utf-8 -*-

import math
import geo_n as geo

p = [147,55,23]
p = [360,00,00]
l = [7,10,31]
p=geo.d2r(p)
l=geo.d2r(l)
k=p-l

print geo.dd2d(geo.r2d(k))

