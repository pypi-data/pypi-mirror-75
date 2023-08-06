import tkinter as tk
from tkinter import ttk
import platform
from scitk.widgets.normal import *
##from .histpanel import HistPanel

widgets = { 'ctrl':None, 'slide':FloatSlider, int:NumCtrl, 'path':PathCtrl,
            float:NumCtrl, 'lab':Label, bool:Check, str:TextCtrl, list:Choice,
            'color':ColorCtrl, 'any':AnyType, 'chos':Choices}# 'hist':HistPanel}

def add_widget(key, value): widgets[key] = value

class ParaDialogFrame (ttk.Frame):
    def __init__( self, parent, title):
        super().__init__ (parent)
        self.lst = ttk.Frame(self)#wx.BoxSizer( wx.VERTICAL )
        self.lst.pack(expand = 1, fill=tk.BOTH)
        self.tus = []
        self.on_ok = self.on_cancel = self.on_help = None
        
        self.handle = print
        self.ctrl_dic = {}

    def commit(self, state):
        self.destroy()
        if state=='ok' and self.on_ok:self.on_ok()
        if state=='cancel' and self.on_cancel:self.on_cancel()

    def add_confirm(self, modal):
        frame = ttk.Frame(self)
        frame.pack(fill= tk.BOTH, expand = True)
        return
            
    def init_view(self, items, para, preview=False, modal = True):
        self.para, self.modal = para, modal
        for item in items:
            self.add_ctrl_(widgets[item[0]], item[1], item[2:])
        if preview:self.add_ctrl_(Check, 'preview', ('preview',))
        self.reset(para)
        self.add_confirm(modal)
        self.pack()
        print('bind close')
    
    
    def OnDestroy( self, event ):
        self.set_handle(None)
        self.on_cancel = self.on_ok = self.on_help = None
        del self.ctrl_dic

    def parse(self, para) :
        self.add_ctrl_(widgets[para[0]], *para[1:])

    def add_ctrl_(self, Ctrl, key, p):
        ctrl = Ctrl(self.lst, *p)
        if not p[0] is None: 
            self.ctrl_dic[key] = ctrl
        if hasattr(ctrl, 'ctrl'):
            pass
            ctrl.ctrl.bind('<KeyRelease>',lambda e: self.para_changed(e,ctrl), add = '+')
            ctrl.ctrl.bind('<Button>',lambda e: self.para_changed(e,ctrl), add = '+')
        if hasattr(ctrl,'on_check_callback'): # 因为事件绑定实在是不怎么样。event是直接留了一个字符串进去。
            ctrl.on_check_callback  = lambda : self.para_changed('button click',ctrl)
        pre = ctrl.prefix if hasattr(ctrl, 'prefix') else None
        post = ctrl.postfix if hasattr(ctrl, 'postfix') else None
        self.tus.append((pre, post))
        ctrl.pack(expand = True, fill=tk.X)        

##    def pack(self):
##        '''
##        这个函数是干什么的？
##        '''
##        return 
##        mint, minu = [], []
##        for t,u in self.tus:
##            if not t is None: mint.append(t.GetSize()[0])
##            if not u is None:minu.append(u.GetSize()[0])
##        for t,u in self.tus:
##            if not t is None:t.SetInitialSize((max(mint),-1))
##            if not u is None:u.SetInitialSize((max(minu),-1))

    def para_check(self, para, key):pass

    def para_changed(self,event, obj):
        key = ''
        para = self.para
        for p in self.ctrl_dic:
            if p in para:
                para[p] = self.ctrl_dic[p].GetValue()
            if self.ctrl_dic[p] == obj: key = p

        sta = sum([i is None for i in list(para.values())])==0

        if not sta: return
        self.para_check(para, key)
        if 'preview' not in self.ctrl_dic:return
        if not self.ctrl_dic['preview'].GetValue():
            if key=='preview' and self.on_cancel != None: 
                return self.on_cancel()
            else: return
        self.handle(para)

    def reset(self, para=None):
        if para!=None:self.para = para
        for p in list(self.para.keys()):
            if p in self.ctrl_dic:
                self.ctrl_dic[p].SetValue(self.para[p])

    def get_para(self): return self.para

    def Bind(self, tag, f):
        if tag == 'parameter': self.handle = f if not f is None else print
        if tag == 'commit': self.on_ok = f
        if tag == 'cancel': self.on_cancel = f

    def show(self):
        if self.modal: 
            status =  self.ShowModal() == 5100
            self.Destroy()
            return status
        else: self.Show()

    def __del__( self ):
        print('panel config deleted!')


class ParaDialog (tk.Toplevel):
    def __init__( self, parent, title):
        super().__init__ (parent)
        self.lst = ttk.Frame(self)#wx.BoxSizer( wx.VERTICAL )
        self.lst.pack(expand = 1, fill=tk.BOTH)
        self.tus = []
        self.on_ok = self.on_cancel = self.on_help = None
        
        self.handle = print
        self.ctrl_dic = {}

    def commit(self, state):
        self.destroy()
        if state=='ok' and self.on_ok:self.on_ok()
        if state=='cancel' and self.on_cancel:self.on_cancel()

    def add_confirm(self, modal):
        frame = ttk.Frame(self)
        frame.pack(fill= tk.BOTH, expand = True)
        self.btn_ok = tk.Button( frame, text =  'OK', command = self.on_ok)
        self.btn_ok.pack(side = tk.LEFT)

        self.btn_cancel = tk.Button( frame, text = 'Cancel')
        self.btn_cancel.pack(side = tk.LEFT)

        self.btn_help = tk.Button( self, text =  'Help')
        self.btn_help.pack(side = tk.LEFT)
        
        self.btn_help.config(command =  lambda : self.on_help and self.on_help())
        if not modal:
            self.btn_ok.config( command =  lambda :self.commit('ok'))
            self.btn_cancel.config( command = lambda :self.commit('cancel'))
        self.on_ok = lambda:print(self.para)
            
    def init_view(self, items, para, preview=False, modal = True):
        self.para, self.modal = para, modal
        for item in items:
            self.add_ctrl_(widgets[item[0]], item[1], item[2:])
        if preview:self.add_ctrl_(Check, 'preview', ('preview',))
        self.reset(para)
        self.add_confirm(modal)
        self.pack()
        print('bind close')
    
    
    def OnDestroy( self, event ):
        self.set_handle(None)
        self.on_cancel = self.on_ok = self.on_help = None
        del self.ctrl_dic

    def parse(self, para) :
        self.add_ctrl_(widgets[para[0]], *para[1:])

    def add_ctrl_(self, Ctrl, key, p):
        ctrl = Ctrl(self.lst, *p)
        if not p[0] is None: 
            self.ctrl_dic[key] = ctrl
        if hasattr(ctrl, 'ctrl'):
            ctrl.ctrl.bind('<KeyRelease>',lambda e: self.para_changed(e,ctrl), add = '+')
            ctrl.ctrl.bind('<Button>',lambda e: self.para_changed(e,ctrl), add = '+')
        if hasattr(ctrl,'on_check_callback'): # 因为事件绑定实在是不怎么样。event是直接留了一个字符串进去。
            ctrl.on_check_callback  = lambda : self.para_changed('button click',ctrl)
        pre = ctrl.prefix if hasattr(ctrl, 'prefix') else None
        post = ctrl.postfix if hasattr(ctrl, 'postfix') else None
        self.tus.append((pre, post))
        ctrl.pack(expand = True, fill=tk.X)        

    def pack(self):
        '''
        这个函数是干什么的？
        '''
        return 
        mint, minu = [], []
        for t,u in self.tus:
            if not t is None: mint.append(t.GetSize()[0])
            if not u is None:minu.append(u.GetSize()[0])
        for t,u in self.tus:
            if not t is None:t.SetInitialSize((max(mint),-1))
            if not u is None:u.SetInitialSize((max(minu),-1))

    def para_check(self, para, key):pass

    def para_changed(self,event, obj):
        key = ''
        para = self.para
        for p in self.ctrl_dic:
            if p in para:
                para[p] = self.ctrl_dic[p].GetValue()
            if self.ctrl_dic[p] == obj: key = p

        sta = sum([i is None for i in list(para.values())])==0

        if not sta: return
        self.para_check(para, key)
        if 'preview' not in self.ctrl_dic:return
        if not self.ctrl_dic['preview'].GetValue():
            if key=='preview' and self.on_cancel != None: 
                return self.on_cancel()
            else: return
        self.handle(para)

    def reset(self, para=None):
        if para!=None:self.para = para
        for p in list(self.para.keys()):
            if p in self.ctrl_dic:
                self.ctrl_dic[p].SetValue(self.para[p])

    def get_para(self): return self.para

    def Bind(self, tag, f):
        if tag == 'parameter': self.handle = f if not f is None else print
        if tag == 'commit': self.on_ok = f
        if tag == 'cancel': self.on_cancel = f

    def show(self):
        if self.modal: 
            status =  self.ShowModal() == 5100
            self.Destroy()
            return status
        else: self.Show()

    def __del__( self ):
        print('panel config deleted!')

def get_para(para, view, title='Parameter', parent=None):
    pd = ParaDialog(parent, title)
    pd.init_view(view, para)
    pd.pack()
    rst = pd.ShowModal()
    pd.Destroy()
    return rst == 5100

if __name__ == '__main__':
    para = {'name':'yxdragon', 'age':10, 'h':1.72, 'w':70, 'sport':True, 'sys':'Mac', 'lan':['C/C++', 'Python'], 'c':(255,0,0)} 

    view = [('lab', 'lab', 'This is a questionnaire'),
            (str, 'name', 'name', 'please'), 
            (int, 'age', (0,150), 0, 'age', 'years old'),
            (float, 'h', (0.3, 2.5), 2, 'height', 'm'),
            ('slide', 'w', (1, 150), 0, 'weight','kg'),
            (bool, 'sport', 'do you like sport'),
            (list, 'sys', ['Windows','Mac','Linux'], str, 'favourite', 'system'),
            ('chos', 'lan', ['C/C++','Java','Python'], 'lanuage you like(multi)'),
            ('color', 'c', 'which', 'you like')]

    app = tk.Tk()
    pd = ParaDialog(None, 'Test')
    pd.init_view(view, para, preview=True, modal=False)
    
    print(para)
    app.mainloop()
