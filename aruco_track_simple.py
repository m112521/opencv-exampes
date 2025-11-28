import cv2 
import numpy as np

vid = cv2.VideoCapture(0)
width = 0
height = 0

i = 0
point_color = (0, 250, 120)
point_radius = 2
point_thickness = -1

points = []

#os.chdir('imgs/calib') 

while True:
    ret, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters()

    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        points.append((int(corners[0][0][0][0]), int(corners[0][0][0][1])))
    
    for point in points:
        cv2.circle(frame, point, point_radius, point_color, point_thickness)

    cv2.imshow('Detected Markers', frame)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
	    break

vid.release()
cv2.destroyAllWindows()