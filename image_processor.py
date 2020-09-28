import imutils
import cv2
import numpy
import pytesseract
import os
DEFAULT_HEIGHT, DEFAULT_WIDTH = 700, 700  # Image size
BOARD_SIZE = 9  # Square board: 9x9
DEFAULT_PIXEL_OFFSET = 5


def main():
    filename = './img/sudoku2.png'
    image = cv2.imread(filename)
    image = imutils.resize(
        image, height=DEFAULT_HEIGHT, width=DEFAULT_WIDTH)
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = numpy.ones((3, 3), numpy.uint8)
    edgedImage = cv2.Canny(grayImage, threshold1=50,
                           threshold2=200)

    # making the countour of the image so edges are more defined
    contours, hierarchy = cv2.findContours(grayImage,
                                           cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(grayImage, contours, -1, (0, 255, 0), 3)

    foundNumbers = []
    emptyRows = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            # finding each square position based in a 9x9 board
            y1 = y * (DEFAULT_HEIGHT//BOARD_SIZE)
            y2 = (y+1) * (DEFAULT_HEIGHT//BOARD_SIZE)
            x1 = x * (DEFAULT_WIDTH//BOARD_SIZE) + DEFAULT_PIXEL_OFFSET
            x2 = (x+1) * (DEFAULT_WIDTH//BOARD_SIZE)
            # cropping based on coordinates
            tempImage = grayImage[y1:y2, x1:x2]

            # Removing all black contours left from cropping the image (edges)
            # Getting the contour of the image
            # New coordinates: nX, nY, w, h
            # Cropping image again based on the new coordinates
            _, thresh = cv2.threshold(tempImage, 1, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnt = contours[0]
            nX, nY, w, h = cv2.boundingRect(cnt)  # new coordinates
            tempImage = tempImage[nY:nY+h, nX:nX+w]  # cropping

            # Resizing image making it easier for Tesseract
            # Applying blur as a form of antialiasing
            # Dilating the image in one iteration to trim black lines
            tempImage = imutils.resize(tempImage, width=110, height=110)
            tempImage = cv2.GaussianBlur(tempImage, (5, 5), 0)
            tempImage = cv2.dilate(tempImage, kernel, iterations=1)

            # Converting image to text using Tesseract
            text = pytesseract.image_to_string(
                tempImage, lang='eng', config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')
            text = str(text).strip().replace(' ', '')
            # print(text)
            # cv2.imshow("Input", tempImage)
            # cv2.waitKey(0)
            if text != '':
                foundNumbers.append(text)
            else:
                emptyRows.append('0')
    foundNumbers = numpy.array(foundNumbers)
    emptyRows = numpy.array(emptyRows)

    testResult(filename, foundNumbers)


def testResult(filename: str, numberArray: list):
    filename = filename.split('.png')[0]
    filenameNumber = filename[len(filename)-1:]
    if filenameNumber == '1':
        testArr = [5, 3, 7, 6, 1, 9, 5, 9, 8, 6, 8, 6, 3, 4,
                   8, 3, 1, 7, 2, 6, 6, 2, 8, 4, 1, 9, 5, 8, 7, 9]
    elif filenameNumber == '2':
        testArr = [3, 8, 5, 1, 2, 5, 7, 4, 1, 9, 5, 7, 3, 2, 1, 4, 9]
    # print(testArr)
    for index, number in enumerate(numberArray):
        try:
            if (int(number) == testArr[index]):
                print((True, number, testArr[index]))
            else:
                print((False, number, testArr[index]))
        except:
            print(False)


main()

# Below are openCV test functions used to understand some of the basic concepts - they were left here for basic documentation porposes
# It builds the outline of the given board and overlaps it with the grayscale version of it
# The idea of it was to understand how openCV behave given basic data and how to develop arround it
# Basic problems found where how trace lines were 'duplicates' and what steps were necessary to clean them
# In the future, maybe this basic premise of creating image outline data can be used by me to train or build generic data
# I know the code itself is not very original but it seemed like a good place to start


def __main():
    image = cv2.imread("./img/sudoku2.png")
    resizedImage = imutils.resize(
        image, height=DEFAULT_HEIGHT, width=DEFAULT_WIDTH)
    grayImage = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2GRAY)
    edgedImage = cv2.Canny(grayImage, threshold1=50,
                           threshold2=200)
    verticalLines = __getVerticalLines(edgedImage, resizedImage)
    horizontalLines = __getHorizontal(edgedImage, resizedImage)
    fullBoardLines = numpy.concatenate((verticalLines, horizontalLines))
    outlinesImage = __negativeImage(fullBoardLines, resizedImage)
    main = cv2.addWeighted(resizedImage, 0.9, outlinesImage, 1, 0)
    cv2.imshow("Press 0 (zero) or ESC to close screen", main)
    print('Press 0 (zero) or ESC to close screen')
    cv2.waitKey(0)


def __getHorizontal(edgedImage, resizedImage):
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


def __getVerticalLines(edgedImage, resizedImage):
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


def __negativeImage(lines, image):
    negativeImage = numpy.zeros_like(image)
    for line in lines:
        coords = line[0]
        x1, y1, x2, y2 = line[0]
        cv2.line(negativeImage, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # cv2.imshow("Input", negativeImage)
    # cv2.waitKey(0)
    return negativeImage


# __main()
