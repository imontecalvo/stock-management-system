import tkinter as tk
from tkinter import ttk
from .tab_frame import TabFrame


class ArticulosTab(TabFrame):
    def __init__(self, root, controller):
        super().__init__(root, controller)
        label_articulos = tk.Label(self.frame, text="Contenido de Articulos", font=("Helvetica", 20))
        label_articulos.pack(expand=True, fill="both")

        self.frame.grid(row=0, column=0, sticky="nsew")