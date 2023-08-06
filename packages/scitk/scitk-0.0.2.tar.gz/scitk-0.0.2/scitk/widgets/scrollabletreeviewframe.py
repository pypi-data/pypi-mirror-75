from tkinter import ttk
import tkinter as tk
import pandas as pd
import numpy as np
class ScrollableTreeviewFrame(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        
        self.hFrame=ttk.Frame(self)
        
        self.hFrame.pack(expand = True, fill = tk.BOTH)
        self.start=False
        self.button=ttk.Button(self,command=lambda : self.set_data(pd.DataFrame(np.random.randn(100,5))))
        self.button.pack(side=tk.LEFT)
        self.set_widgets()
        self.pack(side=tk.LEFT,expand = True, fill = tk.BOTH)

    def set_widgets(self,columns=None):
        if self.start:# 反正不好删改，就直接把控件删掉了。
            self.treeview.destroy()
            self.verticalScrollbar.destroy()
            self.horizontalScrollbar.destroy()
        self.start=True
        self.treeview = ttk.Treeview(self.hFrame, show = "headings", columns = columns, selectmode = tk.BROWSE)
        self.verticalScrollbar = ttk.Scrollbar(self.hFrame, orient="vertical", command=self.treeview.yview)
        
        self.horizontalScrollbar=ttk.Scrollbar(self,orient='horizontal',command=self.treeview.xview)
        self.treeview.pack(side=tk.LEFT,expand = True, fill = tk.BOTH)
        self.verticalScrollbar.pack(side=tk.LEFT, expand=True,fill=tk.Y)
        
        self.horizontalScrollbar.pack(expand=True,fill=tk.X)
        self.treeview.configure(yscrollcommand=self.verticalScrollbar.set)
        self.treeview.configure(xscrollcommand=self.horizontalScrollbar.set)