import matplotlib.pyplot as plt
import numpy as np

lmbda = 0.0000006328
lmbda_c = 0.000000620
na = 0.12
w_laser = 0.00063/2
theta = 0.0013/2
f = 0.0045
a = 2.405*lmbda_c/2/np.pi/na
z = np.arange(0,1, 0.01)
w_objectif = w_laser*(1+(z*theta/w_laser)**2)**(1/2)
w_image = lmbda*f/np.pi/w_objectif
t = (2*w_image*a/(w_image**2+a**2))**2
plt.rcParams.update({'font.size': 24})
plt.plot(z, t, 'bo', markersize=10)
plt.xlabel = 'distance laser/lentille (Z)'
plt.ylabel = 'efficacité d’injection (T)'
plt.show()
print(a)