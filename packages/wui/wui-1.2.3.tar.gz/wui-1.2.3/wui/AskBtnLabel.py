from .Label import Label
from .Group import Group
from .Button import Button
from .EventBase import TouchEvent
from .Dialog import openFileDialog
from .Dialog import openDirDialog

class AskBtnLabelComType:
    AskFile:1
    AskDir:2

class AskBtnLabelCom(Group):
    def __init__(self, master):
        super(Group, self).__init__(master)
        self.initView()
        self.initData()
    
    def initView(self):
        self.group = Group(self)
        self.group.x = 0
        self.group.y = 0

        self.btn1 = Button(self)
        self.btn1.x = 0
        self.btn1.y = 0
        self.btn1.label = "点我选择文件"

        self.lb1 = Label(self)
        self.lb1.x = 90
        self.lb1.y = 3
        self.lb1.text2 = "文件地址"

        self.width = 400
        self.height = 30
    
    def initData(self):
        pass
    
    def setType(self, type:int):
        if type == 1:
            self.btn1.label = "点我选择文件"
            self.btn1.addEventListener(TouchEvent.TOUCH_TAP, self.OnBtn1Tap)
        else:
            self.btn1.label = "选择保存地址"
            self.btn1.addEventListener(TouchEvent.TOUCH_TAP, self.OnBtn2Tap)
    
    @property
    def path(self):
        return self.lb1.text2
     
    @path.setter
    def path(self, value):
        self.lb1.text2 = dir

    def OnBtn1Tap(self, e):
        path = openFileDialog()
        self.path = path
    
    def OnBtn2Tap(self, e):
        dir = openDirDialog()
        self.path = dir