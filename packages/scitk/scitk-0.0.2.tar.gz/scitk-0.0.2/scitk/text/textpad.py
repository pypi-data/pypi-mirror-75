import tkinter as tk
from tkinter import ttk
from tkinter import messagebox,filedialog
import os
from scitk.widgets.tkwidgetext.closablenotebook import ClosableNotebook
class TextPad(ttk.Frame):
    def __init__(self, parent, cont='', title='no name'):
        super().__init__(parent)
        #self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
        self.title = title
        self.savePath=''
        self.parent=parent
        
        self.text=tk.Text(self,undo=True)
        self.text.insert('current',cont)
        self.text.pack()
        self.notebook=None
        self.text.bind('<Button-3>',self.OnRClick)
        
        menus = [
                ## File 
                ('File(&F)',[('Open', self.OnOpen),
                                   ('Save', self.OnSave),
                                  ('Save as', self.OnSaveAs)
                                   ]),
                ## Edit 
                ('Edit(&E)', [ ('Undo', self.OnUndo),
                             ('Redo', self.OnRedo),
                             ('Cut', self.OnCut),
                             ('Copy', self.OnCopy),
                             ('Paste', self.OnPaste),
                             ('All', self.OnSelectAll)
                             ]),               
                ## Help 
                ('Help(&H)', [('About', self.OnAbout)])
        ]
        
        ### Bind menus with the corresponding events 
        self.popupMenu=tk.Menu()
        for menuTup in menus:
            parent=menuTup[0]
            for subcmd in menuTup[1]:
                self.popupMenu.add_command(label=subcmd[0], command=subcmd[1])
            self.popupMenu.add_separator()

    def OnOpen(self):
        filename= filedialog.askopenfilename(title='Select file to open',
                                            filetypes=[('Markdown', '*.md'), ('All Files', '*')]) 
        
        if os.path.isfile(filename):
            with open(filename) as f:
                self.text.delete('0.0',tk.END)
                self.text.insert('0.0',f.read())
            self.savePath=filename
            self.notebook.on_save_path_changed()


    def OnSaveAs(self):
        path=filedialog.asksaveasfilename(title='Choose where to save', defaultextension=".md") 
        if path:
           
            self.savePath=path
            self.notebook.on_save_path_changed()
            with open(path,'w') as f:
                f.write(self.text.get(1.0,tk.END))
                f.close()


    def OnSave(self):
        print(self.savePath,'save')
        if not os.path.isfile(self.savePath):
            self.OnSaveAs()
        else:
            with open(self.savePath,'w' ) as f:
                f.write(self.text.get(1.0,tk.END))

    def OnAbout(self,event):
        pass
        #wx.MessageBox('Text Log Window!','ImagePy',wx.OK)

    def OnRClick(self,event):
        self.popupMenu.tk_popup(event.x_root, event.y_root)

    def OnUndo(self): self.text.edit_undo()

    def OnRedo(self): self.text.edit_redo()

    def OnCut(self):self.text.event_generate("<<Cut>>")

    def OnCopy(self): self.text.event_generate("<<Copy>>")

    def OnPaste(self): self.text.event_generate("<<Paste>>")

    def OnSelectAll(self): self.text.tag_add(tk.SEL, "1.0", tk.END)
        
    def append(self, cont:str):
        self.text.insert("insert",cont)

class TextFrame(ttk.Frame):    
    def __init__(self, parent, title='no name', cont=''):
        super().__init__(parent)
        self.title = title
        self.textpad = TextPad(self, cont, title)
        self.append = self.textpad.append
        self.pack()
        
        ### Create menus (name:event) k-v pairs 
        menus = [
                ## File 
                ('File(&F)',[('Open', self.textpad.OnOpen),
                             ('Save', self.textpad.OnSave),
                             ('Save as', self.textpad.OnSaveAs),
                             ('-'),
                             ('Exit', self.OnClose)
                             ]),
                ## Edit 
                ('Edit(&E)', [ ('Undo', self.textpad.OnUndo),
                             ('Redo', self.textpad.OnRedo),
                             ('-'),
                             ('Cut', self.textpad.OnCut),
                             ('Copy', self.textpad.OnCopy),
                             ('Paste', self.textpad.OnPaste),
                             ('-'),
                             ('All', self.textpad.OnSelectAll)
                             ]),               
                ## Help 
                ('Help(&H)', [('About', self.textpad.OnAbout)])
        ]
        
        ### Bind menus with the corresponding events 
        self.popupMenu=tk.Menu()
        for menuTup in menus:
            parent=menuTup[0]
            for subcmd in menuTup[1]:
                self.popupMenu.add_command(label=subcmd[0], command=subcmd[1])
            self.popupMenu.add_separator()
##        for menu in menus:
##            m = wx.Menu()
##            for item in menu[1]:
##                if item[0]=='-':
##                    m.AppendSeparator()
##                else:
##                    i = m.Append(-1, item[0])
##                    self.Bind(wx.EVT_MENU,item[1], i)
##            self.menuBar.Append(m,menu[0])
##        self.SetMenuBar(self.menuBar) 
##        self.Bind(wx.EVT_CLOSE, self.OnClosing)

    def OnClose(self,event):
        self.Destroy()
        
    def OnClosing(self, event):
        event.Skip()
        
class TextNoteBook(ClosableNotebook):
    def __init__(self, parent):
        super().__init__(parent)
        self.bind("<<SavePathChanged>>",self.on_save_path_changed,add='+')
        
##        self.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_valid) 
##        self.Bind( wx.lib.agw.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)
##        self.Bind( wx.EVT_IDLE, self.on_idle)
##        self.SetArtProvider(aui.AuiSimpleTabArt())
        
    def on_idle(self, event):
        for i in range(self.GetPageCount()):
            title = self.GetPage(i).title
            if self.GetPageText(i) != title:
                self.SetPageText(i, title)

    def textpad(self, i=None):
        self.get_tab(i)
        
    def set_background(self, img):
        self.GetAuiManager().SetArtProvider(ImgArtProvider(img))

    def add_notepad(self, textpad=None):
        if textpad==None:
            textpad=TextPad(self)
            self.add_tab(textpad,textpad.title)
        else:
            self.add_tab(textpad,textpad.title)
        print(textpad)
        textpad.notebook=self
        return textpad

    def set_title(self, panel, title):
        self.SetPageText(self.GetPageIndex(panel), title)

    def on_valid(self, event): pass

    def on_close(self, event): pass
    
    def on_save_path_changed(self):
        for index in range(len(self.tabs())):
            tabText=self.tabList[index].savePath
            self.tab(index,text=tabText)

class TextNoteFrame(ttk.Frame):
    def __init__(self,parent, title='TextPadBookFrame'):
        super().__init__ (parent)
        
        self.notebook = TextNoteBook(parent)
        self.notebook.pack(expand=True,fill=tk.BOTH) 
        self.textpad = self.notebook.textpad
        self.add_notepad=self.notebook.add_notepad
        
        ### Create menus (name:event) k-v pairs 
        menus = [
                ## File 
                ('File(&F)',[('Open', lambda e: self.textpad().OnOpen(e)),
                             ('Save', lambda e: self.textpad().OnSave(e)),
                             ('Save as', lambda e: self.textpad().OnSaveAs(e)),
                             ('-'),
                             ('Exit', self.OnClose)
                             ]),
                ## Edit 
                ('Edit(&E)', [ ('Undo', lambda e: self.textpad().OnUndo(e)),
                             ('Redo', lambda e: self.textpad().OnRedo(e)),
                             ('-'),
                             ('Cut', lambda e: self.textpad().OnCut(e)),
                             ('Copy', lambda e: self.textpad().OnCopy(e)),
                             ('Paste', lambda e: self.textpad().OnPaste(e)),
                             ('-'),
                             ('All', lambda e: self.textpad().OnSelectAll(e))
                             ]),               
                ## Help 
                ('Help(&H)', [('About', lambda e: self.textpad().OnAbout(e))])
        ]
        
        ### Bind menus with the corresponding events 
        self.menuBar=tk.Menu(self)
        for menu in menus:
            self.menuBar.add_command(label=menu[0],command=print)
        parent.config(menu=self.menuBar)
        return
        if i==1:
            for item in menu[1]:
                if item[0]=='-':
                    m.AppendSeparator()
                else:
                    i = m.Append(-1, item[0])
                    self.Bind(wx.EVT_MENU,item[1], i)
            self.menuBar.Append(m,menu[0])
        self.SetMenuBar(self.menuBar) 
        self.Bind(wx.EVT_CLOSE, self.OnClosing)

    def OnClose(self,event):
        self.Destroy()
        
    def OnClosing(self, event):
        event.Skip()
    
if __name__ == '__main__':
    app = tk.Tk()

    npbf = TextNoteFrame(app)
    note1 = npbf.add_notepad()
    note1.append('abc')
    note2 = npbf.add_notepad()
    note2.append('def')
    npbf.pack()
    app.mainloop()
    

