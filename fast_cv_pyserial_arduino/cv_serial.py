import cv2 
import serial
import time
import asyncio

arduino_port = 'COM3'
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)


vid = cv2.VideoCapture(0)
points = []
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

while True:
    ret, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        points.append((int(corners[0][0][0][0]), int(corners[0][0][0][1])))

        data_to_send = "S1:120;S2:250"
        ser.write(data_to_send.encode('utf-8'))

    else:
        data_to_send = "S1:90;S2:250"
        ser.write(data_to_send.encode('utf-8'))
    
    #for point in points:
    #    cv2.circle(frame, point, 2, (0, 250, 120), 1)

    cv2.imshow('Detected Markers', frame)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
	    break

vid.release()
cv2.destroyAllWindows()