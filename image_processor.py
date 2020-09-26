import imutils
import cv2
import numpy
DEFAULT_HEIGHT, DEFAULT_WIDTH = 500, 500


def main():
    image = cv2.imread("./img/sudoku2.png")
    resizedImage = imutils.resize(
        image, height=DEFAULT_HEIGHT, width=DEFAULT_WIDTH)
    grayImage = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2GRAY)
    edgedImage = cv2.Canny(grayImage, threshold1=50,
                           threshold2=200)
    verticalLines = getVerticalLines(edgedImage, resizedImage)
    horizontalLines = getHorizontal(edgedImage, resizedImage)
    fullBoardLines = numpy.concatenate((verticalLines, horizontalLines))
    negativeLines = negativeImage(fullBoardLines, resizedImage)
    main = cv2.addWeighted(resizedImage, 0.9, negativeLines, 1, 0)
    cv2.imshow("out", main)
    cv2.waitKey(0)


def getHorizontal(edgedImage, resizedImage):
    lines = cv2.HoughLinesP(image=edgedImage, rho=1, theta=numpy.pi/2,
                            threshold=100, lines=numpy.array([]), minLineLength=400, maxLineGap=250)
    horizontalLines = []
    PIXEL_TRESHOLD = 10
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(y1 - y2) == 0:
            horizontalLines.append(line)
    horizontalLines = numpy.array(horizontalLines)
    linesToKeep = []
    for line1 in horizontalLines:
        for line2 in horizontalLines:
            if line1[0][1] < line2[0][1] and line1[0][1] + PIXEL_TRESHOLD > line2[0][1]:
                linesToKeep.append(line1)
            elif line1[0][1] < PIXEL_TRESHOLD:
                linesToKeep.append(line1)
            elif line1[0][1] >= DEFAULT_HEIGHT - PIXEL_TRESHOLD:
                linesToKeep.append(line1)
    linesToKeep = numpy.array(linesToKeep)
    # negativeImage(linesToKeep, resizedImage)
    return linesToKeep


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
    # print(lines)
    # negativeImage(linesToKeep, resizedImage)
    return linesToKeep


def negativeImage(lines, image):
    negativeImage = numpy.zeros_like(image)
    for line in lines:
        coords = line[0]
        x1, y1, x2, y2 = line[0]
        cv2.line(negativeImage, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # cv2.imshow("Input", negativeImage)
    # cv2.waitKey(0)
    return negativeImage


main()
