import customtkinter
import tkinter as tk
from tkinter import ttk
from math import ceil
from ...constants import *

class PaginationBar():
    def __init__(self, parent, button_command, total_records_command, tree):
        self.current_page = 1
        self.button_command = button_command
        self.total_records = total_records_command
        self.tree=tree
        self.parent = parent
        

    def initialize(self):
        self.tree.tree.update()
        self.records_per_page = int (self.tree.height() // ROW_HEIGHT) - 1
        last_page = self.get_last_page()

        pagination_frame = tk.Frame(self.parent)
        pagination_frame.grid(row=0,column=1)

        self.prev_page = customtkinter.CTkButton(pagination_frame, text="<", corner_radius=5, anchor="center", height=20, width=20, font=('_',13), command=lambda: self.update(-1))
        self.prev_page.grid(row=0, column=0, padx=(0,5))
        self.prev_page.configure(state="disabled")

        self.page_label = customtkinter.CTkLabel(pagination_frame, text=f"{self.current_page}/{last_page}", fg_color="transparent",text_color="black",font=('_',14))
        self.page_label.grid(row=0,column=1)
        
        self.next_page = customtkinter.CTkButton(pagination_frame, text=">", corner_radius=5, anchor="center", height=20, width=20, font=('_',13), command=lambda: self.update(1))
        self.next_page.grid(row=0, column=2, padx=(5,0))


    # Se llama cada vez que es potencialmente necesaria una actualización:
    #   - Cambio de página por presionanr botón (anterior o siguiente) -> Movement: +-1
    #   - Adicion de articulo (Mostrar el nuevo articulo y ademas puede incrementar el nro de paginas) -> Movement: 0
    #   - Eliminacion de articulo (Dejar de mostrar el nuevo articulo y ademas puede reducirse el nro de paginas) -> Movement: 0
    #   - Edicion de articulo (Mostrar el articulo actualizado) -> Movement: 0
    #   - Carga inicial de datos -> Movement: 0
    #   - Actualizacion de filtros -> Movement: -2 (JUMP_2_FIRST_PAGE)
    # La funcion actualiza correctamente la pagina actual, la información visualizada, habilita/deshabilita botones y llama al 
    # comando que pide e inserta los datos (pasandole el limit y offset correspondientes)
    def update(self, movement):
        last_page = self.get_last_page()

        #Actualizacion de pagina
        if movement==SAME_PAGE and self.current_page > last_page:
            self.current_page = last_page
        elif movement==JUMP_2_FIRST_PAGE:
            self.current_page = 1
        else:
            self.current_page+=movement
        
        #Chequear habilitacion de botones
        self.next_page.configure(state="normal")
        self.prev_page.configure(state="normal")
        if self.current_page == 1:
            self.prev_page.configure(state="disabled")
        if self.current_page == last_page:
            self.next_page.configure(state="disabled")
            

        self.page_label.configure(text=f"{self.current_page}/{last_page}")

        self.button_command()

    
    def get_last_page(self):
        return ceil(self.total_records()/self.records_per_page) 

    def get_limit_offset(self):
        return self.records_per_page, (self.current_page-1)*self.records_per_page