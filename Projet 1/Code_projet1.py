import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("C:\\Users\\ameli\\OneDrive\\Documents\\Amélie\\Université\\Session 4 Hiver 2024\\Travaux pratiques d'optique photonique\\Projet 1\\__scope_7.csv", delimiter=',')

Temps = []
Signal_capté = []
Signal_transmis = []

for i in data:
    Temps.append(i[0])
    Signal_capté.append(i[1])
    Signal_transmis.append(i[2])


# Normalisation des signaux
Capté_norm = Signal_capté / np.max(np.abs(Signal_capté))
Transmis_norm = Signal_transmis / np.max(np.abs(Signal_transmis))

# Recentrer les signaux autour de zéro
Capté_norm_centré = Capté_norm - np.mean(Capté_norm)
Transmis_norm_centré = Transmis_norm - np.mean(Transmis_norm)

# FFT du signal transmis
fft_transmis = np.fft.fft(Transmis_norm_centré)
freq_transmis = np.fft.fftfreq(len(Transmis_norm_centré), d=Temps[1]-Temps[0])

index_transmis = 0
for i, b in enumerate(freq_transmis):
    if b < 0:
        index_transmis = i
        break


# FFT du signal capté
fft_capté = np.fft.fft(Capté_norm_centré)
freq_capté = np.fft.fftfreq(len(Capté_norm_centré), d=Temps[1]-Temps[0])

index_capté = 0
for i, b in enumerate(freq_capté):
    if b < 0:
        index_capté = i
        break

# Normalisation des FFT
fft_transmis_norm = np.abs(fft_transmis) / np.max(np.abs(fft_transmis))
fft_capté_norm = np.abs(fft_capté) / np.max(np.abs(fft_capté))

#Tracer le signal et son spectre en fréquence
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(Temps, Transmis_norm_centré, label='Signal transmis')
plt.plot(Temps, Capté_norm_centré, label='Signal capté')
plt.title('Signal temporel normalisé')
plt.ylabel('Amplitude')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(freq_transmis[0: index_transmis], fft_transmis_norm[0:index_transmis], label='FFT du signal transmis')
plt.plot(freq_capté[0: index_capté], fft_capté_norm[0:index_capté], label='FFT du signal capté')
plt.title('Spectre en fréquence normalisé')
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Amplitude')
plt.legend(loc='upper left')

plt.tight_layout()

plt.show()

print(freq_transmis)
