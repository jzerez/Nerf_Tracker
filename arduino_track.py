#my project
import numpy as np
import cv2
import math
import time
import serial


cap = cv2.VideoCapture(0)
counter = 0
ser = serial.Serial('thing', 9600)

def generate_mask(frame, color = "blue"):
    blur = cv2.GaussianBlur(frame, (7,7), 0)
    blur = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    if (color == "blue"):
        min_color = np.array([90, 50, 30])
        max_color = np.array([120, 255, 210])
    elif (color == "green"):
        min_color = np.array([40, 30, 20])
        max_color = np.array([80, 255,210])
    elif (color == "red"):
        min_color = np.array([-20, 50, 50])
        max_color = np.array([20, 255, 210])

    blur = cv2.GaussianBlur(frame, (7,7), 0)
    blur = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(blur, min_color, max_color)
    kernel = np.ones((3,3),np.uint8)
    mask_clean = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel)
    mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel)
    return mask_clean

def largest_contour(frame, contours):
    max = 0
    index = 0
    for i in range(len(contours)):
        con = cv2.contourArea(contours[i])
        if (con > max):
            max = con
            index = i
    rect = cv2.minAreaRect(contours[index])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    return box

def calc_coordinates(frame, countours):

    box = largest_contour(frame, contours)
    cv2.drawContours(frame, [box], 0, (255,0,0), 3)
    cx = ((box[0][0] - box[2][0]) / -2) + box[0][0]
    cy = ((box[0][1] - box[2][1]) / -2) + box[0][1]
    cv2.circle(frame, (cx, cy), 3, (0,255,0), 2)
    return cx, cy


while (True):
    ret, frame = cap.read()
    mask_clean = generate_mask(frame, "blue")
    _, contours, _ = cv2.findContours(mask_clean,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        x = calc_coordinates(frame, contours)[0]
        y = calc_coordinates(frame, contours)[1]
        ser.write("x = " + str(x))
        ser.write(", y = " + str(y))
        ser.write("\n")
    cv2.imshow('final', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
#print(velocity)
