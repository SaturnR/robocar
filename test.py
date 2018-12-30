import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

#GPIO.setwarnings(False)

GPIO.setwarnings(False)

Front = 40
Back = 38

GPIO.setup(Front, GPIO.OUT)
GPIO.output(Front, GPIO.LOW)
GPIO.setup(Back, GPIO.OUT)
GPIO.output(Back, GPIO.LOW)

GPIO.setup(36, GPIO.OUT)
GPIO.output(36, GPIO.LOW)
GPIO.setup(32, GPIO.OUT)
GPIO.output(32, GPIO.LOW)


FR = GPIO.PWM(40, 5000)
BK = GPIO.PWM(38, 5000)

LR = GPIO.PWM(36, 50)
CAM = GPIO.PWM(32, 50)

LR.start(0)
CAM.start(0)
#CAM.ChangedutyCycle(0)
#LR.ChangedutyCycle(0)


FR.start(0)
BK.start(0)
#CAM.ChangedutyCycle(0)
#LR.ChangedutyCycle(0)

#GPIO.cleanup()


