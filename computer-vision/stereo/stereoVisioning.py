import numpy as np
import cv2
from matplotlib import pyplot as plt

def setup():
    leftCamera = cv2.VideoCapture(1)
    rightCamera = cv2.VideoCapture(0)
    return leftCamera, rightCamera

def showImage(image, title='Snapshot'):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# def getRawData():
def getRawData(imgL, imgR):
    patternSize = (9, 6)
    objp = np.zeros((np.prod(patternSize), 3), np.float32)
    objp[:, :2] = np.indices(patternSize).T.reshape(-1, 2)

    # Object points
    objectPoints = []

    # Image Points
    leftImagePoints = []
    rightImagePoints = []

    leftSuccess, leftCorners = cv2.findChessboardCorners(imgL, patternSize)
    rightSuccess, rightCorners = cv2.findChessboardCorners(imgR, patternSize)
        
    if leftSuccess and rightSuccess:
        objectPoints.append(objp)
        leftImagePoints.append(leftCorners)
        rightImagePoints.append(rightCorners)

    # Load chessboard images from both cameras
    # for i in range(10): # Repeat for accuracy
    #     imgL = cv2.imread(leftCameraIndex)
    #     imgR = cv2.imread(rightCameraIndex)
        
    #     leftSuccess, leftCorners = cv2.findChessboardCorners(imgL, patternSize)
    #     rightSuccess, rightCorners = cv2.findChessboardCorners(imgR, patternSize)
        
    #     if leftSuccess and rightSuccess:
    #         objectPoints.append(objp)
    #         leftImagePoints.append(leftCorners)
    #         rightImagePoints.append(rightCorners)
    
    return objectPoints, leftImagePoints, rightImagePoints, imgL, imgR


# Calibrate cameras
def calibrate(objectPoints, leftImagePoints, rightImagePoints, imgL, imgR):

    # camera matrix, distortion coefficients
    leftSuccess, mtxLeft, distLeft, _, _ = cv2.calibrateCamera(objectPoints, leftImagePoints, imgL.shape[::-1], None, None)
    rightSuccess, mtxRight, distRight, _, _ = cv2.calibrateCamera(objectPoints, rightImagePoints, imgR.shape[::-1], None, None)

    # Stereo calibration
    flags = cv2.CALIB_FIX_INTRINSIC
    ret, _, _, _, _, R, T, _, _ = cv2.stereoCalibrate(objectPoints, leftImagePoints, rightImagePoints,mtxLeft, distLeft, mtxRight, distRight,imgL.shape[::-1], criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-5), flags=flags
    )
    return mtxLeft, distLeft, mtxRight, distRight, imgL, imgR, R, T
    

# undistort
def undistort(mtxLeft, distLeft, mtxRight, distRight, imgL, imgR, R, T):
    R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(mtxLeft, distLeft, mtxRight, distRight, imgL.shape[::-1], R, T)
    # Generate maps for undistortion and rectification
    map1Left, map2Left = cv2.initUndistortRectifyMap(mtxLeft, distLeft, R1, P1, imgL.shape[::-1], cv2.CV_16SC2)
    map1Right, map2Right = cv2.initUndistortRectifyMap(mtxRight, distRight, R2, P2, imgR.shape[::-1], cv2.CV_16SC2)

    return map1Left, map2Left, map1Right, map2Right, Q


def computeDisparityMap(map1Left, map2Left, map1Right, map2Right, Q, imgL, imgR):
    # Stereo BM matcher
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
        
    # Rectify the images
    rectifiedLeft = cv2.remap(imgL, map1Left, map2Left, cv2.INTER_LINEAR)
    rectifiedRight = cv2.remap(imgR, map1Right, map2Right, cv2.INTER_LINEAR)
        
    # Convert to grayscale
    grayLeft = cv2.cvtColor(rectifiedLeft, cv2.COLOR_BGR2GRAY)
    grayRight = cv2.cvtColor(rectifiedRight, cv2.COLOR_BGR2GRAY)
        
    # Compute the disparity map
    disparity = stereo.compute(grayLeft, grayRight)
        
    # Normalize and display
    disparity = cv2.normalize(disparity, disparity, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    disparity = np.uint8(disparity)
    
    return disparity

def depthCalculation(disparity, Q):
    depthMap = cv2.reprojectImageTo3D(disparity, Q)
    return depthMap

cameraLeft, cameraRight = setup()
_, imgL = cameraLeft.read()
_, imgR = cameraRight.read()

objectPoints, leftImagePoints, rightImagePoints, imgL, imgR = getRawData(imgL, imgR)
mtxLeft, distLeft, mtxRight, distRight, imgL, imgR, R, T = calibrate(objectPoints, leftImagePoints, rightImagePoints, imgL, imgR)
map1Left, map2Left, map1Right, map2Right, Q = undistort(mtxLeft, distLeft, mtxRight, distRight, imgL, imgR, R, T)
disparity = computeDisparityMap(map1Left, map2Left, map1Right, map2Right, Q, imgL, imgR)
depthMap = depthCalculation(disparity, Q)


def openAITest():
    print('Test me')