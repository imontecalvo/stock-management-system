import tkinter as tk
from tkinter import ttk

def toggle_scroll():
    global scroll_enabled
    tree.yview_scroll(1,'units')
    scroll_enabled = not scroll_enabled  # Toggle the scroll state
    
    if scroll_enabled:
        tree.configure(yscrollcommand='')
    else:
        tree.configure(yscrollcommand=lambda *args: tree.yview_moveto(0))
        # tree.configure(yscrollcommand=lambda *args: tree.yview_scroll(-100,"units"))
        # tree.configure(yscrollcommand=False)

def on_mousewheel(event):
    # Evitar el desplazamiento al hacer scroll con el ratón
    return "break"

root = tk.Tk()
root.title("Toggle Scrolling in TreeView")

# Create a Treeview widget
tree = ttk.Treeview(root, columns=('Column1', 'Column2'), show='headings')

# Insert some sample data
tree.heading('Column1', text='Column 1')
tree.heading('Column2', text='Column 2')

for i in range(1, 21):
    tree.insert('', 'end', values=(f'Value {i}', f'Value {i*2}'))

# Pack the Treeview
tree.pack(expand=True, fill=tk.BOTH)

tree.bind("<Button-4>",on_mousewheel)
tree.bind("<Button-5>",on_mousewheel)

# Button to toggle scrolling
scroll_enabled = True
toggle_scroll_button = tk.Button(root, text="Toggle Scrolling", command=toggle_scroll)
toggle_scroll_button.pack(pady=5)

root.mainloop()

"""

Now i want to know if there is some solution to this: setting tree.configure(yscrollcommand=lambda *args: tree.yview_moveto(0)) works but when i scroll down i can see for a milisecond the scrolling and then it returns to the top. It's not clean, and i want to know if there is some way to lock the scrollling

"""