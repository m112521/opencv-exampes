import face_recognition
import cv2
import numpy as np

# 1. Slow version on a large frame
# 2. Faster version with resized frame

# 3> Face recognition

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    sm_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    try:
        top, right, bottom, left = face_recognition.face_locations(sm_frame)[0] # take only first face
        cv2.rectangle(frame, (left*4, top*4), (right*4, bottom*4), (0, 0, 255), 2)
    except:
        pass

    cv2.imshow("Face detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
