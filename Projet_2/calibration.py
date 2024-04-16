import numpy as np
import cv2
import os

#Caméra droite chargée
def calib_1camera(camera):
    # Define the size of the checkerboard pattern
    pattern_size = (6, 9)  # Change according to your calibration target

    # Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((pattern_size[0]*pattern_size[1], 3), np.float32)
    objp[:, :2] = 2.29*np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d points in real world space
    imgpoints = []  # 2d points in image plane.

    # Images directory
    images_dir = 'images_calibration/'  # Change this to your directory of calibration images

    # Get list of calibration images
    cwd = os.getcwd()+'/Projet_2/'+images_dir+camera
    images = os.listdir(cwd)
    print(images)

    img = cv2.imread(cwd + '/' +images[0])
    width, height = img.shape[1], img.shape[0]
    shape = width, height
    # Loop through each calibration image
    for fname in images:
        img = cv2.imread(cwd + '/' +fname)
        cv2.imshow('Image', img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
            imgpoints.append(corners2)

            # Draw and display the corners
            # img = cv2.drawChessboardCorners(img, pattern_size, corners2, ret)
            # cv2.imshow('img', img)
            # cv2.waitKey(500)

    cv2.destroyAllWindows()

    # Calibration
    ret, mtx, dist, rvecs, tvecs, shape= cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # Print calibration results
    print("Camera Matrix:\n", mtx)
    print("\nDistortion Coefficients:\n", dist)
    return mtx, dist, objpoints, imgpoints


def read_imgfile(camera):
    # Images directory
    images_dir = 'images_calibration/'

    # Get and read a list of calibration images
    cwd = os.getcwd()+'/Projet_2/'+images_dir+camera
    images = []
    for img in os.listdir(cwd):
        img_read = cv2.imread(cwd + '/' + img, 1)
        images.append(img_read)
    return images


def calibrate_stereocamera(objpoints, imgpoints1, imgpoints2, mtx1, dist1, mtx2, dist2, shape):
    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    stereocalibration_flags = cv2.CALIB_FIX_INTRINSIC
    ret, CM1, dist1, CM2, dist2, R, T, E, F = cv2.stereoCalibrate(objpoints, imgpoints1, imgpoints2, mtx1, dist1,
                                                                 mtx2, dist2, shape, criteria = criteria, flags = stereocalibration_flags)
    return R, T


def DLT(P1, P2, point1, point2):
 
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




mtxD, distD, objpointsD, imgpointsD, shapeD = calib_1camera('imgD')
mtxG, distG, objpointsG, imgpointsG, shapeG = calib_1camera('imgG')

if objpointsD == objpointsG and shapeD == shapeG:
    R, T = calibrate_stereocamera(objpointsG, imgpointsG, imgpointsD, mtxG, distG, mtxD, distD, shapeG)

RT1 = np.concatenate([np.eye(3), [[0],[0],[0]]], axis = -1)
P1 = mtxG @ RT1 #projection matrix for C1
 
#RT matrix for C2 is the R and T obtained from stereo calibration.
RT2 = np.concatenate([R, T], axis = -1)
P2 = mtxD @ RT2 #projection matrix for C2