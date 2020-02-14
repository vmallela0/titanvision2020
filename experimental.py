import sensor, image, time, math

# Specify communication method: "print" "usb" "can"
COMMS_METHOD = "print"
TARGET_WIDTH = 39.25
TARGET_HEIGHT = 17.00

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

# LAB color space
thresholds = [(51, 100), (-128, -24), (-48, 51)]

hfov = 70.8 # horizontal field of view
vfov = 55.6 # vertical field of view

def getValues(wa, ha, img):
    blobs = img.find_blobs(thresholds)

    scenterP = 80 # screen center (pixels) horozontal
    vcenterP = 60 # screen center (pixels) vertical

    for blob in blobs:
        # filtering based on aspect ratio
        aspectRatio = (blob.w() / blob.h())

        # filters pixels, aspect ratio
        if((blob.pixels() >= 17500) or (aspectRatio <= .7*2.84) or (aspectRatio >= 1.3*2.84)):
            continue

        # scope view
        img.draw_cross(blob.cx(), (int(blob.cy() - (blob.h()/2))), size = 5, thickness = 1)
        img.draw_circle(blob.cx(),  (int(blob.cy() - (blob.h()/2))), 5,  thickness = 2)

        # bounding box
        
        img.draw_rectangle(blob.x(), blob.y(),blob.w(), blob.h())

        targetCX = blob.cx()
        targetCY = (blob.cy() - (blob.h()/2))

        # ===Distance===
        differenceC1 = scenterP - targetCX
        differenceC2 = vcenterP - targetCY
        d1 = ((wa/2.0)*img.width())
        d3 = ((ha/2.0)*img.height())

        d2 = 2.0*(blob.w()/2.0)*math.tan(math.radians(hfov/2.0))
        d4 = 2.0*(blob.h()/2.0)*math.tan(math.radians(vfov/2.0))

        dv = (d3/d4)
        dh = (d1/d2)
        dv=1.25*dv # fudge factor calcs
        dh=1.25*dh

        # ===Angle===
        thetaV = math.radians(vfov/2.0)
        thetaH = math.radians(hfov/2.0)

        a1 = 2*dv*math.tan(thetaV)
        a2 = 2*dh*math.tan(thetaH)

        angleDelta1 = (differenceC1*(a1))/(160.0) # angle delta for x
        angleDelta2 = (differenceC2*(a2))/(120.0) # angle delta for y

        anglex = math.degrees(math.atan(angleDelta1/dv)) # angle x degrees change needed
        angley = math.degrees(math.atan(angleDelta2/dh)) # angle y degrees change needed

        # returns the final values
        valuesRobot = [blob.cx(), (blob.cy() - (blob.h()/2)), dh, anglex, angley]
        return valuesRobot


while(True):
    img = sensor.snapshot()
    
    # params: width actual of target and height actual of target 
    # returns: centerX, centerY, distance, angleX, angleY
    values = getValues(TARGET_WIDTH, TARGET_HEIGHT, img)

    if(values == None):
        values = [-1.0,-1.0,-1.0,-1.0,-1.0]
    
    if(COMMS_METHOD == "print"):
        print(values)
    elif(COMMS_METHOD == "usb"):
        pass
    elif(COMMS_METHOD == "can"):
        pass
