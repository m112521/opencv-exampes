import cv2 
import numpy as np
import math

vid = cv2.VideoCapture(0)
width = 0
height = 0

def euclidean_distance(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

while True:
    ret, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters()

    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        p0 = (int(corners[0][0][0][0]), int(corners[0][0][0][1]))
        p1 = (int(corners[0][0][1][0]), int(corners[0][0][1][1]))
        p2 = (int(corners[0][0][2][0]), int(corners[0][0][2][1]))
        cv2.circle(frame, p0, 8, (255, 0, 0), -1)
        cv2.circle(frame, p1, 8, (0, 255, 120), -1)
        cv2.circle(frame, p2, 8, (0, 0, 255), -1)
        print(f"p0-p1: {euclidean_distance(p0, p1)}; p1-p2: {euclidean_distance(p1, p2)}")
    
    cv2.imshow('Detected Markers', frame)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
	    break

vid.release()
cv2.destroyAllWindows()