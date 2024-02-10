import numpy as np
import matplotlib.pyplot as mpl
from statistics import mean, stdev

Temps = []
Tension = []

data = np.genfromtxt('F0000CH2.csv', delimiter=',') #data pas moyenné par oscilloscope

for couple in data:
    Temps.append(couple[0])
    Tension.append(couple[1])

high = []
low = []

# Séparer les deux états (SYNC LOW, SYNC HIGH) en listes (on ne prend que les temps)
for couple in data1:
    if couple[1] > 3.35:
        high.append(couple[0])

    elif couple[1] < 3.34:
        low.append(couple[0])


mpl.plot(Temps, Tension, label = 'Pas moyenné')
mpl.show()