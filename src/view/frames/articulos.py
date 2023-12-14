import tkinter as tk
from tkinter import ttk
from .tab_frame import TabFrame

from view.CTkRangeSlider import *
import customtkinter

from .components.articulos_filters import ArticulosFilter
from .components.error_window import ErrorWindow
from .components.confirm_window import ConfirmWindow
from .components.input_window import InputWindow
from .components.new_articulo import NewArticulo
from .components.edit_articulo import EditArticulo
from .components.pagination_bar import PaginationBar
from .components.custom_treeview import CustomTreeView
from ..constants import *
from utils.response import Response

class ArticulosTab(TabFrame):
    def update_price_range(self, value):
        self.price_filter.config(text=f"${value[0]} - ${value[1]}")

    def __init__(self, root, controller):
        super().__init__(root, controller)

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

        self.new_articulo_modal = NewArticulo(self)
        self.edit_articulo_modal = EditArticulo(self)

        new_item_button = customtkinter.CTkButton(frame1, text="Nuevo Artículo",command=self.new_articulo_modal.show, corner_radius=6, font=(DEFAULT_FONT,14))
        new_item_button.grid(row=0,column=0,padx=10, pady=10)


        import_items_button = customtkinter.CTkButton(frame1, text="Importar desde Excel", corner_radius=6, font=(DEFAULT_FONT,14))
        import_items_button.grid(row=0,column=1,padx=10, pady=10)

        self.ask_confirmation = lambda: ConfirmWindow(self.frame, "¿Desea eliminar el/los artículo/s seleccionados?","Eliminar artículo",self.delete_articulos)

        #Filter seccion
        self.filters = ArticulosFilter(self)

        # Table Actions
        self.actions_frame = tk.Frame(self.frame)
        self.actions_frame.grid(row=4,column=0,sticky="ew")
        self.actions_frame.columnconfigure(1, weight=1)
        x = tk.Button(self.actions_frame, text="Seleccionar todo", command=lambda: print(self.tree.height()))
        x.grid(row=0,column=0,padx=10, pady=10)

        self.edit_button = customtkinter.CTkButton(self.actions_frame, text="Editar", command=self.open_edit_articulo_modal, state="disabled", corner_radius=6, font=(DEFAULT_FONT,14), fg_color=YELLOW, hover_color=YELLOW_HOVER, border_spacing=8, width=30)
        self.edit_button.grid(row=0,column=2,padx=(0,20), pady=5)

        # self.ask_confirmation = lambda: ConfirmWindow(self.frame, "¿Desea eliminar el/los artículo/s seleccionados?","Eliminar artículo",self.delete_articulos)
        
        self.delete_sel_button = customtkinter.CTkButton(self.actions_frame, text="Eliminar selección", command= self.ask_confirmation,state="disabled", corner_radius=6, font=(DEFAULT_FONT,14), fg_color=RED, hover_color=RED_HOVER, border_spacing=8)
        self.delete_sel_button.grid(row=0,column=3,padx=10, pady=5)

    
        # Creacion de Tabla
        self.tree = self.create_tree()
        self.page_bar = PaginationBar(self.actions_frame ,self.update_tree, self.number_of_records,self.tree)
        self.frame.after(500, lambda: self.initialize_page_bar())
        

        # Deseleccionar elementos al hacer click fuera 
        self.frame.bind("<Button-1>", lambda event: self.tree.remove_selection())
        frame1.bind("<Button-1>", lambda event: self.tree.remove_selection())
        self.filters.filter_frame.bind("<Button-1>", lambda event: self.tree.remove_selection())
        self.actions_frame.bind("<Button-1>", lambda event: self.tree.remove_selection())



    

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

    def get_data_to_insert(self,a):
        proveedor = self.proveedores[a.id_proveedor] if a.id_proveedor and a.id_proveedor in self.proveedores.keys() else MISSING_VALUE
        marca = self.marcas[a.id_marca] if a.id_marca and a.id_marca in self.marcas.keys() else MISSING_VALUE
        tipo = self.tipos[a.id_tipo] if a.id_tipo and a.id_tipo in self.tipos.keys() else MISSING_VALUE
        return (a.id, a.descripcion, proveedor, marca, tipo, a.precio_lista, a.stock, a.pto_reposicion)
    
    def initialize_page_bar(self):
        self.page_bar.initialize()
        self.page_bar.update(0)

    def create_tree(self):
        columns = ("Codigo","Descripcion","Proveedor","Marca","Tipo","Precio Costo","Precio Venta")
        col_width = [100,None,None,None,None,None,None]

        tree = CustomTreeView(self, columns, col_width)
        tree.grid(row=3, column=0,sticky='nsew',rowspan=1, padx=5, pady=5)
        tree.add_row_menu([("Editar",self.open_edit_articulo_modal),("Eliminar",self.ask_confirmation)])

        #Habilita/Deshabilita boton de Eliminar Seleccion
        tree.bind("<<TreeviewSelect>>", lambda event: self.update_action_buttons())
        return tree

    #Recibe un diccionario de filtros y actualiza tree view con articulos filtrados
    def update_tree(self):
        filters = self.filters.get_values()
        limit, offset = self.page_bar.get_limit_offset()
        
        self.tree.delete_content()
        r = self.controller.get_articulos_in_range(limit, offset, filters)
        if r.ok:
            articulos = r.content
            for a in articulos:
                proveedor = self.proveedores[a.id_proveedor] if a.id_proveedor and a.id_proveedor in self.proveedores.keys() else MISSING_VALUE
                marca = self.marcas[a.id_marca] if a.id_marca and a.id_marca in self.marcas.keys() else MISSING_VALUE
                tipo = self.tipos[a.id_tipo] if a.id_tipo and a.id_tipo in self.tipos.keys() else MISSING_VALUE
                data = (a.codigo, a.descripcion, proveedor, marca, tipo, a.precio_costo, a.precio_venta)
                self.tree.insert(a.id, data)
        else:
            self.frame.after(100, lambda: ErrorWindow(r.content,self.root))
        
        self.delete_sel_button.configure(state="disabled")
        self.edit_button.configure(state="disabled")

    #Setea estados de botones: "Editar" y "Eliminar seleccion"
    #   - Editar: habilitado si hay 1 item seleccionado, sino deshabilitado
    #   - Eliminar seleccion: habilitado si hay al menos 1 item seleccionado, sino deshabilitado
    def update_action_buttons(self):
        selection = self.tree.selection()
        state_delete = "normal" if selection else "disabled"
        state_edit = "normal" if len(selection)==1 else "disabled"
        
        self.delete_sel_button.configure(state=state_delete)
        self.edit_button.configure(state=state_edit)

    def number_of_records(self):
        filters = self.filters.get_values()
        r = self.controller.get_no_articulos(filters)
        if r.ok:
            return r.content
        else:
            self.frame.after(100, lambda: ErrorWindow(r.content,self.root))
            return 0

    def new_filters(self):
        self.page_bar.update(JUMP_2_FIRST_PAGE)

    #Recibe un diccionario con los valores de un articulo a agregar y lo añade a la base de datos
    #En caso de error, se muestra el mensaje en un pop up
    def add_articulo(self, fields):
        id_proveedor = None if fields[2]==MISSING_VALUE else self.get_id_from_value(self.proveedores, fields[2])
        id_marca = None if fields[3]==MISSING_VALUE else self.get_id_from_value(self.marcas, fields[3])
        id_tipo = None if fields[4]==MISSING_VALUE else self.get_id_from_value(self.tipos, fields[4])

        values = {
            "codigo":fields[0],
            "descripcion":fields[1],
            "id_proveedor":id_proveedor,
            "id_marca":id_marca,
            "id_tipo":id_tipo,
            "precio_lista":int(fields[5]),
            "d1":int(fields[6][0]),
            "d2":int(fields[6][1]),
            "d3":int(fields[6][2]),
            "d4":int(fields[6][3]),
            "iva":int(fields[7]),
            "g1":int(fields[8][0]),
            "g2":int(fields[8][1]),
            "g3":int(fields[8][2]),
            "g4":int(fields[8][3]),
            "stock":int(fields[9]),
            "pto_reposicion":int(fields[10])
        }

        r = self.controller.add_articulo(values)

        if r.ok:
            self.new_articulo_modal.reset()
            self.page_bar.update(0)
        else:
            ErrorWindow(r.content, self.frame)

    #Elimina los articulos seleccionados en el treeview
    def delete_articulos(self):
        #TODO Mostrar advertencia y consultar confirmacion de borrado
        id_articulos = tuple(int(x) for x in self.tree.selection())
        r = self.controller.delete_articulos_by_id(id_articulos)
        if r.ok:
            # self.update_tree()
            self.page_bar.update(0)
        else:
            ErrorWindow(r.content, self.root)

    #Abre modal para editar un articulo ya existente
    def open_edit_articulo_modal(self):
        articulo_id = self.tree.selection()[0]
        r = self.controller.get_articulo_by_id(articulo_id)
        if r.ok:
            articulo = r.content
            self.edit_articulo_modal.show(articulo)
        else:
            ErrorWindow(r.content, self.frame)
            return

    #Recibe id y campos del articulo a editar y lo edita en la base de datos, luego cierra modal
    #En caso de error, muestra el mensaje en un pop up
    def update_articulo(self, id, fields):
        id_proveedor = None if fields[2]==MISSING_VALUE else self.get_id_from_value(self.proveedores, fields[2])
        id_marca = None if fields[3]==MISSING_VALUE else self.get_id_from_value(self.marcas, fields[3])
        id_tipo = None if fields[4]==MISSING_VALUE else self.get_id_from_value(self.tipos, fields[4])

        values = {
            "id":id,
            "codigo":fields[0],
            "descripcion":fields[1],
            "id_proveedor":id_proveedor,
            "id_marca":id_marca,
            "id_tipo":id_tipo,
            "precio_lista":int(fields[5]),
            "d1":int(fields[6][0]),
            "d2":int(fields[6][1]),
            "d3":int(fields[6][2]),
            "d4":int(fields[6][3]),
            "iva":int(fields[7]),
            "g1":int(fields[8][0]),
            "g2":int(fields[8][1]),
            "g3":int(fields[8][2]),
            "g4":int(fields[8][3]),
            "stock":int(fields[9]),
            "pto_reposicion":int(fields[10])
        }

        r = self.controller.update_articulo(values)
        if r.ok:
            self.page_bar.update(SAME_PAGE)
        else:
            ErrorWindow(r.content, self.root)    


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
                return [MISSING_VALUE]+list(self.proveedores.values())
            elif field == "Marca":
                return [MISSING_VALUE]+list(self.marcas.values())
            elif field == "Tipo":
                return [MISSING_VALUE]+list(self.tipos.values())
            return ["error"]
    
    #Dado un diccionario y un valor, obtiene la clave
    #Lo usamos en dropdown menus para obtener el ID a partir del nombre de Proveedores, marcas o tipos
    def get_id_from_value(self, dict, value):
        for k,v in dict.items():
            if v==value:
                return k

    def get_add_method(self, field):
        if field=="Proveedor":
            return self.add_proveedor
        # elif field=="Marca":
        #     return self.add_marca
        # return self.add_tipo
        return None
    
    def add_proveedor(self, name):
        if len(name)==0:
            return Response(False, "ERROR: Ingrese un proveedor.")
        
        r = self.controller.add_proveedor(name)
        if r.ok:
            id=r.content["id"]
            name=r.content["name"]
            self.proveedores[id]=name
            #TODO actualizar proveedores en filtros
            self.filters.update_options("Proveedor")
            return Response(True)
        return Response(False, "ERROR: Proveedor ya existente.")
        
    
    def add_marca(self, name):
        if len(name)==0:
            return Response(False, "ERROR: Ingrese una marca.")
        
        r = self.controller.add_marca(name)
        if r.ok:
            id=r.content["id"]
            name=r.content["name"]
            self.marcas[id]=name
            self.filters.update_options("Marca")
            return Response(True)
        return Response(False, "ERROR: Marca ya existente.")
    

    def add_tipo(self, name):
        if len(name)==0:
            return Response(False, "ERROR: Ingrese un tipo de producto.")
        
        r = self.controller.add_tipo(name)
        if r.ok:
            id=r.content["id"]
            name=r.content["name"]
            self.tipos[id]=name
            self.filters.update_options("Tipo")
            return Response(True)
        return Response(False, "ERROR: Tipo de producto ya existente.")
        

"""
root
 L frameArticulos ->r=0
    L frame1 -> r=0
    L filter_frame -> r=1
    L table_frame -> r2
    L actions_frame -> r3
"""

