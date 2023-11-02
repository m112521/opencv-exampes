#pip install https://pypi.python.org/packages/da/06/bd3e241c4eb0a662914b3b4875fc52dd176a9db0d4a2c915ac2ad8800e9e/dlib-19.7.0-cp36-cp36m-win_amd64.whl#md5=b7330a5b2d46420343fbed5df69e6a3f

import dlib
import cv2 as cv
import numpy as np

detector = dlib.get_frontal_face_detector()

vid = cv.VideoCapture(0)

while True:
	ret, frame = vid.read()

	# TBD: resize to speed-up 

	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

	dets = detector(gray, 1)
	print("Number of faces detected: {}".format(len(dets)))

	for i, d in enumerate(dets):
	  print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(i, d.left(), d.top(), d.right(), d.bottom()))
	  cv.rectangle(frame,(d.left(),d.top()),(d.right(),d.bottom()),(0,255,255),2)

	cv.imshow('faces', frame)

	if cv.waitKey(1) & 0xFF==ord('q'):
		break

vid.release()
cv.destroyAllWindows()
