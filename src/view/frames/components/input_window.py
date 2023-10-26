import tkinter as tk
from tkinter import ttk
import customtkinter
from ...constants import *

class InputWindow():
    def __init__(self, parent, label, title, command=None):
        root = parent.modal
        self.title = title
        self.parent=parent

        self.window = tk.Toplevel(root, bg=WHITE)
        self.window.title(title)
        x = int(1.05*parent.geometry[0])
        y = int(1.5*parent.geometry[1])
        self.window.geometry(f"+{x}+{y}")


        #Label
        customtkinter.CTkLabel(self.window, text=label, fg_color="transparent",text_color="black",font=(DEFAULT_FONT,13.5)).grid(row=0, column=0, pady=(20,8), padx=20)

        #Entry
        input = customtkinter.CTkEntry(self.window, fg_color="white", text_color="black", width=220, font=(DEFAULT_FONT,13.5))
        input.grid(row = 0,column=1, padx = 20, pady = (20,8),sticky='w')
       
        #Error label
        self.error_label = customtkinter.CTkLabel(self.window, text="", fg_color="transparent",text_color=RED,font=(DEFAULT_FONT,13.5))
        self.error_label.grid(row=1, column=0, pady=2, padx=20, columnspan=2, sticky="we")

        #Botones
        button_frame = customtkinter.CTkFrame(self.window, fg_color="transparent")
        button_frame.grid(row=2,column=1, sticky='e', pady=(2,5))

        customtkinter.CTkButton(button_frame, text="Cancelar", command=lambda: self.window.destroy(), corner_radius=6, font=('_',15), fg_color=RED, hover_color=RED_HOVER, border_spacing=5, width=20).grid(row=1, column=0, pady=10, sticky='e',padx=(0,10))

        customtkinter.CTkButton(button_frame, text="Añadir", command=lambda: self.confirm_action(input.get(), command), corner_radius=6, font=('_',15), border_spacing=5, width=80 ).grid(row=1, column=1, pady=10, padx=(0,10), sticky='w')

    def confirm_action(self, input, command):
        r = command(input)
        field = self.title.split(" ")[-1]
        if r.ok:
            self.parent.update_options(field, input)
            self.window.destroy()
        else:
            self.error_label.configure(text=r.content)
