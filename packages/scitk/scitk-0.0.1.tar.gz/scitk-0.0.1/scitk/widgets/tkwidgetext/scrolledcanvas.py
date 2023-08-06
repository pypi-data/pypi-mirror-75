'''
    inspired by yxl
    code by hzyrc6011
    
    要查看示例，请直接运行此文件。
    To view the demo, please directly run this file.
    
'''
import tkinter as tk
from tkinter import ttk


class ScrolledCanvas(ttk.Frame):
    '''
    这是一个用来在可以滚动的区域中容纳其他控件的Frame容器。
    This is a Frame container used for containing other widgets in a scrollable area.
    
    注意：需要添加的控件不能直接放置(place/grid/pack)在此控件上，而应该放置在其scrollable_frame上。
    Attention:  Widgets need to be added cannot be directly put (place/grid/pack) on this frame ,
    but should be put on the scrollable_frame of this widget.
    '''
    def __init__(self, container,orient = 'v',  *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)

       
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion= self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        

       
        if orient.startswith('v'):
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.scrollbar.set)
            self.scrollbar.pack(side="right", fill="y")
            
        elif orient.startswith('h'):
            self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)    
            self.canvas.configure(xscrollcommand=self.scrollbar.set)        
            self.scrollbar.pack(side=tk.BOTTOM, fill="x")
            
        else:
            raise('Unknown scrollbar orientation \'{0}\' (未知的滚动条位置设置：{0})'%(orient) )
        #canvas.configure(yscrollcommand=self.scrollbar.set)
if __name__ == "__main__":
    app=tk.Tk()
    sf=ScrolledCanvas(app,'h')
    sf.pack(expand=1,fill=tk.BOTH)
    for i in range(50):
        ttk.Button(sf.scrollable_frame, text="Sample scrolling label%d"%i).pack(side=tk.LEFT)
    app.mainloop()
