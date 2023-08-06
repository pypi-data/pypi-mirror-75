from tkinter import ttk
import tkinter as tk
from PIL import ImageTk,Image

def make_logo(logo_path:str,logo_size):
    '''
    The lib tkinter only supports .gif format as button logo. This function is used to convert any type of logo file to show on tkinter widgets.
    tkinter 只支持.gif格式的图像作为按钮的图标。这个函数可以将任意格式的图像文件转换为可以显示在控件上的图像。
    '''
    img_origin = Image.open(logo_path)  # 打开图片
    if not type(logo_size)==tuple: 
        raise Exception("Invalid logo size.logo_size should be a tuple such as (24,24)")
    img_origin=  img_origin.resize(logo_size, Image.ANTIALIAS)     # 缩放到所需大小
    img = ImageTk.PhotoImage(img_origin)  # 用PIL模块的PhotoImage打开

    return img
    
class Toolbar(ttk.Frame):
    '''
    Toolbar(ttk.Frame) 
    input params in __init__ method:  parent
    accessible properties(可以访问的属性):
    --logo_size  :the size of logo,is a tuple(w,h),default is (24,24)
    '''
    def __init__(self,parent):
        super().__init__(parent)
        self.logo_size = (24,24) # logo的尺寸。
        self.__image_set = set()# 对各个命令对应的按钮进行引用。

    def add_tool(self,logo:str,tool:callable):
        '''
        logo:str,图片路径
        tool:callable,点击此工具时调用的函数。
        '''
        img = make_logo(logo,self.logo_size)
        self.__image_set.add(img)
        b=ttk.Button(self,text='ddddd',image =img,command = tool)
        b.pack(side=tk.LEFT)


if __name__=="__main__":
    app = tk.Tk()
    tb = Toolbar(app)
    tb.pack(fill=tk.X,expand =True)
    tb.add_tool('/media/hzy/程序/novalide/forgitcommit/NovalIDE/noval/bmp_source/unittest_wizard.png',lambda:print('ddd'))
    text = tk.Text(app)
    text.pack(fill=tk.BOTH,expand=True)
    app.mainloop()
    