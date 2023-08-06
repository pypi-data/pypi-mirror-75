import tkinter as tk
from .EventBase import EventBase
from .StyleBase import StyleBase

## ---------------------------------------------------------------------- 列表
class SimpleList(tk.Listbox, EventBase, StyleBase):
    def __init__(self, master=None):
        self.dataArray = []
        # exportselection 防止失去焦点时，选中状态变为未选中
        # activestyle 去掉选中时的下划线效果
        super(SimpleList, self).__init__(master, activestyle="none", exportselection=False)
        # self.addEventListener(FocusEvent.FOCUS_IN, self.__OnFocusIn)

    @property
    def selectIndex(self):
        return self.curselection()
    
    @selectIndex.setter
    def selectIndex(self, valueArray):
        for index in valueArray:
            self.select_set(index)

    @property
    def dataProvider(self):
        return self.dataArray

    @dataProvider.setter
    def dataProvider(self, valueArray):
        self.dataArray = valueArray
        self.delete(0, tk.END)
        for item in self.dataArray:
            self.insert(tk.END, item)
    
    def addItem(self, item:str):
        self.dataArray.append(item)
        self.insert(tk.END, item)
    
    def removeItem(self, item:str):
        index = 0
        for item2 in self.dataArray:
            if item2 is item:
                break
            index += 1
        self.delete(index, index)
    
    def removeIndex(self, index):
        self.delete(index, index)
    
    def addItemIndex(self, index:int, item:str):
        self.insert(index, item)

    def __OnFocusIn(self, e):
        self.activate = self.selectIndex