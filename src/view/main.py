import tkinter as tk
from tkinter import ttk
from .frames.articulos import ArticulosTab
from .frames.proveedores import ProveedoresTab
from .frames.facturacion import FacturacionTab
from .frames.components.error_window import ErrorWindow
from .constants import *

class View():
    def __init__(self, controller):
        self.controller=controller

        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("Aplicación con Menú y Frames")
        self.root.attributes("-zoomed", True)

        self.root.validate_numeric_input = self.root.register(self.on_validate_input)        

        #Data in memory
        p=SharedData("Proveedor",self.get_proveedores(),self)
        m=SharedData("Marca",self.get_marcas(),self)
        t=SharedData("Tipo",self.get_tipos(),self)

        # Crear la barra de menús
        menubar = tk.Menu(self.root)

        self.articulos_tab = ArticulosTab(self.root, self.controller, p,m,t)
        self.proveedores_tab = ProveedoresTab(self.root, self.controller)
        self.facturacion_tab = FacturacionTab(self.root, self.controller, p,m,t)

        # Agregar las opciones al menú
        menubar.add_command(label="Articulos", command=self.show_articulos)
        menubar.add_command(label="Proveedores", command=self.show_proveedores)
        menubar.add_command(label="Facturación", command=self.show_facturacion)


        # Configurar la barra de menús en la ventana
        self.root.config(menu=menubar)

        # Mostrar el primer frame al inicio
        self.show_articulos()

        self.root.grid_columnconfigure(0, weight=1)

    def start(self):
        self.root.mainloop()

    def show_articulos(self):
        # self.articulos_tab = ArticulosTab(self.root, self.controller)
        self.articulos_tab.show()
        # if hasattr(self, "proveedores_tab"):
        #     del self.proveedores_tab
        # if hasattr(self, "facturacion_tab"):
        #     del self.facturacion_tab

    def show_proveedores(self):
        # self.proveedores_tab = ProveedoresTab(self.root, self.controller)
        self.proveedores_tab.show()
        # if hasattr(self, "articulos_tab"):
        #     del self.articulos_tab
        # if hasattr(self, "facturacion_tab"):
        #     del self.facturacion_tab

    def show_facturacion(self):
        # self.facturacion_tab = FacturacionTab(self.root, self.controller)
        self.facturacion_tab.show()
        # if hasattr(self, "articulos_tab"):
        #     del self.articulos_tab
        # if hasattr(self, "proveedores_tab"):
        #     del self.proveedores_tab
        

    def is_numeric_input(self, P):
        try:
            float(P)
            return True
        except ValueError:
            return False

    def on_validate_input(self, P):
        if self.is_numeric_input(P) or P == "":
            return True
        return False
    
    #Obtiene la lista de proveedores de la base de datos
    def get_proveedores(self):
        proveedores_dic = {}
        
        r = self.controller.get_proveedores()
        if r.ok:
            proveedores=r.content
            for p in proveedores:
                proveedores_dic[p.id]=p.nombre
        else:
            self.frame.after(500, lambda: ErrorWindow(r.content,self.frame))
        return proveedores_dic
    
    #Obtiene la lista de marcas de la base de datos
    def get_marcas(self):
        marcas_dic = {}
        r = self.controller.get_marcas()
        if r.ok:
            marcas = r.content
            for m in marcas:
                marcas_dic[m.id]=m.nombre
        else:
            self.frame.after(500, lambda: ErrorWindow(r.content,self.frame))
        return marcas_dic
    
    #Obtiene la lista de tipos de la base de datos
    def get_tipos(self):
        tipos_dic = {}
        r = self.controller.get_tipos()
        if r.ok:
            tipos = r.content
            for t in tipos:
                tipos_dic[t.id]=t.nombre
        else:
            self.frame.after(500, lambda: ErrorWindow(r.content,self.frame))
        return tipos_dic
    
    #Recibe un campo (Proveedor, Marca o Tipo) y actualiza las opciones de los dropdowns menus en todos los tabs
    def update_options_in_all_tabs(self, field):
        self.articulos_tab.update_options(field)
        self.facturacion_tab.update_options(field)


class SharedData():
    def __init__(self,field,data,parent):
        self.field = field
        self.data = data
        self.parent = parent

    def add(self, id, value):
        self.data[id]=value
        self.parent.update_options_in_all_tabs(self.field)

    def contains(self, key):
        return key in self.data.keys()
    
    #Dado un diccionario y un valor, obtiene la clave
    #Lo usamos en dropdown menus para obtener el ID a partir del nombre de Proveedores, marcas o tipos
    def get_id_from_value(self, value):
        no_filters = NO_FILT_PROVEEDOR if self.field == "Proveedor" else NO_FILT_MARCA if self.field == "Marca" else NO_FILT_TIPO 
        if value == no_filters:
            return ""
        if value == MISSING_VALUE:
            return None
        
        for k,v in self.data.items():
            if v == value:
                return k
        return None
