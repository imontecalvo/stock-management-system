import tkinter as tk
from tkinter import ttk

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="orange")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # Crear la ventana dentro del Canvas
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        if tk.Tk().tk.call('tk', 'windowingsystem') == 'win32':
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        elif tk.Tk().tk.call('tk', 'windowingsystem') == 'x11':
            self.canvas.bind_all("<Button-4>", self._on_mousewheel)
            self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas_width = self.canvas.winfo_width()
        self.canvas.itemconfig(self.window_id, width=canvas_width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def agregar_tarjeta(self, texto):
        tarjeta = tk.Label(self.scrollable_frame, text=texto, relief="solid")
        tarjeta.pack(padx=0, pady=0, ipadx=10, ipady=5)

        # Después de agregar la tarjeta, ajustar el ancho del widget a ancho del Canvas
        # self.update_window_width()

        self.canvas.yview_moveto(1.0)

    def update_window_width(self):
        canvas_width = self.canvas.winfo_width()
        self.canvas.itemconfig(self.window_id, width=canvas_width)
        # self.canvas.update_idletasks()

# Función para agregar un producto
def agregar_producto():
    global contador
    texto_tarjeta = f"Producto {contador}"
    scrollable_frame.agregar_tarjeta(texto_tarjeta)
    contador += 1

# Crear la ventana principal
root = tk.Tk()
root.title("Tarjetas Desplazables")

# Crear un frame scrollable
scrollable_frame = ScrollableFrame(root)
scrollable_frame.pack(expand=True, fill="both")

# Botón para agregar productos
contador = 1
btn_agregar = tk.Button(root, text="Agregar Producto", command=agregar_producto)
btn_agregar.pack(pady=10, side="bottom")

# Iniciar la aplicación
root.mainloop()
