import imutils
import cv2
import numpy
DEFAULT_HEIGHT, DEFAULT_WIDTH = 500, 500


def main():
    image = cv2.imread("./img/sudoku.png")
    resizedImage = imutils.resize(
        image, height=DEFAULT_HEIGHT, width=DEFAULT_WIDTH)
    grayImage = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2GRAY)
    edgedImage = cv2.Canny(grayImage, threshold1=50,
                           threshold2=200)
    verticalLines = getVerticalLines(edgedImage, resizedImage)


def getVerticalLines(edgedImage, resizedImage):
    # VERTICAL LINES
    # 16 lines + doubles
    lines = cv2.HoughLinesP(image=edgedImage, rho=1, theta=numpy.pi,
                            threshold=100, lines=numpy.array([]), minLineLength=400, maxLineGap=250)
    linesToKeep = []
    PIXEL_TRESHOLD = 10
    for line1 in lines:
        for line2 in lines:
            if line1[0][0] < line2[0][0] and line1[0][0] + PIXEL_TRESHOLD > line2[0][0]:
                linesToKeep.append(line1)
            elif line1[0][0] < PIXEL_TRESHOLD:
                linesToKeep.append(line1)
            elif line1[0][0] >= DEFAULT_WIDTH - PIXEL_TRESHOLD:
                linesToKeep.append(line1)
    linesToKeep.append(lines[len(lines)-1])
    linesToKeep = numpy.array(linesToKeep)
    print(lines)
    negativeImage(linesToKeep, resizedImage)
    return linesToKeep


def negativeImage(lines, image):
    negativeImage = numpy.zeros_like(image)
    for line in lines:
        coords = line[0]
        x1, y1, x2, y2 = line[0]
        cv2.line(negativeImage, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow("Input", negativeImage)
    cv2.waitKey(0)


main()
