import tkinter as tk
from .EventBase import EventBase
from .StyleBase import StyleBase

## ---------------------------------------------------------------------- 单选
class RadioButton(tk.Radiobutton, EventBase, StyleBase):
    pass