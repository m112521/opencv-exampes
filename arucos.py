import cv2 
import numpy as np

vid = cv2.VideoCapture(0)
width = 0
height = 0

i = 0
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
        cv2.circle(frame, (int(corners[0][0][0][0]), int(corners[0][0][0][1])), 8, (255, 0, 0), -1)
        cv2.circle(frame, (int(corners[0][0][1][0]), int(corners[0][0][1][1])), 8, (0, 255, 120), -1)
        cv2.circle(frame, (int(corners[0][0][2][0]), int(corners[0][0][2][1])), 8, (0, 0, 255), -1)
    
    cv2.imshow('Detected Markers', frame)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
	    break

vid.release()
cv2.destroyAllWindows()