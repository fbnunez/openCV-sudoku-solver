import imutils
import cv2
import numpy


def main():
    image = cv2.imread("./img/sudoku.png")
    image = imutils.resize(image, height=500)
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edgedImage = cv2.Canny(grayImage, threshold1=100,
                           threshold2=200, apertureSize=3)

    # VERTICAL LINES
    # 16 lines + doubles
    lines = cv2.HoughLinesP(image=edgedImage, rho=1, theta=numpy.pi,
                            threshold=100, lines=numpy.array([]), minLineLength=400, maxLineGap=5)


def negativeImage(lines, image):
    negativeImage = numpy.zeros_like(image)
    for line in lines:
        coords = line[0]
        x1, y1, x2, y2 = coords[0], coords[1], coords[2], coords[3]
        cv2.line(negativeImage, (x1, y1), (x2, y2), (0, 255, 0), 1)
    cv2.imshow("Input", negativeImage)
    cv2.waitKey(0)


main()
