import cv2
import math

tracker = cv2.TrackerCSRT_create()
cap = cv2.VideoCapture(0) # Use 0 for webcam, or provide video file path

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

tracker_state = False

bbox = None
success = None

points = []
point_color = (0, 250, 120)
point_radius = 2
point_thickness = -1


def get_bb(points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]

    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)

    #bounding_box = (min_x, min_y, max_x, max_y)
    return (min_x, min_y, max_x - min_x, max_y - min_y)


while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(gray)

    if tracker_state:
        success, bbox = tracker.update(frame)

    if ids is not None:
        if not tracker_state:
            p0 = (int(corners[0][0][0][0]), int(corners[0][0][0][1]))
            p1 = (int(corners[0][0][1][0]), int(corners[0][0][1][1]))
            p2 = (int(corners[0][0][2][0]), int(corners[0][0][2][1]))
            p3 = (int(corners[0][0][3][0]), int(corners[0][0][3][1]))
            bbox = get_bb([p0, p1, p2, p3]) # (x, y, width, height)
            
            tracker.init(frame, bbox)
            tracker_state = True            

        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        print(corners)

    if success:
        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        points.append((x, y))
    else:
        cv2.putText(frame, "Tracking failed", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    for point in points:
        cv2.circle(frame, point, point_radius, point_color, point_thickness)

    cv2.imshow("Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()