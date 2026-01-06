import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.control.input_mgr import InputManager

class ReflexAgent:
    def __init__(self):
        self.input = InputManager()
        self.is_running = False

    def start(self):
        self.is_running = True
        print("Reflex Agent Started. Walking forward in 3 seconds...")
        print("Click into Minecraft NOW.")
        time.sleep(3)
        
        try:
            while self.is_running and self.input.is_active():
                # Primitive "Loop": just walk forward
                # Later, this will read "Vision" state
                print("Action: Walk Forward")
                self.input.press_key('w', duration=0.5)
                
                # Small pause to look human-ish
                time.sleep(0.1)

        except KeyboardInterrupt:
            pass
        finally:
            print("Reflex Agent Stopped.")

if __name__ == "__main__":
    agent = ReflexAgent()
    agent.start()
