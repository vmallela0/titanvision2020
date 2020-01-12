# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time
from time import sleep
from machine import Pin
import pyb
import framebuf

pin_num = 'P0'
pin = Pin(pin_num, Pin.OUT)
pin.off()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
clock = time.clock()

directory = ""
img_pixels = []
img2_pixels = []
subtracted_img_pixels = []

#sensor.snapshot().save('test.jpg')

"""img = sensor.snapshot()
image.ImageWriter('test.jpg').add_frame(img).close()"""

#sensor.snapshot().save('test.bmp')

#img = image.ImageReader("/test.bmp")
print('getting "img"')
img = image.Image("first_image.bmp", copy_to_fb=True)



"""print('saving first image')
img = sensor.snapshot()
img.save(directory + "first_image.jpg")
print('first image saved')
print()

#print(f"turning pin \"{pin_num}\" high"
print('turning pin ' + str(pin_num) + ' high')
pin.on()

print('setting delay')
sleep(5000)

print('saving second image')
img2 = sensor.snapshot()
img2.save(directory + "second_image.jpg")
print('second image saved')
print()



print('saving subtracted image')
img2.sub(img).save(directory + 'subtracted_img.jpg')
print('subtracted image saved')
print()

print('program complete')"""

"""print('img - Taking snapshot')
img = sensor.snapshot()
print('snapshot taken')
print('iterating')
for i in range(img.width() * img.height()):
    img_pixels.append(img.get_pixel(i))
print('len(img_pixels)')
print(len(img_pixels))
print()

print('img2 - Taking snapshot')
img2 = sensor.snapshot()
print('snapshot taken')
print('iterating')
for i in range(img.width() * img.height()):
    img_pixels.append(img.get_pixel(i))
print('len(img_pixels)')
print(len(img_pixels))
print()"""
