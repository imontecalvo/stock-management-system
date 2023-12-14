import tkinter as tk
from tkinter import ttk
from .tab_frame import TabFrame

from view.CTkRangeSlider import *
import customtkinter

from ..constants import *
from utils.response import Response

class FacturacionTab(TabFrame):
    def __init__(self, root, controller):
        super().__init__(root, controller)

        #Configuracion de frame
        self.frame.config(bg=HEADING_COLOR)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
    
        
        #Titulo seccion
        headingLabel =  tk.Label(self.frame, text = 'Facturacion', font=HEADING_FONT,bg=HEADING_COLOR, foreground=WHITE  )
        headingLabel.grid(row = 0,column= 0,sticky="w",pady=10, padx=10)

        #Datos factura
        self.factura_data()
        self.factura_items()
        
        self.root.bind("<Configure>", self.on_resize)

        # #Botones
        self.button_canvas = tk.Canvas(self.frame, bg="white")
        self.button_canvas.grid(row=3, column=0, sticky="sew", padx=10, pady=10)
        customtkinter.CTkButton(self.button_canvas, text="Guardar", fg_color="green").pack(side="left")




    def show(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.tkraise()

    def factura_data(self):
        factura_data_frame = tk.Frame(self.frame, bg="red")
        factura_data_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        customtkinter.CTkLabel(factura_data_frame, text=f"").grid(row=0, column=0, sticky="nsew", padx=10, pady=50)

    def factura_items(self):
        self.factura_items_frame = tk.Frame(self.frame, bg="red")
        self.factura_items_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.factura_items_frame.grid_columnconfigure(0, weight=1)
        self.factura_items_frame.grid_rowconfigure(0, weight=1)

        screen_width = self.root.winfo_width()

        self.factura_items_frame.list_frame = tk.Frame(self.factura_items_frame, bg="blue",width=screen_width*0.6)
        self.factura_items_frame.list_frame.grid(row=0, column=0, sticky="nsw")
        self.items_list()

        self.factura_items_frame.pricing_frame = tk.Frame(self.factura_items_frame, bg="green", width=screen_width*0.4)
        self.factura_items_frame.pricing_frame.grid(row=0, column=1, sticky="nse", padx=(10,0))

    def factura_pricing(self):
        factura_pricing_frame = tk.Frame(self.frame, bg="red")
        factura_pricing_frame.grid(row=2, column=1, sticky="nse", padx=10, pady=10)

        customtkinter.CTkLabel(factura_pricing_frame, text=f"").grid(row=0, column=0, sticky="nsew", padx=10, pady=60)

    def new_card(self):
        label = customtkinter.CTkLabel(self.scrollable_frame, text=f"Producto {self.curr_row}", fg_color="gray", corner_radius=2)
        label.grid(row=self.curr_row, column=0, sticky="nsew", padx=10, pady=10)
        self.curr_row+=1
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def on_resize(self, event):
        screen_width = self.root.winfo_width()

        # Actualizar el ancho del Frame
        self.factura_items_frame.list_frame.config(width=screen_width*0.6)
        self.factura_items_frame.pricing_frame.config(width=screen_width*0.4)

    def items_list(self):
        #Frame seccion
        self.factura_items_frame.list_frame.grid_columnconfigure(0, weight=1)
        self.factura_items_frame.list_frame.grid_rowconfigure(1, weight=1)

        self.canvas = tk.Canvas(self.factura_items_frame.list_frame, bg="white")
        scrollbar = ttk.Scrollbar(self.factura_items_frame.list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

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
        scrollbar.grid(row=1, column=1, sticky="nse", padx=(5,0), pady=10)

        self.curr_row=1
        add_card = customtkinter.CTkButton(self.factura_items_frame.list_frame, text="Agregar", fg_color="green", command=self.new_card)
        add_card.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    def _on_mousewheel(self, event):
        factor = 1 if event.num == 5 else -1
        self.canvas.yview_scroll(int(factor * 2), "units")