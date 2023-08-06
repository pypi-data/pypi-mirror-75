import tkinter as tk
from .EventBase import EventBase
from .StyleBase import StyleBase

class Panel(tk.Tk, EventBase, StyleBase):
    def setTitle(self, tit:str):
        self.title(tit)
    
    def setSize(self, weight:int, height:int):
        sizeStr = str(weight) + "x" + str(height)
        self.geometry(sizeStr)
    
    def update(self, cbFn):
        cbFn()
        self.mainloop()
    
    ## ---------------------------------------------------------------------- 点击右上角最小化按钮
    def setMinBtnCB(self, cbFn):
        self.protocol("WM_MIN_WINDOW", cbFn)
    
    ## ---------------------------------------------------------------------- 点击右上角关闭按钮
    def setCloseBtnCB(self, cbFn):
        self.protocol("WM_DELETE_WINDOW", cbFn)
    
    ## ---------------------------------------------------------------------- 设置窗体是否可拉伸
    def setResizeAble(self, x:bool, y:bool):
        self.resizable(x, y)
    
    ## ---------------------------------------------------------------------- 添加全局键盘事件
    def addGlobalKeyEvent(self, key:tuple, cbFn):
        import system_hotkey as hotkey
        hk = hotkey.SystemHotkey()
        hk.register(key, callback = cbFn)
    
    ## ---------------------------------------------------------------------- 移除全局键盘事件
    def removeGlobalKeyEvent(self, key:tuple, cbFn):
        import system_hotkey as hotkey
        hk = hotkey.SystemHotkey()
        hk.unregister(key)
    
    