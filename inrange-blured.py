import numpy as np
import cv2

def nothing(args):pass
cv2.namedWindow("setup")
cv2.namedWindow("setup2")
cv2.createTrackbar("b1", "setup", 0, 255, nothing)
cv2.createTrackbar("g1", "setup", 0, 255, nothing)
cv2.createTrackbar("r1", "setup", 0, 255, nothing)
cv2.createTrackbar("b2", "setup", 255, 255, nothing)
cv2.createTrackbar("g2", "setup", 255, 255, nothing)
cv2.createTrackbar("r2", "setup", 255, 255, nothing)
cv2.createTrackbar("blur", "setup2", 0, 10, nothing)
fn = "imgs/laser.jpg" 
img = cv2.imread(fn)
img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

percent = 50
width = int(img.shape[1] * percent / 100)
height = int(img.shape[0] * percent / 100)
dim = (width, height)
img = cv2.resize(img, dim)
while True:
   r1 = cv2.getTrackbarPos('r1', 'setup')
   g1 = cv2.getTrackbarPos('g1', 'setup')
   b1 = cv2.getTrackbarPos('b1', 'setup')
   r2 = cv2.getTrackbarPos('r2', 'setup')
   g2 = cv2.getTrackbarPos('g2', 'setup')
   b2 = cv2.getTrackbarPos('b2', 'setup')
   blur = cv2.getTrackbarPos('blur', 'setup2')
   min_p = (g1,b1,r1)
   max_p = (g2,b2,r2)
   img_bl = cv2.medianBlur(img, 1+blur*2) # smooth
   img_mask = cv2.inRange(img_bl, min_p, max_p)
   img_m = cv2.bitwise_and(img, img, mask = img_mask)
   cv2.imshow('img', img_m)
   if cv2.waitKey(33) & 0xFF == ord('q'):
      break
cv2.destroyAllWindows()
