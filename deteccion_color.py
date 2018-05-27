#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import cv2
import conexion_arduino as arduino
import numpy as np
from ObjectInfo import ObjectInfo

kernelOp = np.ones((3, 3), np.uint8)
kernelCl = np.ones((11, 11), np.uint8)

areaTH = 1500

font = cv2.FONT_HERSHEY_SIMPLEX


def seguir_color(color):

    cap = cv2.VideoCapture(0)

    # Margen de color
    if color == "azul":
        lower = np.array([100, 0, 0])
        upper = np.array([255, 120, 120])

    elif color == "rojo":
        lower = np.array([0, 0, 70])
        upper = np.array([40, 40, 255])

    elif color == "verde":
        lower = np.array([0, 60, 0])
        upper = np.array([60, 255, 60])

    else:
        return 0

    # Dimensiones de la captura
    width_frame = cap.get(3)
    height_frame = cap.get(4)

    print("width ", width_frame, " height ", height_frame)


    # Secciones

    number_of_sections = 32
    sections = []

    distance_between_lines = height_frame / number_of_sections

    for x in range(1, number_of_sections):
        pt1 = (0, int(distance_between_lines) * x)
        pt2 = (int(width_frame), int(distance_between_lines) * x)
        sections.append((pt1, pt2))


    # Crea el objeto de la bola

    ball = ObjectInfo(width_frame, height_frame, number_of_sections)

    trayectory = None

    while True:

        _, frame = cap.read()

        mask = cv2.inRange(frame, lower, upper)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOp)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelCl)

        _, contours0, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours0:
            area = cv2.contourArea(cnt)
            if area > areaTH:
                # cv2.drawContours(frame, cnt, -1, (0,255,0), 3, 8)
                M = cv2.moments(cnt)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.putText(frame, str(area), (x, y), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                trayectory = ball.add_position((int(cx), int(cy)))

                print(trayectory[0], trayectory[1])


                # if cx < 140 or cx > 200:
                #
                #     if cx < 140:
                #         arduino.enviardato(b'1')
                #     elif cx > 200:
                #         arduino.enviardato(b'2')
                #
                # if cy < 100 or cy > 170:
                #
                #     if cy < 100:
                #         arduino.enviardato(b'4')
                #     elif cy > 180:
                #         arduino.enviardato(b'3')

        for x in range(number_of_sections - 1):
            cv2.line(frame, sections[x][0], sections[x][1], (0, 0, 255), 1)

        if trayectory:
             cv2.line(frame, trayectory[0], trayectory[1], (0, 0, 255), 2)

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Finalizó completamente")
