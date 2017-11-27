#my project
import numpy as np
import cv2
import math
import time
import serial
counter = 0
cap = cv2.VideoCapture(0)

def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONCLK:
        cv2.circle(frame, (x,y), 100, (255, 0, 0), -1)

"""
img1 = cv2.resize(img1, None, fx = 2.5, fy = 2.5, interpolation = cv2.INTER_CUBIC)
img1 = cv2.medianBlur(img1, 11)
cv2.imshow('bg', img1)
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#img1 = cv2.threshold(img1,50,255,cv2.THRESH_BINARY)
kernel = np.ones((3,3),np.uint8)
lap = cv2.Laplacian(img1, cv2.CV_64F)
opening = cv2.morphologyEx(lap, cv2.MORPH_OPEN, kernel)
cv2.imshow('lmao', opening)
opening = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

cv2.imshow('lol', opening)

cv2.waitKey(0)
cv2.destroyAllWindows()
"""
counter = 0
past = np.zeros((2, 100))
velocity = np.zeros((2, 200))

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

def calc_velocity(positions):
    pxi = positions[0][(counter % 100) - 1]
    pxf = positions[0][counter % 100]
    vx = pxf - pxi

    pyi = positions[1][(counter % 100) - 1]
    pyf = positions[1][counter % 100]
    vy = pyf - pyi
    velocity[0][counter % 100] = vx
    velocity[1][counter % 100] = vy

while (True):
    ret, frame = cap.read()
    mask_clean = generate_mask(frame, "blue")
    _, contours, _ = cv2.findContours(mask_clean,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    max = 0
    index = 0


    if len(contours) > 0:
        for i in range(len(contours)):
            con = cv2.contourArea(contours[i])
            if (con > max):
                max = con
                index = i
        rect = cv2.minAreaRect(contours[index])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        #print("lol\n" + str(box))
        cv2.drawContours(frame, [box], 0, (255,0,0), 3)
        cx = ((box[0][0] - box[2][0]) / -2) + box[0][0]
        cy = ((box[0][1] - box[2][1]) / -2) + box[0][1]
        past[0][counter % 100] = int(cx)
        past[1][counter % 100] = int(cy)
        calc_velocity(past)
        counter += 1
        #print(counter)
        #print("lol\n" + str(past))

        """
        M = cv2.moments(contours[index])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        """
        for i in range(100):

            cv2.circle(frame, (int(past[0][i]), int(past[1][i])), 2, (0, 255 ,0), 3)

    cv2.imshow('final', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
#print(velocity)

"""
Notes:
OOP = object orientented programing -> classes
    -uses objects to program
        -student.grades = [99, 98, 64, 55]
        -student.class = 21
        -students.GPA = 2.7
        -def calc_GPA(self.grades):
            return GPA

        class Student(object):
            def __init__(self):
                self.grades
                self.class
                self.friends

            def grades_2_GPA(self, grades):
                #convert grades to GPA
                return self.GPA
            if __name__ == "__main__":
                student()

        jon = Student
        eamon = Student
        mork = Student

"""
