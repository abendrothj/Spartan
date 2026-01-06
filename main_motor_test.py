import time
from src.control.input_mgr import InputManager

def main():
    print("Initializing Motor Control Test...")
    print("Press ESC at any time to EMERGENCY STOP.")
    
    mgr = InputManager()
    
    print("\n--- TEST SEQUENCE STARTING IN 5 SECONDS ---")
    print("Please switch to the Minecraft window NOW.")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
        if not mgr.is_active():
            print("Test aborted by user.")
            return

    try:
        if mgr.is_active():
            print("\n1. Jumping...")
            mgr.jump()
            time.sleep(1)

        if mgr.is_active():
            print("\n2. Crouching (Hold 1s)...")
            mgr.crouch(active=True)
            time.sleep(1)
            mgr.crouch(active=False)
            time.sleep(0.5)

        if mgr.is_active():
            print("\n3. Hotbar Cycle (1-3)...")
            mgr.hotbar(1)
            time.sleep(0.5)
            mgr.hotbar(2)
            time.sleep(0.5)
            mgr.hotbar(3)
            time.sleep(0.5)

        if mgr.is_active():
            print("\n4. Attacking (Left Click)...")
            mgr.attack()
            time.sleep(0.5)

        if mgr.is_active():
            print("\n5. Inventory Test (Open/Close)...")
            mgr.inventory() # Open
            time.sleep(1)
            mgr.inventory() # Close
            time.sleep(0.5)
            
        print("\n--- TEST SEQUENCE COMPLETE ---")
            
    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        # Ensure cleanup if stopped mid-crouch
        try:
            mgr.crouch(active=False)
        except:
            pass

if __name__ == "__main__":
    main()
