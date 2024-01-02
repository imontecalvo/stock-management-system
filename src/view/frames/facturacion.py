import tkinter as tk
from tkinter import ttk
from .tab_frame import TabFrame

from view.CTkRangeSlider import *
import customtkinter
from tkcalendar import Calendar, DateEntry
from datetime import datetime as dt

from ..constants import *

PROPORCION_ITEM_LIST = 0.8

class FacturacionTab(TabFrame):
    def __init__(self, root, controller,p,m,t):
        super().__init__(root, controller)

        #Configuracion de frame
        self.frame.config(bg=HEADING_COLOR)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        
        self.proveedores = p
        self.marcas = m
        self.tipos = t

        #Titulo seccion
        headingLabel =  tk.Label(self.frame, text = 'Facturacion', font=HEADING_FONT,bg=HEADING_COLOR, foreground=WHITE  )
        headingLabel.grid(row = 0,column= 0,sticky="w",pady=10, padx=10)

        #Datos factura
        self.factura_data()
        self.factura_items()
        
        self.root.bind("<Configure>", self.on_resize)

        # Table Actions
        self.actions_frame = tk.Frame(self.frame)
        self.actions_frame.grid(row=3,column=0,sticky="sew")
        self.actions_frame.columnconfigure(1, weight=1)
        x = tk.Button(self.actions_frame, text="Limpiar campos", command=self.reset)
        x.grid(row=0,column=0,padx=10, pady=10)
        
        self.delete_sel_button = customtkinter.CTkButton(self.actions_frame, text="Guardar factura", corner_radius=6, font=(DEFAULT_FONT,14), fg_color=RED, hover_color=RED_HOVER, border_spacing=8)
        self.delete_sel_button.grid(row=0,column=3,padx=10, pady=5)


    def show(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.tkraise()

    def factura_data(self):
        self.factura_data_frame = tk.Frame(self.frame, bg=WHITE)
        self.factura_data_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(10,5))

        customtkinter.CTkLabel(self.factura_data_frame, text="Cliente", fg_color="transparent",text_color="black",font=(DEFAULT_FONT,13.5)).grid(row=0, column=0, sticky='w', padx=(10,0))
        self.var_client = tk.StringVar(value="Seleccionar")
        options_client = ["c1","c2","c3"]
        client = customtkinter.CTkOptionMenu(self.factura_data_frame, width=220,dynamic_resizing=False, values=options_client,font=(DEFAULT_FONT,13.5), dropdown_font=(DEFAULT_FONT,14),variable=self.var_client)
        client.grid(row = 0,column = 1, padx = 10, pady = 15,sticky='ew')


        customtkinter.CTkLabel(self.factura_data_frame, text="Condición de Venta", fg_color="transparent",text_color="black",font=(DEFAULT_FONT,13.5)).grid(row=0, column=2, sticky='w', padx=(25,0))
        self.var_venta = tk.StringVar(value="Seleccionar")
        options_venta = ["A","B","X"]
        venta = customtkinter.CTkOptionMenu(self.factura_data_frame, width=220,dynamic_resizing=False, values=options_venta,font=(DEFAULT_FONT,13.5), dropdown_font=(DEFAULT_FONT,14),variable=self.var_venta)
        venta.grid(row = 0,column = 3, padx = 10, pady = 15,sticky='ew')

        curr_date = dt.today()
        self.date_value = tk.StringVar(value=f"{curr_date.day}/{curr_date.month}/{str(curr_date.year)[-2:]}")
        customtkinter.CTkLabel(self.factura_data_frame, text="Fecha", fg_color="transparent",text_color="black",font=(DEFAULT_FONT,13.5)).grid(row=0, column=4, sticky='w', padx=(25,0))

        self.calendar = DateEntry(self.factura_data_frame, locale="es_AR", date_pattern='dd/mm/yyyy', width=20, headersbackground=BLUE,headersforeground="white", font=(DEFAULT_FONT,11))
        self.calendar.grid(row = 0,column = 5, padx = 10, pady = 15,sticky='ew') 
        

    def factura_items(self):
        self.factura_items_frame = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        self.factura_items_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=(0,5))
        self.factura_items_frame.grid_columnconfigure(0, weight=1)
        self.factura_items_frame.grid_rowconfigure(0, weight=1)

        screen_width = self.root.winfo_width()

        self.factura_items_frame.list_frame = tk.Frame(self.factura_items_frame,width=screen_width*PROPORCION_ITEM_LIST)
        self.factura_items_frame.list_frame.grid(row=0, column=0, sticky="nsw")

        self.factura_items_frame.pricing_frame = tk.Frame(self.factura_items_frame, bg=WHITE, width=screen_width*(1-PROPORCION_ITEM_LIST))
        self.factura_items_frame.pricing_frame.grid(row=0, column=1, sticky="nse", padx=(5,0))
        
        self.items_list()
        self.factura_pricing()

    def factura_pricing(self):
        pricing_frame = self.factura_items_frame.pricing_frame
        pricing_frame.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(pricing_frame, text="", fg_color="transparent").grid(row=0,column=0, pady=15, sticky='w')
        
        self.subtotal_var = tk.StringVar(value="$ 0.00")
        customtkinter.CTkLabel(pricing_frame, text="Subtotal", fg_color="transparent",text_color="black",font=('_',14)).grid(row=1,column=0, padx=(20,10), pady=5, sticky='w')
        customtkinter.CTkLabel(pricing_frame, textvariable=self.subtotal_var, fg_color=LIGHT_GRAY,text_color="black",font=('_',14)).grid(row=1,column=1, padx=20, pady=15, columnspan=2,sticky='ew')

        def entry_input(row, label, numeric=False, state="normal", default_value=""):
            customtkinter.CTkLabel(pricing_frame, text=label, fg_color="transparent",text_color="black",font=('_',14)).grid(row=row,column=0, padx=(20,10), pady=5, sticky='w')
            entry = customtkinter.CTkEntry(pricing_frame, state=state, fg_color="white", text_color="black", font=("_",13.5), textvariable=tk.StringVar(value=default_value))
            entry.grid(row=row,column=1, padx=20, pady=15, columnspan=2,sticky='ew')
            if numeric:
                entry.configure(validate="key", validatecommand=(self.root.validate_numeric_input, "%P"))
            return entry

        self.iva_entry = entry_input(2, "IVA (%)", True, default_value="21")
        self.interes_entry = entry_input(3, "Interes (%)", True, default_value="0")
        self.descuento_entry = entry_input(4, "Descuento (%)", True, default_value="0")

        ttk.Separator(pricing_frame, orient="horizontal").grid(row=5, column=0, columnspan=3, sticky="ew", pady=20)
        customtkinter.CTkLabel(pricing_frame, text="TOTAL", fg_color="transparent",text_color="black",font=('_',14)).grid(row=6,column=0, padx=(20,10), pady=10, sticky='w')

        total_var = tk.StringVar(value="$ 0.00")
        customtkinter.CTkLabel(pricing_frame, textvariable=total_var, fg_color=LIGHT_GRAY,text_color="black",font=('_',14)).grid(row=6,column=1, padx=20, pady=20, columnspan=2,sticky='ew')

        def update_total(total_var, iva_entry, interes_entry, descuento_entry):
            subtotal = float(self.subtotal_var.get()[2:])
            iva = float(iva_entry.get())
            interes = float(interes_entry.get())
            descuento = float(descuento_entry.get())
            total_iva = subtotal + subtotal*(iva/100)
            total_iva_int = total_iva + total_iva*(interes/100)
            total = total_iva_int - total_iva_int*(descuento/100)
            total_var.set(f"$ {round(total,2)}")

        #Bindings de eventos
        self.subtotal_var.trace_add("write", lambda x,y,z: update_total(total_var, self.iva_entry, self.interes_entry, self.descuento_entry))
        self.iva_entry.bind("<KeyRelease>", lambda e: update_total(total_var, self.iva_entry, self.interes_entry, self.descuento_entry))
        self.interes_entry.bind("<KeyRelease>", lambda e: update_total(total_var, self.iva_entry, self.interes_entry, self.descuento_entry))
        self.descuento_entry.bind("<KeyRelease>", lambda e: update_total(total_var, self.iva_entry, self.interes_entry, self.descuento_entry))




    def new_articulo_row(self, cantidad, codigo, descripcion, precio, subtotal):
        articulo = FacturaArticuloRow(self, codigo, descripcion, precio, cantidad, subtotal)
        articulo.bind(self.curr_row, 0, (10,0), 2)
        self.curr_row+=1

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

        self.items[self.curr_id]=(cantidad, codigo, descripcion, precio, subtotal)
        self.curr_id+=1

        new_subtotal = float(self.subtotal_var.get()[2:])+float(subtotal[2:])
        self.subtotal_var.set(f"$ {round(new_subtotal,2)}")

    def remove_item(self, id, subtotal_item):
        del self.items[id]
        new_subtotal = float(self.subtotal_var.get()[2:])-float(subtotal_item[2:])
        self.subtotal_var.set(f"$ {round(new_subtotal,2)}")
        

    def on_resize(self, event):
        screen_width = self.root.winfo_width()

        # Actualizar el ancho del Frame
        self.factura_items_frame.list_frame.config(width=screen_width*PROPORCION_ITEM_LIST)
        self.factura_items_frame.pricing_frame.config(width=screen_width*(1-PROPORCION_ITEM_LIST))

    def set_filters(self, frame_row):
        frame = tk.Frame(self.factura_items_frame.list_frame, bg=WHITE)
        frame.grid(row=frame_row, column=0, sticky='ew')
        
        row=0

        pady=10
        tk.Label(frame, text="Filtrar", font="arial 14 bold", bg=WHITE).grid(row=row, column=0, sticky='nw', padx= 5, pady=pady)

        # Proveedor
        customtkinter.CTkLabel(frame, text="Proveedor", fg_color="transparent",text_color="black",font=(DEFAULT_FONT,13.5)).grid(row=row, column=1, sticky='w',padx= (10,0),pady=pady)
        self.var_supplier_filter = tk.StringVar(value="Todos los proveedores")
        options_supplier = ["Todos los proveedores"]+self.get_field_options("Proveedor")
        self.proveedores_menu = customtkinter.CTkOptionMenu(frame, width=220,dynamic_resizing=False, values=options_supplier,font=(DEFAULT_FONT,13.5), dropdown_font=(DEFAULT_FONT,14),variable=self.var_supplier_filter,fg_color=LIGHT_GRAY, button_color=GRAY1,button_hover_color=GRAY2,text_color="black")
        self.proveedores_menu.grid(row=row ,column = 2, padx = (5,30), pady=pady,sticky='ew')

        # Marca
        customtkinter.CTkLabel(frame, text="Marca", fg_color="transparent",text_color="black",font=(DEFAULT_FONT,13.5)).grid(row=row, column=3, sticky='w',padx= (10,0),pady=pady)
        self.var_brand_filter = tk.StringVar(value="Todos las marcas")
        options_brand = ["Todas las marcas"]+self.get_field_options("Marca")
        self.marcas_menu = customtkinter.CTkOptionMenu(frame, width=220,dynamic_resizing=False, values=options_brand,font=(DEFAULT_FONT,13.5), dropdown_font=(DEFAULT_FONT,14),variable=self.var_brand_filter,fg_color=LIGHT_GRAY, button_color=GRAY1,button_hover_color=GRAY2, text_color="black")
        self.marcas_menu.grid(row=row ,column = 4, padx = (5,30), pady=pady,sticky='ew')

        # Tipo
        customtkinter.CTkLabel(frame, text="Tipo", fg_color="transparent",text_color="black",font=(DEFAULT_FONT,13.5)).grid(row=row, column=5, sticky='w',padx= (10,0),pady=pady)
        self.var_type_filter = tk.StringVar(value="Todos los tipos")
        options_types = ["Todos los tipos"]+self.get_field_options("Tipo")
        self.tipos_menu = customtkinter.CTkOptionMenu(frame, width=220,dynamic_resizing=False, values=options_types,font=(DEFAULT_FONT,13.5), dropdown_font=(DEFAULT_FONT,14),variable=self.var_type_filter, fg_color=LIGHT_GRAY, button_color=GRAY1,button_hover_color=GRAY2, text_color="black")
        self.tipos_menu.grid(row=row ,column = 6, padx = (5,30), pady=pady,sticky='ew')

    def get_field_options(self, field):
            if field == "Proveedor":
                return [MISSING_VALUE]+list(self.proveedores.data.values())
            elif field == "Marca":
                return [MISSING_VALUE]+list(self.marcas.data.values())
            elif field == "Tipo":
                return [MISSING_VALUE]+list(self.tipos.data.values())
            return ["error"]


    def items_list(self):
        COLOR_BG = "white"
        self.curr_id = 0
        self.items = {}
        row = 0

        #Filter by Proveedor, Marca, Tipo
        self.set_filters(row)
        row+=1

        #Frame seccion
        self.factura_items_frame.list_frame.grid_columnconfigure(0, weight=1)
        self.factura_items_frame.list_frame.grid_rowconfigure(2, weight=1)

        #Top frame
        header = HeaderItems(self)
        header.grid(row,0)
        row+=1

        #Lista de items
        self.canvas = tk.Canvas(self.factura_items_frame.list_frame, bg=COLOR_BG)
        scrollbar = ttk.Scrollbar(self.factura_items_frame.list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas,bg=COLOR_BG)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # Crear la ventana dentro del Canvas
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Actualizar el ancho del Scrolleable Frame
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.window_id, width=self.canvas.winfo_width()))

        # Configuración del desplazamiento de la rueda del ratón
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)  # Para sistemas Linux
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)  # Para sistemas Linux

        self.canvas.grid(row=row, column=0, sticky="nsew", padx=0, pady=0)
        self.scrollable_frame.columnconfigure(0, weight=1)
        scrollbar.grid(row=row, column=1, sticky="nse")
        row+=1
        self.curr_row=1

        #Events
        header.bind_events()

    def _on_mousewheel(self, event):
        if event.num == 4 and self.canvas.yview()[0]==0:
            return
        factor = 1 if event.num == 5 else -1
        self.canvas.yview_scroll(int(factor * 2), "units")

    def reset(self):
        self.curr_id = 0
        self.items = {}
        self.curr_row=1
        self.subtotal_var.set("$ 0.00")
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.var_client.set("Seleccionar")
        self.var_venta.set("Seleccionar")
        self.calendar.set_date(dt.today())

        self.iva_entry.configure(textvariable=tk.StringVar(value="21"))
        self.interes_entry.configure(textvariable=tk.StringVar(value="0"))
        self.descuento_entry.configure(textvariable=tk.StringVar(value="0"))

        self.var_supplier_filter.set("Todos los proveedores")
        self.var_brand_filter.set("Todas las marcas")
        self.var_type_filter.set("Todos los tipos")

    #Recibe un campo (Proveedor, Marca o Tipo) y actualiza los dropdowns menus de la tab de Facturacion
    def update_options(self, field):
        if field == "Proveedor":
            self.proveedores_menu.configure(values=["Todos los proveedores"]+self.get_field_options("Proveedor"))
        elif field == "Marca":
            self.marcas_menu.configure(values=["Todas las marcas"]+self.get_field_options("Marca"))
        elif field == "Tipo":
            self.tipos_menu.configure(values=["Todos los tipos"]+self.get_field_options("Tipo"))

class HeaderItems:
    def __init__(self, parent):
        self.parent = parent

        self.frame = tk.Frame(parent.factura_items_frame.list_frame, bg="white")
        self.frame.columnconfigure(5, weight=1)
        self.cant_label = customtkinter.CTkLabel(self.frame, text=f"Cantidad", text_color="black", corner_radius=2)
        self.cant_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10,5))
        self.codigo_label = customtkinter.CTkLabel(self.frame, text=f"Codigo", text_color="black", corner_radius=2)
        self.codigo_label.grid(row=0, column=1, sticky="nsew", padx=10, pady=(10,5))
        self.desc_label = customtkinter.CTkLabel(self.frame, text=f"Descripcion", text_color="black", corner_radius=2)
        self.desc_label.grid(row=0, column=2, sticky="nsew", padx=10, pady=(10,5))
        self.precio_label = customtkinter.CTkLabel(self.frame, text=f"Precio", text_color="black", corner_radius=2)
        self.precio_label.grid(row=0, column=3, sticky="nsew", padx=10, pady=(10,5))
        self.subtotal_label = customtkinter.CTkLabel(self.frame, text=f"Subtotal", text_color="black", corner_radius=2)
        self.subtotal_label.grid(row=0, column=4, sticky="nsew", padx=10, pady=(10,5))

        self.cantidad = customtkinter.CTkEntry(self.frame, fg_color="white", text_color="black", corner_radius=2, width=5, textvariable=tk.StringVar(value="1"))
        self.cantidad.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))
        self.cantidad.configure(validate="key", validatecommand=(parent.root.validate_numeric_input, "%P"))

        self.codigo = EntryWithSuggestions(self.frame)
        self.codigo.grid(row=1, column=1, padx=10, pady=(0,10))

        self.descripcion = EntryWithSuggestions(self.frame, 250)
        self.descripcion.grid(row=1, column=2, padx=10, pady=(0,10))

        self.precio = customtkinter.CTkLabel(self.frame, text="", fg_color=LIGHT_GRAY, text_color="black", corner_radius=2, width=90)
        self.precio.grid(row=1, column=3, sticky="nsew", padx=10, pady=(0,10))

        self.subtotal = customtkinter.CTkLabel(self.frame, text="",fg_color=LIGHT_GRAY, text_color="black", corner_radius=2, width=90)
        self.subtotal.grid(row=1, column=4, sticky="nsew", padx=10, pady=(0,10))

        self.add_card = customtkinter.CTkButton(self.frame, text="Agregar", fg_color="green", width=25, command=self.send_data, state="disabled")
        self.add_card.grid(row=1, column=6, sticky="e", padx=5, pady=(0,10))
        self.add_card.articulo_field = False

    def send_data(self):
        cantidad = self.cantidad.get()
        codigo = self.codigo.get()
        descripcion = self.descripcion.get()
        precio = self.precio.cget('text')
        subtotal = self.subtotal.cget('text')
        self.parent.new_articulo_row(cantidad, codigo, descripcion, precio, subtotal)

    def grid(self, row, column):
        self.frame.grid(row=row, column=column, sticky="nsew")

    def bind_events(self):
        for f in [self.parent.frame, self.frame, self.parent.factura_items_frame.pricing_frame, self.parent.factura_data_frame, self.parent.scrollable_frame, self.parent.canvas, self.cant_label, self.codigo_label, self.desc_label, self.precio_label, self.subtotal_label]:
            f.bind("<Button-1>", self.descripcion.hide_menu)
            f.bind("<Button-3>", self.descripcion.hide_menu)
            f.bind("<Button-1>", self.codigo.hide_menu)
            f.bind("<Button-3>", self.codigo.hide_menu)

        def open_widget_menu(widget, field, linked_widget):
            self.change_suggestions(widget, field, linked_widget)
            widget.show_menu()
            linked_widget.hide_menu()

        self.codigo.entry.bind("<Button-1>", lambda e: open_widget_menu(self.codigo, "codigo", self.descripcion))
        self.descripcion.entry.bind("<Button-1>", lambda e: open_widget_menu(self.descripcion, "descripcion", self.codigo))

        self.codigo.change_in_var(lambda x,y,z: self.change_suggestions(self.codigo, "codigo", self.descripcion))
        self.descripcion.change_in_var(lambda x,y,z: self.change_suggestions(self.descripcion, "descripcion", self.codigo))

        self.cantidad.bind("<KeyRelease>", lambda e: self.update_button())

    def change_suggestions(self, widget, field, linked_widget):
        if widget.changed_by_user:
            linked_widget.changed_by_user = False
            LIMIT, OFFSET = 10, 0
            value = widget.get()
            r = self.parent.controller.get_articulos_in_range(LIMIT, OFFSET, filters={field:value}, cols=["codigo","descripcion","precio_venta"])
            if r.ok:
                options=r.content
                codigos, descripciones, precios= zip(*options) if options else [(),(),()]
                options, linked_values, precios = [list(codigos), list(descripciones),list(precios)] if field=="codigo" else [list(descripciones), list(codigos),list(precios)]
                widget.set_options(options)
                
                value = value.upper()
                options = [o.upper() for o in options]
                
                if value not in options:
                    linked_widget.var.set("")
                    linked_widget.menu.delete(0, "end")
                    self.add_card.articulo_field = False
                    self.precio.configure(text="")
                else:
                    linked_value = linked_values[options.index(value)]
                    linked_widget.var.set(linked_value)
                    self.add_card.articulo_field = True
                    self.precio.configure(text=f"$ {precios[options.index(value)]}")
                self.update_button()
        widget.changed_by_user = True

    def update_button(self):
        self.update_subtotal_articulo()
        if self.add_card.articulo_field and self.cantidad.get()!="" and int(self.cantidad.get()) > 0:
            self.add_card.configure(state="normal")
        else:
            self.add_card.configure(state="disabled")

    def update_subtotal_articulo(self):
        if self.cantidad.get()!="" and self.precio.cget('text')!="":
            self.subtotal.configure(text=f"$ {round(int(self.cantidad.get())*float(self.precio.cget('text')[2:]),2)}")
        else:
            self.subtotal.configure(text=f"")


class EntryWithSuggestions:
    def __init__(self, frame, width=150):
        self.changed_by_user = True
        self.var=tk.StringVar(value="")
        self.entry = customtkinter.CTkEntry(frame, fg_color="white", text_color="black", corner_radius=2, width=width, textvariable=self.var)

        self.menu = tk.Menu(self.entry, tearoff=0)
        self.menu.config(bg =WHITE,fg='black',activebackground=BLUE,activeforeground='white')
        self.entry.bind("<FocusOut>", self.hide_menu)

    def set_options(self, options):
        self.menu.delete(0, "end") #Limpia las opciones ya cargadas
        value = self.var.get()

        if value != "":
            for option in options:
                self.menu.add_command(label=option, command=lambda o=option: self.select_item(o))
            
    def get(self):
        return self.var.get()

    # Mostrar el menú cuando se hace clic en el Entry
    def show_menu(self, event=None):
        self.menu.post(self.entry.winfo_rootx(), self.entry.winfo_rooty() + self.entry.winfo_height())

    # Ocultar el menú
    def hide_menu(self, event=None):
        self.menu.unpost()


    def select_item(self, item):
        self.var.set(item)

    def grid(self, row, column, padx, pady):
        self.entry.grid(row=row, column=column, padx=padx, pady=pady, sticky="nsew")

    def bind(self, event, command):
        self.entry.bind(event, command)

    def change_in_var(self, command):
        self.var.trace_add("write", command)

class FacturaArticuloRow():
    def __init__(self, parent, codigo, descripcion, precio, cantidad, subtotal):

        self.frame = tk.Frame(parent.scrollable_frame, bg=WHITE)
        self.frame.columnconfigure(5, weight=1)
        self.id = parent.curr_id
        self.parent = parent

        customtkinter.CTkLabel(self.frame, text=cantidad, text_color="black", width=53).grid(row=0, column=0, sticky="nsew", padx=(0,10), pady=3)
        customtkinter.CTkLabel(self.frame, text=codigo, text_color="black", width=150).grid(row=0, column=1, sticky="nsew", padx=10, pady=3)
        customtkinter.CTkLabel(self.frame, text=descripcion, text_color="black", width=250).grid(row=0, column=2, sticky="nsew", padx=10, pady=3)
        customtkinter.CTkLabel(self.frame, text=precio, text_color="black", width=90).grid(row=0, column=3, sticky="nsew", padx=10, pady=3)
        customtkinter.CTkLabel(self.frame, text=subtotal, text_color="black", width=90).grid(row=0, column=4, sticky="nsew", padx=(10,0), pady=3)
        customtkinter.CTkButton(self.frame, text="X", fg_color=RED, hover_color=RED_HOVER, width=30, command=lambda: self.delete(subtotal)).grid(row=0, column=6, sticky="ne", padx=(10,10), pady=3)

    def bind(self, row, column, padx, pady):
        self.frame.grid(row=row, column=column, padx=padx, pady=pady, sticky="nsew")

    def delete(self, subtotal):
        self.parent.remove_item(self.id, subtotal)
        self.frame.destroy()

