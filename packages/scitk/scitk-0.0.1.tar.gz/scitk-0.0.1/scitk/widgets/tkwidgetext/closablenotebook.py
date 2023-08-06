import tkinter as tk
from tkinter import ttk

class ClosableNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""
    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True
        self.tabList=[]# 类型为ttk.Frame
        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def get_tab(self,i)->ttk.Frame:
        if not i is None:
            return self.tabList[i]
        else: return self.get_current_tab()
    
    def get_current_tab(self)->ttk.Frame:
        return self.tabList[self.index("current")]
        
    def add_tab(self,tab:ttk.Frame,text:str)->None:
        self.add(tab,text=text)
        self.tabList.append(tab)

    def delete_tab(self,tab_id)->None:
        if type(tab_id)==type(""):
            if tab_id=="current":
                i=self.index("current")
            elif tab_id=='end':
                i=len(self.tabs())-1
            else:
                raise Exception("Invalid tab index:%s"%tab_id)
        else:
            i=tab_id
        self.tabList.pop(i)
        self.forget(tab_id)
        

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index

    def on_close_release(self, event):
        """Called when the button is released over the close button"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))

        if "close" in element and self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
            R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
            d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
            5kEJADs=
            '''),
            tk.PhotoImage("img_closeactive", data='''
            R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
            AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
            '''),
            tk.PhotoImage("img_closepressed", data='''
            R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
            d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
            5kEJADs=
        ''')
    )

        style.element_create("close", "image", "img_close",
                        ("active", "pressed", "!disabled", "img_closepressed"),
                        ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
        ("CustomNotebook.tab", {
            "sticky": "nswe", 
            "children": [
                ("CustomNotebook.padding", {
                    "side": "top", 
                    "sticky": "nswe",
                    "children": [
                        ("CustomNotebook.focus", {
                            "side": "top", 
                            "sticky": "nswe",
                            "children": [
                                ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                            ]
                    })
                ]
            })
        ]
    })
])

