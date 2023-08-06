import tkinter
 
win = tkinter.Tk()
win.title("Kahn Software v1")    # #窗口标题
win.geometry("500x300+200+20")   # #窗口位置500后面是字母x


frm = tkinter.Frame(win)             # #创建一个frame控件
frm.place(x=0, y=0)

tkinter.Label(frm, text="左上", bg="pink").pack(side=tkinter.TOP)
tkinter.Label(frm, text="左下", bg="green").pack(side=tkinter.TOP)
 
win.mainloop()