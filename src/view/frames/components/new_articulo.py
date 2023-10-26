import tkinter as tk
from tkinter import ttk

from view.CTkRangeSlider import *
import customtkinter

from ..components.input_window import InputWindow
from ...constants import *

class NewArticulo():
    def __init__(self, parent):
        self.parent=parent
        # Crear una ventana modal personalizada
        self.modal = tk.Toplevel(parent.root, bg=WHITE)
        self.modal.title("Nuevo Artículo")

        # Config
        ventana_principal_ancho = parent.root.winfo_width()
        ventana_principal_alto = parent.root.winfo_height()

        modal_ancho = 350
        modal_alto = 400

        x = (ventana_principal_ancho//2) - (modal_ancho//2)
        y = (ventana_principal_alto//2)-(modal_alto//2)
        self.geometry = (x,y)
        self.modal.geometry(f"+{x}+{y}")

        # Contenido
        ttk.Frame(self.modal).grid(row=0, column=0, pady=10)
        fields = ["Codigo","Descripcion","Proveedor","Marca","Tipo","Stock","Precio de lista", "Punto de reposicion"] #TODO Pedir campos al modelo
        fields_value = []
        curr_row = 1

        #Inputs
        code=self.entry_input(curr_row,"Codigo")
        description=self.entry_input(curr_row+1,"Descripcion")
        self.supplier, supplier_var=self.menu_input(curr_row+2,"Proveedor","Nuevo Proveedor", self.parent.add_proveedor)
        self.brand, brand_var=self.menu_input(curr_row+3,"Marca", "Nueva Marca", self.parent.add_marca)
        self.type, type_var=self.menu_input(curr_row+4,"Tipo", "Nuevo Tipo", self.parent.add_tipo)
        stock=self.entry_input(curr_row+5,"Stock",True)
        list_price=self.entry_input(curr_row+6,"Precio de lista",True)
        rep_point=self.entry_input(curr_row+7, "Punto de reposicion",True)

        fields_value=[code, description, supplier_var, brand_var, type_var, stock, list_price, rep_point]

        #Padding
        curr_row+=8
        ttk.Frame(self.modal).grid(row=curr_row, column=0, pady=10)

        #Buttons
        button_frame = tk.Frame(self.modal, bg=WHITE)
        button_frame.grid(row=curr_row+1, column=2,columnspan=2)

        customtkinter.CTkButton(button_frame, text="Cancelar", command=lambda: self.modal.destroy(), corner_radius=6, font=('_',15), fg_color=RED, hover_color=RED_HOVER, border_spacing=5, width=20).grid(row=0, column=0, pady=10, sticky='e',padx=(0,10))

        customtkinter.CTkButton(button_frame, text="Añadir", command=lambda: self.parent.add_articulo(fields_value), corner_radius=6, font=('_',15), border_spacing=5, width=80 ).grid(row=0, column=1, pady=10, padx=(0,10), sticky='e')


    def entry_input(self, row, label, numeric=False):
        customtkinter.CTkLabel(self.modal, text=label, fg_color="transparent",text_color="black",font=('_',14)).grid(row=row,column=0, padx=10, pady=5, sticky='w')
        entry = customtkinter.CTkEntry(self.modal, fg_color="white", text_color="black", font=("_",13.5))
        entry.grid(row=row,column=1, padx=10, pady=7, columnspan=2,sticky='ew')
        if numeric:
            entry.configure(validate="key", validatecommand=(self.parent.root.validate_numeric_input, "%P"))
        return entry
    
    def menu_input(self, row, label, title, command=None):
        customtkinter.CTkLabel(self.modal, text=label, fg_color="transparent",text_color="black",font=('_',14)).grid(row=row,column=0, padx=10, pady=5, sticky='w')

        var = tk.StringVar(self.modal)
        var.set(MISSING_VALUE)
        options = self.parent.get_field_options(label)
        dropdown_menu = customtkinter.CTkOptionMenu(self.modal,dynamic_resizing=False, width=220, values=options,font=('_',14), dropdown_font=(DEFAULT_FONT,14),variable=var)

        # inputwin_command=lambda: InputWindow(self.modal, label, title, command)
        customtkinter.CTkButton(self.modal, text="+", corner_radius=5, anchor="center", height=20, width=20, font=('_',13), command=lambda: InputWindow(self, "Nombre", title, command)).grid(row=row, column=3, pady=7, padx=(0,10), sticky='e')

        dropdown_menu.grid(row=row,column=1, padx=10, pady=7, columnspan=2,sticky='ew')
        return dropdown_menu, var
    

    def update_options(self, field):
        options = self.parent.get_field_options(field)

        if field=="Proveedor":
            self.supplier.configure(values=options)
        elif field=="Marca":
            self.brand.configure(values=options)
        else:
            self.type.configure(values=options)

            
