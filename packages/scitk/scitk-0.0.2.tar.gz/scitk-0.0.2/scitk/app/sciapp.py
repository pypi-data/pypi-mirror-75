import sys

sys.path.append('/media/hzy/程序/novalide/forgitcommit/scitk/scitk/')
import tkinter as tk
from tkinter import ttk
import os
import sys
import time
import threading

from scitk.grid import GridNoteBook
from scitk.widgets import normal
from scitk.widgets import paradialog
from scitk.widgets.controls import ButtonWidget,SwitchWidget
from scitk.plot.plot import PlotFrame, PlotNoteFrame
import scitk

import numpy as np

view_dic = {'plot': PlotNoteFrame}
control_dic = {'button':ButtonWidget,'switch':SwitchWidget}


class ParamWidget():
    '''
    parent
    widget_name
    widget_type
    widget_args
    callback: function call when value is changed.
    widget_text
    '''

    def __init__(self, parent: ttk.Frame, widget_name: str, widget_type: str, widget_args: tuple, callback=None,
                 widget_text='', initial_value=None):
        self.name = widget_name

        if widget_type in paradialog.widgets.keys():
            self.widget = paradialog.widgets[widget_type](parent, *widget_args)
        else:
            raise Exception("Widget type \'%s\' is invalid." % widget_type)

        self.widget.pack()
        self.callback = None
        self.widget.on_para_change = callback
        if initial_value is not None:
            self.widget.SetValue(initial_value)
        pass

    def get_value(self):
        return self.widget.GetValue()

    def set_value(self, val):
        self.widget.SetValue(val)



class SciApp(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        ##        fileMenu = tk.Menu(menubar)
        ##        fileMenu.add_command(label="Exit", command=lambda:print('hhhhh'))
        ##        menubar.add_cascade(label="File", menu=fileMenu)

        self.toolbar_frame = ttk.Frame(self)
        self.toolbar_frame.pack(fill=tk.X)
        self.toolbar = scitk.widgets.toolbar.Toolbar(self.toolbar_frame)
        self.toolbar.pack(fill=tk.X, expand=1)
        # self.toolbar .add_tool('/media/hzy/程序/novalide/forgitcommit/NovalIDE/noval/bmp_source/unittest_wizard.png',lambda:print('ddd'))

        ##        b = ttk.Button(self.toolbar_frame,text='aaaaa')
        ##        b.pack(side=tk.LEFT)

        frame1 = ttk.Frame(self)
        frame1.pack(expand=1, fill=tk.BOTH)

        self.toolbar_left = ttk.Frame(frame1)
        self.toolbar_left.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        self.mainPane = ttk.Frame(frame1)
        self.mainPane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.m1 = tk.PanedWindow(self.mainPane)  # ,showhandle =False, sashrelief="sunken")
        self.m1.pack(fill="both", expand=1)

        left = ttk.Frame(self.m1)
        self.m1.add(left)

        self.m2 = tk.PanedWindow(self.m1, orient="vertical")  # ,showhandle=True, sashrelief="sunken")
        self.m1.add(self.m2)

        self.view_panel = ttk.Frame(self.m2)
        self.m2.add(self.view_panel)

        self.sub_panel = ttk.Frame(self.m2)
        self.m2.add(self.sub_panel)

        self.control_panel = ttk.Frame(self.m1)
        self.m1.add(self.control_panel)

        self.control_widget_dict = {}
        self.view_widget_dict = {}
        self.param_widget_dict = {}

    def add_view(self, view_type, view_name):
        v = view_dic[view_type](self.view_panel)
        v.pack(fill=tk.BOTH, expand=True)
        self.view_widget_dict[view_name] = v

    def add_param(self, name: str, param_type: object, arguments: tuple, callback=None, initial_value=None):
        '''
        name:str
        param_type
        arguments
        callback
        initial_value
        '''
        self.param_widget_dict[name] = ParamWidget(self.control_panel, name, param_type, arguments, callback=callback,
                                                   initial_value=initial_value)
        self.param_widget_dict[name].widget.set_app(self)

    def add_control(self, name='', control_type='',callback='', text=''):
        '''
        添加控件。
        name:
        control_type
        callback
        text
        '''
        if name in self.control_widget_dict.keys():
            raise  Exception("Control widget '%s' is already defined"%name)
        if control_type not in control_dic.keys():
            raise  Exception("Control Type '%s' is invalid."%control_type)
        self.control_widget_dict[name] = control_dic[control_type](self.control_panel, widget_name=name,
                            callback=lambda: callback(self), widget_text=text)

    def get_param_widget(self, name) -> ParamWidget:
        if name not in self.param_widget_dict.keys():
            raise Exception('Param widget name \'%s\' is not defined!' % name)
        else:
            return self.param_widget_dict[name]

    def get_control_widget(self, name: str) -> ButtonWidget:

        if name not in self.control_widget_dict.keys():
            raise ('Control widget name \'%s\' is not defined!' % name)
        else:
            return self.control_widget_dict[name]

    def get_view_widget(self, button_name: str):

        if button_name not in self.view_widget_dict.keys():
            raise (Exception('View widget name \'%s\' is not defined!' % button_name))
        else:
            return self.view_widget_dict[button_name]


def run_app(add_widgets_fcn):
    app = tk.Tk()
    sa = SciApp(app)

    sa.pack(expand=True, fill=tk.BOTH)
    add_widgets_fcn(sa)
    print('Finished loading widgets. widgets are as follows:')
    print('view_widgets:',list(sa.view_widget_dict.keys()))
    print('param_widgets:',list(sa.param_widget_dict.keys()))
    print('control_widgets:',list(sa.control_widget_dict.keys()))
    app.geometry('800x600+100+100')
    sa.mainloop()


if __name__ == '__main__':
    run_app()
