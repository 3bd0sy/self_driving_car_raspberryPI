import cv2
import numpy as np
#from cameraModule import PIcamera

# Define a class for lane detection
class edgeDetection():
    # Initialize the class with some parameters
    def __init__(self, display=False) -> None:
        # Whether to display the intermediate steps
        self.display = display
        # The height of the region of interest for lane detection
        self.h = 50
        # The histograms for lane and lane end positions
        self.histogramLane = []
        self.histogramLaneEnd = []
        # The positions of the left and right lanes
        self.leftLanePos = 0
        self.rightLanePos = 0
        # The center of the frame and the lane
        self.frameCenter = 0
        self.laneCenter = 0
        # The result of the lane detection
        self.result = 0
        # The position of the lane end
        self.laneEnd = 0
        # The source and destination points for perspective transformation
        self.Source = [(0, 160-self.h), (400, 160-self.h), (0, 200), (400, 200)]
        self.Destination = [(80, 0), (320, 0), (80, 240), (320, 240)]
        # The lower and upper bounds for color thresholding in HSV space
        # self.lower = np.array([15, 10, 70])
        # self.upper = np.array([73, 255, 255])
        self.lower = np.array([20, 155, 50])
        self.upper = np.array([40, 255, 255])
        # Convert the source and destination points to numpy arrays
        self.Source_ = np.array(self.Source, np.float32)
        self.Destination_ = np.array(self.Destination, np.float32)

    # Define a method to process a frame and detect lanes
    def process(self, frame):
        lines=[]
        # Make a copy of the original frame
        frame_Stop = frame.copy()
        # Draw the source points on the frame
#         cv2.line(frame, self.Source[0], self.Source[1], (0, 0, 255), 2)
#         cv2.line(frame, self.Source[1], self.Source[3], (0, 0, 255), 2)
#         cv2.line(frame, self.Source[3], self.Source[2], (0, 0, 255), 2)
#         cv2.line(frame, self.Source[2], self.Source[0], (0, 0, 255), 2)
        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Apply color thresholding to isolate the lane pixels
        frameThresh = cv2.inRange(hsv, self.lower, self.upper)
        # Apply edge detection to enhance the lane boundaries
        frameEdge = cv2.Canny(frameThresh, 200, 400)
        # Combine the thresholded and edge frames
        frameFinal = cv2.add(frameThresh, frameEdge)
        # Convert the final frame to RGB color space for display purposes
        frameFinal = cv2.cvtColor(frameFinal, cv2.COLOR_GRAY2RGB)
        
		# Initialize the histograms for lane and lane end positions with zeros
        self.histogramLane = [0] * 400 
        self.histogramLaneEnd = [0] * 400
		
		# Loop over each column of pixels in the final frame 
        for i in range(400):
		    # Extract a region of interest for lane detection from the bottom half of the frame 
            roiLane = frameFinal[140:240,i:i+1]
		    # Sum up the pixel values in the region of interest and store it in the histogram 
            self.histogramLane[i] = np.int64(np.sum(roiLane[0]))
		    # Extract a region of interest for lane end detection from the whole frame 
            roiLaneEnd = frameFinal[0:240,i:i+1]
		    # Sum up the pixel values in the region of interest and store it in the histogram 
            self.histogramLaneEnd[i] = np.int64(np.sum(roiLaneEnd[0]))
		
		# Sum up all the values in the histogram for lane end detection 
        self.laneEnd = sum(self.histogramLaneEnd)

        # Find the position of the left and right lane edges by finding the maximum value in the histogram
        self.leftLanePos = np.argmax(self.histogramLane[:190])
        self.rightLanePos = np.argmax(self.histogramLane[210:]) + 210
        if self.rightLanePos == 210:self.rightLanePos=398
        # Draw green lines to mark the lane edges
#         cv2.line(frameFinal, (self.leftLanePos, 0),(self.leftLanePos, 240), (0, 255, 0), 2)
#         cv2.line(frameFinal, (self.rightLanePos, 0),(self.rightLanePos, 240), (0, 255, 0), 2)
        lines.append([(self.leftLanePos, 0),(self.leftLanePos, 240)])
        lines.append([(self.rightLanePos, 0),(self.rightLanePos, 240)])
        
        # Calculate the lane center by averaging the left and right lane positions
        self.laneCenter = (self.rightLanePos + self.leftLanePos) // 2
        # Define the frame center as a constant
        self.frameCenter = 195
        # Draw yellow line to mark the lane center and blue line to mark the frame center
#         cv2.line(frameFinal, (self.laneCenter, 0),(self.laneCenter, 240), (0, 255, 255), 3)
#         cv2.line(frameFinal, (self.frameCenter, 0),(self.frameCenter, 240), (255, 0, 0), 3)
#         
        lines.append([(self.laneCenter, 0),(self.laneCenter, 240)])
        lines.append([(self.frameCenter, 0),(self.frameCenter, 240)])
        
        # Calculate the result as the difference between the lane center and the frame center
        self.result = self.laneCenter - self.frameCenter
        # Convert the region of interest to grayscale and equalize the histogram
        RoI_Stop = frame_Stop[0:240, 0:400]
        gray_Stop = cv2.cvtColor(RoI_Stop, cv2.COLOR_RGB2GRAY)
        gray_Stop = cv2.equalizeHist(gray_Stop)
        # Display the frames if display is True
        if self.display:
            cv2.imshow("frame with lines", frame)
            cv2.imshow("frameEdge", frameEdge)
            cv2.imshow("frameFinal", frameFinal)
            
        # Clip the result to be between -90 and 90 degrees
        self.result = np.clip(self.result, -90, 90)
        # Normalize the result to be between -1 and 1
        self.result = self.result / 90
        return round(self.result,4),lines
        
    
if __name__ == '__main__':
    eD=edgeDetection(display=True)
    cam=cv2.VideoCapture(0)#PIcamera(disPlay=True)#h=480,w=640

    while True:
        _,frame=cam.read()#cam.capture()
        deg=eD.process(frame)
        print(deg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()        
