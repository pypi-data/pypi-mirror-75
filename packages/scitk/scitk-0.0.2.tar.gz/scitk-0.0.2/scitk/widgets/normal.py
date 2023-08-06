import tkinter as tk
from tkinter import ttk
import platform
import numpy as np
import warnings
from tkinter import colorchooser
import time
import string

class ParamWidgetFrame(ttk.Frame):
    '''
    基础参数控件的类型。所有的参数控件都在其上派生而来。
    '''

    def __init__(self, parent):
        super().__init__(parent)
        self.on_para_change = None
        self.__app = None  # SciApp。初始化控件的时候指定，并且在调用set_app的时候传入。

    def para_changed(self):
        if (self.on_para_change is not None) and (self.__app is not None):
            self.on_para_change(self.__app)
            print(time.time())

    def set_app(self, app):
        self.__app = app

    def is_key(self,event,type=''):
        '''
        'dir':判断方向键
        'alpha':判断是否为26个字母
        'hex':判断是否为十六进制数字或者字母
        'digit':判断是否为数字0~9
        'valid':包含数字、字母或者退格键。
        '''
        print(event.keysym)
        type = type.lower()
        if type=='':
            return True
        elif type.startswith('dir'):
            return event.keysym.lower() in ('left','right','up','down')
        elif type.startswith('alpha'):
            return event.keysym in  string.ascii_lowercase
        elif type.startswith('hex'):
            return event.keysym in string.hexdigits
        elif type.startswith(('digit')):
            return event.keysym in string.digits



class NumCtrl(ParamWidgetFrame):
    """NumCtrl: derived from tk.Entry
    用于输入数值。
    """

    def __init__(self, parent, rang: tuple, accury: int, title: str, unit: str):
        super().__init__(parent)
        self.on_check_callback = None
        self.prefix = lab_title = ttk.Label(self, text=title)
        self.prefix.pack(fill=tk.X, expand=1)

        entryFrame = ttk.Frame(self)

        self.ctrl = tk.Entry(entryFrame)
        self.ctrl.bind('<KeyRelease>', self.ontext, '+')
        self.ctrl.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.postfix = lab_unit = ttk.Label(entryFrame, text=unit)
        self.postfix.pack(side=tk.LEFT, fill=tk.X, expand=1)
        entryFrame.pack(expand=1, fill=tk.X)

        self.min, self.max = rang
        self.accury = accury

    def Bind(self, z, f):
        self.f = f

    def ontext(self, event):
        self.f(self)
        if self.GetValue() == None:
            self.ctrl.config(bg='#ffff00')
        else:
            self.ctrl.config(bg='#ffffff')
            self.para_changed()
        self.ctrl.update()
        if callable(self.on_check_callback):
            self.on_check_callback()

    def SetValue(self, n):
        self.ctrl.delete(0, tk.END)
        self.ctrl.insert(0, str(round(n, self.accury) if self.accury > 0 else int(n)))

    def GetValue(self):
        sval = self.ctrl.get()
        print(sval)
        try:
            num = float(sval) if self.accury > 0 else int(sval)
        except ValueError:
            import traceback
            traceback.print_exc()
            return None
        if num < self.min or num > self.max:
            return None
        if abs(round(num, self.accury) - num) > 10 ** -(self.accury + 5):  # 这么写才比较严谨吧
            return None
        return num

    def f(self, e):
        pass

    def Refresh(self):
        pass


class TextCtrl(ParamWidgetFrame):
    def __init__(self, parent, title, unit):
        super().__init__(parent)
        self.on_check_callback = None

        self.prefix = lab_title = ttk.Label(self, text=title)
        self.prefix.pack(fill=tk.X, expand=1)

        entryFrame = ttk.Frame(self)

        self.ctrl = tk.Entry(entryFrame)
        self.ctrl.bind('<KeyRelease>', self.ontext)
        self.ctrl.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.postfix = lab_unit = ttk.Label(entryFrame, text=unit)
        self.postfix.pack(side=tk.LEFT, fill=tk.X, expand=1)
        entryFrame.pack(expand=1, fill=tk.X)

    def param_changed(self, event):
        pass

    # ! TODO: what is this?
    def Bind(self, z, f): self.f = f

    def ontext(self, event):
        self.para_changed()

    def SetValue(self, n: str):
        self.ctrl.delete(0, tk.END)
        self.ctrl.insert(0, n)

    def GetValue(self) -> str:
        return self.ctrl.get()


class ColorCtrl(ParamWidgetFrame):
    def __init__(self, parent, title, unit):
        super().__init__(parent)
        self.on_check_callback = None
        self.prefix = lab_title = ttk.Label(self, text=title)
        self.prefix.pack(fill=tk.X, expand=1)

        entryFrame = ttk.Frame(self)

        self.ctrl = tk.Entry(entryFrame)
        self.ctrl.bind('<KeyRelease>', self.ontext)
        self.ctrl.bind('<Double-Button-1>', self.oncolor)
        self.ctrl.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.postfix = lab_unit = ttk.Label(entryFrame, text=unit)
        self.postfix.pack(side=tk.LEFT, fill=tk.X, expand=1)
        entryFrame.pack(expand=1, fill=tk.X)

    def Bind(self, z, f):
        self.f = f

    def ontext(self, event):
        print('value ', self.GetValue())
        if self.GetValue() == None:
            self.ctrl.config(bg='#ffffff')
        else:
            self.ctrl.config(bg=self.ctrl.get())
            self.para_changed()
        self.ctrl.update()
        if callable(self.on_check_callback):
            self.on_check_callback()

    def oncolor(self, event):
        rst = None
        val = self.GetValue()
        print('val', val)
        color = self.colorTup2Str(self.GetValue())
        if color is None:
            color = '#ffffff'
        color = colorchooser.askcolor(color)  # wx.ColourDialog(self)
        print(color)
        self.SetValue(self.colorStr2Tup(color[1]))
        if callable(self.on_check_callback):
            self.on_check_callback()

    ##        dialog.GetColourData().SetChooseFull(True)
    ##        if dialog.ShowModal() == wx.ID_OK:
    ##            rst = dialog.GetColourData().GetColour()
    ##            self.ctrl.SetBackgroundColour(rst)
    ##            self.ctrl.SetValue(rst.GetAsString(wx.C2S_HTML_SYNTAX))
    ##            self.f(self)
    ##        dialog.Destroy()

    def SetValue(self, color):
        print(color)
        if color is None:
            color = (255, 255, 255)
        strcolor = self.colorTup2Str(color)
        self.ctrl.config(bg=strcolor)  # SetBackgroundColour(color)
        self.ctrl.delete(0, tk.END)
        self.ctrl.insert(0, strcolor)

    def GetValue(self):
        rgb = self.ctrl.get().strip()
        print('rgnb', rgb)
        if len(rgb) != 7 or rgb[0] != '#':
            return None
        try:
            int(rgb[1:], 16)
        except:
            import traceback
            traceback.print_exc()
            return None
        return self.colorStr2Tup(rgb)

    def colorStr2Tup(self, value: str) -> tuple:  # pos或者wh的输入都是tuple
        def convert(c):
            v = ord(c)
            if (48 <= v <= 57):
                return v - 48
            else:
                return v - 87  # 返回a的值。

        value = value.lower()
        c0 = convert(value[1]);
        c1 = convert(value[2])
        c2 = convert(value[3]);
        c3 = convert(value[4])
        c4 = convert(value[5]);
        c5 = convert(value[6])
        a1 = c0 * 16 + c1;
        a2 = c2 * 16 + c3;
        a3 = c4 * 16 + c5
        return (a1, a2, a3)

    def colorTup2Str(self, value: tuple) -> str:
        strcolor = '#'
        for i in value:
            strcolor += hex(int(i))[-2:].replace('x', '0')
        return strcolor


class PathCtrl(ParamWidgetFrame):
    def __init__(self, parent, title, filt):
        super().__init__(parent)
        self.prefix = lab_title = ttk.Label(self, text=title)
        self.prefix.pack(fill=tk.X, expand=1)

        entryFrame = ttk.Frame(self)
        self.ctrl = tk.Entry(entryFrame)
        self.ctrl.bind('<KeyRelease>', self.ontext)
        self.ctrl.bind('<ButtonPress-1>', self.onselect)
        self.ctrl.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        entryFrame.pack(expand=1, fill=tk.X)

    def Bind(self, z, f): self.f = f

    def ontext(self, event):
        self.para_changed()
        print('ColorCtrl')

    def onselect(self, event):
        # [TODO]:对应的这个函数是啥意思？一定要注意一下！
        pass

    def SetValue(self, value: str):
        self.ctrl.delete(0, tk.END)
        self.ctrl.insert(0, value)

    def GetValue(self) -> str:
        return self.ctrl.get()


class Choice(ParamWidgetFrame):
    def __init__(self, parent, choices, tp, title, unit):
        super().__init__(parent)
        self.tp, self.choices = tp, choices
        self.on_check_callback = None

        self.prefix = lab_title = ttk.Label(self, text=title)
        self.prefix.pack(anchor=tk.W)

        self.sel = tk.IntVar()
        self.sel.set(0)
        for i, choice in enumerate(self.choices):
            b = ttk.Radiobutton(self, text=str(choice),
                                variable=self.sel, value=i, command=self.on_choice)
            b.pack(anchor=tk.W)

        self.postfix = lab_unit = ttk.Label(self, text=unit)
        self.postfix.pack(side=tk.LEFT, fill=tk.X, expand=1)

    def f(self, v):
        pass

    def Bind(self, z, f):
        self.f = f

    def on_choice(self, event=None):
        # attention : button command will not transfer any event as args .
        # 注意：按钮本身并不会传递event作为参数，与键鼠的event不同。
        self.f(self)
        print(self.GetValue())
        self.para_changed()
        if callable(self.on_check_callback):
            self.on_check_callback()

    def SetValue(self, x):
        n = self.choices.index(x) if x in self.choices else 0
        self.sel.set(n)

    def GetValue(self):
        return self.choices[self.sel.get()]  # self.tp(self.choices[self.ctrl.GetSelection()])


class AnyType(ParamWidgetFrame):
    def __init__(self, parent, title, types=['Int', 'Float', 'Str']):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(-1, -1),
                          style=wx.TAB_TRAVERSAL)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.prefix = lab_title = wx.StaticText(self, wx.ID_ANY, title,
                                                wx.DefaultPosition, wx.DefaultSize)
        lab_title.Wrap(-1)
        sizer.Add(lab_title, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.txt_value = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.txt_value, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        com_typeChoices = types
        self.postfix = self.com_type = wx.ComboBox(self, wx.ID_ANY, 'Float', wx.DefaultPosition, wx.DefaultSize,
                                                   com_typeChoices, 0)
        sizer.Add(self.com_type, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()

        # Connect Events
        self.txt_value.Bind(wx.EVT_KEY_UP, self.on_text)
        self.com_type.Bind(wx.EVT_COMBOBOX, self.on_type)

    def Bind(self, z, f):
        self.f = f

    def SetValue(self, v):
        self.txt_value.SetValue(str(v))
        if isinstance(v, int):
            self.com_type.Select(0)
        if isinstance(v, float):
            self.com_type.Select(1)
        else:
            self.com_type.Select(2)

    def GetValue(self):
        tp = self.com_type.GetValue()
        sval = wx.TextCtrl.GetValue(self.txt_value)
        if tp == 'Float':
            try:
                num = float(sval)
            except ValueError:
                return None
        if tp == 'Int':
            try:
                num = int(sval)
            except ValueError:
                return None
        if tp == 'Str':
            try:
                num = str(sval)
            except ValueError:
                return None
        return num

    # Virtual event handlers, overide them in your derived class
    def on_text(self, event):
        self.f(self)
        if self.GetValue() == None:
            self.txt_value.SetBackgroundColour((255, 255, 0))
        else:
            self.txt_value.SetBackgroundColour((255, 255, 255))
        self.Refresh()

    def on_type(self, event):
        if self.GetValue() == None:
            self.txt_value.SetBackgroundColour((255, 255, 0))
        else:
            self.txt_value.SetBackgroundColour((255, 255, 255))
        self.Refresh()


class Choices(ParamWidgetFrame):
    def __init__(self, parent, choices, title):
        self.choices = list(choices)
        super().__init__(parent)

        self.prefix = lab_title = ttk.Label(self, text=title)
        self.prefix.pack(anchor=tk.W)

        self.boolVarList = [tk.BooleanVar() for i in range(len(self.choices))]
        # print(self.boolVarList)
        self.on_check_callback = None
        for i, choice in enumerate(self.choices):
            b = ttk.Checkbutton(self, text=str(choice),
                                variable=self.boolVarList[i], command=self.on_check)
            b.pack(anchor=tk.W)

    def Bind(self, z, f):
        self.f = f

    def on_check(self):
        self.para_changed()
        if callable(self.on_check_callback):
            self.on_check_callback()

    def GetValue(self):
        l = []
        for i, bv in enumerate(self.boolVarList):
            if bv.get() == True:
                l.append(self.choices[i])
        return l

    def SetValue(self, value: list):
        print('set value', value)
        for bv in self.boolVarList: bv.set(False)
        for i, v in enumerate(value):
            n = self.choices.index(v) if v in self.choices else -1  # -1 stands for input error
            if n != -1:
                self.boolVarList[n].set(True)
            else:
                warnings.warn('Index item \'%s\' is not in choices list : %s' %
                              (v, repr(self.choices)))


class FloatSlider(ParamWidgetFrame):
    def __init__(self, parent, rang, accury, title, unit=''):
        super().__init__(parent)
        self.accury = accury
        self.on_check_callback = None

        self.lab_title = ttk.Label(self, text=title)
        self.lab_title.pack(anchor=tk.W)

        self.slider = ttk.Scale(self, from_=rang[0], to=rang[1], orient=tk.HORIZONTAL, command=self.on_scroll)
        self.slider.pack(expand=1, fill=tk.X)
        self.spinboxFrame = ttk.Frame(self)

        self.lab_min = ttk.Label(self.spinboxFrame)
        self.lab_min.pack(side=tk.LEFT)

        self.spinvar = tk.StringVar()
        self.spin = tk.Spinbox(self.spinboxFrame, from_=rang[0], to=rang[1], increment=10 ** -accury, format='%10.4f',
                               command=self.on_spin, textvariable=self.spinvar)
        self.spin.bind('<KeyRelease>', self.on_text)

        self.spin.pack(side=tk.LEFT)
        self.spinboxFrame.pack(expand=1, fill=tk.BOTH, pady=(3, 0))

        self.lab_max = ttk.Label(self.spinboxFrame)
        self.lab_max.pack(side=tk.LEFT)

        self.lab_unit = ttk.Label(self.spinboxFrame, text=unit)
        self.lab_unit.pack(side=tk.LEFT)

        self.set_para(rang, accury)

    def Bind(self, z, f):
        self.f = f

    def set_para(self, rang, accury):
        self.min = round(rang[0], accury)
        self.max = round(rang[1], accury)
        self.lab_min.config(text=str(round(rang[0], accury)))
        self.lab_max.config(text=str(round(rang[1], accury)))
        self.accury = accury

    def on_scroll(self, event):
        '''
        只有这个方法会调用回调函数。原因：当用户通过拖动滚动条进行操作的时候，输入的值一定是合理的，无需进行判断；
        当用户通过按spinbox或者是对spinbox输入文本的时候，只有文本符合规定的时候会对slider设置值，此时会调用这个方法。
        这样总能调用到这个回调函数。
        '''
        value = self.slider.get()
        self.spinvar.set(round(value, self.accury))
        self.spin.config(bg='#ffffff')
        self.para_changed()
        if callable(self.on_check_callback):
            self.on_check_callback()

    def on_spin(self):

        self.slider.set(self.spin.get())
        if callable(self.on_check_callback):
            self.on_check_callback()

    def on_text(self, event):
        if self.is_key(event,'dir'):
            return
        if self.GetValue() == None:
            self.spin.config(bg="#ffff00")
        else:
            self.spin.config(bg="#ffffff")
            self.SetValue(self.GetValue())

    def SetValue(self, n):
        self.slider.set(n)
        self.spinvar.set(round(n, self.accury))

    def GetValue(self):
        sval = self.spinvar.get()
        try:
            val = float(sval) if self.accury > 0 else int(float(sval))
            if self.min <= val <= self.max:
                return val
            else:
                return None
        except Exception as e:
            print(e)
            #raise Exception('Invalid sval', sval)


class Label(ParamWidgetFrame):
    def __init__(self, parent, title):
        super().__init__(parent)
        lab_title = ttk.Label(self, text=title)
        lab_title.pack(anchor=tk.W)

    def Bind(self, z, f): pass

    def SetValue(self, v): pass

    def GetValue(self, v): pass


class Check(ParamWidgetFrame):
    def __init__(self, parent, title):
        super().__init__(parent)
        lab_title = ttk.Label(self, text=title)
        lab_title.pack(anchor=tk.W)
        self.on_check_callback = None
        self.variable = tk.BooleanVar()
        checkFrame = ttk.Frame(self)
        check = ttk.Checkbutton(checkFrame, command=self.on_check, variable=self.variable)
        check.pack(side=tk.LEFT)
        checkFrame.pack(expand=True, fill=tk.X)

    def GetValue(self):
        return self.variable.get()

    def SetValue(self, value):
        self.variable.set(value)

    def on_check(self):
        ##        print(self.variable.get())
        ##        print(self.GetValue())
        self.para_changed()
        if callable(self.on_check_callback):
            self.on_check_callback()
        pass

    def Bind(self, z, f): self.f = f


if __name__ == '__main__':
    view = [('lab', 'lab', 'This is a questionnaire'),
            (str, 'name', 'name', 'please'),
            (int, 'age', (0, 150), 0, 'age', 'years old'),
            (float, 'h', (0.3, 250000), 8, 'height', 'm'),
            ('slide', 'w', (1, 150), 0, 'weight', 'kg'),
            (bool, 'sport', 'do you like sport'),
            (list, 'sys', ['Windows', 'Mac', 'Linux'], str, 'favourite', 'system'),
            ('chos', 'lan', ['C/C++', 'Java', 'Python'], 'lanuage you like(multi)'),
            ('color', 'c', 'which', 'you like')]
    root = tk.Tk()

    ##    v=view[3]
    ##    print(v,v[2:])
    ##    nc=NumCtrl(root, *v[2:])
    ##    nc.SetValue(123.456)
    ##    nc.pack(fill=tk.BOTH,expand=True)

    ##    v=view[1]
    ##    tc=TextCtrl(root,*v[2:])
    ##    tc.SetValue('123.456')
    ##    tc.pack(fill=tk.BOTH,expand=True)

    ##    v=view[8]
    ##    cc=ColorCtrl(root,*v[2:])
    ##    cc.pack(fill=tk.BOTH,expand=True)

    ##    v = view[6]
    ##    print(v)
    ##    cc=Choice(root,*v[2:])
    ##    cc.pack(fill=tk.BOTH,expand=True)
    ##    cc.SetValue('Mac')

    v = view[3]
    print(v)
    cc = Check(root, *v[2:])
    cc.pack(fill=tk.BOTH, expand=True)
    cc.SetValue(False)
    ##    cc.SetValue(['Java'])
    ##    cc.SetValue(['C/C++','Python','C--'])

    root.mainloop()
