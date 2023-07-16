# Import the modules for computer vision, numpy, picamera and time
import cv2
import numpy as np
import picamera
from time import sleep

# Import the custom modules for camera, motor, edge detection, object detection and drive
from .cameraModule import PIcamera
from .motorModule import motor
from .edgeDetectionModule import edgeDetection
from .tfliteDetection import objectDetection
from .driveModule import driveOBJ

# Define the main function

def run():
    # Create an instance of the PIcamera class with no display
    cam=PIcamera(display= not True)
    # Create an instance of the edgeDetection class with display
    detect = edgeDetection(display=not True)
    # Create an instance of the motor class
    car=motor()
    # Create an instance of the driveOBJ class with the car object
    drv=driveOBJ(car)
    # Create an instance of the objectDetection class
    objectDetect = objectDetection()
    # Initialize a variable for the frame rate calculation
    frame_rate_calc = 1
    # Get the frequency of the clock ticks
    freq = cv2.getTickFrequency()
    # Start a loop
    while True:
        # Get the current tick count
        t1 = cv2.getTickCount()
        # Capture a frame from the PIcamera object
        frame=cam.capture()
        # If the frame is not None, process it with edge detection and object detection
        if frame is not None:
            # Get the degree of deviation from the edge detection module
            deg, lines = detect.process(frame)
            # Get the annotated frame from the object detection module
            frm, speeds, colors, cars = objectDetect.detect(frame)
            # Move the car according to the degree of deviation from the drive module
            drv.move(deg,speeds,colors)
            # Write the annotated frame to the video writer object
            # Put a text on the frame showing the current frame rate
            cv2.line(frm, lines[0][0],lines[0][1], (0, 255, 0), 3)
            cv2.line(frm, lines[1][0],lines[1][1], (0, 255, 0), 3)
            cv2.line(frm, lines[2][0],lines[2][1], (0, 255, 255), 3)
            cv2.line(frm, lines[3][0],lines[3][1], (255, 0, 0), 3)
            cv2.putText(frm, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("frame",frm)
#             ret, buffer = cv2.imencode('.jpeg', frm)
#             frm = buffer.tobytes()
#             yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frm + b'\r\n')

        # Get the current tick count again
        t2 = cv2.getTickCount()
        # Calculate the time elapsed between t1 and t2 in seconds
        time1 = (t2-t1)/freq
        # Calculate the frame rate as the inverse of time elapsed
        frame_rate_calc = 1/time1
        # Check if the user presses 'q' key on the keyboard
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Stop and exit the car object
            # out.release()
            car.stop()
            car.exit()
            # Release the video writer object and break out of the loop
            break

    # Destroy all windows created by cv2.imshow()
    # out.release()
    cv2.destroyAllWindows()
    # Release the video writer object again for safety
    # Stop and exit the car object again for safety

def stream(cam,detect,car,drv,objectDetect):
    frame=cam.capture()
    if frame is not None:
        deg, lines = detect.process(frame)
        frm, speeds, colors, cars = objectDetect.detect(frame)
        drv.move(deg,speeds,colors)
        cv2.line(frm, lines[0][0],lines[0][1], (0, 255, 0), 3)
        cv2.line(frm, lines[1][0],lines[1][1], (0, 255, 0), 3)
        cv2.line(frm, lines[2][0],lines[2][1], (0,255,255), 3)
        cv2.line(frm, lines[3][0],lines[3][1], (255, 0, 0), 3)
        return frm
    
if __name__ == '__main__':
    pass
#    run()