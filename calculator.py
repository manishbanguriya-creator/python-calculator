import tkinter as tk
from tkinter import messagebox
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Full-Featured Calculator")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        
        # Display variable
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        self.expression = ""
        self.history = []
        
        # Create UI
        self.create_widgets()
    
    def create_widgets(self):
        # Display frame
        display_frame = tk.Frame(self.root, bg="#34495e", bd=2, relief=tk.SUNKEN)
        display_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=False)
        
        # Display label
        self.display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 24, "bold"),
            bg="#34495e",
            fg="#ecf0f1",
            anchor="e",
            padx=10,
            pady=20
        )
        self.display_label.pack(fill=tk.BOTH, expand=True)
        
        # History frame
        history_frame = tk.LabelFrame(self.root, text="History", font=("Arial", 10, "bold"), 
                                      bg="#2c3e50", fg="#ecf0f1", padx=5, pady=5)
        history_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # History text widget with scrollbar
        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(history_frame, height=6, font=("Arial", 9), 
                                    bg="#34495e", fg="#ecf0f1", yscrollcommand=scrollbar.set)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_text.yview)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#2c3e50")
        buttons_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=False)
        
        # Button layout
        buttons = [
            ["7", "8", "9", "/", "√"],
            ["4", "5", "6", "*", "^"],
            ["1", "2", "3", "-", "%"],
            ["0", ".", "=", "+", "C"],
            ["sin", "cos", "tan", "π", "DEL"],
            ["log", "ln", "(", ")", "CLR"]
        ]
        
        for row in buttons:
            row_frame = tk.Frame(buttons_frame, bg="#2c3e50")
            row_frame.pack(fill=tk.BOTH, expand=True, pady=2)
            
            for btn_text in row:
                self.create_button(btn_text, row_frame)
    
    def create_button(self, text, parent):
        # Button styling based on type
        if text in ["=", "C", "CLR"]:
            bg_color = "#e74c3c"
            fg_color = "white"
        elif text in ["sin", "cos", "tan", "log", "ln", "√", "^", "%", "π"]:
            bg_color = "#3498db"
            fg_color = "white"
        elif text in ["/", "*", "-", "+"]:
            bg_color = "#f39c12"
            fg_color = "white"
        else:
            bg_color = "#95a5a6"
            fg_color = "white"
        
        btn = tk.Button(
            parent,
            text=text,
            font=("Arial", 14, "bold"),
            bg=bg_color,
            fg=fg_color,
            command=lambda: self.on_button_click(text),
            relief=tk.RAISED,
            bd=2
        )
        btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
    
    def on_button_click(self, char):
        current = self.display_var.get()
        
        if char == "C":
            self.display_var.set("0")
            self.expression = ""
        
        elif char == "CLR":
            self.history = []
            self.history_text.delete(1.0, tk.END)
            self.display_var.set("0")
            self.expression = ""
        
        elif char == "DEL":
            if current != "0":
                self.display_var.set(current[:-1] if len(current) > 1 else "0")
        
        elif char == "=":
            try:
                result = self.evaluate_expression(self.expression or current)
                self.add_to_history(f"{self.expression or current} = {result}")
                self.display_var.set(str(result))
                self.expression = ""
            except Exception as e:
                messagebox.showerror("Error", f"Invalid expression: {str(e)}")
                self.display_var.set("0")
                self.expression = ""
        
        elif char == "π":
            self.expression = current if current == "0" else current
            self.expression = str(math.pi)
            self.display_var.set(str(math.pi)[:10])
        
        elif char in ["sin", "cos", "tan"]:
            try:
                val = float(current if current != "0" else "0")
                if char == "sin":
                    result = math.sin(math.radians(val))
                elif char == "cos":
                    result = math.cos(math.radians(val))
                else:
                    result = math.tan(math.radians(val))
                self.add_to_history(f"{char}({val}) = {result}")
                self.display_var.set(str(round(result, 10)))
                self.expression = str(result)
            except:
                messagebox.showerror("Error", "Invalid input for trigonometric function")
        
        elif char == "√":
            try:
                val = float(current if current != "0" else "0")
                result = math.sqrt(val)
                self.add_to_history(f"√{val} = {result}")
                self.display_var.set(str(result))
                self.expression = str(result)
            except:
                messagebox.showerror("Error", "Cannot calculate square root of negative number")
        
        elif char == "^":
            self.expression = current
            self.display_var.set("0")
        
        elif char == "%":
            try:
                val = float(current if current != "0" else "0")
                result = val / 100
                self.add_to_history(f"{val}% = {result}")
                self.display_var.set(str(result))
                self.expression = str(result)
            except:
                messagebox.showerror("Error", "Invalid input")
        
        elif char == "log":
            try:
                val = float(current if current != "0" else "0")
                result = math.log10(val)
                self.add_to_history(f"log({val}) = {result}")
                self.display_var.set(str(result))
                self.expression = str(result)
            except:
                messagebox.showerror("Error", "Invalid input for logarithm")
        
        elif char == "ln":
            try:
                val = float(current if current != "0" else "0")
                result = math.log(val)
                self.add_to_history(f"ln({val}) = {result}")
                self.display_var.set(str(result))
                self.expression = str(result)
            except:
                messagebox.showerror("Error", "Invalid input for natural logarithm")
        
        else:
            # Number or operator
            if current == "0" and char not in [".", "+", "-", "*", "/"]:
                self.display_var.set(char)
                self.expression = char
            elif char == "." and "." in current:
                pass  # Prevent multiple decimals
            else:
                if char in ["+", "-", "*", "/", "^", "("]:
                    self.expression = current
                self.display_var.set(current + char)
    
    def evaluate_expression(self, expr):
        # Replace ^ with ** for power operation
        expr = expr.replace("^", "**")
        result = eval(expr)
        return round(result, 10)
    
    def add_to_history(self, entry):
        self.history.append(entry)
        self.history_text.insert(tk.END, entry + "\n")
        self.history_text.see(tk.END)  # Auto-scroll to bottom

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
