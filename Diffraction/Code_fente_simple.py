import matplotlib.pyplot as mpl
from math import atan, asin
import scipy
import numpy as np

data1 = np.genfromtxt("C:\\Users\\ameli\\OneDrive\\Documents\\Amélie\\Université\\Session 4 Hiver 2024\\Travaux pratiques d'optique photonique\\TPOP\\Diffraction\\Données_fente_simple.csv", delimiter=',')
d_ecran = 65 #distance entre la fente et l'écran en cm

Position = []
Intensité = []

for couple in data1:
    Position.append(couple[0])
    Intensité.append(couple[1])

def sinc(x, A, B, C):
    x_array = np.array(x)
    return A * np.sin(np.pi * B * x_array) / (np.pi * B * x_array) + C

# Courbe de tendance
#parametres, covariance = scipy.optimize.curve_fit(sinc, Position, Intensité) 
#print(parametres)

mpl.plot(Position, Intensité, label = 'Données', color = 'blue')
#mpl.plot(Position, sinc(Position, *parametres), color='red', label='Courbe de tendance') 
mpl.xlabel("Position [cm]")      # titre des abscisses
mpl.ylabel("Gray Value [-]")      # titre des ordonnées
#mpl.legend()
mpl.show()

#Trouver la position des minimums par rapport au centre
pos_min = []
#minimum1
index_min1 = Intensité.index(min(Intensité[40:86]))
pos_min.append(Position[index_min1])

#minimum2
index_min2 = Intensité.index(min(Intensité[86:151]))
pos_min.append(Position[index_min2])

#minimum3
index_min3 = Intensité.index(min(Intensité[151:214]))
pos_min.append(Position[index_min3])

#minimum4
index_min4 = Intensité.index(min(Intensité[214:270]))
pos_min.append(Position[index_min4])
print(pos_min)
#centre
pos_centre = (Position[index_min3] - Position[index_min2])/2 + Position[index_min2]
print(pos_centre)
#Theta
theta = []

for x in pos_min:
    d_min = x - pos_centre
    theta.append(atan(d_min/d_ecran))

m = [-2,-1,1,2]

a =  np.array(m) * 650 / np.sin(theta)

print(a.mean())