import tkinter as tk
from .EventBase import EventBase
from .StyleBase import StyleBase

## ---------------------------------------------------------------------- 右键菜单
class Menu(tk.Menu, EventBase, StyleBase):
    def addCommand(self, name:str, cbFn=None):
        self.add_command(label=name, command=cbFn)
    
    def setPos(self, x:int, y:int):
        self.post(x, y)