'''
1 mm = 3.8 pixels

152 px / 3.8 px = 40 mm (red one)

'''


import numpy as np
import cv2 as cv

def nothing(x):
    pass

cv.namedWindow('image')

cv.createTrackbar('MinDist','image', 1, 100, nothing) 
cv.createTrackbar('Param1','image', 10, 100, nothing) 
cv.createTrackbar('Param2','image', 10, 100, nothing) 
cv.createTrackbar('MinRadius','image', 0, 100, nothing) 
cv.createTrackbar('MaxRadius','image', 0, 100, nothing) 

cv.setTrackbarPos('MinDist', 'image', 20)
cv.setTrackbarPos('Param1', 'image', 50)
cv.setTrackbarPos('Param2', 'image', 30)
cv.setTrackbarPos('MinRadius', 'image', 0)
cv.setTrackbarPos('MaxRadius', 'image', 0)


minDist = param1 = param2 = minRadius = maxRadius = 0
pminDist = pparam1 = pparam2 = pminRadius = pmaxRadius = 0

img = cv.imread('testHough.PNG', cv.IMREAD_GRAYSCALE)
img = cv.resize(img, (0, 0), fx=0.5, fy=0.5)
waitTime = 33


while (1):
    minDist = cv.getTrackbarPos('MinDist','image')
    param1 = cv.getTrackbarPos('Param1','image')
    param2 = cv.getTrackbarPos('Param2','image')
    minRadius = cv.getTrackbarPos('MinRadius','image')
    maxRadius = cv.getTrackbarPos('MaxRadius','image')
    

    img = cv.medianBlur(img,5)
    cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
    circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT, 1.2, minDist, param1=param1,param2=param2,minRadius=minRadius,maxRadius=maxRadius)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        print(f'Diameter: {i[2]*2}')
        # draw the outer circle
        cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

        

    if ( (pminDist != minDist) | (pparam1 != param1) | (pparam2 != param2) | (pminRadius != minRadius) | (pmaxRadius != maxRadius) ):
        print("(minDist = %d , param1 = %d, param2 = %d), (minRaius = %d , maxRaius = %d)" % (minDist , param1 , pparam2, minRadius, maxRadius))
        pminDist = minDist
        pparam1 = param1
        pparam2 != param2
        pminRadius != minRadius
        pmaxRadius != maxRadius


    cv.imshow('image', cimg)

    if cv.waitKey(waitTime) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()