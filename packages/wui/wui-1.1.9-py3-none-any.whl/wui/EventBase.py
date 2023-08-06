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
        self.bind(type, cbFn)
    
    def removeEventListener(self, type:str):
        self.unbind(type)