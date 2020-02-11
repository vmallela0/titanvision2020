import time
from pyb import CAN
from pyb import LED

TRANSMITTER = False

red_led = LED(1)

can = CAN(2, CAN.NORMAL)
can.restart()

if (TRANSMITTER):
    while (True):
        # Send message with id 1
        can.send('Hello', 123)
        red_led.toggle()
        time.sleep(1000)

else:
    while (True):

        can.setfilter(0, CAN.RANGE, 0, (120, 130))  # set a filter to receive messages with id=123, 124, 125 and 126

        message = can.recv(0)                # receive message on FIFO 0

        if message[0] == 123:
            red_led.toggle()
            print(message)
        time.sleep(1000)
