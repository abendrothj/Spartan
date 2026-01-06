from src.control.spinal_cord import SpinalCord
import time

def main():
    print("--- SPARTAN VLA AGENT: FULL AUTONOMY TEST ---")
    print("Initialization takes a few seconds (loading Brain)...")
    
    cord = SpinalCord()
    
    print("\nREADY TO START.")
    print("1. Open Minecraft.")
    print("2. Make sure you are in a safe spot (Creative Mode recommended).")
    print("3. The bot will take screenshots, think, and try to move.")
    print("4. PRESS 'ESC' TO STOP IMMEDIATELY.")
    
    input("Press Enter to launch...")
    
    print("Launching in 3 seconds...")
    time.sleep(3)
    
    cord.start()

if __name__ == "__main__":
    main()
