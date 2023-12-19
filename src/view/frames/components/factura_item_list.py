import tkinter as tk
from tkinter import ttk

class FacturaItemList(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        COLOR_BG = "white"
        self.items = []

        #Frame seccion
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        #Top frame
        header = HeaderItems(self)
        header.grid(0,0)

        #Lista de items
        self.canvas = tk.Canvas(self.factura_content_frame.list_frame, bg="violet")
        scrollbar = ttk.Scrollbar(self.factura_content_frame.list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas,bg="orange")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Configuración del desplazamiento de la rueda del ratón
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)  # Para sistemas Linux
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)  # Para sistemas Linux

        self.canvas.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        # self.canvas.grid_columnconfigure(0, weight=1)
        # self.scrollable_frame.columnconfigure(0, weight=1)
        scrollbar.grid(row=1, column=1, sticky="nse", padx=(5,0), pady=10)
        self.curr_row=1

        #Events
        header.bind_events()
