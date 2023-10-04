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

        # Crear la barra de menús
        menubar = tk.Menu(self.root)


        articulos_tab = ArticulosTab(self.root, self.controller)
        proveedores_tab = ProveedoresTab(self.root, self.controller)
        facturacion_tab = FacturacionTab(self.root, self.controller)


        # Agregar las opciones al menú
        menubar.add_command(label="Articulos", command= articulos_tab.show)
        menubar.add_command(label="Proveedores", command=proveedores_tab.show)
        menubar.add_command(label="Facturación", command=facturacion_tab.show)

        # Configurar la barra de menús en la ventana
        self.root.config(menu=menubar)

        # Mostrar el primer frame al inicio
        articulos_tab.show()

        self.root.grid_columnconfigure(0, weight=1)

    def start(self):
        self.root.mainloop()
