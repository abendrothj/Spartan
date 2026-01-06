import cv2
import numpy as np
from src.brain.slow_brain import VisionBrain
import os

def create_dummy_image(filename="test_input.png"):
    # Create a simple image: Green ground, Blue sky, Gray "Wall"
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    
    # Sky (Blue-ish)
    img[:256, :] = [235, 206, 135] # Skye Blue in BGR
    
    # Ground (Green)
    img[256:, :] = [34, 139, 34] # Forest Green in BGR
    
    # Wall (Gray Block in middle)
    cv2.rectangle(img, (200, 100), (440, 260), (128, 128, 128), -1)
    
    # Text hint
    cv2.putText(img, "Minecraft Wall", (220, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
    
    cv2.imwrite(filename, img)
    print(f"Created dummy input: {filename}")
    return filename

def main():
    print("--- Brain Verification Test ---")
    
    # 1. Setup Data
    image_path = create_dummy_image()
    history = "[12:00:00] Action: Walk Forward -> Result: Stopped."
    
    # 2. Init Brain
    try:
        brain = VisionBrain()
        
        # 3. Inference
        print("\nThinking...")
        response = brain.see_and_think(image_path, history)
        
        print("\n--- Model Output ---")
        print(response)
        print("--------------------")
        
    except Exception as e:
        print(f"Brain Test Failed: {e}")

if __name__ == "__main__":
    main()
