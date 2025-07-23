import tkinter

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.geometry("400x600")

        self.entry = tkinter.Entry(master, font=("Arial", 24), justify='right')
        self.entry.pack(pady=20, padx=20, fill=tkinter.X)

        title_label = tkinter.Label(master, text="Simple Calculator", font=("Arial", 24))
        title_label.pack(pady=20)

        button_frame = tkinter.Frame(master)
        button_frame.pack(pady=10)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        for button in buttons:
            btn = tkinter.Button(button_frame, text=button, font=("Arial", 18), width=5,
                                 command=lambda value=button: self.button_click(value))
            btn.pack(side=tkinter.LEFT, padx=5, pady=5)

    def button_click(self, value):
        current_text = self.entry.get()
        if value == '=':
            try:
                result = self.evaluate_expression(current_text)
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, result)
            except Exception:
                self.entry.delete(0, tkinter.END)
                self.entry.insert(tkinter.END, "Error")
        else:
            self.entry.insert(tkinter.END, value)

    def evaluate_expression(self, expression):
        try:
            return str(eval(expression))
        except Exception:
            return "Error"