import numpy as np
import matplotlib.pyplot as mpl
from statistics import mean, stdev

Temps = []
Tension = []

Temps_2 = []
Tension_2 = []

data1 = np.genfromtxt('F0001CH2_128.csv', delimiter=',')#data moyenné 128x par oscilloscope
data2 = np.genfromtxt('F0000CH2.csv', delimiter=',')#data pas moyenné par oscilloscope
#print(data1)

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

mpl.xlabel('Temps(s)')      # titre des abscisses
mpl.ylabel('Tension(V)')      # titre des ordonnées
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


moyenneSignal = moyenneSYNC(interhigh)-moyenneSYNC(interlow)
stDev_signal = stdevSYNC(interhigh)
bruithigh1 = ( moyenneSignal/stDev_signal)
incertitude_high1 = incertitude(interhigh)
incertitude_low1 = incertitude(interlow)
# bruithigh2 = noise_on_signal(interhigh)
# bruitlow2 = noise_on_signal(interlow)
#print(bruithigh1,'\n', incertitude_high1, '\n', incertitude_low1, '\n', moyenneSignal, '\n', stDev_signal)


### On va additionner les expériences entre elles pour diminuer le bruit
#Les expériences ne sont pas de la même longueur, on formatte pour avoit toutes les mêmes longueurs
def min_len_listoflist(inter_list):
    min = 100
    index_list = find_index(inter_list)
    for inter in index_list:
        if inter[1]-inter[0] < min:
            min = inter[1]-inter[0]
    return min

#Pour les high, l'intervalle min est de 48, on définit la liste interhigh_formattée pour avoir uniquement des intervalles de 48
indice_high_formattée =[]
for inter in indice_high:
    début, fin = inter[0], inter[0]+ min_len_listoflist(interhigh)+1
    indice_high_formattée.append([début, fin])

#Pour les low, on coupe enlève ceux qui sont plus petit que 48 
indice_low_formattée =[]
for inter in indice_low:
    if inter[1]-inter[0] >=  min_len_listoflist(interhigh):
        début, fin = inter[0], inter[0]+ min_len_listoflist(interhigh)+1
        indice_low_formattée.append([début, fin])

#on fait une liste de Tension High formattée
tension_high = []
for inter in indice_high_formattée:
  tension_high.append(Tension[inter[0]: inter[1]])

##on fait une liste de Tension Low formattée
tension_low = []
for inter in indice_low_formattée:
  tension_low.append(Tension[inter[0]: inter[1]])
  

#On additionne chaque expérience actives SYNCH High,
Moyenne_high = []
Points_high = []

for i in range(49):
    for experience in tension_high:
       Points_high.append(experience[i])
    Moyenne_high.append(sum(Points_high)/len(Points_high))
    Points_high=[]

#On additionne chaque background SYNCH Low,
Moyenne_low = []
Points_low = []

for i in range(49):
    for experience in tension_low:
       Points_low.append(experience[i])
    Moyenne_low.append(sum(Points_low)/len(Points_low))
    Points_low=[]

#Graphique qui montre la diminution du bruit
mpl.plot(np.arange(interhigh[0][0],interhigh[0][1], 0.002), Moyenne_high, color = 'red', label = 'Moyenne des 25 moyennes de 128 expériences')
mpl.plot(np.arange(interlow[1][0],interlow[1][1], 0.002), Moyenne_low, color = 'red')
mpl.legend(loc = 'lower left', fontsize="x-small")
mpl.show()


#On calcule différence (en %) entre le background et le signal avec les signaux moins bruités pour avoir une meilleure précision
Signal_moyen = (mean(Moyenne_high)-mean(Moyenne_low))/mean(Moyenne_low)*100
#print(Signal_moyen)

#On cherche le ratio signal sur bruit en fonction du nombre d'expérience dont nous ferons la moyenne
def SON(n, list_index):
    list_nos = []
    for index in list_index[0:n]:
        list_nos.append(mean(Tension[index[0]: index[1]])/stdev(Tension[index[0]: index[1]]))
    return mean(list_nos)

ratios = []
for n in range(1, 26):
    ratios.append(SON(n,indice_high_formattée))

#mpl.plot([128 * i for i in range(1, 26)], ratios)
#mpl.show()

