import tkinter as tk
from tkinter import ttk
from .tab_frame import TabFrame

from view.CTkRangeSlider import *
import customtkinter

class ArticulosFilter():
    def __init__(self, parent):

        self.parent = parent
        self.filters_dic = {}
        
        self.filter_frame = tk.Frame(parent.frame)
        self.filter_frame.grid(row=1,column=0,sticky="new")
        self.filter_frame.columnconfigure(7, weight=1)


        separator = ttk.Separator(self.filter_frame, orient="horizontal")
        separator.grid(row=1, column=0, sticky='new',columnspan=10)

        tk.Label(self.filter_frame, text="Filtrar").grid(row=2, column=0, sticky='nw')
        tk.Button(self.filter_frame, text="Limpiar filtros").grid(row=2, column=8, sticky='ne')

        
        ##Filters
        tk.Label(self.filter_frame, text="Descripcion").grid(row=3, column=0, sticky='w')
        description = tk.Entry(self.filter_frame)
        description.grid(row = 3,column = 1, padx = 10, pady = 10,sticky='ew',columnspan=3)
        description.bind("<KeyRelease>", lambda event: self.changes_in_filters("descripcion",description.get()))
        self.filters_dic["descripcion"]=description.get()


        tk.Label(self.filter_frame, text="Precio").grid(row=3, column=4, sticky='w')
        range_slider = CTkRangeSlider(self.filter_frame, command=self.update_price_range)
        range_slider.grid(row = 3,column=5, padx = 10, pady = 10,sticky='w')
        
        self.price_filter = tk.Label(self.filter_frame, text="$0 - $1")
        self.price_filter.grid(row=3, column=6, sticky='w')


        tk.Label(self.filter_frame, text="Proveedor").grid(row=4, column=0, sticky='w')
        supplier = tk.Entry(self.filter_frame)
        supplier.grid(row = 4,column = 1, padx = 10, pady = 10,sticky='w')
        supplier.bind("<KeyRelease>", lambda event: self.changes_in_filters("id_proveedor",supplier.get()))
        self.filters_dic["id_proveedor"]=supplier.get()
        

        tk.Label(self.filter_frame, text="Marca").grid(row=4, column=2, sticky='w')
        brand = tk.Entry(self.filter_frame)
        brand.grid(row = 4,column = 3, padx = 10, pady = 10,sticky='w')
        brand.bind("<KeyRelease>", lambda event: self.changes_in_filters("id_marca",brand.get()))
        self.filters_dic["id_marca"]=brand.get()


        tk.Label(self.filter_frame, text="Tipo").grid(row=4, column=4, sticky='w')
        type = tk.Entry(self.filter_frame)
        type.grid(row = 4,column = 5, padx = 0, pady = 10,sticky='ew',columnspan=2)
        type.bind("<KeyRelease>", lambda event: self.changes_in_filters("id_tipo",type.get()))
        self.filters_dic["id_tipo"]=type.get()


    def update_price_range(self, value):
        self.price_filter.config(text=f"${value[0]} - ${value[1]}")

    def changes_in_filters(self, key, new_value):
        #filtros = extraer filtros()
        #self.parent.update_viewtree(filtros)
        self.filters_dic[key]=new_value
        self.parent.update_tree(self.filters_dic)



        