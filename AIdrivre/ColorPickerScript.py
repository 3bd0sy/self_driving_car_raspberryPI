
import cv2
import numpy as np
import time
# frame width and framw height same as in LaneDetectionModule.py
frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture("path.mkv")#"yellow_path.mp4")
cap.set(3, frameWidth)
cap.set(4, frameHeight)
 
#trackbar change will call empty function 
def empty(a):
    pass
 
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 25, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 115, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 100, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 170, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)
        #  self.lowerWhite = np.array([27, 148, 0])
        # self.upperWhite = np.array([148, 255, 255])
# cap = cv2.VideoCapture("vidR.mp4")
frameCounter = 0
 
while True:
 
    frameCounter +=1
    #keep repeating after video is over
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        frameCounter=0
        #cap = cv2.VideoCapture("videos/out.avi")#"yellow_path.mp4")

    _, img = cap.read()
    time.sleep(0.1)
    img=cv2.resize(img,(480,240))
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # adding trackbars for HSV min/max values so that we can change it in real time
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
    #print(h_min)
    
    #get the lower limit
    lower = np.array([h_min, s_min, v_min])
    #get the upper limit
    upper = np.array([h_max, s_max, v_max])
    #passing the upper and lower limit to create the mask
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)
 
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img, mask, result])
    cv2.imshow('Horizontal Stacking', hStack)
    
    
    mask1=cv2.inRange(imgHsv,lower,upper)
    edges1=cv2.Canny(mask,75,150)
    lines1=cv2.HoughLinesP(edges1,1,np.pi/180,50,maxLineGap=50)
    if lines1 is not None:
        for line in lines1:
            x1,y1,x2,y2=line[0]
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),5)
    # cv2.imshow('image',img)
    # cv2.imshow('edges',edges1)
    # cv2.imshow('mask',mask1)
    key=cv2.waitKey(1)
    if key==27:
        break

    
    
cap.release()
cv2.destroyAllWindows()