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
                # Non-blocking control loop (60Hz target)
                start_time = time.time()
                
                # Brain Layer: Decide functionality
                # For now: Just hold W
                self.input.key_down('w')
                
                # Maintain loop rate
                # Sleep small amount to yield but not block for long
                elapsed = time.time() - start_time
                sleep_time = max(0, (1.0/60.0) - elapsed)
                time.sleep(sleep_time)

        except KeyboardInterrupt:
            pass
        finally:
            print("Reflex Agent Stopped.")
            self.input.key_up('w') # Release key on exit

if __name__ == "__main__":
    agent = ReflexAgent()
    agent.start()
