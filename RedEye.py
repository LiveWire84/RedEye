import cv2
import numpy as np
import dlib
from math import hypot
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
yawn = 0
sleep = 0
roi = 0
roi_gray =0
def Coord(l, x):
    return l.part(x).x, l.part(x).y


while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        #x, y = face.left(), face.top()
        #x[1], y[1] = face.right(), face.bottom()
        #cv2.rectangle(frame, (x,y), (x[1],y[1]), (0, 255, 0), 2)
        #Eyes
        l = predict(gray, face)
        x, y = [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]
        x[0], y[0] = Coord(l, 36)
        x[1], y[1] = Coord(l, 39)
       # cv2.line(frame, (x[0], y[0]), (x[1], y[1]), (0, 0, 255), 2)
        x[2], y[2] = int((l.part(37).x + l.part(38).x) / 2), int((l.part(37).y + l.part(38).y) / 2)
        x[3], y[3] = int((l.part(40).x + l.part(41).x) / 2), int((l.part(40).y + l.part(41).y) / 2)
       # cv2.line(frame, (x[2], y[2]), (x[3], y[3]), (0, 0, 255), 2)
        x[4], y[4] = Coord(l, 42)
        x[5], y[5] = Coord(l, 45)
       # cv2.line(frame, (x[4], y[4]), (x[5], y[5]), (0, 0, 255), 2)
        x1, y1 = Coord(l, 43)
        x2, y2 = Coord(l, 44)
        x[6], y[6] = int((x1 + x2)/2), int((y1 + y2)/2)
        x1, y1 = Coord(l, 46)
        x2, y2 = Coord(l, 47)
        x[7], y[7] = int((x1 + x2)/2), int((y1 + y2)/2)
      #  cv2.line(frame, (x[6], y[6]), (x[7], y[7]), (0, 0, 255), 2)
        horizontal = [hypot(x[0] - x[1], y[0] - y[1]), hypot(x[4] - x[5], y[4] - y[5])]
        vertical = [hypot(x[2] - x[3], y[2] - y[3]), hypot(x[6] - x[7], y[6] - y[7])]
        #print(vertical[0]/horizontal[0], vertical[1]/horizontal[1])
        if vertical[0]/horizontal[0] <= 0.2 and vertical[1]/horizontal[1] <= 0.2:
            sleep += 1
        elif vertical[0]/horizontal[0] >= 0.2 and vertical[1]/horizontal[1] >= 0.2:
            sleep = 0
        if sleep >= 10:
            print('Go On A Hike - Harry Lewis')
        #Yawn
        ptx, pty = [0, 0, 0, 0], [0, 0, 0, 0]
        for i in range(len(ptx)):
            ptx[i], pty[i] = Coord(l, 48 + 3*i)
          #  cv2.circle(frame, (ptx[i], pty[i]), 2, (0, 255, 0), 2)
        length = hypot(ptx[0] - ptx[2], pty[0] - pty[2])
        breadth = hypot(ptx[1] - ptx[3], pty[1] - pty[3])
        if breadth/length >= 0.7:
            yawn += 1
        elif breadth/length < 0.7:
            yawn = 0
        if yawn >= 10:
            print('Please Take A Break And Wash Your Eyes')
        x3, y3 = Coord(l, 22)
        x4, y4 = Coord(l, 15)
      #  cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255))
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(30)
    if key == 27:
        break
cv2.destroyAllWindows()
cap.release()
