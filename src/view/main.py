import tkinter as tk
from tkinter import ttk
from .frames.articulos import ArticulosTab
from .frames.proveedores import ProveedoresTab
from .frames.facturacion import FacturacionTab

class View():
    def __init__(self, controller):
        self.controller=controller

        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("Aplicación con Menú y Frames")
        self.root.attributes("-zoomed", True)

        self.root.validate_numeric_input = self.root.register(self.on_validate_input)        

        # Crear la barra de menús
        menubar = tk.Menu(self.root)

        self.articulos_tab = ArticulosTab(self.root, self.controller)
        self.proveedores_tab = ProveedoresTab(self.root, self.controller)
        self.facturacion_tab = FacturacionTab(self.root, self.controller)

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