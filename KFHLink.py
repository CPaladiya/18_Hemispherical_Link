from picamera import PiCamera
from picamera.array import PiRGBArray
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
from time import sleep
import numpy as np
import cv2
import LiveCenter as LC

########### ---------------------- attaching the servos---------------------------
#before running the program do 'sudo pigpiod' in terminal
factory = PiGPIOFactory() #since the pulses are software generated we want to mimic hardware generated to remove jitter from servop

#top camera servo configuration, here we have set pulse width to reach full capabilities of servo
servoT= Servo(17, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory = factory)
#bottom camera servo configuration
servoB = Servo(18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory = factory)

servoT.value = -1 #maximum allowed -1 to -0.4, limited to save hardware and wires
servoB.value = 0 #range allowed -0.6 to 0.6. limited to save hardware and wires

#########-------------------------------Camera config-----------------------------
#lets start all thing related camera
camera = PiCamera()
#setting resoltion of image we need (width,height)
img_h ,img_w = 608, 608
camera.resolution = (img_w,img_h) #setting the feed resolution
camera.framerate = 30 #setting the frame rate of the camera
rawCapture = PiRGBArray(camera, size=(img_w,img_h))
centerOfImage_x = img_w/2 #if height and width is different thenw we will need two values
centerOfImage_y= img_h/2

small_ball = 500 #the minimum area of ball we want to identify

#allow the camera to warmup
sleep(0.1)

#defining color boud for the ball as we required
lower_green = np.array([55,60,60])
upper_green = np.array([86,255,255])

#capturing the image frame by frame
for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port = True):
    #grabbing the numpy array from the frame to do further processing
    image = frame.array

    ####### ----------------- creating a mask------------------
    #converting BGR image into hsv image space
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    #creating mask using inRange function
    #then we perfrom series of dialation and erosion to remove any small blobs left in the mask
    mask = cv2.inRange(hsv_frame, lower_green, upper_green)
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
    
    #now we will use this mask to filter the object based on color as we like
    masked = cv2.bitwise_and(image,image, mask = mask)
    
    #######--------------creating binary image to find centroid & project live location of the object
    #creating binary image helps in increasing the accuracy
    ret,binaryImage = cv2.threshold(mask,250,255,cv2.THRESH_BINARY)
    #finding contours within that binary image
    
    #getting the live center of the ball 
    Ball_X, Ball_Y = LC.GetLiveCenter(binaryImage,masked)
    
    #Drawing axis and center of the image
    LC.DrawAxis(masked)
    #Drawing offset with respect to center of image and drawing live center of the ball
    LC.PrintCentersOnImage(masked, Ball_X,Ball_Y)
    
    cv2.imshow("Frame", image) #showing the frame we just captured
    cv2.imshow("Masked Frame", masked) #showing the live masked feed
    key = cv2.waitKey(1) #& 0xFF #showing the frame
    
    rawCapture.truncate(0) #clear the stream in preparation of the next frame
    
    if key == ord("q"): #making sure if we press q, we stop the stream
        break
