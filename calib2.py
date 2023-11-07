"""
Modified version of the original script from https://github.com/mesutpiskin/opencv-fisheye-undistortion/blob/master/src/python/camera_calibration_undistortion.py
"""

import cv2
import numpy as np
import glob


def calibrate(folder, rows=6, cols=9, save_file='calibrationdata.npz'):
    """
    Calibrates the camera to get the undistortion parameters. Capture a few images of the chessboard pattern
    with your camera and store them in `folder`. This function obtains the undistortion parameters and saves
    them in `save_file`.
    
    Argugments:
    ----------
    `folder`: String, required
        The folder where the images of the chessboard pattern are stored.
    `rows`, `cols`: Integers, optional
        The number of horizontal and vertical lines on your chessboard.
    `save_file`: String, optional
        Path to save the undistortion parameters.
    """

    # Stop / decision criteria for the algorithm
    criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 0.001)

    # Required Variables
    objectPoints = np.zeros((rows * cols, 3), np.float32)
    objectPoints[:, :2] = np.mgrid[0:rows, 0:cols].T.reshape(-1, 2)
    objectPointsArray = []
    imgPointsArray = []

    img_paths = glob.glob(f'{folder.rstrip("/")}/*.png')
    found = 0 

    # Repeat n times until successful calibration is done.
    for img_path in img_paths:
        # Read the next image and convert to grayscale
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the corners of the chessboard within the frame
        isSucces, corners = cv2.findChessboardCorners(gray, (rows, cols), None)

        # If the corners were found succesfully
        if isSucces:
            '''
            If the number of rows and columns we specified is correctly determined
            With the cornerSubPix () method, the sub-pixel of the corners or radial spine points,
            it repeats itself to find the correct position.
            '''
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

            # Save the points we just achieved
            objectPointsArray.append(objectPoints)
            imgPointsArray.append(corners)
            
            found += 1
            
    print(f'{found} usable images found in {folder}.')

    # Save the K and D values obtained as an npz archive
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objectPointsArray, imgPointsArray, gray.shape[::-1], None, None)
    np.savez(save_file, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
    
    return mtx, dist

  
def undistort(img, mtx, dist):
    """
    Utilizes the undistortion parameters obtained via calibration to undistort other images taken from the same
    camera.
    
    Arguments:
    ---------
    `img`: Numpy Array, Required
        The image to be undistorted.
    `mtx`, `dist`: Numpy Arrays, Required
        The undistortion parameters obtained via calibration.
    """

    h, w = img.shape[:2]
    newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    undistortedImg = cv2.undistort(img, mtx, dist, None, newCameraMtx)

    return undistortedImg

if __name__ == '__main__':
    folder = 'imgs/calib'
    rows = 6
    cols = 9
    save_file= 'calibrationdata.npz'
    
    # Calibrate
    mtx, dist = calibrate(
        folder=folder,
        rows=rows,
        cols=cols,
        save_file=save_file
    )
    
    # Test undistortion on a sample image
    img_path = glob.glob(f'{folder.rstrip("/")}/*.png')[0]
    img = cv2.imread(img_path)
    undistorted = undistort(img, mtx, dist)
    cv2.imwrite("imgs/calib/0-undistorted.png", undistorted)
