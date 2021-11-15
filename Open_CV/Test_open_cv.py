import sys
import numpy as np
import cv2 as cv
fn = r"Test.jpg"
img = cv.imread(fn)
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, img = cv.threshold(img, 127, 255, 0)
img = img[60:500, 200:400]
img = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
cv.imshow('Test', img)
cv.waitKey()
cv.destroyAllWindows()