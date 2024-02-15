import matplotlib.pyplot as mpl
from math import sin
import scipy
import numpy as np

data1 = np.genfromtxt("C:\\Users\\ameli\\OneDrive\\Documents\\Amélie\\Université\\Session 4 Hiver 2024\\Travaux pratiques d'optique photonique\\TPOP\\Diffraction\\Données_fente_double_1.csv", delimiter=',')
data2 = np.genfromtxt("C:\\Users\\ameli\\OneDrive\\Documents\\Amélie\\Université\\Session 4 Hiver 2024\\Travaux pratiques d'optique photonique\\TPOP\\Diffraction\\Données_fente_double_2.csv", delimiter=',')
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
mpl.plot(Position_2, Intensité_2, label = 'Données', color = 'red')
#mpl.plot(Position, sinc(Position, *parametres), color='red', label='Courbe de tendance') 
mpl.xlabel("Position [cm]")      # titre des abscisses
mpl.ylabel("Gray Value [-]")      # titre des ordonnées
#mpl.legend()
mpl.show()