import numpy as np
import matplotlib.pyplot as mpl
from statistics import mean, stdev



Temps = []
Tension = []

data1 = np.genfromtxt('F0000CH2.csv', delimiter=',')
#print(data1)

for couple in data1:
    Temps.append(couple[0])
    Tension.append(couple[1])


high = []
low = []
# Séparer les deux états (SYNC LOW, SYNC HIGH) en listes (on me prend que les temps)
for couple in data1:
    if couple[1] > 3.31:
        high.append(couple[0])

    elif couple[1] < 3.26:
        low.append(couple[0])

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
print(interhigh, '\n', interlow)


# On trouve l'index associé au temps des intervalles
def find_index(list_inter):
    index_inter = []
    for inter in list_inter:
        begin, end = Temps.index(inter[0]), Temps.index(inter[1])
        index_inter.append([begin, end])
    return index_inter

### Ici on moyenne le bruit/on moyenne chaque expérience et on fait la moyenne, on va essayer de le réduire en l'annulant en l'additionnant 
# On calcule la moyenne des valeurs avec les indices des temps trouvés avec la fonctione intervalle et find_index
def moyenneSYNC(list_inter):
    index_inter = find_index(list_inter)
    list_mean = []
    for index in index_inter:
        list_mean.append(mean(Tension[index[0]: index[1]]))
    return mean(list_mean)

# On calcule l'écart type des valeurs avec les indices des temps trouvés avec la fonctione intervalle et find_index
def stdevSYNC(list_inter):
    index_inter = find_index(list_inter)
    list_mean = []
    for index in index_inter:
        list_mean.append(stdev(Tension[index[0]: index[1]]))
    return mean(list_mean)

# On calcule la moyenne des ratios signal/bruit avec les indices des temps trouvés avec la fonctione intervalle et find_index
def noise_on_signal(list_inter):
    index_inter = find_index(list_inter)
    list_nos = []
    for index in index_inter:
        list_nos.append(mean(Tension[index[0]: index[1]])/stdev(Tension[index[0]: index[1]]))
    return mean(list_nos)

# Méthode des valeurs extrêmes
def incertitude(list_inter):
    index_inter = find_index(list_inter)
    lis_value = []
    for index in index_inter:
        lis_value += Tension[index[0]: index[1]]
    return (max(lis_value)-min(lis_value))/2
moyenneSignal = moyenneSYNC(interhigh)-moyenneSYNC(interlow)
stDev_signal = stdevSYNC(interhigh)
bruithigh1 = ( moyenneSignal/stDev_signal)
incertitude_high1 = incertitude(interhigh)
incertitude_low1 = incertitude(interlow)
# bruithigh2 = noise_on_signal(interhigh)
# bruitlow2 = noise_on_signal(interlow)

print(bruithigh1,'\n', incertitude_high1, '\n', incertitude_low1, '\n', moyenneSignal, '\n', stDev_signal)

### On va additionner les expériences entre elles pour diminuer le bruit
def min_len_listoflist(inter_list):
    min = 0
    index_list = find_index(inter_list)
    for inter in index_list:
        if inter[1]-inter[0] > min:
            min = inter[1]-inter[0]
    return min


# def add_inter(inter_list):
#     min = min_len_listoflist(inter_list)
#     find_index(inter_list)
#     for inter
        

    




# mpl.plot(Temps, Tension)
# mpl.xlabel('Temps(s)')      # titre des abscisses
# mpl.ylabel('Tension(V)')      # titre des ordonnées
# mpl.show()
        

