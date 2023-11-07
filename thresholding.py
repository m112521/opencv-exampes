import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def nothing(x):
    pass

cv.namedWindow('image')
cv.createTrackbar('Min','image', 0, 255, nothing)
cv.setTrackbarPos('Min', 'image', 127)

Min = 0
pMin  = 0

img = cv.imread('imgs/laser.jpg', cv.IMREAD_GRAYSCALE)
img = cv.resize(img, (0, 0), fx=0.25, fy=0.25)
img = cv.medianBlur(img, 5)

while True:
    min = cv.getTrackbarPos('Min','image')
    ret, th1 = cv.threshold(img, min, 255, cv.THRESH_BINARY)

    if (pMin != Min):
        pMin = Min


    cv.imshow('img', th1)
    if cv.waitKey(33) & 0xFF == ord('q'):
      break

cv.destroyAllWindows()


# img = cv.imread('imgs/laser.jpg', cv.IMREAD_GRAYSCALE)
# img = cv.medianBlur(img,5)

# ret, th1 = cv.threshold(img, 127, 255,cv.THRESH_BINARY)
# th2 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)
# th3 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

# titles = ['Original Image', 'Global Thresholding (v = 127)',
#             'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
# images = [img, th1, th2, th3]
# for i in range(4):
#     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])
# plt.show()