import mss
import numpy as np

class ScreenCapture:
    def __init__(self):
        self.sct = mss.mss()

    def capture_region(self, region):
        """
        Captures a specific region of the screen.
        Args:
            region (dict): {'top': int, 'left': int, 'width': int, 'height': int}
        Returns:
            numpy.ndarray: The captured image in BGR format (ready for OpenCV).
        """
        # mss returns a dictionary with 'bgra' raw bytes
        # We convert it to a numpy array
        
        # Grab the data
        # Note: region keys should be 'top', 'left', 'width', 'height'
        screenshot = self.sct.grab(region)
        
        # Convert to numpy array
        img = np.array(screenshot)
        
        # MSS returns BGRA, typical OpenCV usage is BGR
        # We can drop the alpha channel for processing speed and compatibility
        img_bgr = img[:, :, :3]
        
        return np.ascontiguousarray(img_bgr)

    def save_debug_screenshot(self, img, filename="debug_capture.png"):
        import cv2
        cv2.imwrite(filename, img)
