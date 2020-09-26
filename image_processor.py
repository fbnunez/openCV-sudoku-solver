import imutils
import cv2

image = cv2.imread("./img/sudoku.png")
image = imutils.resize(image, height=500)
grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Input", grayImage)

cv2.waitKey(0)
