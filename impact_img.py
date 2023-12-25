import cv2
import numpy as np
from scipy.spatial import distance
from cv2 import aruco

# import pandas as pd
MARKER_SIZE_MM = 32

img = cv2.imread('media/0.PNG')
frame = cv2.resize(img, (0,0), fx=0.95, fy=0.95)

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
# parameters =  aruco.DetectorParameters_create()
# corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
# frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters =  cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)
markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(gray)
print(markerIds)

if (markerIds is not None) and (len(markerIds) >= 2):
    s1 = (int(markerCorners[0][0][1][0]) *2, int(markerCorners[0][0][1][1]) *2)
    e1 = (int(markerCorners[0][0][3][0]) *2, int(markerCorners[0][0][3][1]) *2)
    
    s2 = (int(markerCorners[1][0][1][0]) *2, int(markerCorners[1][0][1][1]) *2)
    e2 = (int(markerCorners[1][0][3][0]) *2, int(markerCorners[1][0][3][1]) *2)


    

    img = cv2.rectangle(img, s1, e1, (0, 120, 250), 2)
    img = cv2.rectangle(img, s2, e2, (0, 120, 250), 2)

cv2.imshow('Frame', img)
cv2.waitKey(0)

cv2.destroyAllWindows()
