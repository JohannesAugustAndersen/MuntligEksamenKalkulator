import tkinter as tk  # Importerer tkinter biblioteket for GUI
import sympy as sp  # Importerer sympy biblioteket for symbolsk matematikk
from matplotlib.figure import Figure  # Importerer Figure fra matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Importerer FigureCanvasTkAgg for å integrere matplotlib med tkinter
from derivate import Derivation

# Definerer en basis klasse for operasjoner
class Operation:
    def execute(self, x, y):
        pass

# Definerer en klasse for addisjon som arver fra Operation
class Add(Operation):
    def execute(self, x, y):
        return x + y

# Definerer en klasse for subtraksjon som arver fra Operation
class Subtract(Operation):
    def execute(self, x, y):
        return x - y

# Definerer en klasse for multiplikasjon som arver fra Operation
class Multiply(Operation):
    def execute(self, x, y):
        return x * y

# Definerer en klasse for divisjon som arver fra Operation
class Divide(Operation):
    def execute(self, x, y):
        if y == 0:
            return "kan ikke dele på 0"
        return x / y

# Hovedklassen for kalkulator applikasjonen
class CalculatorApp(Derivation):
    def __init__(self, tk_root):
        self.root = tk_root
        self.root.title("Kalkulator")

        # Ordbok for operasjoner
        self.operations = {
            "+": Add(),
            "-": Subtract(),
            "*": Multiply(),
            "/": Divide()
        }

        self.current_input = ""  # Nåværende input
        self.first_num = None  # Første nummer i operasjonen
        self.operator = None  # Operasjonen som skal utføres

        self.create_widgets()  # Oppretter GUI komponenter

    def create_widgets(self):
        # Oppretter displayet
        self.display = tk.Entry(self.root, font=("Arial", 24), bd=10, insertwidth=2, width=14, borderwidth=4)
        self.display.grid(row=0, column=0, columnspan=4)

        # Liste over knapper
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', 'C', '=', '+'
        ]

        # Legger til knappene til grid
        row = 1
        col = 0
        for button in buttons:
            tk.Button(self.root, text=button, padx=20, pady=20, font=("Arial", 18),
                      command=lambda b=button: self.on_button_click(b)).grid(row=row, column=col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Legger til derivasjonsknappen
        tk.Button(self.root, text="Derivasjon", padx=10, pady=20, font=("Arial", 18), command=self.open_derivative_calculator).grid(row=row, column=0, columnspan=4)

    def on_button_click(self, char):
        # Håndterer tallknapper
        if char in '0123456789':
            self.current_input += char
            self.update_display()
        # Håndterer operasjonsknapper
        elif char in '+-*/':
            if self.current_input:
                self.first_num = float(self.current_input)
                self.operator = char
                self.current_input = ""
                self.update_display()
        # Håndterer likhetsknappen
        elif char == '=':
            if self.first_num is not None and self.current_input:
                second_num = float(self.current_input)
                result = self.operations[self.operator].execute(self.first_num, second_num)
                self.current_input = str(result)
                self.update_display()
                self.first_num = None
                self.operator = None
        # Håndterer clear-knappen
        elif char == 'C':
            self.current_input = ""
            self.first_num = None
            self.operator = None
            self.update_display()

    def update_display(self):
        # Oppdaterer displayet med nåværende input
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_input)
    
    def get_input_function(self):
        self.function = self.func_entry.get()
        self.myderivative = self.calculate_derivative(self.function)
        # Plotter den deriverte funksjonen
        self.derivative_result.set(f"f'(x) = {self.myderivative}")
        self.plot.clear()
        x = sp.symbols('x')
        x_vals = [i for i in range(-10, 11)]
        y_vals = [self.myderivative.evalf(subs={x: i}) for i in x_vals]
        self.plot.plot(x_vals, y_vals, label=f"f'(x) = {self.myderivative}")
        self.plot.legend()
        self.plot.set_title("Derivert funksjon")
        self.plot.set_xlabel("x")
        self.plot.set_ylabel("f'(x)")
        self.canvas.draw()

    def open_derivative_calculator(self):
        # Åpner et nytt vindu for derivasjonskalkulator
        self.derivative_window = tk.Toplevel(self.root)
        self.derivative_window.title("Derivasjonskalkulator")

        # Legger til input felt for funksjon
        tk.Label(self.derivative_window, text="Funksjon:").grid(row=0, column=0)
        self.func_entry = tk.Entry(self.derivative_window, font=("Arial", 18), width=15)
        self.func_entry.grid(row=0, column=1)

        # Legger til deriver-knappen
        tk.Button(self.derivative_window, text="Deriver", padx=10, pady=10, font=("Arial", 18), command=self.get_input_function).grid(row=1, column=0, columnspan=2)

        # Resultat for derivasjon
        self.derivative_result = tk.StringVar()
        tk.Label(self.derivative_window, textvariable=self.derivative_result, font=("Arial", 18)).grid(row=2, column=0, columnspan=2)

        # Plott område for deriverte funksjonen
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.plot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.derivative_window)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2)

if __name__ == "__main__":
    myroot = tk.Tk()  # Oppretter hovedvinduet
    app = CalculatorApp(myroot)  # Oppretter en instans av kalkulatorappen
    myroot.mainloop()  # Starter hovedløkken
