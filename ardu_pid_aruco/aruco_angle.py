import cv2
import numpy as np
import math

MARGIN = 30 #px

vid = cv2.VideoCapture(1)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

while True:
    ret, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = detector.detectMarkers(gray)

    if ids is not None:
        #(int(corners[0][0][0][0]), int(corners[0][0][0][1]))
        #for corner in corners:
            # Get the four corners of the first detected marker
        p1, p2, p3, p4 = corners[0][0]
        
        # Calculate the vector along the top edge (p1 to p2)
        # Vector = (x2 - x1, y2 - y1)
        vector_x = p2[0] - p1[0]
        vector_y = p2[1] - p1[1]
        cv2.arrowedLine(frame, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (255, 0, 0), 2, tipLength=0.2)
        cv2.arrowedLine(frame, (int(p1[0]), int(p1[1])), (int(p4[0]), int(p4[1])), (0, 255, 0), 2, tipLength=0.2)
        
        # Use atan2 to find the angle of this vector relative to the x-axis
        # The angle will be in radians, ranging from -pi to pi
        angle_rad = math.atan2(vector_y, vector_x)
        
        # Convert to degrees and normalize if needed (e.g., to 0-360 range)
        angle_deg = math.degrees(angle_rad)
        if angle_deg < 0:
             angle_deg += 360
            
        print(f"2D Angle: {angle_deg:.2f} degrees")

    pt1 = (MARGIN, MARGIN)
    pt2 = (frame.shape[1] - MARGIN, frame.shape[0] - MARGIN)
    cv2.rectangle(frame, pt1, pt2, (0, 120, 255), thickness=3, lineType=cv2.LINE_8, shift=0)

    cv2.imshow('Detected Markers', frame)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
	    break

vid.release()
cv2.destroyAllWindows()
