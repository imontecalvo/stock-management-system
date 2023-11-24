# import tkinter as tk
# from tkinter import ttk

# def calculate_visible_rows(treeview_height, row_height):
#     return int(treeview_height / row_height)

# # Create a simple Tkinter window
# root = tk.Tk()
# root.title("Treeview Pagination")
# root.attributes("-zoomed", True)

# root.grid_rowconfigure(1, weight=1)

# b = tk.Button(root, text="Click", command=lambda: print("Number of visible rows:", int(treeview.winfo_height()//row_height)-1))
# b.grid(row=0,column=0)


# # Create a Treeview widget
# treeview = ttk.Treeview(root, columns=("Column1", "Column2"))
# # Insert sample data
# for i in range(1, 1):
#     treeview.insert("", "end", values=("Item {}".format(i), "Description {}".format(i)))

# # Pack the Treeview widget
# treeview.grid(row=1, column=0, sticky='nsew')

# # Get the total height of the Treeview
# treeview_height = treeview.winfo_reqheight()

# # Assume each row has a height of 20 pixels (you should adjust this based on your actual row height)
# row_height = 20

# # Calculate the number of visible rows
# visible_rows = calculate_visible_rows(treeview.winfo_reqheight(), row_height)

# # Print the result
# # print("Number of visible rows:", calculate_visible_rows(treeview.winfo_reqheight(), row_height))

# print(treeview.winfo_height())
# # print("Number of visible rows:", int(treeview.winfo_height()//row_height)-1)

# root.after(10000, print("Visible rows:", int(treeview.winfo_height()//row_height)-1))
# # Start the Tkinter event loop
# root.mainloop()

# #


import tkinter as tk
from tkinter import ttk

def calculate_visible_rows(treeview, row_height):
    treeview.update()  # Force an update to get the correct dimensions
    treeview_height = treeview.winfo_height()
    return int(treeview_height / row_height)

# Create a simple Tkinter window
root = tk.Tk()
root.title("Treeview Pagination")
root.attributes("-zoomed", True)
root.grid_rowconfigure(0,weight=1)
root.grid_columnconfigure(0,weight=1)

# Create a Treeview widget


frame = tk.Frame(root, bg="red")
frame.grid(row=0, column=0, sticky='nsew')
frame.grid_rowconfigure(1,weight=1)

l = tk.Label(frame, text="ASdadsas")
l.grid(row=0,column=0, pady=100)

treeview = ttk.Treeview(frame, columns=("Column1", "Column2"))

# Insert sample data
for i in range(1, 101):
    treeview.insert("", "end", values=("Item {}".format(i), "Description {}".format(i)))

# Pack the Treeview widget
treeview.grid(row=1,column=0, sticky='nsew')

# Assume each row has a height of 20 pixels (you should adjust this based on your actual row height)
row_height = 20

# Calculate the number of visible rows
visible_rows = calculate_visible_rows(treeview, row_height)

# Print the result
print("Number of visible rows:", visible_rows)

# Start the Tkinter event loop
root.mainloop()
