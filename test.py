import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

def buttonEventHandler_rising(callback):
    print("Button was pressed!")

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(18, GPIO.RISING, callback=buttonEventHandler_rising)
input_state=GPIO.input(18)
i=0
while True:
    #input_state=GPIO.input(18)
    print("This is a test! ",i)
    time.sleep(2)
    print("Hallaleuah", i)
    i=i+1
#     if input_state == False:
#         print("Button Pressed")
#         time.sleep(0.2)
#     while True:
#         print("Hello Test")