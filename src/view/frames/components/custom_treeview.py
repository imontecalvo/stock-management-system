import tkinter as tk
from tkinter import ttk
from ...constants import *
from ..components.error_window import ErrorWindow

class CustomTreeView():
    def __init__(self, parent, columns, col_width=None):        
        self.parent=parent

        self.tree = ttk.Treeview(parent.frame, columns=columns, show="headings")
        self.tree.columns=columns

        for i, c in enumerate(columns):
            self.tree.heading(c,text=c)
            if col_width and col_width[i]:
                self.tree.column(c, width=col_width[i])
            else:
                self.tree.column(c)

        #Deselecciona registros al hacer click en un espacio en blanco de la tabla
        self.tree.bind("<Button-1>", lambda event: self.click_l_event())

        # Vincular el menú contextual al TreeView y habilitar la selección al clic derecho
        self.tree.bind("<Button-3>", self.open_row_menu)

        style = ttk.Style()
        style.configure("Treeview.Heading", background='light yellow')#--> color headings
        self.tree.tag_configure('colour', background=LIGHT_GRAY2)

        self.DISPLAYED_ITEMS = 40  # Cantidad de elementos visibles a la vez
        self.current_page = 0
        self.last_row=0


    #Menu Opciones de cada registro. 
    #Recibe vector 'options'. Cada elemento es una tupla (label, command)
    def add_row_menu(self, options):
        self.row_menu = tk.Menu(self.tree, tearoff=0)
        for o in options:
            self.row_menu.add_command(label=o[0], command=o[1])

        self.row_menu.config(bg =WHITE,fg='black',activebackground=BLUE,activeforeground='white')


    def grid(self, row, column, sticky=None, rowspan=0, padx=0, pady=0):
        self.tree.grid(row=row, column=column,sticky=sticky,rowspan=rowspan, padx=padx, pady=pady)

    def bind(self, event, command):
        try:
            self.tree.bind(event, command)
        except Exception as e:
            print(e)

    #Abre menu al hacer click derecho sobre un articulo en tree view
    def open_row_menu(self, event):
        # Obtener la fila seleccionada
        item = self.tree.identify_row(event.y)
        if item:
            # Seleccionar manualmente la fila
            self.tree.selection_set(item)

            # Mostrar el menú contextual en las coordenadas del evento
            self.row_menu.post(event.x_root, event.y_root)

    def click_l_event(self):
        self.remove_selection()

    #Elimina seleccion y cierra menu en caso de estar abierto cuando se hace click en un la tabla
    def remove_selection(self):
        self.row_menu.unpost()
        self.tree.selection_remove(self.tree.selection())

    def insert(self,id,data):
        try:
            if not self.last_row%2:
                self.tree.insert('',"end",id=id, values=data)
            else:
                self.tree.insert('',"end",id=id, values=data, tags=("colour"))
            self.last_row+=1
        
        except Exception as e:
            print(e)

    def selection(self):
        return self.tree.selection()
    
    def delete_content(self):
        self.last_row=0
        self.tree.delete(*self.tree.get_children())

    def height(self):
        self.tree.update()
        return self.tree.winfo_height()