from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar

from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
import numpy as np
from scitk.widgets.tkwidgetext.closablenotebook import ClosableNotebook
class PlotCanvas(FigureCanvas):
    def __init__(self, parent, id=-1, fig=None, title='Plot'):
        self.figure =  Figure(figsize=(5,4),dpi=100)
        self.title = title
        super().__init__(self.figure,master=parent)

    def add_subplot(self, n=111, **key):
        return self.figure.add_subplot(n, **key)
        
class PlotFrame(ttk.Frame):
    def __init__(self, parent, toolbar=True):
        super().__init__(parent)

        self.figure = PlotCanvas(self)
        
        self.add_subplot = self.figure.add_subplot
        if toolbar: self.add_toolbar()
        self.figure._tkcanvas.pack(expand=True,fill=tk.BOTH)
        
        self.pack(fill=tk.BOTH,expand=True)

    def on_idle(self, event):
        if self.GetTitle()!=self.figure.title:
            self.SetTitle(self.figure.title)


    def add_toolbar(self):
        self.toolbar = NavigationToolbar(self.figure,self)
        self.toolbar.pack()

class PlotNoteBook(ClosableNotebook):
    def __init__(self, parent):
        super().__init__(parent)
        #self.pack(expand = True, fill = tk.BOTH)
        
    def on_idle(self, event):
        for i in range(self.GetPageCount()):
            title = self.GetPage(i).title
            if self.GetPageText(i) != title:
                self.SetPageText(i, title)

    def figure(self, i=None):
        return self.get_tab(i)
        
    def set_background(self, img):
        self.GetAuiManager().SetArtProvider(ImgArtProvider(img))

    def add_figure(self, figure=None):
        if figure is None: 
            return #grid =MGrid(self)
        self.add_tab(figure, text='hhhhhhhhhhhhhhhhhhhhhhhh' )
        return figure

    def set_title(self, panel, title):
        self.SetPageText(self.GetPageIndex(panel), title)

    def on_valid(self, event): pass

    def on_close(self, event): pass

    def mpl_connect(self, evt, method):
        if self.figure() is None: return
        self.figure().mpl_connect(
            'motion_notify_event', self.mouse_move)    



class PlotNoteFrame(ttk.Frame):
    def __init__(self, parent, toolbar=True):
        super().__init__ (parent)
        self.notebook = PlotNoteBook(self)
        self.figure = self.notebook.figure
        self.add_figure = self.notebook.add_figure
        self.notebook.pack(expand = True, fill = tk.BOTH)
        self.pack(expand = True, fill = tk.BOTH)
        
    def add_toolbar(self):
        self.toolbar = NavigationToolbar(self.notebook)
        self.toolbar.Realize()
        self.GetSizer().Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.toolbar.update()
    
    def create_subplot(self):
        '''
        create a new subplot in a new tab, return a new subplot for plot.
        新建一个标签页，并且在其上创建一个新的subplot。返回值为plt.subplot。
        '''
        pframe = PlotFrame(self)
        fig = pframe.figure
        ax = fig.add_subplot()
        self.notebook.add_figure(pframe)    
        return ax
        
    def create_figure(self)->Figure:
        '''
        create a new figure in a new tab, return a new figure for plot.
        新建一个标签页，并且在其上创建一个新的figure。返回值为plt.figure。
        '''
        pframe = PlotFrame(self)
        fig = pframe.figure
        self.notebook.add_figure(pframe)    
        return fig
    
    def clear_figure(self,tab_id:int)->None:
        '''
        clear all plots on tab identified by tab_id. 
        清空tab_id所对应的标签页上的图像。
        '''
        f = self.get_figure(tab_id).clf()
    def get_figure_tab(self,tab_id:int)->PlotFrame:
        """获取tab_id对应的figure的标签页。"""
        return self.notebook.get_tab(tab_id)
        
    def get_figure(self,fig_id=None)->Figure:
        '''获取当前fig_id对应的Figure.'''
        return self.get_figure_tab(fig_id).figure.figure
        
    def delete_figure(self,tab_id:int):
        """
        delete figure tab identified by tab_id.
        删除tab_id表示的标签页及其上的图像。
        """
        self.notebook.delete_tab(tab_id)
    def update(self,tab_id=None):
        '''
        update figure identified by tab_id
        刷新tab_id对应的标签页的Figure，当清除重绘的时候应当调用此函数。
        '''
        canvas = self.get_figure_tab(0).figure
        canvas.draw()
        canvas.flush_events()
        
if __name__ == '__main__':
    app = tk.Tk()
    pnf=PlotNoteFrame(app)
    pnb=pnf.notebook
    pframe = PlotFrame(pnb)
    ax = pframe.add_subplot(111)
    x = np.linspace(0,10,100)
    y = np.sin(x)
    ax.plot(x, y)
    ax.grid()
    ax.set_title('abc')
    pnb.add_figure(pframe)
    
    pframe2 = PlotFrame(pnb)
    ax = pframe2.add_subplot()
    x = np.linspace(0,10,100)
    y = np.exp(x)
    ax.plot(x, y)
    ax.grid()
    ax.set_title('def')
    pnb.add_figure(pframe2)
    
    app.mainloop()


