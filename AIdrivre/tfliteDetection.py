import os
import cv2
import numpy as np
import time
import importlib.util

class objectDetection():
# Define a class for the model
    def __init__(self):
        # Set the model name
        self.MODEL_NAME ="lite"
        # Set the graph name
        self.GRAPH_NAME = 'detect.tflite'
        # Set the label map name
        self.LABELMAP_NAME = 'labelmap.txt'
        # Set the minimum confidence threshold for detection
        self.min_conf_threshold = 0.7
        # Set the image width and height
        self.imW = 400
        self.imH = 208
        # Set the flag for using TPU or not
        # Import the tflite_runtime package if available, otherwise import the tensorflow.lite package
        pkg = importlib.util.find_spec('tflite_runtime')
        if pkg:
            from tflite_runtime.interpreter import Interpreter
        else:
            from tensorflow.lite.python.interpreter import Interpreter
        # Get the current working directory
        CWD_PATH = os.getcwd()
        # Get the path to the model file
        #PATH_TO_CKPT = os.path.join(CWD_PATH,self.MODEL_NAME,self.GRAPH_NAME)
        PATH_TO_CKPT="/home/pi/Desktop/Code/AIdrivre/lite/detect.tflite"

        # Get the path to the label map file
        #PATH_TO_LABELS = os.path.join(CWD_PATH,self.MODEL_NAME,self.LABELMAP_NAME)
        PATH_TO_LABELS="/home/pi/Desktop/Code/AIdrivre/lite/labelmap.txt"

        # Open the label map file and read the labels into a list
        #print("PATH:",PATH_TO_LABELS)
        #print("PATH:",os.listdir())
        #import glob
        #folder = "/AIdrivre"
        #files = glob.glob(folder + "/*") # matches any file or directory under /etc
        #print(files)
        #print(os.access(PATH_TO_LABELS,mode=1))
        with open(PATH_TO_LABELS, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

        # If the first label is '???', remove it from the list
        if self.labels[0] == '???':
            del(self.labels[0])
        # Create an interpreter object with the model file
        PATH_TO_LABELS="/home/pi/Desktop/Code/AIdrivre/lite/labelmap.txt"
        self.interpreter = Interpreter(model_path=PATH_TO_CKPT)
        # Allocate tensors for the interpreter
        self.interpreter.allocate_tensors()
        # Get the input and output details of the interpreter
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        # Get the height and width of the input tensor
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]
        # Check if the input tensor is floating point or not
        self.floating_model = (self.input_details[0]['dtype'] == np.float32)
        # Set the input mean and standard deviation for normalization
        self.input_mean = 127.5
        self.input_std = 127.5
        # Get the output name of the interpreter
        outname = self.output_details[0]['name']
        # Check if the output name contains 'StatefulPartitionedCall' or not and assign the indices of boxes, classes and scores accordingly
        if ('StatefulPartitionedCall' in outname):
            self.boxes_idx, self.classes_idx, self.scores_idx = 1, 3, 0
        else:
            self.boxes_idx, self.classes_idx, self.scores_idx = 0, 1, 2



    # Define a function to detect objects in a frame
    def detect(self,frame):
        # Convert the frame from BGR to RGB color space
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Resize the frame to match the input tensor size
        frame_resized = cv2.resize(frame_rgb, (self.width, self.height))
        # Expand the frame dimension to fit the batch size of 1
        input_data = np.expand_dims(frame_resized, axis=0)
        # If the input tensor is floating point, normalize the frame values
        if self.floating_model:
            input_data = (np.float32(input_data) - self.input_mean) / self.input_std
        # Set the input tensor with the frame data
        self.interpreter.set_tensor(self.input_details[0]['index'],input_data)
        # Invoke the interpreter to run the inference
        self.interpreter.invoke()
        # Get the output tensors for boxes, classes and scores
        boxes = self.interpreter.get_tensor(self.output_details[self.boxes_idx]['index'])[0] 
        classes = self.interpreter.get_tensor(self.output_details[self.classes_idx]['index'])[0]
        scores = self.interpreter.get_tensor(self.output_details[self.scores_idx]['index'])[0] 
        # Loop through the scores and filter out the ones below the confidence threshold
        speeds=[]
        colors=[]
        cars=[]
        for i in range(len(scores)):
            if ((scores[i] > self.min_conf_threshold) and (scores[i] <= 1.0)):
                # Get the coordinates of the bounding box for the detected object
                ymin = int(max(1,(boxes[i][0] * self.imH)))
                xmin = int(max(1,(boxes[i][1] * self.imW)))
                ymax = int(min(self.imH,(boxes[i][2] * self.imH)))
                xmax = int(min(self.imW,(boxes[i][3] * self.imW)))
                # Draw a rectangle around the detected object on the frame
                cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
                # Get the name of the detected object from the label map
                object_name = self.labels[int(classes[i])] 
                # Format a label with the object name and score percentage
                label = '%s: %d%%' % (object_name, int(scores[i]*100)) 
                # Get the size and baseline of the label text
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                # Calculate the y coordinate of the label based on its height and position
                label_ymin = max(ymin, labelSize[1] + 10)
                # Draw a white filled rectangle behind the label text
                cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) 
                # Put the label text on top of the white rectangle
                cv2.putText(frame, label, (xmin+15, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) 

                if classes[i] in ["red","green"]:
                    colors.append([classes[i],scores[i]])
                elif classes[i] in ["s30","s60"]:
                     speeds.append([classes[i],scores[i]])
                else:
                    cars.append([xmin,ymin,xmax,ymax])
        return frame,speeds,colors,cars


if __name__ == "__main__":
    from cameraModule import PIcamera
    obj=objectDetection()
    cam=PIcamera(display= not True)
    while True:
        frame=cam.capture()
        frm, speeds, colors, cars = obj.detect(frame)
        cv2.imshow("frame",frm)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

