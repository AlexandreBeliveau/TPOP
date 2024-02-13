import numpy as np
import matplotlib.pyplot as mpl
from statistics import mean, stdev

Temps = []
Tension = []

data = np.genfromtxt('Bruit\F0000CH2.CSV', delimiter=',') #data pas moyenné par oscilloscope

for couple in data:
    Temps.append(couple[0])
    Tension.append(couple[1])

high = []
low = []

# Séparer les deux états (SYNC LOW, SYNC HIGH) en listes (on ne prend que les temps)
for couple in data:
    if couple[1] > 3.30:
        high.append(couple[0])

    elif couple[1] < 3.29:
        low.append(couple[0])


mpl.plot(Temps, Tension, label = 'Pas moyenné')
mpl.show()

# Trouver l'intervalle de temps qui explicite le début et la fin d'un même SYNC
def intervalle(sets):
    # Liste qui contient le début et la fin d'un même SYNC
    list_inter = []
    # Valeur qui garde en mémoire le temps précédent
    basetemps = sets[0]
    # Valeur qui garde en mémoire le début d'un SYNC
    baseinter = sets[0]

    # On itère en comparent un élément avec le prochain, si la différence est trop grande, on sait qu'un SYNC vient de se finir
    # on l'ajoute dans la liste.
    for temps in sets[1: ]:
        if temps-basetemps > 0.05:
            list_inter.append([baseinter, basetemps])
            baseinter = temps
        basetemps = temps
    list_inter.append([baseinter, basetemps])
    return list_inter

interhigh = intervalle(high)
interlow = intervalle(low)

# On trouve l'index associé au temps des intervalles
def find_index(list_inter):
    index_inter = []
    for inter in list_inter:
        begin, end = Temps.index(inter[0]), Temps.index(inter[1])
        index_inter.append([begin, end])
    return index_inter
indice_high = find_index(interhigh)
indice_low = find_index(interlow)

print(indice_high)
print(interlow)

#moyenne du signal HIGH
tension_high =[]
for i in Tension[indice_high[1][0]: indice_high[1][1]]:
    tension_high.append(i)
#print(mean(tension_high))

#moyenne du signal LOW
tension_low =[]
for i in Tension[indice_low[1][0]: indice_low[1][1]]:
    tension_low.append(i)
#print(mean(tension_low))
print(stdev(tension_high)*100)

Signal_moyen = (mean(tension_high)-mean(tension_low))/mean(tension_low) * 100
print(Signal_moyen)
