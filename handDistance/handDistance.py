import cv2
import numpy as np
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector
import math
import cvzone

#webcam
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

#hand detector
detector = HandDetector(detectionCon=0.8,maxHands=1)

#Find Function
x= [300,245,200,170,145,130,112,103,93,87,80,75,70,67,62,59,57]
y= [40, 50, 60, 70, 80, 90, 100,110,120,130,140,150,160,170,180,190,200]
coff= np.polyfit(x,y,2)

#game variable

cx,cy = 250,250
color=(255,0,255)

while True:
    success,img = cap.read()
    img = cv2.flip(img,1)
    hands,img = detector.findHands(img ,draw=False)

    if hands:
        lmList =  hands[0]['lmList']
        x,y,w,h = hands[0]['bbox']
        x1 , y1 ,_ = lmList[5]
        x2 , y2 ,_ = lmList[17]
        distance = math.hypot(x2-x1 , y2-y1)
        A , B ,C = coff
        distanceCM = A* distance**2 + B*distance + C

        if distanceCM <40:
            if x<cx<x+w and y<cy<y+h:
                color = (0,255,0)
        else:
            color= (255,0,255)


        #print(distanceCM , distance)
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),3)
        cvzone.putTextRect(img , f'{int(distanceCM)} cm',(x+5,y-10) )
        
    #draw button
    cv2.circle(img,(cx,cy),30,color,cv2.FILLED)
    cv2.circle(img,(cx,cy),10,(255,255,255),cv2.FILLED)
    cv2.circle(img,(cx,cy),20,(255,255,255),2)

    #game hud
    cvzone.putTextRect(img,'Time: 30',(1000,75),scale=3,offset = 10)
    cvzone.putTextRect(img,'Score: 04',(60,75),scale=3,offset = 10)


    cv2.imshow("Image",img)
    cv2.waitKey(1)
