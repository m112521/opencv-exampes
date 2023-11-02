import dlib
import cv2 as cv
import numpy as np
import collections

tracker = dlib.correlation_tracker()
vid = cv.VideoCapture(0)

points = collections.deque(maxlen=10) # stroting tail TBD: for each cap
track_objects = [] # list of caps
init_frame = None

width = 0
height = 0


cap_counter = 0

while True:
	ret, frame = vid.read()
	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

	hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
	lower_blue = np.array([80,50,50])
	upper_blue = np.array([130,255,255])
	mask = cv.inRange(hsv, lower_blue, upper_blue)
	mask = cv.erode(mask, None, iterations=2)
	mask = cv.dilate(mask, None, iterations=2)

	if init_frame is None:
		#dets = detector(gray, 1)

		contours, _ = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
		center = None

		if len(contours) > 0:
			c = max(contours, key=cv.contourArea)

			for c in contours:
				((x, y), radius) = cv.minEnclosingCircle(c)
				M = cv.moments(c)
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
				if radius > 10 and radius < 150:
					cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
					cv.circle(frame, center, 5, (0, 0, 255), 1)

					# get bounding box
					c_poly = cv.approxPolyDP(c, 3, True)
					bound_rect = cv.boundingRect(c_poly)

					#cv.rectangle(frame, (int(bound_rect[0]), int(bound_rect[1])), (int(bound_rect[0] + bound_rect[2]), int(bound_rect[1] + bound_rect[3])), (0,255,255), 1)
					
					#top_left = (int(bound_rect[0]), int(bound_rect[1]))
					#bottom_right = (int(bound_rect[0] + bound_rect[2]), int(bound_rect[1] + bound_rect[3]))

					d = dlib.rectangle(int(bound_rect[0]), int(bound_rect[1]), int(bound_rect[0] + bound_rect[2]), int(bound_rect[1] + bound_rect[3]))
					track_objects.append(dlib.correlation_tracker()) # create new tracking object
					track_objects[-1].start_track(frame, d)
		init_frame = 1
	else:
		[t.update(frame) for t in track_objects]

	for tr in track_objects:
		rex = tr.get_position()
		cv.rectangle(frame, (int(rex.left()), int(rex.top())), (int(rex.right()), int(rex.bottom())), (0, 255, 255), 2)
		if rex.top() > (height - 100):
			cap_counter = cap_counter + 1


	cv.line(frame, (0, height - 100), (width, height - 100), (0, 255, 0), 2)
	cv.putText(frame,'Caps: ', (10,100), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2, cv.LINE_AA)

	cv.imshow('caps', frame)

	width = frame.shape[1]
	height = frame.shape[0]

	if cv.waitKey(1) & 0xFF==ord('q'):
		break

vid.release()
cv.destroyAllWindows()