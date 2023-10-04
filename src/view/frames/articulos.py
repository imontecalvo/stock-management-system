import tkinter as tk
from tkinter import ttk
from .tab_frame import TabFrame

from view.CTkRangeSlider import *
import customtkinter



class ArticulosTab(TabFrame):
    def update_price_range(self, value):
        self.price_filter.config(text=f"${value[0]} - ${value[1]}")

    def __init__(self, root, controller):
        super().__init__(root, controller)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.columnconfigure(0, weight=1)

        # new_item_frame = tk.LabelFrame(self.frame, text="Añadir")
        # new_item_frame.grid(row = 0, column = 1,padx=15, pady=15)

        # lowerFrame = tk.Frame(self.frame , bg = 'white' ).grid(row = 0, column = 0)
        # button3 = tk.Button(lowerFrame , text = 'Button3' , font = 'candara 12' , bg = '#f7f7e8' ).grid(row = 5, column = 0,sticky = 'w', padx = 20, pady = 10)
        #tk.Button(lowerFrame, text = 'Button4').grid(row = 0, column = 1 , padx = 20, pady = 10)
        
        #New item section
        frame1 = tk.Frame(self.frame)
        frame1.grid(row=0,column=0, sticky="w")

        new_item_button = tk.Button(frame1, text="Nuevo Artículo")
        new_item_button.grid(row=0,column=0,padx=10, pady=10)

        import_items_button = tk.Button(frame1, text="Importar desde Excel")
        import_items_button.grid(row=0,column=1,padx=10, pady=10)


        #Filter section
        filter_frame = tk.Frame(self.frame)
        filter_frame.grid(row=1,column=0,sticky="ew")
        # filter_frame.columnconfigure(0, weight=1)
        filter_frame.columnconfigure(7, weight=1)


        separator = ttk.Separator(filter_frame, orient="horizontal")
        separator.grid(row=1, column=0, sticky='ew',columnspan=10)

        tk.Label(filter_frame, text="Filtrar").grid(row=2, column=0, sticky='w')
        tk.Button(filter_frame, text="Limpiar filtros").grid(row=2, column=8, sticky='e')

        
        ##Filters
        tk.Label(filter_frame, text="Descripcion").grid(row=3, column=0, sticky='w')
        description = tk.Entry(filter_frame).grid(row = 3,column = 1, padx = 10, pady = 10,sticky='ew',columnspan=3)

        tk.Label(filter_frame, text="Precio").grid(row=3, column=4, sticky='w')
        # description = tk.Entry(filter_frame).grid(row = 3,column=5, padx = 10, pady = 10,sticky='w')
        range_slider = CTkRangeSlider(filter_frame, command=self.update_price_range)
        range_slider.grid(row = 3,column=5, padx = 10, pady = 10,sticky='w')
        
        self.price_filter = tk.Label(filter_frame, text="$0 - $1")
        self.price_filter.grid(row=3, column=6, sticky='w')


        tk.Label(filter_frame, text="Proveedor").grid(row=4, column=0, sticky='w')
        supplier = tk.Entry(filter_frame).grid(row = 4,column = 1, padx = 10, pady = 10,sticky='w')
        
        tk.Label(filter_frame, text="Marca").grid(row=4, column=2, sticky='w')
        supplier = tk.Entry(filter_frame).grid(row = 4,column = 3, padx = 10, pady = 10,sticky='w')

        tk.Label(filter_frame, text="Tipo").grid(row=4, column=4, sticky='w')
        supplier = tk.Entry(filter_frame).grid(row = 4,column = 5, padx = 0, pady = 10,sticky='ew',columnspan=2)

        # Table
        columns = ("Nombre", "Tipo", "Proveedor", "Stock", "Precio")
        tree = ttk.Treeview(root, columns=columns, show="headings")