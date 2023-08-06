from tkinter import ttk
import tkinter as tk
from scitk.widgets.tkwidgetext.choicebook import BaseChoiceBook
class ChoiceBook(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
    def add_wgts(self, name, wgts):
        book = BaseChoiceBook(self)
        for name, wgt in wgts:
            book.add(wgt(book),name)
        book.pack(expand = 1, fill=tk.BOTH )

    def load(self, data):
        for name, wgts in data[1]:
            self.add_wgts(name, wgts)

class TestFrame(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.b=ttk.Button(self,text='哈哈哈哈')
        self.b.pack()
if __name__ == '__main__':
    app = tk.Tk()
    frame = ttk.Frame(None)
    book = ChoiceBook(frame)
    book.load(('widgets', [('panels', [('A', TestFrame), ('B', ttk.Frame)]),
        ('panels2', [('A', ttk.Frame), ('B', ttk.Frame)])]))
    book.pack(expand=True,fill=tk.BOTH)
    frame.pack(expand=True, fill=tk.BOTH)
    app.mainloop()
