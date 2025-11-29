import cv2 
import numpy as np
import math

vid = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (255, 0, 0)
font_thickness = 1
px_per_mm = None

def get_bb(points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]

    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)

    #bounding_box = (min_x, min_y, max_x, max_y)
    return (min_x, min_y, max_x - min_x, min_y - max_y)


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
        p3 = (int(corners[0][0][3][0]), int(corners[0][0][3][1]))
        cv2.circle(frame, p0, 8, (255, 0, 0), -1)
        cv2.circle(frame, p1, 8, (0, 255, 120), -1)
        cv2.circle(frame, p2, 8, (0, 0, 255), -1)
        #print(f"p0-p1: {euclidean_distance(p0, p1)}; p1-p2: {euclidean_distance(p1, p2)}")

        bbox = get_bb([p0, p1, p2, p3])
        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv2.rectangle(frame, (x, y), (x + w, y - h), (0, 255, 0), 2)

        px_per_mm = int(w /40)
        #print(f"px per mm = {px_per_mm}")
        cv2.putText(frame, f"px_per_mm = {px_per_mm}", (30, 50), font, font_scale, font_color, font_thickness, cv2.LINE_AA)
    
    cv2.imshow('Detected Markers', frame)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
	    break

vid.release()
cv2.destroyAllWindows()