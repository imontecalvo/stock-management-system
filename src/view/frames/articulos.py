import tkinter as tk
from tkinter import ttk
from .tab_frame import TabFrame

from view.CTkRangeSlider import *
import customtkinter

from .articulos_filters import ArticulosFilter
from .error_window import ErrorWindow
from .confirm_window import ConfirmWindow
from ..constants import *

class ArticulosTab(TabFrame):
    def update_price_range(self, value):
        self.price_filter.config(text=f"${value[0]} - ${value[1]}")

    def __init__(self, root, controller):
        super().__init__(root, controller)

        #Constantes
        self.MISSING_VALUE = "Sin especificar"
        self.NUMERIC_INPUTS = ["Stock","Precio de lista", "Punto de reposicion"]

        #Configuracion de frame
        self.frame.config(bg=HEADING_COLOR)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.columnconfigure(0, weight=1)

        #(ID:Nombre) de Proveedores, marcas y tipos cargados en memoria
        self.proveedores = self.get_proveedores()
        self.marcas = self.get_marcas()
        self.tipos = self.get_tipos()
        
        #Titulo seccion
        headingLabel =  tk.Label(self.frame, text = 'Articulos', font=HEADING_FONT,bg=HEADING_COLOR, foreground=WHITE  )
        headingLabel.grid(row = 0,column= 0,sticky="w",pady=10, padx=10)
        
        #New item seccion
        frame1 = tk.Frame(self.frame, bg=HEADING_COLOR)
        frame1.grid(row=1,column=0, sticky="nw")

        new_item_button = customtkinter.CTkButton(frame1, text="Nuevo Artículo",command=self.open_new_item_modal, corner_radius=6, font=(DEFAULT_FONT,14))
        new_item_button.grid(row=0,column=0,padx=10, pady=10)


        import_items_button = customtkinter.CTkButton(frame1, text="Importar desde Excel", corner_radius=6, font=(DEFAULT_FONT,14))
        import_items_button.grid(row=0,column=1,padx=10, pady=10)


        #Filter seccion
        filters = ArticulosFilter(self)

        # Table Actions
        actions_frame = tk.Frame(self.frame)
        actions_frame.grid(row=4,column=0,sticky="ew")
        actions_frame.columnconfigure(1, weight=1)
        tk.Button(actions_frame, text="Seleccionar todo").grid(row=0,column=0,padx=10, pady=10)

        self.edit_button = customtkinter.CTkButton(actions_frame, text="Editar", command=self.open_edit_articulo_modal, state="disabled", corner_radius=6, font=(DEFAULT_FONT,14), fg_color=YELLOW, hover_color=YELLOW_HOVER, border_spacing=8, width=30)
        self.edit_button.grid(row=0,column=2,padx=(0,20), pady=5)

        ask_confirmation = lambda: ConfirmWindow(self.frame, "¿Desea eliminar el/los artículo/s seleccionados?","Eliminar artículo",self.delete_articulos)
        
        self.delete_sel_button = customtkinter.CTkButton(actions_frame, text="Eliminar selección", command= ask_confirmation,state="disabled", corner_radius=6, font=(DEFAULT_FONT,14), fg_color=RED, hover_color=RED_HOVER, border_spacing=8)
        self.delete_sel_button.grid(row=0,column=3,padx=10, pady=5)

        #Menu Opciones de registro
        self.row_menu = tk.Menu(root, tearoff=0)
        self.row_menu.add_command(label="Editar", command=self.open_edit_articulo_modal)
        self.row_menu.add_command(label="Eliminar", command=ask_confirmation)

        # Creacion de Tabla
        self.generate_tree()
        self.update_tree()

        # Deseleccionar elementos al hacer click fuera 
        self.frame.bind("<Button-1>", lambda event: self.remove_selection())
        frame1.bind("<Button-1>", lambda event: self.remove_selection())
        filters.filter_frame.bind("<Button-1>", lambda event: self.remove_selection())
        actions_frame.bind("<Button-1>", lambda event: self.remove_selection())
    

    #Pone al frente el frame de Articulos y setea configuraciones de filas
    def show(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.tkraise()

    def set_separator_col(self, columns, force=False):
        if self.update_sep or force:
            total_width = 0
            for i,c in enumerate(columns):
                w=self.tree.column(c,option="width")
                total_width+=w
                self.tree.separators[i].grid(row=1, column=0, ipady=300, pady=20, sticky='w', padx=(total_width,0))

    #Genera tree view
    def generate_tree(self):
        columns = ("Codigo","Descripcion","Proveedor","Marca","Tipo","Stock","Precio de lista", "Punto de reposicion")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        self.tree.columns=columns
        self.tree.separators=[]
        self.update_sep = False

        for i, c in enumerate(columns):
            self.tree.grid_columnconfigure(i, weight=1)
            self.tree.heading(c,text=c)
            if c == "Codigo":
                self.tree.column(c, width=100)

            s = ttk.Separator(master=self.tree, orient='vertical', style='black.TSeparator', takefocus= 0)
            self.tree.separators.append(s)

        self.tree.grid(row=3,column=0, sticky='nsew',rowspan=1, padx=5, pady=5)
        self.set_separator_col(columns,True)

        #Habilita/Deshabilita boton de Eliminar Seleccion
        self.tree.bind("<<TreeviewSelect>>", lambda event: self.update_action_buttons())

        #Deselecciona registros al hacer click en un espacio en blanco de la tabla
        self.tree.bind("<Button-1>", lambda event: self.click_l_event())

        # Vincular el menú contextual al TreeView y habilitar la selección al clic derecho
        self.tree.bind("<Button-3>", self.open_row_menu)

        self.tree.bind("<ButtonRelease-1>", lambda event: self.update_separators())
        self.tree.bind("<Motion>", lambda event: self.set_separator_col(columns))

        style = ttk.Style()
        style.configure("Treeview.Heading", background='light yellow')#--> color headings
        self.tree.tag_configure('colour', background=LIGHT_GRAY2)

        self.tree.after(300, lambda: self.set_separator_col(columns,True))



    #Recibe un diccionario de filtros y actualiza tree view con articulos filtrados
    def update_tree(self, filters={}):
        self.tree.delete(*self.tree.get_children())
        r = self.controller.get_articulos(filters)
        if r.ok:
            articulos = r.content
            for idx,a in enumerate(articulos):
                proveedor = self.proveedores[a.id_proveedor] if a.id_proveedor and a.id_proveedor in self.proveedores.keys() else self.MISSING_VALUE
                marca = self.marcas[a.id_marca] if a.id_marca and a.id_marca in self.marcas.keys() else self.MISSING_VALUE
                tipo = self.tipos[a.id_tipo] if a.id_tipo and a.id_tipo in self.tipos.keys() else self.MISSING_VALUE
                data = (a.codigo, a.descripcion, proveedor, marca, tipo, a.precio_lista, a.stock, a.pto_reposicion)
                
                if not idx%2:
                    self.tree.insert('',"end",id=a.id, values=data)
                else:
                    self.tree.insert('',"end",id=a.id, values=data, tags=("colour"))
        else:
            self.frame.after(100, lambda: ErrorWindow(r.content,self.root))
        
        self.delete_sel_button.configure(state="disabled")
        self.edit_button.configure(state="disabled")
        
    #Abre menu al hacer click derecho sobre un articulo en tree view
    def open_row_menu(self, event):
        # Obtener la fila seleccionada
        item = self.tree.identify_row(event.y)
        if item:
            # Seleccionar manualmente la fila
            self.tree.selection_set(item)

            # Mostrar el menú contextual en las coordenadas del evento
            self.row_menu.post(event.x_root, event.y_root)

    def update_separators(self):
        self.update_sep = False
        self.set_separator_col(self.tree.columns, True)

    def click_l_event(self):
        self.update_sep = True
        self.remove_selection()

    #Elimina seleccion y cierra menu en caso de estar abierto cuando se hace click en un la tabla
    def remove_selection(self):
        self.row_menu.unpost()
        self.tree.selection_remove(self.tree.selection())

    #Setea estados de botones: "Editar" y "Eliminar seleccion"
    #   - Editar: habilitado si hay 1 item seleccionado, sino deshabilitado
    #   - Eliminar seleccion: habilitado si hay al menos 1 item seleccionado, sino deshabilitado
    def update_action_buttons(self):
        selection = self.tree.selection()
        state_delete = "normal" if selection else "disabled"
        state_edit = "normal" if len(selection)==1 else "disabled"
        
        self.delete_sel_button.configure(state=state_delete)
        self.edit_button.configure(state=state_edit)


    #Abre modal para agregar nuevo articulo
    def open_new_item_modal(self):
        # Crear una ventana modal personalizada
        modal = tk.Toplevel(self.root, bg=WHITE)
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
            customtkinter.CTkLabel(modal, text=field, fg_color="transparent",text_color="black",font=('_',14)).grid(row=curr_row,column=0, padx=10, pady=5, sticky='w')

            if field in ["Proveedor","Marca","Tipo"]:
                var = tk.StringVar(modal)
                var.set(self.MISSING_VALUE)
                options = self.get_field_options(field)
                dropdown_menu = customtkinter.CTkOptionMenu(modal,dynamic_resizing=False, width=220, values=options,font=('_',14), dropdown_font=(DEFAULT_FONT,14),variable=var)

                dropdown_menu.grid(row=curr_row,column=1, padx=10, pady=7, columnspan=2,sticky='ew')
                fields_value.append(var)

                customtkinter.CTkButton(modal, text="+", corner_radius=5, anchor="center", height=20, width=20, font=('_',13) ).grid(row=curr_row, column=3, pady=7, padx=(0,10), sticky='e')
            else:
                entry = customtkinter.CTkEntry(modal, fg_color="white", text_color="black", font=("_",13.5))
                entry.grid(row=curr_row,column=1, padx=10, pady=7, columnspan=2,sticky='ew')
                if field in self.NUMERIC_INPUTS:
                    entry.configure(validate="key", validatecommand=(self.root.validate_numeric_input, "%P"))
                fields_value.append(entry)
            curr_row+=1

        ttk.Frame(modal).grid(row=curr_row, column=0, pady=5)

        customtkinter.CTkButton(modal, text="Cancelar", command=lambda: modal.destroy(), corner_radius=6, font=('_',15), fg_color=RED, hover_color=RED_HOVER, border_spacing=5, width=20).grid(row=curr_row+1, column=1, pady=10, sticky='e',padx=(0,10))
        customtkinter.CTkButton(modal, text="Añadir", command=lambda: self.add_articulo(fields_value), corner_radius=6, font=('_',15), border_spacing=5, width=80 ).grid(row=curr_row+1, column=2, pady=10, padx=(0,10), sticky='e')


    #Recibe un diccionario con los valores de un articulo a agregar y lo añade a la base de datos
    #En caso de error, se muestra el mensaje en un pop up
    def add_articulo(self, fields):
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

    #Elimina los articulos seleccionados en el treeview
    def delete_articulos(self):
        #TODO Mostrar advertencia y consultar confirmacion de borrado
        id_articulos = tuple(int(x) for x in self.tree.selection())
        r = self.controller.delete_articulos_by_id(id_articulos)
        if r.ok:
            self.update_tree()
        else:
            ErrorWindow(r.content, self.root)

    #Abre modal para editar un articulo ya existente
    def open_edit_articulo_modal(self):
        articulo_id = self.tree.selection()[0]
        articulo_data = self.tree.item(articulo_id,"values")

        # Crear una ventana modal personalizada
        modal = tk.Toplevel(self.root, bg=WHITE)
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
            customtkinter.CTkLabel(modal, text=field, fg_color="transparent",text_color="black",font=('_',14)).grid(row=curr_row,column=0, padx=10, pady=5, sticky='w')

            if field in ["Proveedor","Marca","Tipo"]:
                var = tk.StringVar(modal)
                var.set(articulo_data[idx])
                options = self.get_field_options(field)
                dropdown_menu = customtkinter.CTkOptionMenu(modal,dynamic_resizing=False, width=220, values=options,font=('_',14), dropdown_font=(DEFAULT_FONT,14),variable=var)
                dropdown_menu.grid(row=curr_row,column=1, padx=10, pady=7, columnspan=2,sticky='ew')
                fields_value.append(var)
                customtkinter.CTkButton(modal, text="+", corner_radius=5, anchor="center", height=20, width=20, font=('_',13) ).grid(row=curr_row, column=3, pady=7, padx=(0,10), sticky='e')

            else:
                entry = customtkinter.CTkEntry(modal, textvariable=tk.StringVar(value=articulo_data[idx]), fg_color="white", text_color="black", font=("_",13.5))
                entry.grid(row=curr_row,column=1, padx=10, pady=7, columnspan=2,sticky='ew')
                if field in self.NUMERIC_INPUTS:
                    entry.configure(validate="key", validatecommand=(self.root.validate_numeric_input, "%P"))
                fields_value.append(entry)
            curr_row+=1
        
        ttk.Frame(modal).grid(row=curr_row, column=0, pady=5)

        # Botón para aceptar y cerrar el modal
        customtkinter.CTkButton(modal, text="Cancelar", command=lambda: modal.destroy(), corner_radius=6, font=('_',15), fg_color=RED, hover_color=RED_HOVER, border_spacing=5, width=20).grid(row=curr_row+1, column=1, pady=10, sticky='e',padx=(0,10))

        customtkinter.CTkButton(modal, text="Guardar", command=lambda: self.update_articulo(articulo_id,fields_value, modal), corner_radius=6, font=('_',15), border_spacing=5, width=80 ).grid(row=curr_row+1, column=2, pady=10, padx=(0,10), sticky='e')


    #Recibe id y campos del articulo a editar y lo edita en la base de datos, luego cierra modal
    #En caso de error, muestra el mensaje en un pop up
    def update_articulo(self, id, fields, modal):
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

        r = self.controller.update_articulo(values)
        if r.ok:
            self.update_tree()
        else:
            ErrorWindow(r.content, self.root)    
        modal.destroy()

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
    
    #Devuelve la lista de opciones de proveedores, marca o tipo para los dropdown menus
    #Concatena el valor "Sin especificar" a la lista de valores extraida de la base de datos
    def get_field_options(self, field):
            if field == "Proveedor":
                return [self.MISSING_VALUE]+list(self.proveedores.values())
            elif field == "Marca":
                return [self.MISSING_VALUE]+list(self.marcas.values())
            elif field == "Tipo":
                return [self.MISSING_VALUE]+list(self.tipos.values())
            return ["error"]
    
    #Dado un diccionario y un valor, obtiene la clave
    #Lo usamos en dropdown menus para obtener el ID a partir del nombre de Proveedores, marcas o tipos
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

