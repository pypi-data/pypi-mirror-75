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
    
class EventBase:
    def addEventListener(self, type:str, cbFn):
        self.bind(type, cbFn) # 也可以用self.bind，但在vs中会报错，但不影响使用，只是有点烦
    
    def removeEventListener(self, type:str):
        self.unbind(type)

## ---------------------------------------------------------------------- 注册全局键盘事件(即使窗体最小化也会检测到)
class GlobalKey:
    Ctrl = "control"
    One = "1"
    Two = "2"
    Three = "3"
    Four = "4"
    Five = "5"
    Six = "6"
    Seven = "7"
    Eight = "8"
    Nine = "9"
    Zero = 0