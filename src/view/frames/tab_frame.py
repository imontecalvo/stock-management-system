import tkinter as tk
from tkinter import ttk


class TabFrame():
    def __init__(self,root, controller):
        self.root=root
        self.controller=controller
        self.frame=tk.Frame(root)
        self.frames=[]

    # def show(self):

    #     self.frame.tkraise()