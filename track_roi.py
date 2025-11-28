import cv2

# Initialize CSRT tracker
tracker = cv2.TrackerCSRT_create()

# Open video stream
cap = cv2.VideoCapture(0) # Use 0 for webcam, or provide video file path

# Read the first frame
ret, frame = cap.read()

# Select ROI
bbox = cv2.selectROI("Tracking", frame, False, False)
print(bbox)

# Initialize tracker with ROI
tracker.init(frame, bbox)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Update tracker
    success, bbox = tracker.update(frame)

    if success:
        # Draw bounding box
        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Tracking failed", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    cv2.imshow("Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()