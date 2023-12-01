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
        modal_alto = 600

        x = (ventana_principal_ancho//2) - (modal_ancho//2)
        y = (ventana_principal_alto//2)-(modal_alto//2)
        self.geometry = (x,y)
        self.modal.after(500, lambda: self.modal.geometry(f"+{x}+{y}"))

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

        ttk.Separator(self.modal, orient="horizontal").grid(row=curr_row+5, column=0, columnspan=4, sticky="ew", pady=10)

        list_price=self.entry_input(curr_row+6,"Precio de lista",True)
        discount=self.multiple_entry_input(curr_row+7,"Descuentos (%)",True)
        iva=self.entry_input(curr_row+8,"IVA",True)
        cost=self.price_label(curr_row+9,"Precio de Costo")
        revenues=self.multiple_entry_input(curr_row+10,"Ganancias (%)",True)
        sell_price=self.price_label(curr_row+11,"Precio de Venta")

        ttk.Separator(self.modal, orient="horizontal").grid(row=curr_row+12, column=0, columnspan=4, sticky="ew", pady=10)
        
        stock=self.entry_input(curr_row+13,"Stock",True)
        rep_point=self.entry_input(curr_row+14, "Punto de reposicion",True)

        field_w_default_values = discount+revenues+[iva, stock, rep_point]
        for field in field_w_default_values:
            field.configure(placeholder_text="0")

        #Bindeos de eventos
        ##Limitar valor maximo en porcentajes
        discount[0].bind("<FocusOut>",lambda event: self.limit_value(discount[0], 100))
        discount[1].bind("<FocusOut>",lambda event: self.limit_value(discount[1], 100))
        discount[2].bind("<FocusOut>",lambda event: self.limit_value(discount[2], 100))
        discount[3].bind("<FocusOut>",lambda event: self.limit_value(discount[3], 100))
        ##Actualizar precios calculados
        for field in discount+revenues+[list_price, iva]:
            field.bind("<KeyRelease>", lambda event: self.update_prices(list_price, discount, iva, revenues, cost, sell_price))

        fields_value=[code, description, supplier_var, brand_var, type_var, list_price, discount, iva, revenues, stock, rep_point,cost,sell_price]

        #Padding
        curr_row+=15
        # ttk.Frame(self.modal).grid(row=curr_row, column=0, pady=(10,0))

        #Error label
        self.error_label = customtkinter.CTkLabel(self.modal, text="", fg_color="transparent",text_color=RED,font=(DEFAULT_FONT,13.5))
        self.error_label.grid(row=curr_row, column=0, pady=(8,8), padx=20, columnspan=4, sticky="we")

        #Buttons
        button_frame = tk.Frame(self.modal, bg=WHITE)
        button_frame.grid(row=curr_row+1, column=2,columnspan=2)

        customtkinter.CTkButton(button_frame, text="Cancelar", command=lambda: self.modal.destroy(), corner_radius=6, font=('_',15), fg_color=RED, hover_color=RED_HOVER, border_spacing=5, width=20).grid(row=0, column=0, pady=10, sticky='e',padx=(0,10))

        customtkinter.CTkButton(button_frame, text="Añadir", command=lambda: self.send_values(fields_value), corner_radius=6, font=('_',15), border_spacing=5, width=80 ).grid(row=0, column=1, pady=10, padx=(0,10), sticky='e')


    #Entry
    def entry_input(self, row, label, numeric=False):
        customtkinter.CTkLabel(self.modal, text=label, fg_color="transparent",text_color="black",font=('_',14)).grid(row=row,column=0, padx=10, pady=5, sticky='w')
        entry = customtkinter.CTkEntry(self.modal, fg_color="white", text_color="black", font=("_",13.5))
        entry.grid(row=row,column=1, padx=10, pady=7, columnspan=2,sticky='ew')
        if numeric:
            entry.configure(validate="key", validatecommand=(self.parent.root.validate_numeric_input, "%P"))
        return entry
    
    #Entry multiple (4 inputs)
    def multiple_entry_input(self, row, label, numeric=False):
        customtkinter.CTkLabel(self.modal, text=label, fg_color="transparent",text_color="black",font=('_',14)).grid(row=row,column=0, padx=10, pady=5, sticky='w')

        values_frame = customtkinter.CTkFrame(self.modal, fg_color="transparent")
        values_frame.grid(row=row, column=1, padx=10, pady=7, columnspan=2,sticky='ew')

        entries = []
        for i in range(4):
            entry = customtkinter.CTkEntry(values_frame, fg_color="white", text_color="black", font=("_",13.5),width=45)
            if i == 0:
                entry.grid(row=0, column=i, padx=(0, 10), sticky="w")
            elif i == 3:
                entry.grid(row=0, column=i, padx=(10, 0), sticky="e")
            else:
                entry.grid(row=0, column=i, padx=10)

            if numeric:
                entry.configure(validate="key", validatecommand=(self.parent.root.validate_numeric_input, "%P"))
            entries.append(entry)

        return entries

    def price_label(self, row, label):
        customtkinter.CTkLabel(self.modal, text=label, fg_color="transparent",text_color="black",font=('_',14)).grid(row=row,column=0, padx=10, pady=5, sticky='w')
        entry = customtkinter.CTkLabel(self.modal, text="N/A",fg_color="white", text_color="black", font=("_",13.5))
        entry.grid(row=row,column=1, padx=10, pady=7, columnspan=2,sticky='ew')
        return entry
    

    #Menu desplegable
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
    
    def set_default_value(self, entry, default_value):
        if entry.get() == "":
            entry.delete(0, tk.END)
            entry.insert(0, default_value)

    def limit_value(self, field, max_value):
        if field.get() != "":
            value = int(field.get())
            if value > max_value:
                field.delete(0, tk.END)
                field.insert(0, max_value)

    #Actualiza las opciones de los menus desplegables
    def update_options(self, field):
        options = self.parent.get_field_options(field)
        if field=="Proveedor":
            self.supplier.configure(values=options)
        elif field=="Marca":
            self.brand.configure(values=options)
        else:
            self.type.configure(values=options)

    def update_prices(self, list_price, discount, iva, revenues, cost, sell_price):
        list_price = list_price.get()
        if list_price != "":
            total_cost = float(list_price)
            for d in discount:
                d=d.get()
                d = 0 if d == "" else float(d)
                total_cost -= (total_cost*d/100)

            iva = iva.get()
            iva = 0 if iva=="" else float(iva)
            total_cost += (total_cost*iva/100)

            total_sell = total_cost
            for g in revenues:
                g=g.get()
                g = 0 if g == "" else float(g)
                total_sell += (total_sell*g/100)
            
            p1=tk.StringVar()
            p2=tk.StringVar()
            p1.set(f"$ {round(total_cost, 2)}")
            p2.set(f"$ {round(total_sell, 2)}")
            cost.configure(textvariable=p1, fg_color=LIGHT_YELLOW)
            sell_price.configure(textvariable=p2, fg_color=LIGHT_YELLOW)
        else:
            p=tk.StringVar()
            p.set("N/A")
            cost.configure(textvariable=p, fg_color="white")
            sell_price.configure(textvariable=p, fg_color="white")

    def send_values(self, values):
        IDX_DISCOUNT = 6
        IDX_REVENUES = 8

        if self.check_values(values):
            for i in range(IDX_DISCOUNT,len(values)-2):
                if i==IDX_DISCOUNT or i==IDX_REVENUES:
                    for value in values[i]:
                        self.set_default_value(value, 0)
                else:
                    self.set_default_value(values[i], 0)

            self.parent.add_articulo(values)
        

    def check_values(self, values):
        if values[0].get()=="":
            self.error_label.configure(text="ERROR: El campo 'Codigo' es obligatorio.")
            return False
        elif values[1].get()=="":
            self.error_label.configure(text="ERROR: El campo 'Descripcion' es obligatorio.")
            return False
        elif values[5].get()=="":
            self.error_label.configure(text="ERROR: El campo 'Precio de lista' es obligatorio.")
            return False
        elif self.parent.controller.exist_articulo_by_code(values[0].get()).content:
            self.error_label.configure(text="ERROR: Ya existe un articulo con ese codigo.")
            return False
        else:
            self.error_label.configure(text="")
            return True
            
