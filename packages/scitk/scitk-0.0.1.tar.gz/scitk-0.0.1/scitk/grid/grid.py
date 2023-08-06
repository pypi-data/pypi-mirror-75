import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np

from scitk.widgets.scrollabletreeviewframe import ScrollableTreeviewFrame
class Grid(ScrollableTreeviewFrame):
    def __init__(self,master):
        super().__init__(master)

    def set_data(self,data):
        columns = ['']+list(data.columns.values)
        
        self.set_widgets(columns)
        self.treeview.bind('<ButtonRelease-1>', self.treeview_click)
        for col in columns:
            self.treeview.column(col, anchor = "center")
            self.treeview.heading(col, text = col)

        for i in range(data.shape[0]):
            row=data.iloc[i]
            #print(row[0],list(row))
            self.treeview.insert('', i, values = [i]+list(row))
            i += 1
         
    def treeview_click(event):  # 单击
        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            print(item_text)
 
    def selectTree(event):
        for item in tree.selection():
            item_text = tree.item(item, "values")
            print(item_text)

if __name__ == '__main__':
    window = tk.Tk()
    # 设置窗口大小
    winWidth = 600
    winHeight = 400
    # 获取屏幕分辨率
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
     
    x = int((screenWidth - winWidth) / 2)
    y = int((screenHeight - winHeight) / 2)
     
    # 设置主窗口标题
    window.title("TreeView参数说明")
    # 设置窗口初始位置在屏幕居中
    window.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
    # 设置窗口图标

    # 设置窗口宽高固定
    window.resizable(0, 0)
     
    # 定义列的名称


    grid=Grid(window)
    
    # 选中行
    #tree.bind('<<TreeviewSelect>>', selectTree)
     
    window.mainloop()
