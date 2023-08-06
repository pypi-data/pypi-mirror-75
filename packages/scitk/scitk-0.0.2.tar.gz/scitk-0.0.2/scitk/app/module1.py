import tkinter as tk
from tkinter import ttk
import os
import sys
import time
import threading


from scitk.grid import GridNoteBook

import scitk.app
class SciApp(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.m1 = tk.PanedWindow(self)
        self.m1.pack(fill="both", expand=1)
         
        left = tk.Label(self.m1, text="left pane")
        self.m1.add(left)
         
        self. m2 = tk.PanedWindow(self,orient="vertical",showhandle=True, sashrelief="sunken")
        self.m1.add(self.m2)
         
        top = tk.Label(self.m2, text="top pane")
        self.m2.add(top)
         
        bottom = tk.Label(self.m2, text="bottom pane")
        self.m2.add(bottom)

if __name__=='__main__':
    app=tk.Tk()
    sa=SciApp(app)
    sa.pack(expand=True,fill=tk.BOTH)
    app.geometry('1024x768+100+100')
    sa.mainloop()
