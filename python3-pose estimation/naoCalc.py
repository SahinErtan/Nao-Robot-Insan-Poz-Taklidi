import math
from cv2 import cv2

def CalcDegree(img,lm1,lm2,lm3,draw=False):

    #RShoulderRoll Hesabi

    x1, y1 = float(lm1[1]), float(lm1[2])
    x2, y2 = float(lm2[1]), float(lm2[2])
    x3, y3 = float(lm3[1]), float(lm3[2])

    x1,y1 = int(x1),int(y1)
    x2, y2 = int(x2), int(y2)
    x3, y3 = int(x3), int(y3)

    angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
    if(angle<=0): angle+=360

    # radian = math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)
    radian = math.radians(angle)
    if (angle <= 0): angle += 360

    # cv2.putText(img,str(int(angle)),(x2+10,y2+10),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),2)
    return angle, radian

def CalcLength(img,lm1,lm2,draw=False):

    x1,y1 = lm1[1], lm1[2]
    x2, y2 = lm2[1], lm2[2]

    length = math.hypot(x2-x1, y2-y1)

    return length

def Calculate(img,lm):

    listRadianofLm=[]

    angle, radian = CalcDegree(img,lm[11],lm[12],lm[14])    #RShoulderRoll 90 to 270
    listRadianofLm.append([0,radian,angle])

    angle, radian = CalcDegree(img,lm[12],lm[11],lm[13])    #LShoulderRoll 270 to 90
    listRadianofLm.append([1, radian, angle])

    length = CalcLength(img, lm[12], lm[16])    #RElbowRoll
    listRadianofLm.append([2, length])

    length = CalcLength(img, lm[11], lm[15])    #LElbowRoll
    listRadianofLm.append([3, length])

    return listRadianofLm

    # if jointName == "RShoulderRoll":
    # if jointName == "LShoulderRoll":
    # if jointName == "ShoulderRoll":
    #     pass
    # if jointName == "ShoulderRoll":
    #     pass
    # if jointName == "ShoulderRoll":
    #     pass
    # if jointName == "ShoulderRoll":
    #     pass