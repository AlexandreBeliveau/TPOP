import numpy as np
import matplotlib.pyplot as plt
import scipy

Cellule = np.array([0.768, 26.0, 53.0, 77.7, 102, 128, 153, 178, 203, 227, 252, 275, 300])
Detecteur = np.array([6.7, 8.18, 10.9, 12.7, 16.1, 19.9, 23.1, 25.7, 28.2, 31, 32, 32.6, 32.2])
Detecteur = Detecteur/ np.max(np.abs(Detecteur))
Erreurs_detecteur = []
for i in Detecteur:
    Erreurs_detecteur.append((i)/100)
Erreurs_cellule = np.array([0.1 , 1.1 , 2.5, 4.4, 5, 4.5, 5.6, 4.2, 5.6, 6.4, 6.8, 6.8, 6.8])
# Relation linéaire
def f(x, a, b):
    x_array = np.array(x)
    return a * x_array + b

def phi(V, V_pi):
    return V * np.pi/V_pi

def intensité(V, I_i, V_pi, A,B):
    return I_i/2*(1-np.cos(phi(V, V_pi))+B) + A

# Fit des données linéaire
paramètres_1, covariance_1 = scipy.optimize.curve_fit(f, Cellule[4:8], Detecteur[4:8])
# Fit des données cos
paramètres_2, covariance_2 = scipy.optimize.curve_fit(intensité, Cellule, Detecteur)

plt.errorbar(Cellule, Detecteur, xerr=Erreurs_cellule, yerr=Erreurs_detecteur, fmt='o', color='blue', capsize=5, label='Données expérimentales')
plt.plot(Cellule[2:9], f(Cellule[2:9], *paramètres_1), color='red', label='Plage linéaire')
#plt.plot(Cellule, intensité(Cellule, *paramètres_2),'o', color='red', label='Courbe de tendance')
plt.xlabel('Tension aux bornes de la cellule [V]', fontsize=16)
plt.ylabel('Signal normalisé du détecteur [-]', fontsize=16)
plt.legend(fontsize=14)
plt.show()