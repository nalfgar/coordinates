#!/usr/bin/env python
"""Skrypt pomaga przeliczac wspolrzedne punktow

pomiedzy ukladami wspolrzednych wystepujacych na
terenie Polski"""

#Dane RCS-a
__version__ = "$Id: uu_n.py,v 1.8 2003/03/25 18:11:45 darek Exp darek $"[15:18]

import math
import geo_n
#Deklaracje elipsoid
G = geo_n.elipsoida("GRS")
K = geo_n.elipsoida("Krasowski")
#deklarace ukladow
#Elipsoida GRS-80
_1992 = geo_n.uklad("1992")
_2000_15 = geo_n.uklad("2000/15")
_2000_18 = geo_n.uklad("2000/18")
_2000_21 = geo_n.uklad("2000/21")
_2000_24 = geo_n.uklad("2000/24")

#Elipsoida Krasowskiego
_1965_1 = geo_n.uklad("1965/1")
_1965_2 = geo_n.uklad("1965/2")
_1965_3 = geo_n.uklad("1965/3")
_1965_4 = geo_n.uklad("1965/4")
_1965_5 = geo_n.uklad("1965/5")
_1942_15 = geo_n.uklad("1942/15")
_1942_18 = geo_n.uklad("1942/18")
_1942_21 = geo_n.uklad("1942/21")
_1942_24 = geo_n.uklad("1942/24")
_1942_15_6 = geo_n.uklad("1942/15/6")
_1942_21_6 = geo_n.uklad("1942/21/6")
_GUGIK_80 = geo_n.uklad("GUGIK-80")

class punkt_xyz:
	def __init__(self, nr, x, y, z=0.0):
		self.nr = str(nr)
		self.x = x
		self.y = y
		self.z = z
	def __str__(self):
		return `self.nr, self.x, self.y, self.z`
	def __repr__(self):
		return `self.nr, self.x, self.y, self.z`
	def __sub__(self, other):
		dx = self.x - other.x
		dy = self.y - other.y
		dz = self.z - other.z
		return (dx, dy, dz)
	
class punkt_blh:
	def __init__(self, nr, b, l, h):
		self.nr = str(nr)
		if type(b) == type(()) or type(b) ==type([]):
			self.b = geo_n.d2dd(b)
		elif type(b) == type(0.0):
			self.b = b
		else: print "uu_n.punkt_blh.b - parametrem moze byc\
		trzyelementowa kolejka badz lista, liczba rzeczywista\
		lub liczba calkowita."
		if type(l) == type(()) or type(l) ==type([]):
			self.l = geo_n.d2dd(l)
		elif type(l) == type(0.0):
			self.l = l
		else: print "uu_n.punkt_blh.l - parametrem moze byc\
		trzyelementowa kolejka badz lista, liczba rzeczywista\
		lub liczba calkowita."
		self.h = h
	def __repr__(self):
		return `[self.b, self.l, self.h]`
	def __str__(self):
		return `[geo_n.dd2d(self.b), geo_n.dd2d(self.l), self.h]`
	def __sub__(self, other):
		db = self.b - other.b
		dl = self.l - other.l
		dh = self.h - other.h
		return (db, dl, dh)

def jeden_wprost(punktXYZ):
	x = (punktXYZ.x * G.c[0][0]) +\
		(punktXYZ.y * G.c[0][1]) +\
		(punktXYZ.z * G.c[0][2]) + G.t[0]
		
	y = (punktXYZ.x * G.c[1][0]) +\
		(punktXYZ.y * G.c[1][1]) +\
		(punktXYZ.z * G.c[1][2]) + G.t[1]
		
	z = (punktXYZ.x * G.c[2][0]) +\
		(punktXYZ.y * G.c[2][1]) +\
		(punktXYZ.z * G.c[2][2]) + G.t[2]		
	return punkt_xyz(punktXYZ.nr, x, y, z)

def jeden_wstecz(punktXYZ):
	x = (punktXYZ.x - G.t[0]) * K.d[0][0] +\
		(punktXYZ.y - G.t[1]) * K.d[0][1] +\
		(punktXYZ.z - G.t[2]) * K.d[0][2]
		
	y = (punktXYZ.x - G.t[0]) * K.d[1][0] +\
		(punktXYZ.y - G.t[1]) * K.d[1][1] +\
		(punktXYZ.z - G.t[2]) * K.d[1][2]
		
	z = (punktXYZ.x - G.t[0]) * K.d[2][0] +\
		(punktXYZ.y - G.t[1]) * K.d[2][1] +\
		(punktXYZ.z - G.t[2]) * K.d[2][2]
	return punkt_xyz(punktXYZ.nr, x, y, z)

def dwa_wprost(punktXYZ, elipsoida):
	r = math.sqrt((punktXYZ.x ** 2)+(punktXYZ.y ** 2))
	q0 = 0.0
	e = 1
	while e > 1e-9:
		b0 = math.atan((punktXYZ.z + q0) / r)
		Rn = elipsoida.a / math.sqrt(1 - (elipsoida.e ** 2) * (math.sin(b0) ** 2))
		q0 = Rn * (elipsoida.e ** 2) * math.sin(b0)
		b = math.atan((punktXYZ.z + q0) / r)
		e = b0 - b
		e = math.sqrt(e ** 2)
	l = math.acos(punktXYZ.x / r)
	dr = r - (Rn * math.cos(b))
	dz = punktXYZ.z - (Rn * (1 - (elipsoida.e ** 2)) * math.sin(b))
	h = math.sqrt((dr ** 2) + (dz ** 2))
	if dz < 0 or dr < 0: h = -1 * h
	b = geo_n.r2d(b)
	l = geo_n.r2d(l)
	return punkt_blh(punktXYZ.nr, b, l, h)

def dwa_wstecz(punktBLH, elipsoida):
	b = geo_n.d2r(punktBLH.b)
	l = geo_n.d2r(punktBLH.l)
	sin_b = math.sin(b)
	sin_l = math.sin(l)
	cos_b = math.cos(b)
	cos_l = math.cos(l)
	c = elipsoida.e * sin_b
	Rn = elipsoida.a / math.sqrt(1 - (elipsoida.e ** 2) * (sin_b ** 2))
	q = Rn * (elipsoida.e ** 2) * sin_b
	x = (Rn + punktBLH.h) * cos_b * cos_l
	y = (Rn + punktBLH.h) * cos_b * sin_l
	z = ((Rn + punktBLH.h) * sin_b) - q	
	return punkt_xyz(punktBLH.nr, x, y, z)

def trzy_wprost(punktBLH, elipsoida, uklad):
		# Przeksztalcenie Lagrange'a
		b = geo_n.d2r(punktBLH.b)		
		L0 = geo_n.d2r(uklad.L0)
		lamb = geo_n.d2r(punktBLH.l)
		d_lamb = lamb - L0
		U = 1 - elipsoida.e * math.sin(b)
		V = 1 + elipsoida.e * math.sin(b)
		K = (U / V) ** (elipsoida.e / 2)
		C = K * math.tan((b / 2) + (math.pi / 4))
		fi = (2 * math.atan(C)) - (math.pi / 2)
		Rn = elipsoida.a / math.sqrt(1 - (elipsoida.e ** 2) * (math.sin(b) ** 2))
		m1 = (elipsoida.R0 * math.cos(fi)) / (Rn * math.cos(b))
		gamma0 = 0.0
		gamma1 = 0.0
		
		# Przeksztalcenie Mercatora
		sin_fi = math.sin(fi)
		cos_fi = math.cos(fi)
		sin_lamb = math.sin(d_lamb)
		cos_lamb = math.cos(d_lamb)
		x_merc = math.atan(sin_fi / (cos_fi * cos_lamb))
		y_merc = 0.5 * math.log((1 + cos_fi * sin_lamb) / (1 - cos_fi * sin_lamb))
		m2 = 1 / (1 - (math.cos(fi) ** 2)* (math.sin(d_lamb) ** 2)) ** 0.5
		gamma2 = math.atan(sin_fi * math.tan(d_lamb))
		
		# Przeksztalcenie Gaussa-Krugera
		alfa, beta = x_merc, y_merc
		x_GK, y_GK, i = 0, 0, 0
		Cx, Cy = 1.0, 0.0
		for k in [2, 4, 6, 8]:
			sin_k = math.sin(k * alfa)
			cosh_k = math.cosh(k * beta)
			cos_k = math.cos(k * alfa)
			sinh_k = math.sinh(k * beta)
			x_GK = x_GK + elipsoida.GK_wprost[i] * sin_k * cosh_k
			y_GK = y_GK + elipsoida.GK_wprost[i] * cos_k * sinh_k
			Cx = Cx + k * elipsoida.GK_wprost[i] * cos_k * cosh_k
			Cy = Cy - k * elipsoida.GK_wprost[i] * sin_k * sinh_k
			i = i + 1
		x_GK = (elipsoida.R0 * (alfa + x_GK)) * uklad.m0 + uklad.x0
		y_GK = (elipsoida.R0 * (beta + y_GK)) * uklad.m0 + uklad.y0
		
		m3 = ((Cx ** 2) + (Cy ** 2)) ** 0.5
		gamma3 = -math.atan(Cy / Cx)
		gamma = gamma0 + gamma1 + gamma2 + gamma3
		gamma = geo_n.r2g(gamma)
		m = uklad.m0 * m1 * m2 *m3
		sigma = (m-1) * 10e4
		return (punktBLH.nr, x_GK, y_GK, sigma, gamma)

def trzy_wstecz(punktXYZ, elipsoida, uklad):
	# Przeksztalcenie Gaussa-Krugera (wstecz)
	alfa, beta, = 0.0, 0.0
	i = 0
	x_GK = (punktXYZ.x - uklad.x0) / uklad.m0
	y_GK = (punktXYZ.y - uklad.y0) / uklad.m0
	u = x_GK / elipsoida.R0
	v = y_GK / elipsoida.R0
	for k in [2,4,6,8]:
		sin_k = math.sin(k * u)
		cosh_k = math.cosh(k * v)
		cos_k = math.cos(k * u)
		sinh_k = math.sinh(k * v)
		alfa = alfa + elipsoida.GK_wstecz[i] * sin_k * cosh_k
		beta = beta + elipsoida.GK_wstecz[i] * cos_k * sinh_k
		i = i + 1
	alfa = u + alfa
	beta = v + beta

	# Przeksztalcenie Mercatora (wstecz)
	w = (2 * math.atan(math.exp(beta))) - (math.pi / 2.0)
	fi = math.asin(math.cos(w) * math.sin(alfa))
	d_lamb = math.atan(math.tan(w) / math.cos(alfa))

	# Przeksztalcenie Lagrange'a (wstecz)
	i, sum = 0, 0
	for k in [2,4,6,8]:
		sum = sum + elipsoida.Lagr_wstecz[i] * math.sin(k * fi)
		i = i + 1
	B = fi + sum
	lamb = d_lamb + geo_n.d2r(uklad.L0)

	return (punktXYZ.nr, B, lamb)

## xyz_1 = punkt_xyz('1',5592239.0600,7486359.4600)
## xyz_2 = jeden_wprost(xyz_1)
## xyz_3 = jeden_wstecz(xyz_2)
## print xyz_1
## print xyz_2
## print xyz_3

xyz_10 = punkt_xyz('10rodi',3795648.263 ,1424998.552 ,4907610.202)
xyz_20 = punkt_xyz('20rodi',3795504.349 ,1425027.854 ,4907720.756)
xyz_30 = punkt_xyz('30rodi',3795755.557 ,1424985.91  ,4907520.713 )


print dwa_wprost(xyz_30, G)
print geo_n.d2dd((50, 37, 35.4211908576832)), geo_n.d2dd((20, 34, 36.91036680186443))
