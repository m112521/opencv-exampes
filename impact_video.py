import cv2
import numpy as np
from scipy.spatial import distance
from cv2 import aruco
import os


i = 0

# import pandas as pd
MARKER_SIZE_MM = 32

PX_PER_MM = 0

cap = cv2.VideoCapture('media/0.mp4')


def calc_px_per_mm(pt_bl, pt_tl, marker_size_mm):
    return distance.euclidean(pt_bl, pt_tl) / marker_size_mm


while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    parameters =  cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)
    print(rejectedCandidates)

    
    if rejectedCandidates is not None:
        s1 = (int(rejectedCandidates[0][0][1][0]) , int(rejectedCandidates[0][0][1][1]))
        s2 = (int(rejectedCandidates[0][0][2][0]) , int(rejectedCandidates[0][0][2][1]))
        e1 = (int(rejectedCandidates[0][0][3][0]), int(rejectedCandidates[0][0][3][1]))
        frame = cv2.rectangle(frame, s1, e1, (0, 120, 250), 5)

        PX_PER_MM = calc_px_per_mm(s1, s2, MARKER_SIZE_MM)
        print(f'PX PER MM: {PX_PER_MM}')

        cv2.imshow('Frame', frame)
        # cv2.waitKey(0)
    
    
    if markerIds is not None:
        s1 = (int(markerCorners[0][0][1][0]), int(markerCorners[0][0][1][1]))
        e1 = (int(markerCorners[0][0][3][0]), int(markerCorners[0][0][3][1]))
        frame = cv2.rectangle(frame, s1, e1, (0, 120, 250), 2)

        cv2.imshow('Frame', frame)
        cv2.waitKey(0)
        cv2.imwrite(f'imgs/{i}.png', frame)
        i += 1


    # if (markerIds is not None) and (len(markerIds) >= 2):
    #     s1 = (int(markerCorners[0][0][1][0]) *2, int(markerCorners[0][0][1][1]) *2)
    #     e1 = (int(markerCorners[0][0][3][0]) *2, int(markerCorners[0][0][3][1]) *2)
        
    #     s2 = (int(markerCorners[1][0][1][0]) *2, int(markerCorners[1][0][1][1]) *2)
    #     e2 = (int(markerCorners[1][0][3][0]) *2, int(markerCorners[1][0][3][1]) *2)


    #     cv2.rectangle(frame, s1, e1, (0, 120, 250), 2)
    #     cv2.rectangle(frame, s2, e2, (0, 120, 250), 2)

    #cv2.imshow('Frame', frame)

    #if markerIds is not None:
        #cv2.waitKey(0)


    if cv2.waitKey(25) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()


