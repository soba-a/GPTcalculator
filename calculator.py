import tkinter as tk
import tkinter.font as font
import ast
import operator as op

# supported operators
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.USub: op.neg, ast.Pow: op.pow}

def evaluate_expr(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return operators[type(node.op)](evaluate_expr(node.left), evaluate_expr(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return operators[type(node.op)](evaluate_expr(node.operand))
    else:
        raise TypeError(node)

def safe_eval(expr):
    return evaluate_expr(ast.parse(expr, mode='eval').body)

# Create the window
window = tk.Tk()

# Create a Text widget to replace the Entry widget
display = tk.Text(window, height=1, borderwidth=5)
display.grid(row=0, column=0, columnspan=4, sticky="nsew")

# Define what each button does
def click(number):
    current = display.get("1.0", 'end-1c')
    if len(current) < 20: # limit length of input
        display.delete("1.0", tk.END)
        display.insert(tk.END, current + str(number))

def clear():
    display.delete("1.0", tk.END)

# def calculate():
#     try:
#         smallest_decimals = float('inf')
#         current = display.get("1.0", 'end-1c')
#         for number in current.split():
#             if '.' in number:
#                 decimals = len(number) - number.index('.') - 1
#                 smallest_decimals = min(smallest_decimals, decimals)
        
#         result = safe_eval(current)

#         if isinstance(result, float):
#             result = round(result, smallest_decimals)

#         display.delete("1.0", tk.END)
#         display.insert(tk.END, result)
#     except Exception as e:
#         display.delete("1.0", tk.END)
#         display.insert(tk.END, "Error: " + str(e))

def calculate():
    try:
        smallest_decimals = float('inf')
        current = display.get("1.0", 'end-1c')
        for number in current.split():
            if '.' in number:
                decimals = len(number) - number.index('.') - 1
                smallest_decimals = min(smallest_decimals, decimals)
        
        result = safe_eval(current)

        if isinstance(result, float):
            # Check if smallest_decimals is still at its initial value
            if smallest_decimals == float('inf'):
                result = round(result)
            else:
                result = round(result, smallest_decimals)

        display.delete("1.0", tk.END)
        display.insert(tk.END, result)
    except Exception as e:
        display.delete("1.0", tk.END)
        display.insert(tk.END, "Error: " + str(e))

def press_button(button):
    button.config(relief='sunken')
    window.after(100, lambda: button.config(relief='raised'))

def key_press(event):
    keysym_to_button_text = {
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
        'plus': '+', 'minus': '-', 'asterisk': '*', 'slash': '/', 'period': '.', 'Return': '=', 'c': 'C', 'C': 'C',
        'Escape': 'C', 'asciicircum': '**'  # This key corresponds to the '^' symbol.
    }
    if event.keysym in keysym_to_button_text:
        button_text = keysym_to_button_text[event.keysym]
        for button in button_widgets:
            if button['text'] == button_text:
                button.invoke()
                press_button(button)
                break

# Create the buttons
buttons = [
    "7", "8", "9", "+",
    "4", "5", "6", "-",
    "1", "2", "3", "*",
    "0", ".", "=", "/",
    "C", "**"  # Added an exponentiation button.
]

button_widgets = []

for i, button in enumerate(buttons):
    if button == "C":
        b = tk.Button(window, text=button, command=clear)
    else:
        b = tk.Button(window, text=button, command=lambda button=button: click(button) if button != "=" else calculate())
    b.grid(row=1+i//4, column=i%4, sticky="nsew")
    b.bind("<Button-1>", lambda event: press_button(event.widget))
    button_widgets.append(b)

# Configure the grid cells to expand to fill the window
for i in range(4):
    window.grid_columnconfigure(i, weight=1)
for i in range(1 + len(buttons) // 4):
    window.grid_rowconfigure(i, weight=1)

def resize_font(event):
    # Calculate the size factor based on window size.
    size_factor = min(window.winfo_height(), window.winfo_width())

    # Change font size based on size_factor. Here 15 is the base size of the font.
    new_font = font.Font(size=int(size_factor // 15))

    # Configure all buttons and the display label to use the new font.
    display.configure(font=new_font)
    for button in button_widgets:
        button['font'] = new_font

window.bind('<Configure>', resize_font)
window.bind_all('<Key>', key_press)
window.mainloop()
