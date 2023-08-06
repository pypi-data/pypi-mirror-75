from tkinter import ttk
import tkinter as tk
from scitk.widgets.toolbar import make_logo
class ControlWidget():
    """
    parent
    widget_name
    callback
    widget_text
    """
    def __init__(self, parent: ttk.Frame, widget_name: str, callback: callable, widget_text='',widget_logo=None):
        if widget_text == '':
            self.text = self.name = widget_name
        else:
            self.name = widget_name
            self.text = widget_text
        self.widget_logo = widget_logo
        self.callback = callback
    def on_action(self):
        self.callback()# 不用显式传入self，因为自身调用的时候就已经传入了。

class ButtonWidget(ControlWidget):
    def __init__(self, parent: ttk.Frame, widget_name: str, callback: str, widget_text='',widget_logo=None):
        super().__init__(parent,widget_name,callback,widget_text,widget_logo)
        self.button = ttk.Button(parent, text=widget_text, command=self.on_action)
        self.button.pack()

class SwitchWidget(ControlWidget): # 有True和False两种状态。
    '''
    按下时为True,弹起时为False
    parent
    widget_name
    callback:tuple型，两元素。分别为按下时事件、弹起时事件。
    widget_text:tuple型，两元素。分别为按下时显示的文字，弹起状态下的文字。
    widget_logo:tuple型，两元素。分别为按下和弹起状态下显示的图片。
    '''
    def __init__(self, parent: ttk.Frame, widget_name: str, callback: str, widget_text=('on','off'),widget_logo=None,status=False):
        super().__init__(parent,widget_name,callback,widget_text,widget_logo)
        text = widget_text[1] if status==False else widget_text[0]
        self.status = status
        self.switch = ttk.Button(parent, text=text, command=self.on_action)
        self.switch.pack()
        if widget_logo is not None:
            self.widget_logo = (make_logo(widget_logo[0],(16*16)),make_logo(widget_logo[1],(16*16)))
        else:
            self.widget_logo=None

    def on_action(self):
        print('on_action',self.status)
        if self.status == False:
            self.switch.config(text=self.text[0])
            if self.widget_logo==None:
                self.switch.state(['pressed'])
            else:
                self.switch.config(image=self.widget_logo[0])
        else:
            self.switch.config(text=self.text[1])
            if self.widget_logo==None:
                self.switch.state(['!pressed'])
            else:
                self.switch.config(image=self.widget_logo[1])
        self.switch.update()
        self.status = not self.status
        self.callback()

    def configs(self):
        pass
