import cv2

qcd = cv2.QRCodeDetector()

img = cv2.imread("imgs/qrtest3.PNG")
# img = cv2.imread("imgs/qrtest_plywod.PNG")

decoded, bbox, _  = qcd.detectAndDecode(img)
print(decoded)

if decoded:
    img = cv2.polylines(img, bbox.astype(int), True, (0, 255, 0), 3)
    cv2.imwrite('imgs/qrcode_opencv2.jpg', img)
else:
    print("No QR found")
