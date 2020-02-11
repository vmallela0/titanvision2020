import sensor, image, time, math

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.RGB565
sensor.set_framesize(sensor.QQVGA) # or sensor.QVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
clock = time.clock()

thresholds = [(51, 100), (-128, -24), (-48, 51)]
thresholdsHM = [(0, 16), (-80, 92), (-60, 127)] #hail mary vision

hfov = 70.8
vfov = 55.6

def distance(wa, ha, img):
    areaTemp = 50
    lod = img.find_blobs(thresholdsHM)

    scenterP = 80

    for i in lod:
        #print(i) #dictionary of values in lod
        aspectRatio = (i.w() / i.h())
        if((i.pixels() >= 17500) or (aspectRatio <= 1.5) or (aspectRatio >= 3.0)):
            continue
        img.draw_cross(i.cx(), (int(i.cy() - (i.h()/2))), size = 5, thickness = 1)
        img.draw_circle(i.cx(),  (int(i.cy() - (i.h()/2))), 5,  thickness = 2)
        img.draw_rectangle(i.x(), i.y(),i.w(), i.h())

        targetCP = i.cx()
        differenceCP = scenterP - targetCP
        d1 = ((wa/2.0)*img.width())
        d3 = ((ha/2.0)*img.height())

        d2 = 2.0*(i.w()/2.0)*math.tan(math.radians(hfov/2.0))
        d4 = 2.0*(i.h()/2.0)*math.tan(math.radians(vfov/2.0))

        dv = (d3/d4)
        dh = (d1/d2)
        dv=1.25*dv
        dh=1.25*dh
        thetaV = math.radians(vfov/2.0)
        #thetaH = math.radians(hfov/2.0)

        a1 = 2*dv*math.tan(thetaV)
        #a2 = 2*dh*math.tan(thetaH)
        angleDelta1 = (differenceCP*(a1))/(160.0)
        #angleDelta2 = (differenceCP*(a2))/(120.0)

        #print("Vertical ", dv," || horzontal ", dh)
        distance = (dv + dh)/2.0

        #print("Angle is :  ", math.degrees(math.atan(angleDelta/distance)))
        angle = math.degrees(math.atan(angleDelta1/distance))
        #angley = math.degrees(math.atan(angleDelta2/distance))

        #returns the final values
        valuesRobot = [i.cx(), (i.cy() - (i.h()/2)), dh, angle]
        return valuesRobot

        while(3.0 >= angle >= -3.0):
            img.draw_rectangle(i.x(), i.y(),i.w(), i.h(), color = (39, 156, 33))


sensor.set_auto_exposure(False, 400)
while(True):
    #clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot()
    print(distance(39.25, 17.00, img))
    #print(clock.fps())




