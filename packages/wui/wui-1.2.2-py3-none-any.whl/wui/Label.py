import tkinter as tk
from .EventBase import EventBase
from .StyleBase import StyleBase

class Label(tk.Label, EventBase, StyleBase):
    @property
    def text2(self):
        return self["text"]

    @text2.setter
    def text2(self, value):
        self["text"] = value