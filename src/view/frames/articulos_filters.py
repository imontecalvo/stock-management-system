import tkinter as tk
from tkinter import ttk
from .tab_frame import TabFrame

from view.CTkRangeSlider import *
import customtkinter
from ..constants import *

class ArticulosFilter():
    def __init__(self, parent):

        self.parent = parent
        self.filters_dic = {} #Diccionario con los filtros actuales
        
        self.filter_frame = tk.Frame(parent.frame, bg = WHITE)
        self.filter_frame.grid(row=2,column=0,sticky="new", padx=5)
        self.filter_frame.columnconfigure(7, weight=1)


        # separator = ttk.Separator(self.filter_frame, orient="horizontal")
        # separator.grid(row=1, column=0, sticky='new',columnspan=10)

        tk.Label(self.filter_frame, text="Filtrar", font="arial 14 bold", bg=WHITE).grid(row=2, column=0, sticky='nw', padx= 5)
        # tk.Button(self.filter_frame, text="Limpiar filtros", command=self.clear_filters).grid(row=2, column=8, sticky='ne')
        customtkinter.CTkButton(self.filter_frame, text="Limpiar filtros", command=self.clear_filters, corner_radius=20, width=10 , font=(DEFAULT_FONT,14), text_color=RED, border_color=RED, border_width=1.5, fg_color="transparent", hover_color=LIGHT_GRAY).grid(row=2, column=8, sticky='ne', padx=(0,10), pady=(10,0))

        
        ##Filters
        # tk.Label(self.filter_frame, text="Descripcion", bg=parent.COLOR_BG).grid(row=3, column=0, sticky='w')
        customtkinter.CTkLabel(self.filter_frame, text="Descripcion", fg_color="transparent",text_color="black",font=(DEFAULT_FONT,13.5)).grid(row=3, column=0, sticky='w',padx= (10,0))
        # description = tk.Entry(self.filter_frame)
        description = customtkinter.CTkEntry(self.filter_frame, fg_color="white", text_color="black", font=(DEFAULT_FONT,13.5))
        description.grid(row = 3,column = 1, padx = (5,10), pady = 5,sticky='ew',columnspan=3)
        description.bind("<KeyRelease>", lambda event: self.changes_in_filters("descripcion",description.get()))
        self.filters_dic["descripcion"]=description.get()


        # #PRECIO
        # customtkinter.CTkLabel(self.filter_frame, text="Precio", fg_color="transparent",text_color="black",font=(DEFAULT_FONT,13.5)).grid(row=3, column=4, sticky='w', padx=(25,5))

        # range_slider = CTkRangeSlider(self.filter_frame, command=self.update_price_range)
        # range_slider.grid(row = 3,column=5, padx = 10, pady = 5,sticky='w')
        
        # self.price_filter = tk.Label(self.filter_frame, text="$0 - $1", bg=WHITE)
        # self.price_filter.grid(row=3, column=6, sticky='w')

        customtkinter.CTkLabel(self.filter_frame, text="Codigo", fg_color="transparent",text_color="black",font=(DEFAULT_FONT,13.5)).grid(row=3, column=4, sticky='w', padx=(25,5))
        code = customtkinter.CTkEntry(self.filter_frame, fg_color="white", text_color="black", width=220, font=(DEFAULT_FONT,13.5))
        code.grid(row = 3,column=5, padx = 10, pady = 5,sticky='w',columnspan=3)
        code.bind("<KeyRelease>", lambda event: self.changes_in_filters("codigo",code.get()))
        self.filters_dic["codigo"]=code.get()


        # tk.Label(self.filter_frame, text="Proveedor", bg=parent.COLOR_BG).grid(row=4, column=0, sticky='w')
        customtkinter.CTkLabel(self.filter_frame, text="Proveedor", fg_color="transparent",text_color="black",font=(DEFAULT_FONT,13.5)).grid(row=4, column=0, sticky='w',padx= (10,0))
        # supplier = tk.Entry(self.filter_frame)
        # supplier.grid(row = 4,column = 1, padx = 10, pady = 10,sticky='w')
        # supplier.bind("<KeyRelease>", lambda event: self.changes_in_filters("id_proveedor",supplier.get()))
        # self.filters_dic["id_proveedor"]=supplier.get()
        var_supplier = tk.StringVar(self.filter_frame)
        var_supplier.set("Todos los proveedores")
        options_supplier = ["Todos los proveedores"]+self.parent.get_field_options("Proveedor")
        # supplier = tk.OptionMenu(self.filter_frame, var_supplier, *options_supplier, command=lambda event: self.changes_in_filters("id_proveedor",self.menu_value_to_id(var_supplier.get(),self.parent.proveedores)))
        # supplier.config(width=20)
        supplier = customtkinter.CTkOptionMenu(self.filter_frame, width=220,dynamic_resizing=False, values=options_supplier,font=(DEFAULT_FONT,13.5), dropdown_font=(DEFAULT_FONT,14),variable=var_supplier,command=lambda event: self.changes_in_filters("id_proveedor",self.menu_value_to_id(var_supplier.get(),self.parent.proveedores)))
        supplier.grid(row = 4,column = 1, padx = (5,30), pady = (7,15),sticky='ew')
        self.filters_dic["id_proveedor"]=self.menu_value_to_id(var_supplier.get(),self.parent.proveedores)



        # tk.Label(self.filter_frame, text="Marca", bg=parent.COLOR_BG).grid(row=4, column=2, sticky='w')
        customtkinter.CTkLabel(self.filter_frame, text="Marca", fg_color="transparent",text_color="black",font=(DEFAULT_FONT,13.5)).grid(row=4, column=2, sticky='w')

        # brand = tk.Entry(self.filter_frame)
        # brand.grid(row = 4,column = 3, padx = 10, pady = 10,sticky='w')
        # brand.bind("<KeyRelease>", lambda event: self.changes_in_filters("id_marca",brand.get()))
        # self.filters_dic["id_marca"]=brand.get()
        var_brand = tk.StringVar(self.filter_frame)
        var_brand.set("Todas las marcas")
        options_brand = ["Todas las marcas"]+self.parent.get_field_options("Marca")
        # brand = tk.OptionMenu(self.filter_frame, var_brand, *options_brand, command=lambda event: self.changes_in_filters("id_marca",self.menu_value_to_id(var_brand.get(),self.parent.marcas)))
        # brand.config(width=20)
        brand = customtkinter.CTkOptionMenu(self.filter_frame, width=220,dynamic_resizing=False, values=options_brand,font=(DEFAULT_FONT,13.5), dropdown_font=(DEFAULT_FONT,14),variable=var_brand,command=lambda event: self.changes_in_filters("id_marca",self.menu_value_to_id(var_brand.get(),self.parent.marcas)))

        brand.grid(row = 4,column = 3, padx = 10, pady = (7,15),sticky='ew')
        self.filters_dic["id_marca"]=self.menu_value_to_id(var_brand.get(),self.parent.marcas)


        # tk.Label(self.filter_frame, text="Tipo", bg=parent.COLOR_BG).grid(row=4, column=4, sticky='w')
        customtkinter.CTkLabel(self.filter_frame, text="Tipo", fg_color="transparent",text_color="black",font=(DEFAULT_FONT,13.5)).grid(row=4, column=4, sticky='w', padx=(25,0))

        # type = tk.Entry(self.filter_frame)
        # type.grid(row = 4,column = 5, padx = 0, pady = 10,sticky='ew',columnspan=2)
        # type.bind("<KeyRelease>", lambda event: self.changes_in_filters("id_tipo",type.get()))
        # self.filters_dic["id_tipo"]=type.get()
        var_type = tk.StringVar(self.filter_frame)
        var_type.set("Todos los tipos")
        options_type = ["Todos los tipos"]+self.parent.get_field_options("Tipo")
        # type = tk.OptionMenu(self.filter_frame, var_type, *options_type, command=lambda event: self.changes_in_filters("id_tipo",self.menu_value_to_id(var_type.get(),self.parent.tipos)))
        # brand.config(width=20)

        type = customtkinter.CTkOptionMenu(self.filter_frame, width=220,dynamic_resizing=False, values=options_type,font=(DEFAULT_FONT,13.5), dropdown_font=(DEFAULT_FONT,14),variable=var_type,command=lambda event: self.changes_in_filters("id_tipo",self.menu_value_to_id(var_type.get(),self.parent.tipos)))

        type.grid(row = 4,column = 5, padx = 10, pady = (7,15),sticky='ew')
        self.filters_dic["id_tipo"]=self.menu_value_to_id(var_type.get(),self.parent.tipos)



        self.filter_entries = [description, code, var_supplier, var_brand, var_type]
        self.default_filters = self.filters_dic.copy() #Diccionario con los filtros default


    def update_price_range(self, value):
        self.price_filter.config(text=f"${value[0]} - ${value[1]}")

    def changes_in_filters(self, key, new_value):
        self.filters_dic[key]=new_value
        if key in ["codigo","descripcion"]: #Si es entry optimizo para ahorrar queries
            on_key_release(self)
        else:
            self.parent.update_tree(self.filters_dic.copy())

    def clear_filters(self):
        self.filters_dic = self.default_filters.copy()

        self.filter_entries[0].delete(0,"end")
        self.filter_entries[1].delete(0,"end")
        self.filter_entries[2].set("Todos los proveedores")
        self.filter_entries[3].set("Todas las marcas")
        self.filter_entries[4].set("Todos los tipos")

        self.parent.update_tree(self.filters_dic)


    def menu_value_to_id(self,value, dict):
        if value in ["Todos los proveedores","Todas las marcas","Todos los tipos"]:
            return ""
        if value == self.parent.MISSING_VALUE:
            return None
        return self.parent.get_id_from_value(dict,value)


def on_key_release(articulos_filter):
        if hasattr(on_key_release, "timer"):
            articulos_filter.filter_frame.after_cancel(on_key_release.timer)
        on_key_release.timer = articulos_filter.filter_frame.after(250, lambda: articulos_filter.parent.update_tree(articulos_filter.filters_dic.copy()))