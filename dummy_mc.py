import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Minecraft - Dummy Window")
    root.geometry("800x600")
    
    label = tk.Label(root, text="This is a dummy Minecraft window for testing capture.", font=("Arial", 20))
    label.pack(expand=True)
    
    # create a canvas with some moving things or colors to test FPS
    canvas = tk.Canvas(root, bg="green", width=400, height=300)
    canvas.pack()
    
    rect = canvas.create_rectangle(10, 10, 60, 60, fill="brown")
    
    dx = 2
    dy = 2
    
    def animate():
        nonlocal dx, dy
        coords = canvas.coords(rect)
        if coords[0] <= 0 or coords[2] >= 400:
            dx = -dx
        if coords[1] <= 0 or coords[3] >= 300:
            dy = -dy
            
        canvas.move(rect, dx, dy)
        root.after(16, animate) # ~60 FPS
        
    animate()
    
    root.mainloop()

if __name__ == "__main__":
    main()
