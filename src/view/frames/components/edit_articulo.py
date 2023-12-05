import tkinter as tk
from tkinter import ttk

from view.CTkRangeSlider import *
import customtkinter

from ..components.input_window import InputWindow
from ...constants import *



class EditArticulo():
    def __init__(self, parent):
        self.parent=parent
        # Crear una ventana modal personalizada
        self.modal = tk.Toplevel(parent.root, bg=WHITE)
        self.hide()
        self.modal.protocol("WM_DELETE_WINDOW", self.hide)
        self.modal.title("Editar Artículo")
        
        # Contenido
        ttk.Frame(self.modal).grid(row=0, column=0, pady=10)
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
        self.cost=self.price_label(curr_row+9,"Precio de Costo")
        revenues=self.multiple_entry_input(curr_row+10,"Ganancias (%)",True)
        self.sell_price=self.price_label(curr_row+11,"Precio de Venta")

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
            field.bind("<KeyRelease>", lambda event: self.update_prices(list_price, discount, iva, revenues, self.cost, self.sell_price))

        self.fields_value=[code, description, supplier_var, brand_var, type_var, list_price, discount, iva, revenues, stock, rep_point]

        #Padding
        curr_row+=15
        # ttk.Frame(self.modal).grid(row=curr_row, column=0, pady=(10,0))

        #Error label
        self.error_label = customtkinter.CTkLabel(self.modal, text="", fg_color="transparent",text_color=RED,font=(DEFAULT_FONT,13.5))
        self.error_label.grid(row=curr_row, column=0, pady=(8,8), padx=20, columnspan=4, sticky="we")

        #Buttons
        button_frame = tk.Frame(self.modal, bg=WHITE)
        button_frame.grid(row=curr_row+1, column=2,columnspan=2)

        customtkinter.CTkButton(button_frame, text="Cancelar", command=lambda: self.hide(), corner_radius=6, font=('_',15), fg_color=RED, hover_color=RED_HOVER, border_spacing=5, width=20).grid(row=0, column=0, pady=10, sticky='e',padx=(0,10))

        customtkinter.CTkButton(button_frame, text="Guardar", command=lambda: self.send_values(), corner_radius=6, font=('_',15), border_spacing=5, width=80 ).grid(row=0, column=1, pady=10, padx=(0,10), sticky='e')


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

    #Chequea que los campos sean validos. Luego obtiene los valores de los campos, en caso de ser necesario
    #establece el valor por defecto, y los envía a la ventana de Articulos
    def send_values(self):
        if self.check_values():
            values = []
            for i in range(len(self.fields_value)):
                #Son los campos que tienen valores por defecto
                if i >= IDX_DISCOUNT:
                    if i==IDX_DISCOUNT or i==IDX_REVENUES:
                        v=[0 if x.get()=="" else x.get() for x in self.fields_value[i]]
                    else:
                        v= 0 if self.fields_value[i].get()=="" else self.fields_value[i].get()
                else:
                    v=self.fields_value[i].get()
                values.append(v)
            self.parent.update_articulo(self.current_id, values)

            self.hide()
    

    def check_values(self):
        if self.fields_value[IDX_CODE].get()=="":
            self.error_label.configure(text="ERROR: El campo 'Codigo' es obligatorio.")
            return False
        elif self.fields_value[IDX_DESCRIPTION].get()=="":
            self.error_label.configure(text="ERROR: El campo 'Descripcion' es obligatorio.")
            return False
        elif self.fields_value[IDX_LIST_PRICE].get()=="":
            self.error_label.configure(text="ERROR: El campo 'Precio de lista' es obligatorio.")
            return False
        else:
            self.error_label.configure(text="")
            return True
        
    # Config
    def config_geometry(self):
        ventana_principal_ancho = self.parent.root.winfo_width()
        ventana_principal_alto = self.parent.root.winfo_height()

        modal_ancho = 350
        modal_alto = 600
        x = (ventana_principal_ancho//2) - (modal_ancho//2)
        y = (ventana_principal_alto//2)-(modal_alto//2)
        self.geometry = (x,y)
        self.modal.geometry(f"+{x}+{y}")

    def show(self,articulo):
        self.config_geometry()
        self.current_id=articulo.id
        self.reset(articulo)
        self.modal.deiconify()

    def hide(self):
        self.modal.withdraw()

    def reset(self,articulo):
        for idx, field in enumerate(self.fields_value):
            if idx not in [IDX_SUPPLIER, IDX_BRAND, IDX_TYPE, IDX_DISCOUNT, IDX_REVENUES]:
                field.delete(0, "end")

        proveedor = self.parent.proveedores[articulo.id_proveedor] if articulo.id_proveedor else MISSING_VALUE
        marca = self.parent.marcas[articulo.id_marca] if articulo.id_marca else MISSING_VALUE
        tipo = self.parent.tipos[articulo.id_tipo] if articulo.id_tipo else MISSING_VALUE

        self.fields_value[IDX_CODE].insert(0,articulo.codigo)
        self.fields_value[IDX_DESCRIPTION].insert(0,articulo.descripcion)
        self.fields_value[IDX_SUPPLIER].set(proveedor)
        self.fields_value[IDX_BRAND].set(marca)
        self.fields_value[IDX_TYPE].set(tipo)
        self.fields_value[IDX_LIST_PRICE].insert(0,articulo.precio_lista)
        self.fields_value[IDX_IVA].insert(0,articulo.iva)
        self.fields_value[IDX_STOCK].insert(0,articulo.stock)
        self.fields_value[IDX_REP_POINT].insert(0,articulo.pto_reposicion)

        dtos=[articulo.d1, articulo.d2, articulo.d3, articulo.d4]
        for idx, field in enumerate(self.fields_value[IDX_DISCOUNT]):
            field.delete(0,"end")
            field.insert(0,dtos[idx])

        revs=[articulo.g1, articulo.g2, articulo.g3, articulo.g4]
        for idx, field in enumerate(self.fields_value[IDX_REVENUES]):
            field.delete(0,"end")
            field.insert(0,revs[idx])

        self.update_prices(self.fields_value[IDX_LIST_PRICE], self.fields_value[IDX_DISCOUNT], self.fields_value[IDX_IVA], self.fields_value[IDX_REVENUES], self.cost, self.sell_price)