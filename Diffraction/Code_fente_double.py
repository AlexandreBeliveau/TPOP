import matplotlib.pyplot as mpl
from math import atan
import scipy
import numpy as np

data1 = np.genfromtxt("C:\\Users\\ameli\\OneDrive\\Documents\\Amélie\\Université\\Session 4 Hiver 2024\\Travaux pratiques d'optique photonique\\TPOP\\Diffraction\\Données_fente_double_1.csv", delimiter=',')
data2 = np.genfromtxt("C:\\Users\\ameli\\OneDrive\\Documents\\Amélie\\Université\\Session 4 Hiver 2024\\Travaux pratiques d'optique photonique\\TPOP\\Diffraction\\Données_fente_double_2.csv", delimiter=',')
d_ecran = 65 #distance entre la fente et l'écran en cm
Position_1 = []
Intensité_1 = []

for couple in data1:
    Position_1.append(couple[0])
    Intensité_1.append(couple[1])

Position_2 = []
Intensité_2 = []

for couple in data2:
    Position_2.append(couple[0])
    Intensité_2.append(couple[1])

def sinc(x, A, B, C):
    x_array = np.array(x)
    return A * np.sin(np.pi * B * x_array) / (np.pi * B * x_array) + C

# Courbe de tendance
#parametres, covariance = scipy.optimize.curve_fit(sinc, Position, Intensité) 
#print(parametres)

mpl.plot(Position_1, Intensité_1, label = 'Données', color = 'blue')
#mpl.plot(Position_2, Intensité_2, label = 'Données', color = 'red')
#mpl.plot(Position, sinc(Position, *parametres), color='red', label='Courbe de tendance') 
mpl.xlabel("Position [cm]")      # titre des abscisses
mpl.ylabel("Gray Value [-]")      # titre des ordonnées
#mpl.legend()
mpl.show()

#Trouver la position des minimums par rapport au centre
pos_min = []
#minimum1
index_min1 = Intensité_1.index(min(Intensité_1[24:101]))
pos_min.append(Position_1[index_min1])

#minimum2
index_min2 = Intensité_1.index(min(Intensité_1[101:161]))
pos_min.append(Position_1[index_min2])

#minimum3
index_min3 = Intensité_1.index(min(Intensité_1[161:217]))
pos_min.append(Position_1[index_min3])

#minimum4
index_min4 = Intensité_1.index(min(Intensité_1[217:361]))
pos_min.append(Position_1[index_min4])

#minimum5
index_min5 = Intensité_1.index(min(Intensité_1[361:438]))
pos_min.append(Position_1[index_min5])

#minimum6
index_min6 = Intensité_1.index(min(Intensité_1[438:509]))
pos_min.append(Position_1[index_min6])


#centre
pos_centre = (Position_1[index_min4] - Position_1[index_min3])/2 + Position_1[index_min3]
print(pos_centre)
#Theta
theta = []

for x in pos_min:
    d_min = x - pos_centre
    theta.append(atan(d_min/d_ecran))

m = [-2.5,-1.5,-0.5,0.5,1.5,2.5]

a =  np.array(m) * 650 / np.sin(theta)

print(a.mean())