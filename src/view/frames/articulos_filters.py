import tkinter as tk
from tkinter import ttk
from .tab_frame import TabFrame

from view.CTkRangeSlider import *
import customtkinter

class ArticulosFilter():
    def __init__(self, parent):

        self.parent = parent
        self.filters_dic = {} #Diccionario con los filtros actuales
        
        self.filter_frame = tk.Frame(parent.frame)
        self.filter_frame.grid(row=1,column=0,sticky="new")
        self.filter_frame.columnconfigure(7, weight=1)


        separator = ttk.Separator(self.filter_frame, orient="horizontal")
        separator.grid(row=1, column=0, sticky='new',columnspan=10)

        tk.Label(self.filter_frame, text="Filtrar").grid(row=2, column=0, sticky='nw')
        tk.Button(self.filter_frame, text="Limpiar filtros", command=self.clear_filters).grid(row=2, column=8, sticky='ne')

        
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
        # supplier = tk.Entry(self.filter_frame)
        # supplier.grid(row = 4,column = 1, padx = 10, pady = 10,sticky='w')
        # supplier.bind("<KeyRelease>", lambda event: self.changes_in_filters("id_proveedor",supplier.get()))
        # self.filters_dic["id_proveedor"]=supplier.get()
        var_supplier = tk.StringVar(self.filter_frame)
        var_supplier.set("Todos los proveedores")
        options = ["Todos los proveedores"]+self.parent.get_field_options("Proveedor")
        supplier = tk.OptionMenu(self.filter_frame, var_supplier, *options, command=lambda event: self.changes_in_filters("id_proveedor",self.menu_value_to_id(var_supplier.get(),self.parent.proveedores)))
        supplier.config(width=20)
        supplier.grid(row = 4,column = 1, padx = 10, pady = 10,sticky='ew')
        self.filters_dic["id_proveedor"]=self.menu_value_to_id(var_supplier.get(),self.parent.proveedores)

        

        tk.Label(self.filter_frame, text="Marca").grid(row=4, column=2, sticky='w')
        # brand = tk.Entry(self.filter_frame)
        # brand.grid(row = 4,column = 3, padx = 10, pady = 10,sticky='w')
        # brand.bind("<KeyRelease>", lambda event: self.changes_in_filters("id_marca",brand.get()))
        # self.filters_dic["id_marca"]=brand.get()
        var_brand = tk.StringVar(self.filter_frame)
        var_brand.set("Todas las marcas")
        options = ["Todas las marcas"]+self.parent.get_field_options("Marca")
        brand = tk.OptionMenu(self.filter_frame, var_brand, *options, command=lambda event: self.changes_in_filters("id_marca",self.menu_value_to_id(var_brand.get(),self.parent.marcas)))
        brand.config(width=20)
        brand.grid(row = 4,column = 3, padx = 10, pady = 10,sticky='ew')
        self.filters_dic["id_marca"]=self.menu_value_to_id(var_brand.get(),self.parent.marcas)


        tk.Label(self.filter_frame, text="Tipo").grid(row=4, column=4, sticky='w')
        # type = tk.Entry(self.filter_frame)
        # type.grid(row = 4,column = 5, padx = 0, pady = 10,sticky='ew',columnspan=2)
        # type.bind("<KeyRelease>", lambda event: self.changes_in_filters("id_tipo",type.get()))
        # self.filters_dic["id_tipo"]=type.get()
        var_type = tk.StringVar(self.filter_frame)
        var_type.set("Todos los tipos")
        options = ["Todos los tipos"]+self.parent.get_field_options("Tipo")
        type = tk.OptionMenu(self.filter_frame, var_type, *options, command=lambda event: self.changes_in_filters("id_tipo",self.menu_value_to_id(var_type.get(),self.parent.tipos)))
        # brand.config(width=20)
        type.grid(row = 4,column = 5, padx = 10, pady = 10,sticky='ew',columnspan=2)
        self.filters_dic["id_tipo"]=self.menu_value_to_id(var_type.get(),self.parent.tipos)



        self.filter_entries = [description, var_supplier, var_brand, var_type]
        self.default_filters = self.filters_dic.copy() #Diccionario con los filtros default



    def update_price_range(self, value):
        self.price_filter.config(text=f"${value[0]} - ${value[1]}")

    def changes_in_filters(self, key, new_value):
        self.filters_dic[key]=new_value
        self.parent.update_tree(self.filters_dic.copy())

    def clear_filters(self):
        self.filters_dic = self.default_filters.copy()

        self.filter_entries[0].delete(0,"end")
        self.filter_entries[1].set("Todos los proveedores")
        self.filter_entries[2].set("Todas las marcas")
        self.filter_entries[3].set("Todos los tipos")
        
        self.parent.update_tree(self.filters_dic)

    def menu_value_to_id(self,value, dict):
        if value in ["Todos los proveedores","Todas las marcas","Todos los tipos"]:
            return ""
        if value == self.parent.MISSING_VALUE:
            return None
        return self.parent.get_id_from_value(dict,value)



        