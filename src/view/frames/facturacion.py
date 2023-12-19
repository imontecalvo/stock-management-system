import tkinter as tk
from tkinter import ttk
from .tab_frame import TabFrame

from view.CTkRangeSlider import *
import customtkinter

from ..constants import *

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
        customtkinter.CTkButton(self.button_canvas, text="Guardar", fg_color="green", command=lambda: print(self.items)).pack(side="left")




    def show(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.tkraise()

    def factura_data(self):
        self.factura_data_frame = tk.Frame(self.frame, bg="red")
        self.factura_data_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        customtkinter.CTkLabel(self.factura_data_frame, text=f"").grid(row=0, column=0, sticky="nsew", padx=10, pady=50)

    def factura_items(self):
        self.factura_items_frame = tk.Frame(self.frame, bg="red")
        self.factura_items_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.factura_items_frame.grid_columnconfigure(0, weight=1)
        self.factura_items_frame.grid_rowconfigure(0, weight=1)

        screen_width = self.root.winfo_width()

        self.factura_items_frame.list_frame = tk.Frame(self.factura_items_frame, bg="blue",width=screen_width*0.6)
        self.factura_items_frame.list_frame.grid(row=0, column=0, sticky="nsw")

        self.factura_items_frame.pricing_frame = tk.Frame(self.factura_items_frame, bg="green", width=screen_width*0.4)
        self.factura_items_frame.pricing_frame.grid(row=0, column=1, sticky="nse", padx=(10,0))
        
        self.items_list()

    def factura_pricing(self):
        factura_pricing_frame = tk.Frame(self.frame, bg="red")
        factura_pricing_frame.grid(row=2, column=1, sticky="nse", padx=10, pady=10)

        customtkinter.CTkLabel(factura_pricing_frame, text=f"").grid(row=0, column=0, sticky="nsew", padx=10, pady=60)

    def new_articulo_row(self, cantidad, codigo, descripcion, precio, subtotal):
        articulo = FacturaArticuloRow(self, codigo, descripcion, precio, cantidad, subtotal)
        articulo.bind(self.curr_row, 0, (10,0), 5)
        self.curr_row+=1

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

        self.items[self.curr_id]=(cantidad, codigo, descripcion, precio, subtotal)
        self.curr_id+=1


    def on_resize(self, event):
        screen_width = self.root.winfo_width()

        # Actualizar el ancho del Frame
        self.factura_items_frame.list_frame.config(width=screen_width*0.7)
        self.factura_items_frame.pricing_frame.config(width=screen_width*0.3)

    def items_list(self):
        COLOR_BG = "white"
        self.curr_id = 0
        self.items = {}

        #Frame seccion
        self.factura_items_frame.list_frame.grid_columnconfigure(0, weight=1)
        self.factura_items_frame.list_frame.grid_rowconfigure(1, weight=1)

        #Top frame
        header = HeaderItems(self)
        header.grid(0,0)

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

        self.canvas.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        # self.canvas.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.columnconfigure(0, weight=1)
        scrollbar.grid(row=1, column=1, sticky="nse", padx=(5,0), pady=10)
        self.curr_row=1

        #Events
        header.bind_events()

    def _on_mousewheel(self, event):
        if event.num == 4 and self.canvas.yview()[0]==0:
            return
        factor = 1 if event.num == 5 else -1
        self.canvas.yview_scroll(int(factor * 2), "units")


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

        customtkinter.CTkLabel(self.frame, text=cantidad, text_color="black", width=53).grid(row=0, column=0, sticky="nsew", padx=(0,10), pady=(10,10))
        customtkinter.CTkLabel(self.frame, text=codigo, text_color="black", width=150).grid(row=0, column=1, sticky="nsew", padx=10, pady=(10,10))
        customtkinter.CTkLabel(self.frame, text=descripcion, text_color="black", width=250).grid(row=0, column=2, sticky="nsew", padx=10, pady=(10,10))
        customtkinter.CTkLabel(self.frame, text=precio, text_color="black", width=90).grid(row=0, column=3, sticky="nsew", padx=10, pady=(10,10))
        customtkinter.CTkLabel(self.frame, text=subtotal, text_color="black", width=90).grid(row=0, column=4, sticky="nsew", padx=(10,0), pady=(10,10))
        customtkinter.CTkButton(self.frame, text="X", fg_color=RED, hover_color=RED_HOVER, width=30, command=self.delete).grid(row=0, column=6, sticky="ne", padx=(10,10), pady=(10,10))

    def bind(self, row, column, padx, pady):
        self.frame.grid(row=row, column=column, padx=padx, pady=pady, sticky="nsew")

    def delete(self):
        del self.parent.items[self.id]
        self.frame.destroy()
