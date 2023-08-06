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