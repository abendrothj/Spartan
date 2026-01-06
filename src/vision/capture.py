import mss
import numpy as np
import cv2
import Quartz
import ctypes

class ScreenCapture:
    def __init__(self):
        self.sct = mss.mss()

    def capture_region(self, region, target_size=(640, 360)):
        """
        Captures a specific region of the screen (efficiently).
        Args:
            region (dict): {'top': int, 'left': int, 'width': int, 'height': int}
            target_size (tuple): (width, height) to resize for the brain. Default 640x360.
        Returns:
            numpy.ndarray: The captured image in BGR format.
        """
        screenshot = self.sct.grab(region)
        img = np.array(screenshot)
        img_bgr = img[:, :, :3]
        
        if target_size:
            img_bgr = cv2.resize(img_bgr, target_size, interpolation=cv2.INTER_AREA)
        
        return np.ascontiguousarray(img_bgr)

    def capture_window_exclusive(self, window_id, target_size=(640, 360)):
        """
        Captures a specific window ID, even if occluded.
        Uses macOS Quartz API (CGWindowListCreateImage).
        """
        # CGWindowListOptionIncludingWindow = 8
        # kCGWindowImageBoundsIgnoreFraming = 1
        # kCGWindowImageNominalResolution = 16 (optional, speeds up if 1.0 scale)
        
        image_ref = Quartz.CGWindowListCreateImage(
            Quartz.CGRectNull,
            8, # kCGWindowListOptionIncludingWindow
            window_id,
            1 | 16 # IgnoreFraming | NominalResolution
        )
        
        if not image_ref:
            return None
            
        width = Quartz.CGImageGetWidth(image_ref)
        height = Quartz.CGImageGetHeight(image_ref)
        bytes_per_row = Quartz.CGImageGetBytesPerRow(image_ref)
        pixel_data = Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(image_ref))
        
        # Convert raw bytes to numpy array
        # Handle Potential Stride/Padding
        # Raw data might have padding bytes at the end of each row
        raw_data = np.frombuffer(pixel_data, dtype=np.uint8)
        
        # Reshape to (Height, BytesPerRow) then crop to (Height, Width * 4)
        # Note: bytes_per_row >= width * 4
        if len(raw_data) == height * bytes_per_row:
             img_padded = raw_data.reshape((height, bytes_per_row))
             img_flat = img_padded[:, :width*4]
             img = img_flat.reshape((height, width, 4))
        else:
             # Fallback or error if size doesn't match expected stride logic
             # Trying direct reshape if matches perfectly (rare)
             img = raw_data.reshape((height, width, 4))
        
        # Drop Alpha channel (BGRA -> BGR)
        img_bgr = img[:, :, :3]
        
        if target_size:
            img_bgr = cv2.resize(img_bgr, target_size, interpolation=cv2.INTER_AREA)

        return np.ascontiguousarray(img_bgr)

    def save_debug_screenshot(self, img, filename="debug_capture.png"):
        cv2.imwrite(filename, img)
