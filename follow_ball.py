# !/usr/bin/env python3

from __future__ import division
import cv2
import numpy as np
from ObjectInfo import ObjectInfo
import conexion_arduino


def nothing(*arg):
    print("Nothing!!!")
    pass


def get_percentage(value):

    result = int(value * 100 / FRAME_WIDTH)
    if result > 100:
        return 100
    elif result < 0:
        return 0
    else:
        return result


icol = (93, 76, 47, 139, 198, 133, 31000)

cv2.namedWindow('colorTest')

# # Lower range colour sliders.
cv2.createTrackbar('lowHue', 'colorTest', icol[0], 255, nothing)
cv2.createTrackbar('lowSat', 'colorTest', icol[1], 255, nothing)
cv2.createTrackbar('lowVal', 'colorTest', icol[2], 255, nothing)
# # Higher range colour sliders.
cv2.createTrackbar('highHue', 'colorTest', icol[3], 255, nothing)
cv2.createTrackbar('highSat', 'colorTest', icol[4], 255, nothing)
cv2.createTrackbar('highVal', 'colorTest', icol[5], 255, nothing)

# # Area Value
cv2.createTrackbar('MinArea', 'colorTest', icol[6], 31000, nothing)

# Initialize camera
vidCapture = cv2.VideoCapture(0)

FRAME_WIDTH = vidCapture.get(3)
FRAME_HEIGHT = vidCapture.get(4)

RESIZED_WIDTH = int(FRAME_WIDTH/1)
RESIZED_HEIGHT = int(FRAME_HEIGHT/1)

# Secciones

number_of_sections = 32
sections = []

distance_between_lines = FRAME_HEIGHT / number_of_sections

for x in range(1, number_of_sections):
    pt1 = (0, int(distance_between_lines) * x)
    pt2 = (int(FRAME_WIDTH), int(distance_between_lines) * x)
    sections.append((pt1, pt2))

 # Crea el objeto de la bola

ball = ObjectInfo(FRAME_WIDTH, FRAME_HEIGHT, number_of_sections)

trayectory = None

while True:

    e1 = cv2.getTickCount()

    # Get HSV values from the GUI sliders.
    lowHue = cv2.getTrackbarPos('lowHue', 'colorTest')
    lowSat = cv2.getTrackbarPos('lowSat', 'colorTest')
    lowVal = cv2.getTrackbarPos('lowVal', 'colorTest')
    highHue = cv2.getTrackbarPos('highHue', 'colorTest')
    highSat = cv2.getTrackbarPos('highSat', 'colorTest')
    highVal = cv2.getTrackbarPos('highVal', 'colorTest')
    min_area = cv2.getTrackbarPos('MinArea', 'colorTest')


    # Get webcam frame
    _, frame = vidCapture.read()

    # Convert the frame to HSV colour model.
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # HSV values to define a colour range we want to create a mask from.
    colorLow = np.array([lowHue, lowSat, lowVal])
    colorHigh = np.array([highHue, highSat, highVal])
    mask = cv2.inRange(frameHSV, colorLow, colorHigh)
    # Show the first mask
    cv2.imshow('mask-plain', mask)

    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]

    if contour_sizes:

        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

        area = cv2.contourArea(biggest_contour)

        if area > min_area:
            x, y, w, h = cv2.boundingRect(biggest_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            M = cv2.moments(biggest_contour)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            x, y, w, h = cv2.boundingRect(biggest_contour)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            trayectory = ball.add_position((int(cx), int(cy)))

            conexion_arduino.send_serial(get_percentage(trayectory[1][0]))


    for x in range(number_of_sections - 1):
        cv2.line(frame, sections[x][0], sections[x][1], (0, 0, 255), 1)

    if trayectory:
        cv2.line(frame, trayectory[0], trayectory[1], (0, 0, 255), 2)

    # Show final output image
    resized = cv2.resize(frame, (RESIZED_WIDTH, RESIZED_HEIGHT), interpolation=cv2.INTER_AREA)
    cv2.imshow('colorTest', resized)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

    e2 = cv2.getTickCount()
    time = (e2 - e1) / cv2.getTickFrequency()
    print(time)

cv2.destroyAllWindows()
vidCapture.release()
