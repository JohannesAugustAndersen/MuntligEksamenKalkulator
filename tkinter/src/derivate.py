import tkinter as tk  # Importerer tkinter biblioteket for GUI
from tkinter import messagebox  # Importerer messagebox for feilmeldinger
import sympy as sp  # Importerer sympy biblioteket for symbolsk matematikk

class Derivation:
    def calculate_derivative(self, function):
        # Beregner derivasjonen av funksjonen
        myfunction = function
        x = sp.symbols('x')
        try:
            parsed_function = sp.sympify(myfunction)
            derivative = sp.diff(parsed_function, x)
            return derivative
        except (sp.SympifyError, ValueError):
            messagebox.showerror("Input error", "Ugyldig funksjon. Vennligst skriv inn en gyldig funksjon.")