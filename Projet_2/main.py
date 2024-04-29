import cv2
import os
import numpy as np
import matplotlib.pyplot as plt


def DLT(P1, P2, point1, point2):
 #Find the 3Dpoint in the object space with the 2 camera matrices and the image point in each camera.
    A = [point1[1]*P1[2,:] - P1[1,:],
         P1[0,:] - point1[0]*P1[2,:],
         point2[1]*P2[2,:] - P2[1,:],
         P2[0,:] - point2[0]*P2[2,:]
        ]
    A = np.array(A).reshape((4,4))
    #print('A: ')
    #print(A)
 
    B = A.transpose() @ A
    from scipy import linalg
    U, s, Vh = linalg.svd(B, full_matrices = False)
 
    print('Triangulated point: ')
    print(Vh[3,0:3]/Vh[3,3])
    return Vh[3,0:3]/Vh[3,3]


def find_2D_point(im):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
    
    filtered = cv2.morphologyEx(binary, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    contours, hierarchy = cv2.findContours(filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    list_moments = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if 10000 > area > 20:
            cv2.drawContours(im, [contour], 0, (0, 255, 0), 2)
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])    
            list_moments.append((cX, cY))
    if len(list_moments) > 0:
        cX, cY = min(list_moments, key=lambda point: point[0])
        cv2.circle(im, (cX, cY), 5, (0, 0, 255), -1)
        #cv2.imshow('filtered image', im)
        #cv2.waitKey(0)
        return (cX, cY)
    return None


imgG = []
imgD = []

cwd = os.getcwd()+'/Projet_2/images_calibration/laserG'
images = os.listdir(cwd)
images.sort()
for name in images:
    im = cv2.imread(cwd + '/' + name)
    imgG.append(im)

cwd = os.getcwd()+'/Projet_2/images_calibration/laserD'
images = os.listdir(cwd)

images.sort()
for name in images:
    im = cv2.imread(cwd + '/' + name)
    imgD.append(im)

    # Read calibration parameters from file
# calibration_file = os.getcwd() + '/Projet_2/calibration_parameters.txt'
# with open(calibration_file, 'r') as file:
#     lines = file.readlines()

# Extract mtxG, mtxD, R, and T from the file
# mtxG = np.array([float(x) for x in line.split() for line in lines[2:5]])
# mtxD = np.array([float(x) for x in lines[1].split()])
# R = np.array([float(x) for x in lines[2].split()])
# T = np.array([float(x) for x in lines[3].split()])

mtxG = np.array([[3.895982728481461436e+03,0.000000000000000000e+00,2.375302528636943862e+03],
                [0.000000000000000000e+00,3.891338795863054202e+03,1.714470306147638212e+03],
                [0.000000000000000000e+00,0.000000000000000000e+00,1.000000000000000000e+00]])
mtxD = np.array([[3.853913056025005972e+03,0.000000000000000000e+00,2.395379896638006812e+03],
                [0.000000000000000000e+00,3.861999576279004941e+03,1.676414607137890243e+03],
                [0.000000000000000000e+00,0.000000000000000000e+00,1.000000000000000000e+00]])
R = np.array([[9.995506058225234192e-01,2.499335064457210067e-04,-2.997538878928698511e-02],
                [-2.118932446361477097e-04,9.999991682789086678e-01,1.272219612998739440e-03],
                [2.997568182843275350e-02,-1.265296302522394894e-03,9.995498274344243317e-01]])
T = np.array([[-1.345002257294719961e+01],
[-3.600602819934663468e-01],
[-9.956976352171891254e-01]])
print(mtxG, mtxD, R, T)

RT1 = np.concatenate([np.eye(3), [[0],[0],[0]]], axis = -1)
P1 = mtxG @ RT1 #projection matrix for C1
 
#RT matrix for C2 is the R and T obtained from stereo calibration.
RT2 = np.concatenate([R, T], axis = -1)
P2 = mtxD @ RT2 #projection matrix for C2

pos_reel = [100, 200, 150, 100, 50, 30, 25]
pos_calc = []
for i in range(len(imgD)):
    pointG = find_2D_point(imgG[i])
    pointD = find_2D_point(imgD[i])
    x, y, z = DLT(P1, P2, pointG, pointD)
    pos_calc.append(z)

err = []
for i in range(len(pos_calc)):
    err.append(abs(pos_calc[i] - pos_reel[i]))

plt.rcParams.update({'font.size': 28})
plt.plot(pos_reel[1:], err[1:], 'bo', markersize=13)
plt.yscale('log')
plt.xlabel('Distance de référence (cm)')
plt.ylabel('Erreur (cm)')
plt.grid()
plt.show()

