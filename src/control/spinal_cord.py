import threading
import time
import queue
import cv2
import os

from src.brain.slow_brain import VisionBrain
from src.control.input_mgr import InputManager
from src.vision.capture import ScreenCapture
from src.vision.window_mgr import get_minecraft_window

class SpinalCord:
    def __init__(self):
        print("Initializing Spinal Cord (Integration Layer)...")
        
        # 1. The Body (Fast / Real-time)
        self.input = InputManager()
        
        # 2. The Eyes
        self.eyes = ScreenCapture()
        self.window_info = None
        
        # 3. The Brain (Slow / Async)
        # Verify model exists or handle loading
        try:
            self.brain = VisionBrain()
        except Exception as e:
            print(f"CRITICAL: Failed to load Brain: {e}")
            self.brain = None
            
        self.action_queue = queue.Queue()
        self.running = True
        self.latest_plan = "Idle"

    def start(self):
        """Starts the autonomous loop."""
        if not self.brain:
            print("Brain not loaded. Aborting.")
            return

        print("Spinal Cord Active.")
        print(" [!] PRESS ESC TO KILL BOT [!]")
        
        # Start Thinking (Background Thread)
        think_thread = threading.Thread(target=self.think_loop)
        think_thread.daemon = True
        think_thread.start()
        
        # Run Acting (Main Thread - blocks until ESC)
        self.act_loop()

    def think_loop(self):
        """
        The Slow Loop:
        1. Capture Image
        2. VLM Inference
        3. Parse Command -> Action Queue
        """
        print("Think Loop Started.")
        
        while self.running and self.input.is_active():
            # Rate limit the brain to avoid spamming if inference is fast (unlikely)
            time.sleep(1.0) 
            
            # 1. Update Window Info (in case it moved)
            if not self.window_info:
                self.window_info = get_minecraft_window("Minecraft")
            
            if not self.window_info:
                print("Brain: Waiting for 'Minecraft' window...")
                time.sleep(2)
                continue
                
            # 2. See
            frame = self.eyes.capture_window_exclusive(self.window_info.get('window_id'))
            if frame is None:
                continue
                
            # Save temp for VLM
            temp_path = "vision_temp.png"
            cv2.imwrite(temp_path, frame)
            
            # 3. Think
            history = f"Last Plan: {self.latest_plan}"
            print("\nBrain: Thinking...")
            response = self.brain.see_and_think(temp_path, history)
            
            print(f"Brain: Thought -> '{response}'")
            self.latest_plan = response
            
            # 4. Parse & Queue Actions
            self.parse_thought_to_actions(response)

    def parse_thought_to_actions(self, thought_text):
        """
        Crude parser to convert VLM natural text into Motor Actions.
        TODO: Improve this with structured JSON output from VLM later.
        """
        text = thought_text.lower()
        
        # Clear previous queue actions? 
        # Yes, new thought overrides old plans usually.
        # But be careful not to jerk too much. For now, clear.
        with self.action_queue.mutex:
            self.action_queue.queue.clear()
            
        # --- Simple Heuristics ---
        
        # Walk Forward
        if "walk" in text or "forward" in text or "approach" in text:
            # Queue: Hold W for 2 seconds
            self.action_queue.put(("key_down", "w"))
            self.action_queue.put(("wait", 2.0))
            self.action_queue.put(("key_up", "w"))
            
        # Jump
        if "jump" in text:
            self.action_queue.put(("press", "space"))
            
        # Stop / Wait
        if "stop" in text or "wait" in text:
            self.action_queue.put(("key_up", "w")) # Safety ensure stop
            
        # Turn Left/Right (Crudely)
        if "left" in text:
             self.action_queue.put(("mouse_move", (-200, 0)))
        if "right" in text:
             self.action_queue.put(("mouse_move", (200, 0)))

        # Interact / Attack
        if "break" in text or "attack" in text or "hit" in text:
            self.action_queue.put(("attack", None))
        if "place" in text or "use" in text:
            self.action_queue.put(("interact", None))

    def act_loop(self):
        """
        The Fast Loop:
        Executes actions from the queue safely.
        """
        while self.running and self.input.is_active():
            try:
                # Non-blocking get
                cmd_tuple = self.action_queue.get(timeout=0.1)
                cmd, val = cmd_tuple
                
                print(f"Act: Executing {cmd} {val}")
                
                if cmd == "key_down":
                    self.input.key_down(val)
                elif cmd == "key_up":
                    self.input.key_up(val)
                elif cmd == "press":
                    self.input.press_key(getattr(os, 'dummy', val), duration=0.1) # Handle string vs Key obj? InputMgr handles strings.
                elif cmd == "wait":
                    time.sleep(val) # Note: input_mgr.is_active() check is inside start of next loop, but sleep blocks ESC check in this thread. 
                    # Better: sleep in chunks
                    elapsed = 0
                    while elapsed < val:
                        if not self.input.is_active(): break
                        time.sleep(0.1)
                        elapsed += 0.1
                elif cmd == "mouse_move":
                    self.input.move_mouse(val[0], val[1])
                elif cmd == "attack":
                    self.input.attack()
                elif cmd == "interact":
                    self.input.interact()
                    
            except queue.Empty:
                pass
            except Exception as e:
                print(f"Act Error: {e}")
                
        # Cleanup
        print("Spinal Cord stopping...")
        self.running = False

if __name__ == "__main__":
    # Test Stub
    cord = SpinalCord()
    # cord.start() 
    print("SpinalCord Class Ready.")
