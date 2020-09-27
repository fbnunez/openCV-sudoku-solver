import imutils
import cv2
import numpy
from PIL import Image
import pytesseract
import argparse
import os
DEFAULT_HEIGHT, DEFAULT_WIDTH = 700, 700  # Image size
BOARD_SIZE = 9  # Square board: 9x9


def main():
    image = cv2.imread("./img/sudoku.png")
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
    # edgedImage = cv2.Canny(grayImage, threshold1=50, threshold2=200)

    # grayImage = cv2.dilate(grayImage, kernel, iterations=1)
    # cv2.imshow("out", grayImage)
    # cv2.waitKey(0)
    # exit(1)
    edgedSquaresImages = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            y1 = y * (DEFAULT_HEIGHT//BOARD_SIZE)
            y2 = (y+1) * (DEFAULT_HEIGHT//BOARD_SIZE)
            x1 = x * (DEFAULT_WIDTH//BOARD_SIZE)
            x2 = (x+1) * (DEFAULT_WIDTH//BOARD_SIZE)
            tempImage = grayImage[y1:y2, x1:x2]
            _, thresh = cv2.threshold(tempImage, 1, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnt = contours[0]
            nX, nY, w, h = cv2.boundingRect(cnt)
            tempImage = tempImage[nY:nY+h, nX:nX+w]
            tempImage = cv2.dilate(tempImage, kernel, iterations=1)
            # filename = f"./out/square_{y}_{x}.png"
            # cv2.imwrite(filename, tempImage)
            # _, img_binarized = cv2.threshold(
            #     tempImage, 100, 255, cv2.THRESH_BINARY)
            # pil_img = Image.fromarray(img_binarized)
            text = pytesseract.image_to_string(
                tempImage, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
            text = str(text).strip().replace(' ', '')
            # print(text)
            if text != '':
                print(text)
                cv2.imshow("out", tempImage)
                cv2.waitKey(0)
            # if text != '':
    # edgedSquaresImages.append(tempImage)
    # text = pytesseract.image_to_string(Image.open('./out/square_1_5.png'))
    # # os.remove(filename)


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
