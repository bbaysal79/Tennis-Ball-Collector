import numpy as np
import cv2 as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils
import time
import RPi.GPIO as GPIO
from threading import Thread

# Global variables
ball_color = 0
rw_speed = 70
lw_speed = 70 # int(rw_speed*1.14 if rw_speed*1.14 < 100 else 100)
center = None
msg = 1
x, y, radius = None, None, None
v_height = 272
v_width = 480

wrf_pinout = 29
wrr_pinout = 31
wlf_pinout = 11
wlr_pinout = 7
thrower_r_pinout = 16
thrower_l_pinout = 18

greenLower = (30, 80, 80)
greenUpper = (45, 255, 255)
#blueLower = (95, 50, 40)
#blueUpper = (120, 255, 255)
#redLower = (0, 100, 20)
#redUpper = (10, 255, 255)


def start_throwers(trp, tlp):
    GPIO.setup(trp, GPIO.OUT)
    GPIO.setup(tlp, GPIO.OUT)
    tr = GPIO.PWM(trp, 100)
    tl = GPIO.PWM(tlp, 100)
    tr.start(11.2)
    tl.start(11.2)
    return tr, tl


def start_wheels(wrfp, wrrp, wlfp, wlrp):
    GPIO.setup(wrfp, GPIO.OUT)
    GPIO.setup(wrrp, GPIO.OUT)
    GPIO.setup(wlfp, GPIO.OUT)
    GPIO.setup(wlrp, GPIO.OUT)
    wrf = GPIO.PWM(wrfp, 100)
    wrr = GPIO.PWM(wrrp, 100)
    wlf = GPIO.PWM(wlfp, 100)
    wlr = GPIO.PWM(wlrp, 100)
    wrf.start(0)
    wrr.start(0)
    wlf.start(0)
    wlr.start(0)
    return wrf, wrr, wlf, wlr


def drive_forward(wrf, wrr, wlf, wlr):
    wrf.ChangeDutyCycle(rw_speed)
    wlf.ChangeDutyCycle(lw_speed)
    wrr.ChangeDutyCycle(0)
    wlr.ChangeDutyCycle(0)


def turn_right(wrf, wrr, wlf, wlr):
    wrf.ChangeDutyCycle(0)
    wlf.ChangeDutyCycle(lw_speed)
    wrr.ChangeDutyCycle(0)
    wlr.ChangeDutyCycle(0)


def turn_left(wrf, wrr, wlf, wlr):
    wrf.ChangeDutyCycle(rw_speed)
    wlf.ChangeDutyCycle(0)
    wrr.ChangeDutyCycle(0)
    wlr.ChangeDutyCycle(0)


def turn_around(wrf, wrr, wlf, wlr):
    wrf.ChangeDutyCycle(rw_speed*0.75)
    wlf.ChangeDutyCycle(0)
    wrr.ChangeDutyCycle(0)
    wlr.ChangeDutyCycle(lw_speed*0.75)


def stop_t(wrf, wrr, wlf, wlr):
    wrf.ChangeDutyCycle(0)
    wrr.ChangeDutyCycle(0)
    wlf.ChangeDutyCycle(0)
    wlr.ChangeDutyCycle(0)
    
    
def stop(wrf, wrr, wlf, wlr):
    wrf.stop(0)
    wrr.stop(0)
    wlf.stop(0)
    wlr.stop(0)


def throw_left(tr, tl):
    tr.ChangeDutyCycle(12)
    tl.ChangeDutyCycle(10)


def throw_right(tr, tl):
    tr.ChangeDutyCycle(10)
    tl.ChangeDutyCycle(12)


def throw_forward(tr, tl):
    tr.ChangeDutyCycle(12)
    tl.ChangeDutyCycle(12)


def throw_idle(tr, tl):
    tr.ChangeDutyCycle(11)
    tl.ChangeDutyCycle(11)
    
    
def stop_thrower(tr, tl):
    tr.stop(0)
    tl.stop(0)


def detect_ball(gL, gU):
    global x, y, radius, center, v_height, v_width, msg
    camera = PiCamera()
    camera.resolution = (v_width, v_height)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(v_width, v_height))
    print("camera starting...")
    time.sleep(1.0)
    
    for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # time.sleep(.05)
        frame = image.array
        # frame = imutils.resize(frame, height=v_height)
        frame = cv.rotate(frame, cv.ROTATE_180)
        blurred = cv.GaussianBlur(frame, (5, 5), 0)
        hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

        #mask_r = cv.inRange(hsv, rL, rU)
        mask = cv.inRange(hsv, gL, gU)
        #mask_b = cv.inRange(hsv, bL, bU)
        #mask = cv.bitwise_or(mask_r, mask_g)
        #mask = cv.bitwise_or(mask, mask_b)
        mask = cv.erode(mask, None, iterations=2)
        mask = cv.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        if len(cnts) > 0:
            c = max(cnts, key=cv.contourArea)
            ((x, y), radius) = cv.minEnclosingCircle(c)
            M = cv.moments(c)
            center = 1
            if radius > 6:
                #cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                #cv.circle(frame, center, 2, (0, 0, 255), -1)
                print("x=", int(x), "y=", int(y), "r=", int(radius))
                
                    #elif bL[0] < hsv[int(y)][int(x)][0] < bU[0]:
                     #   ball_color = 2
                     #   print("c blue")
                    #elif rL[0] < hsv[int(y)][int(x)][0] < rU[0]:
                     #   ball_color = 3
                     #   print("c red")
        cv.imshow("frame", 0)
        rawCapture.truncate(0)
        key = cv.waitKey(1) & 0xFF
        if key == ord("q") or msg == 0:
            break
    msg = 0
    camera.close()
    cv.destroyAllWindows()

def main():
    global msg
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    wrf, wrr, wlf, wlr = start_wheels(wrf_pinout, wrr_pinout, wlf_pinout, wlr_pinout)
    tr, tl = start_throwers(thrower_r_pinout, thrower_l_pinout)
    print("robot starting...")
    time.sleep(4.0)
    

    camera_thread = Thread(target=detect_ball, args=(greenLower, greenUpper,))
    # thrower_thread = Thread(target=run_throwers, args=(tr, tl,))
    camera_thread.start()
    time.sleep(4.0)
    throw_forward(tr, tl)
    time.sleep(4.0)
    #thrower_thread.start()
    #time.sleep(2.0)
    counter = 0
    while msg != 0:
        if center is not None:
            counter = 0
            if radius > 48:
                print("collect")
                drive_forward(wrf, wrr, wlf, wlr)
                time.sleep(1.5)
                stop_t(wrf, wrr, wlf, wlr)
            if x < -(y/v_height)*v_width/3 + v_width/3:
                print("turn left")
                turn_left(wrf, wrr, wlf, wlr)
                time.sleep(.07)
                stop_t(wrf, wrr, wlf, wlr)
                time.sleep(.04)
            elif x > (y/v_height)*v_width/3 + 2*v_width/3:
                print("turn right")
                turn_right(wrf, wrr, wlf, wlr)
                time.sleep(.07)
                stop_t(wrf, wrr, wlf, wlr)
                time.sleep(.04)
            else:
                print("forward")
                drive_forward(wrf, wrr, wlf, wlr)
                time.sleep(.15)
                stop_t(wrf, wrr, wlf, wlr)
                time.sleep(.04)
        else:
            if counter < 70:
                print("searching")
                turn_around(wrf, wrr, wlf, wlr)
                time.sleep(.1)
                stop_t(wrf, wrr, wlf, wlr)
                time.sleep(.04)
                counter += 1
            else:
                break
    # When everything done, release the video capture object
    msg = 0
    stop(wrf, wrr, wlf, wlr)
    stop_thrower(tr, tl)
    # Closes all the frames

main()
