import tkinter as tk
from tkinter import ttk
from ...constants import *
from ..components.error_window import ErrorWindow

class CustomTreeView():
    def __init__(self, parent, columns, fetch_records, fetch_n_records, col_width=None, updating_tv_commands=None):
        self.fetch_records=fetch_records
        self.fetch_n_records=fetch_n_records
        self.updating_tv_commands=updating_tv_commands
        
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

        self.tree.bind("<Button-4>", lambda event: self.on_scrolling_up())
        self.tree.bind("<Button-5>", lambda event: self.on_scrolling_down())


        #Carga inicial de datos
        self.total_items = self.fetch_n_records()  # Cantidad total de elementos en tu base de datos
        self.DISPLAYED_ITEMS = 40  # Cantidad de elementos visibles a la vez
        self.OFFSET_EXTRA = 4 # Desplazamiento
        self.offset = 0
        self.global_selection=()



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
        self.update_sep = True
        self.remove_selection()

    #Elimina seleccion y cierra menu en caso de estar abierto cuando se hace click en un la tabla
    def remove_selection(self):
        self.global_selection=()
        self.row_menu.unpost()
        self.tree.selection_remove(self.tree.selection())

    def on_scrolling_up(self):
        new_value = max(0,self.offset-self.OFFSET_EXTRA)
        if new_value != self.offset:
            self.offset = new_value
            self.update_tree(keep_selection=True)
        return "break"

    def on_scrolling_down(self):
        new_value = min(self.total_items-self.DISPLAYED_ITEMS , self.offset+self.OFFSET_EXTRA)
        #Si el offset sigue siendo el mismo, no hace falta actualizar el treeview
        if new_value != self.offset:
            self.offset = new_value
            self.update_tree(keep_selection=True)

        #Si estoy visualizando los ultimos elementos, ahi si puedo scrollear, de lo contraro
        #scrollear fisicamente no desplaza el treeview, sino que recarga nuevos registros
        if self.offset+self.OFFSET_EXTRA >= self.total_items-self.DISPLAYED_ITEMS:
            self.tree.configure(yscrollcommand='')
        else:
            return "break"


    def update_tree(self, filters={}, keep_selection=False):
        if keep_selection:
            self.global_selection += self.tree.selection()

        self.tree.yview_moveto(0.0)
        self.tree.delete(*self.tree.get_children())
        
        lower = max(0, self.offset)
        greater = min(self.total_items,lower+self.DISPLAYED_ITEMS)

        r = self.fetch_records(lower, greater, filters)
        if r.ok:
            content = r.content
            for idx,item in enumerate(content):
                data = self.parent.get_data_to_insert(item)
                
                if not idx%2:
                    self.tree.insert('',"end",id=item.id, values=data)
                else:
                    self.tree.insert('',"end",id=item.id, values=data, tags=("colour"))
        else:
            self.frame.after(100, lambda: ErrorWindow(r.content,self.parent.frame))
        
        for s in self.global_selection:
            if self.tree.exists(s):
                self.tree.selection_add(s)

        if self.updating_tv_commands:
            self.updating_tv_commands()

    def selection(self):
        return self.tree.selection()