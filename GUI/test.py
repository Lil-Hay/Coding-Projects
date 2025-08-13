import tkinter as tk

root = tk.Tk()
root.title("Grid with Lines")

# Create a 3x3 grid of frames with borders
for r in range(3):
    for c in range(3):
        # Create a Frame for each cell with a border
        cell_frame = tk.Frame(root, borderwidth=1, relief="solid", width=50, height=50)
        cell_frame.grid(row=r, column=c, padx=2, pady=2, sticky="nsew") # Add padding for visual separation

        # Place a label inside each cell frame
        label = tk.Label(cell_frame, text=f"R{r}C{c}")
        label.pack(expand=True, fill="both") # Make label fill the frame

root.mainloop()