import tkinter as tk
from .EventBase import EventBase
from .StyleBase import StyleBase

## 单行输入框
class InputBox(tk.Entry, EventBase, StyleBase):
    def __init__(self, master):
        self.varStr = tk.StringVar()
        self.varStr.set("")
        super(InputBox, self).__init__(master, textvariable=self.varStr)
    
    @property
    def text2(self):
        return self.varStr.get()

    @text2.setter
    def text2(self, value):
        self.varStr.set(value)