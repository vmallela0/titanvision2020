from pyb import CAN
from pyb import LED
red_led = LED(1)
can = CAN(2, CAN.LOOPBACK)
#can.setfilter(0, CAN.LIST16, 0, (123, 124, 125, 126))  # set a filter to receive messages with id=123, 124, 125 and 126
can.send('message!', 123)   # send a message with id 123
value = can.recv(0)                # receive message on FIFO 0
if value[0] == 123:
    red_led.LED.on()
    print(value[3])
