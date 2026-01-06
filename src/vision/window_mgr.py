import Quartz

from AppKit import NSRunningApplication, NSApplicationActivateIgnoringOtherApps

def get_minecraft_window(target_title="Minecraft", ignore_titles=None):
    """
    Finds a window with the given title (partial match) using Quartz.
    Args:
        target_title (str): The window title to search for. Default "Minecraft".
        ignore_titles (list): List of strings to exclude (case-insensitive).
    Returns:
        dict: {'x': int, 'y': int, 'width': int, 'height': int, 'pid': int} or None
    """
    if ignore_titles is None:
        ignore_titles = []

    # Get all on-screen windows
    options = Quartz.kCGWindowListOptionOnScreenOnly
    window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)

    print(f"Debug: Searching for window containing '{target_title}'...")

    for window in window_list:
        title = window.get('kCGWindowName', '')
        owner = window.get('kCGWindowOwnerName', '')
        pid = window.get('kCGWindowOwnerPID')
        
        full_title = str(title).lower()
        full_owner = str(owner).lower()
        target = target_title.lower()

        # Skip if matches ignore list
        if any(ignored.lower() in full_title for ignored in ignore_titles) or \
           any(ignored.lower() in full_owner for ignored in ignore_titles):
            continue

        # Check if target is in title or owner (case-insensitive for better UX)
        if target in full_title or target in full_owner:
            bounds = window.get('kCGWindowBounds')
            if bounds:
                return {
                    'top': int(bounds['Y']),
                    'left': int(bounds['X']),
                    'width': int(bounds['Width']),
                    'height': int(bounds['Height']),
                    'pid': int(pid)
                }
    
    # If not found during loop, print what we saw to debug
    print("Debug: List of windows found:")
    for window in window_list:
        title = window.get('kCGWindowName', '')
        owner = window.get('kCGWindowOwnerName', '')
        if title:
            print(f" - Title: '{title}', Owner: '{owner}'")
    
    return None

def activate_window(pid):
    """
    Brings the application with the given PID to the foreground.
    """
    app = NSRunningApplication.runningApplicationWithProcessIdentifier_(pid)
    if app:
        app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
        return True
    return False

if __name__ == "__main__":
    win = get_minecraft_window()
    if win:
        print(f"Found Minecraft window: {win}")
    else:
        print("Minecraft window not found.")
