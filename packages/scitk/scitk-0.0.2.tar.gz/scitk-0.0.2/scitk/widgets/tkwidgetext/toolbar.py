from tkinter import ttk
class Toolbar(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        b=ttk.Button(text='aa')
        b.pack()
        pass
