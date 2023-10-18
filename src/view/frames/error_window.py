import tkinter as tk

class ErrorWindow():
    def __init__(self, message, root):
        error_window = tk.Toplevel(root)
        error_window.title("Error")
        error_label = tk.Label(error_window, text=message, padx=10, pady=10)
        error_label.grid(row=0, column=0)

        # Config
        ventana_principal_ancho = root.winfo_width()
        ventana_principal_alto = root.winfo_height()

        modal_ancho = 200
        modal_alto = 100

        x = (ventana_principal_ancho//2) - (modal_ancho//2)
        y = (ventana_principal_alto//2)-(modal_alto//2)

        error_window.geometry(f"+{x}+{y}")
        error_window.grab_set()