import matplotlib.pyplot as mpl
from math import sin
import scipy
import numpy as np

data1 = np.genfromtxt("C:\\Users\\ameli\\OneDrive\\Documents\\Amélie\\Université\\Session 4 Hiver 2024\\Travaux pratiques d'optique photonique\\TPOP\\Diffraction\\Données_holes.csv", delimiter=',')

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
mpl.ylabel("Valeur de gris [-]")      # titre des ordonnées
#mpl.legend()
mpl.show()