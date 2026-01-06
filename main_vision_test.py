import cv2
import time
from src.vision.window_mgr import get_minecraft_window, activate_window
from src.vision.capture import ScreenCapture
import mss

import sys

def main():
    print("Initializing Screen Capture...")
    cap = ScreenCapture()
    
    # Allow user to pass window name, e.g. "python main_vision_test.py Firefox"
    target_window = "Minecraft"
    if len(sys.argv) > 1:
        target_window = sys.argv[1]

    print(f"Searching for window: '{target_window}'...")
    
    # Ignore common terminal/runner windows that might match the search query
    ignore_list = ["main_vision_test", "python", "Terminal", "iTerm", "VS Code"]
    window_region = get_minecraft_window(target_window, ignore_titles=ignore_list)
    
    if not window_region:
        print(f"WARNING: Window '{target_window}' not found.")
        print("Falling back to Full Screen capture for performance test.")
        # mss monitor 1 is usually the main screen
        with mss.mss() as sct:
            window_region = sct.monitors[1]

    print(f"Found window at: {window_region}")
    
    # Try to bring window to front
    if 'pid' in window_region:
        print(f"Activating window (PID: {window_region['pid']})...")
        activate_window(window_region['pid'])
    
    # FPS counters
    prev_time = 0
    curr_time = 0
    
    try:
        while True:
            # Capture frame
            if isinstance(window_region, dict) and 'window_id' in window_region:
                frame = cap.capture_window_exclusive(window_region['window_id'])
            else:
                frame = cap.capture_region(window_region)
            
            if frame is None:
                # Window might be minimized or closed
                time.sleep(0.1)
                continue
            
            # FPS Calculation
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time > 0 else 0
            prev_time = curr_time
            
            # Draw FPS on frame
            cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Display
            cv2.imshow("Minecraft Vision (Test)", frame)
            
            # Exit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            # Optional: re-check window position occasionally 
            # if the user moves the window, we might want to update window_region
            # keeping it simple for now to maximize FPS
            
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        print("Vision test stopped.")

if __name__ == "__main__":
    main()
