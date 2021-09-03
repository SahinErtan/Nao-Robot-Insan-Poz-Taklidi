"""
11-22 arasi tum pozlar kollar ile ilgili
"""
"""
HeadYaw - HeadPitch
LShoulderPitch - LShoulderRoll - LElbowYaw - LElbowRoll - LWristYaw
RShoulderPitch - RShoulderRoll - RElbowYaw - RElbowRoll - RWristYaw
LHand - RHand
LHipYawPitch - RHipYawPitch
LHipRoll - LHipPitch - LKneePitch - LAnklePitch - LAnkleRoll
RHipRoll - RHipPitch - RKneePitch - RAnklePitch - RAnkleRoll
"""
"""
(-119.5 ile 119.5) - 
Joint name	Range (degrees)	Range (radians)
HeadYaw	    -119.5 to 119.5	-2.0857 to 2.0857
HeadPitch   -38.5 to 29.5	-0.6720 to 0.5149
LShoulderPitch	-119.5 to 119.5	-2.0857 to 2.0857
LShoulderRoll	-18 to 76	-0.3142 to 1.3265
LElbowYaw	-119.5 to 119.5	-2.0857 to 2.0857
LElbowRoll	-88.5 to -2	-1.5446 to -0.0349
LWristYaw	-104.5 to 104.5	-1.8238 to 1.8238
LHand	Open and Close	Open and Close
RShoulderPitch	-119.5 to 119.5	-2.0857 to 2.0857
RShoulderRoll	-76 to 18	-1.3265 to 0.3142
RElbowYaw	-119.5 to 119.5	-2.0857 to 2.0857
RElbowRoll	2 to 88.5	0.0349 to 1.5446
RWristYaw	-104.5 to 104.5	-1.8238 to 1.8238
RHand	Open and Close	Open and Close
LHipYawPitch	-65.62 to 42.44	-1.145303 to 0.740810
RHipYawPitch*	-65.62 to 42.44	-1.145303 to 0.740810
LHipRoll	-21.74 to 45.29	-0.379472 to 0.790477
LHipPitch	-88.00 to 27.73	-1.535889 to 0.484090
LKneePitch	-5.29 to 121.04	-0.092346 to 2.112528
LAnklePitch	-68.15 to 52.86	-1.189516 to 0.922747
LAnkleRoll	-22.79 to 44.06	-0.397880 to 0.769001
RHipRoll	-45.29 to 21.74	-0.790477 to 0.379472
RHipPitch	-88.00 to 27.73	-1.535889 to 0.484090
RKneePitch	-5.90 to 121.47	-0.103083 to 2.120198
RAnklePitch	-67.97 to 53.40	-1.186448 to 0.932056
RAnkleRoll	-44.06 to 22.80	-0.768992 to 0.397935

"""

import sys
import time
from naoqi import ALProxy
import math
import numpy



def getLimits(jointName):

    try:
        motionProxy = ALProxy("ALMotion", "127.0.0.1", 9559)
    except Exception,e:
        print "Could not create proxy to ALMotion"
        print "Error was: ",e
        sys.exit(1)

    # Example showing how to get the limits for the whole body
    # name = "Body"
    print jointName
    limits = motionProxy.getLimits(jointName)
    # jointNames = motionProxy.getBodyNames(name)
    # for i in range(0,len(limits)):
    #     print jointNames[i] + ":"
    #     print "minAngle", limits[i][0],\
    #         "maxAngle", limits[i][1],\
    #         "maxVelocity", limits[i][2],\
    #         "maxTorque", limits[i][3]
    return limits



def setValue(jointName,value,realJointParam,axis=0,valueType=0):   # valueType=> 0-radian 1-length

    if (valueType == 0):    # For radian value
        limits = getLimits(jointName)
        print limits
        print limits[0][0]
        print limits[0][1]
        if(axis==0):    # Ilk parametre en kapali deger ( For Right Joints )
            limitedJointParam = [limits[0][0],limits[0][1]]
        elif(axis==1):  # Ikinci parametre en kapali deger ( For Left Joints )
            limitedJointParam = [limits[0][1], limits[0][0]]
        print(limitedJointParam)
        return numpy.interp(value,realJointParam,limitedJointParam)

    elif (valueType == 1):
        limits = getLimits(jointName)
        if (axis == 0):  # Ilk parametre en kapali deger ( For Right Joints )
            limitedJointParam = [limits[0][0], limits[0][1]]
        elif (axis == 1):  # Ikinci parametre en kapali deger ( For Left Joints )
            limitedJointParam = [limits[0][1], limits[0][0]]
        print(limitedJointParam)
        return numpy.interp(value, realJointParam, limitedJointParam)



def komut(jointName,value):
    names = list()
    times = list()
    keys = list()
    robotIP = "127.0.0.1"  # "192.168.11.3"

    port = 9559  # 9559 # Insert NAO port

    ETime=0.05

    if(jointName=="LElbowRoll"):    # -1.5446 to -0.0349
        value = setValue(jointName, value, [50, 450], axis = 0, valueType = 1)
        names.append("LElbowRoll")
        times.append([ETime])
        keys.append([value])


    # names.append("LElbowYaw")
    # times.append([ETime])
    # keys.append([])
    #
    # names.append("LHand")
    # times.append([ETime])
    # keys.append([])
    #
    # names.append("LShoulderPitch")
    # times.append([ETime])
    # keys.append([])
    if(jointName=="LShoulderRoll"):
        value = setValue(jointName, value, [3.14, 4.71],axis=1)
        names.append("LShoulderRoll")   # -0.3142 to 1.3265
        times.append([ETime])
        keys.append([value])
    #
    # names.append("LWristYaw")
    # times.append([ETime])
    # keys.append([])
    #
    if(jointName=="RElbowRoll"):
        value = setValue(jointName, value, [50, 450], axis = 1, valueType = 1)
        names.append("RElbowRoll")
        times.append([ETime])
        keys.append([value])
    #
    # names.append("RElbowYaw")
    # times.append([ETime])
    # keys.append([])
    #
    # names.append("RHand")
    # times.append([ETime])
    # keys.append([])

    # names.append("RShoulderPitch")
    # times.append([ETime])
    # keys.append([])

    if (jointName == "RShoulderRoll"):
        value = setValue(jointName, value, [1.57,3.14], axis=1)
        names.append("RShoulderRoll")   # -1.3265 to 0.3142
        times.append([ETime])
        keys.append([value])

    # names.append("RWristYaw")
    # times.append([ETime])
    # keys.append([])
    print(value)
    try:
      # uncomment the following line and modify the IP if you use this script outside Choregraphe.
      # motion = ALProxy("ALMotion", IP, 9559)
      motion = ALProxy("ALMotion", robotIP, port)
      motion.angleInterpolationBezier(names, times, keys)
    except BaseException, err:
      print err
      print ("hatali ", jointName)





def main():
    print("Baslangic Konumuna Geliniz")

    try:
      motion = ALProxy("ALMotion", robotIP, port)
      motion.wakeUp()
      getLimits(port)
    except BaseException, err:
      print err

    # time.sleep(3)

    lastLm = []
    while(True):

        lm = []
        with open("C:/Users/ASUS/PycharmProjects/ProjectNao/poz.csv","r") as file:
            for satir in file:
                lm.append(satir.split(";"))

        if(lm!=lastLm):
            jointList = []
            # print(lm)
            try:

                print(lm[0][2],lm[1][2])
                print(lm)
                print(lm[0][1])
                radian = lm[0][1]
                # deger = numpy.interp(radian,[1.57,3.14],[0.3142, -1.3265])
                komut("RShoulderRoll", radian)

                radian = lm[1][1] # -0.3142 to 1.3265
                # deger = numpy.interp(radian,[3.14,4.71],[1.3265, -0.3142])
                komut("LShoulderRoll", radian)

                length = lm[2][1]
                komut("RElbowRoll",length)

                length = lm[3][1]
                komut("LElbowRoll", length)

            except BaseException, err:
                print err

        lastLm=lm
        # angle = hesapla(lm)
        # radian=math.radians(angle)
        # komut("127.0.0.1", 9559,radian)




if __name__ == "__main__":

    robotIP = "127.0.0.1"  # "192.168.11.3"

    port = 9559  # 9559 # Insert NAO port

    if len(sys.argv) <= 1:
        print"(robotIP default: 127.0.0.1)"
    elif len(sys.argv) <= 2:
        robotIP = sys.argv[1]
    else:
        port = int(sys.argv[2])
        robotIP = sys.argv[1]

    main()

"""
StandInit
# Choregraphe simplified export in Python.
from naoqi import ALProxy
names = list()
times = list()
keys = list()

names.append("HeadPitch")
times.append([0.16])
keys.append([-0.00335425])

names.append("HeadYaw")
times.append([0.16])
keys.append([0])

names.append("LAnklePitch")
times.append([0.16])
keys.append([-0.341318])

names.append("LAnkleRoll")
times.append([0.16])
keys.append([-0.00256276])

names.append("LElbowRoll")
times.append([0.16])
keys.append([-1.00737])

names.append("LElbowYaw")
times.append([0.16])
keys.append([-1.38892])

names.append("LHand")
times.append([0.16])
keys.append([0.25845])

names.append("LHipPitch")
times.append([0.16])
keys.append([-0.449367])

names.append("LHipRoll")
times.append([0.16])
keys.append([0.00635712])

names.append("LHipYawPitch")
times.append([0.16])
keys.append([-0.00335943])

names.append("LKneePitch")
times.append([0.16])
keys.append([0.694895])

names.append("LShoulderPitch")
times.append([0.16])
keys.append([1.4098])

names.append("LShoulderRoll")
times.append([0.16])
keys.append([0.292504])

names.append("LWristYaw")
times.append([0.16])
keys.append([0.00538665])

names.append("RAnklePitch")
times.append([0.16])
keys.append([-0.341319])

names.append("RAnkleRoll")
times.append([0.16])
keys.append([0.0025626])

names.append("RElbowRoll")
times.append([0.16])
keys.append([1.00737])

names.append("RElbowYaw")
times.append([0.16])
keys.append([1.38892])

names.append("RHand")
times.append([0.16])
keys.append([0.25845])

names.append("RHipPitch")
times.append([0.16])
keys.append([-0.449375])

names.append("RHipRoll")
times.append([0.16])
keys.append([-0.0065374])

names.append("RHipYawPitch")
times.append([0.16])
keys.append([-0.00335943])

names.append("RKneePitch")
times.append([0.16])
keys.append([0.69489])

names.append("RShoulderPitch")
times.append([0.16])
keys.append([1.4098])

names.append("RShoulderRoll")
times.append([0.16])
keys.append([-0.292498])

names.append("RWristYaw")
times.append([0.16])
keys.append([0.00538664])

try:
  # uncomment the following line and modify the IP if you use this script outside Choregraphe.
  # motion = ALProxy("ALMotion", IP, 9559)
  motion = ALProxy("ALMotion")
  motion.angleInterpolation(names, keys, times, True)
except BaseException, err:
  print err

"""
