import numpy as np
import dlib
import cv2 as cv

detector = dlib.get_frontal_face_detector()


vid = cv.VideoCapture(0)

# cv2.TrackerKCF_create || cv2.TrackerBoosting_create || cv2.TrackerMIL_create || cv2.TrackerTLD_creat || cv2.TrackerMedianFlow_create || cv2.TrackerMOSSE_create
curr_bbox = None # boundingBox
trackers = cv.MultiTracker_create()

while True:
	ret, frame = vid.read()

	if frame is None:
		break

	if curr_bbox is not None:
		(success, boxes) = trackers.update(frame)

		for box in boxes:
			#(x, y, w, h) = [int(v) for v in box] 
			print(box)
			cv.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 255), 2)

	else:
		gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)	
		dets = detector(gray, 1)

		for i, d in enumerate(dets):
			curr_bbox = (d.left(), d.top(), d.right(), d.bottom())
			tracker = cv.TrackerCSRT_create()
			trackers.add(tracker, frame, curr_bbox)
			#cv.rectangle(frame,(d.left(),d.top()),(d.right(),d.bottom()),(0,255,255),2)

	cv.imshow("Track", frame)


	if cv.waitKey(1) & 0xFF==ord('q'):
		break

vid.release()
cv.destroyAllWindows()
