import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

class PaginatedTreeView:
    def __init__(self, root, items_per_page=10):
        self.root = root
        self.items_per_page = items_per_page
        self.page_number = 1

        # Crear el Treeview
        self.tree = ttk.Treeview(root, columns=('ID', 'Nombre', 'Precio'))
        self.tree.heading('#0', text='ID')
        self.tree.column('#0', width=50, anchor='center')
        self.tree.heading('#1', text='Nombre')
        self.tree.column('#1', width=150, anchor='w')
        self.tree.heading('#2', text='Precio')
        self.tree.column('#2', width=100, anchor='center')

        # Agregar datos de ejemplo (reemplácelos con sus propios datos)
        self.data = [
            (1, 'Artículo 1', 10.99),
            (2, 'Artículo 2', 19.99),
            # ... más datos ...
            (100, 'Artículo 100', 5.99)
        ]

        self.show_page()

        # Crear botones de navegación
        prev_button = ttk.Button(root, text='Anterior', command=self.prev_page)
        prev_button.pack(side=tk.LEFT, padx=5)
        next_button = ttk.Button(root, text='Siguiente', command=self.next_page)
        next_button.pack(side=tk.RIGHT, padx=5)

    def show_page(self):
        # Limpiar Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Calcular índices de inicio y fin para la página actual
        start_index = (self.page_number - 1) * self.items_per_page
        end_index = start_index + self.items_per_page

        # Mostrar los datos de la página actual en el Treeview
        for item_data in self.data[start_index:end_index]:
            self.tree.insert('', 'end', values=item_data)

    def prev_page(self):
        if self.page_number > 1:
            self.page_number -= 1
            self.show_page()

    def next_page(self):
        max_page = len(self.data) // self.items_per_page + 1
        if self.page_number < max_page:
            self.page_number += 1
            self.show_page()

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Puedes cambiar el tema según tus preferencias
    root.title('Treeview Paginado')
    
    paginated_treeview = PaginatedTreeView(root)
    
    paginated_treeview.tree.pack(expand=True, fill=tk.BOTH)
    
    root.mainloop()
