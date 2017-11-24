#!/usr/bin/env python

"""Modul posiada funkcje potrzebme podczas obliczen geodezyjnych"""
import math

#Dane RCS-a
RCS_file = "$RCSfile: geo_n.py,v $"
__version__ = "$Id: geo_n.py,v 1.7 2003/03/25 17:37:22 darek Exp darek $"[16:19]

class elipsoida:
	"""Klasa definiuje paramerty elipsoid odniesienia."""
	def __init__(self, nazwa):
		"""Definicja elipoidy GRS-80"""
		if nazwa == "GRS" or nazwa == "GRS-80" or\
		nazwa == "WGS" or nazwa == "WGS-84" or\
		nazwa == "G" or nazwa == "W":
			self.nazwa = "WGS-84"
			self.a =   6378137.000000
			self.b =   6356752.314141
			self.e =   0.818191910428e-1
			self.f =   0.335281068118e-2
			self.R0 =  6367449.145778
			self.b2a = 0.996647189319
			self.n =   0.167922039463e-2
			self.e2 =  0.669438002290e-2
			self.ep =  0.820944381519e-1
			self.ep2 = 0.673949677548e-2
			self.c = ((1.00000084076440, 4.08960694e-6, 0.25613907e-6),
				(-4.08960650e-6, 1.00000084076292, -1.73888787e-6),
				(-0.25614618e-6, 1.73888682e-6, 1.00000084077125))
			self.t = (-33.4297, 146.5746, 76.2865)
			self.GK_wprost = (0.8377318247344e-3,
						0.7608527788826e-6,
						0.1197638019173e-8,
						0.2443376242510e-11)
			self.GK_wstecz = (-0.8377321681641e-3,
						-0.5905869626083e-7,
						-0.1673488904988e-9,
						-0.2167737805597e-12)
			self.Lagr_wstecz = (0.3356551485597e-2,
						0.6571873148459e-5,
						0.1764656426454e-7,
						0.5400482187760e-10)

			"""Definicja elipsoidy Krasowskiego"""
		elif nazwa == "Krasowski" or nazwa == "K" or\
		nazwa == "K-42":
			self.nazwa = "Krasowskiego"
			self.a = 6378245.00000
			self.b = 6356863.018778
			self.e = 0.818133340169e-1
			self.f = 0.335232986926e-2
			self.R0 = 6367558.497000
			self.b2a = 0.9966477670131
			self.n = 0.167897918066e-2
			self.e2 = 0.669342162297e-2
			self.ep = 0.820885218206e-1
			self.ep2 = 0.673852541468e-2
			self.d = ((0.99999915921952, -4.08959962e-6, -0.25614575e-6),
				(4.08960007e-6, 0.99999915921804, 1.73888389e-6),
				(0.25613864e-6, -1.73888494e-6, 0.99999915922637))
			self.GK_wprost = (0.8376117571403e-3,
						0.7606346141534e-6,
						0.1197122824063e-8,
						0.2441972616146e-11)
			self.GK_wstecz = (-0.8376121004223e-3,
						-0.5904168570212e-7,
						-0.1672768339465e-9,
						-0.2166492522990e-12)
			self.Lagr_wstecz = (0.3356069601754e-2,
						0.6569986331658e-5,
						0.1763896519657e-7,
						0.5397379816930e-10)
		else: print "Niezdefinowana elipsoida."
	def __str__(self):
			return `self.nazwa`
	def __repr__(self):
			return `self.nazwa`

class uklad:
	def __init__(self, nazwa):
		if nazwa == "1992" or nazwa == "92":
			self.m0 = 0.9993
			self.x0 = -5300000.0
			self.y0 = 500000.0
			self.L0 = (19,0,0.0)

		elif nazwa == "2000/15":
			self.m0 = 0.999923
			self.x0 = 0.0
			self.y0 = 5 * 1000000 + 500000.0
			self.L0 = (15,0,0.0)
		elif nazwa == "2000/18":
			self.m0 = 0.999923
			self.x0 = 0.0
			self.y0 = 6 * 1000000 + 500000.0
			self.L0 = (18,0,0.0)
		elif nazwa == "2000/21":
			self.m0 = 0.999923
			self.x0 = 0.0
			self.y0 = 7 * 1000000 + 500000.0
			self.L0 = (21,0,0.0)
		elif nazwa == "2000/24":
			self.m0 = 0.999923
			self.x0 = 0.0
			self.y0 = 8 * 1000000 + 500000.0
			self.L0 = (24,0,0.0)

		elif nazwa == "1942/15":
			self.m0 = 1.0
			self.L0 = (15, 0, 0.0)
		elif nazwa == "1942/18":
			self.m0 = 1.0
			self.L0 = (18, 0, 0.0)
		elif nazwa == "1942/21":
			self.m0 = 1.0
			self.L0 = (21, 0, 0.0)
		elif nazwa == "1942/24":
			self.m0 = 1.0
			self.L0 = (24, 0, 0.0)
		elif nazwa == "1942/15/6":
			self.m0 = 1.0
			self.L0 = (15, 0, 0.0)
		elif nazwa == "1942/21/6":
			self.m0 = 1.0
			self.L0 = (21, 0, 0.0)

		elif nazwa == "1965/1":
			self.m0 = 0.9998
			self.B0 = (50, 37, 30.0)
			self.L0 = (21, 5, 0.0)
		elif nazwa == "1965/2":
			self.m0 = 0.9998
			self.B0 = (53, 0, 7.0)
			self.L0 = (21, 30, 10.0)
		elif nazwa == "1965/3":
			self.m0 = 0.9998
			self.B0 = (53, 35, 0.0)
			self.L0 = (17, 0, 30.0)
		elif nazwa == "1965/4":
			self.m0 = 0.9998
			self.B0 = (51, 40, 15.0)
			self.L0 = (16, 40, 20.0)
		elif nazwa == "1965/5":
			self.m0 = 0.999983
			self.L0 = (18, 57, 30.0)
			self.x0 = -4700000.0
			self.y0 = 237000.0

		elif nazwa == "GUGIK-80":
			self.m0 = 0.9997142857
			self.B0 = (52, 10, 0.0)
			self.L0 = (19, 10, 0.0)
			self.x0 = 500000.0
			self.y0 = 500000.0

		else: print "Uklad niezdefiniowany, lub zla nazwa ukladu"


"""Funkcje do konwersji katow"""
def d2g(k):
	"""d2g(90.00) --> 100.0, Zamiena stopnie(w zapisie dziesietnym) na grady."""
	return k * (10/9.0)

def g2d(k):
	"""g2d(200.0) --> 180.0, Zmienia grady na stopnie."""
	return k * (9/10.0)

def g2r(k):
	"""Zamiena grady na radiany.
	g2r(100.0) --> 1.5707963267948968"""
	return k * (math.pi/200.0)

def r2d(k):
	"""Zamienia radiany na stopnie.
	r2d(1.5707963267948968) --> 90.0"""
	return k * (180.0/math.pi)

def r2g(k):
	"""Zamienia radiany na grady.
	r2g(1.5707963267948968) --> 100.0"""
	return k * (200.0/math.pi)

def d2dd(k):
	"""Zamienia stopnie w zapisie stopniowym na zapis dziesietny.
	d2dd([1, 1, 1.1]) --> 1.0169722222222222"""
	if type(k)==type([]) or type(k)==type(()):
		if len(k)==3:
			s = int(k[0])
			m = int(k[1])/60.0
			sek = int(k[2])/3600.0
			ss = (k[2]-int(k[2]))/3600.0
			return s+m+sek+ss
		elif len(k)==4:
			s = int(k[0])
			m = int(k[1])/60.0
			sek = int(k[2])/3600.0
			ss = (k[3]*10**-(len(str(k[3]))))/3600.0
			return s+m+sek+ss
		else: print "d2dd: Bledna ilosc elementow."
	else: print "d2dd: Bledny typ danych."

def dd2d(k):
	"""Zamienia stopnie w zapisie dziesietnym na zapis stopniowy.
	dd2d(1.0169722222222222) --> (1, 1, 1.1)"""
	if type(k)!=type(0) or type(k)!=type(0.0):
		s = int(k)
		r = k-s
		m = int(r*60)
		r = (r*60)-m
		ss = r*60
		return (s,m,ss)
	else: print "dd2d: Blad na wejsciu."

def d2r(k):
	"""Zamiena stopnie(w zapisie dziesietnym lub stopniowym) na radiany.
	d2r(90.0) --> 1.5707963267948966
	d2r([180,0,0.0]) --> 3.1415926535897931"""

	if type(k) == type(()) or type(k) == type([]):
		k = d2dd(k)
	elif type(k)==type(0) or type(k)==type(0.0):
		pass
	else:
		print 'Podales zle dane wejsciowe.\n\
		podaj liste lub kolejke np. [1,23,45.65]'
	return k * (math.pi/180.0)

def sec2sms(sekundy):
    """Zamiena sekundy na [stpnie, minuty, sekundy]"""
    if 0 <= sekundy < 60:
        stopnie = 0
        minuty = 0
        print stopnie,minuty,sekundy
    elif 60 <= sekundy < 3600 :
        stopnie = 0
        minuty = sekundy/60
        sekundy = sekundy - (minuty*60)
        print stopnie,minuty,sekundy
    elif sekundy >= 3600:
        stopnie = sekundy/3600
        sekundy = sekundy - (stopnie*3600)
        if 0 <= sekundy < 60:
            minuty = 0
            sekundy = sekundy
        elif 60 <= sekundy < 3600 :
            minuty = sekundy/60
            sekundy = sekundy - (minuty*60)
        print stopnie,minuty,sekundy

