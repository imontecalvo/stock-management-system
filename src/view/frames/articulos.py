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
        
        #New item section
        frame1 = tk.Frame(self.frame)
        frame1.grid(row=0,column=0, sticky="nw")

        new_item_button = tk.Button(frame1, text="Nuevo Artículo",command=self.open_new_item_modal)
        new_item_button.grid(row=0,column=0,padx=10, pady=10)

        import_items_button = tk.Button(frame1, text="Importar desde Excel")
        import_items_button.grid(row=0,column=1,padx=10, pady=10)


        #Filter section
        filter_frame = tk.Frame(self.frame)
        filter_frame.grid(row=1,column=0,sticky="new")
        # filter_frame.columnconfigure(0, weight=1)
        filter_frame.columnconfigure(7, weight=1)


        separator = ttk.Separator(filter_frame, orient="horizontal")
        separator.grid(row=1, column=0, sticky='new',columnspan=10)

        tk.Label(filter_frame, text="Filtrar").grid(row=2, column=0, sticky='nw')
        tk.Button(filter_frame, text="Limpiar filtros").grid(row=2, column=8, sticky='ne')

        
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
        # table_frame = tk.Frame(self.frame)
        # table_frame.grid(row=2,column=0,sticky="nsew")
        # table_frame.columnconfigure(0, weight=1)
        # table_frame.grid_rowconfigure(0, weight=1)


        columns = ("Nombre", "Tipo", "Proveedor", "Stock", "Precio")
        tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        for c in columns:
            tree.heading(c,text=c)
        tree.grid(row=2,column=0, sticky='nsew',rowspan=1)

        # Table Actions
        actions_frame = tk.Frame(self.frame)
        actions_frame.grid(row=3,column=0,sticky="ew")
        actions_frame.columnconfigure(1, weight=1)
        tk.Button(actions_frame, text="Seleccionar todo").grid(row=0,column=0,padx=10, pady=10)
        tk.Button(actions_frame, text="Editar").grid(row=0,column=2,padx=10, pady=10)
        tk.Button(actions_frame, text="Eliminar").grid(row=0,column=3,padx=10, pady=10)

    def show(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.tkraise()

    def open_new_item_modal(self):
        # Crear una ventana modal personalizada
        modal = tk.Toplevel(self.root)
        modal.title("Nuevo Artículo")

        # Config
        ventana_principal_ancho = self.root.winfo_width()
        ventana_principal_alto = self.root.winfo_height()

        modal_ancho = 300
        modal_alto = 200

        x = (ventana_principal_ancho//2) - (modal_ancho//2)
        y = (ventana_principal_alto//2)-(modal_alto//2)

        modal.geometry(f"+{x}+{y}")

        # Contenido
        ttk.Frame(modal).grid(row=0, column=0, pady=5)
        fields = ["Codigo","Descripcion","Proveedor","Marca","Tipo","Stock","Precio de lista", "Punto de reposicion"] #TODO Pedir campos al modelo
        fields_value = []
        curr_row = 1
        for field in fields:
            label = ttk.Label(modal, text=field)
            label.grid(row=curr_row,column=0, padx=10, pady=5, sticky='w')
            entry = ttk.Entry(modal)
            entry.grid(row=curr_row,column=1, padx=10, pady=5, columnspan=2,sticky='ew')
            curr_row+=1

            fields_value.append(entry)
        
        ttk.Frame(modal).grid(row=curr_row, column=0, pady=5)

        # Botón para aceptar y cerrar el modal
        ttk.Button(modal, text="Cancelar",command=lambda: modal.destroy()).grid(row=curr_row+1, column=1, padx=10, pady=10, sticky='e')
        ttk.Button(modal, text="Añadir", command=lambda: self.add_articulo(fields_value, modal)).grid(row=curr_row+1, column=2, padx=10, pady=10,sticky='e')

    def add_articulo(self, fields, model):
        #TODO Reemplazar ids de proveedor, tipo y marca
        #TODO Chequear tipos de datos y Nulls

        values = {
            "codigo":fields[0].get(),
            "descripcion":fields[1].get(),
            "id_proveedor":int(fields[2].get()),
            "id_marca":int(fields[3].get()),
            "id_tipo":int(fields[4].get()),
            "precio_lista":int(fields[5].get()),
            "stock":int(fields[6].get()),
            "pto_reposicion":int(fields[7].get())
        }

        self.controller.add_articulo(values) #TODO Chequear respuesta del controller y avisar si fallo

        for field in fields:
            field.delete(0, "end")


"""
root
 L frameArticulos ->r=0
    L frame1 -> r=0
    L filter_frame -> r=1
    L table_frame -> r2
    L actions_frame -> r3
"""