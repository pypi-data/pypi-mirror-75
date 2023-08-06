import tkinter as tk

class Panel(tk.Tk):
    def setTitle(self, tit:str):
        self.title(tit)
    
    def setSize(self, weight:int, height:int):
        sizeStr = str(weight) + "x" + str(height)
        self.geometry(sizeStr)
    
    def update(self, cbFn):
        cbFn()
        self.mainloop()