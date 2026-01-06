from pynput.keyboard import Key, Controller as KeyboardController, Listener
from pynput.mouse import Button, Controller as MouseController
import time
import threading

class InputManager:
    def __init__(self, kill_key=Key.esc):
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.stop_event = threading.Event()
        self.kill_key = kill_key
        
        # Start the failsafe listener in a non-blocking way
        self.listener = Listener(on_press=self._on_press)
        self.listener.start()
        print(f"InputManager initialized. Press '{self.kill_key}' to trigger emergency stop.")

    def _on_press(self, key):
        # Emergency Kill Switch
        if key == self.kill_key:
            print(f"\n[FAILSAFE] {self.kill_key} pressed! Stopping all input...")
            self.stop_event.set()
            return False # Stop listener

    def key_down(self, key):
        """Hold a key down."""
        if not self.is_active(): return
        self.keyboard.press(key)

    def key_up(self, key):
        """Release a key."""
        # Always allow releasing keys even if stopped, to prevent stuck keys
        self.keyboard.release(key)

    def is_active(self):
        """Check if we are allowed to proceed."""
        return not self.stop_event.is_set()

    def press_key(self, char_or_key, duration=0.1):
        """
        Presses a key for a specific duration.
        Args:
            char_or_key: A character string ('w') or Key object (Key.space).
        """
        if not self.is_active(): return

        self.key_down(char_or_key)
        
        # We need to sleep in small chunks to check for stop interrupt
        start = time.time()
        while time.time() - start < duration:
            if not self.is_active():
                self.key_up(char_or_key)
                return
            time.sleep(0.01)
            
        self.key_up(char_or_key)

    def move_mouse(self, dx, dy):
        """
        Moves the mouse relative to current position.
        Crucial for Minecraft 3D camera control.
        """
        if not self.is_active(): return
        self.mouse.move(dx, dy)

    def click(self, button=Button.left):
        if not self.is_active(): return
        self.mouse.click(button)

    def jump(self):
        self.press_key(Key.space, duration=0.1)

if __name__ == "__main__":
    print("Testing InputManager - PRESS ESC TO STOP")
    mgr = InputManager()
    
    # Simple test loop: Type 'a' every second
    try:
        while mgr.is_active():
            print("Typing 'a'...")
            mgr.press_key('a')
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    print("Test finished.")
