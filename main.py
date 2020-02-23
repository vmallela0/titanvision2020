import sensor
import image
import time
import math
import ustruct
from pyb import USB_VCP, CAN

# Specify communication method: "print" "usb" "can"
COMMS_METHOD = "print"
TARGET_WIDTH = 39.25
TARGET_HEIGHT = 17.00
HISTORY_LENGTH = 10

# make USB_VCP object
usb = USB_VCP()

SCREEN_CENTERP = 80 # screen center (pixels) horizontal
VERTICAL_CENTERP = 60 # screen center (pixels) vertical

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.RGB565
sensor.set_framesize(sensor.QQVGA) # or sensor.QVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
clock = time.clock()

# setting autoexposure automatically
KMAN = 0.065 # constant for exposure setting
autoExposureSum = 0
readExposureNum = 10
for i in range(readExposureNum):
   autoExposureSum += sensor.get_exposure_us()

autoExposure = autoExposureSum/readExposureNum
manualExposure = int(autoExposure * KMAN) # scalefactor for decreasing autoExposure
sensor.set_auto_exposure(False,  manualExposure) # autoset exposures

values_history = [] # for median function

# LAB color space
thresholds = [(10, 100), (-128, -24), (-48, 51)]


HFOV = 70.8 # horizontal field of view
VFOV = 55.6 # vertical field of view

def drawScope(img, blob):
    # scope view
    img.draw_cross(blob.cx(), (int(blob.cy() - (blob.h()/2))), size = 5, thickness = 1)
    img.draw_circle(blob.cx(),  (int(blob.cy() - (blob.h()/2))), 5,  thickness = 2)

    # bounding box
    img.draw_rectangle(blob.x(), blob.y(),blob.w(), blob.h())

def getCenterX(blob):
    targetCX = blob.cx()
    return targetCX

def getCenterY(blob):
    targetCY = blob.cy() - (blob.h()/2)
    return targetCY

def getDistanceVFOV(wa, ha, blob):

    d3 = ((ha/2.0)*img.height())
    d4 = 2.0*(blob.h()/2.0)*math.tan(math.radians(VFOV/2.0))
    dv = (d3/d4)
    dv = 1.25*dv # fudge factor calcs
    return dv

def getDistanceHFOV(wa, ha, blob):
    d1 = ((wa/2.0)*img.width())
    d2 = 2.0*(blob.w()/2.0)*math.tan(math.radians(HFOV/2.0))
    dh = (d1/d2)
    dh = 1.25*dh # fudge factor calcs
    return dh

def getAngleX(VFOV, targetCX, dv):
    thetaV = math.radians(VFOV/2.0)
    differenceC1 = SCREEN_CENTERP - targetCX
    a1 = 2*dv*math.tan(thetaV)
    angleDelta1 = (differenceC1*(a1))/(160.0) # angle delta for x
    anglex = math.degrees(math.atan(angleDelta1/dv)) # angle x degrees change needed
    return anglex

def getAngleY(HVOV, targetCY, dh):
    thetaH = math.radians(HFOV/2.0)
    differenceC2 = VERTICAL_CENTERP - targetCY
    a2 = 2*dh*math.tan(thetaH)
    angleDelta2 = (differenceC2*(a2))/(120.0) # angle delta for y
    angley = math.degrees(math.atan(angleDelta2/dh)) # angle y degrees change needed
    return angley

def getOptimizedValues(history):
    finalValues = []
    if (len(history) < HISTORY_LENGTH):
        return [-1.0,-1.0,-1.0,-1.0,-1.0]

    for j in range(len(history[0])):
        medianList = []
        for i in range(len(history)):
            medianList.append(history[i][j])
        medianList.sort()
        finalValues.append(medianList[int(HISTORY_LENGTH/2)])

    return finalValues

def getValues(wa, ha, img):
    blobs = img.find_blobs(thresholds)

    for blob in blobs:
        # filtering based on aspect ratio
        aspectRatio = (blob.w() / blob.h())

        # filters pixels, aspect ratio
        if((blob.pixels() >= 17500) or (blob.density() <.15) or (blob.density() > 0.35) or
            (aspectRatio <= .45*2.84) or (aspectRatio >= 1.3*2.84)):
            continue

        print(blob.density())

        #===Bounding Box===
        drawScope(img, blob)

        #==Centers===
        targetCX = getCenterX(blob)
        targetCY = getCenterY(blob)

        # ===Distance===
        dv = getDistanceVFOV(TARGET_WIDTH, TARGET_HEIGHT, blob)
        dh = getDistanceHFOV(TARGET_WIDTH, TARGET_HEIGHT, blob)

        # ===Angle===
        angleX = getAngleX(VFOV, targetCX, dv)
        angleY = getAngleY(HFOV, targetCY, dh)

        # ===Median Values===
        angleXArr = []
        angleYArr = []
        distanceArr = []
        targetCXArr = []
        targetCYArr = []
        for i in range(15):
            targetCXArr.append(targetCX)
            targetCYArr.append(targetCY)
            distanceArr.append(dh)
            angleXArr.append(angleX)
            angleYArr.append(angleY)

        # returns the final values
        valuesRobotArr = []
        valuesRobotFinal = []
        distance = dv
        while(angleY >= 15):
            distance = dh
            
        valuesRobot = [targetCX, targetCY, distance, angleX, angleY] 

        return valuesRobot

while(True):
    img = sensor.snapshot()

    # params: width actual of target and height actual of target
    # returns: centerX, centerY, distance, angleX, angleY
    unfiltered_values = getValues(TARGET_WIDTH, TARGET_HEIGHT, img)
    if(unfiltered_values == None):
        unfiltered_values  = [-1.0,-1.0,-1.0,-1.0,-1.0]

    values_history.append(unfiltered_values)
    if len(values_history) > HISTORY_LENGTH:
        values_history.pop(0)

    values = getOptimizedValues(values_history)

    if(COMMS_METHOD == "print"):
        print("VALUES", values)
    elif(COMMS_METHOD == "usb"):
        # values = memoryview(values)
        usb.send(ustruct.pack("<d", values[0], values[1], values[2], values[3], values[4] ))
    elif(COMMS_METHOD == "can"):
        pass
