import tkinter as tk
from .EventBase import EventBase
from .StyleBase import StyleBase

## ---------------------------------------------------------------------- 多行输入框
class InputArea(tk.Text, EventBase, StyleBase):
    def __init__(self, master=None):
        super(InputArea, self).__init__(master)
        self.place(x=0, y=0)
    
    @property
    def text2(self):
        return self.get("0.0", tk.END).strip()

    @text2.setter
    def text2(self, value):
        self.delete("1.0", tk.END)
        self.insert(1.0, value)
    
    def addText(self, value:str):
        self.insert(tk.END, value)
    
    @property
    def editable(self):
        return self["state"] == "normal"

    @editable.setter
    def editable(self, value:bool):
        if value is True:
            self["state"] = "normal"
        else:
            self["state"] = "disabled"
    
    @property
    def bg(self):
        return self["bg"]

    @bg.setter
    def bg(self, value:str):
        self["bg"] = value
    
    @property
    def selectBg(self):
        return self["selectbackground"]

    @selectBg.setter
    def selectBg(self, value:str):
        self["selectbackground"] = value
    
    @property
    def selectFg(self):
        return self["selectforeground"]

    @selectFg.setter
    def selectFg(self, value:str):
        self["selectforeground"] = value