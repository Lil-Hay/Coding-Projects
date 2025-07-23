import tkinter

root = tkinter.Tk()
root.title("Calculator")
root.geometry("400x600")

# Create a label to display the calculator title
title_label = tkinter.Label(root, text="Simple Calculator", font=("Arial", 24))
title_label.pack(pady=20)
# Create a frame for the calculator buttons
button_frame = tkinter.Frame(root)
button_frame.pack(pady=10)
# Create buttons for numbers 0-9 and operations
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]
for button in buttons:
    btn = tkinter.Button(button_frame, text=button, font=("Arial", 18), width=5)
    btn.pack(side=tkinter.LEFT, padx=5, pady=5)
# Create an entry widget to display the input and output
entry = tkinter.Entry(root, font=("Arial", 24), justify='right')
entry.pack(pady=20, padx=20, fill=tkinter.X)
# Function to handle button clicks
def button_click(value):
    current_text = entry.get()
    if value == '=':
        try:
            result = evaluate_expression(current_text)
            entry.delete(0, tkinter.END)
            entry.insert(tkinter.END, result)
        except Exception as e:
            entry.delete(0, tkinter.END)
            str(eval(current_text))
            entry.insert(tkinter.END, "Error")
    else:
        entry.insert(tkinter.END, value)    
# Function to evaluate the expression
def evaluate_expression(expression):
    try:
        return str(eval(expression))
    except Exception:
        return "Error"  
# Bind button clicks to the button_click function
for button in buttons:  
    btn = tkinter.Button(button_frame, text=button, font=("Arial", 18), width=5,
                         command=lambda value=button: button_click(value))
    btn.pack(side=tkinter.LEFT, padx=5, pady=5)
# Start the main loop
root.mainloop()
