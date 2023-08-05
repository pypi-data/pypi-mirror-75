import tkinter as tk

## ---------------------------------------------------------------------- 颜色属性
class Color:
    White = "white"
    Blue = "blue"
    LightBlue = "light blue"
    Grey = "grey"
    LightGrey = "light grey"
    Black = "black"

## ---------------------------------------------------------------------- 事件名称
class TouchEvent:
    TOUCH_TAP = "<Button-1>"
    DOUBLE_TAP = "<Double-Button-1>"
    RIGHT_TAP = "<Button-3>"

class FocusEvent:
    FOCUS_IN = "<FocusIn>"
    FOCUS_OUT = "<FocusOut>"

class KeyBoardEvent:
    Key = "<Key>"

class Event:
    ITEM_SELECT = "<<ListboxSelect>>"

## ---------------------------------------------------------------------- 事件基础类
class EventBase:
    def addEventListener(self, type:str, cbFn):
        self.bind(type, cbFn)
    
    def removeEventListener(self, type:str):
        self.unbind(type)
    
## ---------------------------------------------------------------------- 样式基础类
class StyleBase:
    # 移除舞台
    def removeSelf(self):
        self.destroy()
    @property
    def x(self):
        return 0 # 暂无~
     
    @x.setter
    def x(self, value):
        self.place(x=value)
    
    @property
    def y(self):
        return 0 # 暂无~
     
    @y.setter
    def y(self, value):
        self.place(y=value)
    
    @property
    def width(self):
        return 0 # 暂无~
     
    @width.setter
    def width(self, value):
        self.place(width=value)
    
    @property
    def height(self):
        return 0 # 暂无~
     
    @height.setter
    def height(self, value):
        self.place(height=value)
    

## ---------------------------------------------------------------------- 封装组件
## ---------------------------------------------------------------------- 封装组件
## ---------------------------------------------------------------------- 封装组件
class Tk(tk.Tk):
    pass

class Panel(tk.Tk):
    def setTitle(self, tit:str):
        self.title(tit)
    
    def setSize(self, weight:int, height:int):
        sizeStr = str(weight) + "x" + str(height)
        self.geometry(sizeStr)
    
    def update(self, cbFn):
        cbFn()
        self.mainloop()

## ---------------------------------------------------------------------- 打开文件
def openFileDialog():
    import tkinter.filedialog as fd
    path = fd.askopenfilename()
    return path

## ---------------------------------------------------------------------- 打开文件夹
def openDirDialog():
    import tkinter.filedialog as fd
    dir = fd.askdirectory()
    return dir

## ---------------------------------------------------------------------- 弹窗
def alert(title:str, content:str):
    import tkinter.messagebox as mb
    mb.showinfo(title, content)

## ---------------------------------------------------------------------- 带输入框的弹窗
def askAlert(title:str, content:str):
    import tkinter.simpledialog as dialog
    answer = dialog.askstring(title, content)
    return answer

## ---------------------------------------------------------------------- 拖拽
## 回调函数中参数为 文件绝对路径
def dragfiles(component, cbFn):
    import windnd
    windnd.hook_dropfiles(component, func=cbFn)

## ---------------------------------------------------------------------- 右键菜单
class Menu(tk.Menu, EventBase, StyleBase):
    def addCommand(self, name:str, cbFn=None):
        self.add_command(label=name, command=cbFn)
    
    def setPos(self, x:int, y:int):
        self.post(x, y)

## ---------------------------------------------------------------------- 列表
class SimpleList(tk.Listbox, EventBase, StyleBase):
    def __init__(self, master=None):
        self.dataArray = []
        # exportselection 防止失去焦点时，选中状态变为未选中
        # activestyle 去掉选中时的下划线效果
        super(SimpleList, self).__init__(master, activestyle="none", exportselection=False)
        self.addEventListener(FocusEvent.FOCUS_IN, self.__OnFocusIn)

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

## ---------------------------------------------------------------------- 图片(待完成)
class Image(tk.Label, EventBase, StyleBase):
    # def __init__(self, master, source:str=None):
    #     if source is not None:
    #         # img = Pmg.open(source)
    #         self.img = tk.PhotoImage(file=source)
    #         super(Image, self).__init__(master, image=self.img)
    #     else:
    #         super(Image, self).__init__(master)

    # @property
    # def source(self):
    #     return ""

    # @source.setter
    # def source(self, value):
    #     self.__init__(self, value)
    pass

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

## ---------------------------------------------------------------------- 单行输入框
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

## ---------------------------------------------------------------------- Button
class Button(tk.Button, EventBase, StyleBase):
    @property
    def label(self):
        return self["text"]

    @label.setter
    def label(self, value):
        self["text"] = value

## ---------------------------------------------------------------------- Label
class Label(tk.Label, EventBase, StyleBase):
    @property
    def text2(self):
        return self["text"]

    @text2.setter
    def text2(self, value):
        self["text"] = value

## ---------------------------------------------------------------------- 单选
class RadioButton(tk.Radiobutton, EventBase, StyleBase):
    pass
    


