#!/usr/bin/env python3
import time
import datetime
import RPi.GPIO as GPIO



class Car():

    def __init__(self, pwm_frequency=5000, state={}):
        
        self.__testName = str(datetime.datetime.now()).replace(' ','_')
        self.__FW_MOVE_PIN = 40
        self.__BW_MOVE_PIN = 38
        self.__LR_MOVE_PIN = 36
        self.__CAM_MOVE_PIN = 32
        
        # Prevent setting distructive frequency
        if pwm_frequency >= 100 and pwm_frequency <= 5000:
            self.pwm_frequency = pwm_frequency
        else:
            self.pwm_frequency = 5000
        
        # Set gpio pin mode
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        GPIO.setup(self.__FW_MOVE_PIN, GPIO.OUT)
        GPIO.output(self.__FW_MOVE_PIN, GPIO.LOW)
        GPIO.setup(self.__BW_MOVE_PIN, GPIO.OUT)
        GPIO.output(self.__BW_MOVE_PIN, GPIO.LOW)
        GPIO.setup(self.__LR_MOVE_PIN, GPIO.OUT)
        GPIO.output(self.__LR_MOVE_PIN, GPIO.LOW)
        GPIO.setup(self.__CAM_MOVE_PIN, GPIO.OUT)
        GPIO.output(self.__CAM_MOVE_PIN, GPIO.LOW)
        
        
        self.__FR = GPIO.PWM(self.__FW_MOVE_PIN, self.pwm_frequency)
        self.__BK = GPIO.PWM(self.__BW_MOVE_PIN, self.pwm_frequency)
        
        # Setup servos
        self.__LR = GPIO.PWM(self.__LR_MOVE_PIN, 50)
        self.__CAM = GPIO.PWM(self.__CAM_MOVE_PIN, 50)
        
        self.__LR.start(0)
        self.__CAM.start(0)
        #CAM.ChangedutyCycle(0)
        #LR.ChangedutyCycle(0)
        
        
        self.__FR.start(0)
        self.__BK.start(0)
        #CAM.ChangedutyCycle(0)
        #LR.ChangedutyCycle(0)
        self.state = state
        
    def forward(self, duration, speed):
        '''
        duration <float> in seconds
        speed <int> in % 
        '''
        # switch off BW
        self.__FR.ChangeDutyCycle(speed)
        # switch on FW
        time.sleep(duration)
        self.__FR.ChangeDutyCycle(0)
        return self.state
        
    def backward(self, duration, speed):
        '''
        duration <float> in seconds
        speed <int> in % 
        '''
        # switch off BW
        #pass
        # switch on FW
        self.__BK.ChangeDutyCycle(speed)
        time.sleep(duration)
        # stop motorb
        self.__BK.ChangeDutyCycle(0)
        return self.state
    
    def turn_lr(self, degree):
        '''
        degree <int> between 5 and 10
        Returns degree if ok.
        Returns -1, if error
        '''
        if degree >= 5 and degree <=9:
            self.__LR.ChangeDutyCycle(degree)
            time.sleep(0.5)
            self.__LR.ChangeDutyCycle(0)
            self.state['turn_degree'] = degree
            return degree
        else:
            return -1
        
        
    #def turn_l(self, degree):
    #    LR.ChangedutyCycle(degree)

    def camera_position(self, position):
        if  position >= 7 and position <=12:
            self.__CAM.ChangeDutyCycle(position)
            time.sleep(0.5)
            self.__CAM.ChangeDutyCycle(0)
            self.state['camera_position'] = position
            return self.state
        else:
            return -1
        
        
    def __del__(self):
        GPIO.cleanup()

    







