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