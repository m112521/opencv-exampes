import numpy as np
import dlib
import cv2 as cv
import collections

detector = dlib.get_frontal_face_detector()
vid = cv.VideoCapture(0)

points = collections.deque(maxlen=10)

while True:
	ret, frame = vid.read()

	if frame is None:
		break

	# TBD: resize to speed-up 
	hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

	lower_blue = np.array([80,50,50])
	upper_blue = np.array([130,255,255])

	mask = cv.inRange(hsv, lower_blue, upper_blue)
	mask = cv.erode(mask, None, iterations=2)
	mask = cv.dilate(mask, None, iterations=2)

	#blue_cap = cv.bitwise_and(frame, frame, mask = mask)

	contours, _ = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
	center = None

	if len(contours) > 0:
		c = max(contours, key=cv.contourArea)
		((x, y), radius) = cv.minEnclosingCircle(c)
		M = cv.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		if radius > 30:
			cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv.circle(frame, center, 5, (0, 0, 255), 1)

	points.append(center)

	for i in range(1, len(points)):
		if points[i - 1] is None or points[i] is None:
			continue
 
		cv.line(frame, points[i - 1], points[i], (0, 255, 255), 1)

	cv.imshow("Track", frame)
	
	if cv.waitKey(1) & 0xFF==ord('q'):
		break


vid.release()
cv.destroyAllWindows()
