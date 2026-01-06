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
    
    # --- Higher Level Actions ---
    
    def sprint(self):
        """Toggle sprint (Hold Ctrl + W is typical, but this helper just taps)."""
        # Note: In MC, double-tap W or Hold Ctrl. 
        # For simplicity, our agent should probably explicitly Hold Ctrl if we want to run.
        pass # To be implemented by the Brain logic explicitly calling key_down/up

    def crouch(self, active=True):
        """Holds or releases Shift."""
        if active:
            self.key_down(Key.shift)
        else:
            self.key_up(Key.shift)
            
    def hotbar(self, slot_idx):
        """Select hotbar slot (1-9)."""
        if 1 <= slot_idx <= 9:
            self.press_key(str(slot_idx), duration=0.05)
            
    def inventory(self):
        """Open/Close Inventory (E)."""
        self.press_key('e', duration=0.05)
        
    def interact(self):
        """Right Click (Place, Use, Eat)."""
        self.click(Button.right)
        
    def attack(self):
        """Left Click (Hit, Break)."""
        self.click(Button.left)

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
