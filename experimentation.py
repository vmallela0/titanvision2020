import sensor, image, time, math

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.RGB565
sensor.set_framesize(sensor.QQVGA) # or sensor.QVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
clock = time.clock()

#setting autoexposure automatically
KMAN = 0.065 #constant for exposure setting
autoExposureSum = 0
readExposureNum = 10
for i in range(readExposureNum):
   autoExposureSum += sensor.get_exposure_us()
autoExposure = autoExposureSum/readExposureNum
manualExposure = int(autoExposure * KMAN) #scalefactor for decreasing autoExposure

thresholds = [(51, 100), (-128, -24), (-48, 51)]
thresholdsHM = [(0, 16), (-80, 92), (-60, 127)] #hail mary vision

hfov = 70.8 #horozontal field of view
vfov = 55.6 #vertical field of view

def distance(wa, ha, img):
    areaTemp = 50
    lod = img.find_blobs(thresholds) #finding blobs

    scenterP = 80 #screen center (pixels) horozontal
    vcenterP = 60 #screen center (pixels) vertical


    if(len(lod) == 0):
        return [-1,-1,-1,-1,-1]
    else:
        for i in lod:

            #filtering based on aspect ratio
            aspectRatio = (i.w() / i.h())

            #filters pixels, aspect ratio
            if((i.pixels() >= 17500) or (aspectRatio <= .7*2.84) or (aspectRatio >= 1.3*2.84)):
                continue

            #scope view
            img.draw_cross(i.cx(), (int(i.cy() - (i.h()/2))), size = 5, thickness = 1)
            img.draw_circle(i.cx(),  (int(i.cy() - (i.h()/2))), 5,  thickness = 2)

            #bounding box
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
            dv=1.25*dv #fudge factor calcs
            dh=1.25*dh

            thetaV = math.radians(vfov/2.0)
            thetaH = math.radians(hfov/2.0)

            a1 = 2*dv*math.tan(thetaV)
            a2 = 2*dh*math.tan(thetaH)

            angleDelta1 = (differenceC1*(a1))/(160.0) #angle delta for x
            angleDelta2 = (differenceC2*(a2))/(120.0) #angle delta for y

            anglex = math.degrees(math.atan(angleDelta1/dv)) #angle x degrees change needed
            angley = math.degrees(math.atan(angleDelta2/dh)) #angle y degrees change needed

            #returns the final values
            valuesRobot = [i.cx(), (i.cy() - (i.h()/2)), dh, anglex, angley]
            return valuesRobot

            while((5.0 >= anglex >= -5.0) and (5.0 >= angley >= -5.0)):
                img.draw_rectangle(i.x(), i.y(), i.w(), i.h(), color = (0, 10, 0))


sensor.set_auto_exposure(False,  manualExposure) #autoset exposures

while(True):
    img = sensor.snapshot()
    print(distance(39.25, 17.00, img)) #parameters take in width actual of target and height actual of target
