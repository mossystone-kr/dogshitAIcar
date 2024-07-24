import cv2 
import numpy as np 
import RPi.GPIO as GPIO
from time import sleep

STOP = 0
FORWARD = 1
BACKWORD = 2

CH1 = 0
CH2 = 1

OUTPUT = 1
INPUT = 0

HIGH = 1
LOW = 0

ENA = 26
ENB = 0
IN1 = 19
IN2 = 13
IN3 = 6
IN4 = 5

def setPinConfig(EN, INA, INB):        
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    pwm = GPIO.PWM(EN, 100)  
    pwm.start(0) 
    return pwm

def setMotorContorl(pwm, INA, INB, speed, stat):

    pwm.ChangeDutyCycle(speed)  
    
    if stat == FORWARD:
        GPIO.output(INA, HIGH)
        GPIO.output(INB, LOW)
        
    elif stat == BACKWORD:
        GPIO.output(INA, LOW)
        GPIO.output(INB, HIGH)
    
    elif stat == STOP:
        GPIO.output(INA, LOW)
        GPIO.output(INB, LOW)

GPIO.setmode(GPIO.BCM)
pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)
 
def setMotor(ch, speed, stat):
    if ch == CH1:
        setMotorContorl(pwmA, IN1, IN2, speed, stat)
    else:
        setMotorContorl(pwmB, IN3, IN4, speed, stat)


def main():
    camera1 = cv2.VideoCapture(0)
    camera2 = cv2.VideoCapture(2)
    camera1.set(3,320) 
    camera1.set(4,240)
    camera2.set(3,320) 
    camera2.set(4,240)
   
    while( camera1.isOpened() and camera2.isOpened() ): 
        ret1, frame1 = camera1.read() 
        ret2, frame2 = camera2.read()
        #cv2.imshow( 'normal' , frame1) 
        #cv2.imshow( 'normal2' , frame2)

        gray1_1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY) 
        gray2_1 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY) 
        
        blur1_1 = cv2.GaussianBlur(gray1_1, (5,5) , 0) 
        blur2_1 = cv2.GaussianBlur(gray2_1, (5,5) , 0) 
       
        ret1,thresh1 = cv2.threshold(blur1_1, 123, 255, cv2.THRESH_BINARY_INV)
        ret2,thresh2 = cv2.threshold(blur2_1, 123, 255, cv2.THRESH_BINARY_INV) 
        
        mask1 = cv2.erode(thresh1, None, iterations=2)  
        mask1 = cv2.dilate(mask1, None, iterations=2)
        cv2.imshow('mask1',mask1)

        mask2 = cv2.erode(thresh2, None, iterations=2)  
        mask2 = cv2.dilate(mask2, None, iterations=2)
        cv2.imshow('mask2',mask2)
    
        contours1,hierarchy1 = cv2.findContours(mask1.copy(), 1, cv2.CHAIN_APPROX_NONE)
        contours2,hierarchy2 = cv2.findContours(mask2.copy(), 1, cv2.CHAIN_APPROX_NONE)
        
        if len(contours1) > 0:
            c = max(contours1, key=cv2.contourArea)
            M = cv2.moments(c)
             
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            
            cv2.line(frame1,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(frame1,(0,cy),(1280,cy),(255,0,0),1)
        
            cv2.drawContours(frame1, contours1, -1, (0,255,0), 1)
            
            #print(cx,end=" ") 
            
        if len(contours2) > 0:
            c2 = max(contours2, key=cv2.contourArea)
            M2 = cv2.moments(c2)
             
           
            cx2 = int(M2['m10']/M2['m00'])
            cy2 = int(M2['m01']/M2['m00'])
            
           
            cv2.line(frame2,(cx2,0),(cx2,720),(255,0,0),1)
            cv2.line(frame2,(0,cy2),(1280,cy2),(255,0,0),1)
        
            cv2.drawContours(frame2, contours2, -1, (0,255,0), 1)
            
            #print(cx2)
            
        
        if cx>=180 and cx<=220:
            if cx2<=180:
                #setMotor(CH1, 90, FORWARD)
                #setMotor(CH2, 40, FORWARD)
                print("Left")
                
            else:
                #setMotor(CH1, 90, FORWARD)
                #setMotor(CH2, 90, FORWARD)
                print("Forward")

        else:
            #setMotor(CH1, 90, FORWARD)
            #setMotor(CH2, 90, FORWARD)
            print("Forward")
        
        
        if cv2.waitKey(1) == ord('q'): 
            break
        
    cv2.destroyAllWindows() 
     
if __name__ == '__main__':
    main()
