import tkinter
import calculator

evaluate_expression = calculator.Calculator.evaluate_expression

def button_click(value):
    current_text = entry.get()
    if value == '=':
        try:
            result = evaluate_expression(current_text)
            entry.delete(0, tkinter.END)
            entry.insert(tkinter.END, result)
        except Exception:
            entry.delete(0, tkinter.END)
            entry.insert(tkinter.END, "Error")
    else:
        entry.insert(tkinter.END, value)

root = tkinter.Tk()
root.title("Calculator")
root.geometry("400x600")

title_label = tkinter.Label(root, text="Simple Calculator", font=("Arial", 24))
title_label.pack(pady=20)

button_frame = tkinter.Frame(root)
button_frame.pack(pady=10)

buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

for button in buttons:
    btn = tkinter.Button(button_frame, text=button, font=("Arial", 18), width=5,
                         command=lambda value=button: button_click(value))
    btn.grid(row=buttons.index(button) // 4, column=buttons.index(button) % 4)

entry = tkinter.Entry(root, font=("Arial", 24), justify='right')
entry.pack(pady=20, padx=20, fill=tkinter.X)

root.mainloop()