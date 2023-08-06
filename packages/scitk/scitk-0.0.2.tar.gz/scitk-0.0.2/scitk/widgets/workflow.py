import tkinter as tk
from tkinter import ttk
from scitk.widgets.tkwidgetext.scrolledcanvas import ScrolledCanvas
def parse(cont):
    ls = cont.split('\n')
    workflow = {'title':ls[0], 'chapter':[]}
    for line in ls[2:]:
        line = line.strip()
        if line == '':continue
        if line.startswith('## '):
            chapter = {'title':line[3:], 'section':[]}
            workflow['chapter'].append(chapter)
        elif line[1:3] == '. ':
            section = {'title':line[3:]}
        else:
            section['hint'] = line
            chapter['section'].append(section)
    print(workflow)
    return workflow

class WorkFlowPanel (ttk.Frame):
    def __init__( self, parent ):
        super().__init__ (parent)
        self.app, self.f = parent, print

    def SetValue(self, cont):
        self.workflow, self.cont = parse(cont), cont
        self.workflow_canvas = ScrolledCanvas(self, orient = 'horizontal')
        self.scr_workflow = self.workflow_canvas.scrollable_frame
        
        self.workflow_canvas .pack(side=tk.LEFT, expand = True, fill = tk.BOTH)
        
        for chapter in self.workflow['chapter']:
            self.pan_chapter = ttk.Frame(self.scr_workflow)
            
            
            b=tk.Button(self.pan_chapter,text='ddddddddddd')
            b.pack()

            self.pan_chapter.pack(expand=True,fill=tk.Y,side=tk.LEFT) 
            
            self.lab_chapter = ttk.Label(self.pan_chapter, text = chapter['title'])
            self.lab_chapter.pack()
            
            for section in chapter['section']:
                btn = ttk.Button( self.pan_chapter, text= section['title'])
                btn.pack()
                btn.config(command = lambda x=section['title']: self.f(x))
                btn.bind( '<Motion>', lambda e, info=section['hint']: self.set_info(info))# show information when mouse is moving
           
            self.btn_snap = ttk.Label( self.pan_chapter, text= u" Snap ")
            self.btn_snap.pack()
            
            self.btn_load = ttk.Button( self.pan_chapter, text = u" Load ")
            self.btn_load.pack()
            
            self.btn_step = ttk.Button( self.pan_chapter, text= u" >> ")
            self.btn_step.pack()

        self.btn_help = ttk.Button( self, text = u" Click For Detail Document ", 
                                   command=lambda event='e'  : self.on_help(event)) # 'e'  is just an non_sense argument for occupy args position.
        self.btn_help.pack(side=tk.LEFT)
        
        self.txt_info = tk.Text( self )
        self.txt_info.pack(side=tk.LEFT)

    def set_info(self, info):
        self.txt_info.delete('0.0',tk.END)
        self.txt_info.insert('0.0',info)
    
    def f(self,event):
        self.on_spn(event)
    def on_spn(self, event):
        v = self.spn_scroll.GetValue()
        self.scr_workflow.Scroll(v, 0)
        self.spn_scroll.SetValue(self.scr_workflow.GetViewStart()[0])

    def Bind(self, event, f=print): self.f = f

    def on_help(self, event):
        self.app.show_md(self.cont, self.workflow['title'])

if __name__ == '__main__':

    cont = '''Title
=====
## Chapter1
1. Section1
some coment for section1 ...
2. Section2
some coment for section2 ...
## Chapter2
1. Section1
some coment for section1 ...
2. Section2
some coment for section2 ...
## Chapter2
1. Section1
some coment for section1 ...
2. Section2
some coment for section2 ...
## Chapter2
1. Section1
some coment for section1 ...
2. Section2
some coment for section2 ...
## Chapter2
1. Section1
some coment for section1 ...
2. Section2
some coment for section2 ...
## Chapter2
1. Section1
some coment for section1 ...
2. Section2
some coment for section2 ...
## Chapter2
1. Section1
some coment for section1 ...
2. Section2
some coment for section2 ...
## Chapter2
1. Section1
some coment for section1 ...
2. Section2
some coment for section2 ...
'''

    app = tk.Tk()
    frame = ttk.Frame(app)
##    sizer = wx.BoxSizer(wx.VERTICAL)
    wf = WorkFlowPanel(app)
    wf.SetValue(cont*1)
    wf.pack(expand=1,fill=tk.X)
    frame.pack(expand=1,fill=tk.BOTH)
    btn2 = ttk.Button(frame, text='sssssssssss')
    btn2.pack(expand=1 , fill=tk.BOTH)
    app.mainloop()
