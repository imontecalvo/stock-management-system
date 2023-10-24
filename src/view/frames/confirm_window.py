import tkinter as tk
from tkinter import ttk
import customtkinter
from ..constants import *

class ConfirmWindow():
    def __init__(self, root, message, title, command=None):
        self.window = tk.Toplevel(root, bg=WHITE)
        self.window.title(title)

        customtkinter.CTkLabel(self.window, text=message, fg_color="transparent",text_color="black",font=(DEFAULT_FONT,13.5)).grid(row=0, column=0, pady=10, padx=20)

        # Config
        ventana_principal_ancho = root.winfo_width()
        ventana_principal_alto = root.winfo_height()

        modal_ancho = 200
        modal_alto = 100

        x = (ventana_principal_ancho//2) - (modal_ancho//2)
        y = (ventana_principal_alto//2)-(modal_alto//2)

        self.window.geometry(f"+{x}+{y}")

        button_frame = customtkinter.CTkFrame(self.window, fg_color="transparent")
        button_frame.grid(row=1,column=0, sticky='e', pady=(5,5))

        customtkinter.CTkButton(button_frame, text="Cancelar", command=lambda: self.window.destroy(), corner_radius=6, font=('_',15), fg_color=RED, hover_color=RED_HOVER, border_spacing=5, width=20).grid(row=1, column=0, pady=10, sticky='e',padx=(0,10))

        customtkinter.CTkButton(button_frame, text="Confirmar", command=lambda: self.confirm_action(command), corner_radius=6, font=('_',15), border_spacing=5, width=80 ).grid(row=1, column=1, pady=10, padx=(0,10), sticky='w')

    def confirm_action(self, command):
        command()
        self.window.destroy()
