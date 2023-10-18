import tkinter as tk
from tkinter import ttk
from .tab_frame import TabFrame

from view.CTkRangeSlider import *
import customtkinter

from .articulos_filters import ArticulosFilter
from .error_window import ErrorWindow



class ArticulosTab(TabFrame):
    def update_price_range(self, value):
        self.price_filter.config(text=f"${value[0]} - ${value[1]}")

    def __init__(self, root, controller):
        super().__init__(root, controller)
        
        self.MISSING_VALUE = "Sin especificar"
        self.NUMERIC_INPUTS = ["Stock","Precio de lista", "Punto de reposicion"]

        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.columnconfigure(0, weight=1)

        self.proveedores = self.get_proveedores()
        self.marcas = self.get_marcas()
        self.tipos = self.get_tipos()
        
        #New item section
        frame1 = tk.Frame(self.frame)
        frame1.grid(row=0,column=0, sticky="nw")

        new_item_button = tk.Button(frame1, text="Nuevo Artículo",command=self.open_new_item_modal)
        new_item_button.grid(row=0,column=0,padx=10, pady=10)

        import_items_button = tk.Button(frame1, text="Importar desde Excel")
        import_items_button.grid(row=0,column=1,padx=10, pady=10)


        #Filter section
        filters = ArticulosFilter(self)

        # Table Actions
        actions_frame = tk.Frame(self.frame)
        actions_frame.grid(row=3,column=0,sticky="ew")
        actions_frame.columnconfigure(1, weight=1)
        tk.Button(actions_frame, text="Seleccionar todo").grid(row=0,column=0,padx=10, pady=10)
        # tk.Button(actions_frame, text="Editar").grid(row=0,column=2,padx=10, pady=10)
        self.delete_sel_button = tk.Button(actions_frame, text="Eliminar selección", command=self.delete_articulos,state="disabled")
        self.delete_sel_button.grid(row=0,column=3,padx=10, pady=10)

        #Menu Opciones de registro
        self.row_menu = tk.Menu(root, tearoff=0)
        self.row_menu.add_command(label="Editar", command=self.open_edit_articulo_modal)
        self.row_menu.add_command(label="Eliminar", command=self.delete_articulos)

        # Creacion de Tabla
        self.update_tree()

        # Deseleccionar elementos al hacer click fuera 
        self.frame.bind("<Button-1>", lambda event: self.remove_selection())
        frame1.bind("<Button-1>", lambda event: self.remove_selection())
        filters.filter_frame.bind("<Button-1>", lambda event: self.remove_selection())
        actions_frame.bind("<Button-1>", lambda event: self.remove_selection())
    

    def show(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.tkraise()

    
    def update_tree(self, filters={}):
        if hasattr(self, "tree") and self.tree:
            del self.tree

        columns = ("Codigo","Descripcion","Proveedor","Marca","Tipo","Stock","Precio de lista", "Punto de reposicion")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        for c in columns:
            self.tree.heading(c,text=c)
            if c == "Codigo":
                self.tree.column(c, width=100)
        self.tree.grid(row=2,column=0, sticky='nsew',rowspan=1)

        #Habilita/Deshabilita boton de Eliminar Seleccion
        self.tree.bind("<<TreeviewSelect>>", lambda event: self.update_delete_sel_button())

        #Deselecciona registros al hacer click en un espacio en blanco de la tabla
        self.tree.bind("<Button-1>", lambda event: self.remove_selection())

        # Vincular el menú contextual al TreeView y habilitar la selección al clic derecho
        self.tree.bind("<Button-3>", self.open_row_menu)

        # Vincular el menú contextual para cerrar al clic izquierdo en cualquier parte del TreeView
        # self.tree.bind("<Button-1>", lambda event: self.row_menu.unpost())
        
        r = self.controller.get_articulos(filters)
        if r.ok:
            articulos = r.content
            for a in articulos:
                proveedor = self.proveedores[a.id_proveedor] if a.id_proveedor and a.id_proveedor in self.proveedores.keys() else self.MISSING_VALUE
                marca = self.marcas[a.id_marca] if a.id_marca and a.id_marca in self.marcas.keys() else self.MISSING_VALUE
                tipo = self.tipos[a.id_tipo] if a.id_tipo and a.id_tipo in self.tipos.keys() else self.MISSING_VALUE
                data = (a.codigo, a.descripcion, proveedor, marca, tipo, a.precio_lista, a.stock, a.pto_reposicion)
                self.tree.insert('',"end",id=a.id, values=data)
        else:
            self.frame.after(100, lambda: ErrorWindow(r.content,self.root))

    def open_row_menu(self, event):
        # Obtener la fila seleccionada
        item = self.tree.identify_row(event.y)
        if item:
            # Seleccionar manualmente la fila
            self.tree.selection_set(item)

            # Mostrar el menú contextual en las coordenadas del evento
            self.row_menu.post(event.x_root, event.y_root)


    #Elimina seleccion y cierra menu en caso de estar abierto cuando se hace click en un la tabla
    def remove_selection(self):
        self.row_menu.unpost()
        self.tree.selection_remove(self.tree.selection())


    def update_delete_sel_button(self):
        state = "normal" if self.tree.selection() else "disabled"
        self.delete_sel_button.config(state=state)


    def open_new_item_modal(self):
        # Crear una ventana modal personalizada
        modal = tk.Toplevel(self.root)
        modal.title("Nuevo Artículo")

        # Config
        ventana_principal_ancho = self.root.winfo_width()
        ventana_principal_alto = self.root.winfo_height()

        modal_ancho = 300
        modal_alto = 200

        x = (ventana_principal_ancho//2) - (modal_ancho//2)
        y = (ventana_principal_alto//2)-(modal_alto//2)

        modal.geometry(f"+{x}+{y}")

        # Contenido
        ttk.Frame(modal).grid(row=0, column=0, pady=5)
        fields = ["Codigo","Descripcion","Proveedor","Marca","Tipo","Stock","Precio de lista", "Punto de reposicion"] #TODO Pedir campos al modelo
        fields_value = []
        curr_row = 1

        for idx, field in enumerate(fields):
            label = tk.Label(modal, text=field)
            label.grid(row=curr_row,column=0, padx=10, pady=5, sticky='w')
            if field in ["Proveedor","Marca","Tipo"]:
                var = tk.StringVar(modal)
                var.set(self.MISSING_VALUE)
                options = self.get_field_options(field)
                dropdown_menu = tk.OptionMenu(modal, var, *options)
                dropdown_menu.grid(row=curr_row,column=1, padx=10, pady=5, columnspan=2,sticky='ew')
                fields_value.append(var)
            else:
                entry = tk.Entry(modal)
                entry.grid(row=curr_row,column=1, padx=10, pady=5, columnspan=2,sticky='ew')
                if field in self.NUMERIC_INPUTS:
                    entry.config(validate="key", validatecommand=(self.root.validate_numeric_input, "%P"))
                fields_value.append(entry)
            curr_row+=1

        ttk.Frame(modal).grid(row=curr_row, column=0, pady=5)

        # Botón para aceptar y cerrar el modal
        ttk.Button(modal, text="Cancelar",command=lambda: modal.destroy()).grid(row=curr_row+1, column=1, padx=10, pady=10, sticky='e')
        ttk.Button(modal, text="Añadir", command=lambda: self.add_articulo(fields_value, modal)).grid(row=curr_row+1, column=2, padx=10, pady=10,sticky='e')

    def add_articulo(self, fields, model):
        #TODO Reemplazar ids de proveedor, tipo y marca
        #TODO Chequear tipos de datos y Nulls

        id_proveedor = None if fields[2].get()==self.MISSING_VALUE else self.get_id_from_value(self.proveedores, fields[2].get())
        id_marca = None if fields[3].get()==self.MISSING_VALUE else self.get_id_from_value(self.marcas, fields[3].get())
        id_tipo = None if fields[4].get()==self.MISSING_VALUE else self.get_id_from_value(self.tipos, fields[4].get())

        values = {
            "codigo":fields[0].get(),
            "descripcion":fields[1].get(),
            "id_proveedor":id_proveedor,
            "id_marca":id_marca,
            "id_tipo":id_tipo,
            "precio_lista":int(fields[5].get()),
            "stock":int(fields[6].get()),
            "pto_reposicion":int(fields[7].get())
        }

        r = self.controller.add_articulo(values) #TODO Chequear respuesta del controller y avisar si fallo
        for idx,field in enumerate(fields):
            if 2 <= idx <= 4:
                field.set(self.MISSING_VALUE)
            else:
                field.delete(0, "end")

        if r.ok:
            self.update_tree()
        else:
            ErrorWindow(r.content, self.frame)

    def delete_articulos(self):
        #TODO Mostrar advertencia y consultar confirmacion de borrado
        id_articulos = tuple(int(x) for x in self.tree.selection())
        r = self.controller.delete_articulos_by_id(id_articulos)
        if r.ok:
            self.update_tree()
        else:
            ErrorWindow(r.content, self.root)

    def open_edit_articulo_modal(self):
        articulo_id = self.tree.selection()[0]
        articulo_data = self.tree.item(articulo_id,"values")

        # Crear una ventana modal personalizada
        modal = tk.Toplevel(self.root)
        modal.title("Editar Artículo")

        # Config
        ventana_principal_ancho = self.root.winfo_width()
        ventana_principal_alto = self.root.winfo_height()

        modal_ancho = 300
        modal_alto = 200

        x = (ventana_principal_ancho//2) - (modal_ancho//2)
        y = (ventana_principal_alto//2)-(modal_alto//2)

        modal.geometry(f"+{x}+{y}")

        # Contenido
        ttk.Frame(modal).grid(row=0, column=0, pady=5)
        fields = ["Codigo","Descripcion","Proveedor","Marca","Tipo","Stock","Precio de lista", "Punto de reposicion"] #TODO Pedir campos al modelo
        fields_value = []
        curr_row = 1

        for idx, field in enumerate(fields):
            label = tk.Label(modal, text=field)
            label.grid(row=curr_row,column=0, padx=10, pady=5, sticky='w')
            if field in ["Proveedor","Marca","Tipo"]:
                var = tk.StringVar(modal)
                var.set(articulo_data[idx])
                options = self.get_field_options(field)
                dropdown_menu = tk.OptionMenu(modal, var, *options)
                dropdown_menu.grid(row=curr_row,column=1, padx=10, pady=5, columnspan=2,sticky='ew')
                fields_value.append(var)
            else:
                entry = tk.Entry(modal, textvariable=tk.StringVar(value=articulo_data[idx]))
                entry.grid(row=curr_row,column=1, padx=10, pady=5, columnspan=2,sticky='ew')
                if field in self.NUMERIC_INPUTS:
                    entry.config(validate="key", validatecommand=(self.root.validate_numeric_input, "%P"))
                fields_value.append(entry)
            curr_row+=1
        
        ttk.Frame(modal).grid(row=curr_row, column=0, pady=5)

        # Botón para aceptar y cerrar el modal
        ttk.Button(modal, text="Cancelar",command=lambda: modal.destroy()).grid(row=curr_row+1, column=1, padx=10, pady=10, sticky='e')
        ttk.Button(modal, text="Guardar", command=lambda: self.update_articulo(articulo_id,fields_value, modal)).grid(row=curr_row+1, column=2, padx=10, pady=10,sticky='e')


    def update_articulo(self, id, fields, modal):
        #TODO Reemplazar ids de proveedor, tipo y marca
        #TODO Chequear tipos de datos y Nulls
        id_proveedor = None if fields[2].get()==self.MISSING_VALUE else self.get_id_from_value(self.proveedores, fields[2].get())
        id_marca = None if fields[3].get()==self.MISSING_VALUE else self.get_id_from_value(self.marcas, fields[3].get())
        id_tipo = None if fields[4].get()==self.MISSING_VALUE else self.get_id_from_value(self.tipos, fields[4].get())

        values = {
            "id":int(id),
            "codigo":fields[0].get(),
            "descripcion":fields[1].get(),
            "id_proveedor":id_proveedor,
            "id_marca":id_marca,
            "id_tipo":id_tipo,
            "precio_lista":int(fields[5].get()),
            "stock":int(fields[6].get()),
            "pto_reposicion":int(fields[7].get())
        }

        r = self.controller.update_articulo(values) #TODO Chequear respuesta del controller y avisar si fallo
        if r.ok:
            self.update_tree()
        else:
            ErrorWindow(r.content, self.root)    
        modal.destroy()

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
    
    def get_field_options(self, field):
            if field == "Proveedor":
                return [self.MISSING_VALUE]+list(self.proveedores.values())
            elif field == "Marca":
                return [self.MISSING_VALUE]+list(self.marcas.values())
            elif field == "Tipo":
                return [self.MISSING_VALUE]+list(self.tipos.values())
            return ["error"]
    
    def get_id_from_value(self, dict, value):
        for k,v in dict.items():
            if v==value:
                return k

"""
root
 L frameArticulos ->r=0
    L frame1 -> r=0
    L filter_frame -> r=1
    L table_frame -> r2
    L actions_frame -> r3
"""

