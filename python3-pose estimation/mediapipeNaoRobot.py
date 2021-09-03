"""
11 left Shouler
12 Right Shoulder
13 Left Elbow
14 Right Elbow
15 Left Wrist
16 Right Wrist
17 left Pinky
18 Right Pinky
19 Legt Index
20 Right Index
21 Left Thumb
22 Right Thumb
"""


from cv2 import cv2
import mediapipe as mp
import numpy as np
import time
import csv
import math
import naoCalc


def hesapla(img,lm):

    #RShoulderRoll Hesabi

    x1, y1 = float(lm[11][1]), float(lm[11][2])
    x2, y2 = float(lm[12][1]), float(lm[12][2])
    x3, y3 = float(lm[14][1]), float(lm[14][2])

    x1,y1 = int(x1),int(y1)
    x2, y2 = int(x2), int(y2)
    x3, y3 = int(x3), int(y3)

    angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
    if(angle<=0): angle+=360
    print(angle)
    radian = math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)
    if (angle <= 0): angle += 360
    print(angle - 90, radian)
    cv2.putText(img,str(int(angle)),(x2+10,y2+10),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),2)
    return angle

# cap=cv2.VideoCapture("vid/3.mp4")
cap= cv2.VideoCapture(0)

width=640
height=480

mpPose = mp.solutions.pose
pose = mpPose.Pose()

# mpHand = mp.solutions.hands
# hands=mpHand.Hands()

mpDraw = mp.solutions.drawing_utils

pTime = 0

while cap.isOpened():

    success, img = cap.read()
    # img=cv2.flip(img,1)
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    results = pose.process(imgRGB)


    if results.pose_landmarks:
        listLandmark = []
        lm=results.pose_landmarks
        mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        # print(results.pose_landmarks)

        for id, lm in enumerate(results.pose_landmarks.landmark):

            cx,cy,cz,cv=lm.x , lm.y,lm.z,lm.visibility
            # print(id,cx,cy,cz,cv)
            listLandmark.append([id,cx*width,cy*height,cz,cv])
            # cv2.circle(img,(int(cx*width),int(cy*height)),5,(0,255,255),cv2.FILLED)

        listRadianofLm = naoCalc.Calculate(img,listLandmark)

        with open("C:/Users/ASUS/PycharmProjects/ProjectNao/poz.csv", "w", encoding="utf-8") as csvfile:
            # print("yaziyorum")

            spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for lm in listRadianofLm:
                spamwriter.writerow(lm)

        # print(listLandmark[11],listLandmark[13])
        # hesapla(img,listLandmark)
        print(listRadianofLm)
        # print(listLandmark[13][2],listLandmark[15][2])







    # resultsHand = hands.process(imgRGB)
    #
    #
    # if resultsHand.multi_hand_landmarks:
    #     lms = resultsHand.multi_hand_landmarks
    #     listLandmark = []
    #     lastId = 0
    #     for handLms in resultsHand.multi_hand_landmarks:
    #         # print(handLms)
    #         mpDraw.draw_landmarks(img,handLms,mpHand.HAND_CONNECTIONS)
    #
    #
    #         for newId, lm in enumerate(handLms.landmark):
    #             id = newId + lastId
    #             cx,cy=lm.x , lm.y
    #             print(id,cx,cy)
    #             listLandmark.append([id,cx,cy])
    #
    #         lastId=20
    #
    #
    #     with open("C:/Users/ASUS/PycharmProjects/ProjectNao/poz.csv","w", encoding="utf-8") as csvfile:
    #         print("yaziyorum")
    #
    #         spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #
    #         for lm in listLandmark:
    #             spamwriter.writerow(lm)



    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f"FPS: {int(fps)}",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)

    cv2.imshow("IMG",img)
    cv2.waitKey(1)



"""
Gonderilen pose listesi ve aciklamasi (index , radian , derece)
0 => Kucuk deger kapali, buyuk deger kol acik demek
1 => Kucuk deger acik, buyuk deger kol kapali demek
"""