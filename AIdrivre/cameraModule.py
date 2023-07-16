from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import cv2

class PIcamera():
    """A class to capture images from Raspberry Pi camera."""

    # Define the constants for resolution and framerate
    RESOLUTION = (400, 208)
    FRAMERATE = 32

    def __init__(self, display=False):
        """Initialize the camera and the raw capture object."""
        self.camera = PiCamera()
        self.display = display
        self.camera.resolution = self.RESOLUTION
        self.camera.framerate = self.FRAMERATE
        self.raw_capture = PiRGBArray(self.camera, size=self.RESOLUTION)
        # Allow the camera to warm up
        sleep(0.1)

    def capture(self):
        """Capture an image from the camera and return it as a numpy array."""
        try:
            # Capture a frame from the camera
            self.camera.capture(self.raw_capture, format="bgr", use_video_port=True)
            # Get the image as a numpy array
            image = self.raw_capture.array
            # Show the image if display is True
            if self.display:
                cv2.imshow("Frame", image)
            # Clear the raw capture for the next frame
            self.raw_capture.truncate(0)
            # Return the image
            return image
        except Exception as e:
            # Handle any exceptions that may occur
            print(f"An error occurred while capturing an image: {e}")
            # Return None if no image was captured
            return None

if __name__ == '__main__':
    cam=PIcamera()
    while True:
        frame=cam.capture()
        cv2.imshow('Horizontal Stacking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
