import sensor, image, time, math

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.RGB565
sensor.set_framesize(sensor.QQVGA) # or sensor.QVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
clock = time.clock()

KMAN = 0.065
autoExposureSum = 0
readExposureNum = 10
for i in range(readExposureNum):
   autoExposureSum += sensor.get_exposure_us()
autoExposure = autoExposureSum/readExposureNum
manualExposure = int(autoExposure * KMAN) #scalefactor for decreasing autoExposure

thresholds = [(51, 100), (-128, -24), (-48, 51)]
thresholdsHM = [(0, 16), (-80, 92), (-60, 127)] #hail mary vision
thresholdsMC = [(28, 65), (-66, 19), (-74, 27)] #media center vision

hfov = 70.8
vfov = 55.6

def distance(wa, ha, img):
    areaTemp = 50
    lod = img.find_blobs(thresholds)

    scenterP = 80
    vcenterP = 60
    #if(len(lod) == 0):
        #return [-1,-1,-1,-1,-1]

    for i in lod:
        #print(i) #dictionary of values in lod
        aspectRatio = (i.w() / i.h())
        if((i.pixels() >= 17500) or (aspectRatio <= .7*2.84) or (aspectRatio >= 1.3*2.84)):
            continue
        img.draw_cross(i.cx(), (int(i.cy() - (i.h()/2))), size = 5, thickness = 1)
        img.draw_circle(i.cx(),  (int(i.cy() - (i.h()/2))), 5,  thickness = 2)
        img.draw_rectangle(i.x(), i.y(),i.w(), i.h())

        targetCX = i.cx()
        targetCY = (i.cy() - (i.h()/2))
        differenceC1 = scenterP - targetCX
        differenceC2 = vcenterP - targetCY
        d1 = ((wa/2.0)*img.width())
        d3 = ((ha/2.0)*img.height())

        d2 = 2.0*(i.w()/2.0)*math.tan(math.radians(hfov/2.0))
        d4 = 2.0*(i.h()/2.0)*math.tan(math.radians(vfov/2.0))

        dv = (d3/d4)
        dh = (d1/d2)
        dv=1.25*dv
        dh=1.25*dh

        thetaV = math.radians(vfov/2.0)
        thetaH = math.radians(hfov/2.0)

        a1 = 2*dv*math.tan(thetaV)
        a2 = 2*dh*math.tan(thetaH)

        angleDelta1 = (differenceC1*(a1))/(160.0)
        angleDelta2 = (differenceC2*(a2))/(120.0)

        #print("Vertical ", dv," || horzontal ", dh)
        distance = (dv + dh)/2.0

        #print("Angle is :  ", math.degrees(math.atan(angleDelta/distance)))
        anglex = math.degrees(math.atan(angleDelta1/dv))
        angley = math.degrees(math.atan(angleDelta2/dh))

        #returns the final values
        valuesRobot = [i.cx(), (i.cy() - (i.h()/2)), dh, anglex, angley]
        return valuesRobot
        while(3.0 >= angle >= -3.0):
            img.draw_rectangle(i.x(), i.y(),i.w(), i.h(), color = (39, 156, 33))


sensor.set_auto_exposure(False,  manualExposure)
while(True):
    #clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot()
    print(distance(39.25, 17.00, img))
    #print(clock.fps())




