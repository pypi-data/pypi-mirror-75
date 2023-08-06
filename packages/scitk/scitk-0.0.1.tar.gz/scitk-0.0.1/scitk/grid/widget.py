from tkinter import ttk
import tkinter as tk   
from scitk.widgets.tkwidgetext.closablenotebook import ClosableNotebook
from scitk.widgets.toolbar import Toolbar

class MGrid(ttk.Frame):
    def __init__(self, parent=None, autofit=False):
        ttk.Frame.__init__ ( self, parent)
##        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
##        
##        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
        sizer = ttk.Frame(self)# wx.BoxSizer( wx.VERTICAL )
        sizer.pack(expand = True, fill=tk.BOTH)
        self.lab_info =ttk.Label(sizer,text ='information')
        self.lab_info.pack()
        
##        self.Bind(wx.EVT_IDLE, self.on_idle)
##        sizer.Add( self.lab_info, 0, wx.EXPAND, 0 )
##        
        self.grid = Grid(self)
        self.grid.pack(fill=tk.BOTH,expand=True)
##        sizer.Add( self.grid, 1, wx.EXPAND |wx.ALL, 0 )
##        self.SetSizer(sizer)
        self.select = self.grid.select
        self.set_data = self.grid.set_data

    @property
    def table(self): return self.grid.table

    @property
    def name(self): return self.grid.table.name

    def on_idle(self, event):
        if self.table.data is None: return
        if self.lab_info.GetLabel() != self.table.info:
            self.lab_info.SetLabel(self.table.info)

class GridFrame(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__ ( self, parent)
##                            , id = wx.ID_ANY,
##                            title = 'GridFrame',
##                            pos = wx.DefaultPosition,
##                            size = wx.Size( 800, 600 ),
##                            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        sizer = ttk.Frame(self)#wx.BoxSizer(wx.VERTICAL)
        sizer.pack(expand=True,fill=tk.BOTH)
        self.grid = MGrid(sizer)
##        self.SetSizer(sizer)
        self.set_data = self.grid.set_data
##        self.Bind(wx.EVT_IDLE, self.on_idle)

    def on_idle(self, event):
        if self.GetTitle()!=self.grid.table.name:
            self.SetTitle(self.grid.table.name)
    
    def set_title(self, tab): self.SetTitle(tab.name)

    def on_valid(self, event): event.Skip()

    def on_close(self, event): event.Skip()

    def Show(self):
        self.Fit()
        wx.Frame.Show(self)

class GridNoteBook(ClosableNotebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand = True, fill = tk.BOTH)
        
    def on_idle(self, event):
        for i in range(self.GetPageCount()):
            title = self.GetPage(i).table.title
            if self.GetPageText(i) != title:
                self.SetPageText(i, title)

    def grid(self, i=None)->ttk.Frame:
        return self.get_tab(i)
        
    def set_background(self, img):
        self.GetAuiManager().SetArtProvider(ImgArtProvider(img))

    def add_grid(self, grid=None):
        if grid is None: 
            return #grid =MGrid(self)
        self.add_tab(grid, text='hhhhhhhhhhhhhhhhhhhhhhhh' )
        return grid

    def set_title(self, panel, title):
        self.SetPageText(self.GetPageIndex(panel), title)

    def on_valid(self, event): pass

    def on_close(self, event): pass
    

class GridNoteFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__ (parent)
        
        
        self.notebook = GridNoteBook(self)
        self.toolbarFrame=ttk.Frame(self)
        self.grid = self.notebook.grid # 这个是重写了函数
        self.toolbarFrame.pack(expand=True,fill=tk.X)
        self.notebook.pack(expand=True,fill=tk.BOTH)
        self.add_grid = self.notebook.add_grid

        self.pack(expand=True,fill=tk.BOTH)

    def add_toolbar(self):
        toolbar = ToolBar(self.toolbarFrame)
        toolbar.pack()
        return toolbar 

    def on_close(self, event):
        while self.notebook.GetPageCount()>0:
            self.notebook.DeletePage(0)
        event.Skip()

if __name__=='__main__':
    from scitk.grid.grid import Grid
    import pandas as pd
    import numpy as np
    window = tk.Tk()
    gnf=GridNoteFrame(window)
    nb=gnf.notebook
    grid2=Grid(nb)
    nb.add_grid(Grid(nb))
    nb.add_grid(grid2)
    nb.add_grid(Grid(nb))
    nb.add_grid(Grid(nb))
    nb.delete_tab('current')
    nb.grid(1).set_data(pd.DataFrame(np.random.randn(100,5)*100))
    window.mainloop()
