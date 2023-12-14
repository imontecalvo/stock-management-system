import tkinter as tk
from tkinter import ttk
from .tab_frame import TabFrame

from view.CTkRangeSlider import *
import customtkinter

from ..constants import *
from utils.response import Response

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
        customtkinter.CTkButton(self.button_canvas, text="Guardar", fg_color="green").pack(side="left")




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

    def new_card(self):
        label = customtkinter.CTkLabel(self.scrollable_frame, text=f"Producto {self.curr_row}", fg_color="gray", corner_radius=2)
        label.grid(row=self.curr_row, column=0, sticky="nsew", padx=10, pady=10)
        self.curr_row+=1
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def on_resize(self, event):
        screen_width = self.root.winfo_width()

        # Actualizar el ancho del Frame
        self.factura_items_frame.list_frame.config(width=screen_width*0.6)
        self.factura_items_frame.pricing_frame.config(width=screen_width*0.4)

    def items_list(self):
        #Frame seccion
        self.factura_items_frame.list_frame.grid_columnconfigure(0, weight=1)
        self.factura_items_frame.list_frame.grid_rowconfigure(1, weight=1)

        #Top frame
        header = HeaderItems(self)
        header.grid(0,0)

        #Lista de items
        self.canvas = tk.Canvas(self.factura_items_frame.list_frame, bg="white")
        scrollbar = ttk.Scrollbar(self.factura_items_frame.list_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Configuración del desplazamiento de la rueda del ratón
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)  # Para sistemas Linux
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)  # Para sistemas Linux

        self.canvas.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        scrollbar.grid(row=1, column=1, sticky="nse", padx=(5,0), pady=10)
        self.curr_row=1

        #Events
        header.bind_events()
        




    def _on_mousewheel(self, event):
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

        self.cantidad = customtkinter.CTkEntry(self.frame, fg_color="white", text_color="black", corner_radius=2, width=5)
        self.cantidad.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))

        # self.codigo = customtkinter.CTkEntry(self.frame,fg_color="white", text_color="black", corner_radius=2)
        # self.codigo.grid(row=1, column=1, sticky="nsew", padx=10, pady=(0,10))

        self.codigo = EntryWithSuggestions(self.frame)
        self.codigo.grid(row=1, column=1, padx=10, pady=(0,10))

        # self.descripcion = customtkinter.CTkComboBox(self.frame, fg_color="white", text_color="black", corner_radius=2, width=250)
        # self.descripcion.grid(row=1, column=2, sticky="nsew", padx=10, pady=(0,10))
        self.descripcion = EntryWithSuggestions(self.frame, 250)
        self.descripcion.grid(row=1, column=2, padx=10, pady=(0,10))

        self.precio = customtkinter.CTkLabel(self.frame, text="", fg_color=LIGHT_GRAY, text_color="black", corner_radius=2, width=90)
        self.precio.grid(row=1, column=3, sticky="nsew", padx=10, pady=(0,10))

        self.subtotal = customtkinter.CTkLabel(self.frame, text="",fg_color=LIGHT_GRAY, text_color="black", corner_radius=2, width=90)
        self.subtotal.grid(row=1, column=4, sticky="nsew", padx=10, pady=(0,10))

        add_card = customtkinter.CTkButton(self.frame, text="Agregar", fg_color="green", width=25, command=parent.new_card)
        add_card.grid(row=1, column=6, sticky="e", padx=5, pady=(0,10))

    def grid(self, row, column):
        self.frame.grid(row=row, column=column, sticky="nsew")

    def bind_events(self):
        for f in [self.parent.frame, self.frame, self.parent.factura_items_frame.pricing_frame, self.parent.factura_data_frame, self.parent.scrollable_frame, self.parent.canvas, self.cant_label, self.codigo_label, self.desc_label, self.precio_label, self.subtotal_label]:
            f.bind("<Button-1>", self.descripcion.hide_menu)
            f.bind("<Button-3>", self.descripcion.hide_menu)

class EntryWithSuggestions:
    def __init__(self, frame, width=150):
        self.var=tk.StringVar(value="")
        self.entry = customtkinter.CTkEntry(frame, fg_color="white", text_color="black", corner_radius=2, width=width, textvariable=self.var)

        self.menu = tk.Menu(self.entry, tearoff=0)
        options=["a1","a2","a12","b23","bb45","c1"]
        for option in options:
            self.menu.add_command(label=option, command=lambda o=option: self.select_item(o))
        self.menu.config(bg =WHITE,fg='black',activebackground=BLUE,activeforeground='white')

        # Configurar eventos de clic en el Entry
        # self.entry.bind("<FocusIn>", self.show_menu)
        self.entry.bind("<Button-1>", self.show_menu)
        self.entry.bind("<FocusOut>", self.hide_menu)

        #Actualizar menu
        # self.entry.bind("<KeyRelease>", self.show_options)

    def show_options(self, *args):
        options=["a1","a2","a12","b23","bb45","c1"]

        value = self.var.get()

        if value != "":
            # Agregar opciones que coincidan con el texto actual
            for option in options:
                if option.startswith(value):
                    self.menu.add_command(label=option, command=lambda: self.select_item(option))

    # Mostrar el menú cuando se hace clic en el Entry
    def show_menu(self, event):
        self.menu.post(self.entry.winfo_rootx(), self.entry.winfo_rooty() + self.entry.winfo_height())

    # Ocultar el menú
    def hide_menu(self, event):
        self.menu.unpost()


    def select_item(self, item):
        self.var.set(item)

    def grid(self, row, column, padx, pady):
        self.entry.grid(row=row, column=column, padx=padx, pady=pady, sticky="nsew")


#Se queda con el ultimo elemento -> se reemplaza en memoria
#Cerrar menu al clickear fuera
#Chequear que ande bien la seleccion del item
        
#Actualizar dinamicamente las opciones del menu
#Autoupdate de codigo-descripcion
#Bloquear Agregar si falta algun campo o el codigo o descripcion no existen o la cant <= 0 