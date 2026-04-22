# Copyright (C) 2026 Cryptix
# SPDX-License-Identifier: GPL-3.0-or-later 

import tkinter as tk
import math

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        
        # Input field
        self.display = tk.Entry(root, width=35, justify='right', font=('Arial', 12))
        self.display.grid(row=0, column=0, columnspan=6, pady=15, padx=10)

        # Bind keyboard events
        self.bind_keys()
        self.create_buttons()

    def calculate(self, event=None):
        equation = self.display.get()
        
        # Replace display characters with Python-readable characters
        equation = equation.replace('÷', '/').replace('x', '*').replace(',', '.')
        
        self.display.delete(0, tk.END)
        try:
            # Safe eval: Only allow variables from the math module
            allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
            result = eval(equation, {"__builtins__": {}}, allowed_names)
            
            # Round result to avoid floating-point errors (e.g., 0.300000000004)
            if isinstance(result, float):
                result = round(result, 10)
                
            self.display.insert(0, str(result))
            
        except ZeroDivisionError:
            self.display.insert(0, "Error: Div by 0")
        except (SyntaxError, NameError, TypeError):
            self.display.insert(0, "Invalid Syntax")
        except Exception:
            self.display.insert(0, "Error")

    def clear(self, event=None):
        self.display.delete(0, tk.END)

    def delete_last(self, event=None):
        current_text = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(0, current_text[:-1])

    def insert_value(self, value):
        # Clear the field first if an error message is displayed
        if self.display.get() in ("Invalid Syntax", "Error: Div by 0", "Error"):
            self.clear()
        self.display.insert(tk.END, value)

    def create_buttons(self):
        # Layout for buttons
        buttons = [
            (" 1 ", 1, 0, lambda: self.insert_value("1")),
            (" 2 ", 1, 1, lambda: self.insert_value("2")),
            (" 3 ", 1, 2, lambda: self.insert_value("3")),
            (" ( ", 1, 3, lambda: self.insert_value("(")),
            (" ) ", 1, 4, lambda: self.insert_value(")")),
            (" π ", 1, 5, lambda: self.insert_value(str(math.pi))),

            (" 4 ", 2, 0, lambda: self.insert_value("4")),
            (" 5 ", 2, 1, lambda: self.insert_value("5")),
            (" 6 ", 2, 2, lambda: self.insert_value("6")),
            (" x ", 2, 3, lambda: self.insert_value("*")),
            (" ÷ ", 2, 4, lambda: self.insert_value("/")),
            (" √ ", 2, 5, lambda: self.insert_value("sqrt(")),

            (" 7 ", 3, 0, lambda: self.insert_value("7")),
            (" 8 ", 3, 1, lambda: self.insert_value("8")),
            (" 9 ", 3, 2, lambda: self.insert_value("9")),
            (" + ", 3, 3, lambda: self.insert_value("+")),
            (" - ", 3, 4, lambda: self.insert_value("-")),
            (" ² ", 3, 5, lambda: self.insert_value("**2")),

            (" CLR ", 4, 0, self.clear),
            (" 0 ", 4, 1, lambda: self.insert_value("0")),
            (" DEL ", 4, 2, self.delete_last),
            (" = ", 4, 3, self.calculate),
            (" , ", 4, 4, lambda: self.insert_value(".")),
            (" ³ ", 4, 5, lambda: self.insert_value("**3"))
        ]

        for text, row, column, command in buttons:
            # padx and pady add some spacing between buttons
            btn = tk.Button(self.root, text=text, width=4, height=2, command=command)
            btn.grid(row=row, column=column, padx=2, pady=2)

    def bind_keys(self):
        self.root.bind("<Return>", self.calculate)
        self.root.bind("<Delete>", self.clear)
        self.root.bind("<BackSpace>", self.delete_last)
        # Allow typing directly on the keyboard
        for key in "0123456789+-*/.()":
            self.root.bind(key, lambda event, char=key: self.insert_value(char))

if __name__ == "__main__":
    # This block ensures that the window only opens when the script is run directly.
    root = tk.Tk()
    
    # Prevents the window from being too small or too large and the layout from breaking
    root.resizable(False, False) 
    
    app = CalculatorApp(root)
    root.mainloop()