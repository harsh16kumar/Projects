import cv2
import mediapipe as mp
import numpy as np
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
cap.set(3,1288)
cap.set(4,720)
detector = htm.handDetector(detectionCon=0.8)
colorR = (255,0,0)

#cx, cy, w, h = 100, 100,200, 200

class DragRect():
    def __init__(self,posCenter,size=[200,200]):
        self.posCenter = posCenter
        self.size = size

    def update(self,cursor):
        cx,cy = self.posCenter
        w,h = self.size

        if cx-w//2<cursor[1]<cx+w//2 and cy-h//2//2<cursor[2]<cy+h//2:
            cx, cy = cursor[1], cursor[2]
            self.posCenter = (cx,cy)

rectList = []
for x in range(5):
    rectList.append(DragRect([x*250+150,150]))


while True:
    success , img = cap.read()
    img = cv2.flip(img ,1) #invert left right
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if lmList:
        distTip = detector.findDistance(8,12,img)
        if distTip < 60:
            cursor = lmList[8] 
            for rect in rectList:
                rect.update(cursor)

    #Draw
    for rect in rectList:
        cx,cy = rect.posCenter
        w,h = rect.size
        cv2.rectangle(img , (cx-w//2,cy-h//2) ,(cx+w//2,cy+h//2) ,
                    colorR,cv2.FILLED)

    cv2.imshow("Image" , img)
    cv2.waitKey(1)