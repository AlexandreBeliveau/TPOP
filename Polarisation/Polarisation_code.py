import matplotlib.pyplot as mpl
from math import cos
import scipy
import numpy as np

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

#mpl.plot(Angle, Courant_TM, "o", label = 'Polarisation TM', color = 'blue')
#mpl.plot(Angle, Courant_TE, "o", label = 'Polarisation TE', color = 'red')
#mpl.xlabel("Angle d'incidence (°)")      # titre des abscisses
#mpl.ylabel("Courant proportionnel à l'intensité lumineuse (μA)")      # titre des ordonnées
#mpl.legend()
#mpl.show()

#D) Vérification de la loi de Malus

Angle = [0,
10,
20,
30,
40,
50,
60,
70,
80,
90,
100,
110,
120,
130,
140,
150,
160,
170,
180
]

Courant = [186,
202, 
206,
197,
176,
146,
110,
75,
44.5,
19.5,
4.5,
1.6,
12.5,
31.5,
60,
96,
136,
168,
195]

def Malus(theta, I_0, delta_theta):
    theta_array = np.array(theta)
    return I_0 * np.cos(np.radians(theta_array - delta_theta))**2

# Courbe de tendance avec décalage
parametres, covariance = scipy.optimize.curve_fit(Malus, Angle, Courant, p0=[100, 0])  # p0=[100, 0] est un point de départ pour les paramètres
print(parametres)
mpl.rcParams.update({'font.size': 24})
mpl.plot(Angle, Courant, "bo", markersize=10, label='Données')  # Plot Données
mpl.plot(Angle, Malus(Angle, *parametres), color='red', label='Courbe de tendance')  # Plot courbe de tendance
mpl.xlabel("Angle du prisme de Glan-Thompson (°)")  # titre des abscisses
mpl.ylabel("Courant proportionnel à l'intensité lumineuse (μA)")  # titre des ordonnées
# Ajout de la boîte de texte
texte = "I(θ) = 207.80092645 cos^2(θ - 16.89594484) "
mpl.text(122, max(Courant), texte, bbox=dict(facecolor='white', alpha=0.5), ha='center')
mpl.legend()
mpl.show()