import matplotlib.pyplot as mpl

#A) Polarisation par réflexion

#Polarisation TM
Angle = [10,
15,
20,
25,
30,
35,
40,
45,
50,
55,
60,
65,
70,
75,
80]

Courant_TM = [18.2,
17.3,
15.8,
14.1,
12.2,
10.0,
7.6,
5.4,
3.5,
3.0,
5.2,
12.0,
28.6,
50,
98]

#Polarisation TE
Courant_TE = [13.5,
13.3,
16.1,
18.7,
19.9,
24.1,
28.4,
43.0,
51.1,
65.4,
77.2,
98.7,
134,
174,
251
]

mpl.plot(Angle, Courant_TM, "o", label = 'Polarisation TM', color = 'blue')
mpl.plot(Angle, Courant_TE, "o", label = 'Polarisation TE', color = 'red')
mpl.xlabel("Angle d'incidence (°)")      # titre des abscisses
mpl.ylabel("Courant proportionnel à l'intensité lumineuse (μA)")      # titre des ordonnées
mpl.legend()
mpl.show()