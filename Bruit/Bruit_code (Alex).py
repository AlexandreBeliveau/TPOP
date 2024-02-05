import numpy as np
import matplotlib.pyplot as mpl
from statistics import mean, stdev

Temps = []
Tension = []

Temps_2 = []
Tension_2 = []

data1 = np.genfromtxt('/Users/alexandrebeliveau/Code_TPOP/TPOP_Bruit_lab/TPOP/Bruit/F0001CH2_128.csv', delimiter=',')#data moyenné 128x par oscilloscope
data2 = np.genfromtxt('/Users/alexandrebeliveau/Code_TPOP/TPOP_Bruit_lab/TPOP/Bruit/F0000CH2.csv', delimiter=',')#data pas moyenné par oscilloscope
#print(data1)
#F0001CH2_128
for couple in data1:
    Temps.append(couple[0])
    Tension.append(couple[1])

for couple in data2:
    Temps_2.append(couple[0]+0.025)
    Tension_2.append(couple[1]+0.08)



high = []
low = []

# Séparer les deux états (SYNC LOW, SYNC HIGH) en listes (on ne prend que les temps)
for couple in data1:
    if couple[1] > 3.35:
        high.append(couple[0])

    elif couple[1] < 3.34:
        low.append(couple[0])

mpl.plot(Temps_2, Tension_2, label = 'Pas moyenné')#Afficher le graphique
mpl.plot(Temps, Tension, label = 'Moyenne de 128 expériences')

     # titre des ordonnées
#mpl.show()
        
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
#print(interhigh, '\n', interlow)


# On trouve l'index associé au temps des intervalles
def find_index(list_inter):
    index_inter = []
    for inter in list_inter:
        begin, end = Temps.index(inter[0]), Temps.index(inter[1])
        index_inter.append([begin, end])
    return index_inter
indice_high = find_index(interhigh)
indice_low = find_index(interlow)
#print(indice_low)
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


moyenneSignal = moyenneSYNC(interhigh)#-moyenneSYNC(interlow)
stDev_signal = stdevSYNC(interhigh)
bruithigh1 = ( moyenneSignal/stDev_signal)
incertitude_high1 = incertitude(interhigh)
# incertitude_low1 = incertitude(interlow)
bruithigh2 = noise_on_signal(interhigh)
# bruitlow2 = noise_on_signal(interlow)
print(bruithigh1, '\n', incertitude_high1, '\n', moyenneSignal, '\n', stDev_signal)


### On va additionner les expériences entre elles pour diminuer le bruit
#Les expériences ne sont pas de la même longueur, on trouve la longueur du plus petit bloc.
def min_len_listoflist(index_list):
    min = 10000
    for inter in index_list:
        if inter[1]-inter[0] < min:
            min = inter[1]-inter[0]
    return min

# On formatte les blocs indices pour qu'ils soient tous de la longueur du plus petit bloc.
def cut_blocs(index_list):
    format_index =[]
    inter_len_min = min_len_listoflist(index_list)
    for inter in index_list:
        début, fin = inter[0], inter[0]+inter_len_min
        format_index.append([début, fin])
    return format_index
    

#On moyenne n expériences en faisant la moyenne de deux listes en les parcourant un élément à la fois
def add_n_blocs(format_index, n):
    if len(format_index) < n:
        n = len(format_index)
    added_data = Tension[format_index[0][0]: format_index[0][1]]
    for i, _ in enumerate(added_data):
        for j in range(1, n):
            this_bloc = Tension[format_index[j][0]: format_index[j][1]]
            added_data[i] += this_bloc[i]
    return added_data


def incert(data):
    return (max(data)-min(data))/2

#On calcule la ratio signal sur bruit de 1 jusqu'à n expérience pour voir la tendance.
list_of_SoN = []
error_SoN = []
cut_high = cut_blocs(indice_high)
cut_low = cut_blocs(indice_low)
for exp in range(1, len(cut_high)):
    added_data_high = add_n_blocs(cut_high, exp)
    added_data_low = add_n_blocs(cut_low, exp)
    # mpl.plot(np.arange(0, len(added_data_high)+len(added_data_low)), added_data_high+added_data_low)
    # mpl.show()
    delta = mean(added_data_high)#-mean(added_data_low)
    list_of_SoN.append(delta/stdev(added_data_high))
    error_SoN.append((incert(added_data_low)+incert(added_data_high))/delta*list_of_SoN[-1])
    # background = (mean(added_data_high)-mean(added_data_low))/mean(added_data_low)*100
    # print(background, ((incert(added_data_low)+incert(added_data_high))/delta+incert(added_data_low)/mean(added_data_low))*background)


mpl.rcParams.update({'font.size': 22})
fig, ax = mpl.subplots()
mpl.plot(np.arange(1, 128*(len(list_of_SoN)+1), 128), [86]+list_of_SoN, 'bo')
x = np.arange(0, 128*(len(list_of_SoN)+1))
mpl.plot(x, 11.7*x**(1/2), 'b--')
# mpl.errorbar(np.arange(128, 128*(len(list_of_SoN)+1), 128), list_of_SoN, 'o', yerr =error_SoN)
mpl.xlabel("""Nombre de mesures moyennées""")      # titre des abscisses
mpl.ylabel('Ratio signal sur bruit') 
#mpl.text(2000, 15, """La numérisation d'un signal carré a été faite sur un oscilloscope qui moyennait le signal 128 fois. Les différents plateaux du signal numérisé ont été additionés entre eux avec Python pour diminuer le bruit encore plus. Le ratio du point le plus à gauche a été calculé avec un plateau et chaque point est calculé avec un plateau de plus que celui à sa gauche.""")
props = dict(boxstyle='round', facecolor='grey', alpha=0.5)
textstr = """Un curve fit des données moyennées a été fait pour une
courbe y(n) = 11.7 * n^0.5."""
# La numérisation d'un signal carré a été faite sur un
# oscilloscope qui moyennait le signal 128 fois. Les
# différents plateaux du signal numérisé ont été
# additionés entre eux avec Python pour diminuer le
# bruit encore plus. Le graphique montre le ratio
# signal sur bruit pour l'addition de 1 à 24 plateaux.
# # place a text box in upper left in axes coords
mpl.text(0.98, 0.03, textstr, transform=ax.transAxes,
        verticalalignment='bottom', horizontalalignment='right', bbox=props)
mpl.show()


